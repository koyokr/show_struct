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
	index = plain.find('struct '+string+' {')
	if index != -1:
		length = 9 + len(string)
		index2 = index + length
		n1 = plain[index2:].find('{')
		n2 = plain[index2:].find('}')
		index2 += n2 + 1
		if n1 < n2 and n1 != -1:
			while True:
				n1 = plain[index2:].find('{')
				n2 = plain[index2:].find('}')
				index2 += n2 + 1
				if n1 > n2 or n1 == -1:
					index2 += 1
					break;
		print(url)
		print(plain[index:index2])

def main(string):
	search(string)

if __name__ == '__main__':
	main(sys.argv[1])
