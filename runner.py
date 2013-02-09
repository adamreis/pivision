import os
import continuous_listen
import translate
#import lookup
from time import sleep
import RPi.GPIO as GPIO

lang_dict = {'english': 'en', 'spanish': 'es', 'french': 'fr', 'german': 'de', 'chinese': 'zh', 'portuguesse': 'pt', 'russian': 'ru'}
rev_lang_dict = dict([[v,k] for k,v in lang_dict.items()])

def init():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(2, GPIO.IN)

def espeak(phrase, language="en-us"):
	os.system('espeak -v ' + language + '"' + phrase + '"')

def process_lookup(word):
	result = lookup.lookup(word)
	if result != "-1":
		espeak("The definition of " + word + " is " + result)
	else:
		espeak("Error looking up " + word)

def process_translate(i, words):
	from_language = "en"
	into_language = "en"

	for j,graph in enumerate(words):
		if graph == "from":
			from_language = words[j+1]
		if graph =="into":
			into_language = words[j+1]
	
	if from_language in rev_lang_dict and into_language in rev_lang_dict:
		espeak("translate from " + from_language + " into " + into_language) 		
		espeak("say the phrase: ")
		hypos = continuous_listen.listen(from_language)
                if len(hypos) > 0 and type(hypos) is not str:
			confidence, speech = hypos[0]['confidence'], str(hypos[0]['utterance'])
			espeak("translating ")
			espeak(speech, language_dict[from_language])
			espeak("into " + into_language)
			translation = translate.translate(sentence, language_dict[into_language])
			espeak(translation, language_dict[into_language])
		else:
			espeak("input not understood")	
	else:
		espeak("language is not supported")

def process_utterance(hypos):
	confidence, speech = hypos[0]['confidence'], str(hypos[0]['utterance'])
	if confidence > 0.50:
        	print speech
	os.system('espeak "' + speech + '"')

	words = speech.split(' ')
	for i,word in enumerate(words):
		if word =="define":
                	process_lookup(words[i+1])
		if word =="translate":			
			process_translate(i, words)

init()

while True:

	if ( GPIO.input(2) == True ):
		espeak("say a command")
		hypos = continuous_listen.listen()
        	if len(hypos) > 0 and type(hypos) is not str:
			process_utterance(hypos)
		else:
			espeak("Command not understood")
		sleep(1)
	else:
		espeak("not being recognized")

	# hypos = continuous_listen.listen()

  	# if len(hypos) > 0 and  type(hypos) is not str:
		# process_utterance(hypos)
