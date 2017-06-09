"""Helper functions reused throughout plugin

Mainly message log and qgis layer functions."""

from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsMessageLog
import csv
from PyQt4.QtCore import *

from ggapi import settings


def batch(iterable, n=1):
    """Batches an iteratable"""
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

def next_weekday():
    date = QDate.currentDate().addDays(1)
    while date.dayOfWeek() > 5:
        date = date.addDays(1)
    return date

class Feature:
    def __init__(self, geometry, attributes=dict()):
        self.geometry = geometry
        self.attributes = attributes


class Features:
    """TODO: Always convert to wgs84???"""
    TARGET_SRID = 4326
    TARGET_CRS = QgsCoordinateReferenceSystem(TARGET_SRID)

    def __init__(self, layer):
        self.layer = layer
        crs = self.layer.crs()
        self.fromcrs = crs
        if not crs.postgisSrid() == self.TARGET_SRID:
            self.transform = QgsCoordinateTransform(crs, self.TARGET_CRS)
        else:
            self.transform = None

    @classmethod
    def fromlayer(cls, layer):
        return cls(layer)

    def __iter__(self):
        selected_features = self.layer.selectedFeatures()
        features =  selected_features if len(selected_features) != 0 else self.layer.getFeatures()
        for feature in features:
            attributes = feature.attributes()
            geometry = feature.geometry()
            if self.transform:
                geometry.transform(self.transform)

            yield Feature(geometry, attributes)

    def __len__(self):
        return int(self.layer.featureCount())



def write(filepath, rows):
    with open(filepath, 'wb') as filehandle:
        writer = csv.writer(filehandle, quoting=csv.QUOTE_ALL)

        for cells in rows:
            accumulator = []
            for cell in cells:
                if isinstance(cell, int):
                    item = cell
                elif isinstance(cell, float):
                    # python thinks cell is float. BUT IT REALLY IS INT!!
                    if cell.is_integer():
                        cell = int(cell)
                    item = cell
                else:
                    item = unicode(cell).encode('utf-8')
                accumulator.append(item)
            writer.writerow(accumulator)
