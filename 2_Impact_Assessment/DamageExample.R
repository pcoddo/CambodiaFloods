##############################################
## Damage estimations for 2019 Cambodia Floods
##
## file: DamageExample.R
## author: Perry Oddo (perry.oddo@nasa.gov)
## last modified: 10.15.19
##############################################
##############################################


# load libraries
library(raster)


# read in rasters 
landcover = raster("Landcover/LULC_Cambodia.tif")
depth = raster("../1_Depth_Estimation/Results/depth_final.tif")


# convert to array
land.mat = as.matrix(landcover)
depth.mat = as.matrix(depth)


######################
### damage factors ###
######################

## Rice-specific damage factor
rice_factor = function(d, rice_type){
  rice_tab = read.table("Damage_tables/damage_factor_rice.txt", header = T)
  select = rice_tab[which(rice_tab$type == rice_type), 1:2]
  len = length(which(rice_tab$type == rice_type))
  
  x = as.vector(select$depth)
  y = as.vector(select$damage_factor)
  
  return(approx(x = x, y = y, xout = d, yleft = 0, yright = 1)$y)
  
}



## general agriculture damage factor
ag_factor = function(d){
  
  min(d, 0.24*d +0.4, 0.07*d + 0.75, 1)
  
}



# Chen Jorik
chen_jorik = function(d, land_type){
  
  tabtest = read.table("Damage_tables/chen_jorik.txt", header = T)
  select = tabtest[which(tabtest$type == land_type), 1:2]
  len = length(which(tabtest$type == land_type))
  
  x = as.vector(select$depth)
  y = as.vector(select$damage_factor)
  
  return(approx(x = x, y = y, method = "linear", xout = d, yleft = 0, yright = 1)$y)
  
}



# find indices of flooded land cover

floodIndex = function(landcover) {
  
  flood.mat = which(depth.mat > 0)#, arr.ind = T)
  land.index = which(land.mat == landcover)
  
  return(Reduce(intersect, list(flood.mat, land.index)))
  
}



######
# Damage Function
######

damage_fn = function(landcover) {
  
  # Find indices of inundated landcover
  ind = floodIndex(landcover)
  
  # Look up damage function for selected land cover
  # Look up maximum damage value for selected land cover
  
  damages = sapply(ind, function(x){
    
    if(landcover == 1 | landcover == 2 | landcover == 3)
      return(NA) # No damages for 'Other', 'Surface Water', 'Snow and Ice'
    
    else
      
      if(landcover == 4) # Mangrove
        chen_jorik(depth.mat[x], land_type = 'Forest_Area') * 30^2 * 0.639
    
    else
      
      if(landcover == 5) # Flooded Forest
        chen_jorik(depth.mat[x], land_type = 'Forest_Area') * 30^2 * 0.84
    
    else
      
      if(landcover == 6 | landcover == 12) # Deciduous and Mixed Forest
        chen_jorik(depth.mat[x], land_type = 'Forest_Area') * 30^2 * 0.84
    
    else
      
      if(landcover == 7) # Orchard / Plantation
        chen_jorik(depth.mat[x], land_type = 'Forest_Area') * 30^2 * 0.030
    
    else
      
      if(landcover == 8 | landcover == 9 | landcover == 10 | landcover == 11) # Mixed Forest
        chen_jorik(depth.mat[x], land_type = 'Forest_Area') * 30^2 * 0.84
    

    else
      
      if(landcover == 13) # Urban and Built Up
        chen_jorik(depth.mat[x], land_type = 'Urban_household') * 30^2* 29 * 0.75 * 0.4
    
    else
      
      if(landcover == 14) # Cropland
        ag_factor(depth.mat[x]) * 30^2 * 0.109
    
    else
      
      if(landcover == 15) # Rice Paddy
        rice_factor(depth.mat[x], rice_type = 'rainfed') * 30^2 * 0.078
    
    else
      
      if(landcover == 16) # Intertidal
        ag_factor(depth.mat[x]) * 30^2 * 0.030
    
    else
      
      if(landcover == 17)
        return(NA) # No damages for mining
    
    else
      
      if(landcover == 18)
        return(NA) # No damages for barren
    
    else
      
      if(landcover == 19) # Wetlands
        ag_factor(depth.mat[x]) * 30^2 * 0.030
    
    else
      
      if(landcover == 20 | landcover == 21) # Grassland and Shrubland
        ag_factor(depth.mat[x]) * 30^2 * 0.030
    

  })
  
}

########################
# Plot damages as raster
########################

# Create matrix for damages with dimensions of land cover
damage.mat = matrix(data = NA, ncol = ncol(land.mat), nrow = nrow(land.mat))

# Find vector for flooded land cover classes
class_vec = vector(length = 21)

for(i in 1:21){
  class_vec[i] = length(floodIndex(i))
}

flood_vec = which(class_vec>0)


# Loop to find damages for each land cover class
for(i in flood_vec){
  
  damage.mat[floodIndex(i)] <- damage_fn(i)
  
}


# Convert damage matrix to raster object
r = raster(damage.mat)

# Plot results
plot(r, col = rainbow(100, start=0.55, end = 1),
     alpha = 1, 
     add = F,
     legend = T, axes = F)


# Set extent and coordinate reference system
crs(r) <- crs(landcover)
extent(r) <- extent(landcover)


# Write out raster
writeRaster(r, "damage_raster", format = "GTiff")

