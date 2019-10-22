# Flood Impact Assessment Tutorial #
#### Case Study Example for SWAT-SEA Conference in Krong Siem Reap, Cambodia, 22 October, 2019 ####


### Introduction ###
This document contains the code used to generate a sample flood impact assessment based on the analysis found in Oddo *et al.* (2018), *Socioeconomic Impact Evaluation for Near Real-Time Flood Detection in the Lower Mekong River Basin.*


### Requirements ###
1. Python version 3
	* This analysis uses version 3.6.7 (64 bit)
	* Python environment from [Anaconda Distribution](https://www.anaconda.com/distribution/#download-section)
	* Environment file included as `flood_env.yml`

2. QGIS version 3
	* This analysis uses version 3.2.2 Bonn (64 bit)
	* It has been tested using QGIS compiled from [OSGeo4W installer](https://qgis.org/en/site/forusers/download.html) (Standalone installer may not import properly)
	* Specific locations of QGIS packages must be added to Python system path (see line 13 in `1_Depth_Estimation` > `Scripts` > `initialize.py`): 

```
sys.path = ['', 'C:\\OSGeo4W64\\bin\\python36.zip', 'C:\\OSGeo4W64\\apps\\Python36\\DLLs', 'C:\\OSGeo4W64\\apps\\Python36\\lib', 'C:\\OSGeo4W64\\apps\\Python36', 'C:\\OSGeo4W64\\apps\\Python36\\lib\\site-packages', 'C:\\OSGeo4W64\\apps\\qgis\\python', 'C:\\OSGeo4W64\\apps\\qgis\\python\\plugins', 'C:\\OSGeo4W64\\apps\\qgis\\bin']`

```

To test installation, run line 8 from `1_Depth_Estimation` > `DepthExample.py`

Output should read:

```python
In [1] from Scripts.initialize import *
"Qgis import successful!"		
```

3. R version [3.3.3](https://cran.r-project.org/bin/windows/base/old/3.3.3/)
	* Impact assessment produced using [RStudio](https://rstudio.com/products/rstudio/download/) IDE but is not required 


### Structure ###
* **1_Depth Estimation**
	* `DepthExample.py`: Intakes flood detection (flood_poly.shp) from "Data" folder to produce estimates of inundation depths

The workflow for this procedure is illustrated using the following schematic:
![Workflow](https://github.com/pcoddo/CambodiaFloods/blob/master/Images/Workflow.png)

* **2_Impact Assessment**
	* `DamageExample.R`: Intakes estimated inundation depths to produce a raster of provisional flood damages

### Data Sources ###
* Flood Extent Detection: [Dartmouth Flood Observatory](https://floodobservatory.colorado.edu/Events/4795/2019Cambodia4795.html)
* Digital Elevation Model (DEM): [Yamadai MERIT DEM](http://hydro.iis.u-tokyo.ac.jp/~yamadai/MERIT_DEM/)
* Land Use / Land Cover Map: [Regional Land Cover Monitoring System (RCLMS)](https://rlcms-servir.adpc.net/en/landcover/#)


Author: [Perry Oddo](mailto:perry.oddo@nasas.gov)

Copyright (2019)

