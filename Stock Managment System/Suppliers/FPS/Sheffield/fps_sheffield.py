import openpyxl, os, glob, yaml, sys

def fps_sheffield():
    with open("config.yml", 'r') as cfg:
        config = yaml.load(cfg, Loader=yaml.FullLoader)

    MAX = config['suppliers']['fps']['max']
    MIN = config['suppliers']['fps']['min']
    temptext = ""

    for file in glob.glob('Suppliers/FPS/Sheffield/FPS_STOCK_*.xlsx'):
        doc = openpyxl.load_workbook(file)
        sheet = doc.active

        for x in range(1, sheet.max_column+1):
            if sheet.cell(row = 1, column = x).value == "Product Code":
                productcode = x
            if sheet.cell(row = 1, column = x).value == "MFG Code":
                mfgcode = x
            if sheet.cell(row = 1, column = x).value == "Free Stock Available Flag":
                freestk = x

        for row in range(2, sheet.max_row + 1):
            suppcode = sheet.cell(row = row, column = productcode).value + "-" + sheet.cell(row = row, column = mfgcode).value[0:3] + "-FPS"
            if sheet.cell(row = row, column = freestk).value == "8":
                stk = MAX
            else:
                stk = MIN
            temptext += suppcode + "\t" + str(stk) + "\n"

    with open("Suppliers/FPS/fps_sheffield.txt", "w") as text:
        text.write(temptext)
        text.close()
#fps_sheffield()
