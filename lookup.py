from nltk.corpus import wordnet
from sys import argv

def lookup(word):
	print wordnet.synsets(word)[0].definition

if __name__ == '__main__':
	word = argv[0] if len(argv) > 0 else 'hacker'
	lookup('penis')
