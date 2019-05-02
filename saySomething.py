import pyttsx
import sys
engine = pyttsx.init()
engine.setProperty('rate', 120)
engine.setProperty('voice', 'english+f3')

engine.say(sys.argv[1])

engine.runAndWait()
