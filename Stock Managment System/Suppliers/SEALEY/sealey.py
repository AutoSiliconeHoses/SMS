import openpyxl, os, sys, yaml
import Server.supplier_ftp as supplier_ftp

#Download file from FTP
def sealey():
    supplier_ftp.getFile("sealey")

    with open("config.yml", 'r') as cfg:
        config = yaml.load(cfg, Loader=yaml.FullLoader)

    doc = openpyxl.load_workbook('Suppliers/SEALEY/Datacut.xlsx')
    sheet = doc['Export_models_select_files_xls']

    vallist = []
    for row in range(2, sheet.max_row + 1):
        vallist.append((sheet.cell(row=row, column=1).value+"-SY", sheet.cell(row=row, column = 5).value))

    temptext = ""
    for i in range(0, len(vallist)):
        temptext += vallist[i][0] + "\t" + str(vallist[i][1]) + "\n"

    with open("Suppliers/SEALEY/sealey.txt", "w") as text:
        text.write(temptext)
        text.close()
