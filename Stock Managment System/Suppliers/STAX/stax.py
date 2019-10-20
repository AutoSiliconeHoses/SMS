import sys, string, os, yaml
import requests, csv

def download_file_from_server_endpoint(server_endpoint, local_file_path):
    # Send HTTP GET request to server and attempt to receive a response
    response = requests.get(server_endpoint)

    # If the HTTP GET request can be served
    if response.status_code == 200:

        # Write the file contents in the response to a file specified by local_file_path
        with open(local_file_path, 'wb') as local_file:
            for chunk in response.iter_content(chunk_size=128):
                local_file.write(chunk)

def stax(zero=False):
    if zero:
        print("Zeroing Stax")
    else:
        print("Starting Stax")

    # Read config file
    with open("config.yml", 'r') as cfg:
        config = yaml.load(cfg, Loader=yaml.FullLoader)

    MAX = config['suppliers']['fps']['max']
    MIN = config['suppliers']['fps']['min']

    # Create alter list
    alter = []
    with open('Suppliers/alterlist.csv') as altercsv:
        csvlist = list(csv.reader(altercsv))
        skuind = csvlist[0].index("stax")
        quaind = skuind + 1
        for row in csvlist[2:]:
            alter.append([row[skuind],row[quaind]])

    download_file_from_server_endpoint(config['suppliers']['stax']['url'], "Suppliers/STAX/stax.csv")

    with open('Suppliers/STAX/stax.csv') as csvfile:
        full = csvfile.read().splitlines(True)
        reader = csv.DictReader(full[1:])
        next(reader, None)
        data = []
        for row in reader:
            # Alter
            if row['Item']+"-SX" in [line[0] for line in alter]:
                row['Quantity'] = alter[[line[0] for line in alter].index(row['Item']+"-SX")][1]

            if int(row['Quantity']) > MAX:
                row['Quantity'] = MAX
            elif int(row['Quantity']) < MIN:
                row['Quantity'] = 0

            if zero:
                row['Quantity'] = 0

            data.append([row['Item']+"-SX",row['Quantity']]) 

    with open("Server/Send/StockFiles/stax.tsv", "w", newline="") as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(data)


    print("finished stax.py")
