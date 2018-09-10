import spacy

nlp = spacy.en.English()  
doc = nlp(u'Hello, world. Here are two sentences.')
#sentences. es un iterator. agafar elements amb sents.next()
sents = doc.sents

#tag des segon token
pos = doc[2].tag_

#dependencia des quart token
dependency = doc[4].dep_
head = doc[4].head

def dependency_labels_to_root(token):
    '''Walk up the syntactic tree, collecting the arc labels.'''
    dep_labels = []
    while token.head is not token:
        dep_labels.append(token.dep)
        token = token.head
    return dep_labelsdef dependency_labels_to_root(token):
    '''Walk up the syntactic tree, collecting the arc labels.'''
    dep_labels = []
    while token.head is not token:
        dep_labels.append(token.dep)
        token = token.head
    return dep_labels