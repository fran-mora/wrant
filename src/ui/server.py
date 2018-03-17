#!/usr/bin/env python3
# NOQA
from http.server import SimpleHTTPRequestHandler, HTTPServer
from pprint import pprint
from urllib.parse import urlparse, parse_qs
import json
from pathlib import Path
from wrant.utils import util


def get_params(path):
    params_temp = parse_qs(urlparse(path).query)
    params = {}
    for param in params_temp:
        params[param] = params_temp[param][0]
    return params

# HTTPRequestHandler class
class WrantHTTPServer_RequestHandler(SimpleHTTPRequestHandler):

  # GET
  def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type','text/html')
        self.end_headers()

        page = ''
        params = get_params(self.path)
        print(params)
        page = util.read('src/ui/index.html')
        # else:
        #     page = util.read('src/ui/' + self.path[1:])
        # Write content as utf-8 data
        self.wfile.write(bytes(page, "utf8"))
        return

def run():
  print('starting server...')

  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('127.0.0.1', 8000)
  httpd = HTTPServer(server_address, WrantHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()


run()
