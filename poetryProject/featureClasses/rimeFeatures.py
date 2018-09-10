# -*- coding: utf-8 -*-
from __future__ import division
from elasticSearch.elasticClient import ElasticClient
import os
import codecs
import sys
from pprint import pprint
import math
import re
import utils

class RimeFeatures:

	vocalSounds = ["ɪ","i",u'æ',"e",u'ɛ',"a",u'ə',u'ɑ',u'ɒ',u'ɔ',u'ʌ',"o",u'ʊ',"u","y",u'œ',u'ɐ',u'ɜ',u'ɞ',u'ɘ',u'ɵ']

	def __init__(self,iC, modelName):	
		self.client = ElasticClient()
		self.iC = iC
		self.type = "RimeFeatures"
		self.iC.initFeatureType(self.type)
		self.modelName = modelName
		self.dictTranscripts = self.loadDump()

	def loadDump(self):
		pathDump = "/home/joan/repository/cleanElasticDump.tsv"
		dictTranscripts = {}
		fd = codecs.open(pathDump,"r",encoding="utf-8")

		lines = fd.read().split("\n")
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
		return dictTranscripts

	def search(self, word):
		cleanInfo = self.dictTranscripts.get(word)
		return cleanInfo

	def get_rime_length(self, w1, w2):

		if w1 == w2:
			return None, None, None

		w1Info = self.search(w1.lower())
		w2Info = self.search(w2.lower())

		if not w1Info or not w2Info:
			return None, None, None

		rimeLength = 0

		for ipa1Elem, ipa2Elem in zip(reversed(w1Info["ipa"]), reversed(w2Info["ipa"])):
			if ipa1Elem == ipa2Elem:
				rimeLength+=1
			else:
				break

		if rimeLength > 1:
			return w1Info, w2Info, rimeLength
		else:
			return None, None, None

	def get_asonance_length(self, w1, w2):
		
		if w1 == w2:
			return None

		w1Info = self.search(w1.lower())
		w2Info = self.search(w2.lower())

		if not w1Info or not w2Info:
			return None

		ipa1Vowels = ""
		ipa2Vowels = ""

		for phoneme in w1Info["ipa"]:
			if unicode(phoneme) in self.vocalSounds:
				ipa1Vowels+=phoneme

		for phoneme in w2Info["ipa"]:
			if unicode(phoneme) in self.vocalSounds:
				ipa2Vowels+=phoneme

		rimeLength = 0

		for ipa1Elem, ipa2Elem in zip(reversed(ipa1Vowels), reversed(ipa2Vowels)):
			if ipa1Elem == ipa2Elem:
				rimeLength+=1
			else:
				break

		if rimeLength > 1:
			return rimeLength
		else:
			return None


	def get_rime_features(self):

		featureNames = [self.type+"_assonancePerVerse", self.type+"_assonancePerStanza", self.type+"_assonanceLengthPerVerse",self.type+"_assonanceLengthPerStanza", self.type+"_rimesPerStanza", self.type+"_rimesPerVerse", self.type+"_rimeLengthPerStanza",self.type+"_rimesLengthPerVerse"]
		functionName = "get_rime_features"

		idToken = 0
		totalRimesPerVerse = 0
		
		totalVerses = 0
		avgRimesPerVerse = 0
		totalRimesPerStanza = 0
		totalRimeLengthPerVerse = 0
		totalRimeLengthPerStanza = 0

		totalAssonancesPerVerse = 0
		totalAssonancesPerStanza = 0
		totalAssonanceLengthPerVerse = 0
		totalAssonanceLengthPerStanza = 0
		
		if os.path.isfile(self.iC.featurePath+self.modelName+"_"+functionName):
			utils.load_features_from_file(self.iC.featurePath+self.modelName+"_"+functionName, self.iC, self.type)
			print "loaded "+functionName
			return

		for instance in self.iC.instances:
			for stanza in instance.stanzas:
				stanzaWords = []
				for verse in stanza["verses"]:
					tokens = verse["tokens"]
					if tokens:
						totalVerses+=1
						analized = []
						for id1, token in enumerate(tokens):
							for id2, token2 in enumerate(tokens):
								if (id1,id2) not in analized and (id2,id1) not in analized:
									token = token.lower()
									token2 = token2.lower()
									t1info, t2info, rimeLength = self.get_rime_length(token,token2)
									asonanceLength = self.get_asonance_length(token,token2)
									
									analized.append((id1,id2))
									if rimeLength:
										totalRimesPerVerse+=1
										totalRimeLengthPerVerse+=rimeLength

									if asonanceLength:
										totalAssonancesPerVerse+=1
										totalAssonanceLengthPerVerse+=asonanceLength

							stanzaWords.append((idToken,token))
							idToken+=1


				analized = []
				for idx1, word1, in stanzaWords:
					for idx2, word2 in stanzaWords:
						distance = math.fabs(idx2 - idx1)
						if (idx1,idx2) not in analized and (idx2,idx1) not in analized and distance < 20:
							word1 = word1.lower()
							word2 = word2.lower()							
							t1info, t2info, rimeLength = self.get_rime_length(word1,word2)
							asonanceLength = self.get_asonance_length(word1,word2)
							analized.append((id1,id2))
							if rimeLength:
								totalRimesPerStanza+=1
								totalRimeLengthPerStanza+=rimeLength

							if asonanceLength:
								totalAssonancesPerStanza+=1
								totalAssonanceLengthPerStanza+=asonanceLength

			meanRimeLengthStanza=0
			if totalRimesPerStanza > 0:
				meanRimeLengthStanza = totalRimeLengthPerStanza / totalRimesPerStanza
			
			meanRimeLengthVerse=0
			if totalRimesPerVerse > 0:
				meanRimeLengthVerse = totalRimeLengthPerVerse / totalRimesPerVerse
			

			meanAssonanceLengthPerVerse = 0
			
			if totalAssonancesPerVerse > 0:
				meanAssonanceLengthPerVerse = totalAssonanceLengthPerVerse / totalAssonancesPerVerse

			meanAssonanceLengthPerStanza=0
	
			if totalAssonancesPerStanza > 0:
				meanAssonanceLengthPerStanza = totalAssonanceLengthPerStanza / totalAssonancesPerStanza

			meanAssonancePerVerse = totalAssonancesPerVerse / totalVerses
			meanAssonancePerStanza = (totalAssonancesPerStanza / len(instance.stanzas)) / totalVerses

			meanRimesPerVerse = totalRimesPerVerse / totalVerses
			meanRimesPerStanza = (totalRimesPerStanza / len(instance.stanzas)) / totalVerses

			instance.addFeature(self.type, self.type+"_rimeLengthPerStanza", meanRimeLengthStanza)
			instance.addFeature(self.type, self.type+"_rimesLengthPerVerse", meanRimeLengthVerse)

			instance.addFeature(self.type, self.type+"_rimesPerStanza", meanRimesPerStanza)
			instance.addFeature(self.type, self.type+"_rimesPerVerse", meanRimesPerVerse)

			instance.addFeature(self.type, self.type+"_assonanceLengthPerStanza", meanAssonanceLengthPerStanza)
			instance.addFeature(self.type, self.type+"_assonanceLengthPerVerse", meanAssonanceLengthPerVerse)

			instance.addFeature(self.type, self.type+"_assonancePerStanza", meanAssonancePerStanza)
			instance.addFeature(self.type, self.type+"_assonancePerVerse", meanAssonancePerVerse)

		utils.save_features_to_file(self.iC.featurePath+self.modelName+"_"+functionName,featureNames,self.iC, self.type)


	def get_meter_features(self):
		featureNames = [self.type+"_alliterationsPerVerse" , self.type+"_iambsPerVerse", self.type+"_pyrricPerVerse", self.type+"_spondeePerVerse",self.type+"_trocheePerVerse", self.type+"_anapestPerVerse", self.type+"_dactylPerVerse"]
		functionName = "get_meter_features"

		if os.path.isfile(self.iC.featurePath+self.modelName+"_"+functionName):
			utils.load_features_from_file(self.iC.featurePath+self.modelName+"_"+functionName, self.iC, self.type)
			print "loaded "+functionName
			return

		'''
			iamb - an unstressed syllable followed by a stressed syllable. x/
			pyrrhic - two unstressed syllables. xx
			spondee - two stressed syllables. //
			trochee - a stressed syllable followed by an unstressed syllable. /x
			anapest - two unstressed syllables followed by a stressed syllable. xx/
			dactyl -  one stressed syllable followed by two unstressed syllables. /xx
		'''
		iambRegex = "x/"
		pyrrhicRegex = r'xx'
		spondeeRegex = r'//'
		trocheeRegex = r'/x'
		anapestRegex = r'xx/'
		dactylRegex = r'/xx'

		for instance in self.iC.instances:
			totalVerses = 0
			totalIamb = 0
			totalPyrrhic = 0
			totalSpondee = 0
			totalTrochee = 0
			totalAnapest = 0
			totalDactyl = 0
			totalAlliterations = 0

			for stanza in instance.stanzas:
				for verse in stanza["verses"]:
					totalVerses+=1
					stressPattern = verse["stress"]

					totalIamb += len(re.findall(iambRegex,stressPattern))
					totalPyrrhic += len(re.findall(pyrrhicRegex,stressPattern))
					totalSpondee += len(re.findall(spondeeRegex,stressPattern))
					totalTrochee += len(re.findall(trocheeRegex,stressPattern))
					totalAnapest += len(re.findall(anapestRegex,stressPattern))
					totalDactyl += len(re.findall(dactylRegex,stressPattern))

					'''
						ALLITERATION
						stylistic device in which a number of words, 
						having the same first consonant sound, 
						occur close together in a series
					'''

					initialSounds = {}
					for idx, token in enumerate(verse["tokens"]):
						infoWord = self.search(token.lower())
						if infoWord:
							initialSound = infoWord["ipa"][0]
							if initialSound not in initialSounds.keys():
								initialSounds[initialSound] = []
	
							if initialSound not in self.vocalSounds:
								initialSounds[initialSound].append(idx)

					for phoneme, indexWords in initialSounds.iteritems():
						stored = []
						for index1 in indexWords:
							for index2 in indexWords:
								if index1 != index2 and (index1,index2) not in stored and (index2,index1) not in stored:
									dist = math.fabs(index1-index2)
									if dist < 6:
										totalAlliterations+=1
									stored.append((index1,index2))

			instance.addFeature(self.type, self.type+"_alliterationsPerVerse", totalAlliterations/totalVerses)
			instance.addFeature(self.type, self.type+"_iambsPerVerse", totalIamb/totalVerses)
			instance.addFeature(self.type, self.type+"_pyrricPerVerse", totalPyrrhic/totalVerses)
			instance.addFeature(self.type, self.type+"_spondeePerVerse", totalSpondee/totalVerses)
			instance.addFeature(self.type, self.type+"_trocheePerVerse", totalTrochee/totalVerses)
			instance.addFeature(self.type, self.type+"_anapestPerVerse", totalAnapest/totalVerses)
			instance.addFeature(self.type, self.type+"_dactylPerVerse", totalDactyl/totalVerses)

		utils.save_features_to_file(self.iC.featurePath+self.modelName+"_"+functionName,featureNames,self.iC, self.type)
