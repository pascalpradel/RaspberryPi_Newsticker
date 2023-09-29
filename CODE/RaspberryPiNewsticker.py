from GoogleFinanceWebScraper import GoogleFinanceWebScraper
from ReutersWebScraper import ReutersWebScraper
from LEDMatrix import LEDMatrix
import requests
import random
import json
import time


#Gloabl Consts:
DATAFILE_PATH = "displayData.json"
CONFIG_PATH = "config.json"
SHUFFLE = True

#Matrix Constants:
ROWS = 32
COLS = 128
BRIGHTNESS = 75
FONT = "fonts/Calibri-26.bdf"
TEXTCOLOR=[0, 255, 0]


class RaspiPiNewsticker(object):
    def __init__(self):
        self.displayDataList = self.readJsonData()
        self.OWM_API_KEY = self.readConfig()
        self.financeScraper = GoogleFinanceWebScraper()
        self.reutersScraper = ReutersWebScraper()
        self.ledMatrix = LEDMatrix(rows=ROWS, cols=COLS, brightness=BRIGHTNESS, font=FONT, textColor=TEXTCOLOR)

        self.iterator = 0


    def start(self):
        self.ledMatrix.setText(self.getNextText())
        while True:
            self.ledMatrix.offscreenCanvas.Clear()
            lenText = self.ledMatrix.lenText()
            self.ledMatrix.pos -= 1

            if (self.ledMatrix.pos + lenText < COLS):
                self.ledMatrix.text += self.getNextText()

            time.sleep(0.01)
            self.ledMatrix.offscreenCanvas = self.ledMatrix.matrix.SwapOnVSync(self.ledMatrix.offscreenCanvas)


    def getNextText(self):
        if len(self.displayDataList) > 0:
            if SHUFFLE:
                randNr = random.randint(0, len(self.displayDataList)-1)
                record = self.displayDataList[randNr]
                text = self.displayRecord(record)
                del self.displayDataList[randNr]
            else:
                text = self.displayRecord(self.displayDataList[self.iterator])
                self.iterator+= 1
            return text + "  "
        else:
            return None


    def displayRecord(self, record):
        if record[0] == "stock":
            exchange, currency, lastPrice, changeValue = self.financeScraper.getCurrentStockData(record[2], record[1])
            return str(record[1]) + " [" + str(exchange) + "] " + str(lastPrice) + " " + str(currency) + " ( " + str(changeValue) + ")"

        elif record[0] == "index":
            exchange, lastPoints, changeValue = self.financeScraper.getCurrentIndexData(record[2], record[1])
            return str(record[1]) + " [" + str(exchange) + "] " + str(lastPoints) + " ( " + str(changeValue) + ")"
            
        elif record[0] == "reuters":
            headline, publishedTime, publishedTimeRound = self.reutersScraper.getCurrentHeadline(record[2])
            return str(headline) + " [" + str(publishedTimeRound) + "]"

        elif record[0] == "weather":
            temp, humid = self.getWeather(record[2])
            return str(record[1]) + ": " + str(temp) + "°C &" + str(humid) + "%"


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