import json
import requests
import re
from bs4 import BeautifulSoup


class PageGrabber:
    def __init__(self, url):
        self.url = url

    def scrape(self):
        res = requests.get(self.url)
        soup = BeautifulSoup(res.content, "html.parser")
        self.text = soup.get_text()
    def getText(self):
        return self.text

class CitationParser:

    # Define regex patterns here as constants

    ################
    ####EXAMPLES####
    ################

    # BASIC => Uri D. Herscher, Jewish Agricultural Utopias in America, 1880-1910 (Detroit: Wayne State University Press, 1991), 123.
    # WIKIPEDIA-BIB => Diamond, Jared (2005). Collapse. How Societies Choose to Fail or Succeed. New York: Viking. ISBN 978-0-14-303655-5.
    _PATTERNS = {
        "BASIC" : re.compile(r'.*, .* \(.*,\s(?:Inc\.\s)?\d\d\d\d\)(?:,)?\s?(?:\d*(?:,\s)?)*\.'),
        "ISBN" : re.compile(r'ISBN:?\s(?P<isbn>(?:\d|-)+)'),
        "WIKIPEDIA-BIB" : re.compile(r'(?:[a-z] )*(?P<author>(?:[A-Za-z]\.?\,? ?)*)\((?P<year>\d\d\d\d)\)\.\s(?P<title>[^"\n]*\.\s)(?:(?P<city>(?:\w\.?,?\s?)*):\s)(?P<publisher>(?:\w\'?\s?)*)\.\s(?:ISBN\s(?P<isbn>(?:\d-?)+)\.)?')
    }
    _FIELDS = ["author", "title", "city", "publisher", "year", "isbn"]
    def __init__(self, pattern = "basic"):
        self.pattern = self._PATTERNS[pattern.upper()]

    def findall(self,string):
        return self.pattern.findall(string)
    def finditer(self, string):
        return self.pattern.finditer(string)
# TODO: Union all regex's (https://stackoverflow.com/questions/3274027/python-defining-a-union-of-regular-expressions)

class BookSearch:

    def getIdentifier(isbn):
        response = BookSearch.searchISBN(isbn)
        pattern = re.compile(r'"identifier":"(?P<identifier>[A-Za-z\d]*)"')
        result = pattern.search(response)
        if result:
            return result.group('identifier')
        else:
            return None
    def searchISBN(isbn):
        isbn_10, isbn_13 = BookSearch.parseISBN(isbn)
        query = BookSearch.getQuery(isbn_10, isbn_13)
        url = 'https://archive.org/advancedsearch.php?q='+query+'&fl%5B%5D=identifier&sort%5B%5D=&sort%5B%5D=&sort%5B%5D=&rows=50&page=1&output=json&callback=callback&save=yes'
        res = requests.get(url)
        return res.text

    def parseISBN(isbn):
        clean_isbn = BookSearch.normalize(isbn)
        isbn_10, isbn_13 = "", ""
        if(len(clean_isbn) == 10):
            isbn_10 = clean_isbn
            isbn_13 = BookSearch.getISBN13(isbn_10)
        elif(len(clean_isbn) == 13):
            isbn_13 = clean_isbn
            isbn_10 = BookSearch.getISBN10(isbn_13)
        else:
            return None
        return isbn_10, isbn_13

    def getQuery(isbn10, isbn13):
          return 'mediatype:texts AND (isbn:' + isbn10 + ' OR isbn:'+isbn13+' OR related-external-id:"urn:isbn:'+isbn10+'" OR related-external-id:"urn:isbn:'+isbn13+'")'

    def normalize(isbn):
        normalized = re.sub(r'[^0-9Xx]+', '', isbn)
        return normalized if(len(normalized) != 9) else "0" + normalized

    def getISBN10(isbn):
        isbn_no_check = isbn[:-1]
        if(isbn_no_check[:3] != "978"):
            return False
        isbn9 = isbn_no_check[3:]
        return isbn9 + str(BookSearch.checksum(isbn9))
    def getISBN13(isbn):
        isbn_no_check = isbn[:-1]
        isbn12 = "978" + isbn_no_check
        return isbn12 + str(BookSearch.checksum(isbn12))

    def checksum(isbn):
        sum = 0
        if(len(isbn) == 9):
            for i in range(9):
                sum += (i+1)*int(isbn[i])
            check = sum%11
            return (10-(sum%10))%10
        if(len(isbn) == 12):
            k = 1
            for i in range(12):
                sum += int(isbn[i])*k
                k = 4-k
            return (10-(sum%10))%10
        return None
