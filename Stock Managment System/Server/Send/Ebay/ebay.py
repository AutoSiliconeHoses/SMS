import yaml, os, re

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
        print(storecode, "enabled")
        for supplier in config['suppliers']:
            if config['suppliers'][supplier]['enabled']:
                storePath = os.path.join("Server/Send/Ebay/StoreFiles/", storecode.upper(), supplier+"-FULLSTOCK.csv")
                if os.path.isfile(storePath):
                    print("\t", storePath)
                    # TODO: Check for new file and then binary search them together
                    
                    # store = []
                    # with open() as storeFile:
                    #     storeLines = sto.readlines()
                    #     for line in storeLines:
                    #         store.append(re.split('\t',line.strip()))

                    # stock = []
                    # with open() as stockFile:
                    #     stockLines = stoc.readlines()
                    #     for line in stockLines:
                    #         stock.append(re.split('\t',line.strip()))