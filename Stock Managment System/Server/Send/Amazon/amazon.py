import mws, os, yaml, csv

with open("config.yml", 'r') as cfg:
    config = yaml.load(cfg, Loader=yaml.FullLoader)

class AmazonMWS():
    def format(self, file):
        lead = config['amazon']['leadShipping']
        data = "sku\tprice\tminimum-seller-allowed-price\tmaximum-seller-allowed-price\tquantity\tleadtime-to-ship\n"

        alter = []
        with open("Server/Send/Amazon/alterlist.csv") as csvfile:
            full = csvfile.read().splitlines(True)
            alterdata = csv.DictReader(full)
            for line in alterdata:
                alter.append((line['sku'],line['quantity']))

        with open(file) as tsvfile:
            reader = csv.reader(tsvfile, delimiter="\t")
            for row in reader:
                if row[0] in [line[0] for line in alter]:
                    row[1] = alter[[line[0] for line in alter].index(row[0])][1]
                data += (row[0]) + "\t\t\t\t" + str(row[1]) + "\t" + str(lead) + "\n"

        newfile = "Server/Send/Amazon/Uploading/"+ os.path.basename(file)
        with open(newfile, 'w') as tsvfile:
            tsvfile.write(data)
            tsvfile.close()
        return newfile

    def SubmitFeed(self, files):
        feeds_api = mws.Feeds(
            access_key=config['amazon']['accessKeyId'],
            secret_key=config['amazon']['secretAccessKey'],
            account_id=config['amazon']['merchantId'],
            region='UK',
        )
        results = []
        for file in files:
            # @todo: Find out if submit_feed takes file data or paths
            with open("Server/Send/Amazon/Uploading/"+file, 'r') as tsvfile:
                data = tsvfile.read()
            receive = feeds_api.submit_feed(feed=data.encode(), feed_type="_POST_FLAT_FILE_INVLOADER_DATA_")
            results.append(receive)
        return results
