# ModTrack for Python
Player of mod files and inline track-data (old Amiga music format) coded in Python.


## What is does:
ModTracker is a player of mod tracks (old Amiga music format) loaded from disk or 
inline mod-data. You can load instruments/samples from disk or synthesize them in code.  
 
Modtracker for Python is based on ProTracker:
  - All basic effect except E-effects are implemented. (Effect B never found and not tested!)
  - Read and play 4-channel mod files in the Ultimate Soundtracker or Protracker format.
  - Load and save in native format (see next bullets for differences)
  - Specify track-info inline as a array (python list) 
  - Load samples (sounds) from wav files (unsigned 8 bit int, signed 32 bit float, signed 16 bit int, signed 32 bit int)
  - Specify samples as a waveform-array (python list)
  - Modtracker does not have a position table to specify a sequence of patterns to play. You can simulate this in your own python code.    

## How it works:
Python is not fast enough to synthesize sounds on-the-fly (not using external libraries in e.g. C). 
So Modtracker identifies and synthesizes all unique sounds beforehand and stores this in a library/dictionary.
For each channel a playlist of references to these sounds is build. This minimizes the needed memory.   
Python uses pygame to play the sounds and numpy to synthesize the sounds with the effects. 


## How to use it:
The basic framework is:
  1) Import modtrack              - from modtrack import tracker
  2) Init modtrack                - tracker.init
  3) Load or specify your song    - tracker.load / tracker.load_amigamodule / song array=[[--- --- 00 000 000],[--- --- 00 000 000]] 
  4) load samples (optionally)    - wav2sample / tracker.custom_waveform   
  5) Synthesize the song          - tracker.make_pattern
  6) Play the song                - tracker.play_pattern

A song array (python list) consists of: 
  - rows to be played one after another,
  - and each row consists of 4 channels,
  - each channel has a sequence either in amiga format or in (expanded) native format
  - each channel has a sequence consisting of note1, (note2), sample number, effect1 (effect2)
    ```python
    amiga_song= [
                  ["C-3 04 000", "--- 00 000", "--- 00 000", "--- 00 000"],
                  ["--- 00 000", "--- 00 000", "--- 00 000", "--- 00 000"],
                ]
                
    native_song=[
                  ["C-3 --- 04 000 000", "--- --- 00 000 000", "--- --- 00 000 000", "--- --- 00 000 000"],
                  ["--- --- 00 000 000", "--- --- 00 000 000", "--- --- 00 000 000", "--- --- 00 000 000"]
                  ["D-3 --- 04 000 000", "--- --- 00 000 000", "--- --- 00 000 000", "--- --- 00 000 000"]
                ]
    ```
  - A note is 3 positions long, starting with 'A'-'G', followed by - or # and last the octave number
  - Sample numbers are 2 positions long, in hex and start at 01
  - Effects are 3 positions long, start with effect number 'A'-'F', followed by the effect value (2 positions) in hex
  - A note(group) starts if note1 is not --- and ends on the next row where note2 is not ---
  - Instrument is only needed in first row of note-group.
  - If the first row of the group has note1 and note2 specified, they are both played and all effects are applied to both of them.
  - If a consequetive row has note2 (but not note1 off course), this note2 is not played but interpreted as an argument of the effect on that row.
  - Effects don't have to span the entire group and effect1 and effect2 can start/stop at different rows within the group.
    
Samples (instruments) can be internal, wav files or custom waveforms:
  - Default samples/instruments are:
      1: tri, 2: saw, 3: pulse, 4:sin, 5:whitenoise
  - If you load a sample from disk, this sample should have a frequency of C-3 (261Hz) 
  - A custom sample from a waveform shape is made with a two dimensional array:
    ```python
    triangle_waveform = ["  /\  ",
                         " /  \ ",
                         "/    \"]
    ```
    You can use every character you like to specify it. Don't put multiple characters in the same column.

