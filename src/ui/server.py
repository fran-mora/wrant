#!/usr/bin/env python3
# NOQA
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
from wrant.utils import util
from wrant import create_wrant

# TODO: Replace with Flask

public_dir = 'src/ui/public'

PATHS = [path[len(public_dir):] for path in util.files(public_dir, rec=True)]
print(util.white(PATHS))

CONTENT_TYPES = {
    'html': 'text/html',
    'css': 'text/css',
    'js': 'application/javascript'
}
wrant = create_wrant()


def get_params(path):
    params_temp = parse_qs(urlparse(path).query)
    params = {}
    for param in params_temp:
        params[param] = params_temp[param][0]
    return params


def serve(path):
    if path == '/':
        return util.read(f'{public_dir}/index.html'), 'text/html'
    if path in PATHS:
        return (
            util.read(f'{public_dir}/{path}'),
            CONTENT_TYPES.get(path.split('.')[-1], 'text/plain')
        )
    return '', 'text/plain'


class WrantHTTPServer_RequestHandler(SimpleHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)
        # Send headers

        print(util.white(self.path))
        params = get_params(self.path)
        print(util.white(params))
        response = ''
        if 'text' in params:
            content_type = 'application/json'
            highlights = wrant.check(params['text'])
            response = json.dumps(highlights)
        else:
            response, content_type = serve(self.path)
            print(util.yellow(response[:50] + '...'))

        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        print('params:', params)
        # Write content as utf-8 data
        self.wfile.write(bytes(response, "utf8"))
        return

    def do_POST(self):
        # Send response status code
        self.send_response(200)
        # Send headers
        content_length = int(self.headers['Content-Length'])
        post_data = '?' + self.rfile.read(content_length).decode('utf-8')
        print(util.white(post_data))
        params = get_params(post_data)
        print(util.white(params))
        response = ''
        content_type = 'application/json'
        if 'text' in params:
            highlights = wrant.check(params['text'])
            response = json.dumps(highlights)
            print(util.yellow(response[:50] + '...'))

        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        print('params:', params)
        # Write content as utf-8 data
        self.wfile.write(bytes(response, "utf8"))
        return


def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server,
    # you need root access
    server_address = ('127.0.0.1', 8001)
    httpd = HTTPServer(server_address, WrantHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


run()
