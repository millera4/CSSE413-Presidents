import json, util, os, math

class Document():
	# Class representing document D
	def __init__(self, fileName):
		parsed_data = json.load(open('parsed/' + fileName))
		
		self.fileName = fileName
		self.words = util.Counter(parsed_data['words'])	
		self.headers = parsed_data['headers']
		self.title = parsed_data['title']
		self.skipgrams = parsed_data['skipgrams']
		
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
	EPSILON = math.e # Constant to force IDF to be positive
	# Constant needed because our sample size is small
	# Any word that occurs in more than half the documents has a 
	# negative IDF (such as "Bush").  By default, this gives a negative 
	# score to a document that DOES include the search query
	
	N = len(documents)
	n_q = num_containing(documents, word)

	return math.log( EPSILON + (N - n_q + 0.5) / (n_q + 0.5) )
				
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