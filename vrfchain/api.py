# coding: utf-8

import tornado.web
import json
import flow

class APIHandler(tornado.web.RequestHandler):
	def __init__(self, *args, **kwargs):
		super(APIHandler, self).__init__(*args, **kwargs)

	def post(self):
		try:
			request = json.loads(self.get_argument("request"))
		except:
			raise tornado.web.HTTPError(403)

		result = self.request_process(request)
		self.write(json.dumps(result))

	def request_process(self, request):
		# TODO: validate prefix and functions
		prefix = request['prefix']
		functions = request['functions']

		if ((request['command'] != "announce")
		and (request['command'] != "withdraw")):
			raise tornado.web.HTTPError(403)

		cmd = request['command']
		return flow.flow_generate(functions, cmd, prefix)

