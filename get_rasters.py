#!/usr/bin/env python3

from datetime import date
import arcpy
import os

arcpy.env.workspace = 'data/COL/'
fn = 'source/M6_COL.shp'
arcpy.env.extent = arcpy.Describe(fn).extent

years = set(date.strftime(row[0], "%Y")
            for row in arcpy.da.SearchCursor(fn, "ACQ_DATE"))
years = sorted(list(years))

for yr in years:
    directory = f'data/COL/raster/{yr}'
    if not os.path.isdir(directory):
        os.mkdir(directory)
    tmp_yr = f'in_memory/freq{yr}'
    out_yr = f'raster/{yr}/M6freq{yr}.tif'

    # get feature within yr and create new frequency raster
    sql = f'EXTRACT(YEAR FROM "ACQ_DATE") = {yr}'
    arcpy.Select_analysis(fn, tmp_yr, sql)
    arcpy.PointToRaster_conversion(tmp_yr, '', out_yr, 'COUNT')
    print(f'{yr} done.')

    months = set(date.strftime(row[0], "%m")
                 for row in arcpy.da.SearchCursor(tmp_yr, "ACQ_DATE"))
    months = sorted(list(months))

    for mo in months:
        tmp_mo = f'in_memory/freq{mo}'
        out_mo = f'raster/{yr}/M6freq{yr}{mo}.tif'
        sql = f'EXTRACT(MONTH FROM "ACQ_DATE") = {mo}'
        arcpy.Select_analysis(tmp_yr, tmp_mo, sql)
        arcpy.PointToRaster_conversion(tmp_mo, '', out_mo, 'COUNT')
        arcpy.Delete_management(tmp_mo)
        print(f'{yr}/{mo} done.')

    arcpy.Delete_management(tmp_yr)
