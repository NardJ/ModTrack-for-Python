from modtrack import tracker

import pygame
from textfield import Textfield

#for file dialogs
import tkinter as tk
import os
from tkinter import filedialog
from tkinter import messagebox
tkroot = tk.Tk()
tkroot.withdraw()
fd_opts = {}
fd_opts['initialdir'] = [os.path.dirname(os.path.abspath(__file__))]

ret=tracker.load_amigamodule('ProTracker-win32/modules/oxygene.mod') #M.K. (make_pattern: 2.8s)
#ret = tracker.load_amigamodule('ProTracker-win32/modules/Tubbs and Valerie.mod')  # M.K.
#ret = tracker.load_amigamodule('ProTracker-win32/modules/equinoxe.mod')  # M.K.
#ret=tracker.load_amigamodule('ProTracker-win32/modules/POPCORN.MOD')  # M.K.
#ret=tracker.load_amigamodule('ProTracker-win32/modules/equinoxe ii.mod') #M.K.
#ret=tracker.load_amigamodule('ProTracker-win32/modules.stk/STK.ghostbusters')  # original 15 samples Soundtracker file


#ret = tracker.load_amigamodule('TEST_0.MOD')  # M.K.

#################################################################
#INIT SCREEN AND TRACKER
#################################################################

#determine resolution/window-size on nr of rows to display
nr_rows=12
resolution=(89*8,(nr_rows+5)*8)

#init the tracker module and make pattern
screen=tracker.init(0x40,resolution)
dummy, raw_pattern_text, cumtimings = tracker.make_pattern(True)

#load a font
pygame.font.init()
myfont = pygame.font.Font('C64_Pro_Mono-STYLE.ttf', 8)


#################################################################
#PLAY AND DISPLAY TRACK
#################################################################

#Construct screen from textfields
if tracker.songtitle=="" : tracker.songtitle=tracker.filename
textfields=[]
str_songtitle="{:_<20}".format(tracker.songtitle[:20].replace(" ", "_").upper())
str_samples="{:_<22}".format(tracker.samples[0]["name"][:22].replace(" ", "_").upper())
str_samples="1234567890123456789012"
tf_label_songtitle  = Textfield((1,1),"NAME:",True)
tf_songtitle        = Textfield((6,1),str_songtitle,[],20)
tf_load             = Textfield((27,1),"L",True)
tf_save             = Textfield((29,1),"S",True)
tf_new              = Textfield((31,1),"N",True)
tf_load.border      = (255,255,255)
tf_save.border      = (255,255,255)
tf_new.border       = (255,255,255)
tf_label_samples    = Textfield((46,1)," | SAMPLE:",True)
tf_samplenr         = Textfield((56,1),"01|",True)
tf_samples          = Textfield((59,1),str_samples,[],22)
tf_prev             = Textfield((81,1),"<",True)
tf_next             = Textfield((82,1),">",True)
tf_prev.border      = (255,255,255)
tf_next.border      = (255,255,255)
tf_time             = Textfield((74,nr_rows+4),"000:000 | 0000",True)
tf_time.color       = (255,255,255)
tf_status           = Textfield((1,nr_rows+4),"STATUS:PLAY",True)
tf_status.color     = (255,255,255)
str_sequence        = "--- --- 00 000 000"
all_hex             = '0123456789abcdef'
allowed             = ['abcdefg','#-','12345','',\
                       'abcdefg','#-','12345','',\
                       all_hex,all_hex,'',\
                       all_hex,all_hex,all_hex,'',\
                       all_hex,all_hex,all_hex]
uneditable_sequence = [3,7,10,14]
textfields.append(tf_label_songtitle)
textfields.append(tf_songtitle)
textfields.append(tf_load)
textfields.append(tf_save)
textfields.append(tf_new)
textfields.append(tf_label_samples)
textfields.append(tf_samplenr)
textfields.append(tf_samples)
textfields.append(tf_prev)
textfields.append(tf_next)
textfields.append(tf_time)
textfields.append(tf_status)
first_textfield=len(textfields)+1 #so we don't count first row-nr text-field
for row in range(0, nr_rows):
    pos = (1, row + 3)
    tf_row_id = Textfield(pos,"{:03d} |".format(row),True)
    textfields.append(tf_row_id)
    for col in range (0,4):
        pos=(7+col*21,row+3)
        div=((col+1)*21+5,row+3)
        tf_sequence=Textfield(pos,str_sequence,uneditable_sequence,None,allowed)
        textfields.append(tf_sequence)
        if col<3:
            tf_div=Textfield(div, "|",True)
            textfields.append(tf_div)

