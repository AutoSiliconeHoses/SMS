import openpyxl, time, os, zipfile, glob

def decco():
	doc = openpyxl.load_workbook('')
	sheet = doc['']

	vallist = []
	for row in range(2, sheet.max_row + 1):
		vallist.append((sheet.cell(row=row, column=1).value+"-SY", sheet.cell(row=row, column = 5).value))

	temptext = ""
	for i in range(0, len(vallist)):
		temptext = temptext + vallist[i][0] + "\t" + str(vallist[i][1]) + "\n"

	text = open("Suppliers/DECCO/decco.txt", "w")
	text.write(temptext)
	text.close()
