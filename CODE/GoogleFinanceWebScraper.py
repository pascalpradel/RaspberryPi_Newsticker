import requests


class GoogleFinanceWebScraper(object):
    def __init__(self, saveLastPage=False):
        self.saveLastPage = saveLastPage
        self.session = requests.Session()
        self.session.cookies.set("CONSENT", "PENDING+229")
        self.session.cookies.set("SOCS", "CAISNQgSEitib3FfaWRlbnRpdHlmcm9udGVuZHVpc2VydmVyXzIwMjMwOTI0LjA5X3AxGgJkZSACGgYIgITTqAY")


    def getCurrentStockData(self, url):
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

            return exchange, currency, lastPrice

        except:
            return "ERROR", "ERROR", "0.0"
        

    def getCurrentIndexData(self, url):
        try:
            content =  self.getPage(url)

            posExchange = content.find('data-exchange="')
            posEndExchange = content.find('"', posExchange+16)
            posLastPoints = content.find('data-last-price="')
            posEndLastPoints = content.find('"', posLastPoints+18)

            exchange = content[posExchange+15:posEndExchange]
            lastPoints = content[posLastPoints+17:posEndLastPoints].replace(',','.')

            return exchange, lastPoints

        except:
            return "ERROR", "0.0"


    def getPage(self, url):
        response = self.session.get(url)
        if self.saveLastPage:
            with open("lastSite.html", "w") as file:
                file.write(str(response.content))
        return response.content.decode('utf-8')

"""
if __name__ == '__main__':
    financeScraper = GoogleFinanceWebScraper(True)
    data = financeScraper.getCurrentStockData("https://www.google.com/finance/quote/DAX:INDEXDB")
    print(data)
"""
