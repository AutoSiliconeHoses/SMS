import openpyxl, os, glob, yaml, sys, csv

def fps_sheffield():
    with open("config.yml", 'r') as cfg:
        config = yaml.load(cfg, Loader=yaml.FullLoader)

    MAX = config['suppliers']['fps']['max']

    if os.path.isfile('Server/Receive/Emails/FPS_STOCK.csv'):
        with open('Server/Receive/Emails/FPS_STOCK.csv') as csvfile:
            full = csvfile.read().splitlines(True)
            reader = csv.DictReader(full)
            next(reader, None)
            data = ""
            for row in reader:
                if int(row['Free Stock Available Flag']) == 8:
                    row['Free Stock Available Flag'] = str(MAX)
                elif int(row['Free Stock Available Flag']) == 0:
                    row['Free Stock Available Flag'] = "0"
                data += (row['Product Code'] + "-" + row['MFG Code'] + "-FPS")+"\t"+row['Free Stock Available Flag']+"\n"

        with open("Suppliers/FPS/fps_sheffield.tsv", "w") as text:
            text.write(data)
            text.close()
    else:
        print("Error: FPS_STOCK file not found")
