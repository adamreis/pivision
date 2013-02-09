import os
import continuous_listen
import translate
import lookup
from time import sleep
import RPi.GPIO as GPIO

def init():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(23, GPIO.IN)

def espeak(phrase):
	os.system('espeak "' + phrase + '"')

def process_lookup(word):
	result = lookup.lookup(word)
	if result != "-1":
		espeak("The definition of " + word + " is " + result)
	else:
		espeak("Error looking up " + word)

def process_translate(rest_of_sentence):
	if word == "translate":
        	rest_of_sentence = words[i+1:]
                for j,graph in enumerate(rest_of_sentence):
                	if graph=="into":
                        	sentence = " ".join(words[i+1:j])
                        	language = words[j+1]
				espeak("translate " + sentence + " into " + language + " ")
                        	os.system('espeak "' + 'translate ' + sentence + 'into'+language +'"')
                                translation = translate.translate(sentence, "es")
                                espeak(translation)

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
			process_translate(words[i+1:])

init()

while True:
	if ( GPIO.input(23)== False ):
		espeak("say a command")
		hypos = continuous_listen.listen()
        	if len(hypos) > 0:
			process_utterance(hypos)
		else:
			espeak("Command not understood")

	hypos = continuous_listen.listen()
  	if len(hypos) > 0:
		process_utterance(hypos)
