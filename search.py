import document



def main():
	while True:
		query = raw_input("Please enter search query (\"quit\" to quit): ")
		if query == 'quit':
			return
		
		results = score_documents(query)
		
		for r in results:
			print r # Print Name, Confidence (sorted order)
			
		print "\n"
	
def score_documents(query):
	mb25 = bm25Score(query)
	return sorted(mb25)
	# return mb25

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
			score+= IDF * top / bot
		output.append((score, doc.fileName))
	return output
		

if __name__ == "__main__":
	main()