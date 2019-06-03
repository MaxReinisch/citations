import citations
print("Test Started.")

parser = "ISBN"
# url = "http://www.world-nuclear.org/information-library/safety-and-security/safety-of-plants/chernobyl-accident.aspx"
url = "https://en.wikipedia.org/wiki/Easter_Island"
# url = "https://jwa.org/teach/livingthelegacy/jews-and-farming-in-america"

page = citations.PageGrabber(url)
page.scrape()
print("Page Downloaded Successfully.")
# print(page.getText())
parser = citations.CitationParser(parser)
for count, citation in enumerate(parser.finditer(page.getText())):
    print("Citation: %d" % count)
    # for field in parser._FIELDS:
    #     if(citation.group(field)):
    #         print(field + ": " + citation.group(field))
    #     else:
    #         print(field + ": ''")

    print(citation.group())
    print(citations.BookSearch.getIdentifier(citation.group('isbn')))
    print()
