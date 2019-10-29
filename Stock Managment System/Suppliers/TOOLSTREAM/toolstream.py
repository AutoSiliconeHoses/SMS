import xlrd, os, yaml, csv
import Server.Receive.supplier_ftp as supplier_ftp

def toolstream(zero=False):
    if zero:
        print("Zeroing Toolstream")
    else:
        print("Starting Toolstream")

    supplier_ftp.getFile("toolstream")

    with open("config.yml", 'r') as cfg:
        config = yaml.load(cfg, Loader=yaml.FullLoader)

    MAX = config['suppliers']['toolstream']['max']
    MIN = config['suppliers']['toolstream']['min']

    # Create alter list
    alter = []
    with open('Suppliers/alterlist.csv') as altercsv:
        csvlist = list(csv.reader(altercsv))
        skuind = csvlist[0].index("toolstream")
        quaind = skuind + 1
        for row in csvlist[2:]:
            alter.append([row[skuind],row[quaind]])

    workbook = xlrd.open_workbook('Suppliers/TOOLSTREAM/Product Content And Pricing Information ENGLISH.xls')
    worksheet = workbook.sheet_by_index(0)
    
    # Read header values into the list    
    keys = [worksheet.cell(0, col_index).value for col_index in range(worksheet.ncols)]

    # Build Dictionary
    dict_list = []
    for row_index in range(1, worksheet.nrows):
        d = {keys[col_index]: worksheet.cell(row_index, col_index).value 
            for col_index in range(worksheet.ncols)}
        dict_list.append(d)

    data = []
    for row in dict_list:
        # Alter
        if row['Product Code']+"-TS" in [line[0] for line in alter]:
            row['In Stock'] = alter[[line[0] for line in alter].index(row['Product Code']+"-TS")][1]

        if row['In Stock'] == 'Y':
            row['In Stock'] = MAX
        elif row['In Stock'] == 'N':
            row['In Stock'] = 0

        if zero:
            row['In Stock'] = 0

        data.append([row['Product Code']+"-TS",row['In Stock']]) 

    with open("Server/Send/StockFiles/toolstream.tsv", "w", newline="") as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(data)


    print("Finished Toolstream")