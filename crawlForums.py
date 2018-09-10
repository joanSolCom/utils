# -*- coding: utf-8 -*-
from lxml import etree
import os
import re
from lxml import html
import codecs
import requests
import json

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

######  Gets the full box
xpathGeneral = "//div[contains(@id,'edit')]"

######  The box has a header and a content box
xpathHeader = "./table/tr/td[@class='thead']//text()"

xpathContent = "./table/tr[@valign='top']" 

######  The content has the user info and the content/citations
xpathUser = "./td[@class='alt2']/div/a[@class='bigusername']//text()"
xpathPost = "./td[@class='alt1']/div[contains(@id,'post_message')]/text() | ./td[@class='alt1']/div[contains(@id,'post_message')]/b/text() | ./td[@class='alt1']/div[contains(@id,'post_message')]/font/text() | ./td[@class='alt1']/div[contains(@id,'post_message')]/i/text() | ./td[@class='alt1']/div[contains(@id,'post_message')]/b/i/text() | ./td[@class='alt1']/div[contains(@id,'post_message')]/a/text() | ./td[@class='alt1']/div[contains(@id,'post_message')]/i/b/text()"
xpathPostCited = "./td[@class='alt1']/div[contains(@id,'post_message')]/div/table//text()"

def stormfrontCrawl():
	entryPoints = ["https://www.stormfront.org/forum/f191-"]
	nPages = [665]
	pathBase = "/home/joan/Escritorio/Datasets/forumData/json2/"

	for idx, entryPoint in enumerate(entryPoints):
		print entryPoint
		i=1	
		url = entryPoint + str(i)+"/"

		while i <= nPages[idx]:
			print "crawling page " + str(i) + " " + url
			page = requests.get(url)
			tree = html.fromstring(page.content)
			linkList = tree.xpath("//td[@class='alt1']/div[not(@class)]/a[contains(@id,'thread_title_')]/@href")

			for link in linkList:
				posts = []

				print "crawling " + link
				idThread = link.split("/")[-2]
				j=1
				pathOut = pathBase+idThread

				urlBase = link[:-1]
				linkPage = requests.get(link)
				treeLink = html.fromstring(linkPage.content)
				maxPages = treeLink.xpath("//td[@class='alt1']/a[contains(@title,'Last Page')]/@href")

				if not maxPages:
					maxPages = 1
				else:
					maxPages = maxPages[0].split("-")[1].split("/")[0]
				k=1
				while j <= int(maxPages):
					print "page "+str(j)+ " of "+ str(maxPages)
					urlPost = urlBase+"-"+str(j)+"/"
					page = session.get(urlPost)
					tree = html.fromstring(page.content)
					boxes = tree.xpath(xpathGeneral)
					
					fname = urlBase.split("/")[-1][:-1]

					for box in boxes:
						dictPost = {}
						dictPost["page"] = j
						dictPost["idFile"] = fname
						dictPost["idFileEnriched"] = fname+"_"+str(k)+".NAF"
						header = box.xpath(xpathHeader)
						date = header[1].replace("\n","")
						dictPost["date"] = date

						if box.xpath(xpathContent):
							content = box.xpath(xpathContent)[0]
							if content.xpath(xpathUser):
								user = content.xpath(xpathUser)[0]
								dictPost["user"] = user
								
								post = " ".join(content.xpath(xpathPost)).replace("\n","").replace("\t","").strip()
								dictPost["post"] = re.sub("\s\s+" , " ", post).encode("utf-8")

								citation = " ".join(content.xpath(xpathPostCited)).replace("\n","").replace("\t","").strip()
								dictPost["citation"] = re.sub("\s\s+" , " ", citation).encode("utf-8")
								if dictPost["post"]:
									posts.append(dictPost)

								k+=1

					j+=1

				with open(pathOut, 'w') as outfile:
					json.dump(posts, outfile)
				
				print "written thread "+str(idThread)
			
			i+=1
			url = entryPoint + str(i)+"/"


stormfrontCrawl()
exit()


baseUrl = 'https://www.stormfront.org/forum/t1227535-'
MAX_PAGES = 4
i=1
posts = []
j=1
while i<=MAX_PAGES:
	urlPost = baseUrl+str(i)+"/"
	page = session.get(urlPost)
	tree = html.fromstring(page.content)
	boxes = tree.xpath(xpathGeneral)
	
	fname = baseUrl.split("/")[-1][:-1]

	for box in boxes:
		dictPost = {}
		dictPost["page"] = i
		dictPost["idFile"] = fname
		dictPost["idFileEnriched"] = fname+"_"+str(j)+".NAF"
		header = box.xpath(xpathHeader)
		date = header[1].replace("\n","")
		dictPost["date"] = date

		content = box.xpath(xpathContent)[0]

		user = content.xpath(xpathUser)[0]
		dictPost["user"] = user
		
		post = " ".join(content.xpath(xpathPost)).replace("\n","").replace("\t","").strip()
		dictPost["post"] = re.sub("\s\s+" , " ", post).encode("utf-8")

		citation = " ".join(content.xpath(xpathPostCited)).replace("\n","").replace("\t","").strip()
		dictPost["citation"] = re.sub("\s\s+" , " ", citation).encode("utf-8")

		if dictPost["post"]:
			posts.append(dictPost)
		j+=1

	i+=1

	
fname = baseUrl.split("/")[-1][:-1]
pathOut = "/home/joan/Escritorio/Datasets/forumData/json/"+fname
with open(pathOut, 'w') as outfile:
    json.dump(posts, outfile)