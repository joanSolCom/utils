# -*- coding: utf-8 -*-
from lxml import etree
import os
import re
from lxml import html
import codecs
import requests
from string import ascii_lowercase

baseUrl = 'https://www.imdb.com/feature/genre/?ref_=tt_ov_inf'

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

page = session.get(baseUrl)
tree = html.fromstring(page.content)

genres = tree.xpath("//div[@class='widget_image']/div[@class='image']/a/@href")
baseUrl = "https://www.imdb.com/search/title"
baseUrlMovie = "https://www.imdb.com"
outDir = "/home/joan/Escritorio/IMDBCorpus/"

for genreLink in genres:
	genreName = genreLink.split("?")[1].split("&")[0].replace("genres=","").replace("keywords=","")

	pageGenre = session.get(genreLink)
	treePage = html.fromstring(pageGenre.content)

	done = False
	fd = open(outDir+genreName,"w")

	while not done:
		listMovies = treePage.xpath("//h3[@class='lister-item-header']/a/@href")
		for movie in listMovies:
			fd.write(baseUrlMovie+movie+"\n")

		linkNext = treePage.xpath("//div[@class='desc']/a[contains(@class,'next-page')]/@href")

		if len(linkNext) >0:
			linkNextComplete = baseUrl + linkNext[0]
			pageMovies = session.get(linkNextComplete)
			treePage = html.fromstring(pageMovies.content)
		else:
			done = True
	
	fd.close()
