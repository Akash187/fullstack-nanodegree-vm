#server imports
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import cgi

#database imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                for item in session.query(Restaurant).all():
                    output += "<h2 style='margin:0;'>%s</h2>" %(item.name)
                    output += "<a href='/restaurants/%d/edit'>Edit</a>" %(item.id)
                    output += "</br>"
                    output += "<a href='#'>Delete</a>"
                    output += "<div style='margin-bottom:20px'></div>"
                session.close()
                output += '<a href="restaurants/new"><h2>Make a New Restaurant Here</h2></a>'
                output += "</body></html>"
                self.wfile.write(output)
                #print output
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                x = self.path.rindex('/') #give the last indexof '/' in path
                restaurant_id = self.path[13:x]
                #print("id : " + restaurant_id)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurant = session.query(Restaurant).filter_by(id= restaurant_id).one()

                output = ""
                output += "<html><body>"
                output += "<h1>Rename Restaurant :- %s</h1>" %(restaurant.name)
                output += "<form method = 'POST' enctype='multipart/form-data' action =  %s>" %(self.path)
                output += "<input name = 'updateRestaurantName' type = 'text' placeholder = 'New Name' > "
                output += "<input type='submit' value='rename'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    print(fields)
                    restaurantName = fields.get('newRestaurantName')

                    if restaurantName[0]:
                        myRestaurant = Restaurant(name=restaurantName[0])
                        session.add(myRestaurant)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
                    else:
                        self.send_response(301)
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith("/edit"):
                print(self.path)
                #extracting id from path
                x = self.path.rindex('/')  # give the last indexof '/' in path(e.g:- /restaurants/12/edit)
                restaurant_id = self.path[13:x]
                print(restaurant_id)
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    newName = fields.get('updateRestaurantName')
                    print(newName)
                    if len(newName[0]) != 0:
                        restaurantName = session.query(Restaurant).filter_by(id = restaurant_id).one()
                        restaurantName.name = newName[0]
                        session.add(restaurantName)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
                    else:
                        self.send_response(301)
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
        except:
            pass


def main():
    try:
        port = 8081
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        # for constant listining
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()


if __name__ == '__main__':
    main()
