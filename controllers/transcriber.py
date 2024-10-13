import asyncio
import numpy as np
from models.data_queues.data_queue import DataQueue

class Transcriber:
    def __init__(self, model):
        self.model = model
        self.data_queue = DataQueue()
        self.audio_buffer = []
        self.CHUNK_SIZE = 16000 * 5  # 2 seconds of audio at 16 kHz

    async def collect_audio(self):
        while True:
            if not self.data_queue.is_empty():
                data = self.data_queue.get()
                self.audio_buffer.extend(np.frombuffer(data, dtype=np.int16))
                #print(f"Collected audio chunk, buffer size: {len(self.audio_buffer)}")
            else:
                await asyncio.sleep(0.1)

    async def transcribe_and_process(self, text_processor, websocket_handler):
        while True:
            if len(self.audio_buffer) >= self.CHUNK_SIZE:
                print("Taking audio chunk...")
                chunk = np.array(self.audio_buffer[:self.CHUNK_SIZE], dtype=np.int16)
                del self.audio_buffer[:self.CHUNK_SIZE]

                text = await asyncio.to_thread(self.model.transcribe, chunk.astype(np.float32) / 32768.0)

                if text.strip():
                    print("Transcribed:", text)
                    processed_text = text_processor.process(text)
                    await websocket_handler.send_message(processed_text)
            else:
                await asyncio.sleep(0.1)