# space will unpause and pause so state should be logged
#init cursor
play_offset = nr_rows // 3
# start player
activerow=0
active_textfield=textfields[first_textfield+(nr_rows-play_offset) *8]
cursor=active_textfield.startpos
edited=False
pause = False
samplenr=0
tf_samplenr.text = "{:02d}".format(samplenr)
tf_samples.text = tracker.samples[samplenr]["name"]
player = tracker.play_pattern()
while True:
    #clean screen
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((0, 0), resolution))
    #draw cursor
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((cursor[0]*8,cursor[1]*8), (8, 8)),0)
    #draw screen
    if pause:
        pos = "{:07.3f} | {:04}".format(tracker.get_play_pos(), activerow)
        tf_time.text = pos
        if textfields.index(active_textfield)>=first_textfield:
            offset=nr_rows-(cursor[1]-3)
            pass
    else:
        pos = "{:07.3f} | {:04}".format(tracker.get_play_pos(), tracker.get_play_row())
        tf_time.text = pos
        offset = play_offset
        activerow = tracker.get_play_row()

    for i in range(0,nr_rows):
        pattern_rownr = activerow + i - nr_rows + offset
        textfield=textfields[first_textfield-1 + i * 8]
        if 0<=pattern_rownr<len(raw_pattern_text):
            textfield.text="{:03d} |".format(pattern_rownr)
        else:
            textfield.text = ""
        if i == nr_rows - offset:
            textfield.color = (255, 255, 255)
        else:
            textfield.color = (255, 0, 255)
        for channel in range(0,4):
            textfield=textfields[first_textfield + i * 8 + channel * 2]
            if 0 <= pattern_rownr < len(raw_pattern_text):
                textfield.text = raw_pattern_text[pattern_rownr][channel]
            else:
                textfield.text = ""
            if i==nr_rows-offset:
                textfield.color = (255,255,255)
            else:
                textfield.color = (255, 0, 255)
            pass
        if textfields.index(active_textfield)>=first_textfield:
            active_textfield.color = (255,255,0)
    for textfield in textfields:
        textfield.draw(myfont,screen)
    pygame.display.flip()
    pygame.time.Clock().tick(60)

    #check for user events
    for event in pygame.event.get():

        #Key event
        if event.type == pygame.KEYDOWN:
            #Close window
            if event.key==pygame.K_ESCAPE:
                tracker.abort_play()
                quit()
            #Play control
            if event.key==pygame.K_RALT:
                pause=False
                if edited:
                    tracker.make_pattern(False, raw_pattern_text)
                    edited = False
                # resume
                player = tracker.play_pattern()
            if event.key==pygame.K_SPACE:
                if pause:#not is_playing:
                    #set cursor
                    cursor=(7,3 + nr_rows - play_offset)
                    idx=first_textfield+(nr_rows-play_offset)*8
                    active_textfield=textfields[idx]
                    #we could play from cursor, but from now we resume from pause
                    #we should reparse edited raw_track_pattern
                    tf_status.text = "STATUS:RESYNTH"
                    if edited:
                        tracker.make_pattern(False,raw_pattern_text)
                        edited = False
                        tracker.play_pattern(None, tracker.get_play_pos())
                    #resume
                    else:
                        tracker.resume_play()
                    pause=False
                    tf_status.text="STATUS:PLAY"
                    print ("RESUME playback")
                else:
                    print("PAUSE playback")
                    tf_status.text = "STATUS:PAUSE"
                    pause=True
                    tracker.pause_play()
                    #set cursor and active_textfield
                    cursor=(7,3 + nr_rows - offset )
                    idx=first_textfield+(cursor[1]-3)*8
                    active_textfield=textfields[idx]
            #Edit
            req_next_row  = False
            req_next_char = False
            req_next_field= False
            req_prev_field= False
            if activerow == len(raw_pattern_text):
                raw_pattern_text.append(["--- --- 00 000 000"] * 4)
                active_textfield.text="--- --- 00 000 000"
            for textfield in textfields:
                idx=textfields.index(textfield)
                if textfield.edit(event.key,cursor):
                    if idx<first_textfield:   #we are editing song title or sample names
                        req_next_char= True
                    else:       #we are in pattern data
                        edited=True
                        req_next_row = True
                        channel=((idx-first_textfield)%8)//2
                        print ("activerow, channel:",activerow, channel)
                        raw_pattern_text[activerow][channel]=textfields[idx].text

            #Navigate (only if not playing)
            if pause:
                if event.key == pygame.K_UP:
                    idx=textfields.index(active_textfield)
                    char_nr=active_textfield.char_nr(cursor)
                    if idx>first_textfield+6:
                        active_textfield=textfields[idx-8]
                        cursor=(active_textfield.startpos[0]+char_nr,active_textfield.startpos[1])
                    if idx>=first_textfield and activerow>0:
                        activerow=activerow-1
                if event.key == pygame.K_DOWN or req_next_row:
                    idx=textfields.index(active_textfield)
                    char_nr=active_textfield.char_nr(cursor)
                    if (first_textfield-1)<idx<len(textfields)-7:
                        idx=idx+8
                        active_textfield=textfields[idx]
                        cursor = (active_textfield.startpos[0] + char_nr, active_textfield.startpos[1])
                    if idx>=first_textfield and activerow<len(raw_pattern_text):
                        activerow=activerow+1
                if event.key == pygame.K_RIGHT or req_next_char:
                    ret = active_textfield.next_editable(cursor)
                    if ret:
                        ncursor=ret
                        if textfields.index(active_textfield) > first_textfield:
                            if ncursor[1] > cursor[1]: activerow = activerow + 1
                        cursor=ncursor
                    else: req_next_field=True
                    pass
                if event.key == pygame.K_LEFT:
                    ret = active_textfield.prev_editable(cursor)
                    if ret:
                        ncursor=ret
                        ncursor=ret
                        if textfields.index(active_textfield) > first_textfield:
                            if ncursor[1] < cursor[1]: activerow = activerow - 1
                        cursor=ncursor
                    else: req_prev_field=True
                if event.key==pygame.K_TAB or req_next_field or req_prev_field:
                    idx = textfields.index(active_textfield)
                    if (pygame.key.get_mods() & pygame.KMOD_SHIFT) or req_prev_field:
                        tf_range=range(idx - 1, 0,-1)
                    else:
                        tf_range = range(idx + 1, len(textfields))
                    for idxn in tf_range :
                        textfield=textfields[idxn]
                        if not textfield.readonly:
                            active_textfield=textfields[idxn]
                            ncursor = active_textfield.startpos
                            if textfields.index(active_textfield)>first_textfield:
                                if ncursor[1] > cursor[1]: activerow = activerow + 1
                                if ncursor[1] < cursor[1]: activerow = activerow - 1
                            cursor=ncursor
                            if req_prev_field: cursor = active_textfield.endpos
                            break

        #Mouse event
        else:
            # Window Close Button
            if event.type == pygame.QUIT:
                tracker.abort_play()
                quit()

            # Click on window surface
            if event.type == pygame.MOUSEBUTTONDOWN and pause:
                x,y=pygame.mouse.get_pos()
                c = [x // 8,y // 8]
                for textfield in textfields:
                    if textfield.is_editable(c):
                        cursor=c
                        active_textfield=textfield

                if tf_load.is_selected(c):
                    tkroot.lift()
                    tkroot.focus_force()
                    fd_opts['title'] = 'Open Music Track File'
                    fd_opts['filetypes'] = [('Supported files', '*.mod;*.pyt'),('MOD files', '.mod'),('PYT files', '.pyt'), ('All files', '.*')]
                    fd_opts['initialdir']
                    file_path = filedialog.askopenfilename(**fd_opts)
                    if file_path:
                        tracker.load(file_path)
                        pass
                if tf_save.is_selected(c):
                    tkroot.lift()
                    tkroot.focus_force()
                    fd_opts['title'] = 'Save Music Track File'
                    fd_opts['filetypes'] = [('PYT files', '.pyt')]
                    file_path = filedialog.asksaveasfilename(**fd_opts)
                    if file_path:
                        tracker.songtitle=tf_songtitle.text
                        tracker.save(file_path)
                        messagebox.showinfo("Saved", "Track saved as "+file_path)
                if tf_new.is_selected(c):
                    tkroot.lift()
                    tkroot.focus_force()
                    fd_opts['title'] = 'Create Music Track File'
                    fd_opts['filetypes'] = [('PYT files', '.pyt')]
                    file_path = filedialog.asksaveasfilename(**fd_opts)
                    if file_path:
                        tracker.clear(file_path)

                if tf_samples.is_selected(c):
                    tkroot.lift()
                    tkroot.focus_force()
                    fd_opts['title'] = 'Load Sample'
                    fd_opts['filetypes'] = [('WAV files', '.wav')]
                    file_path = filedialog.askopenfilename(**fd_opts)
                    if file_path:
                        tracker.samples[samplenr] = tracker.wav2sample(file_path)
                        tf_samples.text = tracker.samples[samplenr]["name"]
                        edited = True

                if tf_prev.is_selected(c):
                    samplenr=(samplenr-1) % 16
                    tf_samplenr.text="{:02d}".format(samplenr)
                    tf_samples.text = tracker.samples[samplenr]["name"]
                if tf_next.is_selected(c):
                    samplenr=(samplenr+1) % 16
                    tf_samplenr.text="{:02d}".format(samplenr)
                    tf_samples.text = tracker.samples[samplenr]["name"]


            pass

