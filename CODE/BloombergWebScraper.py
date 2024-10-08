import xml.etree.ElementTree as ET
import requests
import html


class BloombergWebScraper(object):
    def __init__(self, saveLastPage=False):
        self.saveLastPage = saveLastPage
        self.session = requests.Session()


    def getCurrentHeadline(self, url, position):
        """
        Retrieves current headline from Bloomberg based on URL
        input: Bloomberg URL, position
        output: Headline, timePostet
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
                    "pubDate": item.findtext("pubDate"),
                    #"author": item.findtext("{http://www.itunes.com/dtds/podcast-1.0.dtd}author"),
                    #"subtitle": item.findtext("{http://www.itunes.com/dtds/podcast-1.0.dtd}subtitle"),
                    #"summary": item.findtext("{http://www.itunes.com/dtds/podcast-1.0.dtd}summary"),
                    #"duration": item.findtext("{http://www.itunes.com/dtds/podcast-1.0.dtd}duration"),
                    #"guid": item.findtext("guid")
                }
                items.append(entry)

            returnItem = items[position]
            headline = html.unescape(returnItem['title'])
            splitList = returnItem['pubDate'].split(" ")
            timePostet = splitList[1] + " " + splitList[2] + " " + splitList[4][:5]
            return headline, timePostet
        
        except ET.ParseError as e:
            print(f"Fehler beim Parsen des XML-Dokuments: {e}")
        except:
            return "ERROR", "ERROR"



    def getPage(self, url):
        """
        Pulls the web page with request
        input: Bloomberg URL
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
    bloombergScraper = BloombergWebScraper(True)
    data = bloombergScraper.getCurrentHeadline("https://feeds.megaphone.fm/BLM8578726790", 3)
    print(data)
