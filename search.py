def main():
	query = ""
	while query != "quit":
		query = raw_input("Please enter search query (\"quit\" to quit): ")
		
		results = score_documents(query)
		
		for r in results:
			print r # Print Name, Confidence (sorted order)
			
		print "\n"
	
def score_documents(query):
	return []


if __name__ == "__main__":
	main()