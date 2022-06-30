# -------------------------------------------------------------------------------
# Name:        Split_Wall_Building
# Purpose:     intern
#
# Author:      rnicolescu
#
# Created:     30/06/2022
# Copyright:   (c) rnicolescu 2022
# Licence:     <your license here>
# -------------------------------------------------------------------------------

from arcpy import env
from datetime import datetime
import arcpy
import os

def split_wall_bulding(gdbPath):
    env.workspace = gdbPath
    env.overwriteOutput = True
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    wall = raw_input("Enter fcode of wall:")
    building = raw_input("Enter fcode of building:")

    # check if extension ends with gdb or folder exists
    with open(os.path.join(os.getcwd(), "log.txt"), "w") as logFile:
        if gdbPath.endswith("gdb"):
            logFile.write("Workspace loaded -- {}\n".format(dt_string))
            arcpy.FeatureVerticesToPoints_management(wall, "points_all", "ALL")
            logFile.write("Wall vertices to point ('ALL') created -- {}\n".format(dt_string))
            arcpy.FeatureVerticesToPoints_management(wall, "points_end", "BOTH_ENDS")
            logFile.write("Wall vertices to point ('BOTH_ENDS') created -- {}\n".format(dt_string))
            arcpy.MakeFeatureLayer_management("points_all", "lyrAllPoints")
            logFile.write("Temporary feature layer created -- {}\n".format(dt_string))
            arcpy.SelectLayerByLocation_management("lyrAllPoints", "ADD_TO_SELECTION", "points_end")
            logFile.write("Select layer by location succesfully finished -- {}\n".format(dt_string))
            arcpy.DeleteFeatures_management("lyrAllPoints")
            logFile.write("Deleting selected feature layer by location -- {}\n".format(dt_string))
            arcpy.Intersect_analysis(["lyrAllPoints", building], "points_all_sal013")
            logFile.write("Checking intersection -- {}\n".format(dt_string))
            arcpy.SplitLineAtPoint_management(wall, "points_all_building", "wall_temp", "0.01 Meters")
            logFile.write("Spliting line at point of intersection -- {}\n".format(dt_string))
            arcpy.Delete_management("lyrAllPoints")
            logFile.write("Deleting temporary layer -- {}\n".format(dt_string))
            arcpy.Delete_management("points_all")
            arcpy.Delete_management("points_end")
            arcpy.Delete_management("points_all_building")
            arcpy.Rename_management("wall_temp", "wall", "FeatureClas")
            logFile.write("Renaming temp layer with name of original layer -- {}\n".format(dt_string))
            logFile.close()

        else:
            print "GDB path is invalid"


if __name__ == '__main__':
    gdb = raw_input("Add path to GDB:")
    split_wall_bulding(gdb)
    raw_input("Press any key to exit...")
    print "Script done!"
