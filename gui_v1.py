#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import rules_v1
from bildgenerator_v1 import Bildgenerator
from psychopy import locale_setup, sound, gui, visual,event , core, data, logging, hardware, parallel, iohub
import time
import pyglet
import sys
from random import randint

class Gui:
    
    '''Provides an userinterface and analyzes the userinputs'''
    def __init__(self, input_keys, highscore,picture_size, evaluation_time, color_scheme):
        self.evaluation_time = evaluation_time
        self.picture_size = picture_size
        self.keys = input_keys
        self.win = visual.Window(
            fullscr=True, screen=2,
            allowGUI=True, allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            blendMode='avg', useFBO=True)
        self.win.color = [-1,-1,-1]
        self.win.mouseVisible=False
        self.win.flip()
        
        self.score = 0 #zu Beginn 0 Punkte
        self.highscore_anzeige = visual.TextStim(win = self.win, units='pix', pos=(0,2.5*self.picture_size), text = "Highscore: "+str(highscore), height = self.picture_size/4)
        self.blocksleft = visual.TextStim(win = self.win, units='pix', pos=(0,1.5*self.picture_size), height = self.picture_size/4)
        self.score_anzeige = visual.TextStim(win=self.win, units='pix', pos=(0,2.0*self.picture_size), height = self.picture_size/4)

        
        self.pictures = Bildgenerator(color_scheme)
        self.mouse=event.Mouse(win=self.win)
        self.image = []
        self.image1 = visual.ImageStim(win=self.win, units='pix', pos=(0,self.picture_size), size=(self.picture_size*4,self.picture_size*2))
        #Dient für das zeichnen der Zielbilder
        self.shapes = []
        self.text = visual.TextStim(win = self.win, units='pix', pos=(0,self.picture_size), height = self.picture_size/3)
        self.text.wrapWidth = self.win.size[0]
        #Dient für anzeigen von Texten wie z.B. "End of Game"
        self.texts = []
        self.create_textshapes_and_pictures()
        
    def create_textshapes_and_pictures(self):
        '''Creates the textshape for highscore screen and the pictures which could be selected'''
        for i in range(0,4):
            self.shapes.append(visual.ShapeStim(win = self.win ,units = 'pix',
                                                vertices = ((-self.picture_size/2,self.picture_size/2),(-self.picture_size/2,-self.picture_size/2),
                                                (self.picture_size/2,-self.picture_size/2),(self.picture_size/2,self.picture_size/2)),
                                                fillColor = [1,1,1], lineColor = [-1,1,-1]))
            self.shapes[i].pos = (self.picture_size*(1.2*i-1.8),-self.picture_size)
            #Generiert  vier gruene Vierecke mit der selben Position und Groesse wie die Auswahlbilder
            self.texts.append(visual.TextStim(win = self.win,units = 'pix',pos=(self.picture_size*(1.2*i-1.8),-self.picture_size), color = [-1,-1,-1]))
            #Generiert vier Textfelder mit der selben Position wie die Auswahlbilder
            self.texts[i].height = self.picture_size/5
            self.texts[i].wrapWidth = self.picture_size/2
            #Passt die Schriftgroesse an die groesse aus dem configfile an
            self.image.append(visual.ImageStim(win=self.win, units = 'pix', pos=(self.picture_size*(1.2*i-1.8),-self.picture_size), size=(self.picture_size,self.picture_size)))
            self.image[i].setImage("Bilder/tmp/option"+str(i)+".jpg")
            #Legt die Auswahlbilder fest
        self.texts[0].text = "Ja"
        self.texts[1].text = "Vielleicht ja"
        self.texts[2].text = "Vielleicht nicht"
        self.texts[3].text = "Nein"
        
    def show_pictures(self, trial):
        aim_vertices =self.picture_size/10
        aim = visual.ShapeStim(win = self.win ,units = 'pix',
                               vertices = ((-aim_vertices,aim_vertices),(-aim_vertices,-aim_vertices),
                               (aim_vertices,-aim_vertices),(aim_vertices,aim_vertices)),pos=(0,self.picture_size))
        aim.draw()  #Zeichnet ein viereck an die Stelle der Bilder
        for i in range(4):
            self.image[i].opacity = 1
            self.image[i].draw()
        self.win.flip()
        waittime = randint(6,10)
        time.sleep(waittime/10.0)   #Zeige das viereck für 0.6 bis 1 Sekunde
        self.pictures.set_target(trial[0], trial[1])
        self.image1.setImage("Bilder/tmp/target.jpg")
        self.image1.draw()
        for i in range(0,4):
            self.image[i].opacity = 1
            self.image[i].draw()
        self.win.flip()
        
    def show_right(self, choosen):
        '''Shows the correct and the chosen picture for introduction Block; after this the self-evaluation screen is shown'''
        for i in range(4):
            if i == self.pictures.position:
                self.shapes[i].lineColor = (-1,1,-1)        #Umrandet das richtige Bild mit einem gruenen Kasten
                self.shapes[i].lineWidth = 5
                self.shapes[i].draw()
            elif i==choosen:
                self.shapes[i].lineColor = (1,-1,-1)        #Umrandet das gewaehlte Bild mit einem roten Kasten
                self.shapes[i].lineWidth = 5
                self.shapes[i].draw()
            else:
                self.image[i].opacity = 0.5                 #Alle anderen Bilder werden ausgeblasst
            self.image[i].draw()
        self.image1.draw()
        self.win.flip()
        event.waitKeys(keyList = self.keys)
            
    
    def show_intertrial(self, choosen):
        '''Returns the button which is pressed in the self-evaluation screen, returns -1 if no key is pressed'''
        for i in range(4):
            if i==choosen:
                self.shapes[i].lineColor = (0.1,0.9,1)        #Umrandet das gewaehlte Bild mit einem tuerkis blauen Kasten
                self.shapes[i].lineWidth = 5
                self.shapes[i].draw()
            else:
                self.image[i].opacity = 0.3                 #Alle anderen Bilder werden ausgeblasst
            self.image[i].draw()
        self.win.flip()
        time.sleep(0.7)
        self.win.flip()
        time.sleep(1)
        self.text.setText("War das gewaehlte Bild richtig?")
        self.text.color = [1,1,1]
        self.text.draw()
        for i in range(0,4):
            self.shapes[i].lineColor = (0.1,0.9,1) 
            self.shapes[i].lineWidth = 3
            self.shapes[i].draw()
            self.texts[i].draw()
        self.win.flip()
        key_input = []
        event.getKeys()                                         #Leert den Eingabebuffer
        starttime2 = time.time()
        key_input = event.waitKeys(maxWait = self.evaluation_time, keyList = self.keys)
        if key_input:
            return (self.keys.index(key_input[0]),round((time.time()-starttime2)*1000, 5))
        return (-1, 0)                                               #Returnt -1 falls keine Eingabe stattfindet


    def show_timeout(self):
        self.text.setText("TIMEOUT!")
        self.text.color = [1,-1,-1]
        self.text.draw()
        
        
    def show_introduction(self):
        '''Asks whether another introduction block should be started'''
        self.text.setText("Erneuter Durchgang der Einleitung?")
        self.text.draw()
        self.texts[1].text = "Ja" # Setzt den Text zweier Evaluationsbuttons auf 'Ja' und 'Nein'
        self.texts[2].text = "Nein"  
        for i in range(1,3):
            self.shapes[i].lineColor = (0.1,0.9,1) 
            self.shapes[i].lineWidth = 3
            self.shapes[i].draw()
            self.texts[i].draw()
        self.win.flip()
        key_input = event.waitKeys(keyList = ['y', 'n'])
        self.texts[1].text = "Vielleicht ja" #Setzt den Text zurück auf die Evaluationstexte
        self.texts[2].text = "Vielleicht nicht"
        return key_input[0] == 'y'
        
    def show_tryout(self):
        '''Asks whether another tryout block should be started'''
        self.text.setText("Erneuter Durchgang des Trainings?")
        self.text.draw()
        self.texts[1].text = "Ja" # Setzt den Text zweier Evaluationsbuttons auf 'Ja' und 'Nein'
        self.texts[2].text = "Nein"         
        for i in range(1,3):
            self.shapes[i].lineColor = (0.1,0.9,1) 
            self.shapes[i].lineWidth = 3
            self.shapes[i].draw()
            self.texts[i].draw()
        self.win.flip()
        key_input = event.waitKeys(keyList = ['y', 'n'])
        self.texts[1].text = "Vielleicht ja" #Setzt den Text zurück auf die Evaluationstexte
        self.texts[2].text = "Vielleicht nicht"
        return key_input[0] == 'y'
        
        
    def show_end_of_game(self, max):
        '''Shows the score and the highscore at the end of game'''
        self.score_anzeige.setText("Score: "+str(self.score)+ " / "+str(max))
        self.text.setText("Ende des Spiels")
        self.text.draw()
        self.score_anzeige.draw()
        self.highscore_anzeige.draw()
        self.win.flip()
        event.waitKeys(keyList = self.keys)
        

    def show_begin_of_block(self, pause, max, counter):
        ''' Shows the  highscore, own score and the maximum possible score at the beginning of each block, 
        pause is the minimum time a participant has to wait before they can start the next block'''
        for i in range(pause):
            self.score_anzeige.setText("Score: "+str(self.score)+ " / "+str(max))
            self.score_anzeige.draw()
            self.blocksleft.setText("Verbleibende Durchgaenge: "+str(counter))
            self.blocksleft.draw()
            self.highscore_anzeige.draw()
            self.text.setText("Weiter in:"+str(pause-i)+" Sekunden")
            self.text.draw()
            self.win.flip()
            time.sleep(1)
        self.score_anzeige.setText("Score: "+str(self.score)+ " / "+str(max))
        self.score_anzeige.draw()
        self.blocksleft.setText("Verbleibende Durchgaenge: "+str(counter))
        self.blocksleft.draw()
        self.highscore_anzeige.draw()
        self.text.setText("Druecken Sie eine Taste um weiter zu machen")
        self.text.draw()
        self.win.flip()
        event.waitKeys(keyList = self.keys)
        aim_vertices =  self.picture_size/10
        aim = visual.ShapeStim(win = self.win ,units = 'pix',
                               vertices = ((-aim_vertices,aim_vertices),(-aim_vertices,-aim_vertices),
                               (aim_vertices,-aim_vertices),(aim_vertices,aim_vertices)),pos=(0,self.picture_size))
        aim.draw()                          #Zeichnet ein kleines Viereck an die Stelle des Bilder
        self.win.flip()
        time.sleep(1)

    
    def which_button(self, stoptime):
        '''Returns the button which is pressed while Gamescreen'''
        event.getKeys()         #Leert den Eingabebuffer
        starttime = time.time()
        key_input = event.waitKeys(maxWait = stoptime, keyList = self.keys)
        if key_input:
            return (self.keys.index(key_input[0]),round((time.time()-starttime)*1000, 5))   #returnt (Den eingebenen Button, Die benötigte Zeit)
        return (-1, -1)  #Sollte keine Eingabe erfolgen wird fuer Zeit und Button -1 zurueck gegeben
        
    def show_rules(self):
        ''' Shows an introduction to the rules and the experiment'''
        text_display = visual.TextStim(self.win, units = 'pix', pos = (0, -1.5*self.picture_size), height = self.picture_size/5)
        image_display = visual.ImageStim(self.win, units = 'pix', pos=(0, 1.5*self.picture_size),
                                size = (self.picture_size*6, self.picture_size*3.5))
        #Erzeugen von Text und Bildfeld zum anzeigen der Einfuehrung
        while rules_v1.content:
            text_display.setText(rules_v1.content[0][0])   #Setzt den Text auf den als erstes im Tupel angegebenen String
            image_display.setImage(rules_v1.content[0][1]) #Setzt das Bild auf die als zweites im Tupel angegebene Quellldatei
            del rules_v1.content[0]
            text_display.draw()
            image_display.draw()
            self.win.flip()
            event.waitKeys(keyList = self.keys)
            
