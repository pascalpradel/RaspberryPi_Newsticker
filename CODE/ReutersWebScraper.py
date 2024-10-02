import xml.etree.ElementTree as ET
import requests
import html


class ReutersWebScraper(object):
    def __init__(self, saveLastPage=False):
        self.saveLastPage = saveLastPage
        self.session = requests.Session()
    

    def getCurrentHeadline(self, url, position):
        """
        Retrieves current headline from Reuters based on URL
        input: Reuters URL, position
        output: Headline of Article, Publish Time
        """

        try:
            content = self.getPage(url)
            content = content.replace('&', '&amp;')
            root = ET.fromstring(content)
            items = []

            for item in root.findall(".//item"):
                entry = {
                    "title": item.findtext("title"),
                    "link": item.findtext("link"),
                    #"creator": item.findtext("{http://purl.org/dc/elements/1.1/}creator"),
                    "pubDate": item.findtext("pubDate"),
                    #"guid": item.findtext("guid"),
                    "description": item.findtext("description"),
                    #"content": item.findtext("{http://purl.org/rss/1.0/modules/content/}encoded")
                }
                items.append(entry)
            
            returnItem = items[position]
            headline = html.unescape(returnItem["title"])
            splitList = returnItem['pubDate'].split(" ")
            timePostet = splitList[1] + " " + splitList[2] + " " + splitList[4][:5]
            
            return headline, timePostet

        except:
            return "ERROR", "ERROR"


    def getPage(self, url):
        """
        Pulls the web page with request
        input: Reuters URL
        output: Page HTML code
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = self.session.get(url, headers=headers)
        if self.saveLastPage:
            with open("lastSite.html", "w") as file:
                file.write(str(response.content))
        return response.content.decode('utf-8')


if __name__ == '__main__':
    reutersScraper = ReutersWebScraper(True)
    #headline, publishedTime = reutersScraper.getCurrentHeadline("https://www.reutersagency.com/feed/?taxonomy=best-sectors&post_type=best", 1) #https://www.reutersagency.com/en/reutersbest/reuters-best-rss-feeds/
    headline, publishedTime = reutersScraper.getCurrentHeadline("https://www.reutersagency.com/feed/?best-topics=health&post_type=best", 3)
    print(headline, publishedTime)
