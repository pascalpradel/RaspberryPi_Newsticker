import requests


class ReutersWebScraper(object):
    def __init__(self, saveLastPage=False):
        self.saveLastPage = saveLastPage
        self.session = requests.Session()
        self.session.cookies.set("CONSENT", "PENDING+229")


    def getCurrentHeadline(self, url):
        """
        Retrieves current headline from Reuters based on URL
        input: Reuters URL
        output: Headline of Article, Publish Time, Publish Time in HH:mm format
        """
        try:
            content = self.getPage(url)

            posBasicHeadline = content.find('"basic_headline":"')
            posEndBasicHeadline = content.find('"', posBasicHeadline+19)

            posPublishedTime = content.find('"published_time":"')
            posEndPublishedTime = content.find('"', posPublishedTime+19)

            headline = content[posBasicHeadline+18:posEndBasicHeadline]
            publishedTime = content[posPublishedTime+18:posEndPublishedTime]
            publishedTimeRound = publishedTime[11:16]

            return headline, publishedTime, publishedTimeRound
        except:
            return "ERROR", "ERROR", "ERROR"


    def getPage(self, url):
        """
        Pulls the web page with request
        input: Reuters URL
        output: Page HTML code
        """
        response = self.session.get(url)
        if self.saveLastPage:
            with open("lastSite.html", "w") as file:
                file.write(str(response.content))
        return response.content.decode('utf-8')

"""
if __name__ == '__main__':
    reutersScraper = ReutersWebScraper(True)
    data = reutersScraper.getCurrentHeadline("https://www.reuters.com/breakingviews/")
    print(data)
"""