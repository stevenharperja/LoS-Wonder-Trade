from http.server import *
import os
import random
import sys

class GFG(BaseHTTPRequestHandler): 
    filepath = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(filepath, 'pokemon')
    os.makedirs(filepath, exist_ok=True)
    
    default = os.path.join(filepath, 'default.txt')
    popped = os.path.join(filepath, 'popped.txt')
    
    # creating a function for Get Request 
    def do_GET(self): 
        
        # Success Response --> 200 
        self.send_response(200) 

        # Type of file that we are using for creating our 
        # web server. 
        self.send_header('content-type', 'text/html') 
        self.end_headers() 

        # what we write in this function it gets visible on our 
        # web-server 
        if os.path.exists(self.popped):
            with open(self.popped, 'r', encoding='utf-8') as file:
                popped_pokemon = file.read()
                # print("popped pokemon: ", self.popped)
                self.wfile.write(popped_pokemon.encode("utf-8"))
        else:
            print("error, no popped pokemon")

    def write_popped(self, pokemon):
        with open(self.popped, 'w', encoding='utf-8') as file:
            file.write(pokemon)

    def do_PUT(self):
        """Save a file following a HTTP PUT request"""
        filename = os.path.join(self.filepath, str(random.randint(0,9)) + ".txt")

        #read the file 
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                popped_pokemon = file.read()
                print("popped pokemon: ", filename)
                self.write_popped(popped_pokemon)
        except:
            with open(self.default, 'r', encoding='utf-8') as file:
                popped_pokemon = file.read()
                print("popped pokemon: ", self.default)
                self.write_popped(popped_pokemon)

        file_length = int(self.headers['Content-Length'])
        with open(filename, 'wb') as output_file:
            output_file.write(self.rfile.read(file_length))
        self.send_response(201, 'Created')
        self.end_headers()
        reply_body = 'Saved "%s"\n' % filename
        self.wfile.write(reply_body.encode('utf-8'))

# this is the object which take port  
# number and the server-name 
# for running the server 
port = HTTPServer(('', int(sys.argv[1])), GFG) 

def initialize_pokemon():
    #fill in the pokemon files if they don't exist
    for i in range(10):
        if not os.path.exists(os.path.join(GFG.filepath, str(i) + ".txt")):
            #copy default to all files
            with open(GFG.default, 'r', encoding='utf-8') as default_file:
                default_pokemon = default_file.read()
                with open(os.path.join(GFG.filepath, str(i) + ".txt"), 'w', encoding='utf-8') as file:
                    file.write(default_pokemon)
initialize_pokemon()
print("started server")
port.serve_forever() 
