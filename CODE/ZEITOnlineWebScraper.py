import requests


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
            posTitle = content.find('</span><span class="visually-hidden">: </span><span class="zon-teaser-news__title">', posTitleOffset)
            posEndTitle = content.find('<', posTitle+84)
            posTitleOffset = posEndTitle
            headlineNumber -= 1

        posTimeClass = content.find('<time class="zon-teaser-news__date" datetime=')
        posTime = content.find('">', posTimeClass+46)
        posEndTime = content.find("<", posTime+2)

        headline = content[posTitle+83:posEndTitle]
        timePostet = content[posTime+2:posEndTime]

        return headline, timePostet


    def getPage(self, url):
        """
        Pulls the web page with request
        input: Zeit Online URL
        output: Page HTML code
        """
        response = self.session.get(url)
        if self.saveLastPage:
            with open("lastSite.html", "w") as file:
                file.write(str(response.content))
        return response.content.decode('utf-8')



if __name__ == '__main__':
    reutersScraper = ZEITOnlineWebScraper(True)
    data = reutersScraper.getHeadline("https://www.zeit.de/news/index", 3)
    print(data)
