from modtrack import tracker
import pygame


#################################################################
#PLAY DEFAULT SAMPLES AND TRACK
#################################################################

#init the tracker module
screen=tracker.init(0x40,(100,100))

#make default/internal pattern
tracker.make_pattern()

#play pattern
tracker.play_pattern()


#################################################################
#PLAY WHILE USER DOES NOT QUIT PROGRAM
#################################################################

while True:#player.isAlive():
    for event in pygame.event.get():

        #Key event
        if event.type == pygame.KEYDOWN:
            #Close window
            if event.key==pygame.K_ESCAPE:
                tracker.abort_play()
                quit()

        # Window Close Button
        if event.type == pygame.QUIT:
            tracker.abort_play()
            quit()
