import argparse
import asyncio
from models.speech_models.speech_models import WhisperSpeechModel as Model
from models.recorder.recorder import Recorder
from controllers.transcriber import Transcriber
from controllers.text_processor import TextProcessor
from controllers.websocket_handler import WebSocketHandler

async def async_main(args):
    
    # Initialise model
    if args.model != "large" and not args.non_english:
        args.model = args.model + ".en"
    model = Model(args.model)
    
    # Handle keywords 
    keywords = ['HELLO', 'KEYWORD', 'TEST']  # Example keyword list
    cluster_name = 'test_1'
    
    # Initialise my controllers
    text_processor = TextProcessor(cluster_name, keywords=keywords)
    transcriber = Transcriber(model)
    websocket_handler = WebSocketHandler(args.websocket_uri)
    
    # Start the websocket server
    await websocket_handler.start_server()

    recorder = Recorder(args.energy_threshold, lambda _, audio: transcriber.data_queue.put(audio.get_raw_data()))
    recorder.start_recording()

    # Tasks to run concurrently
    tasks = [
        transcriber.collect_audio(),
        transcriber.transcribe_and_process(text_processor, websocket_handler)
    ]

    await asyncio.gather(*tasks)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="small", help="Model to use",
                        choices=["tiny", "base", "small", "medium", "large"])
    parser.add_argument("--non_english", action='store_true',
                        help="Don't use the English model.")
    parser.add_argument("--energy_threshold", default=1000,
                        help="Energy level for mic to detect.", type=int)
    parser.add_argument("--record_timeout", default=2,
                        help="How real-time the recording is in seconds.", type=float)
    parser.add_argument("--phrase_timeout", default=3,
                        help="How much empty space between recordings before we "
                             "consider it a new line in the transcription.", type=float)
    parser.add_argument("--websocket_uri", default="ws://localhost:8765", help="WebSocket server URI", type=str)

    args = parser.parse_args()

    try:
        asyncio.run(async_main(args))
    except KeyboardInterrupt:
        print("Shutting down...")

if __name__ == "__main__":
    main()
