# coding: utf-8

import json
import os

class Flow():
	def __init__(self):
		filename = os.path.join(os.path.dirname(__file__),
			"config.json")
		with open(filename, 'r') as f:
			self.config = json.load(f)

	def flow_generate(self, functions, cmd, prefix):
		result = []

		for i, func_req in enumerate(functions):
			func = {}
			for func_config in self.config['functions']:
				if func_req['id'] == func_config['id']:
					func = func_config

			func_next = {}
			if i < len(functions):
				func_req_next = functions[i + 1]
				for func_config in self.config['functions']:
					if func_req_next['id'] == func_config['id']:
						func_next = func_config
			else:
				func_next['id'] = 100
				func_next['target'] = '65000:100'
				func_next['mark'] = 0

			result.append(self.flow_topside(cmd, func, func_next, prefix))
			result.append(self.flow_btmside(cmd, func, func_next, prefix))

		return result

	def flow_topside(self, cmd, func, func_next, prefix):
		result = []
		result.append(self.flow_topside_egress(cmd, func, func_next, prefix))
		result.append(self.flow_topside_ingress(cmd, func, func_next, prefix))
		return result

	def flow_topside_egress(self, cmd, func, func_next, prefix):
		route = {}
		fc = self.config['classes'][func['class']]

		route['rd'] = self.config['router-id'] + ':' + func['id']
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
		fc = self.config['classes'][func['class']]

		route['rd'] = self.config['router-id'] + ':' + fc['id']
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
		result.append(self.flow_btmside_egress(cmd, func, func_next, prefix))
		result.append(self.flow_btmside_ingress(cmd, func, func_next, prefix))
		return result

	def flow_btmside_egress(self, cmd, func, func_next, prefix):
		route = {}
		fc = self.config['classes'][func['class']]

		route['rd'] = self.config['router-id'] + ':' + fc['id']
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
		fc = self.config['classes'][func['class']]

		route['rd'] = self.config['router-id'] + ':' + func_next['id']
		route['match'] = {}
		route['match']['destination'] = prefix
		route['then'] = {}
		route['then']['extended-community'] = 'target:' + func_next['target']
		route['then']['mark'] = func['mark']
		route['then']['redirect'] = 'target:' + fc['target']

		result = cmd + ' flow route ' + json.dumps(route)
		return result

