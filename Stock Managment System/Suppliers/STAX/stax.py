import sys, string, os, yaml
import requests

def download_file_from_server_endpoint(server_endpoint, local_file_path):
    # Send HTTP GET request to server and attempt to receive a response
    response = requests.get(server_endpoint)

    # If the HTTP GET request can be served
    if response.status_code == 200:

        # Write the file contents in the response to a file specified by local_file_path
        with open(local_file_path, 'wb') as local_file:
            for chunk in response.iter_content(chunk_size=128):
                local_file.write(chunk)

def stax:
    # Read config file
    with open("config.yml", 'r') as cfg:
        config = yaml.load(cfg, Loader=yaml.FullLoader)

    download_file_from_server_endpoint(config['suppliers']['stax']['url'], "Suppliers/STAX/stax.csv")


    with open('Suppliers/STAX/stax.csv') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            #TODO: Add to file here
            #FILE.append(row)
            print(row)
