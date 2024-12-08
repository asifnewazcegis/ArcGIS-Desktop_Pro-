
## N.B: One & Only lulc layer will be opened in new unsaved mxd.
## N.B: If gdb formatted folder contain another gdb, it will not work.

import arcpy
import sys
import os
import random

p_path=[]
lyrname=[]
mxd = arcpy.mapping.MapDocument("CURRENT")
for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.supports("DATASOURCE"):
        p_path.append(lyr.workspacePath)
        lyrname.append(lyr)
        #print(lyr.workspacePath)

p_path=''.join(map(str, p_path))
lyrname=''.join(map(str, lyrname))
#print(p_path)
#print(lyrname)
#p_path="I:\Gouripur_utm46_Final.gdb"
arcpy.env.workspace=p_path

# Findout dataset name as per layer
datasets = arcpy.ListDatasets(feature_type='feature')
datasets = [''] + datasets if datasets is not None else []
for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        if lyrname in fc:
            #ds_path = os.path.join(arcpy.env.workspace, ds, fc)
            ds_path = os.path.join(ds)
            #print(ds_path)
        else:
            pass


# Similar name of dataset check in gdb, which will be create automatically

rand= ["na", "nb","nc", "nd", "ne", "nf","ng","nh","ni"]
rand_1=(random.choice(rand))
#print(rand_1)

out_name=[]
dst=str([arcpy.ListDatasets('*','Feature')])
if "layer_new" in dst:
    out_name.append("_{}".format(rand_1))
    #print("Warning: Please select new name of dataset [layer_new] in gdb and run again."+"\n"+p_path+"\layer_new")
    #sys.exit()  # Terminate the program with status code 0
else:
    pass
out_name=''.join(map(str, out_name))
#print(out_name)
    

# Dataset create
out_dataset = p_path
out_name="layer_new{}".format(out_name)
#spatial_ref=arcpy.SpatialReference("WGS 1984 UTM Zone 46N")
spatial_ref=arcpy.Describe(ds_path).spatialReference
#arcpy.CreateFeatureDataset_management(out_dataset, out_name, spatial_ref)
outpath=arcpy.CreateFeatureDataset_management(out_dataset, out_name, spatial_ref)


# New Layer name formation (p 01): as per Spatial Reference
spatial_ref_2=arcpy.Describe(ds_path).spatialReference.Name 
list=[]
list.append(spatial_ref_2)
list_2=str(list)
ut_name=[]
ut_45="WGS_1984_UTM_Zone_45N"
if ut_45 in list_2:
    ut_name.append("45N")
    #print("45")
else:
    ut_name.append("46N")
    #print("46")
#print(ut_name)
ut_name_2= ''.join(map(str, ut_name))
river_canal = "river_canal_utm{}_new".format(ut_name_2)
waterbody= "waterbody_utm{}_new".format(ut_name_2)
roadpoly= "roadpoly_utm{}_new".format(ut_name_2)
#print(river_canal+waterbody+roadpoly)

ut_name_3=[] #Feature name automation if is it existed then name will be changed

# New Layer name formation (p 02): name matching with exist feature
rand_2=(random.choice(rand))
#print(rand_2)

N_L=[river_canal,waterbody,roadpoly]
datasets = arcpy.ListDatasets(feature_type='feature')
datasets = [''] + datasets if datasets is not None else []

for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        for i in N_L:
            if i in fc:
                ut_name_3.append("_{}".format(rand_2)) # Existed feature name will be chnaged automatically
                path = os.path.join(arcpy.env.workspace, ds, fc)
                #print ("change the feature name"+"\n"+path)
                #sys.exit()
            else:
                pass

#"Random number between 5 and 15 is % s" % (r1)
# New Layer name formation (p 03): Existed feature name will be chnaged automatically 
ut_name_4=''.join(map(str, ut_name_3))[0:3]
#print(ut_name_4)
river_canal_2 = "river_canal_utm{}_new{}".format(ut_name_2,ut_name_4)
waterbody_2= "waterbody_utm{}_new{}".format(ut_name_2,ut_name_4)
roadpoly_2= "roadpoly_utm{}_new{}".format(ut_name_2,ut_name_4)
#print("Feature name: "+"\n"+river_canal_2+"\n"+waterbody_2+"\n"+roadpoly_2)

# Feature layer export
Lulc = lyrname    # lulc file
#outpath = p_path+"\layer_new{}".format(out_name)

try:
    arcpy.FeatureClassToFeatureClass_conversion(Lulc, outpath, river_canal_2, "class_name IN(31,32)")
    print("river_canal layer exported:"+river_canal_2)
except:
	print("river_canal export error")

try:	
	arcpy.FeatureClassToFeatureClass_conversion(Lulc, outpath, waterbody_2, "class_name IN(33,34,35,36,38,77,37,56)")
	print("waterbody layer exported: "+waterbody_2)
except:
	print("waterbody layer export error")

try:
	arcpy.FeatureClassToFeatureClass_conversion(Lulc, outpath, roadpoly_2, "class_name IN(39,40,41,42,43,44,78,79,45,80,81)")
	print("roadpoly layer exported: "+roadpoly_2)
except:
    print("roadpoly  layer export error")
