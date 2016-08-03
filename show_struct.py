#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
import requests
from bs4 import BeautifulSoup
from collections import Counter

slist = list()
number = 0

def search(string):
	url = "https://www.google.com/search?q=" + string + "+structure"
	code = requests.get(url).text
	soup = BeautifulSoup(code, "lxml")
	print("Searching...")
	for link in soup.select("div > h3 > a"):
		page(link.get("href").split("?q=")[1].split("&sa")[0], string)
	if len(slist) > 0:
		stuple = Counter(slist).most_common(1)[0]
		print("\n[*] Recommand: "+repr(stuple[1]))
		print(stuple[0])
	else:
		print("Not found "+string+" structure")

def page(url, string):
	code = requests.get(url).text
	soup = BeautifulSoup(code, "lxml")
	plain = "".join(soup.findAll(text=True))
	index = plain.find("struct "+string+" {")
	if index != -1:
		global number
		number += 1
		print("["+repr(number)+"] "+url)

		plain = plain[index:]
		index = len(string) + 9
		while True:
			n1 = plain[index:].find("{")
			n2 = plain[index:].find("}")
			index += n2 + 1
			if n1 == -1 or n1 > n2:
				index += 1
				break
		struct = plain[:index]
		print(struct)

		index = n1 = n2 = 0
		while True:
			n1 = struct[index:].find(";")
			n2 = struct[index:].find("\n")
			if n1 == -1 or n2 == -1:
				break
			while n1 > n2:
				n3 = struct[index+n2+1:].find("\n")
				n2 += n3 + 2
				if n3 == -1:
					break
			if n2 == -1:
				break
			struct = struct.replace(struct[index+n1+1:index+n2-1], "")
			index += n1 + 1
		#print(struct)
		global slist
		slist.append(struct)

def main():
	if len(sys.argv) == 2:
		search(sys.argv[1])
	else:
		print("Usage: python "+sys.argv[0]+" [structure name]")

if __name__ == "__main__":
	main()
