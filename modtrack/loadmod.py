
def nibbles(bt):
    h = bt >> 4
    l = bt & 0x0F
    return h,l

def nibbles2byte(low,high):
    return high*16+low

def nibbles2(bt_array):
    nibble_array=[]
    for bt in bt_array:
        h,l=nibbles(bt)
        nibble_array.append(h)
        nibble_array.append(l)
    return nibble_array
def hexs(bt_array):
    hexout=""
    for bt in bt_array:
        hexout=hexout+(hex(bt)[2:].zfill(2))
    return hexout.upper()

songtitle=""
format=""
samples=[]
patterns=[]
pattern_table=None
nr_playedpatterns=0

def amigaword_toint(b1,b2):
    return b2*256+b1

def read_module(filename):
    global songtitle,format,samples,patterns,pattern_table,nr_playedpatterns

    with open(filename, 'rb') as fh:
        f=fh.read()
        barr=bytearray(f)
    """
    #output file data
    line=""
    for byte in barr:
        line=line+"{:0<2}".format(hex(byte)[2:].upper())+" "
        if len(line)>45:
            print (line)
            line=""
    """

    #https://wiki.multimedia.cx/index.php/Protracker_Module
    #http://www.fileformat.info/format/mod/corion.htm
    #http://elektronika.kvalitne.cz/ATMEL/MODplayer3/doc/MOD-FORM.TXT
    #http://www.eblong.com/zarf/blorb/mod-spec.txt
    #http://web.archive.org/web/20120806024858/http://16-bits.org/mod/
    #ftp://ftp.modland.com/pub/documents/format_documentation/FireLight%20MOD%20Player%20Tutorial.txt
    if barr[0:4]=="PP20":
        #compressed with PowerPacker, we can't decode this
        return None

    d=False
    if d: print (barr[1080:1084])
    #If no letters in barr[1080:1084] then this is the start of the pattern data, and only 15 samples were present.
    try:
      format=barr[1080:1084].decode("utf-8")
    except UnicodeDecodeError:
      format="STK."
    if barr[1080:1084]==b'\x00\x00\x00\x00': format="STK."
    if not format.isprintable(): format="STK."

    nr_samples=31
    nr_channels=4
    compatible=False
    formdesc="Unknown format"

    if format=="STK.":
        formdesc="Ultimate Soundtracker (Original) 4 channel / 15 instruments"
        nr_samples=15
        compatible = True
    if format=="M.K.":  # Protracker 4 channel
        formdesc = "Protracker 4 channel / 31 instruments"
        compatible = True
        pass
    if format=="M!K!":  # Protracker 4 channel / >64 pattern
        formdesc = "Protracker 4 channel / 31 instruments / >64 patterns"
    if format=="FLT4":  # Startracker 4 channel
        formdesc = "Startracker 4 channel / 31 instruments"
        compatible = True
        pass
    if format=="FLT8":  # Startracker 8 channel
        formdesc = "Startracker 8 channel / 31 instruments"
    if format=="2CHN":  # Fasttracker 2 channel
        formdesc = "Fasttracker 2 channel / 31 instruments"
    if format=="4CHN":  # Fasttracker 4 channel
        formdesc = "Fasttracker 4 channel / 31 instruments"
        compatible = True
        pass
    if format=="6CHN":  # Fasttracker 6 channel
        formdesc = "Fasttracker 6 channel / 31 instruments"
    if format=="8CHN":  # Fasttracker 8 channel
        formdesc = "Fasttracker 8 channel / 31 instruments"
    if format=="CD81":  # Atari oktalyzer 8 channel
        formdesc = "Atari oktalyzer 8 channel / 31 instruments"
    if format=="OKTA":  # Atari oktalyzer 8 channel
        formdesc = "Atari oktalyzer 8 channel / 31 instruments"
    if format=="OCTA":  # Atari oktalyzer 8 channel
        formdesc = "Atari oktalyzer 8 channel / 31 instruments"
    if format=="16CN":  # Taketracker 16 channel
        formdesc = "Taketracker 16 channel / 31 instruments"
    if format=="32CN":  # Taketracker 32 channel
        formdesc = "Taketracker 32 channel / 31 instruments"

    if d: print (format,"format detected: "+formdesc)
    if not compatible:
        errmsg="Format "+format+" ("+formdesc+") is not supported!"
        raise ValueError(errmsg)

    songtitle=barr[0:20].decode("utf-8")

    if d: print (songtitle)
    offset=20
    if d: print ("nr_samples:",nr_samples)
    for sample in range (0,nr_samples):
        sample = {}
        sample["name"]=barr[offset:offset+22].decode("utf-8").replace('\x00', '')

        # sample len in words (1word=2bytes). 1st word overwritten by tracker
        sample["len"]=2*int.from_bytes(barr[offset+22:offset+24],byteorder="big",signed=False)
        sample["finetune"] = barr[offset + 24]#.decode("utf-8")
        sample["volume"] = barr[offset + 25]#.decode("utf-8")
        sample["repeat_from"] = 2* int.from_bytes(barr[offset + 26:offset + 28],byteorder="big",signed=False)
        sample["repeat_len"] = 2* int.from_bytes(barr[offset + 28:offset + 30],byteorder="big",signed=False)

        if d:
            print("-------------------")
            print("sample_name       : ",sample["name"])
            print("sample_len        : ",sample["len"])
            print("sample_finetune   : ",sample["finetune"])
            print("sample_volume     : ",sample["volume"])
            print("sample_repeat_from: ",sample["repeat_from"])
            print("sample_repeat_len : ",sample["repeat_len"])
        samples.append(sample)
        offset=offset+30

    if d: print ("offset:",offset)
    #offset=470 15 samples Ultimate Soundtracker, id at 600
    #offset=950 31 samples Protracker and similar, id at 1080
    nr_playedpatterns=barr[offset] # hex value was loaded as byte and is automatically converted to int
    offset=offset+1
    dummy127=barr[offset]
    offset=offset+1
    pattern_table=barr[offset:offset+128]
    offset=offset+128
    if d: print ("offset:",offset)
    if not format == "STK.":# Only other format then Ultimate Soundtracker have bytes to specify format
      dummyformat=barr[offset:offset+4].decode("utf-8")
      offset=offset+4
    if d: print ("nr patterns played: ",nr_playedpatterns)
    if d: print ("format            : |"+format+"|")

    #read nr patterns stored
    #equal to the highest patternnumber in the song position table(at offset 952 - 1079).
    nr_patterns_stored=0
    for chnr in range (0,128):
        if d: print ("pattern_table[chnr]:",chnr,pattern_table[chnr])
        if pattern_table[chnr]!=0: #check for first not possible because 0 is also a valid pattern number
            nr_patternsplayed=chnr+1
        if (pattern_table[chnr]+1)>nr_patterns_stored:
            nr_patterns_stored=(pattern_table[chnr]+1)

    pattern_table=pattern_table[:nr_playedpatterns]
    if d: print ("nr patterns stored: ",nr_patterns_stored)

    notelist = ["C-", "C#", "D-", "D#", "E-", "F-", "F#", "G-", "G#", "A-", "A#", "B-"]
    periods=[1712,1616,1525,1440,1357,1281,1209,1141,1077,1017, 961, 907,
             856, 808, 762, 720, 678, 640, 604, 570, 538, 508, 480, 453,
             428, 404, 381, 360, 339, 320, 302, 285, 269, 254, 240, 226,
             214, 202, 190, 180, 170, 160, 151, 143, 135, 127, 120, 113,
             107, 101,  95,  90,  85,  80,  76,  71,  67,  64,  60,  57,
    ]
    def period2note(period):
        notenr=-1
        for nr,val in enumerate(periods):
            if val==period:
                notenr=nr % 12
                oct=nr//12
        if notenr>=0:
            note=notelist[notenr]+str(oct)
        else:
            note="---"
        return note

    if d: print("---patterns---")
    patterns = []
    for pattern in range (0,nr_patterns_stored):
        pattern=[]
        if d: print (len(patterns),": offset ",offset)
        for row in range (0,64):
            row=[]
            txt=""
            txt2= ""
            for channel in range (0,nr_channels):
              bytes=barr[offset:offset+4]
              nibbles=hexs(bytes)
              samplenr=int(nibbles[0]+nibbles[4],16)
              samplehex=nibbles[0]+nibbles[4]

              noteperiod=int(nibbles[1:4],16)

              effect = nibbles[5:8]
              txt2=txt2+"{} -> {} {} {} | ".format(nibbles,noteperiod,samplehex,effect)
              note=period2note(noteperiod)
              seq_text="{:<3} {} {:<3}".format(note,samplehex,effect)
              row.append(seq_text)
              #txt = txt + seq_text+ " "
              txt=txt+"|"+nibbles+"|"+str(noteperiod)
              offset=offset+4
            #print (txt2)
            if d: print (row,txt)
            pattern.append(row)
        patterns.append(pattern)

    if d: print ("---samples---")
    #samples are @ 8287Hz
    if d: print ("total: ",len(samples))
    for i, sample in enumerate(samples):
        sample_len=sample["len"]
        #first two bytes  always two zeros, and used for repeating is the sample is to be terminated.
        sample_data=barr[offset+2:offset+sample_len]
        sample["data"] = sample_data
        if d: print(i, "data offset: ", offset, "len: ", sample_len, sample_data)
        filename="ProTracker-win32/modules/t"+str(i)+".wav"
        #with open(filename, 'wb') as fh:
        #    fh.write(sample_data)
        offset=offset+sample_len

    if d: print ("--- check ---")
    if d: print ("File length: ", len(barr))
    if d: print ("Offset     : ", offset)
    if offset!=len(barr):
        print ("ERROR....NOT ALL BYTES PROCESSED! ", len(barr)-offset, "remain.")

    return True