## All user-commands:
```python
    init (volume, resolution, flags) - init pygame engine and window at desired resolution/flags and sets master volume
    songtitle                        - title of song

    clear (pytfilename)              - start new song, clear samples, pattern and sets filename for song
    load (pytfilename) 		            - load song in native Modtrack format 
    save (pytfilename) 		            - save song in native Modtrack format 
    load_amigamodule	(modfile)       - load song in Ultimate Soundtracker and ProTracker format	
    wav2sample (filename,volume,samplenr=-1) 
                                     - loads wav file, and amplifies to required volume and returns a sample (optionally set at samplenr)
    custom_waveform (usr_waveform_array, volume, samplenr, name) 
                                     - converts a wavefrom array and returns a sample (optionally set at samplenr)
    
    octave_transpose                 - must be set before make-pattern (will effect song-array as well as mod files)
    master_volume                    - must be set before make-pattern, can also be set from init()
    make_pattern (legacy,pattern_text) - converts pattern array into sound, legacy should be set to False if pattern_text is in native format ("C-2 D-2 01 C40 000")
    
    get_play_pos()                   - returns playing position in msecs
    get_play_row()                   - converts msecs in row nr in pattern
    
    abort_play                       - stops play at next row
    pause_play                       - pause play at next row
    resume_play                      - resume play from paused row
    play_pattern(soundrefs,from_time)- play_pattern (soundrefs is optionally) from given time (optionally)
```

## Effect commands
In a song array the following effects can be used: 
```
    0 - Normal play or Arpeggio             0xy : x-first halfnote add, y-second
    1 - Slide Up                            1xx : upspeed
    2 - Slide Down                          2xx : downspeed
    3 - Tone Portamento                     3xx : up/down speed
    4 - Vibrato                             4xy : x-speed,   y-depth
    5 - Tone Portamento + Volume Slide      5xy : x-upspeed, y-downspeed
    6 - Vibrato + Volume Slide              6xy : x-upspeed, y-downspeed
    7 - Tremolo                             7xy : x-speed,   y-depth
    9 - Set SampleOffset                    9xx : offset (23 -> 2300)
    A - VolumeSlide                         Axy : x-upspeed, y-downspeed
    B - Position Jump                       Bxx : go to start of pattern at position xx in position list
    C - Set Volume                          Cxx : volume, 00-40
    D - Pattern Break                       Dxx : go to row xx of next pattern in position list
    B+D - on same row                       Bxx Dyy: go to row yy of pattern at pos xx in pos list
    F - Set Speed                           Fxx : speed (00-1F) / tempo (20-FF)
    
    NOT IMPLEMENTED:
    E9      - Retrig Note                   E9x : retrig from note + x vblanks
    E00/1   - filter on/off
    E1x/2x  - FineSlide Up/Down 
    E30/1   - tonep ctrl off/on
    E40/1/2 - Vib Waveform sine/rampdown/square
    E5x     - set loop point
    E6x     - jump to loop+play x times
    E70/1/2 - Tremolo Waveform
    EAx/EBx - Fine volslide up/down
    ECx/EDx - notecut after x vblanks/notedelay by x vblanks
    EEx/EFx - PatternDelay by x notes/Invert loop, x=speed
```
### Remarks (native format):
  - B and D are not necessary in native format. In ModTrack you can (should) just make one complete pattern.  
  - In native track format (two effects per sequence) the effect commands 5,6 are not necessary since they are combinations of other effects:
         <br>5 -> 3, A 
         <br>6 -> 4, A
  - Amiga files use patterns of 64 rows and the F00 command is used to stop the song before a 64-row block
    In ModTrack a song can be of any number of rows, so to stop the song just don't add any rows after the last note.      

  Internally patterns in amiga format will be rewritten to native format:
  Example of second note as chord (C-3 E-3) and effect parameter (D-3)
  ```        
            C-3 E-3 00 102 000
            --- --- 00 102 A02
            --- D-3 00 302 A02
            --- --- 00 302 A02
  ```        
            
  Compact sequences like in Protracker are expanded as follows:
  ```
            ProTracker  ->  ModTrack
            C-3 00 000      C-3 --- 00 000 000
            E-3 00 302      --- E-3 00 302 000
            ...
            C-3 00 000      C-3 --- 00 000 000
            E-3 00 302      --- E-3 00 302 000
            --- 00 513      --- --- 00 302 A13
   ```
            
   The effectcombo's 5 and 6 are rewritten to seperate effects:
   ```
            ProTracker  ->  ModTracker
            C-3 01 000      C-3 --- --- 01 000 000
            G-3 01 343      --- G-3 --- 01 343 000
            --- 01 502      --- --- --- 01 343 A02
            
            C-3 01 000      C-3 --- --- 01 000 000
            G-3 01 443      --- G-3 --- 01 443 000
            --- 01 502      --- --- --- 01 443 A02
   ```
