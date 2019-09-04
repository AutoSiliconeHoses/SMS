import os, zipfile, csv

def decco():
    print("Starting Decco")
    if os.path.isfile('Server/Receive/Emails/decco.zip'):
        with zipfile.ZipFile('Server/Receive/Emails/decco.zip', 'r') as zip_ref:
            zip_ref.extractall('Suppliers/DECCO')
        os.rename('Suppliers/DECCO/barc5-3628270409191600.xls', "Suppliers/DECCO/decco.xml")
        # TODO: Parse XML despite it being broken