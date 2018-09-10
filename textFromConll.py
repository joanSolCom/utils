import sys
import os

fpath = sys.argv[1]

conll = open(fpath,"r").read()

sentences = conll.split("\n\n")
text = ""
for sentence in sentences:
	tokens = sentence.split("\n")
	for token in tokens:
		word = token.split("\t")[1]
		text+=word + " "
	text+="\n"

print text