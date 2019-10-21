# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 11:50:56 2018

@author: poddo
"""

import sys, os
from osgeo import gdal, ogr, osr

### Set paths and import QGIS procesing algorithms
# Add QGIS to system path
sys.path = ['', 'C:\\OSGeo4W64\\bin\\python36.zip', 'C:\\OSGeo4W64\\apps\\Python36\\DLLs', 'C:\\OSGeo4W64\\apps\\Python36\\lib', 'C:\\OSGeo4W64\\apps\\Python36', 'C:\\OSGeo4W64\\apps\\Python36\\lib\\site-packages', 'C:\\OSGeo4W64\\apps\\qgis\\python', 'C:\\OSGeo4W64\\apps\\qgis\\python\\plugins', 'C:\\OSGeo4W64\\apps\\qgis\\bin']

try:
    from qgis.core import *
    from qgis.analysis import QgsNativeAlgorithms
    
    # Set QGIS prefix
    QgsApplication.setPrefixPath('/usr', True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    
    # Import QGIS and native algorithms
    import processing
    from processing.core.Processing import Processing
    Processing.initialize()
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

except:
    print("Qgis import unsuccessful")

else:
    print("Qgis import successful!")