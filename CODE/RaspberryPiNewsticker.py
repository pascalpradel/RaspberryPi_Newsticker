import json
import random
import requests
from GoogleFinanceWebScraper import GoogleFinanceWebScraper
from ReutersWebScraper import ReutersWebScraper


#Gloabl Consts:
DATAFILE_PATH = "displayData.json"
CONFIG_PATH = "config.json"
SHUFFLE = False


class RaspiPiNewsticker(object):
    def __init__(self):
        self.displayDataList = self.readJsonData()
        self.OWM_API_KEY = self.readConfig()
        self.financeScraper = GoogleFinanceWebScraper()
        self.reutersScraper = ReutersWebScraper()


    def start(self):
        if SHUFFLE:
            while len(self.displayDataList) > 0:
                randNr = random.randint(0, len(self.displayDataList)-1)
                record = self.displayDataList[randNr]
                self.displayRecord(record)
                del self.displayDataList[randNr]
        else:
            for record in self.displayDataList:
                self.displayRecord(record)


    def displayRecord(self, record):
        if record[0] == "stock":
            print(self.financeScraper.getCurrentStockData(record[2]), record[1])
        elif record[0] == "index":
            print(self.financeScraper.getCurrentIndexData(record[2]), record[1])
        elif record[0] == "reuters":
            print(self.reutersScraper.getCurrentHeadline(record[2]), record[1])
        elif record[0] == "weather":
            print(self.getWeather(record[2]), record[1])



    def getWeather(self, city):
        url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + self.OWM_API_KEY + "&units=metric"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            main_data = data['main']
            temperature = main_data['temp']
            humidity = main_data['humidity']

            return temperature, humidity
        else:
            return "ERROR", "ERROR"




    def readJsonData(self):
        file = open(DATAFILE_PATH, "r")
        jsonData = json.load(file)
        file.close()

        dataList = []
        for data in jsonData["dataList"]:
            dataRecord = [data["type"], data["topic"], data["url"]]
            dataList.append(dataRecord)

        return dataList
    

    def readConfig(self):
        file = open(CONFIG_PATH, "r")
        jsonData = json.load(file)
        file.close()

        keyList = []
        for keys in jsonData["KEYS"]:
            keyList.append(keys["KEY"])
        return keyList[0]




if __name__ == '__main__':
    ticker = RaspiPiNewsticker()
    ticker.start()