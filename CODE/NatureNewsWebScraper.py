import requests
import html


class NatureNewsWebScraper(object):
    def __init__(self, saveLastPage=False):
        self.saveLastPage = saveLastPage
        self.session = requests.Session()


    def getHeadline(self, url, headlineNumber=1):
        """
        Retrieves current headline from Zeit Online besed on URL and Number of Article
        input: Nature News Url
        output: Headline of Article, Publish Time
        """
        content = self.getPage(url)

        posTitleOffset = 0
        while headlineNumber > 0:
            posTitle = content.find('<h3 class="c-card__title u-serif u-text17 u-font-weight--regular">', posTitleOffset)
            posEndTitle = content.find('<', posTitle+66)
            posTitleOffset = posEndTitle
            headlineNumber -= 1

        posTimeClass = content.find('<span class="c-card__date u-sans-serif u-text13 u-upper">')
        posTime = content.find('">', posTimeClass+16)
        posEndTime = content.find("<", posTime+2)

        headline = content[posTitle+66:posEndTitle]
        timePostet = content[posTime+2:posEndTime]

        timePostet = timePostet.split(" 20")[0]

        return headline, timePostet


    def getPage(self, url):
        """
        Pulls the web page with request
        input: Nature News URL
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
    natureScraper = NatureNewsWebScraper(True)
    print(natureScraper.getHeadline("https://www.nature.com/news", 1))