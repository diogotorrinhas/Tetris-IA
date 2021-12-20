#Starting AI
import asyncio
import getpass 
import json
import os
from game import *  

from shape import *
from AI_Functions import *
from tree_search import *

import websockets

async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        last_Game = None
        Coordenadas = [[[4,2], [4,3], [5,3], [5,4]],[[4,2], [3,3], [4,3], [3,4]],[[2,2], [3,2], [4,2], [5,2]],[[3,3], [4,3], [3,4], [4,4]],[[4,2], [5,2], [4,3], [4,4]],[[4,2], [4,3], [4,4], [5,4]],[[4,2], [4,3], [5,3], [4,4]]]
        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server
                if 'piece' in state.keys() and last_Game != state['game'] and state['piece'] != None and state['piece'] in Coordenadas:   #"O"
                    last_Game = state['game']
                    keys = []
                    #####
                    grid = state['game']
                    p = state['piece']
                    keys = best_position(grid,p)
                    
                    for j in range(len(keys)):
                        key = keys[j]
                    # send key command to server - you must implement this send in the AI agent
                        await websocket.send(json.dumps({"cmd": "key", "key": key}))
                        await websocket.recv() 
                    await websocket.send(json.dumps({"cmd": "key", "key": "s"}))
                    
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return

         
# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
