import array
import rp2
from machine import Pin
from defines import *
from structures import *

@rp2.asm_pio(sideset_init = rp2.PIO.OUT_LOW, out_shiftdir = rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh = 24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1) .side(0) [T3-1]
    jmp(not_x, "do_zero") .side(1) [T1-1]
    jmp("bitloop") .side(1) [T2-1]
    label("do_zero")
    nop() .side(0) [T2-1]
    wrap()

class Fretboard:
    def __init__(self, string_pins):
        self.rootNote = notes["E"]
        self.structuretype = StructureType.scale
        self.tuning = tunings_list[0]
        self.structure = structures_list[self.structuretype][0]
        self.brightness = DEFAULT_BRIGHTNESS
        
        #Create a state machine for each string with the corresponding output pin
        self.sm_arr = [rp2.StateMachine(i, ws2812, freq = 8_000_000, sideset_base = Pin(string_pins[i])) for i in range(NUM_STRINGS)]
        for sm in self.sm_arr:
            sm.active(1)
            
        self.color_arr = [array.array("I", [0 for _ in range(NUM_LEDS)]) for _ in range(NUM_STRINGS)]
    
    #sends signal to designated string to tell it to display colors currently stored in color_arr for that string
    def led_string_show(self, string):
        sm = self.sm_arr[string-1]
        dimmer_arr = array.array("I", [0 for _ in range(NUM_LEDS)])
        for i, c in enumerate(self.color_arr[string-1]):
            r = int(((c>>8) & 0xFF) * self.brightness)
            g = int(((c>>16) & 0xFF) * self.brightness)
            b = int((c & 0xFF) * self.brightness)
            #ws2812 expects color information in GRB format
            dimmer_arr[i] = (g<<16) + (r<<8) + b
        sm.put(dimmer_arr, 8)
        
    #sends signals to all strongs to tell them to display colors currently stroed in color_arr
    def show(self):
        for string in range(NUM_STRINGS):
            self.led_string_show(string+1)
        
    #sets color in color_arr for a particular string and fret (does not update fretboard)
    def set_led(self, string, fret, color):
        self.color_arr[string-1][NUM_FRETS - fret] = (color[1] << 16) + (color[0]<<8) + color[2]
        
    #sets color for all frets on a particular string to a single color (does not update fretboard)
    def set_string(self, string, color):
        for fret in range(NUM_LEDS):
            self.set_led(string, fret, color)
        
    #sets color for all frets on all strings to a single color (does not update fretboard)
    def set_all_leds(self, color):
        for string in range(NUM_STRINGS):
            self.set_string(string, color)
    
    #sets color for all frets on all strings to black and updates fretboard
    def reset(self):
        self.set_all_leds(BLACK)
        self.show()
    
    #determines what color an LED should be based on what note it is supposed to be showing
    def get_led_color(self, note):
        if note in self.structure.notes:
            return self.structure.colors[self.structure.notes.index(note)]
        else:
            return BLACK
    
    #updates all fret positions on all strings to appropriate color for the note it is showing, then updates fretboard
    def update_board_colors(self):
        self.reset()
        for string in range(NUM_STRINGS):
            stringRoot = self.tuning.notes[string]
            for fret in range(NUM_LEDS):
                fretNote = (stringRoot + fret - self.rootNote)%12
                self.set_led(string+1, fret, self.get_led_color(fretNote))
        self.show()
        
    #shifts the root note up by one fret/semitone and updates fretboard
    def increment_root_note(self):
        self.rootNote = (self.rootNote + 1)%12
        self.update_board_colors()
        
    #switches the current structure between available variations of that structure (e.g. between scale shapes for scales) and updates fretboard
    def next_structure(self):
        structure_index = structures_list[self.structuretype].index(self.structure)
        structure_index = (structure_index + 1)%len(structures_list[self.structuretype])
        self.structure = structures_list[self.structuretype][structure_index]
        self.update_board_colors()
        
    #switches between available tunings and updates fretboard
    def next_tuning(self):
        tuning_index = tunings_list.index(self.tuning)
        tuning_index = (tuning_index + 1)%len(tunings_list)
        self.tuning = tunings_list[tuning_index]
        self.update_board_colors()
        
    #switches between available musical structure types (chords, scales, etc) and updates fretboard
    def next_structuretype(self):
        self.structuretype = (self.structuretype + 1)%StructureType.nstructures
        self.structure = structures_list[self.structuretype][0]
        self.update_board_colors()
            