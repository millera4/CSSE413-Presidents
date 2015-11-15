from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import os, string, util
from htmlentitydefs import name2codepoint
import json, nltk


class MyHTMLParser(HTMLParser):
    def __init__(self, data=''):
        HTMLParser.__init__(self)
        self.isPrinting = False
        self.endOfContent = False
        self.isHeader = False
        self.isTitle = False
        self.rawData = data
        
        self.words = util.Counter()
        self.headers = []
        self.title = []
        
        self.feed(data)
        
    def handle_starttag(self, tag, attrs):
        if ('id', 'mw-content-text') in attrs:
            # print "PARSING CONTENT"
            self.isPrinting = True
            
        if ('id', 'External_links') in attrs:
            # print "END OF CONTENT"
            self.endOfContent = True
            self.isPrinting = False
            
        if tag == 'h2' or tag == 'h3' or tag == 'h4':
            # Section headers
            self.isHeader = True
            
        if tag == 'h1':
            # Title of document
            self.isPrinting = True
            self.isTitle = True
              
    def handle_endtag(self, tag):       
        if tag == 'h2' or tag == 'h3' or tag == 'h4':
            self.isHeader = False
        
        if tag == 'h1':
            self.isPrinting = False
            self.isTitle = False
 
    def handle_data(self, data):
        data = data.rstrip().lower()
        if data == '[':
            # Don't print the references [1]
            self.isPrinting = False
        elif data == ']':
            if not self.endOfContent:
                self.isPrinting = True         
        elif self.isPrinting and data != '':            
            # validCharFn basically removes "double quote" characters, punctuation marks '.,:;', and dashes
            # (but keeps contractions -> don't I'm aren't)
            data = filter(util.validSearchChar, data)
            data = data.split()
            
            for w in data:
                self.words[w] += 1
                
            if self.isHeader:
                self.headers.append(data)
                
            if self.isTitle:
                self.title = data
                
class NLPParser():
    def __init__(self, data=''):
        self.sentences = []
        self.sent_pos = []
        
        self.feed(data)
        
    def feed(self, data):
        self.sentences = nltk.word_tokenize(data)
        #self.send_pos = 
        #line_num = 0
        #for line in data.split():
        #    print line
        #    line = line.rstrip()
        #    
        #    if line == '':
        #        #print "empty line found"
        ##        continue    # Ignore empty line
        #        
        #    tokens = nltk.word_tokenize(line)
        #    #tagged = nltk.pos_tag(tokens)
        #    
        #    self.sentences.append(tokens)
        #    #self.sent_pos.append(tagged)
        #    
        #    if line_num % 500 == 0:
        #        print "line: ", line_num
        #    line_num += 1
        
        
            

# Test code
def main():
    print os.getcwd()
    for fileName in os.listdir(os.getcwd() + '\unparsed'):
        if fileName != 'Barack_Obama.txt': continue  # Testing
        print fileName
        try:      
            # Parsing 
            data = open('unparsed/' + fileName).read()
            data = filter(lambda x: x in string.printable, data)
            parser = NLPParser(data)
            
            f = open('parsed.txt', 'w')
            parsed_data = { 'sentences': parser.sentences }
            json.dump(parsed_data, f)
            
            # Saving parsed data
            #f = open('parsed/' + fileName, 'w')
            #parsed_data = { 'words': parser.words, 'headers': parser.headers , 'title': parser.title }
            #json.dump(parsed_data, f)
            
        except Exception as e:
            print "Could not parse file:", e
            print type(e)
            
if __name__ == "__main__":
    main()
