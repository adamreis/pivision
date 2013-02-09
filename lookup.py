from nltk.corpus import wordnet
from sys import argv

def lookup(word):
	if len(wordnet.synsets(word)) > 0:
		return wordnet.synsets(word)[0].definition
	else:
		return "-1"
