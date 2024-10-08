import asyncio
import websockets
import json
import numpy as np

class Transcriber:
    def __init__(self, model, data_queue, websocket_uri):
        self.model = model
        self.data_queue = data_queue
        self.audio_buffer = []
        self.websocket_uri = websocket_uri
        self.transcription_queue = asyncio.Queue()
        self.CHUNK_SIZE = 16000 * 2  # 5 seconds of audio at 16 kHz

    async def collect_audio(self):
        while True:
            if not self.data_queue.is_empty():
                data = self.data_queue.get()
                self.audio_buffer.extend(np.frombuffer(data, dtype=np.int16))
                print(f"Collected audio chunk, buffer size: {len(self.audio_buffer)}")
            else:
                await asyncio.sleep(0.1)

    async def transcribe_audio(self):
        while True:
            if len(self.audio_buffer) >= self.CHUNK_SIZE:
                print("Taking audio chunk...")
                chunk = np.array(self.audio_buffer[:self.CHUNK_SIZE], dtype=np.int16)
                del self.audio_buffer[:self.CHUNK_SIZE]

                text = await asyncio.to_thread(self.model.transcribe, chunk.astype(np.float32) / 32768.0)
                
                if text.strip():
                    await self.transcription_queue.put(text)
            else:
                await asyncio.sleep(0.1)

    async def send_transcription(self):
        while True:
            try:
                async with websockets.connect(self.websocket_uri) as websocket:
                    while True:
                        text = await self.transcription_queue.get()
                        await self.send_message(text, websocket)
            except websockets.exceptions.ConnectionClosed:
                print("WebSocket connection closed. Reconnecting...")
                await asyncio.sleep(5)
            except Exception as e:
                print(f"Error in send_transcription: {e}")
                await asyncio.sleep(5)

    async def send_message(self, text, websocket):
        message = {
            'message': text,
            'matches': 0,
            'matched_keywords': [],
            'match_dict': {},
        }
        print(f"Sent: {message['message']}")
        await websocket.send(json.dumps(message))
