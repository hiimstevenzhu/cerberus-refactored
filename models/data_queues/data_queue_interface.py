'''
Data queues will be defined here.
The data queues will be used to store the data that is to be processed by the speech models.
'''

class DataQueueInterface:
    def __init__(self) -> None:
        '''
        Initialise the data queue.
        '''
        print("Data queue interface loaded.")
        pass
    def put(self, data) -> None:
        '''
        Add data to the queue.
        '''
        pass
    def get(self):
        '''
        Get data from the queue.
        '''
        pass
    def get_size(self) -> int:
        '''
        Get the size of the queue.
        '''
        pass
    def is_empty(self) -> bool:
        '''
        Check if the queue is empty.
        '''
        pass
    
    