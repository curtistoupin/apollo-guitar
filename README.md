# apollo-guitar
The Apollo guitar helps players learn by enabling them to practise on a fretboard which lights up to any scale or chord with colors corresponding to different notes. The scale or chord can be chosen using buttons and a display on the body of the guitar. The guitar also has a basic on-board amplifier and speaker as well as a basic overdrive circuit for distortion. These are controlled via knobs located next to the standard volume/tone knobs. A split 1/4" output jack is used so that when the jack is plugged in the pickup signal is cut off from the amp circuit.

This project contains
 *An R script used to calculate the exact (center) positions of LEDs on the fretboard for the custom PCB design and manufacturing process (./fretboard-led-position-locator.R)
 *A set of 3D printed jigs used to help with routing and drilling in the correct locations for allowing the PCB to align properly with the fretboard (./templates/)
 *A copy of the code required for a Raspberry Pi Pico to control the fretboard and a display. As coded, the display used must be based on a ST7735 chip (./source/)