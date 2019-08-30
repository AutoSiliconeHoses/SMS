import yaml, os, re
from operator import itemgetter

def Binary_search(L, target):
	start = 0
	end = len(L) - 1
	while start <= end:
		middle = int((start + end)/ 2)
		midpoint = L[middle]
		if midpoint > target:
			end = middle - 1
		elif midpoint < target:
			start = middle + 1
		else:
			return middle

with open("config.yml", 'r') as cfg:
    config = yaml.load(cfg, Loader=yaml.FullLoader)

for storecode in config['ebay']:
    if config['ebay'][storecode]['enabled']:
        print(storecode.upper())
        for supplier in config['suppliers']:
            if config['suppliers'][supplier]['enabled']:
                storePath = os.path.join("Server/Send/Ebay/StoreFiles/", storecode.upper(), supplier+"-FULLSTOCK.csv")
                if os.path.isfile(storePath):
                    stockPath = os.path.join("Server/Send/Ebay/StockFiles/", supplier + ".tsv")
                    if os.path.isfile(stockPath):
                        print("\t", supplier, "MATCH")
                        store = []
                        with open(storePath) as storeFile:
                            storeLines = storeFile.readlines()
                            for line in storeLines:
                                store.append(re.split(',',line.strip()))

                        stock = []
                        with open(stockPath) as stockFile:
                            stockLines = stockFile.readlines()
                            for line in stockLines:
                                stock.append(re.split('\t',line.strip()))

                        stockSort = sorted(stock, key=itemgetter(0))
                        stockSkus = [line[0] for line in stockSort]

                        newdata = ""
                        for storeLine in store:
                            found = Binary_search(stockSkus,storeLine[5])
                            if found:
                                print("\t\t", storeLine[5], "has a match")
                                # TODO: Add to output data
                        # TODO: Write data to file
                        with open('''PUT FILEPATH HERE''', 'w') as txtfile:
                            txtfile.write(newdata)
                            txtfile.close()

                        # TODO: Upload to File Exchange