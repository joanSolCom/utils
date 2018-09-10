# -*- coding: utf-8 -*-
import MySQLdb
from gensim.models.word2vec import Word2Vec
from gensim.models import KeyedVectors
from alphabet_detector import AlphabetDetector

ad = AlphabetDetector()

db = MySQLdb.connect(host="localhost",    # tu host, usualmente localhost
                     user="root",         # tu usuario
                     passwd="pany8491",  # tu password
                     db="Embeddings",
                     use_unicode=True)        # el nombre de la base de datos

cur = db.cursor()

word_vectors = KeyedVectors.load_word2vec_format('/home/joan/Escritorio/trainEmbed/genericw2v/wiki.en.vec')
#word_vectors = KeyedVectors.load_word2vec_format('/home/joan/Escritorio/trainEmbed/genericw2v/wiki.en.bin', binary=True)
zipped = zip(word_vectors.wv.index2word, word_vectors.wv.syn0)

for word, vector in zipped:
	strQuery = "INSERT IGNORE INTO `wiki_en` VALUES ("
	vector = vector.tolist()

	if u'ń' in word or ad.is_greek(word):
		continue

	strQuery+='"'+word+'"'+","

	for dim in vector:
		strQuery+=str(dim)+","

	strQuery = strQuery[:-1]
	strQuery+=")"
	try:
		cur.execute(strQuery)
		db.commit()
	except:
		print word
		continue
db.close()