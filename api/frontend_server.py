import http.server
import socketserver
import os

PORT = 8000

if __name__ == '__main__':
    web_dir = os.path.join(os.path.dirname(__file__), '../dist')
    os.chdir(web_dir)

    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(('', PORT), Handler)
    print('Serving at port ' + str(PORT))
    httpd.serve_forever()

