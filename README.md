# GIS Group QGIS Plugin

developed by [Henning Jagd (GisGroup)](mailto:henningjagd@gmail.com)

## Install
1. Add repository `http://gisgroup.eu/plugins.xml` in `Settings>Manage and Install Plugins>Settings>Plugin repositories`
2. Select *Gis Group API plugin* from list; install.

## Config
Plugin set-up for denmark service url. In `~/.qgis2/python/plugins/ggapi`, you can add service areas in constants.py to the `COUNTRY_DICT`, change the `COUNTRY` value in settings.py, and add `API_ENDPOINT` logic to workers/worker_service_area.py if need be.

## Basic Use
- Set API key using the *Manage key* button ![manage key](icon_key.png)
- Create polygons using the *service area* button ![service area](icon_servicearea.png)
