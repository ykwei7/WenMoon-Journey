import requests
from bs4 import BeautifulSoup



def stock_price(stock):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}

    url = "https://finance.yahoo.com/quote/{stock}/".format(stock=stock)

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    closing_price = soup.find('td', {"class": "Ta(end) Fw(600) Lh(14px)", "data-test": "PREV_CLOSE-value"})
    opening_price = soup.find('td', {"class": "Ta(end) Fw(600) Lh(14px)", "data-test": "OPEN-value"})

    try:
        change = soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('span')[1].text
    except AttributeError:
        change = "NA"

    if(closing_price == None):
        closing_price = 0
    else:
        closing_price = remove_commas(closing_price.text)
    if(opening_price == None):
        opening_price = 0
    else:
        opening_price = remove_commas(opening_price.text)

    return([float(opening_price), float(closing_price), change])

def remove_commas(text):
    str = ""
    for x in text:
        if(x != ','):
            str += x
    return str
