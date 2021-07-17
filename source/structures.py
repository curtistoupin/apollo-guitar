#Use dict to enumerate notes for tunings and determining LED values
#Keys are identical to note names for convenience
notes = {
    "A" : 0,
    "B`" : 1,
    "B" : 2,
    "C" : 3,
    "C#" : 4,
    "D" : 5,
    "E`" : 6,
    "E" : 7,
    "F" : 8,
    "F#" : 9,
    "G" : 10,
    "A`" : 11
}

#Note names used for printing on the display. Backticks (`) are used to denote a flat
#and pound signs (#) are used to denote a sharp. Custom shapes have been added to the 
#font definition lib/sysfont.py to replace ` with a flat symbol and # with a sharp symbol
noteNames = ("A", "B`", "B", "C", "C#", "D", "E`", "E", "F", "F#", "G", "A`")

class StructureType:
    nstructures = 2
    scale = 0
    chord = 1

#Notes here are defined as a number of semitones away from the root note
#This allows scales to be defined independent of a root note
class Scale:
    def __init__(self, name, notes, colors):
        self.name = name
        self.notes = notes
        self.colors = colors
        
#Notes here are defined as a number of semitones away from the root note
#This allows chords to be defined independent of a root note
class Chord:
    def __init__(self, name, notes, colors):
        self.name = name
        self.notes = notes
        self.colors = colors
        
#Notes here are defined as their numerical value in the notes dict
#This allows us to reconstruct actual note values from a root note and a scale/chord shape
class Tuning:
    def __init__(self, name, notes):
        self.name = name
        self.notes = notes
    