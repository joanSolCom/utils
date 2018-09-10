from __future__ import division
import os
from collections import Counter
import nltk
import codecs

dirCorpus = "/home/joan/Escritorio/Datasets/hateSpeech/meuCorpusHate/clean/"
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
extraStopPath = "/home/joan/repository/PhD/BESTVersion/dicts/extraStop.txt"

extraStop = open(extraStopPath,"r").read().split("\n")
stopwords = nltk.corpus.stopwords.words('english')

for word in extraStop:
	stopwords.append(unicode(word))

def mostCommonPerLabel(labels,N):

	dictStats = {}
	for label in labels:
		dictStats[label] = []

	for fname in os.listdir(dirCorpus):
		label = fname.split("_")[2]
		tokens = codecs.open(dirCorpus+fname,"r", encoding="utf-8").read().replace(".","").replace(",","").replace('"',"").replace("'","").lower().split()
		for idx,token in enumerate(tokens):
			if token in stopwords:
				del tokens[idx]

		dictStats[label].extend(tokens)

	dictCounters = {}

	for label in labels:
		print "MOST COMMON WORDS FOR LABEL " + label
		dictCounters[label] = Counter(dictStats[label])
		most_common = dictCounters[label].most_common(N)
		print most_common

def mostCommon(N):
	all_tokens = []

	for fname in os.listdir(dirCorpus):
		label = fname.split("_")[2]
		tokens = codecs.open(dirCorpus+fname,"r",encoding="utf-8").read().replace(".","").replace(",","").replace('"',"").replace("'","").lower().split()
		all_tokens.extend(tokens)

	counter = Counter(all_tokens)
	most_common = counter.most_common(N)
	for idx, word in enumerate(most_common):
		if word[0] in stopwords:
			del most_common[idx]
	print most_common

def characteristics():
	print "\n------------GENERAL STATS------------"
	tokLengthGeneral = 0
	charLengthGeneral = 0
	nTexts = len(os.listdir(dirCorpus))
	maxChars = 0
	minChars = 9999999999
	meanTokens = 0
	acumSents = 0
	minTokens = 99999
	maxTokens = 0

	for fname in os.listdir(dirCorpus):
		meanTokLength = 0
		raw = codecs.open(dirCorpus+fname,"r",encoding="utf-8").read()
		
		sents = tokenizer.tokenize(raw)
		nSents = len(sents)
		acumSents += nSents / nTexts

		nChars = len(raw)

		if maxChars < nChars:
			maxChars = nChars

		if minChars > nChars:
			minChars = nChars

		charLengthGeneral += nChars / nTexts
		tokens = raw.split()
		nTokens = len(tokens)
		if nTokens > maxTokens:
			maxTokens = nTokens
		if nTokens < minTokens:
			minTokens = nTokens

		meanTokens += nTokens / nTexts
		for token in tokens:
			meanTokLength += len(token) / nTokens

		tokLengthGeneral += meanTokLength / nTexts
	
	print "Mean Number of Tokens " + str(meanTokens)
	print "Min Number of Tokens " + str(minTokens)
	print "Max Number of Tokens " + str(maxTokens)
	print "Mean Token Length " + str(tokLengthGeneral)
	print "Mean Char Length " + str(charLengthGeneral)
	print "Min Char Length " + str(minChars)
	print "Max Char Length " + str(maxChars)
	print "Mean Sents Per Text " + str(acumSents)

def characteristicsPerClass(labels):
	print "\n------------STATS PER CLASS-------------"
	dictStats = {}
	for label in labels:
		dictStats[label] = {}
		dictStats[label]["tokLength"] = 0
		dictStats[label]["charLength"] = 0
		dictStats[label]["minChar"] = 99999
		dictStats[label]["maxChar"] = 0
		dictStats[label]["ninstances"] = 0
		dictStats[label]["nSents"] = 0
		dictStats[label]["nTokens"] = 0
		dictStats[label]["maxTokens"] = 0
		dictStats[label]["minTokens"] = 99999

	tokLengthGeneral = 0
	charLengthGeneral = 0
	nTexts = len(os.listdir(dirCorpus))
	srcStats = {}
	for fname in os.listdir(dirCorpus):
		
		label = fname.split("_")[2]

		src = fname.split("_")[1]
		key = src+"_"+label
		if key not in srcStats:
			srcStats[key] = 0
		srcStats[key]+=1

		dictStats[label]["ninstances"] += 1

		raw = codecs.open(dirCorpus+fname,"r",encoding="utf-8").read()
		nChars = len(raw)
		dictStats[label]["charLength"] += nChars

		sents = tokenizer.tokenize(raw)
		nSents = len(sents)
		dictStats[label]["nSents"] += nSents

		if dictStats[label]["maxChar"] < nChars:
			dictStats[label]["maxChar"] = nChars

		if dictStats[label]["minChar"] > nChars:
			dictStats[label]["minChar"] = nChars

		tokens = raw.split()
		nTokens = len(tokens)

		if dictStats[label]["maxTokens"] < nTokens:
			dictStats[label]["maxTokens"] = nTokens

		if dictStats[label]["minTokens"] > nTokens:
			dictStats[label]["minTokens"] = nTokens

		dictStats[label]["nTokens"] += nTokens

		for token in tokens:
			dictStats[label]["tokLength"] +=len(token) / nTokens

	print "SRC STATS "
	print srcStats

	for label, innerDict in dictStats.iteritems():
		print "STATS FOR LABEL " + label
		dictStats[label]["charLength"] /= dictStats[label]["ninstances"]
		dictStats[label]["tokLength"] /= dictStats[label]["ninstances"]
		dictStats[label]["nSents"] /= dictStats[label]["ninstances"]
		dictStats[label]["nTokens"] /= dictStats[label]["ninstances"]

		print "Ninstances " + str(dictStats[label]["ninstances"]) 
		print "Mean Number of Tokens " + str(dictStats[label]["nTokens"])
		print "Min Number of Tokens " + str(dictStats[label]["minTokens"])
		print "Max Number of Tokens " + str(dictStats[label]["maxTokens"])
		print "Mean Token Length " + str(dictStats[label]["tokLength"])
		print "Mean Char Length " + str(dictStats[label]["charLength"])
		print "Min Char Length " + str(dictStats[label]["minChar"])
		print "Max Char Length " + str(dictStats[label]["maxChar"])
		print "Mean Sents Per Text " + str(dictStats[label]["nSents"])

labels = ["misogyny.txt","nazi.txt","antilgbt.txt","fatshaming.txt","racism.txt","NOHATE.txt"]

mostCommonPerLabel(labels,100)
mostCommon(100)
characteristics()
characteristicsPerClass(labels)