from modtrack import tracker
import pygame

#################################################################
#LOAD AMIGA MOD FILE
#################################################################
#tracker.octave_transpose=2
#ret=tracker.load_amigamodule('ProTracker-win32/modules/equinoxe ii.mod') #M.K.
#ret=tracker.load_amigamodule('ProTracker-win32/modules.stk/STK.oxygene')  # original 15 samples Soundtracker file
#ret=tracker.load_amigamodule('ProTracker-win32/modules/Tubbs and Valerie.mod')  # M.K.
#D00 ret=tracker.load_amigamodule('ProTracker-win32/modules/BLAKWHIT.MOD')
#D00 ret=tracker.load_amigamodule('ProTracker-win32/modules/waitingfor cousteau.mod') #M.K.
ret=tracker.load_amigamodule('ProTracker-win32/modules/airwolf.MOD')  # M.K. - instruments not playing or pattern in wrong order
#D00 ret=tracker.load_amigamodule('ProTracker-win32/modules/rendez-mix.mod') #M.K.
#D15 ret = tracker.load_amigamodule('ProTracker-win32/modules.stk/eye of the tiger.mod')  # original 15 samples Soundtracker file
#ret=tracker.load_amigamodule('ProTracker-win32/modules/oxygene.mod') #M.K.
#ret=tracker.load_amigamodule('ProTracker-win32/modules/CARIBMEM.MOD')
#ret=tracker.load_amigamodule('ProTracker-win32/modules/boysblue.MOD')
#ret=tracker.load_amigamodule('ProTracker-win32/modules/POPCORN.MOD')  # M.K.
#ret=tracker.load_amigamodule('ProTracker-win32/modules/COUNTRY.MOD')  # M.K.
#ret = tracker.load_amigamodule('ProTracker-win32/modules.stk/tubularbells.mod')  # original 15 samples Soundtracker file
#ret = tracker.load_amigamodule('ProTracker-win32/modules.stk/tubularbells_pt.mod')  # PT 31 samples file
#ret=tracker.load_amigamodule('ProTracker-win32/modules.stk/STK.crockets')  # original 15 samples Soundtracker file
#ret = tracker.load_amigamodule('ProTracker-win32/modules.stk/STK.equinoxe vii')  # original 15 samples Soundtracker file
#ret=tracker.load_amigamodule('ProTracker-win32/modules.stk/STK.magnum2')  # original 15 samples Soundtracker file
#ret=tracker.load_amigamodule('ProTracker-win32/modules.stk/STK.99redballoons')  # original 15 samples Soundtracker file
#ret=tracker.load_amigamodule('ProTracker-win32/modules.stk/STK.7')  # original 15 samples Soundtracker file
#ret=tracker.load_amigamodule('ProTracker-win32/modules.stk/STK.ghostbusters')  # original 15 samples Soundtracker file
#ret=tracker.load_amigamodule('ProTracker-win32/modules/happy.MOD') #M.K.
#ret = tracker.load_amigamodule('ProTracker-win32/modules/equinoxe.mod')  # M.K.
#ret=tracker.load_amigamodule('ProTracker-win32/modules.stk/STK.combodia')  # original 15 samples Soundtracker file
#ret = tracker.load_amigamodule('ProTracker-win32/modules.stk/STK.airwolf')  # original 15 samples Soundtracker file
#ret = tracker.load_amigamodule('ProTracker-win32/modules.stk/souvenir of china [stk].mod')  # original
#ret=tracker.load_amigamodule('ProTracker-win32/modules.stk/STK.popcorn')  # original 15 samples Soundtracker file
#ret=tracker.load_amigamodule('ProTracker-win32/modules.stk/STK.ghostriders')  # original 15 samples Soundtracker file
#ret = tracker.load_amigamodule('ProTracker-win32/modules.stk/STK.dont-cry')  # original 15 samples Soundtracker file
#ret = tracker.load_amigamodule('ProTracker-win32/modules.stk/STK.in the army now')  # original 15 samples Soundtracker file
#ret=tracker.load_amigamodule('ProTracker-win32/modules/moskwa.MOD') #M.K. - instruments not playing or patterns in wrong order
#ret=tracker.load_amigamodule('ProTracker-win32/modules.stk/STK.dervish')  # original 15 samples Soundtracker file
#ret=tracker.load_amigamodule('ProTracker-win32/modules.stk/STK.starwars')  # original 15 samples Soundtracker file
#ret = tracker.load_amigamodule('ProTracker-win32/modules.stk/STK.magnetic_nj.mod')  # original 15 samples Soundtracker file
#ret=tracker.load_amigamodule('ProTracker-win32/modules.stk/thunderchild.mod')  # original 15 samples Soundtracker file

#INSTRUMENTS DON'T PLAY CORRECTLY
#ret=tracker.load_amigamodule('ProTracker-win32/modules/final_fantasy.mod') #M.K.
#ret=tracker.load_amigamodule('ProTracker-win32/modules/magnetic fields.mod') #M.K.
#ret=tracker.load_amigamodule('ProTracker-win32/modules/enigma.mod')  # M.K.

#NOT WORKING
#ret=tracker.load_amigamodule('ProTracker-win32/modules/2peaks.mod') #8CHN
#ret=tracker.load_amigamodule('ProTracker-win32/modules.stk/STK.magnetic fields iv.crb-md-version')  # CORRUPT - original 15 samples Soundtracker file (Axy commands are replaced by Dxy commands

#TEST MODULES
#tracker.load_amigamodule('TEST_SAMPLE_REPEAT.MOD')  # M.K.
#tracker.load_amigamodule('TEST_D.MOD')  # M.K.
#tracker.load_amigamodule('TEST_SAMPLE_NR.MOD')  # M.K.

#ret = tracker.load_amigamodule('tests/TEST_C3.MOD')  # M.K.
#ret = tracker.load_amigamodule('ProTracker-win32/modules/Tubbs and Valerie.mod')  # M.K.
#ret = tracker.load_amigamodule('TEST_7.MOD')  # M.K.
#ret = tracker.load_amigamodule('TEST_A.MOD')  # M.K.
#ret = tracker.load_amigamodule('TEST_A_REV.MOD')  # M.K.
#ret = tracker.load_amigamodule('TEST_2.MOD')  # M.K.
#ret = tracker.load_amigamodule('TEST_0.MOD')  # M.K.
#ret = tracker.load_amigamodule('TEST_4.MOD')  # M.K.

#if not ret: return
#quit()

#import cProfile as profile
#profile.run('tracker.make_pattern()')
#profile.run('tracker.save("test3.pyt")')
#quit()

#import time
#t0=time.time()


#################################################################
#INIT, MAKE AND PLAY
#################################################################

screen=tracker.init(0x40,(100,100))
tracker.make_pattern(True) #True because we load a legacy module format ([C-2 01 F01] instead of [C-2 --- 01 F01 ---])
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
