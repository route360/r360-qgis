from .worker_feature import FeatureWorker
from .request import Request
from ggapi import logging
from ggapi.helpers import write
from ggapi.constants import (
    FORMAT_LINEAR,
    FORMAT_STANDARD,
    MODE_BICYCLING,
    MODE_DRIVING,
    MODE_TRANSIT,
    MODE_WALKING,
    POI_TYPES
)


class POIWorker(FeatureWorker):
    """Determines distances to point-of-interest from given features.
    """
    def __init__(self, features, idcolumn, pois, outfile, mode):
        super(POIWorker, self).__init__(features)

        self.idcolumn = idcolumn
        self.outfile = outfile
        self.mode = mode

        self.destinationtypes = pois

    def process(self, feature):
        """Do the work"""
        # get fromfeature
        point = feature.geometry.asPoint()
        origin = '{},{}'.format(point.y(), point.x())
        distances = dict()

        if self.mode == MODE_DRIVING:
            mode = 'car'
        elif self.mode == MODE_WALKING:
            mode = 'foot'
        elif self.mode == MODE_TRANSIT:
            mode = 'public'
        elif self.mode == MODE_BICYCLING:
            mode = 'bycicle'
        request = Request('http://viamap.dk',
                          'nearestpoi',
                          fromcoord=origin,
                          poitypes=','.join(self.destinationtypes),
                          mot=mode)

        for type in self.destinationtypes:
            try:
                place = request.json[type]
                distance = place['routedmeters']
                distances[type] = distance
            except:
                distances[type] = ''

        # iterate over result list
        fromid = feature.attributes[self.idcolumn]

        return (fromid, distances)

    def generaterows(self, result):
        yield ['origin'] + self.destinationtypes
        for (fromid, distances) in result:
            yield [fromid] + [distances[t] for t in self.destinationtypes]

    def postprocess(self, result):
        write(self.outfile, self.generaterows(result))
        return result
