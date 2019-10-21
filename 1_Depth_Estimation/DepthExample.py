# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 11:50:56 2018

@author: poddo
"""

from Scripts.initialize import *
from Scripts.q_func import get_coords, cleanup

# Digital elevation model 
dem = 'dem_proj.tif'
dem_res = 90 # 90-meter resolution (MERIT)

# Flood extent polygon
input = 'flood_poly.shp'

### Read in flooded extent
flood = QgsVectorLayer(os.path.join('Data', input))


### Run depth tool
### Select flooded attributes
params = {
	'INPUT': flood,
	'FIELD': 'DN',
	'OPERATOR': 0,
	'VALUE': 255,
	'OUTPUT': os.path.join('Layers', 'flood_select.shp')
}
feedback = QgsProcessingFeedback()
res = processing.run('native:extractbyattribute', params, feedback=feedback)



### Convert from polygon to polyline
params = {
	'POLYGONS': QgsVectorLayer(os.path.join('Layers', 'flood_select.shp')),
	'LINES': os.path.join('Layers', 'flood_lines.shp')
}
feedback = QgsProcessingFeedback()
res = processing.run('saga:convertpolygonstolines', params, feedback=feedback)



### Create points along lines
params = {
	'INPUT': QgsVectorLayer(os.path.join('Layers', 'flood_lines.shp')),
	'DISTANCE': dem_res, # Generates point at intervals based on DEM resolution
	'START_OFFSET': 0,
	'END_OFFSET': 0,
	'OUTPUT': os.path.join('Layers', 'flood_chain.shp')
}
feedback = QgsProcessingFeedback()
res = processing.run('qgis:pointsalonglines', params, feedback=feedback)



### Sample DEM elevations at point locations
params = {
	'SHAPES': QgsVectorLayer(os.path.join('Layers', 'flood_chain.shp')),
	'GRIDS': os.path.join('DEM', dem),
	'RESAMPLING': 0,
	'RESULT': os.path.join('Layers', 'flood_chain_dem.shp')
}
feedback = QgsProcessingFeedback()
res = processing.run('saga:addrastervaluestopoints', params, feedback=feedback)



### Find layer extent
params = {
	'SHAPES': QgsVectorLayer(os.path.join('Layers', 'flood_chain_dem.shp')),
	'OUTPUT': 0,
	'EXTENTS': os.path.join('Layers', 'flood_extent.shp')
}
feedback = QgsProcessingFeedback()
res = processing.run('saga:featureextents', params, feedback=feedback)



### Extract extent coordinates (XMIN, XMAX, YMIN, YMAX)
extent_coords = get_coords('flood_extent.shp')


### Produce TIN
params = {
	'SHAPES': QgsVectorLayer(os.path.join('Layers', 'flood_chain_dem.shp')),
	'FIELD': 'demproj',
	'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': extent_coords,
	'TARGET_USER_SIZE': dem_res, # DEM resolution
	'TARGET_USER_FITS': 0, # Nodes
	'TARGET_OUT_GRID': os.path.join('Layers', 'tin_full.sdat') # Saga Grid format
}
feedback = QgsProcessingFeedback()
res = processing.run('saga:triangulation', params, feedback=feedback)
	
	
#### Add smoothing filter to TIN raster
params = {
	'INPUT': QgsRasterLayer(os.path.join('Layers', 'tin_full.sdat')),
	'MODE': 0, # Square
	'METHOD': 0, # Smooth
	'RADIUS': 5,
	'RESULT': os.path.join('Layers', 'tin_final.sdat')
}
feedback = QgsProcessingFeedback()
res = processing.run('saga:simplefilter', params, feedback=feedback)



### Use raster calculator to subtract from underlying DEM
# First clip dem to flooding extent
params = {
	'INPUT': QgsRasterLayer(os.path.join('DEM', 'dem_proj.tif')),
	'POLYGONS': QgsVectorLayer(os.path.join('Layers', 'flood_extent.shp')),
	'OUTPUT': os.path.join('Layers', 'dem_clip.sdat')
}
feedback = QgsProcessingFeedback()
res = processing.run('saga:cliprasterwithpolygon', params, feedback=feedback)


# Raster Calculator
params = {
	'GRIDS': QgsRasterLayer(os.path.join('Layers', 'tin_final.sdat')),
	'XGRIDS': QgsRasterLayer(os.path.join('Layers', 'dem_clip.sdat')),
	'FORMULA': "a-b",
	'RESAMPLING': 0, # Nearest Neighbour
	'USE_NODATA': False,
	'TYPE': 7, # 4 byte floating point number
	'RESULT': os.path.join('Results', 'depth_full.sdat')	
}
feedback = QgsProcessingFeedback()
res = processing.run('saga:rastercalculator', params, feedback=feedback)



### Clip depth to flood extent
params = {
	'INPUT': QgsRasterLayer(os.path.join('Results', 'depth_full.sdat')),
	'POLYGONS': QgsVectorLayer(os.path.join('Layers', 'flood_select.shp')),
	'OUTPUT': os.path.join('Results', 'depth_clip.sdat')
}
feedback = QgsProcessingFeedback()
res = processing.run('saga:cliprasterwithpolygon', params, feedback=feedback)



### Remove values less than zero
params = {
	'GRIDS': QgsRasterLayer(os.path.join('Results', 'depth_clip.sdat')),
	'FORMULA': "(a>0)*a",
	'RESAMPLING': 0, # Nearest Neighbour
	'USE_NODATA': False,
	'TYPE': 7, # 4 byte floating point number
	'RESULT': os.path.join('Results', 'depth_final.sdat')	
}
feedback = QgsProcessingFeedback()
res_out = processing.run('saga:rastercalculator', params, feedback=feedback)



### Remove intermediate files (layers not tagged as _final) 
layer_dir = "Layers"
result_dir = "Results"
    
#cleanup(layer_dir)
#cleanup(result_dir)
    
QgsApplication.exit()

