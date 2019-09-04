import os, sys, yaml, time, re
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


def fps():
	print("running fps.py")
	fps_sheffield.fps_sheffield()
	fps_leeds.fps_leeds()

	leeds = []
	with open("Suppliers/FPS/fps_leeds.tsv") as l:
		leedsFile = l.readlines()
		for line in leedsFile:
			leeds.append(re.split('\t',line.strip()))

	sheffield = []
	with open("Suppliers/FPS/fps_sheffield.tsv") as s:
		sheffieldFile = s.readlines()
		for line in sheffieldFile:
			sheffield.append(re.split('\t',line.strip()))

	sheffield = sorted(sheffield, key=itemgetter(0))
	leffield = [ line[0] for line in sheffield ]

	fullfps = ""
	matches = []
	for lLine in leeds:
		found = Binary_search(leffield,lLine[0])
		if found:
			if lLine[1] >= sheffield[found][1]:
				fullfps += lLine[0] + "\t" + lLine[1] + "\n"
			elif lLine[1] < sheffield[found][1]:
				fullfps += sheffield[found][0] + "\t" + sheffield[found][1] + "\n"
			matches.append(lLine[0])
		elif not found:
			fullfps += lLine[0] + "\t" + lLine[1] + "\n"

	for sLine in sheffield:
		found = Binary_search(matches,sLine[0])
		if not found:
			fullfps += sLine[0] + "\t" + sLine[1] + "\n"

	with open("Server/Send/StockFiles/fps.tsv", "w") as txtfile:
		txtfile.write(fullfps)
		txtfile.close()

	print("finished fps.py")
