# Open an new mxd.
# Need to add layer: aoi, waterbody, river, road. But-
# You have to ensured: specific layer name- must have specific part(aoi/waterbody/river/road).
# N.B: Ignore captal or samll letter in name.
# Run this script.


import arcpy
import os
import sys

list_vari=[]
p_path=[]
aoi=[]
waterbody=[]
river=[]
road=[]
mxd = arcpy.mapping.MapDocument("CURRENT")
for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.supports("DATASOURCE"):
        if(arcpy.Describe(lyr).dataType)=='FeatureLayer':
            if arcpy.Describe(lyr).shapeType=="Polygon":
                if ((lyr.name).lower()).find("aoi")>=0:
                    aoi.append(lyr.name)
                    list_vari.insert(0,lyr.name)
                elif ((lyr.name).lower()).find("waterbody")>=0:
                    waterbody.append(lyr.name)
                    list_vari.insert(1,lyr.name)
                    p_path.append(lyr.workspacePath)
                elif ((lyr.name).lower()).find("river")>=0:
                    river.append(lyr.name)
                    list_vari.insert(2,lyr.name)
                elif ((lyr.name).lower()).find("road")>=0:
                    road.append(lyr.name)
                    list_vari.insert(3,lyr.name)
                else:
                    pass
p_path=''.join(map(str, p_path))
aoi=''.join(map(str,aoi))           
waterbody=''.join(map(str, waterbody))   
river=''.join(map(str, river))   
road=''.join(map(str, road))   

if len(list_vari)==4:
    pass
else:
    dict={"aoi":aoi,"waterbody":waterbody,"river":river,"road":road} 
    value = [i for i in dict if dict[i]==""]
    value=','.join(map(str, value ))
    print("Missing layer: {}. Please check and run again.".format(value))
    sys.exit()

fcAndcls = {
    waterbody:"class_name IN(33,34,35,36,38,77,37,56)",
    river: "class_name IN(31,32)",
    road: "class_name IN(39,40,41,42,43,44,78,79,45,80,81)"
    }
for fc, cls in fcAndcls.items():
    l=set([row[0] for row in arcpy.da.SearchCursor(fc,["class_name"],cls)])
    l=','.join(map(str,l))
    if l =="":
        print("Please check: {} layer- layer name with attribute values of class_name and run again".format(fc)+"\n")
    else:
        pass
if l=="":
    sys.exit()
arcpy.env.workspace=p_path
datasets = arcpy.ListDatasets(feature_type='feature')
datasets = [''] + datasets if datasets is not None else []
for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        if road in fc:
            ds_path = os.path.join(ds)
        else:
            pass



out_dataset = p_path
out_name="lulc"
dst=str([arcpy.ListDatasets('*','Feature')])
if "lulc" in dst:
    pass
else:
    spatial_ref=arcpy.Describe(ds_path).spatialReference
    arcpy.CreateFeatureDataset_management(out_dataset, out_name, spatial_ref)
sp_ref_2=arcpy.Describe(ds_path).spatialReference.Name 
list=[]
list.append(sp_ref_2)
list_2=str(list)
ut_nam=[]
ut_45="WGS_1984_UTM_Zone_45N"
if ut_45 in list_2:
    ut_nam.append("45n")
else:
    ut_nam.append("46n")

ut_nam_2= ''.join(map(str, ut_nam))
outpath=p_path+"\lulc"
arcpy.FeatureClassToFeatureClass_conversion(aoi, outpath, "aoi_xyz")
arcpy.FeatureClassToFeatureClass_conversion(waterbody, outpath, "waterbody_xyz")
arcpy.FeatureClassToFeatureClass_conversion(river, outpath, "river_xyz")
arcpy.FeatureClassToFeatureClass_conversion(road, outpath, "road_xyz")

lastpart=[]
if "lulc_utm_{}".format(ut_nam_2) in arcpy.ListFeatureClasses(feature_dataset="lulc"):
    lastpart.append("_2")
else:
    pass
lastpart_2= ''.join(map(str, lastpart))

arcpy.env.workspace=outpath
aoi="aoi_xyz"
lyr=aoi
waterbody="waterbody_xyz"
river="river_xyz"
road="road_xyz"
try:
    desc = arcpy.Describe(aoi)
    fieldObjList = arcpy.ListFields(aoi)   
    fieldNameList = []	
    for field in fieldObjList:
        if not field.required:
            fieldNameList.append(field.name)	    
    if desc.dataType in ["ShapeFile", "DbaseTable"]:
        fieldNameList = fieldNameList[1:]
    arcpy.DeleteField_management(aoi, fieldNameList)
except Exception as err:																						
    print("Fields of aoi is not deleted",err.args[0])

try:
    arcpy.AddField_management(lyr,"class_name","LONG","","","100")
    arcpy.AddField_management(lyr,"maj_class","TEXT","","","100")
    arcpy.AddField_management(lyr,"maj_class_bn","TEXT","","","254")
    arcpy.AddField_management(lyr,"sub_class","TEXT","","","100")
    arcpy.AddField_management(lyr,"sub_class_bn","TEXT","","","254")
    arcpy.AddField_management(lyr,"spl_class","TEXT","","","100")
    arcpy.AddField_management(lyr,"spl_class_bn","TEXT","","","254")
    arcpy.AddField_management(lyr,"ftr_name","TEXT","","","100")
    arcpy.AddField_management(lyr,"crop_pattern","TEXT","","","100")
    arcpy.AddField_management(lyr,"kharif_1","TEXT","","","100")
    arcpy.AddField_management(lyr,"kharif_2","TEXT","","","100")
    arcpy.AddField_management(lyr,"rabi_crops","TEXT","","","100")
    arcpy.AddField_management(lyr,"boro","TEXT","","","100")
    arcpy.AddField_management(lyr,"image_name","TEXT","","","254")
    arcpy.AddField_management(lyr,"remarks","TEXT","","","254")
    arcpy.AddField_management(lyr,"done_by","TEXT","","","3")
except:
    print("Add Field Error")
    
try:
    arcpy.Update_analysis(aoi, waterbody, "wb_update", "BORDERS")
    arcpy.Update_analysis("wb_update",river, "wb_river_update", "BORDERS")
    arcpy.Update_analysis("wb_river_update", road, "lulc_utm_{}{}".format(ut_nam_2,lastpart_2), "BORDERS")
except:
    print("Update Error. Please check again")
    sys.exit()
fclst=[]
for fc in arcpy.ListFeatureClasses():
    if fc.endswith("xyz") or fc.endswith("update"):
        fclst.append(fc)
for df in arcpy.mapping.ListDataFrames(mxd):
    for lyr in arcpy.mapping.ListLayers(mxd,"",df):
        if lyr.name in fclst:
            arcpy.mapping.RemoveLayer(df,lyr)   
for fc in fclst:
    arcpy.management.Delete(fc)
print("Done"+"\n"+"N.B. Please open new mxd to check attribute(class_name) and conduct others operation(Multipart explode, Spilit,.....)")