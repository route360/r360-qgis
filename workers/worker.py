from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot
import traceback
import itertools
import multiprocessing

from ggapi.errors import KillError
from ggapi import logging


class Worker(QObject):
    """Base worker class.
    """
    progress = pyqtSignal(int) # processed more items
    killed = pyqtSignal() # killed itself as instructed
    raised = pyqtSignal(str) # raised an exception
    completed = pyqtSignal(object) # completed succesfully
    finished = pyqtSignal() # is ready for deletion

    # progress emits every PROGRESS_THROTTLE iterations
    PROGRESS_THROTTLE = 1

    # initial progress emit (for instant user feedback)
    PROGRESS_MIN = 0.01

    def __init__(self):
        super(Worker, self).__init__()
        self.suicide = False # flag for suicide

    @pyqtSlot()
    def kill(self):
        """Flag worker to die on next iteration"""
        logging.debug('[WORKER] flagged for suicide')
        self.suicide = True

    @pyqtSlot()
    def start(self):
        """Start the worker.

        Wrapped in try block to ensure correct signals are emitted on error
        """
        try:
            items = self.iterator()

            # set to float to avoid integer division during progress calculation
            self.goal = float(self.count())

            # emit small progress value to instantly indicate progress
            self.progress.emit(self.PROGRESS_MIN)

            # this can probably be parallelized
            processed = itertools.imap(self.process, items)
            updated = map(self.update, enumerate(processed))

            # make sure full progress is emitted (in case of throttling)
            self.progress.emit(100)

            # worker may perform postprocessing on result
            result = self.postprocess(updated)
        except KillError:
            # emit killed signal instead of raised signal on suicide
            self.killed.emit()
        except:
            # emit uncaught errors as strings
            error = traceback.format_exc()
            logging.warn(error)
            self.raised.emit(error)
        else:
            # if no errors were raised, emit completed signal with result
            self.completed.emit(result)
        finally:
            # finally, emit finished signal (even on errors)
            self.finished.emit()

    def update(self, enumerated):
        """Update progress value and periodically emit signal"""
        (i, item) = enumerated
        # before each item, check if worker should kill itself
        if self.suicide:
            raise KillError()
        # throttle progress emits
        if i % self.PROGRESS_THROTTLE == 0:
            # force progress above minimum threshold
            progress = max(self.PROGRESS_MIN, i / self.goal)
            # multiply by 100 to convert from unit to percentage
            self.progress.emit(100*progress)
        # and pipe out item
        return item

    def postprocess(self, result):
        """Override in subclass to implement postprocessing"""
        return result
