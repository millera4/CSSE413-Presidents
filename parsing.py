from HTMLParser import HTMLParser
import os, string, util, json, nltk
from nltk.util import skipgrams


class MyHTMLParser(HTMLParser):
    def __init__(self, data=''):
        HTMLParser.__init__(self)
        self.isPrinting = False
        
        self.startOfContent = False
        self.endOfContent = False
        
        self.isHeader = False
        self.isTitle = False
        self.rawData = data
        
        self.words = util.Counter()
        self.headers = []
        self.title = []
        
        self.skipgrams = []
        self.currentData = ''
        
        self.stemmer = nltk.stem.porter.PorterStemmer()
        
        self.feed(data)
        
    def handle_starttag(self, tag, attrs):
        if ('id', 'mw-content-text') in attrs:
            # print "PARSING CONTENT"
            self.startOfContent = True
            
        if ('id', 'External_links') in attrs:
            # print "END OF CONTENT"
            self.endOfContent = True
            self.isPrinting = False
            
        if tag == 'h2' or tag == 'h3' or tag == 'h4':
            # Section headers
            if self.startOfContent and not self.endOfContent:
                self.isPrinting = True
            self.isHeader = True
            self.currentData = ''
            
        if tag == 'h1':
            # Title of document
            self.isPrinting = True
            self.isTitle = True
            self.currentData = ''
            
        if tag == 'p':
            # Paragraph
            if self.startOfContent and not self.endOfContent:
                self.isPrinting = True
            self.currentData = ''
              
    def handle_endtag(self, tag):       
        if tag == 'h2' or tag == 'h3' or tag == 'h4':
            self.isHeader = False
            self.parseHeader()
        
        if tag == 'h1':
            self.isPrinting = False
            self.isTitle = False
            self.parseTitle()
            
        if tag == 'p':
            self.isPrinting = False
            self.parseParagraph()
            
    def parseHeader(self):
        data = nltk.word_tokenize(self.currentData)
        self.headers.append(data)
    
    def parseTitle(self):
        data = nltk.word_tokenize(self.currentData)
        self.title = data
            
    def parseParagraph(self):
        data = nltk.word_tokenize(self.currentData)
        words = [w for w in data if w.isalnum()]
        skip_bigrams = list(skipgrams(words, 2, len(words)))
        self.skipgrams = self.skipgrams + skip_bigrams
        
 
    def handle_data(self, data):
        data = data.rstrip()  #.lower() - not ignore case anymore
        if data == '[':
            # Don't print the references [1]
            self.isPrinting = False
        elif data == ']':
            if not self.endOfContent:
                self.isPrinting = True         
        elif self.isPrinting and data != '':            
            # validCharFn basically removes "double quote" characters, punctuation marks '.,:;', and dashes
            # (but keeps contractions -> don't I'm aren't)
            # data = filter(util.validSearchChar, data)
            self.currentData += data + " "
            
            data = nltk.word_tokenize(data)
            
            for w in data:
                stemmed_word = self.stemmer.stem(w)
                self.words[stemmed_word] += 1
                

# Test code
def main():
    print os.getcwd()
    for fileName in os.listdir(os.getcwd() + '\unparsed'):
        #if fileName != 'Obama.txt': continue  # Testing
        print fileName
        try:      
            # Parsing 
            data = open('unparsed/' + fileName).read()
            data = filter(lambda x: x in string.printable, data)
            parser = MyHTMLParser(data)
                        
            # Saving parsed data
            f = open('parsed/' + fileName, 'w')
            #f = open('parsed.txt', 'w')
            parsed_data = { 'skipgrams': parser.skipgrams, 'words': parser.words, 'headers': parser.headers , 'title': parser.title }
            json.dump(parsed_data, f)
            
        except Exception as e:
            print "Could not parse file:", e
            print type(e)
            
if __name__ == "__main__":
    main()
