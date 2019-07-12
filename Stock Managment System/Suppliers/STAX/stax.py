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
def stax():
	# Read config file
	with open("../../config.yml", 'r') as cfg:
		config = yaml.load(cfg, Loader=yaml.FullLoader)

	download_file_from_server_endpoint(config['suppliers']['stax']['url'], "stax.csv")
	
	
	# TODO: Remove first and third line from CSV then create file
	with open('stax.csv') as csvfile:
		reader = csv.reader(csvfile)
		next(reader)
		
	
	with open('stax.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		next(reader, None)
		for row in reader:
			print(row)
			print(row['Item'], row['Quantity'])

stax()
