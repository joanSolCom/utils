import os

pathBase = "/home/joan/repository/poetryProject/outputs/"

labelSet = set()
dictAllign = {}
first = True
dictAllign["labels"] = []
j = 0

for arffPath in os.listdir(pathBase):
	raw = open(pathBase+arffPath,"r").read()
	pieces = raw.split("\n\n")
	header = pieces[0].split("\n")
	labels = header[-1].replace("}","").split("{")[1].split(",")
	for label in labels:
		labelSet.add(label)

	attributeList = header[1:-1]

	for attr in attributeList:
		if attr not in dictAllign:
			dictAllign[attr] = []


attrList = dictAllign.keys()

for arffPath in os.listdir(pathBase):
	raw = open(pathBase+arffPath,"r").read()
	pieces = raw.split("\n\n")
	header = pieces[0].split("\n")
	attributeList = header[1:-1]
	data = pieces[1].replace("@data\n","").split("\n")
	
	for instance in data:
		dictInst = {}
		features = instance.split(",")[:-1]
		if features:
			label = instance.split(",")[-1]
			dictAllign["labels"].append(label)
			for idx, attr in enumerate(attributeList):
				dictInst[attr] = features[idx]

			for attr in attrList:
				if attr in dictInst:
					dictAllign[attr].append(dictInst[attr])
				else:
					if attr != "labels":
						dictAllign[attr].append(0.0)


stringArff = "@relation MERGED\n"

for attr in attrList:
	if attr != "labels":
		stringArff+=attr+"\n"

stringArff+="@attribute label {"+",".join(labelSet)+"}\n\n"+"@data\n"

i=0
nInsts = len(dictAllign["labels"])
while i < nInsts:
	instance = []
	for attr in attrList:
		if attr!="labels":
			instance.append(dictAllign[attr][i])

	instance.append(dictAllign["labels"][i])
	stringArff+=",".join(instance)+"\n"

	i+=1

print stringArff