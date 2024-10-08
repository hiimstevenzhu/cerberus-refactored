print("Data queue loaded.")

from models.data_queues.data_queue_interface import DataQueueInterface
from queue import Queue

class DataQueue(DataQueueInterface):
    def __init__(self):
        self.data_queue = Queue()
    
    def put(self, data):
        self.data_queue.put_nowait(data)
    
    def get(self):
        return self.data_queue.get_nowait()
    
    def get_size(self):
        return self.data_queue.qsize()
        
    def is_empty(self):
        return self.data_queue.empty()
    
    