#!/usr/bin/python

import sys
from elasticSearch.elasticClient import ElasticClient
import json

def preprocess(field, content):
	if field == "ipa":
		content = content.split(",")[0]
		content = content.replace("/","")
		content = content.split(";")[0]
		content = content.replace("stressed ","")
		content = content.replace("noun ","")
		content = content.replace("verb ","")

	elif field == "spell":
		content = content.replace("[","")
		content = content.replace("]","")
		content = content.split(";")[0]
		content = content.split(",")[0]
		content = content.replace("stressed ","")
		content = content.replace("noun ","")
		content = content.replace("verb ","")

	elif field == "syllables":
		content = content.replace("noun ","")
		content = content.replace("verb ","")

	return content

def annotateRimes(self, text):
		paragraphs = text.split("\n\n")
		idToken = 0
		idSentence = 0
		rawWords = []
		totalRimes = 0
		for idParagraph, paragraph in enumerate(paragraphs):
			words=[]
			sents = paragraph.split("\n")
			for sent in sents:
				wordList = sent.split()
				for token in wordList:
					token = token.encode("utf-8").lower().replace(".","").replace(",","").replace("'","").replace("—","").replace("[","").replace("]","").replace("!","").replace('"',"").replace(";","").replace("?","").replace("(","").replace(")","").replace(":","")
					words.append((token, idToken,idSentence,idParagraph))
					rawWords.append(token)
					idToken+=1
				idSentence+=1

			rimes = []
			cache = []
			for wordTupl1 in words:
				for wordTupl2 in words:
					if wordTupl1[0]!=wordTupl2[0] and wordTupl1[1]!=wordTupl2[1] and (wordTupl2[1],wordTupl1[1]) not in cache:
						rimeInfo = self.testRime(wordTupl1,wordTupl2)
						cache.append((wordTupl1[1],wordTupl2[1]))
						if rimeInfo:
							if abs(rimeInfo[0]["idSentence"] - rimeInfo[1]["idSentence"]) < 4:
								rimes.append(rimeInfo)
			pprint(rimes)
			totalRimes+=len(rimes)
		
		print totalRimes
		print rawWords

if len(sys.argv) < 3:
	print "WRONG number of args"
else:
	w1 = sys.argv[1]
	w2 = sys.argv[2]
	e = ElasticClient()
	w1obj = e.search_word_info(w1)
	w2obj = e.search_word_info(w2)
	
	if w1obj["hits"]["hits"] and w2obj["hits"]["hits"]:
		w1info = w1obj["hits"]["hits"][0]["_source"]
		w2info = w2obj["hits"]["hits"][0]["_source"]

		w1ipa = preprocess("ipa",w1info["ipa"])
		w2ipa = preprocess("ipa",w2info["ipa"])		
		w1spell = preprocess("spell",w1info["spell"])
		w2spell = preprocess("spell",w2info["spell"])

		w1syllables = preprocess("syllables",w1info["syllables"])
		w2syllables = preprocess("syllables",w2info["syllables"])


		print w1ipa,w2ipa
		print w1syllables,w2syllables
		print w1spell, w2spell
	else:
		if not w1obj["hits"]["hits"]:
			print w1+ " not found"

		if not w2obj["hits"]["hits"]:
			print w2+ " not found"
