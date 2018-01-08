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
                output += "<a href='/restaurants/new'>Add a new Restaurant.</a><br><br>"
                for resto in restaurants:
                    output += resto.name
                    output += "<br>"                    
                    output += "<a href='/restaurants/%s/edit'>Edit</a><br>"%resto.id
                    output += "<a href='#'>Delete</a><br>"
                    output += "<br>"

                output += "</body></html>"
                self.wfile.write(output)
                # print(output)
                return
            if self.path.endswith('/restaurants/new'):
                self.send_response(200) # Response code for Successful GET
                self.send_header('Content-type','text/html')
                self.end_headers()
                
                output = "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name='name' type='text'><input type='submit' value='Create'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                # print(output)
                return
            if self.path.endswith('/restaurants/new'):
                self.send_response(200) # Response code for Successful GET
                self.send_header('Content-type','text/html')
                self.end_headers()
                
                output = "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name='name' type='text'><input type='submit' value='Create'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                # print(output)
                return
            if self.path.endswith('/edit'):
                self.send_response(200) # Response code for Successful GET
                self.send_header('Content-type','text/html')
                self.end_headers()
                
                restaurantId = self.path.split('/')[2]

                restaurant = session.query(Restaurant).filter_by(id = restaurantId).one()

                output = "<html><body>"
                output += "<h1>%s</h1>"%restaurant.name
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'><input name='name' placeholder='%s' type='text'><input type='submit' value='Rename'></form>"%(restaurantId,restaurant.name)
                output += "</body></html>"
                self.wfile.write(output)
                
        except IOError:
            self.send_error(404,"File not found%s"%self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/restaurants/new'):
                self.send_response(301) # Response code for Successful POST
                self.send_header('location','/restaurants')
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                # print(ctype,pdict)
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurantName = fields.get('name')
                
                print(restaurantName)
                newRestaurant    = Restaurant(name = restaurantName[0])
                session.add(newRestaurant)
                session.commit()
                return
            if self.path.endswith('/edit'):
                self.send_response(301) # Response code for Successful POST
                self.send_header('location','/restaurants')
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                # print(ctype,pdict)
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurantName = fields.get('name')
                
                restaurantId = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id = restaurantId).one()
                restaurant.name = restaurantName[0]
                session.add(restaurant)
                session.commit()
                return
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