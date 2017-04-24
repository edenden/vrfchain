# coding: utf-8

import tornado.web
import json
import flow

class APIHandler(tornado.web.RequestHandler):
	def __init__(self, *args, **kwargs):
		super(APIHandler, self).__init__(*args, **kwargs)

	def post(self):
		try:
			request = tornado.escape.json_decode(
				self.request.body)
		except:
			raise tornado.web.HTTPError(403)

		results = self.request_process(request)
		for result in results:
			print result

		self.write(json.dumps(result))

	def request_process(self, request):
		# TODO: validate prefix and functions
		prefix = request['prefix']
		functions = request['functions']

		if ((request['command'] != "announce")
		and (request['command'] != "withdraw")):
			raise tornado.web.HTTPError(403)

		cmd = request['command']
		generator = flow.Flow()
		return generator.flow_generate(functions, cmd, prefix)

