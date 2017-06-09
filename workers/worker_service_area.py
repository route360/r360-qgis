import json

import json
from qgis.core import *
from qgis.utils import *
from qgis.gui import *
from osgeo import ogr
from PyQt4.QtCore import QVariant, QSettings
from ggapi import settings
import sys


from .worker_feature import FeatureWorker
from .request import Request, quote
from ggapi import logging
from ggapi.constants import (
    FORMAT_LINEAR,
    FORMAT_STANDARD,
    MODE_BICYCLING,
    MODE_DRIVING,
    MODE_TRANSIT,
    MODE_WALKING,
    UNIT_METERS,
    UNIT_MINUTES,
    POI_TYPES
)

if settings.COUNTRY == 'DENMARK':
    API_ENDPOINT = "https://service.route360.net/denmark/v1/polygon"
if settings.COUNTRY == 'FRANCE':
    API_ENDPOINT = "https://service.route360.net/france/v1/polygon"
if settings.COUNTRY == 'GERMANY':
    API_ENDPOINT = "https://service.route360.net/germany/v1/polygon"


class ServiceAreaWorker(FeatureWorker):
    """Constructs service areas from features
    """
    def __init__(self, features, idcolumn, idfield, radii, mode, outfile, buffer, date, time, bike_speed, walk_speed):
        super(ServiceAreaWorker, self).__init__(features)

        self.features = features
        self.idcolumn = idcolumn
        self.idfield = idfield
        self.radii = radii
        self.mode = mode
        self.outfile = outfile
        self.buffer = buffer
        self.date = date
        self.time = time
        self.walk_speed = walk_speed
        self.bike_speed = bike_speed
        self.settings = QSettings()
        self.key = str(self.settings.value("ggapi/test_key_1", "NO_KEY_SET"))
        print str(type(self.key))

    # def count(self):
    #     return 1
    #
    # def iterator(self):
    #     return [self.features]

    def process(self, feature):
        """Do the work"""
        # get fromfeature

        speed = None

        if self.mode == MODE_DRIVING:
            mode = 'car'
        elif self.mode == MODE_WALKING:
            mode = 'walk'
            if self.walk_speed:
                speed = self.walk_speed
        elif self.mode == MODE_TRANSIT:
            mode = 'transit'
        elif self.mode == MODE_BICYCLING:
            mode = 'bike'
            if self.bike_speed:
                speed = self.bike_speed
        tm = {}
        tm[mode] = {}
        if speed:
            tm[mode]['speed'] = speed
        if self.mode == MODE_TRANSIT:
            tm[mode]['frame']= {}
            tm[mode]['frame']['date'] = self.date
            tm[mode]['frame']['time'] = self.time

        logging.debug(mode)
        sources = []
        fromid = feature.attributes[self.idcolumn]
        point = feature.geometry.asPoint()
        attributes = feature.attributes
        sources.append(dict(id=attributes[self.idcolumn],
                            lat=point.y(),
                            lng=point.x(),
                            tm=tm))

        feat_dict = dict()
        for time in self.radii:
            config = dict(sources=[sources[0]],
                          elevation=False,
                          polygon=dict(serializer='geojson',
                                       pointReduction=True,
                                       values=[time*60],
                                       minPolygonHoleSize=1000000000)
                          )

            request = Request(API_ENDPOINT,
                              cfg=quote(json.dumps(config)),
                              key=self.key,
                              _='1444398161936')
            servicearea = request.json['data']
            if len(servicearea) != 3:
                print "FEJL, makker. len: {}".format(len(servicearea))
            feat_dict[time] = servicearea


        return (fromid, feat_dict)

    def postprocess(self, result):
        """Put geojson into shapefile.

        As of now this will only handle one incoming feature.
        It should be able to handle multiple.
        """

        #Coordinate transformation setup
        sourceCrs = QgsCoordinateReferenceSystem(3857, QgsCoordinateReferenceSystem.EpsgCrsId)
        destCrs = self.features.fromcrs
        transform = QgsCoordinateTransform(sourceCrs, destCrs)
        # Fields setup
        fields = QgsFields()
        fields.append(QgsField(self.idfield.name(), self.idfield.type()))
        fields.append(QgsField("time", QVariant.Double))
        # Shape file writing setup
        writer = QgsVectorFileWriter(self.outfile, "utf8", fields, QGis.WKBMultiPolygon, destCrs, "ESRI Shapefile")
        for id_key, id_dict in result:
            for time_key, data in sorted(id_dict.items(), reverse=True, key=lambda pair: pair[0]):

                # Data extraction
                features = data["features"]
                #if len(features) > 0:
                try:
                    first_feature = features[0]
                    geom = first_feature["geometry"]
                    extract = json.dumps(geom)  # This requires the geojson to be in the right format... Kinda dangerous.
                    s = extract.replace("u'", "'").replace("'",'"')
                    ogr_geom = ogr.CreateGeometryFromJson(s)
                    # Geometry preparation
                    #ogr_geom = ogr_geom.Buffer(self.buffer) # Buffering. This is a bit slow at times.
                    qgis_geom_in = QgsGeometry.fromWkt(ogr_geom.ExportToWkt())
                    qgis_geom = qgis_geom_in.buffer(self.buffer, 5) if buffer != 0 else qgis_geom_in
                    qgis_geom.transform(transform)
                    # Creating the feature
                    feat = QgsFeature(fields)
                    feat.setGeometry(qgis_geom)
                    feat.setAttributes([id_key, time_key])
                    writer.addFeature(feat)
                #else:
                except Exception:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
                    #print u"Opland med tid {} til ID {} kunne ikke laves".format(time_key, id_key).encode("utf8")

        del writer

        return result
