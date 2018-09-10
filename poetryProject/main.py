# -*- coding: utf-8 -*-
import instanceManager
from instanceManager import InstanceCollection
from featureClasses.characterBasedFeatures import CharacterBasedFeatures
from featureClasses.wordBasedFeatures import WordBasedFeatures
from featureClasses.sentenceBasedFeatures import SentenceBasedFeatures
from featureClasses.dictionaryBasedFeatures import DictionaryBasedFeatures
from featureClasses.syntacticFeatures import SyntacticFeatures
from featureClasses.discourseFeatures import DiscourseFeatures
from featureClasses.lexicalFeatures import LexicalFeatures
from featureClasses.rimeFeatures import RimeFeatures
from featureClasses.syllableFeatures import SyllableFeatures
from pprint import pprint

def compute_features(paths, featureGroups, modelName, labelPosition, selectedLabels = None):
	print "Creating Instance Collection"
	iC = instanceManager.createInstanceCollection(paths, labelPosition, "_" ,selectedLabels)
	
	if "RimeFeatures" in featureGroups:
		print "rime features"
		iR = RimeFeatures(iC, modelName)
		iR.get_meter_features()
		iR.get_rime_features()

	if "SyllableFeatures" in featureGroups:
		print "syllable features"
		iSyl = SyllableFeatures(iC, modelName)
		iSyl.get_syllable_stats()
		iSyl.get_stress_stats()

	if "CharacterBasedFeatures" in featureGroups:
		print "charbased"
		iChar = CharacterBasedFeatures(iC,modelName)
		iChar.get_uppers()
		iChar.get_numbers()
		iChar.get_symbols([","],"commas")
		iChar.get_symbols(["."],"dots")
		iChar.get_symbols(['?',"¿"],"questions")
		iChar.get_symbols(['!','¡'],"exclamations")
		iChar.get_symbols([":"],"colons")
		iChar.get_symbols([";"],"semicolons")
		iChar.get_symbols(['"',"'","”","“", "’"],"quotations")
		iChar.get_symbols(["—","-","_"],"hyphens")
		iChar.get_symbols(["(",")"],"parenthesis")
		iChar.get_in_parenthesis_stats()

	if "WordBasedFeatures" in featureGroups:
		print "wordbased"
		iWord = WordBasedFeatures(iC,modelName)
		iWord.get_twothree_words()
		iWord.get_word_stdandrange()
		iWord.get_chars_per_word()
		iWord.get_vocabulary_richness()
		iWord.get_stopwords()
		iWord.get_acronyms()
		iWord.get_firstperson_pronouns()
		iWord.get_proper_nouns()

	if "SentenceBasedFeatures" in featureGroups:
		print "sentbased"
		iSent = SentenceBasedFeatures(iC,modelName)
		iSent.get_wordsPerSentence_stdandrange()

	if "DictionaryBasedFeatures" in featureGroups:
		print "dictbased"
		iDict = DictionaryBasedFeatures(iC,modelName)
		iDict.get_discourse_markers()
		iDict.get_dict_count()
		iDict.get_interjections()
		iDict.get_mean_mood()
	
	if "SyntacticFeatures" in featureGroups:
		print "syntactic"
		iSyntactic = SyntacticFeatures(iC,modelName)
		iSyntactic.compute_syntactic_features()

	return iC

modelName = "poetry"
paths = {}
paths["clean"] = "/home/joan/Escritorio/Datasets/poetry/clean/"
#paths["synParsed"] = "/home/joan/Escritorio/Datasets/poetry/synParsed/"

featureGroups = ["CharacterBasedFeatures", "WordBasedFeatures", "SentenceBasedFeatures", "SyntacticFeatures","DictionaryBasedFeatures", "SyllableFeatures","RimeFeatures"]
suffix = "_".join(featureGroups)
pathArff = "/home/joan/repository/poetryProject/outputs/"

labelPosition = 2
labeling = "poet"
print modelName
print featureGroups
print labeling

iC = compute_features(paths, featureGroups, modelName, labelPosition)

print "to Arff"
iC.toArff(pathArff, modelName+"_"+labeling+suffix+".arff")
