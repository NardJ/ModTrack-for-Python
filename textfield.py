import pygame

class Textfield:
    allowed_ascii = list(range(ord('A'), ord('Z')+1)) + \
                    list(range(ord('a'), ord('z')+1)) + \
                    list(range(ord('0'), ord('9') + 1)) + \
                    [ord('#')]

    def __init__(self,pos,text,uneditable=[],length=None,allowed=None):
        if length == None: length = len(text)
        text=text.replace('\x00','').upper()
        #pad spaced to text to match length (if given)
        self.text=("{:<" + str(length) + "}").format(text)
        self.color=(255,0,255)
        self.startpos=pos
        self.endpos=(pos[0]+length-1,pos[1])
        self.border=None
        if uneditable==True:
                uneditable=[i for i in range(len(text))]
                self.readonly=True
        else:
            self.readonly=False
        self.uneditable=uneditable
        #make allowed chars
        if allowed==None:
            self.allowed_chars=[self.allowed_ascii]*length
        else:
            self.allowed_chars=[]
            for all in allowed:
                all_arr=[ord(c) for c in all]
                self.allowed_chars.append(all_arr)

    def is_selected(self,mpos):
        if not mpos[1] == self.startpos[1]: return False
        if mpos[0] < self.startpos[0] or mpos[0] > self.endpos[0]: return False
        return True

    def is_editable(self,mpos):
        if not mpos[1] == self.startpos[1]: return False
        if mpos[0] < self.startpos[0] or mpos[0] > self.endpos[0]: return False
        charpos = mpos[0] - self.startpos[0]
        if charpos in self.uneditable: return False
        #print ("Textfield:",self.text)
        #print("  charpos:", charpos)
        return True

    def next_editable(self, mpos):
        if self.is_editable(mpos):
            charpos = mpos[0] - self.startpos[0]
            for cp in range(charpos+1,len(self.text)):
                if cp not in self.uneditable: return (self.startpos[0]+cp,mpos[1])
        return False

    def prev_editable(self, mpos):
        if self.is_editable(mpos):
            charpos = mpos[0] - self.startpos[0]
            for cp in range(charpos-1,-1,-1):
                if cp not in self.uneditable: return (self.startpos[0]+cp,mpos[1])
        return False

    def char_nr(self,mpos):
        return (mpos[0] - self.startpos[0])

    def edit(self,char,mpos):
        if self.is_editable(mpos):
            charpos=mpos[0]-self.startpos[0]
            if char not in self.allowed_chars[charpos]: return False
            chars=list(self.text)
            if charpos<len(chars):
              chars[charpos]=chr(char).upper()
            self.text="".join(chars)
            return True
        return False

    def draw(self,myfont,screen,charsize=(8,8)):
        rtext = myfont.render(self.text, False, self.color)
        rpos=self.startpos[0]*charsize[0],self.startpos[1]*charsize[1]
        bpos = self.startpos[0] * charsize[0]-1, self.startpos[1] * charsize[1]-2
        bsize = (len(self.text)*charsize[0]+2,charsize[1]+3)
        screen.blit(rtext,rpos)
        if self.border:
            pygame.draw.rect(screen, self.border, pygame.Rect(bpos,bsize),1)
        return
