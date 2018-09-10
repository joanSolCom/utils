import os
import sys
import nltk
from nltk import word_tokenize

fn = sys.argv[1]
LANG = sys.argv[2]


def text2Conll(sentences):
	conll = ""
	noelem = "_"
	separator = "\t"
	for sentence in sentences:
		tokens = word_tokenize(sentence)
		idx = 1
		line = ""
		for token in tokens:
					#1					2				3				  4				  5					6				7				  8				  9					10
			line += str(idx)+separator+token+separator+noelem+separator+noelem+separator+noelem+separator+noelem+separator+noelem+separator+noelem+separator+noelem+separator+noelem+"\n"
			idx+=1
		conll+= line+"\n"

	print conll
	return conll

if os.path.exists(fn):
	print os.path.basename(fn)
	if LANG == "EN":
		print LANG
		tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
		txt = open(fn,"r").read()
		sentences = tokenizer.tokenize(txt)
		conll = text2Conll(sentences)
	else:
		print "NOT SUPPORTED YET"