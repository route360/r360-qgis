import time
from .worker import Worker


class DummyWorker(Worker):
    """Just a slow worker for testing purposes.

    Does not do any real work. Simply sleeps a few seconds at a time.
    """

    def __init__(self, input):
        super(DummyWorker, self).__init__()
        self.length = input

    def count(self):
        return self.length

    def iterator(self):
        return range(self.count())

    def process(self, item):
        time.sleep(0.01)
        return item
