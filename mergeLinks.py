

path = "./data/data.tsv"

lines = open(path,"r").read().split("\n")[1:]

acumLinks = set()

fdOut = open("acumLinks.tsv","w")

for line in lines:
	columns = line.split("\t")
	if len(columns) > 2:
		idx = columns[0]
		titleType = columns[1]

		if titleType == "movie":
			primaryTitle = columns[2]
			if columns[4] == "0":
				year = columns[5]
				runtime = columns[7]
				genres = columns[8]
				link = "https://www.imdb.com/title/"+idx+"/?ref_=adv_li_tt"
				lineOut = link+"\t"+primaryTitle+"\t"+year+"\t"+genres.lower()+"\t"+runtime+"\n"
				fdOut.write(lineOut)

import os

for fname in os.listdir("."):
	if fname != "data" and fname != "mergeLinks.py" and fname!="acumLinks.tsv":
		fd = open(fname,"r")
		lines = fd.read().split("\n")
		for line in lines:
			lineOut = line+"\t"+"_"+"\t"+"_"+"\t"+fname+"\t"+"_"+"\n"
			fdOut.write(lineOut)
		fd.close()


fdOut.close()