import document



def main():
	while True:
		query = raw_input("Please enter search query (\"quit\" to quit): ").lower()
		if query == 'quit':
			return
		
		results = score_documents(query)
		
		for r in results:
			print r # Print Name, Confidence (sorted order)
			
		print "\n"
	
def score_documents(query):
	mb25 = bm25Score(query)
	title = titleScore(query)
	merged = []
	for i in range(0,len(mb25)):
		merged.append((mb25[i][0]+title[i][0],mb25[i][1]))
	return sorted(merged)
	
def bm25Score(query):
	output = []
	k = 1
	b= 0.75
	documents = document.getDocuments()
	for doc in documents:
		score = 0
		for searchTerm in query.split():
			IDF = document.IDF(documents, searchTerm)
			top = doc.freq(searchTerm)*(k+1)
			bot = doc.freq(searchTerm)+k*(1-b+b*doc.length()/document.avgdl(documents))
			score+= 1.0*IDF * top / bot
		output.append((score, doc.fileName))
	return output
	
def titleScore(query):
	output = []
	documents = document.getDocuments()
	for doc in documents:
		score = 0
		headers = doc.headers
		for searchTerm in query.split():
			for heading in doc.headers:
				for word in heading:
					if(word==searchTerm):
						score+=document.IDF(documents, searchTerm)
		output.append((score,doc.fileName))
	return output

if __name__ == "__main__":
	main()