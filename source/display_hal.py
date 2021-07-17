from machine import Pin, SPI
from ST7735 import TFT, TFTColor
from sysfont import sysfont
from time import sleep_ms
from defines import *
from structures import *

TFT.PINK = TFTColor(225, 51, 132)
screen_left = 0
screen_left_offset = 5
screen_top = 0
screen_width = 160
screen_height = 128
scale_notes_height = 11
scale_notes_y = screen_height-scale_notes_height
size_2_rows = 16
type_y = 90
mode_y = 66
scale_x = 43
scale_y = 27
tuning_y = 3
scale_width = screen_width - scale_x + 1
size_4_rows = 32
note_y = 28
note_width = 42
        

#TODO remove magic numbers

class Display:
    def __init__(self, clk_pin, sda_pin, dc_pin, rst_pin, cs_pin, height, width):
        self.spi = SPI(0, baudrate=992063, polarity=1, phase=1, bits=8, sck=Pin(clk_pin), mosi=Pin(sda_pin))
        self.tft = TFT(self.spi, dc_pin, rst_pin, cs_pin)
        self.tft.initr()
        self.tft.rgb()
        self.tft.rotation(1)
        self.tft.fill(BACKGROUND_COLOR)
        self.height = height
        self.width = width
    
    #writes a character string to the display at a given position, ensuring that new lines are started when necessary
    def write_string(self, string, px, py, color=TFT.GREEN, size=1):
        original_x = px
        original_y = py
        words = string.split(" ")
        for i in range(len(words)):
            word = words[i]
            if px + (size*5 + 1)*len(word) - 1 < self.tft._size[0]:
                self.tft.overwrite_text((px, py), str(word), color, BACKGROUND_COLOR, sysfont, size)
                px += (size*5+1)*len(word) - 1
                if px + size*5 + 1 < self.tft._size[0] and i!=(len(words)-1):
                    self.tft.overwrite_text((px, py), " ", color, BACKGROUND_COLOR, sysfont, size)
                    px += size*5 + 2
            else:
                px = original_x
                py += size*8 + 1
                max_letters = int((self.tft._size[0] + 1 - original_x)/(size*5 + 1))
                word = word[0:max_letters]
                self.tft.overwrite_text((px, py), str(word), color, BACKGROUND_COLOR, sysfont, size)
                px += (size*5+1)*len(word) - 1
                if px + size*5 + 1 < self.tft._size[0] and i!=(len(words)-1):
                    self.tft.overwrite_text((px, py), " ", color, BACKGROUND_COLOR, sysfont, size)
                    px += size*5 + 2
                else:
                    px = original_x
                    py += size*8 + 1
        py += size*8 + 1
        return py
    
    #sets lines ystart to yend to background color
    def clear_lines(self, ystart, yend):
        self.tft.fillrect((0, ystart), (self.tft._size[0], yend-ystart-1), BACKGROUND_COLOR)
        
    #writes the scale's root note to the display
    def write_note(self, new_note):
        self.tft.fillrect((screen_left, note_y), (note_width, size_4_rows), BACKGROUND_COLOR)
        note_start_x = screen_left
        if len(new_note) == 1:
            note_start_x += 10
        self.write_string(str(new_note), note_start_x, note_y, NOTE_COLOR, 4)
        
    #writes scale name to the display
    def write_scale(self, new_scale):
        words = new_scale.split(" ")
        scale_start_y = scale_y
        if len(words) == 1:
            scale_start_y += 8
        self.tft.fillrect((scale_x, scale_y), (scale_width, size_4_rows), BACKGROUND_COLOR)
        self.write_string(str(new_scale), scale_x, scale_start_y, SCALE_COLOR, 2)
        
    #writes tuning name to the display top row
    def write_tuning(self, new_tuning):
        self.tft.fillrect((screen_left, tuning_y), (screen_width, size_2_rows), BACKGROUND_COLOR)
        self.write_string(str(new_tuning), screen_left_offset, tuning_y, TUNING_COLOR, 2)
        
    #writes the musical structure type to the display (chords vs scale)
    def write_structuretype(self, new_mode):
        self.tft.fillrect((screen_left,mode_y), (screen_width, size_2_rows), BACKGROUND_COLOR)
        self.write_string(str(new_mode), screen_left_offset, mode_y, MODE_COLOR, 2)
        
    #writes the variant of the current structure type to the display (e.g. 1st position, 2nd position, 1st inversion, etc)
    def write_variant(self, new_type):
        self.tft.fillrect((screen_left, type_y), (screen_width, size_2_rows), BACKGROUND_COLOR)
        self.write_string(str(new_type), screen_left_offset, type_y, TYPE_COLOR, 2)
        
    #used to match colors from fretboard to colors on display for consistency
    def match_fretboard_color(self, color):
        if color == GREEN:
            return TFT.GREEN
        elif color == WHITE:
            return TFT.WHITE
        elif color == YELLOW:
            return TFT.YELLOW
        elif color == BLUE:
            return TFT.BLUE
        elif color == RED:
            return TFT.RED
        elif color == MAGENTA:
            return TFT.PINK
        else:
            return BACKGROUND_COLOR
        
    #writes list of scale (or chord) notes on bottom row of display with note colors matching the colors they appear in on the fretboard
    def write_scale_notes(self, root, notes, colors):
        self.tft.fillrect((screen_left, scale_notes_y), (screen_width, scale_notes_height), BACKGROUND_COLOR)
        px=screen_left_offset
        for i in range(len(notes)):
            note_name = noteNames[(root + notes[i])%NOTES_PER_OCTAVE]
            self.write_string(note_name, px, scale_notes_y, self.match_fretboard_color(colors[i]))
            px += len(note_name)*6 - 1
            if(i + 1 < len(notes)):
                self.write_string(", ", px, scale_notes_y, TFT.WHITE)
                px += 11
            