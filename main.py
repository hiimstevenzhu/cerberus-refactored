import argparse
import asyncio
from models.speech_models.speech_models import WhisperSpeechModel as Model
from models.data_queues.data_queue import DataQueue
from models.recorder.recorder import Recorder
from controllers.transcriber import Transcriber

async def async_main(args):
    data_queue = DataQueue()
    
    if args.model != "large" and not args.non_english:
        args.model = args.model + ".en"
    model = Model(args.model)

    transcriber = Transcriber(model, data_queue, args.websocket_uri)

    recorder = Recorder(args.energy_threshold, lambda _, audio: data_queue.put(audio.get_raw_data()))
    recorder.start_recording()

    tasks = [
        transcriber.collect_audio(),
        transcriber.transcribe_audio(),
        transcriber.send_transcription()
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
