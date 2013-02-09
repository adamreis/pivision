""" Record audio from the microphone and encode as x-speex-with-header-byte to pass to Google
    for speech recognition.

    Aaron J. Miller, 2012. No copyright held. Use freely for your purposes.
    I provide this code for informational purposes only.
"""

import sys
import pyaudio, speex
import numpy as np  # just for doing a standard deviation for audio level checks
import urllib2
import json

def listen(lang="en-US"):
  e = speex.Encoder()
  e.initialize(speex.SPEEX_MODEID_WB)
  d = speex.Decoder()
  d.initialize(speex.SPEEX_MODEID_WB)  

  chunk = 320 # tried other numbers... some don't work
  FORMAT = pyaudio.paInt16
  bytespersample=2
  CHANNELS = 1
  RATE = 16000 # "wideband" mode for speex. May work with 8000. Haven't tried it.  

  p = pyaudio.PyAudio()  

  # Start the stream to record the audio
  stream = p.open(format = FORMAT,
                  channels = CHANNELS,
                  rate = RATE,
                  input = True,
                  output = True,
                  frames_per_buffer = chunk)  

  print "Listening. Recording will start when some sound is heard."  

  threshold = 1600  # Adjust this to be slightly above the noise level of your recordings.
  nquit = 30 # number of silent frames before terminating the program
  nover = 0
  keepgoing = True
  spxlist=[]  # list of the encoded speex packets/frames
  while keepgoing:
    try:
      data = stream.read(chunk)	
    except IOError as err:
      pass
    # grab 320 samples from the microphone
    spxdata = e.encode(data) # encode using the speex dll
    # print "Length encoded: %d"%len(spxdata) # print the length, after encoding. Can't exceed 255!
    spxlist.append(chr(len(spxdata))+spxdata) # add the length "header" onto the front of the frame  

    a=np.frombuffer(data,np.int16) # convert to numpy array to check for silence or audio
    audiolevel=np.std(a)
    if audiolevel < threshold:  # too quiet
      nover+=1
    else:
      nover=0  

    if nover >= nquit:
      keepgoing=False  

    # print '%2.1f (%d%% quiet)'%(audiolevel, nover*100/nquit)  

  # print "End of input."
  stream.stop_stream()
  stream.close()
  p.terminate()  

  fullspx=''.join(spxlist)  # make a string of all the header-ized speex packets
  # print 'Length before speex: %d, Length after speex: %d'%(len(spxlist)*chunk,len(fullspx))  

  print 'Sending to google.'  

  # see http://sebastian.germes.in/blog/2011/09/googles-speech-api/ for a good description of the url
  url = 'https://www.google.com/speech-api/v1/recognize?xjerr=1&pfilter=1&client=chromium&lang=' + lang + '&maxresults=4'
  header = {'Content-Type' : 'audio/x-speex-with-header-byte; rate=16000'}
  req = urllib2.Request(url, fullspx, header)
  try:
    data = urllib2.urlopen(req)
  except urllib2.HTTPError:
    pass
  if not type(data) is str:
	hypos = json.loads(data.read())['hypotheses']
  else:
	hypos = "-1"
  return hypos
  #yes!
