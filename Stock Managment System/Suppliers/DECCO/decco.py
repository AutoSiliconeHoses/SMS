import os, zipfile, csv, re, yaml
import xml.etree.ElementTree as ET

def decco():
    print("Starting Decco")
    if os.path.isfile('Server/Receive/Emails/decco.zip'):
        # Load config data
        with open("config.yml", 'r') as cfg:
            config = yaml.load(cfg, Loader=yaml.FullLoader)

        MAX = config['suppliers']['decco']['max']
        MIN = config['suppliers']['decco']['min']

        # Fetch file and unzip
        with zipfile.ZipFile('Server/Receive/Emails/decco.zip', 'r') as zip_ref:
            zip_ref.extractall('Suppliers/DECCO')
        os.rename('Suppliers/DECCO/barc5-3628270409191600.xls', "Suppliers/DECCO/decco.xml")

        # Fix Decco file
        clean = []
        with open("Suppliers/DECCO/decco.xml", "r") as f:
            for line in f:
                cleanline = re.sub(r" *(?=<\/Data>)", "", line)
                cleanline = re.sub(r'(?<=<Data ss:Type="String">) *', "", cleanline)
                cleanline = cleanline.replace("&", "&amp;")
                clean.append(cleanline)

        # Write fixed data to file
        with open("Suppliers/DECCO/clean.xml", "w") as f:
            f.writelines(clean)
            f.close()

        # Find Worksheet node
        root = ET.parse('Suppliers/DECCO/clean.xml').getroot()
        for node in root.iter('{urn:schemas-microsoft-com:office:spreadsheet}Worksheet'):
            if node.attrib['{urn:schemas-microsoft-com:office:spreadsheet}Name'] == 'barc5':
                ws_node = node
                break

        # Build table data
        for table in ws_node.iter('{urn:schemas-microsoft-com:office:spreadsheet}Table'):
            tabledata = []
            for row in table.iter('{urn:schemas-microsoft-com:office:spreadsheet}Row'):
                rowdata = []
                for cell in row.iter('{urn:schemas-microsoft-com:office:spreadsheet}Cell'):
                    for data in cell.iter('{urn:schemas-microsoft-com:office:spreadsheet}Data'):
                        rowdata.append(data.text)
                tabledata.append(rowdata)

        # Use tabledata to make stockfile
        vallist = []
        for row in tabledata[6:-1]:
            if len(row) >= 16:
                sku = str(row[1]+"-DC")
                stock = int(row[16])

                if stock > MAX:
                    stock = MAX
                elif stock < MIN:
                    stock = 0
                vallist.append([sku,stock])

        # Write to file
        with open("Server/Send/StockFiles/decco.tsv", "w", newline="") as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(vallist)

        print("Decco Finished")
    else:
        print("Decco file missing")