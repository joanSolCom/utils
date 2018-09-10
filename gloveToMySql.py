# -*- coding: utf-8 -*-
import MySQLdb
import numpy as np

db = MySQLdb.connect(host="localhost",    # tu host, usualmente localhost
                     user="root",         # tu usuario
                     passwd="pany8491",  # tu password
                     db="Embeddings",
                     use_unicode=True)        # el nombre de la base de datos

cur = db.cursor()

print "Loading Glove Model"

gloveFile = "PATH"

f = open(gloveFile,'r')

    for line in f:
        splitLine = line.split()
        word = splitLine[0]
        vector = np.array([float(val) for val in splitLine[1:]])

        strQuery = "INSERT IGNORE INTO `glove` VALUES ("
        vector = vector.tolist()

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
