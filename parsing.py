from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import os, string, util
from htmlentitydefs import name2codepoint
import json


class MyHTMLParser(HTMLParser):
    def __init__(self, data=''):
        HTMLParser.__init__(self)
        self.isPrinting = False
        self.endOfContent = False
        self.isHeader = False
        self.rawData = data
        
        self.words = util.Counter()
        self.headers = []
        
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
            self.isHeader = True

        # Do we only care about things in <p> tags?
        # That is all the paragraphs of "content"
        # (no tables, captions, images, lists)
        
    def handle_endtag(self, tag):
        # if tag == 'html':
        #     print "End of document"
        #     print "Total words:", self.words.totalCount()
            
        #     # Further processing?
        
        if tag == 'h2' or tag == 'h3' or tag == 'h4':
            self.isHeader = False

            
            
    def handle_data(self, data):
        # Hardcoding so much stuff
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
            validCharFn = lambda x: x in string.letters or x in string.digits or x in string.whitespace or x == '\'' or x == '-'
            data = filter(validCharFn, data)
            data = data.split()
            
            for w in data:
                self.words[w] += 1
                
            if self.isHeader:
                self.headers.append(data)
                

# Test code
def main():
    print os.getcwd()
    for fileName in os.listdir(os.getcwd() + '\unparsed'):
        # if fileName != 'BenjaminHarrison.txt': continue  # Testing
        print fileName
        try:      
            # Parsing 
            data = open('unparsed/' + fileName).read()
            data = filter(lambda x: x in string.printable, data)
            parser = MyHTMLParser(data)
            
            f = open('parsed/' + fileName, 'w')
            parsed_data = { 'words': parser.words, 'headers': parser.headers }
            json.dump(parsed_data, f)
            
        except Exception as e:
            print "Could not parse file:", e
            print type(e)
            
if __name__ == "__main__":
    main()
