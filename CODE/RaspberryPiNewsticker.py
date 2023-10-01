from GoogleFinanceWebScraper import GoogleFinanceWebScraper
from ZEITOnlineWebScraper import ZEITOnlineWebScraper
from ReutersWebScraper import ReutersWebScraper
from datetime import datetime, timedelta
from LEDMatrix import LEDMatrix
import threading
import requests
import random
import json



#Gloabl Consts:
DATAFILE_PATH = "displayData.json"
CONFIG_PATH = "config.json"
SHUFFLE = True
LIVEREQUEST = True #not recommended on Pi Zero
STOPTIME = 22 #Uhr
SHOWTIMECYCLE = True
TIMECYCLE = 5 #shows current time every x news, only available in LIVEREQUEST Mode

#Matrix Constants:
ROWS = 32
COLS = 192
BRIGHTNESS = 35
FONT = "fonts/Calibri-26.bdf"
TEXTCOLOR=[0, 155, 0]



class RaspiPiNewsticker(object):
    def __init__(self):
        self.displayDataList = self.readJsonData()
        self.OWM_API_KEY = self.readConfig()
        self.financeScraper = GoogleFinanceWebScraper()
        self.reutersScraper = ReutersWebScraper()
        self.zeitScraper = ZEITOnlineWebScraper()
        self.ledMatrix = LEDMatrix(rows=ROWS, cols=COLS, brightness=BRIGHTNESS, font=FONT, textColor=TEXTCOLOR)

        self.iterator = 0
        self.newText = ""
        self.stopThreadCreationFlag = False
        self.newTextFlag = False

        print("Started at ", datetime.now())


    def start(self):
        if LIVEREQUEST:
            self.ledMatrix.text = self.getNextText()
            timeCycle = TIMECYCLE
            while True:
                self.ledMatrix.offscreenCanvas.Clear()
                lenText = self.ledMatrix.lenText()
                self.ledMatrix.pos -= 1

                if (self.ledMatrix.pos + lenText < COLS*4):
                    if self.stopThreadCreationFlag == False:
                        if timeCycle >= 0 and SHOWTIMECYCLE:
                            self.stopThreadCreationFlag = True
                            threading.Thread(target=self.threadAddNextText).start()
                            timeCycle -= 1
                        else:
                            self.ledMatrix.text+= " " + datetime.now().strftime('%H:%M') + " Uhr  "
                            timeCycle = TIMECYCLE

                if self.newTextFlag:
                    if self.newText != None:
                        self.ledMatrix.text += self.newText
                        self.newTextFlag = False

                self.customSleep(0.015)

                self.ledMatrix.offscreenCanvas = self.ledMatrix.matrix.SwapOnVSync(self.ledMatrix.offscreenCanvas)

        else:
            self.requestAll()
            while True:
                self.ledMatrix.offscreenCanvas.Clear()
                lenText = self.ledMatrix.lenText()
                self.ledMatrix.pos -= 1

                if (self.ledMatrix.pos + lenText < COLS):
                    if SHUFFLE:
                        self.displayDataList = self.readJsonData()
                    else:
                        self.iterator = 0
                    self.ledMatrix.text = ""
                    self.requestAll()
                    self.ledMatrix.pos = self.ledMatrix.offscreenCanvas.width

                self.customSleep(0.015)

                self.ledMatrix.offscreenCanvas = self.ledMatrix.matrix.SwapOnVSync(self.ledMatrix.offscreenCanvas)


    def getNextText(self):
        if len(self.displayDataList) > 0 or self.iterator > len(self.displayDataList):
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
            if LIVEREQUEST:
                #self.ledMatrix.text = ""
                if SHUFFLE:
                    self.displayDataList = self.readJsonData()
                else:
                    self.iterator = 0
            else:
                return None
        

    def threadAddNextText(self):
        self.newText = self.getNextText()
        self.newTextFlag = True
        self.stopThreadCreationFlag = False


    def displayRecord(self, record):
        if record[0] == "stock":
            exchange, currency, lastPrice, changeValue = self.financeScraper.getCurrentStockData(record[2], record[1])
            return str(record[1]) + " [" + str(exchange) + "] " + str(lastPrice) + " " + str(currency) + " ( " + str(changeValue) + ")"

        elif record[0] == "index":
            exchange, lastPoints, changeValue = self.financeScraper.getCurrentIndexData(record[2], record[1])
            return str(record[1]) + " [" + str(exchange) + "] " + str(lastPoints) + " (" + str(changeValue) + ")"
            
        elif record[0] == "reuters":
            headline, publishedTime, publishedTimeRound = self.reutersScraper.getCurrentHeadline(record[2])
            return str(headline) + " [" + str(publishedTimeRound) + "]"

        elif record[0] == "weather":
            temp, humid = self.getWeather(record[2])
            return str(record[1]) + ": " + str(temp) + "°C, " + str(humid) + "%" + " rH"
        
        elif record[0] == "ZeitOnline":
            headline, timePostet = self.zeitScraper.getHeadline(record[2], int(record[1]))
            return " " + headline + " [" + timePostet + "]"


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
    

    def customSleep(self, seconds):
        endTime = datetime.now() + timedelta(seconds=seconds)
        while datetime.now() < endTime:
            pass


    def requestAll(self):
        while True:
            nextText = self.getNextText()
            if nextText != None:
                self.ledMatrix.text += nextText
            else:
                break



if __name__ == '__main__':
    ticker = RaspiPiNewsticker()
    ticker.start()