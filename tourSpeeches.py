import pyttsx
engine = pyttsx.init()
engine.setProperty('rate', 120)
engine.setProperty('voice', 'english+f3')
engine.say("Below is the O U Sooner Rover Team. This is an O U engineering competition team composed of mechanical, electrical, aerospace, and computer engineers. They design, build, and document a rover for the University Rover Challenge competition. The competition takes place on May 30th at the Mars Societies Mars Desert Research Station.")

engine.say("Below is the Sooner Off Road Team. Sooner Off Road designs and builds a go-kart style off-road vehicle to race in Baja S A E competitions each year, where they compete against hundreds of teams from around the world.")

engine.say("Below is the Crimson Skies Design Build Fly team. The team competes in an international engineering competition to develop an unmanned aerial system that is required to complete a series of missions, which vary from year to year.")

engine.say("Below is the Boomer Rocket Team. The Boomer Rocket Team does research, design, and developing of High-powered rockets for the purpose of competing against other universities. We do tasks such as programming, fiberglassing, testing of chemicals, etc.. Competitions take place nationally.")

engine.say("Below is the E V Grand Prix team. The E V Grand Prix team works to research, design and develop electric vehicles to compete in a variety of races. Competitions take place at the Indianapolis Motor Speedway.")

print(engine.getProperty('rate'))

engine.runAndWait()
