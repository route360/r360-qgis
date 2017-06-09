from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsMessageLog

from ggapi import settings


def warn(message):
    """Display a warning"""
    try:
        QgsMessageLog.logMessage(str(message),
                                 settings.PLUGIN_NAME,
                                 level=QgsMessageLog.CRITICAL)
    except:
        pass


def debug(message):
    """Log a message

    But only when debugging."""
    if settings.DEBUG:
        try:
            QgsMessageLog.logMessage(str(message),
                                     settings.PLUGIN_NAME)
        except:
            pass
