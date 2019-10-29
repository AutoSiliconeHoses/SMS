import os, yaml, csv
import Server.Receive.supplier_ftp as supplier_ftp

#Download file from FTP
def homehardware(zero=False):
    if zero:
        print("Zeroing HomeHardware")
    else:
        print("Starting HomeHardware")

    supplier_ftp.getFile("homehardware")

    with open("config.yml", 'r') as cfg:
        config = yaml.load(cfg, Loader=yaml.FullLoader)

    MAX = config['suppliers']['homehardware']['max']
    MIN = config['suppliers']['homehardware']['min']

    # Create alter list
    alter = []
    with open('Suppliers/alterlist.csv') as altercsv:
        csvlist = list(csv.reader(altercsv))
        skuind = csvlist[0].index("homehardware")
        quaind = skuind + 1
        for row in csvlist[2:]:
            alter.append([row[skuind],row[quaind]])

    # stock_no	primary
    with open('Suppliers/HOMEHARDWARE/Primary1.csv') as csvfile:
        full = csvfile.read().splitlines(True)
        reader = csv.DictReader(full)
        next(reader, None)
        data = []
        for row in reader:
            # Alter
            if row['\ufeffstock_no']+"-HH" in [line[0] for line in alter]:
                row['primary'] = alter[[line[0] for line in alter].index(row['\ufeffstock_no']+"-HH")][1]

            if int(row['primary']) > MAX:
                row['primary'] = MAX
            elif int(row['primary']) < MIN:
                row['primary'] = 0

            if zero:
                row['primary'] = 0

            data.append([row['\ufeffstock_no']+"-HH",row['primary']]) 

    with open("Server/Send/StockFiles/homehardware.tsv", "w", newline="") as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(data)


    print("Finished HomeHardware")