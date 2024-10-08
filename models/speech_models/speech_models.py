'''
Speech models will be defined here.
All models will follow the methods defined in the SpeechModelInterface, under speech_models_interface.py
'''
print("Speech models loaded.")

from models.speech_models.speech_model_interface import SpeechModelInterface
import numpy as np
import os
import whisper
import torch

class WhisperSpeechModel(SpeechModelInterface):
    def __init__(self, args) -> None:
        self.model = self.load_model(args)
    
    def load_model(self, args):
        print(f"Loading model: OpenAI Whisper")
        return whisper.load_model(args)
        
    def transcribe(self, audio: np.array) -> str:
        return self.model.transcribe(audio.np, fp16=torch.cuda.is_available())['text'].strip()
    