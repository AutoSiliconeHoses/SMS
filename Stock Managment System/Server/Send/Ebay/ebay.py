import yaml, os, re, csv, requests
from bs4 import BeautifulSoup
from operator import itemgetter

# Used for finding skus in stockfile
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

# Used to find text in HTML
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

with open("config.yml", 'r') as cfg:
    config = yaml.load(cfg, Loader=yaml.FullLoader)

class EbayAPI():
    def process(self, suppliers, upload=True):
        for storecode in config['ebay']: # Loop through enabled stores
            if config['ebay'][storecode]['enabled']:
                print(storecode.upper())
                for supplier in suppliers: # Loop through enabled suppliers
                    if config['suppliers'][supplier]['enabled']:
                        storePath = os.path.join("Server/Send/Ebay/StoreFiles/", storecode.upper(), supplier+"-FULLSTOCK.csv")
                        if os.path.isfile(storePath): # Check for matching files
                            stockPath = os.path.join("Server/Send/StockFiles/", supplier + ".tsv")
                            if os.path.isfile(stockPath):
                                print("\t", supplier, end=" ")

                                # Load both files into lists
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

                                # Setup reference variables
                                stockSort = sorted(stock, key=itemgetter(0))
                                stockSkus = [line[0] for line in stockSort]

                                newdata = []
                                newdata.append(store[0])
                                for storeLine in store[1:-1]: # Begin building newdata
                                    if storeLine[2] is "" and storeLine[3] is "": # Check for header
                                        lastHeader = storeLine[0:6]
                                        checked = False
                                    else:
                                        splitList = re.split(r"\+",storeLine[5]) # Seperates combined special skus
                                        splitInts = []
                                        for splitItem in splitList:
                                            multiDiv = re.search(r"(?<=#)\d*", splitItem) # Get divider number
                                            if multiDiv is None:
                                                multiDiv = 1
                                            else:
                                                multiDiv = int(multiDiv.group(0))
                                            cleanSku = re.sub(r"[\|#].*","",splitItem) # Clean the sku ready for search. TODO: Change weird supplier skus
                                            found = Binary_search(stockSkus,cleanSku)
                                            if found:
                                                if storeLine[0] is "": # Adds Header if neccasary
                                                    if not checked:
                                                        newdata.append(lastHeader)
                                                        checked = True
                                                splitVal = int(int(stockSort[found][1])/multiDiv) # Divide stock number by divider and floor
                                                splitInts.append(splitVal)
                                                if splitItem is splitList[-1]: # Check if last value in splitlist. NOTE: Will not append with broken skus, this might be a good thing
                                                    storeLine[2] = min(splitInts)
                                                    newdata.append(storeLine[0:6])
                                            else: # Essentially zeroes the entire line, but with maths. NOTE: Can be changed to two lines, but I like it
                                                if storeLine[0] is "": # Adds Header if neccasary
                                                    if not checked:
                                                        newdata.append(lastHeader)
                                                        checked = True
                                                splitVal = 0 # Zero sku
                                                splitInts.append(splitVal)
                                                if splitItem is splitList[-1]: # Check if last value in splitlist. NOTE: Will not append with broken skus, this might be a good thing
                                                    storeLine[2] = min(splitInts)
                                                    newdata.append(storeLine[0:6])

                                # Check to make sure there is data
                                if len(newdata) > 1:
                                    # Write to file
                                    outPath = os.path.join("Server/Send/Ebay/Updated", storecode.upper() + "-" + supplier + ".csv")
                                    with open(outPath, "w", newline="") as f:
                                        writer = csv.writer(f)
                                        writer.writerows(newdata)
                                    if upload:
                                        # Send file data in bytes along with token to eBay
                                        url = 'https://bulksell.ebay.com/ws/eBayISAPI.dll?FileExchangeUpload'
                                        data = { 'token' : config['ebay'][storecode]['token'] }
                                        files = {'file': open(outPath,'rb')}
                                        r = requests.post(url, data=data, files=files)

                                        # Parse HTML response data and get text
                                        soup = BeautifulSoup(r.content, features="html.parser")
                                        data = soup.findAll(text=True)
                                        
                                        # Get result from parsed html
                                        result = filter(visible, data)
                                        cleanResult = list(result)[2].strip()
                                        print("-> ", cleanResult)
                                        
                                        # Fetching the reference ID
                                        refIdRE = re.search(r"(?<=File upload successful. Your ref # is )\d*", cleanResult)
                                        if refIdRE is not None:
                                            refId = int(refIdRE.group(0))
                                            # TODO: Download Reports using refId
                                    else:
                                        print("-> File Complete")
                                else:
                                    print("-> No matches found")

                            