# coding: utf-8

import json

class Flow():
	def __init__(self):
		config = """{
			router-id: '10.0.0.100',
			functions [
				{
					id: 101,
					target: '65000:101',
					mark: 1,
					class: 0
				},
				{
					id: 102,
					target: '65000:102',
					mark: 2,
					class: 0
				},
				{
					id: 501,
					target: '65000:501',
					mark: 10,
					class: 1
				},
				{
					id: 502,
					target: '65000:502',
					mark: 11,
					class: 1
				},
				{
					id: 110,
					target: '65000:110',
					mark: 3,
					class: 0
				}
			],
			classes [
				{
					id: 1000,
					target: '65000:1000'
				},
				{
					id: 1001,
					target: '65000:1001'
				}
			]
		}"""
		self.data = json.loads(self.config)

	def flow_generate(self, functions, cmd, prefix):
		result = []

		for i, func_req in enumerate(functions):
			func = {}
			for func_data in self.data['functions']:
				if func_req['id'] == func_data['id']:
					func = func_data

			func_next = {}
			if i < len(functions):
				func_req_next = functions[i + 1]
				for func_data in self.data['functions']:
					if func_req_next['id'] == func_data['id']:
						func_next = func_data
			else:
				func_next['id'] = 100
				func_next['target'] = '65000:100'
				func_next['mark'] = 0

			result.append(self.flow_topside(cmd, func, func_next, prefix))
			result.append(self.flow_btmside(cmd, func, func_next, prefix))

		return result

	def flow_topside(self, cmd, func, func_next, prefix):
		result = []
		result.append(flow_topside_egress(cmd, func, func_next, prefix))
		result.append(flow_topside_ingress(cmd, func, func_next, prefix))
		return result

	def flow_topside_egress(self, cmd, func, func_next, prefix):
		route = {}
		fc = self.data['classes'][func['class']]

		route['rd'] = self.data['router-id'] + ':' + func['id']
		route['match'] = {}
		route['match']['source'] = prefix
		route['then'] = {}
		route['then']['extended-community'] = 'target:' + func['target']
		route['then']['mark'] = func_next['mark']
		route['then']['redirect'] = 'target:' + fc['target']

		result = cmd + ' flow route ' + json.dumps(route)
		return result

	def flow_topside_ingress(self, cmd, func, func_next, prefix):
		route = {}
		fc = self.data['classes'][func['class']]

		route['rd'] = self.data['router-id'] + ':' + fc['id']
		route['match'] = {}
		route['match']['dscp'] = func['mark']
		route['match']['destination'] = prefix
		route['then'] = {}
		route['then']['extended-community'] = 'target:' + fc['target']
		route['then']['redirect'] = func['target']

		result = cmd + ' flow route ' + json.dumps(route)
		return result

	def flow_btmside(self, cmd, func, func_next, prefix):
		result = []
		result.append(flow_btmside_egress(cmd, func, func_next, prefix))
		result.append(flow_btmside_ingress(cmd, func, func_next, prefix))
		return result

	def flow_btmside_egress(self, cmd, func, func_next, prefix):
		route = {}
		fc = self.data['classes'][func['class']]

		route['rd'] = self.data['router-id'] + ':' + fc['id']
		route['match'] = {}
		route['match']['dscp'] = func_next['mark']
		route['match']['source'] = prefix
		route['then'] = {}
		route['then']['extended-community'] = 'target:' + fc['target']
		route['then']['redirect'] = func_next['target']

		result = cmd + ' flow route ' + json.dumps(route)
		return result

	def flow_btmside_ingress(self, cmd, func, func_next, prefix):
		route = {}
		fc = self.data['classes'][func['class']]

		route['rd'] = self.data['router-id'] + ':' + func_next['id']
		route['match'] = {}
		route['match']['destination'] = prefix
		route['then'] = {}
		route['then']['extended-community'] = 'target:' + func_next['target']
		route['then']['mark'] = func['mark']
		route['then']['redirect'] = 'target:' + fc['target']

		result = cmd + ' flow route ' + json.dumps(route)
		return result

