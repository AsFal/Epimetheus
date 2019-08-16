from urllib.request import urlopen
from bs4 import BeautifulSoup
from pprint import pprint
from nltk.corpus import stopwords
import nltk

# Source
# https://towardsdatascience.com/gentle-start-to-natural-language-processing-using-python-6e46c07addf3

# Get SpaceX html page
response = urlopen('https://en.wikipedia.org/wiki/SpaceX')
html = response.read()

# Convert html to somewhat readable text
soup = BeautifulSoup(html, 'html.parser')
text = soup.get_text(strip = True)

tokens = [t for t in text.split()]

sr = stopwords.words('english')
clean_tokens = tokens[:]
for token in tokens:
    if token in stopwords.words('english'):
        clean_tokens.remove(token)
freq = nltk.FreqDist(clean_tokens)
for key, val in freq.items():
    print(str(key) + ':' + str(val))

freq.plot(20, cumulative=False)
