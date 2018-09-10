import requests
import os
path = "linksWithVideo.tsv"

fd = open(path, "r")
lines = fd.read().split("\n")

nLines = len(lines)

for idx, line in enumerate(lines):
	pieces = line.split("\t")
	idLink = pieces[0].split("/?ref_=adv_li_tt")[0].split("/")[-1]
	movieName = pieces[1]
	genre = pieces[3]
	trailer_name = idLink+"_"+movieName.replace(" ","").replace("/","") + "_"+genre+".mp4"
	if os.path.isfile("/media/joan/Maxtor/IMDB/trailers/"+trailer_name):
		print "Skipping " + trailer_name
		continue

	link = pieces[-1]
	page = requests.get(link)
	try:
		videoLink = page.content.split('"video/mp4","videoUrl":')[1].split("}")[0].replace('"',"")
	except IndexError as e:
		print e
		print "Skipping "+str(idx)
		continue

	videoRaw = requests.get(videoLink).content
	if len(videoRaw)/float(1000000) > 300:
		print "TOO BIG OMG"
		continue

	out = open("/media/joan/666CDBA407245B45/IMDB_2/trailers/"+trailer_name,"w")
	out.write(videoRaw)
	out.close()
	print "Downloaded "+str(idx+1)+ " of "+str(nLines)

fd.close()