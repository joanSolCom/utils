# -*- coding: utf-8 -*-

from __future__ import division
import os
import codecs
from nltk import word_tokenize
import requests
from lxml import html
import time
from scandroid2.syllables import Syllabizer


path = "/home/joan/Escritorio/Datasets/LiteraryMerged/chapter_divided/"
pathDump = "/home/joan/repository/cleanElasticDump.tsv"

def loadDump():

	dictTranscripts = {}

	fd = codecs.open(pathDump,"r",encoding="utf-8")

	lines = fd.read().split("\n")
	print "loading dict"
	for line in lines:
		if line:
			pieces = line.split("\t")
			word = pieces[0]
			dictTranscripts[word] = {}
			dictTranscripts[word]["ipa"] = pieces[1]
			dictTranscripts[word]["syllables"] = pieces[2]
			dictTranscripts[word]["syllablesComputed"] = pieces[3]
			dictTranscripts[word]["spell"] = pieces[4]

	fd.close()
	print "loaded dict"
	return dictTranscripts



i=0
notFound = set()
d = loadDump()
for fname in os.listdir(path):

	txt = codecs.open(path+fname,"r",encoding="utf-8").read()
	#tokens = word_tokenize(txt)
	tokens = txt.split()
	nCovered = 0
	
	cache = {}
	start = time.time()

	for token in tokens:
		token = token.lower().replace(".","").replace(",","").replace("'","").replace("[","").replace("]","").replace("!","").replace('"',"").replace(";","").replace("?","").replace("(","").replace(")","").replace(":","")
		if token:
			if token in cache:
				nCovered+=1
			else:
				obj = d.get(token)
				if not obj:
					if "-" in token:
						together = token.replace("-","")
						obj2 = d.get(token)
						if not obj2:
							separated = token.split("-")
							for sep in separated:
								tokens.append(sep)
						else:
							nCovered+=1
					elif token.endswith("s"):
						token = token[:-1]
						tokens.append(token)
					else:
						notFound.add(token)
					
				else:
					cache[token] = obj
					nCovered+=1

		else:
			nCovered+=1
	
	nTokens = len(tokens)
	print "Coverage on file "+fname+" is "+ str(nCovered/nTokens)
	print len(notFound)
	end = time.time()
	print(end - start)
	i+=1

ahUrlBase = "http://lingorado.com/ipa/"
session = requests.Session()
session.max_redirects = 10000000000
headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded'
}
session.headers = headers

fd = codecs.open(pathDump,"a",encoding="utf-8")
S = Syllabizer()

for token in notFound:
	print token
	data = {'text_to_transcribe': token, 'submit': 'Show transcription','output_dialect':'br','output_style':'only_tr'}
	page = session.post(ahUrlBase,data=data)
	tree = html.fromstring(page.content)
	ipa = tree.xpath("//div[@id='transcr_output']/span[@class='transcribed_word']//text()")
	if ipa:
		print "found "+token, ipa[0]
		token = token.lower()
		computedSyllables = "|".join(S.Syllabize(token))
		line = "\t".join([token, ipa[0],"MISSING",computedSyllables,"MISSING"])+"\n"
		fd.write(line)
		print "INSERTED"

fd.close()