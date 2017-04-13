#!/usr/bin/env python
# coding: utf-8

import tornado.ioloop
import tornado.web
import tornado.websocket
import os
import argparse
import vrfchain.api

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='vrfchain')
	parser.add_argument('--port', default=8080, help='port number')

	args = parser.parse_args()

	settings = {
	}

	application = tornado.web.Application([
		(r"/api", vrfchain.api.APIHandler),
	], **settings)

	application.listen(args.port)
	tornado.ioloop.IOLoop.current().start()
