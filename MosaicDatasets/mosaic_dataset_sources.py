import sys
import os
import arcpy
import arcpy.da
import xml.etree.ElementTree as et

theme_manager_path = r"X:\GIS\ThemeMgr\AKR Theme List.tml"
output_filename = r"mosaic_dataset_files.csv"

referencing_mosaic_datasets = {
    "X:\Albers\parks\gaar\LIDAR\PipelineLiDAR\CorridorGAAR.gdb\HillshadeDSM":"X:\Albers\parks\gaar\LIDAR\PipelineLiDAR\CorridorGAAR.gdb\HighestHitDSM",
    "X:\Albers\parks\gaar\LIDAR\PipelineLiDAR\CorridorGAAR.gdb\HillshadeDTM":"X:\Albers\parks\gaar\LIDAR\PipelineLiDAR\CorridorGAAR.gdb\BareEarthDTM",
    "X:\Albers\parks\gaar\Imagery\NDVI_GAAR.gdb\GaarFinalNDVI":"X:\IKONOS\NWAK\IKONOS_GAAR.gdb\GaarFinal",
    "X:\Albers\parks\gaar\AmblerRoad\AmblerRdDEM.gdb\BareEarth5ft_SR_REF":"",
    "X:\Albers\parks\gaar\AmblerRoad\AmblerRdDEM.gdb\BareEarth5ft_HS_REF":"",
    "X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\REF_DTM_Aspect":"X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\DTM",
    "X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\REF_DSM_SR":"X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\DSM",
    "X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\REF_DSM_HS":"X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\DSM",
    "X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\REF_DTM_Slope":"X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\DTM",
    "X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\REF_DTM_SR":"X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\DTM",
    "X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\REF_DTM_HS":"X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\DTM",
    "X:\Albers\parks\katm\LiDAR\BrooksCamp2012\KATMBrooksCamp.gdb\BareEarth_HS_Ref":"X:\Albers\parks\katm\LiDAR\BrooksCamp2012\KATMBrooksCamp.gdb\BareEarthDEM",
    "X:\Albers\parks\katm\LiDAR\BrooksCamp2012\KATMBrooksCamp.gdb\BareEarth_SR_Ref":"X:\Albers\parks\katm\LiDAR\BrooksCamp2012\KATMBrooksCamp.gdb\BareEarthDEM",
    "X:\DEM\SDMI\DEM_REF.gdb\DSM_HS":"X:\DEM\SDMI\IFSARDEM.gdb\DSM",
    "X:\DEM\SDMI\DEM_REF.gdb\DSM_SR":"X:\DEM\SDMI\IFSARDEM.gdb\DSM",
    "X:\DEM\SDMI\DEM_REF.gdb\DTM_HS":"X:\DEM\SDMI\IFSARDEM.gdb\DTM",
    "X:\DEM\SDMI\DEM_REF.gdb\DTM_SR":"X:\DEM\SDMI\IFSARDEM.gdb\DTM",
    "X:\Albers\parks\lacl\LiDAR\Kijik2013\LACLKijik.gdb\DEMHydFlat_HS_Ref":"",
    "X:\Albers\parks\lacl\LiDAR\Kijik2013\LACLKijik.gdb\DEMHydFlat_SR_Ref":"",
    "X:\Albers\parks\lacl\LiDAR\Kijik2013\LACLKijik.gdb\DEMHydEnf_HS_Ref":"",
    "X:\Albers\parks\lacl\LiDAR\Kijik2013\LACLKijik.gdb\DEMHydEnf_SR_Ref":"",
}

mosaic_datasets = []
xmlroot = et.parse(theme_manager_path).getroot()
for data in xmlroot.iter('data'):
    if data.get('datasettype') == 'MosaicDataset':
        #print data.get('datasource')
        mosaic_datasets.append(data.get('datasource'))

# Add referenced datasets
for referencing, referenced in referencing_mosaic_datasets.iteritems():
    if referencing in mosaic_datasets and referenced:
        mosaic_datasets.remove(referencing)
        mosaic_datasets.append(referenced)


gdb = arcpy.env['scratchGDB']
arcpy.env.workspace = gdb
#print gdb, arcpy.env.workspace
results = {}
for dataset in mosaic_datasets:
    # Skip duplicate datasets
    if dataset in results:
        continue
    # Skip Referenced Mosaic Dataset
    try:
        if arcpy.Describe(dataset).referenced:
            print "{0} is a Referenced Mosaic Dataset. Skipping.".format(dataset)
            # TODO: find the source of the referenced dataset
            continue
    except:
        continue
    
    name = arcpy.CreateScratchName("temp", data_type="Dataset")
    table = os.path.join(gdb,name)
    #print table
    try:
        arcpy.ExportMosaicDatasetPaths_management(dataset,table)
    except:  # catch *all* exceptions
        print "  **ERROR** reading dataset {0}\n{1}".format(dataset,sys.exc_info()[1])
    if arcpy.Exists(table):    
        results[dataset] = {}
        with arcpy.da.SearchCursor(table,"Path") as cursor:
            for row in cursor:
                try:
                    path, file = os.path.split(row[0])
                    if not path in results[dataset]:
                        results[dataset][path] = set()
                    results[dataset][path].add(file)
                except:  # catch *all* exceptions
                    print "  **ERROR** reading row {0}\n{1}".format(row[0],sys.exc_info()[1])

with open(output_filename,'w') as f:
    f.write("mosaic_path,mosaic_name,ref_path,ref_name\n")
    for dataset in results:
        ds_path, ds_name = os.path.split(dataset)
        for ref_path in results[dataset]:
            for ref_name in results[dataset][ref_path]:
                f.write("{0},{1},{2},{3}\n".format(ds_path, ds_name, ref_path, ref_name))
