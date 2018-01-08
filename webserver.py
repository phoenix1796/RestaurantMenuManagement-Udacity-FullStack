from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                
                output = '<html><head><title>Hello</title></head><body>Hello how are you ?</body></html>'
                self.wfile.write(output)
                print(output)
                return
            if self.path.endswith('/hola'):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                
                output = '<html><head><title>Hola</title></head><body>Hola como estas &#161 <a href="/hello">Back to hello</a></body></html>'
                self.wfile.write(output)
                print(output)
                return
        except IOError:
            self.send_error(404,"File not found%s"%self.path)

def main():
    try:
        port = 8080
        server = HTTPServer(('',port),webServerHandler)
        print("Server running on %s"%port)
        server.serve_forever()
    except KeyboardInterrupt:
        print("^C entered")
        server.socket.close()

if __name__ == '__main__':
    main()