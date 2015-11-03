import document.py



def main():
	query = ""
	while query != "quit":
		query = raw_input("Please enter search query (\"quit\" to quit): ")
		
		results = score_documents(query)
		
		for r in results:
			print r # Print Name, Confidence (sorted order)
			
		print "\n"
	
def score_documents(query):
	return bm25Score(query)

def bm25Score(query):
	output = []
	k = 1
	b= 0.75
	documents = document.getDocuments()
	for doc in documents:
		score = 0
		for searchTerm in query:
			IDF = Document.IDF(searchTerm)
			top = doc.freq(searchTerm)*(k+1)
			bot = doc.freq(searchTerm)+k*(1-b+b*doc.length()/document.avgdl())
			score+= IDF * top / bot
		output.append((doc.filename,score))
	return output
		

if __name__ == "__main__":
	main()