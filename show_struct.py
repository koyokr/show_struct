#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
import requests
from bs4 import BeautifulSoup
from collections import Counter

slist = list()

def search(string):
	url = 'https://www.google.com/search?q=' + string + '+structure'
	code = requests.get(url).text
	soup = BeautifulSoup(code, 'lxml')
	for link in soup.select('div > h3 > a'):
		page(link.get('href').split('?q=')[1].split('&sa')[0], string)
	#print(Counter(slist))
	print(Counter(slist).keys()[0])

def page(url, string):
	code = requests.get(url).text
	soup = BeautifulSoup(code, 'lxml')
	plain = ''.join(soup.findAll(text=True))
	index = plain.find('struct '+string+' {')
	if index != -1:
		index2 = index + len(string) + 9
		while True:
			n1 = plain[index2:].find('{')
			n2 = plain[index2:].find('}')
			index2 += n2 + 1
			if n1 == -1 or n1 > n2:
				index2 += 1
				break
		struct = plain[index:index2]
		print(url)
		#print(struct)

		index = n1 = n2 = 0
		while True:
			n1 = struct[index:].find(';')
			n2 = struct[index:].find('\n')
			if n1 == -1 or n2 == -1:
				break
			while n1 > n2:
				n2 += struct[n2:].find('\n') + 1
				if n2 == -1:
					break
			if n2 == -1:
				break
			struct = struct.replace(struct[index+n1+1:index+n2-1], '')
			index += n1 + 1
		#print(struct)

		slist.append(struct)

def main(string):
	search(string)

if __name__ == '__main__':
	main(sys.argv[1])
