import mws, os, yaml, csv

with open("config.yml", 'r') as cfg:
    config = yaml.load(cfg, Loader=yaml.FullLoader)

class AmazonMWS():
    def format(self, file, prime=False, zero=False):
        data = [["sku","price","minimum-seller-allowed-price","maximum-seller-allowed-price","quantity","leadtime-to-ship"]] # Add header
        lead = config['amazon']['leadShipping']

        # Build file data
        with open(file) as tsvfile:
            reader = csv.reader(tsvfile, delimiter="\t")
            for row in reader:
                if zero:
                    row[1] = 0
                if prime:
                    data.append([row[0]+"-PRIME","","","",row[1]])
                else:
                    data.append([row[0],"","","",row[1],lead])

        # Write file to Uploading directory
        base = os.path.basename(file)
        if prime:
            supplier = os.path.splitext(base)[0]
            newfile = os.path.join("Server/Send/Amazon/Uploading/",supplier+"-PRIME.tsv")
        else:
            newfile = os.path.join("Server/Send/Amazon/Uploading/", base)

        with open(newfile, "w", newline="") as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(data)
        return newfile

    def SubmitFeed(self, newfiles):
        # Setup API
        feeds_api = mws.Feeds(
            access_key=config['amazon']['accessKeyId'],
            secret_key=config['amazon']['secretAccessKey'],
            account_id=config['amazon']['merchantId'],
            region='UK',
        )
        # Upload each file
        results = []
        for file in newfiles:
            with open(file, 'r') as tsvfile:
                data = tsvfile.read()
            receive = feeds_api.submit_feed(feed=data.encode(), feed_type="_POST_FLAT_FILE_INVLOADER_DATA_")
            results.append(receive)
        return results
