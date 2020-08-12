#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import string


def clean_entry(entry):
    asciis = set(string.printable)
    clean = ''.join(filter(lambda x: x in asciis, entry))  # remove non-ascii
    replace_dict = {' ': '', 'www.': '', 'ru.': ''}
    for (k, v) in replace_dict.items():
        clean = clean.replace(k, v)
    return clean


def find_url(entry):
    url = re.findall(r"[-\w]*[.]{1}\w+", entry)
    if url:
        return url[0]


def parse_page(page):
    soup = BeautifulSoup(open(page), 'html.parser')
    table = soup.table.tbody
    rows = table.find_all('tr')
    print ('Rows in table:', len(rows))

    urls = []
    for tr in rows:
        td = tr.find_all('td')
        if td:
            url = find_url(clean_entry(td[0].text))
            if url:
                urls.append(url.lower())
    return urls

urls1 = parse_page("./mgf.html")  # save http://moy-m-portal.ru as mgf.html
urls2 = parse_page("./podpiski.html") # save http://www.podpiskimf.ru as podpiski.html
urls = list(set(urls1+urls2))
urls.sort()
print ('URLs in hosts:', len(urls))

with open('hosts', 'w') as hosts:
    for url in urls:
        hosts.write("0.0.0.0 " + url + '\n')
