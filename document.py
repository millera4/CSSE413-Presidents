import json, util, os, math

class Document():
	# Class representing document D
	def __init__(self, fileName):
		parsed_data = json.load(open('parsed/' + fileName))
		
		self.fileName = fileName
		self.words = util.Counter(parsed_data)	
		
	def freq(self, word):
		return self.words[word]
		
	def length(self):
		return self.words.totalCount()

def getDocuments():
	# Parse all files and create Document objects
	documents = []
	for fileName in os.listdir(os.getcwd() + '\parsed'):
		documents.append(Document(fileName))
		
	
	return documents
	
def IDF(documents, word):
	# Compute IDF of word in all documents	
	N = len(documents)
	n_q = num_containing(documents, word)
	return math.log( (N - n_q + 0.5) / (n_q + 0.5) )
				
def avgdl(documents):
	# Average length of all documents
	return sum(d.length() for d in documents) / len(documents)
		
def num_containing(documents, word):
	# Number of documents containing words
	count = 0
	for doc in documents:
		if doc.freq(word) != 0:
			count += 1
	return count