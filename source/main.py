from defines import *
from structures import *
from fretboard_hal import *
from button_hal import *
from display_hal import *
import time

#initialize hardware
fretboard = Fretboard([D1, D2, D3, D4, D5, D6])
fretboard.update_board_colors()
display = Display(CLK_PIN, SDA_PIN, DC_PIN, RST_PIN, CS_PIN, DISPLAY_HEIGHT, DISPLAY_WIDTH)

root_button = Button(ROOT_BUTTON_PIN)
scale_button = Button(STRUCTURE_BUTTON_PIN)
tuning_button = Button(TUNING_BUTTON_PIN)
structure_type_button = Button(STRUCTURE_TYPE_BUTTON_PIN)

#print default values on display
display.write_tuning(fretboard.tuning.name)
display.write_note(noteNames[fretboard.rootNote])
display.write_scale(fretboard.structure.name)
display.write_structuretype("Scale")
display.write_variant("--")
display.write_scale_notes(fretboard.rootNote, fretboard.structure.notes, fretboard.structure.colors)

#continually watch for buttons to be pressed and perform the corresponding action
while True:
    if root_button.pressed():
        fretboard.increment_root_note()
        display.write_note(noteNames[fretboard.rootNote])
        display.write_scale_notes(fretboard.rootNote, fretboard.structure.notes, fretboard.structure.colors)
    
    if scale_button.pressed():
        fretboard.next_structure()
        display.write_scale(fretboard.structure.name)
        display.write_scale_notes(fretboard.rootNote, fretboard.structure.notes, fretboard.structure.colors)
    
    if tuning_button.pressed():
        fretboard.next_tuning()
        display.write_tuning(fretboard.tuning.name)
    
    if structure_type_button.pressed():
        fretboard.next_structuretype()
        display.write_scale(fretboard.structure.name)
        display.write_structuretype(structure_names[fretboard.structuretype])
        display.write_scale_notes(fretboard.rootNote, fretboard.structure.notes, fretboard.structure.colors)