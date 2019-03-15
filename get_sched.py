import os
import urllib
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

BASE_SRC='https://www.hinatazaka46.com/s/official/media/list'
YEAR_SRC='2019'
MONTH_SRC='03'

FILE_DST="hinata.txt"

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
        and content_type is not None
        and content_type.find('html') > -1)

def log_error(e):
    print(e)


def main():
    global YEAR_SRC
    global MONTH_SRC

    html_link = BASE_SRC + '?' + 'dy=' + YEAR_SRC + MONTH_SRC
    raw_html = simple_get(html_link)
    html_bs = BeautifulSoup(raw_html, 'html.parser')
    list_bs = html_bs.findAll('div', {'p-schedule__list-group'})

    f = open(FILE_DST, "w+")

    for entry in list_bs:
        txt =""
        date = entry.find("span").text
        if (len(date) != 2):
            date = "0"+ date
        entry_list = entry.findAll('li', {'p-schedule__item'})
        for schedule in entry_list:
            txt = YEAR_SRC + MONTH_SRC + date
            tp = schedule.find('div', {'c-schedule__category'})
            txt = txt + ',' + tp.text.strip()
            time = schedule.find('div', {'c-schedule__time--list'}).text
            txt = txt + ',' + time.strip()
            content = schedule.find('p', {'c-schedule__text'}).text
            txt = txt + ',' + content.strip() + '\n'
            f.write(txt)
    f.close()


if __name__ == "__main__":
    main()
