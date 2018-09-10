import re

pathTest = "/home/joan/Escritorio/Datasets/langDataset/synUniversal/1034_female_de"
txt = open(pathTest,"r").read()

posBlocks = re.findall("\(ROOT\n(.*?)\)\n\n",txt,re.DOTALL)

for posBlock in posBlocks:
	pos = []
	lines = posBlock.split("\n")
	for line in lines:
		pieces = line.strip().split()
		for i in range(len(pieces)):
			if not pieces[i].startswith("("):
				p = pieces[i-1].replace("(", "")
				tok = pieces[i].replace(")", "") + "-" + str(len(pos)+1)
				pos += [(p, tok)]
	print pos

exit()

dependenciesBlocks = re.findall("\)\n\n(.*?)\n\n",txt,re.DOTALL)
for dependencyBlock in dependenciesBlocks:
	dependencies = dependencyBlock.split("\n")
	for dependency in dependencies:
		dependencyName = dependency.split("(")[0]
		destiny = dependency.split("(")[1].split(",")[0]
		origin = dependency.split("(")[1].split(",")[1].strip()[:-1]
		print dependencyName,destiny,origin


