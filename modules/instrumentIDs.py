import string
import requests
from bs4 import BeautifulSoup

class InstrumentIds:

    def getInstrumentIds(self, exchange, Url=None, file=None):
        if Url is None and file is None:
            print('before')
            print(exchange)
            print('after')
# default case: use eoddata.com
            alpha = list(string.ascii_uppercase)
            symbols = []
            for each in alpha:
                url = "http://eoddata.com/stocklist/" + exchange + "/{}.htm".format(each)
                resp = requests.get(url)
                site = resp.content
                soup = BeautifulSoup(site, 'html.parser')
                table = soup.find('table', {'class': 'quotes'})
                for row in table.findAll('tr')[1:]:
                    symbols.append(row.findAll('td')[0].text.rstrip())
            return symbols

if __name__ == '__main__':
    iIds = InstrumentIds()
    idList = iIds.getInstrumentIds('LSE')
    print(idList)