from .request import Request
from .worker_feature import FeatureWorker
from ggapi.helpers import batch, write, Features
from ggapi import logging, settings
from PyQt4.QtCore import QVariant
from qgis.core import *


from ggapi.constants import (
    FORMAT_LINEAR,
    FORMAT_STANDARD,
    FORMAT_ROUTES,
    FORMAT_LINES,
    MODE_BICYCLING,
    MODE_DRIVING,
    MODE_TRANSIT,
    MODE_WALKING,
    UNIT_METERS,
    UNIT_MINUTES
)

COORD_BATCH_SIZE = 5

MODE2GG_MOT = {MODE_BICYCLING: 'bycicle',
               MODE_DRIVING:   'car',
               MODE_TRANSIT:   'public',
               MODE_WALKING:   'foot'}
MODE2STRING = {MODE_DRIVING: 'bil',
               MODE_WALKING: 'gang',
               MODE_TRANSIT: 'offentlig',
               MODE_BICYCLING: 'cykel'}

# 'http://api.gisgroup.dk/distance/library/Rysagervej%205,%204690%20Haslev/?dbg=1'

class DistanceMatrixWorker(FeatureWorker):
    """Calculate distance matrix between two layers of point-data.

    For calculating the total area of all features in a layer.
    """

    def __init__(self, fromlayer, tolayer, fromidcolumn, toidcolumn,
                 format, outfile, mode, unit, traveltime, timevalue, routelinetype, limitnearest=None):

        self.tolayer = tolayer
        self.fromlayer = fromlayer
        self.from_features = Features.fromlayer(self.fromlayer)
        self.to_features = Features.fromlayer(self.tolayer)
        super(DistanceMatrixWorker, self).__init__(features=self.from_features)
        self.fromidcolumn = fromidcolumn
        self.toidcolumn = toidcolumn
        self.format = format
        self.outfile = outfile
        self.mode = mode
        self.unit = unit
        self.traveltime = traveltime
        self.timevalue = timevalue
        self.routelinetype = routelinetype
        self.limitnearest = limitnearest

        coords = []
        ids = []
        for feature in self.to_features:
            point = feature.geometry.asPoint()
            coord = '{},{}'.format(point.y(), point.x())
            coords.append(coord)
            ids.append(feature.attributes[toidcolumn])
        # concat into api-compatible string
        self.toids = ids
        self.tocoords = coords

        self.fromidtype = self.fromlayer.pendingFields()[self.fromidcolumn].type()
        self.toidtype = self.tolayer.pendingFields()[self.toidcolumn].type()

    def process(self, feature):
        """Do the work.

        How is the work split out? We have NxM combinations. API can only take
        smaller number of to-coords at a time.
        """
        geometry = feature.geometry
        attributes = feature.attributes

        # get fromfeature
        point = geometry.asPoint()
        fromcoord = '{},{}'.format(point.y(), point.x())

        # build api request
        values = []
        routes = []
        for tocoords in batch(self.tocoords, COORD_BATCH_SIZE):
            try:
                mot = MODE2GG_MOT[self.mode]
                request = Request('http://viamap.dk', 'router',
                                  fromcoord=fromcoord,
                                  tocoords='+'.join(tocoords),
                                  mot=mot,
                                  traveltime=self.traveltime,
                                  timevalue=self.timevalue,
                                  zoomlevel=self.routelinetype, # The zoomlevel refers to the polyline.
                                  decodepolyline=1)

                logging.debug("url %s" % str(request.url))
                distances = request.json
                if self.unit is UNIT_METERS:
                    batchvalues = [d['routedmeters'] for d in distances]
                if self.unit is UNIT_MINUTES:
                    batchvalues = [d['travelseconds']/60 for d in distances]
                if self.format == FORMAT_ROUTES:
                    batch_routes = [d['routepolyline'] for d in distances]
                if self.format == FORMAT_LINES:
                    batch_routes = [[d['routepolyline'][0], d['routepolyline'][-1]] for d in distances]
            except Exception as e:
                logging.warn(e)
                batchvalues = ['error' for i in tocoords]

            values = values + batchvalues
            if self.format == FORMAT_ROUTES or self.format == FORMAT_LINES:
                routes = routes + batch_routes

        fromid = attributes[self.fromidcolumn]
        if self.format == FORMAT_ROUTES or self.format == FORMAT_LINES:
            return (fromid, zip(values, routes))
        else:
            return (fromid, values)

    def generaterows(self, result):
        # optionally write header to file
        header = None
        if self.format == FORMAT_STANDARD:
            header = ['fra/til'] + self.toids
        if self.format == FORMAT_LINEAR:
            mode = MODE2STRING[self.mode]
            if self.unit == UNIT_METERS:
                unit = 'meter'
            elif self.unit == UNIT_MINUTES:
                unit = 'minutter'
            header = ['fra', 'til', 'afstand {} ({})'.format(unit, mode)]
        if header:
            yield header

        # write each row to file
        for (fromid, values) in result:
            if self.format == FORMAT_STANDARD:
                yield [fromid] + values
            if self.format == FORMAT_LINEAR:
                rows = zip(self.toids, values)
                if self.limitnearest:
                    rows = sorted(rows, key=lambda t: t[1])
                    rows = rows[:self.limitnearest]
                for toid, value in rows:
                    yield [fromid, toid, value]

    def wkt_from_coordlist(self, coord_list):
        beginning = "MULTILINESTRING (("
        middle = ', '.join(str(c[1]) + " " + str(c[0]) for c in coord_list)
        end = "))"
        return beginning+middle+end

    def write_shapefile(self, result):
        fields = QgsFields()
        fields.append(QgsField("routeID", QVariant.Int))
        fields.append(QgsField("fromID", self.fromidtype))
        fields.append(QgsField("toId", self.toidtype))
        if self.unit == UNIT_METERS:
            unit = 'meter'
        elif self.unit == UNIT_MINUTES:
            unit = 'minutter'
        fields.append(QgsField(unit, QVariant.Double))
        count = 1
        writer = QgsVectorFileWriter(self.outfile, "utf8", fields, QGis.WKBMultiLineString, QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId), "ESRI Shapefile")
        for (fromid, data) in result:
            z = zip(self.toids, data)
            for (toid, data) in z:
                value = data[0]
                route = data[1]
                route_coords = route
                feat = QgsFeature(fields)
                feat.setGeometry(QgsGeometry.fromWkt(self.wkt_from_coordlist(route_coords)))
                feat.setAttributes([count, fromid, toid, value])
                writer.addFeature(feat)
                count += 1
        del writer

    def postprocess(self, result):
        """Result is written to disk

        Format depends on input.
        """
        if self.format == FORMAT_STANDARD or self.format == FORMAT_LINEAR:
            write(self.outfile, self.generaterows(result))
        else:
            self.write_shapefile(result)
        return result
