import os
import random

from flask import Flask
from flask import request


app = Flask(__name__)

@app.route('/', methods = ['GET', 'PUT'])
def handle_request():
    start_up()
    if request.method == 'PUT':
        #pass the content of the file to the PUT request
        return do_PUT(request.data)
    if request.method == 'GET':
        return do_GET()


# creating a function for Get Request
def do_GET():
    if os.path.exists(popped):
        with open(popped, 'r', encoding='utf-8') as file:
            popped_pokemon = file.read()
            return popped_pokemon
    else:
        with open(default, 'r', encoding='utf-8') as file:
            popped_pokemon = file.read()
            print("no popped.txt found, using default")
            return popped_pokemon

def write_popped(pokemon):
    with open(popped, 'w', encoding='utf-8') as file:
        file.write(pokemon)

def do_PUT(content):
    """Save a file following a HTTP PUT request"""
    filename = os.path.join(filepath, str(random.randint(0,9)) + ".txt")

    #read the file
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            popped_pokemon = file.read()
            print("popped pokemon: ", filename)
            write_popped(popped_pokemon)
    except:
        with open(default, 'r', encoding='utf-8') as file:
            popped_pokemon = file.read()
            print("popped pokemon: ", default)
            write_popped(popped_pokemon)

    with open(filename, 'wb') as output_file:
        output_file.write(content)
    reply_body = 'Saved "%s"\n' % filename
    return reply_body.encode('utf-8')


def initialize_pokemon():
    #fill in the pokemon files if they don't exist
    for i in range(10):
        if not os.path.exists(os.path.join(filepath, str(i) + ".txt")):
            #copy default to all files
            with open(default, 'r', encoding='utf-8') as default_file:
                default_pokemon = default_file.read()
                with open(os.path.join(filepath, str(i) + ".txt"), 'w', encoding='utf-8') as file:
                    file.write(default_pokemon)

def start_up():
    global filepath
    global default
    global popped
    filepath = "/home/shweshipu/LoS-Wonder-Trade/wonder_trade_server/"
    filepath = os.path.join(filepath, 'pokemon')
    os.makedirs(filepath, exist_ok=True)

    default = os.path.join(filepath, 'default.txt')
    popped = os.path.join(filepath, 'popped.txt')

if __name__ == "__main__":
    app.run()