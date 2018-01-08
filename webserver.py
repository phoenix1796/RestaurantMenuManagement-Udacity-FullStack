from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/restaurants'):
                self.send_response(200) # Response code for Successful GET
                self.send_header('Content-type','text/html')
                self.end_headers()
                
                restaurants = session.query(Restaurant).all()

                output = "<html><body>"
                for resto in restaurants:
                    output += "%s<br>" % resto.name
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return
        except IOError:
            self.send_error(404,"File not found%s"%self.path)

    def do_POST(self):
        try:
            self.send_response(301) # Response code for Successful POST
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            # print(ctype,pdict)
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messageContent = fields.get('message')

            output = ""
            output += "<html><body>"
            output += "<h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messageContent[0]
            output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say ?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"            
            output += "</body></html>"
            self.wfile.write(output)
            # print(output)

        except:
            pass

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