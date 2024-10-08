""" 
Speech model methods will be defined here. 
An informal interface will be used to ensure abstraction - there is no need for strict enforcement.
"""
import numpy as np

print("Speech model interface loaded.")

class SpeechModelInterface:
    def __init__(self) -> None:
        '''
        Initialise the speech model with the necessary parameters.
        '''
        pass
    def transcribe(self, audio: np.array) -> str:
        '''
        Transcribes an audio clip to text. Audio clip will be as a numpy array.
        '''
        pass
    def load_model(self) -> None:
        '''
        Load the model given the necessary parameters.
        '''
        pass
