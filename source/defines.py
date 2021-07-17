from structures import *
from ST7735 import TFT, TFTColor


NOTES_PER_OCTAVE = 12
NUM_STRINGS = 6
NUM_FRETS = 22
NUM_LEDS = NUM_FRETS + 1
DEFAULT_BRIGHTNESS = 0.05

#defines pinout for display
DC_PIN = 22
RST_PIN = 21
CS_PIN = 20
SDA_PIN = 19
CLK_PIN = 18
DISPLAY_HEIGHT = 128
DISPLAY_WIDTH = 160

#colors
BACKGROUND_COLOR = TFT.BLACK
NOTE_COLOR = TFT.GREEN
SCALE_COLOR = TFT.RED
TUNING_COLOR = TFT.PURPLE
MODE_COLOR = TFT.YELLOW
TYPE_COLOR = TFT.CYAN

#defines the pins which read each button
ROOT_BUTTON_PIN = 7
STRUCTURE_BUTTON_PIN = 8
TUNING_BUTTON_PIN = 9
STRUCTURE_TYPE_BUTTON_PIN = 11

#defines the pins which drive each string
D6 = 0
D5 = 1
D4 = 2
D3 = 3
D2 = 10
D1 = 5

#Colors
BLACK = (0,0,0)
RED = (0xFF, 0x00, 0x00)
GREEN = (0x00, 0xFF, 0x00)
BLUE = (0x00, 0x00, 0xFF)
YELLOW = (0xFF, 0xFF, 0x00)
CYAN = (0x00, 0xFF, 0xFF)
MAGENTA = (0xFF, 0x00, 0xFF)
WHITE = (0xFF, 0xFF, 0xFF)

#Color lists for various scale shapes
diatonic_scale_colors = (GREEN, WHITE, YELLOW, WHITE, RED, WHITE, WHITE)
pentatonic_scale_colors = (GREEN, YELLOW, WHITE, RED, WHITE)
minor_blues_scale_colors = (GREEN, YELLOW, WHITE, BLUE, RED, WHITE)
major_blues_scale_colors = (GREEN, YELLOW, BLUE, WHITE, RED, WHITE)
harmonic_minor_scale_colors = (GREEN, WHITE, YELLOW, WHITE, RED, WHITE, MAGENTA)

#Scales
#Notes are defined as the number of semitones away from the root
major = Scale("Major", (0,2,4,5,7,9,11), diatonic_scale_colors)
dorian = Scale("Dorian", (0,2,3,5,7,9,10), diatonic_scale_colors)
phrygian = Scale("Phrygian", (0,1,3,5,7,8,10), diatonic_scale_colors)
lydian = Scale("Lydian", (0,2,4,6,7,9,11), diatonic_scale_colors)
mixolydian = Scale("Mixolydian", (0,2,4,5,7,9,10), diatonic_scale_colors)
minor = Scale("Minor", (0,2,3,5,7,8,10), diatonic_scale_colors)
locrian = Scale("Locrian", (0,1,3,5,6,8,10), diatonic_scale_colors)
minor_pent = Scale("Minor Pentatonic", (0,3,5,7,10), pentatonic_scale_colors)
major_pent = Scale("Major Pentatonic", (0,2,4,7,9), pentatonic_scale_colors)
minor_blues = Scale("Minor Blues", (0,3,5,6,7,10), minor_blues_scale_colors)
major_blues = Scale("Major Blues", (0,2,3,4,6,9), major_blues_scale_colors)
hminor = Scale("Harmonic Minor", (0,2,3,5,7,8,11), harmonic_minor_scale_colors)

scales_list = (major,
               dorian,
               phrygian,
               lydian,
               mixolydian,
               minor,
               locrian,
               minor_pent,
               major_pent,
               minor_blues,
               major_blues,
               hminor)

#Chords
#Notes are defined as number of semitones away from the root
majorchord = Chord("maj", (0, 4, 7), (GREEN, YELLOW, RED))
minorchord = Chord("m", (0, 3, 7), (GREEN, YELLOW, RED))
power = Chord("5 (Power)", (0, 7), (GREEN, RED))
dom7 = Chord("7", (0,4,7,10), (GREEN, YELLOW, RED, WHITE))
maj7 = Chord("maj7", (0,4,7,11), (GREEN, YELLOW, RED, WHITE))
m7 = Chord("m7", (0,3,7,10), (GREEN, YELLOW, RED, WHITE))
sus2 = Chord("sus2", (0,2,7), (GREEN, WHITE, RED))
sus4 = Chord("sus4", (0,5,7), (GREEN, WHITE, RED))
add9 = Chord("add9", (0,2,4,7), (GREEN, WHITE, YELLOW, RED))
madd9 = Chord("madd9", (0,2,3,7), (GREEN, WHITE, YELLOW, RED))

chords_list = (majorchord,
               minorchord,
               power,
               dom7,
               maj7,
               m7,
               sus2,
               sus4,
               add9,
               madd9)

#Compile structures into one object
structures_list = (scales_list,
                   chords_list)

structure_names = ("Scale",
                   "Chord")

#Tunings
#Notes are defined as the number of semitones away from A, as in structures.py
standard = Tuning("E Standard", (notes["E"], notes["A"], notes["D"], notes["G"], notes["B"], notes["E"]))
flatstandard = Tuning("E` Standard", (notes["E`"], notes["A`"], notes["C#"], notes["F#"], notes["B`"], notes["E`"]))
dropd = Tuning("Drop D", (notes["D"], notes["A"], notes["D"], notes["G"], notes["B"], notes["E"]))
openc = Tuning("Open C", (notes["C"], notes["G"], notes["C"], notes["G"], notes["C"], notes["E"]))

tunings_list = (standard,
                flatstandard,
                dropd,
                openc)