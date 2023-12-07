import requests
import html


class BloombergWebScraper(object):
    def __init__(self, saveLastPage=False):
        self.saveLastPage = saveLastPage
        self.session = requests.Session()
        self.session.cookies.set("CONSENT", "PENDING+400")


    def getCurrentHeadline(self, url, position):
        """
        Retrieves current headline from Bloomberg based on URL
        input: Bloomberg URL
        output: Headline
        """
        try:
            content = self.getPage(url)

            posStartHeadline = 0
            searchStringHeadline = '<div class="hover:underline focus:underline" data-component="headline">'

            for i in range(position):
                posStartHeadline = content.find(searchStringHeadline, posStartHeadline+1)
            posStartHeadline = content.find('>', posStartHeadline+len(searchStringHeadline)+1)
            posEndHeadline = content.find('<', posStartHeadline)

            headline = content[posStartHeadline+1:posEndHeadline]

            return headline
        except:
            return "ERROR"



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
    data = bloombergScraper.getCurrentHeadline("https://www.bloomberg.com/europe",30)
    #data = bloombergScraper.getCurrentHeadline("https://www.bloomberg.com/economics", 9)
    print(data)
