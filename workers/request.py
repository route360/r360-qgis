from urllib2 import urlopen, HTTPError, quote
import json
from StringIO import StringIO
import gzip
from operator import itemgetter

from ggapi.errors import RequestError
from ggapi import logging

from ggapi.constants import (
    FORMAT_LINEAR,
    FORMAT_STANDARD,
    MODE_BICYCLING,
    MODE_DRIVING,
    MODE_TRANSIT,
    MODE_WALKING,
    UNIT_METERS,
    UNIT_MINUTES
)


DELIMETER = ','


class Request:
    """Represent a request to the api.

    After initializing the request, one can read an appropriate property to
    parse the response as the corresponding format.
    """
    def __init__(self, base, *segments, **params):
        """Perform a request in each language and return a list of responses.

        Positional arguments become url segments appended to the base url,
        while keyword arguments turn into query parameters.
        """
        self.url = self.buildurl(base, *segments, **params)
        logging.debug('URl is {}'.format(self.url))
        self.raw = self.process()
        self.json = self._parsejson(self.raw)

    def buildurl(self, base, *segments, **params):
        url = base
        if segments:
            segments = [s for s in self._prep(segments) if s]
            url += '/' + '/'.join(segments) + '/'

        if params:
            # sort and unzip parameter dictionary
            keys, values = zip(*sorted(params.items(), key=itemgetter(0)))

            # prep and re-zip
            pairs = zip(keys, self._prep(values))

            strings = [k+'='+v for (k, v) in pairs if v]
            url += '?' + '&'.join(strings)

        return url

    def process(self):
        """Make request to url and return the raw response object.
        """
        try:
            response = urlopen(str(self.url))
            # support gzipped responses (route360 always gzips response)
            if response.info().get('Content-Encoding') == 'gzip':
                buffer = StringIO(response.read())
                response = gzip.GzipFile(fileobj=buffer)
            return response
        except HTTPError as error:
            try:
                # parse error body as json
                parsed = self._parsejson(error)
                raise RequestError(parsed)
            except ValueError:
                # when error body is not valid json, might be caused by server
                raise RequestError(error)

    @staticmethod
    def _parsejson(response):
        """Deserialize file-like object containing json to a Python obejct.
        """
        return json.loads(response.read().decode('utf-8'))

    @staticmethod
    def _prep(values):
        for value in values:
            if value is MODE_BICYCLING:
                yield 'bicycle'
            elif value is MODE_DRIVING:
                yield 'car'
            elif value is MODE_TRANSIT:
                yield 'public'
            elif value is MODE_WALKING:
                yield 'foot'
            elif value is None or type(value) == str or str(type(value)) == "<class 'future.types.newstr.newstr'>": # ugly hack. for some reason the "key" attribute from service areas comes as a backported py3 string
                yield value
            else:
                try:
                    yield '+'.join([str(v) for v in value])
                except TypeError:
                    yield str(value).lower()
