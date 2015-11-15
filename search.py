import document, util
import nltk.stem.porter
from nltk.util import skipgrams

stemmer = nltk.stem.porter.PorterStemmer()
documents = document.getDocuments()
#skipper= nltk.util.skipgrams()

def main():
	while True:
		query = raw_input("Please enter search query (\"quit\" to quit): ").lower()
		if query == 'quit':
			return
		
		# Remove bad search characters like punctuation
		query = filter(util.validSearchChar, query)
		results = score_documents(query)
		
		for i in range(10): # Print top 10 results
			print results[i] # Print Name, Confidence (sorted order)
			
		# for r in results: # Print all results
		# 	print r
			
		print "\n"
	
def score_documents(query):

	query = query.split()
	stemmedQuery = map(stemmer.stem, query)
	
	
	scores = []
	weights = [0,0,0,1]
	mb25 = bm25Score(stemmedQuery)
	scores.append(mb25)
	scores.append(titleScore(stemmedQuery))
	scores.append(headerScore(stemmedQuery))
	scores.append(skipScore(query))
	merged = []
	for i in range(0,len(mb25)):
		score = 0
		for j in range(0,len(scores)):
			score += weights[j]*scores[j][i][0]
		merged.append((score,mb25[i][1]))
	return sorted(merged, reverse=True)
	
def bm25Score(query):
	output = []
	k = 1
	b= 0.75
	for doc in documents:
		score = 0
		for searchTerm in query:
			IDF = document.IDF(documents, searchTerm)
			top = doc.freq(searchTerm)*(k+1)
			bot = doc.freq(searchTerm)+k*(1-b+b*doc.length()/document.avgdl(documents))
			score+= 1.0*IDF * top / bot
		output.append((score, doc.fileName))
	return output
	
def headerScore(query):
	output = []
	for doc in documents:
		score = 0
		headers = doc.headers
		for searchTerm in query:
			for heading in headers:
				for word in heading:
					if(word==searchTerm):
						score+=1 #document.IDF(documents, searchTerm)
		output.append((score,doc.fileName))
	return output
		
def titleScore(query):
	output = []
	for doc in documents:
		score = 0
		title = doc.title
		for searchTerm in query:
			for word in title:
				if(word==searchTerm):
					score+=10
		output.append((score,doc.fileName))
	return output

def skipScore(query):
	skips = skipgrams(query,2,len(query))
	skips = list(skips)
	output = []
	for doc in documents:
		score=0
		
		for gram in skips:
			for g in doc.skipgrams:
				if(g[0]==gram[0] and g[1]==gram[1]):
					score+=1
		output.append((score,doc.fileName))
	return output
	
if __name__ == "__main__":
	main()