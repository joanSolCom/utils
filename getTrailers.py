
# -*- coding: utf-8 -*-
from lxml import etree
import os
from lxml import html
import requests
import codecs

outPath = "./trailers/"
session = requests.Session()

headers = {
	    'Accept-Encoding': 'gzip, deflate, sdch',
	    'Accept-Language': 'en-US,en;q=0.8',
	    'Upgrade-Insecure-Requests': '1',
	    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	    'Cache-Control': 'max-age=0',
	    'Connection': 'keep-alive',
	}
session.headers = headers

lines = codecs.open("acumLinks.tsv","r",encoding="utf-8").read().split("\n")
fdOut = open("linksWithVideo.tsv","a")
withLink = 0
nLines = len(lines)

dondemequedao = 613749

for idx, line in enumerate(lines):
	if idx < dondemequedao:
		print "Skipping link "+str(idx)
		continue

	print idx
	columns = line.split("\t")
	link = columns[0]
	try:
		page = session.get(link)
	except BaseException as e:
		print link
		print e
		exit() 
	tree = html.fromstring(page.content)
	trailerLink = tree.xpath("//div[@class='slate']/a[@itemprop='trailer']/@href")
	movieName = tree.xpath("//div[@class='title_wrapper']/h1[@itemprop='name']/text()")
	if movieName:
		movieName = movieName[0].strip()
	else:
		continue
	if trailerLink:
		videoLink = "https://www.imdb.com" + trailerLink[0]
		fdOut.write(line.encode("utf-8")+"\t"+movieName.encode("utf-8")+"\t"+videoLink+"\n")
		withLink+=1
		print str(withLink) + " of "+ str(nLines) +" with trailer"

fdOut.close()
