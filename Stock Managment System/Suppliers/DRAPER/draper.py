import os, yaml, csv
import Server.Receive.supplier_ftp as supplier_ftp

#Download file from FTP
def draper(zero=False):
    if zero:
        print("Zeroing Draper")
    else:
        print("Starting Draper")

    supplier_ftp.getFile("draper")

    with open("config.yml", 'r') as cfg:
        config = yaml.load(cfg, Loader=yaml.FullLoader)

    MAX = config['suppliers']['draper']['max']

    # Create alter list
    alter = []
    with open('Suppliers/alterlist.csv') as altercsv:
        csvlist = list(csv.reader(altercsv))
        skuind = csvlist[0].index("draper")
        quaind = skuind + 1
        for row in csvlist[2:]:
            alter.append([row[skuind],row[quaind]])

    with open('Suppliers/DRAPER/stock.csv') as csvfile:
        full = csvfile.read().splitlines(True)
        reader = csv.DictReader(full)
        next(reader, None)
        data = []
        for row in reader:
            # Alter
            if row['Stock Item']+"-DP" in [line[0] for line in alter]:
                row['In Stock'] = alter[[line[0] for line in alter].index(row['Stock Item']+"-DP")][1]

            if row['In Stock'] == 'Y':
                row['In Stock'] = MAX
            elif row['In Stock'] == 'N':
                row['In Stock'] = 0

            if zero:
                row['In Stock'] = 0

            data.append([row['Stock Item']+"-DP",row['In Stock']]) 

    with open("Server/Send/StockFiles/draper.tsv", "w", newline="") as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(data)


    print("Finished Draper")