import asyncio
import websockets
import json

import asyncio
import websockets
import json

class WebSocketHandler:
    def __init__(self, websocket_uri, port=8765):
        self.websocket_uri = websocket_uri
        self.port = port
        self.clients = None 

    async def start_server(self):
        print(f"Starting WebSocket server on port {self.port}")
        await websockets.serve(self.register_client, "localhost", self.port)
        
        
    async def register_client(self, websocket, path):
        print(f"Client connected from {websocket.remote_address}")
        self.client = websocket
        try:
            await websocket.wait_closed()
        finally:
            self.client = None
            print(f"Client disconnected: {websocket.remote_address}")


    async def send_message(self, message):
        if self.client:
            message_json = json.dumps(message)
            await self.client.send(message_json)
            #print(f"Sent message to client: {message}")
        else:
            print("No client connected.")

