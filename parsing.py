from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import os, string, util
from htmlentitydefs import name2codepoint


class MyHTMLParser(HTMLParser):
    def __init__(self, data):
        HTMLParser.__init__(self)
        self.isPrinting = False
        self.rawData = data
        
        self.words = util.Counter()
        
        self.feed(data)
        
    def handle_starttag(self, tag, attrs):
        if ('id', 'mw-content-text') in attrs:
            # print "PARSING CONTENT"
            self.isPrinting = True
            
        if ('class', 'printfooter') in attrs:
            # print "END OF CONTENT"
            self.isPrinting = False

        # Do we only care about things in <p> tags?
        # That is all the paragraphs of "content"
        # (no tables, captions, images, lists)
        
    def handle_endtag(self, tag):
        if tag == 'html':
            # print "End of document"
            # print "Total words:", self.words.totalCount()
            
            # Further processing?

            
            
    def handle_data(self, data):
        # Hardcoding so much stuff
        data = data.rstrip()
        if data == '[':
            # Don't print the references [1]
            self.isPrinting = False
        elif data == ']':
            self.isPrinting = True         
        elif self.isPrinting and data != '':            
            # validCharFn basically removes "double quote" characters, punctuation marks '.,:;', and dashes
            # (but keeps contractions -> don't I'm aren't)
            validCharFn = lambda x: x in string.letters or x in string.digits or x in string.whitespace or x == '\''
            data = filter(validCharFn, data)
            data = data.split()
            
            for w in data:
                self.words[w] += 1

# Test code
print os.getcwd()
for fileName in os.listdir(os.getcwd() + '\unparsed'):
    # if fileName != 'Obama.txt': continue  # Testing
    print fileName
    try:      
        ### HTMLParsing
        data = open('unparsed/' + fileName).read()
        data = filter(lambda x: x in string.printable, data)
        parser = MyHTMLParser(data)
        
        
    except Exception as e:
        print "Could not parse file:", e
        print type(e)
