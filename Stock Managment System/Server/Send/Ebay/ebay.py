import yaml, os, re, csv
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

                        newdata = []
                        newdata.append(store[0])
                        for storeLine in store:
                            if storeLine[2] is "" and storeLine[3] is "":
                                lastHeader = storeLine
                                checked = False
                            else:
                                cleanSku = re.sub(r"[\|#].*","",storeLine[5])
                                found = Binary_search(stockSkus,cleanSku)
                                if found:
                                    if storeLine[0] is "": # Requires Header
                                        if not checked:
                                            newdata.append(lastHeader)
                                            checked = True
                                    storeLine[2] = stockSort[found][1]
                                    newdata.append(storeLine)

                        # Write to outFile
                        if len(newdata) > 1:
                            outPath = os.path.join("Server/Send/Ebay/Updated", storecode.upper() + "-" + supplier + ".csv")
                            with open(outPath, "w", newline="") as f:
                                writer = csv.writer(f)
                                writer.writerows(newdata)

                        # TODO: Upload to File Exchange