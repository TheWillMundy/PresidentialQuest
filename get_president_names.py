import urllib2
from bs4 import BeautifulSoup

html = urllib2.urlopen('http://www.ipl.org/div/potus/').read()
soup = BeautifulSoup(html, "html5lib")

soup = soup.find('table', {'class': 'potusTableIndex'})
for listItem in soup.findAll('li'):
    text = listItem.a.text
    find_comma = text.index(',')
    print text[:find_comma]
