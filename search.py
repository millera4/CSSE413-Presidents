import document



def main():
	while True:
		query = raw_input("Please enter search query (\"quit\" to quit): ").lower()
		if query == 'quit':
			return
		
		results = score_documents(query)
		
		for i in range(10): # Print top 10 results
			print results[i] # Print Name, Confidence (sorted order)
			
		# for r in results: # Print all results
		# 	print r
			
		print "\n"
	
def score_documents(query):
	mb25 = bm25Score(query)
	title = titleScore(query)
	header = headerScore(query)
	merged = []
	for i in range(0,len(mb25)):
		merged.append((mb25[i][0]+title[i][0]+header[i][0],mb25[i][1]))
	return sorted(merged, reverse=True)
	
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
	
def headerScore(query):
	output = []
	documents = document.getDocuments()
	for doc in documents:
		score = 0
		headers = doc.headers
		for searchTerm in query.split():
			for heading in headers:
				for word in heading:
					if(word==searchTerm):
						score+=document.IDF(documents, searchTerm)
		output.append((score,doc.fileName))
	return output
		
def titleScore(query):
	output = []
	documents = document.getDocuments()
	for doc in documents:
		score = 0
		title = doc.title
		for searchTerm in query.split():
			for word in title:
				if(word==searchTerm):
					score+=10
		output.append((score,doc.fileName))
	return output

if __name__ == "__main__":
	main()