from machine import Pin
import utime

class Button:
    def __init__(self, pin):
        self.pin = pin
        self.button = Pin(pin, Pin.IN)
        self.current_value = 0
        self.last_value = 0
        self.last_debounce_time = 0
        self.debounce_delay = 10
    
    def value(self):
        return self.button.value()
    
    #returns true if button state changes from unpressed to pressed
    #includes basic debounce check to eliminate accidental double presses
    def pressed(self):
        self.last_value = self.current_value
        self.current_value = self.value()
        if (utime.ticks_ms() - self.last_debounce_time) > self.debounce_delay:
            if self.current_value != self.last_value:
                self.last_debounce_time = utime.ticks_ms()
                if self.current_value:
                    return True
        return False