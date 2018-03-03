#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from wrant.utils import util
from pprint import pprint

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

  # GET
  def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        print(dir(self))
        page = ''
        if self.path.startswith('/check'):
            pass
        else:
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
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()


run()
