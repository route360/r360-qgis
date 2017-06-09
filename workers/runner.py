from PyQt4.QtCore import Qt, QThread, pyqtSlot

from ggapi import settings, logging
from ggapi.errors import KillTimeoutError


class Runner:
    """A wrapper around thread and worker objects

    Correctly starts a new thread and moves worker to it.
    """
    def __init__(self, cls):
        """Store worker class in instance"""
        self.cls = cls
        self.running = False

    def start(self, *args, **kwargs):
        """Starts worker in separate thread"""
        # stop any previously running workers
        self.stop()
        self.result = None
        self.error = None
        self.running = True

        self.thread = QThread()
        self.worker = self.cls(*args, **kwargs)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.start)
        # graceful stop does not work without direct connection (?)
        self.worker.finished.connect(self.thread.quit, Qt.DirectConnection)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # also save result/error on finish (useful for testing)
        self.worker.finished.connect(self.handlefinished, Qt.DirectConnection)
        self.worker.raised.connect(self.handleraised, Qt.DirectConnection)
        self.worker.completed.connect(self.handlecompleted, Qt.DirectConnection)
        self.worker.killed.connect(self.handlekilled, Qt.DirectConnection)

        self.thread.start()

        # returns worker so caller can connect signals, etc.
        return self.worker

    def stop(self):
        """Attempts to gracefully stop worker

        Forcefully terminates otherwise."""
        logging.debug('Worker: trying to stop gracefully')
        if not self.running:
            logging.debug('Worker was not running')
            return
        try:
            self.worker.kill()
            if not self.thread.wait(settings.KILL_TIMEOUT):
                raise KillTimeoutError()
        except KillTimeoutError:
            logging.warn('Worker: kill timed out, force terminating...')
            self.thread.terminate()
            self.thread.wait()
        except Exception as e:
            logging.warn('Worker: terminate failed!?')
            logging.warn(e)

    # The following methods are for testing
    @pyqtSlot(str)
    def handleraised(self, error):
        """Slot that saves error, useful for testing"""
        logging.warn('[WORKER] raised: {}'.format(error))
        self.error = error

    @pyqtSlot(object)
    def handlefinished(self):
        logging.debug('[WORKER] finished')
        self.running = False

    @pyqtSlot(object)
    def handlecompleted(self, result):
        """Slot that saves result, useful for testing"""
        logging.debug('[WORKER] completed')
        self.result = result

    @pyqtSlot(object)
    def handlekilled(self):
        logging.debug('[WORKER] killed')


    def wait(self, timeout):
        """Wait for thread to end, and return result

        Useful for testing.
        """
        try:
            self.thread.wait(timeout)
            return self.result
        except:
            return None
