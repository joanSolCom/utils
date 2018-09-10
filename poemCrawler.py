# -*- coding: utf-8 -*-
from lxml import etree
import os
import re
from lxml import html
import codecs
import requests
from string import ascii_lowercase

baseUrl = 'http://www.dictionary.com/list/'

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

baseUrl = "https://www.poemhunter.com"
url = "https://www.poemhunter.com/dorothy-parker/poems/page-"

links = []
i=1

while i < 6:
	completeUrl = url + str(i)+"/?a=a&l=3&y="
	page = session.get(completeUrl)
	tree = html.fromstring(page.content)
	l = tree.xpath("//table[@class='poems']/tbody/tr/td[@class='title']/a/@href")
	links.extend(l)
	i+=1

idx = 1
author = "dorothyParker"
gender = "female"
outPath = "/home/joan/Escritorio/Datasets/poetry/clean/"

for link in links:
	fullUrl = baseUrl+link
	page = session.get(fullUrl)
	tree = html.fromstring(page.content)
	poem = tree.xpath("//div[@class='KonaBody']/p")
	htmlContent = etree.tostring(poem[0], pretty_print=True)
	text = htmlContent.replace("<br/>","\n")
	text = text.replace("&#13;","").replace("</p>","").replace("&#13;","").replace("<p>","").replace("&#8212;","").replace("—","-").replace("&#8201;","").replace("&#8217;","").replace("``","").replace("</ae>","").replace("<ae>","").strip()
	text = re.sub("(.*I\.\n)|(.*V\.\n)|(.*X\.\n)","",text)
	text = re.sub('\n{2,}','\n\n',text)

	poemName = link.replace("/poem/","").replace("-","").replace("/","")
	fname = "_".join([str(idx),poemName,author,gender])
	fd = open(outPath+fname,"w")
	fd.write(text)
	fd.close()
	idx+=1
