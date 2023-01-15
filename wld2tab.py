#!/usr/bin/env python3

"""
    Convert TWF, JGW, PGW to MapInfo TAB file
"""
from sys import argv
from os import path

WORLD_EXT = {'.TFW': '.TIF', '.JGW': '.JPG', '.PGW': '.PNG', '.WLD': '.TIF'}
WIDTH = 100
HEIGHT = 100

if len(argv) < 2:
    print(f"Usage: {argv[0]} world_file [world_file]")
    exit()

for name in argv[1:]:
    name1, ext = path.splitext(name)
    _, name2 = path.split(name1)
    if ext.upper() in WORLD_EXT.values():   # raster file extension
        ext = ext[0:2] + ext[3] + 'w'
    if ext.upper() in WORLD_EXT.keys():     # world file extension
        # load world file
        with open(name1+ext, 'r') as fp:
            w = fp.readlines()
            if len(w) < 6:
                print(f"Invalid world file, few lines: {name}")
                continue
            try:
                dx = float(w[0].strip())
                ro = float(w[1].strip())
                sk = float(w[2].strip())
                dy = float(w[3].strip())
                xul = float(w[4].strip()) - dx / 2
                yul = float(w[5].strip()) - dy / 2
                xlr = xul + dx * WIDTH
                ylr = yul + dy * HEIGHT
            except:
                print(f"Invalid world file, numbers: {name}")
                continue

            if dx - abs(dy) > 1e-2:
                print(f"Different horizontal and vertical resolution: {name}")
                continue
            with open(name1+'.tab', 'w') as fo:
                print("!table\n!version 300\n!charset WindowsLatin1\n", file=fo)
                print("Definition Table", file=fo)
                print(f'  File "{name2+WORLD_EXT[ext.upper()]}"', file=fo)
                print('  Type "RASTER"', file=fo)
                print(f'  ({xul:.2f},{yul:.2f}) (0,0) Label "Pt 1",', file=fo)
                print(f'  ({xlr:.2f},{yul:.2f}) ({WIDTH},0) Label "Pt 2",', file=fo)
                print(f'  ({xul:.2f},{ylr:.2f}) (0,{HEIGHT}) Label "Pt 3",', file=fo)
                print(f'  ({xlr:.2f},{ylr:.2f}) ({WIDTH},{HEIGHT}) Label "Pt 4"', file=fo)
                print('  CoordSys NonEarth Units "m"', file=fo)
                print('  Units "m"', file=fo)
                print('RasterStyle 1 50', file=fo)
                print('RasterStyle 2 50', file=fo)
    else:
        print(f"Invalig file extension: {name}")
