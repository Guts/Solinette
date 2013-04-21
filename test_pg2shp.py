# -*- coding: cp1252 -*-
#!/usr/bin/env python
import sys
from osgeo import ogr               # pour la géométrie
from osgeo.gdal import SetConfigOption    # variables environnement de gdal
from os import path, getcwd
##

##os.environ['PATH'] = "c:\\Program Files\\GDAL\\bin" + ';' + os.environ['PATH']
##os.environ['GDAL_DRIVER_PATH'] = "c:\\Program Files\\GDAL\\bin\\gdal\\plugins-optional"
##os.environ['GDAL_DATA'] = "c:\\Program Files\\GDAL\\bin\\gdal-data"
##import ogr


##http://gis.stackexchange.com/a/16766

SetConfigOption("GDAL_DATA", getcwd() + r'/gdal')

conn=ogr.Open("PG: host=localhost dbname=testgis user=postgres password=jsnl9a85")
if conn is None:
    print 'Could not open a database or GDAL is not correctly installed!'
    sys.exit(1)

output = path.join(getcwd(), 'output\test.shp')

# Schema definition of SHP file
out_driver = ogr.GetDriverByName( 'ESRI Shapefile' )
out_ds = out_driver.CreateDataSource(output)
out_srs = None
out_layer = out_ds.CreateLayer("point", out_srs, ogr.wkbPoint)
fd = ogr.FieldDefn('name',ogr.OFTString)
out_layer.CreateField(fd)


layer = conn.GetLayerByName("Puentes_peatonales")
#layer = conn.ExecuteSQL(sql)

feat = layer.GetNextFeature()
while feat is not None:
    featDef = ogr.Feature(out_layer.GetLayerDefn())
    featDef.SetGeometry(feat.GetGeometryRef())
    featDef.SetField('name',feat.TITLE)
    out_layer.CreateFeature(featDef)
    feat.Destroy()
    feat = layer.GetNextFeature()

conn.Destroy()
out_ds.Destroy()