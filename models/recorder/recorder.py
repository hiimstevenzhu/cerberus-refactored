print("Recorder module loaded.")

from models.recorder.recorder_interface import RecorderInterface
import speech_recognition as sr
import setuptools.dist

class Recorder(RecorderInterface):
    def __init__(self, energy_threshold, callback) -> None:
        self.recorder = sr.Recognizer()
        self.recorder.energy_threshold = energy_threshold
        self.callback = callback
        self.sample_rate = 16000 
        
    def start_recording(self):
        source = sr.Microphone(sample_rate=self.sample_rate)
        with source:
            self.recorder.adjust_for_ambient_noise(source)
            self.recorder.listen_in_background(source, self.callback)
            print("Recording started...\n")
