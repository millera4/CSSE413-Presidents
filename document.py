import json, util, os, math

# Global variables
documents = [] 	# array holding document objects
N = 44 			# number of documents (number of presidents)
avgdl = -1 		# average document length (initialized on getDocuments)

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
	if documents:
		return documents # if computed, don't parse again
	
	for fileName in os.listdir(os.getcwd() + '\parsed'):
		documents.append(Document(fileName))
		
	avgdl = sum(d.length() for d in documents) / N
	
	return documents
	
def IDF(word):
	# Compute IDF of word in all documents
	if not documents:
		documents = getDocuments()
		
	n_q = num_containing(word)
	return math.log( (N - n_q + 0.5) / (n_q + 0.5) )
				
def avgdl():
	# Average length of all documents
	if not documents:
		documents = getDocuments()
		
	return avgdl
		
def num_containing(word):
	# Number of documents containing words
	count = 0
	for doc in documents:
		if doc.freq(word) != 0:
			count += 1
	return count