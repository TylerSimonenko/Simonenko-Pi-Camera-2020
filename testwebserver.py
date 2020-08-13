from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = '192.168.8.125'  # Raspberry Pi IP address
host_port = 8080             # Port that the Raspberry binds to


class MyServer(BaseHTTPRequestHandler):  # Name of class, apparently special, used for reading GPIO on Raspberry
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):  # ''' used to enclose the html text for the web page
        html = '''
        <html>
            <head>
                <title>PiCamera System</title>
            </head>
            <body>
                This is a test sentence.
            </body>
        </html>
        '''
        self.do_HEAD()  # This is necessary to run the command below
        self.wfile.write(html.encode())  # This writes the html file for the web browser to read


# This prints that the server has started, printing is not necessary but the __name__ == __main__ is important
if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
