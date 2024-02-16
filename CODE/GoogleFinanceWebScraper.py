from datetime import datetime
import requests
import json


DATAZIP = ["name", "value", "lastChange"]


class GoogleFinanceWebScraper(object):
    def __init__(self, stockDataCachePath = "stockDataCache.json", saveLastPage=False):
        self.saveLastPage = saveLastPage
        self.stockDataCachePath = stockDataCachePath
        self.session = requests.Session()
        self.session.cookies.set("CONSENT", "PENDING+229")
        self.session.cookies.set("SOCS", "CAISNQgSEitib3FfaWRlbnRpdHlmcm9udGVuZHVpc2VydmVyXzIwMjMwOTI0LjA5X3AxGgJkZSACGgYIgITTqAY")

        self.startTimestamp = datetime.now().day
        self.stockDataCacheList = self.loadStockDataCache()


    def getCurrentStockData(self, url, name):
        """
        Scraper function for stock values at Google Finance
        input: Google Finance URL and name of stock
        output: exchange, currency, price, difference in % to last day
        """
        try:
            content =  self.getPage(url)

            posExchange = content.find('data-exchange="')
            posEndExchange = content.find('"', posExchange+16)
            posCurrency = content.find('data-currency-code="')
            posEndCurrency = content.find('"',posCurrency+21)
            posLastPrice = content.find('data-last-price="')
            posEndLastPrice = content.find('"', posLastPrice+18)

            exchange = content[posExchange+15:posEndExchange]
            currency = content[posCurrency+20:posEndCurrency]
            lastPrice = content[posLastPrice+17:posEndLastPrice].replace(',','.')

            cachePrice = self.updateStockDataCacheList(name, lastPrice)
            self.saveStockDataCacheList()

            return exchange, currency, self.roundIfNecessary(lastPrice), self.calculateDifference(float(lastPrice), float(cachePrice))

        except:
            return "ERROR", "ERROR", "0.0", "ERROR"
        

    def getCurrentIndexData(self, url, name):
        """
        Scraper function for index values or crypto at Google Finance
        input: Google Finance URL and name of index/crypto
        output: exchange, price/points, difference in % to last day
        """
        try:
            content =  self.getPage(url)

            posExchange = content.find('data-exchange="')
            posEndExchange = content.find('"', posExchange+16)
            posLastPoints = content.find('data-last-price="')
            posEndLastPoints = content.find('"', posLastPoints+18)

            exchange = content[posExchange+15:posEndExchange]
            lastPoints = content[posLastPoints+17:posEndLastPoints].replace(',','.')

            cachePoints = self.updateStockDataCacheList(name, lastPoints)
            self.saveStockDataCacheList()

            return exchange, self.roundIfNecessary(lastPoints), self.calculateDifference(float(lastPoints), float(cachePoints))

        except:
            return "ERROR", "0.0", "ERROR"


    def getPage(self, url):
        """
        Pulls the web page with request
        input: Google Finance URL
        output: Page HTML code
        """
        response = self.session.get(url)
        if self.saveLastPage:
            with open("lastSite.html", "w") as file:
                file.write(str(response.content))
        return response.content.decode('utf-8')
    

    def calculateDifference(self, value, cachedValue):
        """
        Calulates to difference to last day
        Input: Current Value, Last Value
        output: Formattet string with difference
        """
        change = ((value - cachedValue) / cachedValue) * 100
        if value-cachedValue >= 0:
            return "+" + str(round(change,1)) + "%"
        else:
            return str(round(change,1)) + "%"
    

    def loadStockDataCache(self):
        """
        Reads Cached Data Json
        input: /
        output: Cached Data List
        """
        try:
            file = open(self.stockDataCachePath, "r")
            jsonData = json.load(file)
            file.close()

            stockDataCache = []
            for stock in jsonData["stockValues"]:
                record = [stock["name"], stock["value"], stock["lastChange"]]
                stockDataCache.append(record)
            
            return stockDataCache
        except:
            return []
    

    def updateStockDataCacheList(self, stockName, stockValue):
        """
        Updates the Value in Cached Data Json
        input: Name of Stock/Index, Value of Stock/Index
        output: Value of Stock/Index
        """
        foundFlag = False
        for stock in self.stockDataCacheList:
            if stock[0] == stockName:
                foundFlag = True
                if stock[2] != self.startTimestamp:
                    oldValue = stock[1]
                    stock[1] = stockValue
                    stock[2] = self.startTimestamp
                    return oldValue
                else:
                    return stock[1]
        if foundFlag == False:
            self.stockDataCacheList.append([stockName, stockValue, self.startTimestamp])
        return stockValue


    def saveStockDataCacheList(self):
        """
        Dumps List Back to Json File
        """
        stockDicList = []
        for stock in self.stockDataCacheList:
            stockDicList.append(dict(zip(DATAZIP, stock)))

        cacheDicList = dict(zip(["stockValues"], [stockDicList]))
        with open(self.stockDataCachePath, "w") as file:
            json.dump(cacheDicList, file, indent=2)


    def roundIfNecessary(self, inputString):
        """
        Rounds if more than two decimal places
        input: float as string
        output: string (rounded)
        """
        parts = inputString.split(".")
        
        if len(parts) > 1 and len(parts[1]) > 2:
            rounded_value = round(float(inputString), 2)
            return str(rounded_value)
        else:
            return inputString


if __name__ == '__main__':
    financeScraper = GoogleFinanceWebScraper()
    print(financeScraper.getCurrentStockData("https://www.google.com/finance/quote/SIE:ETR", "Siemens"))
    print(financeScraper.getCurrentIndexData("https://www.google.com/finance/quote/BTC-EUR", "Bitcoin"))
