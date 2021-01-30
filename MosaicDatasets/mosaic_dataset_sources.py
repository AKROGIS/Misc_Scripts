# -*- coding: utf-8 -*-
"""
Create a list (CSV) of all mosaic datasets in Theme Manager and reference datasets.

Third party requirements:
* arcpy - Installed with ArcGIS
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from io import open
import os
import sys
import xml.etree.ElementTree as et

import arcpy


class Config(object):
    """Namespace for configuration parameters."""

    # pylint: disable=useless-object-inheritance,too-few-public-methods

    theme_manager_path = r"X:\GIS\ThemeMgr\AKR Theme List.tml"
    output_filename = r"mosaic_dataset_files.csv"

    # pylint: disable=line-too-long
    referencing_mosaic_datasets = {
        r"X:\Albers\parks\gaar\LIDAR\PipelineLiDAR\CorridorGAAR.gdb\HillshadeDSM": r"X:\Albers\parks\gaar\LIDAR\PipelineLiDAR\CorridorGAAR.gdb\HighestHitDSM",
        r"X:\Albers\parks\gaar\LIDAR\PipelineLiDAR\CorridorGAAR.gdb\HillshadeDTM": r"X:\Albers\parks\gaar\LIDAR\PipelineLiDAR\CorridorGAAR.gdb\BareEarthDTM",
        r"X:\Albers\parks\gaar\Imagery\NDVI_GAAR.gdb\GaarFinalNDVI": r"X:\IKONOS\NWAK\IKONOS_GAAR.gdb\GaarFinal",
        r"X:\Albers\parks\gaar\AmblerRoad\AmblerRdDEM.gdb\BareEarth5ft_SR_REF": "",
        r"X:\Albers\parks\gaar\AmblerRoad\AmblerRdDEM.gdb\BareEarth5ft_HS_REF": "",
        r"X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\REF_DTM_Aspect": r"X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\DTM",
        r"X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\REF_DSM_SR": r"X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\DSM",
        r"X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\REF_DSM_HS": r"X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\DSM",
        r"X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\REF_DTM_Slope": r"X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\DTM",
        r"X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\REF_DTM_SR": r"X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\DTM",
        r"X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\REF_DTM_HS": r"X:\Albers\UTM8\glba\SDMI\IFSAR.gdb\DTM",
        r"X:\Albers\parks\katm\LiDAR\BrooksCamp2012\KATMBrooksCamp.gdb\BareEarth_HS_Ref": r"X:\Albers\parks\katm\LiDAR\BrooksCamp2012\KATMBrooksCamp.gdb\BareEarthDEM",
        r"X:\Albers\parks\katm\LiDAR\BrooksCamp2012\KATMBrooksCamp.gdb\BareEarth_SR_Ref": r"X:\Albers\parks\katm\LiDAR\BrooksCamp2012\KATMBrooksCamp.gdb\BareEarthDEM",
        r"X:\DEM\SDMI\DEM_REF.gdb\DSM_HS": r"X:\DEM\SDMI\IFSARDEM.gdb\DSM",
        r"X:\DEM\SDMI\DEM_REF.gdb\DSM_SR": r"X:\DEM\SDMI\IFSARDEM.gdb\DSM",
        r"X:\DEM\SDMI\DEM_REF.gdb\DTM_HS": r"X:\DEM\SDMI\IFSARDEM.gdb\DTM",
        r"X:\DEM\SDMI\DEM_REF.gdb\DTM_SR": r"X:\DEM\SDMI\IFSARDEM.gdb\DTM",
        r"X:\Albers\parks\lacl\LiDAR\Kijik2013\LACLKijik.gdb\DEMHydFlat_HS_Ref": "",
        r"X:\Albers\parks\lacl\LiDAR\Kijik2013\LACLKijik.gdb\DEMHydFlat_SR_Ref": "",
        r"X:\Albers\parks\lacl\LiDAR\Kijik2013\LACLKijik.gdb\DEMHydEnf_HS_Ref": "",
        r"X:\Albers\parks\lacl\LiDAR\Kijik2013\LACLKijik.gdb\DEMHydEnf_SR_Ref": "",
    }


try:
    dict.iteritems
except AttributeError:

    def iteritems(dictionary):
        """Python 3 iteritems."""
        return iter(dictionary.items())


else:
    # Python 2
    def iteritems(dictionary):
        """Python 2 iteritems."""
        return dictionary.iteritems()


def get_mosaics():
    """Get the mosaic datasets in Theme Manager plus the list above."""
    mosaic_datasets = []
    xmlroot = et.parse(Config.theme_manager_path).getroot()
    for data in xmlroot.iter("data"):
        if data.get("datasettype") == "MosaicDataset":
            # (data.get('datasource'))
            mosaic_datasets.append(data.get("datasource"))

    # Add referenced datasets
    for referencing, referenced in iteritems(Config.referencing_mosaic_datasets):
        if referencing in mosaic_datasets and referenced:
            mosaic_datasets.remove(referencing)
            mosaic_datasets.append(referenced)
    return mosaic_datasets


def get_dataset(mosaic_datasets):
    """Get the datasets in mosaic_datasets."""

    gdb = arcpy.env["scratchGDB"]
    arcpy.env.workspace = gdb
    # print(gdb, arcpy.env.workspace)
    results = {}
    for dataset in mosaic_datasets:
        # Skip duplicate datasets
        if dataset in results:
            continue
        # Skip Referenced Mosaic Dataset
        try:
            if arcpy.Describe(dataset).referenced:
                print("{0} is a Referenced Mosaic Dataset. Skipping.".format(dataset))
                # TODO: find the source of the referenced dataset
                continue
        except arcpy.ExecuteError:  # all arcpy errors
            continue

        name = arcpy.CreateScratchName("temp", data_type="Dataset")
        table = os.path.join(gdb, name)
        # print(table)
        try:
            arcpy.ExportMosaicDatasetPaths_management(dataset, table)
        except arcpy.ExecuteError:  # all arcpy errors
            print(
                "  **ERROR** reading dataset {0}\n{1}".format(
                    dataset, sys.exc_info()[1]
                )
            )
        if arcpy.Exists(table):
            results[dataset] = {}
            with arcpy.da.SearchCursor(table, "Path") as cursor:
                for row in cursor:
                    try:
                        path, filename = os.path.split(row[0])
                        if not path in results[dataset]:
                            results[dataset][path] = set()
                        results[dataset][path].add(filename)
                    except IndexError:
                        print("  **ERROR** reading row\n{0}".format(sys.exc_info()[1]))
    return results


def write_results(results):
    """Write all the datasets to a CSV file"""

    with open(Config.output_filename, "w", encoding="utf-8") as out_file:
        out_file.write("mosaic_path,mosaic_name,ref_path,ref_name\n")
        for dataset in results:
            ds_path, ds_name = os.path.split(dataset)
            for ref_path in results[dataset]:
                for ref_name in results[dataset][ref_path]:
                    out_file.write(
                        "{0},{1},{2},{3}\n".format(ds_path, ds_name, ref_path, ref_name)
                    )


if __name__ == "__main__":
    write_results(get_dataset(get_mosaics()))
