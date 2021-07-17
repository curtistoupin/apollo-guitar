library(ggplot2)

scale.length <- 635 #mm
nut.spread <- 33 #string spread @ nut in mm
nut.width <- 43.5 #total nut width in mm
bridge.spread <- 53.7 #string spread @ bridge in mm
led.distance.to.fret <- 4 #distance from led centre to fret centre in mm
num.of.frets <- 22 #number of frets excluding nut/zero
led.width <- 8 #led footprint dimension in the x direction (parallel to fretwire) in mm
led.length <- 8 #led footprint dimension in the y direction (parallel to truss rod) in mm
fretboard.radius <- 12 * 25.4 #fretboard radius in mm (1in x 25.4mm/in)

#takes in fret number and returns distance from nut to centre of fret in mm
fret.distance <- function(fret) {
  return(scale.length*(1-1/2^(fret/12)))
}

#takes position distance from nut in mm and returns string spread at that position in mm
string.spread <- function(distance.from.nut){
  return(nut.spread + (distance.from.nut/scale.length)*(bridge.spread - nut.spread))
}

fretboard.width <- function(distance.from.nut){
  return(string.spread(distance.from.nut) + (nut.width - nut.spread))
}

#takes distance from centre of fretboard on the flat underside and returns the equivalent arclength travelled along the curved top
#this will let me make a printout for the top of the fretboard so i can lay the fretboard on the flat side for drilling
arc.length <- function(lateral.distance) {
  return(fretboard.radius * asin(lateral.distance/fretboard.radius))
}

frets <- c(1:num.of.frets)
fret.distance.from.nut <- fret.distance(frets)
led.distance.from.nut <- c(led.distance.to.fret, fret.distance.from.nut - led.distance.to.fret) #here we add in the nut/zero fret. Leds will be forward from the nut whereas the rest will be behind the fret
led.centre.spread <- string.spread(led.distance.from.nut)
led.fretboard.width <- fretboard.width(led.distance.from.nut)

x.positions <- data.frame(string1 = rep(NA, num.of.frets + 1),
                          string2 = rep(NA, num.of.frets + 1),
                          string3 = rep(NA, num.of.frets + 1),
                          string4 = rep(NA, num.of.frets + 1),
                          string5 = rep(NA, num.of.frets + 1),
                          string6 = rep(NA, num.of.frets + 1))

for(fret in 1:(num.of.frets + 1)){
  x.positions[fret,] <- (-led.centre.spread[fret]/2) + c(0:5)*led.centre.spread[fret]/5
}

#PCB must allow for physical size of LEDs. WS2812s are actually 5mm x 5mm, but I am allowing at least 6mm for each dimension just in case.
##THerefore once the centre of an LED is known, the width of the PCB 3mm (led.length/2 in general) must be at least 6mm = 2*3mm (= 2*(led.width/2 = led.width in general)
#wider than the string spread at the LED center position
min.pcb.width <- function(distance.from.nut) {
  return(led.width + string.spread(distance.from.nut+led.length/2))
}

x.coords <- NULL
for(i in 1:23) {
 x.coords <- c(x.coords, as.numeric(x.positions[i,]))
}

y.coords <- NULL
for(i in 1:23) {
  y.coords <- c(y.coords, rep(led.distance.from.nut[i], 6))
}

pocket.pcb.width <- min.pcb.width(fret.distance(22))
nut.pcb.width <- min.pcb.width(0)
x.coords <- x.coords + pocket.pcb.width/2
x.positions <- x.positions + pocket.pcb.width/2

corners <- data.frame(x=rep(NA,4), y=rep(NA,4))
corners[1,] <- c((pocket.pcb.width-nut.pcb.width)/2,0)
corners[2,] <- c((pocket.pcb.width+nut.pcb.width)/2,0)
corners[3,] <- c(0, fret.distance(22))
corners[4,] <- c(pocket.pcb.width, fret.distance(22))

df <- data.frame(x=x.coords, y=y.coords)
ggplot(df, aes(x=x.coords, y=y.coords)) + 
  geom_point() + 
  geom_segment(x=corners$x[1], y=corners$y[1], xend=corners$x[2], yend=corners$y[2], color="darkgreen") + 
  geom_segment(x=corners$x[2], y=corners$y[2], xend=corners$x[4], yend=corners$y[4], color="darkgreen") + 
  geom_segment(x=corners$x[4], y=corners$y[4], xend=corners$x[3], yend=corners$y[3], color="darkgreen") + 
  geom_segment(x=corners$x[3], y=corners$y[3], xend=corners$x[1], yend=corners$y[1], color="darkgreen")

arc.lengths <- pocket.pcb.width/2 + arc.length(x.positions - pocket.pcb.width/2)
arc.lengths - x.positions #for comparison only the difference between the curved and flat side is only 20 microns. I can't achieve that accuracy with a drill anyway, so I'm not going to bother making a curved image

rotate.by.90 <- function(x ,y) {
  return(data.frame(x = -y, y=x))
}
centered.corners <- data.frame(x = (corners$x - max(corners$x)/2), y=corners$y)
rotated.corners <- rotate.by.90(centered.corners$x, centered.corners$y)
rotated.shifted.corners <- rotated.corners + data.frame(x=rep(900,6), y=rep(200,6))
