import os
import arcpy
from arcpy import env
from arcpy.sa import *

# Get the current project and active map
aprx = arcpy.mp.ArcGISProject("CURRENT")
active_map = aprx.activeMap
raster_list = []

# Loop through all layers in the active map
for layer in active_map.listLayers():
    if layer.isRasterLayer:
        raster_list.append(layer)

# Sort raster layers by their name
raster_list = sorted(raster_list, key=lambda l: l.name)

# location of .shp file
inzone = r'G:/jamuna_AOI/jamuna_river_cl_buffer_10km_45N_clip_1976_81_ndwi_extrac.shp'

# dbf out path
out_dbf = 'G:/ndwi_ndvi_dbf/'

# Define field name to Add the new field to the DBF file
new_field_name = "Period"

for raster in raster_list:
    # Check out the ArcGIS Spatial Analyst extension license
    raster_1 = str(raster)
    raster_2 = raster_1 +".dbf"
    dbf_file = os.path.join(out_dbf,raster_2)
    print(raster_1,raster_2,dbf_file)
    
    arcpy.CheckOutExtension("Spatial")
    ZonalStatisticsAsTable(inzone,"OBJECTID" , raster, dbf_file, "NODATA", "ALL")   
    print(f"Extracted values: {raster_2}. path: {dbf_file}")
    

    # Add the new field to the DBF file
    try:
        arcpy.AddField_management(dbf_file, new_field_name, "TEXT")
        print(f"Field '{new_field_name}' added successfully.")
        # Update the new field with the default value for all records
        with arcpy.da.UpdateCursor(dbf_file, [new_field_name]) as cursor:
            for row in cursor:
                row[0] = raster_1      # Set a default value for the new field
                cursor.updateRow(row)
                print(f"Field '{new_field_name}' updated with {raster_1 } values.")
    except Exception as e:
        print(f"An error occurred: {e}")