import os, yaml, csv
import Server.Receive.supplier_ftp as supplier_ftp

#Download file from FTP
def toolbank(zero=False):
    if zero:
        print("Zeroing Toolbank")
    else:
        print("Starting Toolbank")

    supplier_ftp.getFile("toolbank")

    with open("config.yml", 'r') as cfg:
        config = yaml.load(cfg, Loader=yaml.FullLoader)

    MAX = config['suppliers']['toolbank']['max']
    MIN = config['suppliers']['toolbank']['min']

    # Create alter list
    alter = []
    with open('Suppliers/alterlist.csv') as altercsv:
        csvlist = list(csv.reader(altercsv))
        skuind = csvlist[0].index("toolbank")
        quaind = skuind + 1
        for row in csvlist[2:]:
            alter.append([row[skuind],row[quaind]])

    with open('Suppliers/TOOLBANK/Availability20D.csv') as csvfile:
        full = csvfile.read().splitlines(True)
        reader = csv.DictReader(full)
        next(reader, None)
        data = []
        for row in reader:
            if row['cstock'] != '':
                # Alter
                if row['\ufeffstock_no']+"-TB" in [line[0] for line in alter]:
                    row['cstock'] = alter[[line[0] for line in alter].index(row['\ufeffstock_no']+"-TB")][1]

                if int(row['cstock']) > MAX:
                    row['cstock'] = MAX
                elif int(row['cstock']) < MIN:
                    row['cstock'] = 0

                if zero:
                    row['cstock'] = 0

                data.append([row['\ufeffstock_no']+"-TB",row['cstock']]) 

    with open("Server/Send/StockFiles/toolbank.tsv", "w", newline="") as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(data)


    print("Finished Toolbank")