import requests
import html


class ZEITOnlineWebScraper(object):
    def __init__(self, saveLastPage=False):
        self.saveLastPage = saveLastPage
        self.session = requests.Session()


    def getHeadline(self, url, headlineNumber=1):
        """
        Retrieves current headline from Zeit Online besed on URL and Number of Article
        input: Zeit Online URL
        output: Headline of Article, Publish Time
        """
        content = self.getPage(url)

        posTitleOffset = 0
        while headlineNumber > 0:
            posTitle = content.find('<span class="visually-hidden">: </span><span class="zon-teaser__title zon-teaser__title--small">', posTitleOffset)
            posEndTitle = content.find('<', posTitle+96)
            posTitleOffset = posEndTitle
            headlineNumber -= 1

        posTimeClass = content.find('<time datetime="')
        posTime = content.find('">', posTimeClass+16)
        posEndTime = content.find("<", posTime+2)

        headline = content[posTitle+96:posEndTitle]
        timePostet = content[posTime+2:posEndTime]

        return headline, timePostet


    def getPage(self, url):
        """
        Pulls the web page with request
        input: Zeit Online URL
        output: Page HTML code
        """
        response = self.session.get(url)
        response = response.content.decode('utf-8')
        response = html.unescape(response)

        if self.saveLastPage:
            with open("lastSite.html", "w", encoding='utf-8') as file:
                file.write(str(response))
        return response



if __name__ == '__main__':
    reutersScraper = ZEITOnlineWebScraper(True)
    print(reutersScraper.getHeadline("https://www.zeit.de/news/index", 1))
