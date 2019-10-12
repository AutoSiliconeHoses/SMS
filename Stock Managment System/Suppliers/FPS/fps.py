import os, sys, yaml, time, re, csv
from operator import itemgetter
import Suppliers.FPS.Sheffield.fps_sheffield as fps_sheffield
import Suppliers.FPS.Leeds.fps_leeds as fps_leeds

def Binary_search(L, target):
    start = 0
    end = len(L) - 1
    while start <= end:
        middle = int((start + end)/ 2)
        midpoint = L[middle]
        if midpoint > target:
            end = middle - 1
        elif midpoint < target:
            start = middle + 1
        else:
            return middle


def fps(zero=False):
    print("running fps.py")

    # Create alter list
    alter = []
    with open('Suppliers/alterlist.csv') as altercsv:
        csvlist = list(csv.reader(altercsv))
        skuind = csvlist[0].index("fps")
        quaind = skuind + 1
        for row in csvlist[2:]:
            alter.append([row[skuind],row[quaind]])

    # Generate data
    fps_sheffield.fps_sheffield()
    fps_leeds.fps_leeds()

    # Load Leeds data
    leeds = []
    with open("Suppliers/FPS/fps_leeds.tsv") as l:
        leedsFile = l.readlines()
        for line in leedsFile:
            leeds.append(re.split('\t',line.strip()))

    # Load Sheffield data
    sheffield = []
    with open("Suppliers/FPS/fps_sheffield.tsv") as s:
        sheffieldFile = s.readlines()
        for line in sheffieldFile:
            sheffield.append(re.split('\t',line.strip()))

    # Sort Sheffield and get skulist
    sheffield = sorted(sheffield, key=itemgetter(0))
    leffield = [ line[0] for line in sheffield ]

    fullfps = []
    matches = []
    for lLine in leeds:
        # Look for Leeds sku in Sheffield
        found = Binary_search(leffield,lLine[0])
        if found:
            # Find larger value
            if lLine[1] >= sheffield[found][1]:
                fullfps.append([lLine[0],lLine[1]]) 
            elif lLine[1] < sheffield[found][1]:
                fullfps.append([sheffield[found][0],sheffield[found][1]])
            # Add to list as to not check again
            matches.append(lLine[0])
        elif not found:
            fullfps.append([lLine[0],lLine[1]])

    # Add all leftover non-matches
    for sLine in sheffield:
        found = Binary_search(matches,sLine[0])
        if not found:
            fullfps.append([sLine[0],sLine[1]])

    # Post processing alter
    for fpsline in fullfps:
        if fpsline[0] in [line[0] for line in alter]:
            fpsline[1] = alter[[line[0] for line in alter].index(fpsline[0])][1]

    with open("Server/Send/StockFiles/fps.tsv", "w", newline="") as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(fullfps)

    print("finished fps.py")