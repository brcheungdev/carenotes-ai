import http.server
import socketserver

class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = http.server.SimpleHTTPRequestHandler.extensions_map.copy()
    extensions_map.update({
        '.js': 'application/javascript',
        '.mjs': 'application/javascript',
        '.css': 'text/css',
    })

if __name__ == '__main__':
    with socketserver.TCPServer(('127.0.0.1', 8001), Handler) as httpd:
        print('Serving at http://127.0.0.1:8001')
        httpd.serve_forever()
