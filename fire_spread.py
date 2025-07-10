from graph_builder import set_weights
from sim_events import post
from utils import set_up_listeners
from grids import practice
from http.server import HTTPServer, BaseHTTPRequestHandler
import random
import time
import json
import threading


"""
This module performs 2 key duties. The first is to set up the HTTP server that the Render communicates with to set the simulation parameters,
and the second is to actually run the simulation. 

The UserInputHTTP class is the one that handles HTTP requests, and only allows the JavaScript Render to POST, no other HTTP methods are supported.
Ths POST method modifies the sim_config dictionary, which contains all the information that the spread() function needs to run the simulation. 

The spread() function communicates with the other modules of the backend in order to run the actual simulation engine. It takes the parameters from
sim_config and sends them to the set_weights function in the graph_builder module, which returns a weighted dictionary that the spread function uses
to stochastically propagate the fire. Each time a new cell is lit, it posts an event to the sim_events event manager, which then sends the information 
to the appropraite listener within the utils module.

Additional functions are implemented to start the server, and threading is used to ensure the server doesn't intefere with the implementation of
the simulation itself.

Ideally, the simulation would be run from this file.
"""
sim_config = {
    "humidity": 0.5,
    "wind_speed":  10,
    "wind_direction": (2, 9)
}

#setup HTTP server
class UserInputHTTP(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # This handles CORS preflight requests from browsers.
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow all origins to access
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')  # Allow POST and OPTIONS methods
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')  # Allow Content-Type header
        self.end_headers()

    def do_POST(self):
        # This function runs whenever the server receives a POST request.

        # 1. Read how many bytes the POST body has
        content_length = int(self.headers['Content-Length'])

        # 2. Read that many bytes from the input stream
        body = self.rfile.read(content_length)

        # 3. Parse the bytes as JSON (convert JSON string into Python dictionary)
        data = json.loads(body)

        # 4. Update the global config dictionary:
        #    - Use new values from POST if provided
        #    - Otherwise, keep old values (fallback with .get())
        sim_config["humidity"] = data.get("humidity", sim_config["humidity"])
        sim_config["wind_speed"] = data.get("wind_speed", sim_config["wind_speed"])
        sim_config["wind_direction"] = tuple(data.get("wind_direction", sim_config["wind_direction"]))
        print(sim_config)

        spread(practice, (1, 0))

        # 5. Send back a 200 OK response with CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow cross-origin JS requests
        self.end_headers()

        # 6. Send JSON response to frontend saying "status": "updated"
        self.wfile.write(json.dumps({"status": "updated"}).encode('utf-8'))


#start http server
def start_http_server():
    server = HTTPServer(('localhost', 5000), UserInputHTTP)
    print("HTTP server running at http://localhost:5000")
    server.serve_forever()


# spread the fire, and send updates to Utils module
def spread(grid: list, fire_start: tuple) :
    fire_graph = set_weights(grid, sim_config["humidity"], sim_config["wind_speed"], sim_config["wind_direction"], fire_start)

    #keep track of on_fire cells
    on_fire = set()
    
    #keep track of queue
    queue = set()

    #add the first item to both on_fire and queue
    on_fire.add(fire_start)
    queue.add(fire_start)

    # loops through queue
    while len(queue) > 0 :
        time.sleep(1)
        current_cell = queue.pop()


        for neighbour, weight in fire_graph[current_cell].items() :
            if neighbour not in on_fire:
                if random.random() <= weight:
                    #print(f"{neighbour} caught fire")
                    on_fire.add(neighbour)
                    queue.add(neighbour)

                    post("fire_update", grid[neighbour[0]][neighbour[1]])


    
    post("fire_done", None)


if __name__ == "__main__":
    set_up_listeners()

    # Start server in the background so it doesn't block simulation
    threading.Thread(target=start_http_server, daemon=True).start()

    # Run your simulation
    spread(practice, (1, 0))