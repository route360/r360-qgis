from .worker import Worker


class FeatureWorker(Worker):
    """Base worker for working on features.

    Implements standard length and iterator methods for features
    """
    def __init__(self, features):
        self.features = features

        super(FeatureWorker, self).__init__()

    def count(self):
        return len(self.features)

    def iterator(self):
        return iter(self.features)
