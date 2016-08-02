#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
import requests
from bs4 import BeautifulSoup

def search(string):
	url = 'https://www.google.com/search?q=' + string + '+structure'
	code = requests.get(url).text
	soup = BeautifulSoup(code, 'lxml')
	for link in soup.select('div > h3 > a'):
		page(link.get('href').split('?q=')[1].split('&sa')[0], string)

def page(url, string):
	code = requests.get(url).text
	soup = BeautifulSoup(code, 'lxml')
	plain = "".join(soup.findAll(text=True))
	index = plain.find('struct ' + string + ' {')
	if index != -1:
		index2 = index + plain[index:].find('}') + 1
		print(url)
		print(plain[index:index2])

search(sys.argv[1])
