import xml.etree.ElementTree as ET
import requests
import html


class TheEconomistWebScraper(object):
    def __init__(self, saveLastPage=False):
        self.saveLastPage = saveLastPage
        self.session = requests.Session()


    def getCurrentHeadline(self, url, position):
        """
        Retrieves current headline from Bloomberg based on URL
        input: The Economist URL
        output: Headline, timestamp posted
        """
        try:
            content = self.getPage(url)
            content = content.replace('&', '&amp;')
            root = ET.fromstring(content)
            items = []

            for item in root.findall(".//item"):
                entry = {
                    "title": item.findtext("title"),
                    #"link": item.findtext("link"),
                    "description": item.findtext("description"),
                    #"guid": item.findtext("guid"),
                    "pubDate": item.findtext("pubDate")
                }
                items.append(entry)

            returnItem = items[position]
            splitList = returnItem['pubDate'].split(" ")
            timePostet = splitList[1] + " " + splitList[2] + " " + splitList[4][:5]
            headline = html.unescape(returnItem['title'])
            
            return headline, timePostet
        except:
            return "ERROR", "ERROR"



    def getPage(self, url):
        """
        Pulls the web page with request
        input: Economist URL
        output: Page HTML code
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = self.session.get(url, headers=headers)
        response = response.content.decode('utf-8')
        response = html.unescape(response)


        if self.saveLastPage:
            with open("lastSite.html", "w", encoding='utf-8') as file:
                file.write(str(response))
        return response


if __name__ == '__main__':
    economistScraper = TheEconomistWebScraper(True)
    headline, timePostet = economistScraper.getCurrentHeadline("https://www.economist.com/business/rss.xml", 1) #https://www.economist.com/rss
    print(headline, timePostet)
