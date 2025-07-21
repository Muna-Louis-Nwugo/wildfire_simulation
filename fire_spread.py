from graph_builder import set_weights
from sim_events import post
from utils import set_up_listeners
from grids import grid_dict
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
    "grid": None,
    "humidity": 0.5,
    "wind_speed":  10,
    "wind_direction": (2, 9),
    "fire_start": (0, 0),
    "sim_started": False,
    "simulation_end": False
}

#setup HTTP server
class UserInputHTTP(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        #print("DEBUG: OPTIONS request received!")  # Add this
        # This handles CORS preflight requests from browsers.
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS') 
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        #print("DEBUG: OPTIONS response sent!")  # Add this

    def do_POST(self):
        #print("DEBUG: POST request received!")  
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
        sim_config["grid"] = data.get("grid", "practice")
        sim_config["fire_start"] = tuple(data.get("fire_start", sim_config["fire_start"]))
        sim_config["simulation_end"] = data.get("simulation_end", sim_config["simulation_end"])

        if sim_config["simulation_end"]:
            # Send response first
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "shutting_down"}).encode('utf-8'))
            
            # Shutdown in a separate thread
            threading.Thread(
                target=shutdown_server, 
                args=(self.server,), 
                daemon=True
            ).start()
            return
        

        #start the simulation once the post has been received
        if not sim_config["sim_started"]:
            print(sim_config)
            sim_config["sim_started"] = True
            threading.Thread(
                target=run_spread,
                args=(self.server, sim_config["fire_start"]),
                daemon=True
            ).start()

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
    try:
        print("Starting HTTP server on port 5000…")
        server.serve_forever()
    except Exception as e:
        print("Server error:", e)
    finally:
        server.server_close()
        print("HTTP server shut down cleanly.")

def shutdown_server(server, delay=0.5):
    """Shutdown the server after a delay"""
    time.sleep(delay)
    print("Shutting down HTTP server...")
    server.shutdown()
    print("Server shutdown complete.")


# spread the fire, and send updates to Utils module
def spread(fire_start: tuple) :
    grid = grid_dict[sim_config["grid"]]
    print("spread() STARTED")
    print(f"{fire_start} caught fire")
    post("fire_update", grid[fire_start[0]][fire_start[1]])
    fire_graph = set_weights(grid, sim_config["humidity"], sim_config["wind_speed"], sim_config["wind_direction"], fire_start)

    #keep track of on_fire cells
    on_fire = set()
    
    #keep track of queue
    queue = set()

    #add the first item to both on_fire and queue
    on_fire.add(fire_start)
    queue.add(fire_start)
    #print("fire-start added to queue")

    # loops through queue
    while len(queue) > 0 :
        #print("while loop started")
        time.sleep(0.7)
        current_cell = queue.pop()


        for neighbour, weight in fire_graph[current_cell].items() :
            #print("for loop running")
            if neighbour not in on_fire:
                #print(f"{neighbour} not on fire")
                r = random.random()
                #print(r)
                #print(weight)
                #print(r<=weight)

                if r <= weight:
                    print(f"{neighbour} caught fire")
                    on_fire.add(neighbour)
                    queue.add(neighbour)

                    post("fire_update", grid[neighbour[0]][neighbour[1]])


    print("spread() ENDED")
    post("fire_done", None)

#helps run the spread server when it's needed
def run_spread(server, coord: tuple) -> None:
    set_up_listeners()
    spread(coord)
    sim_config["sim_started"] = False
    #threading.Thread(target=server.shutdown, daemon=True).start()


if __name__ == "__main__":
    start_http_server()