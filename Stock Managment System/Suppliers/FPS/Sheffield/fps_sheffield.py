import openpyxl, os, glob, yaml, sys

def fps_sheffield():
    with open("config.yml", 'r') as cfg:
        config = yaml.load(cfg, Loader=yaml.FullLoader)

    MAX = config['suppliers']['fps']['max']
    MIN = config['suppliers']['fps']['min']

    for file in glob.glob('Suppliers/FPS/Sheffield/FPS_STOCK_*.xlsx'):
        doc = openpyxl.load_workbook(file)
        sheet = doc['Sheet1']

        vallist = []
        for row in range(2, sheet.max_row + 1):
            vallist.append((sheet.cell(row=row, column=1).value + "-" + sheet.cell(row=row, column = 3).value + "-FPS",sheet.cell(row=row, column=4).value))

        temptext = ""
        for i in range(0, len(vallist)):
            if int(vallist[i][1]) == 8:
                templine = vallist[i][0] + "\t"+str(MAX)+"\n"
            elif int(vallist[i][1]) <= MIN:
                templine = vallist[i][0] + "\t0\n"
            else:
                templine = vallist[i][0] + "\t" + vallist[i][1] + "\n"
            temptext = temptext + templine

    with open("Suppliers/FPS/fps_sheffield.txt", "w") as text:
        text.write(temptext)
        text.close()
