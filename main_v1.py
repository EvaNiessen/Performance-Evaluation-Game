#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.85.3),
    on Do 30 Aug 2018 10:16:54 CEST
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from gui_v1 import Gui
import random, configparser, cv2, time

ID = 'Demo'
max = 0

def generate_block(block_length, congruent_quantity):
    '''Preset which rules and which pictures are shown during a block'''
    block = []
    congruent = random.sample(range(block_length),congruent_quantity) #Zieht die Stellen des Blockes an welchem die congruent rule verwendet wird
    pool = range(block_length)
    picture = [[],[],[],[]]
    for i in range(4):                                                #Fuer jedes Bild
        for j in range((block_length/4)+1):                           #Wird (Blocklaenge/4) mal
            if (4*(j+1)) <= block_length or i<block_length % 4:       #Wenn noch "Positionen uebrig" sind
                picture[i].append(random.choice(pool))                #Zufaellig eine Position gezogen
                pool.remove(picture[i][j])
    for i in range(block_length):                                     #Fuer jede Stelle des Blockes wird
        next_trial = []                                               #Wird nun ein Wertepaar erzeug
        if i in congruent:                                            #Fuer den ersten Wert wird nur geprueft ob die Stelle als congruent gezogen wird
            next_trial.append(1)
        else :
            next_trial.append(2)
        if i in picture[0]:                                           #Fuer den zwei6ten Wert wird geprueft zu welchem Bild die Stelle des Blockes gehoert
            next_trial.append(0)
        elif i in picture[1]:
            next_trial.append(1)
        elif i in picture[2]:
            next_trial.append(2)
        elif i in picture[3]:
            next_trial.append(3)
        block.append(next_trial)
    return block


def introduction(gui, configs):
    '''first practise without timelimit and feedback, no info in logfile'''
    pool = [0,0,1,1,2,2,3,3]
    block_procedure = generate_block(int(configs['Block']['tryout_length']), int(configs['Block']['congruent_number']))
    for j in range(int(configs['Block']['tryout_length'])):
        gui.show_pictures(block_procedure[j])
        guessed_number=gui.which_button('inf')
        choosen = guessed_number[0]
        evaluation = gui.show_right(choosen)
        

def tryout(gui, configs):
    '''second practise identical with real experiment, but without timeout adjustment, no info in logfile'''
    pool = [0,0,1,1,2,2,3,3]
    block_procedure = generate_block(int(configs['Block']['tryout_length']), int(configs['Block']['congruent_number']))
    for j in range(int(configs['Block']['tryout_length'])):
        gui.show_pictures(block_procedure[j])
        guessed_number=gui.which_button(float(configs['General']['timeout']))
        choosen = guessed_number[0]
        if guessed_number[0] == -1:
            if not pool:
                pool = [0,0,1,1,2,2,3,3]
            choosen = random.choice(pool)
            pool.remove(choosen)
            gui.show_timeout()
        evaluation = gui.show_intertrial(choosen)


def real_game(gui, configs):
    global max
    timeout = float(configs['General']['timeout'])
    starttime = time.time()
    logfile = open("logfile_{0}.txt".format(ID), 'w')
    logfile2 = open("logfile2_{0}.txt".format(ID), 'w')
    logheader = "block \t trial_nr \t trial_type \t RT \t miss \t ".expandtabs(2) + \
                "chosen_button \t correct_button \t evaluation \t".expandtabs(2) + \
                "accuracy \t RT_eval \t category_left \t".expandtabs(2) + \
                "color_left \t category_right \t color_right \r\n".expandtabs(2)
    logfile.write(logheader)
    for i in range(int(configs['General']['block_number'])):
        pool = [0,0,1,1,2,2,3,3]                                #Ist der Imagepool fuer CPU-Auswahl bei Timeout am anfang jedes Blockes aufgefuellt
        block_procedure = generate_block(int(configs['Block']['main_length']), int(configs['Block']['congruent_number_main']))
        gui.show_begin_of_block(int(configs['Block']['pause']), max, int(configs['General']['block_number']) - i)
        guessed_right = 0
        for j in range(int(configs['Block']['main_length'])):
            gui.show_pictures(block_procedure[j])
            guessed_number=gui.which_button(timeout)
            choosen = guessed_number[0]
            if guessed_number[0] == gui.pictures.position:      #Wenn das geratene Bild richtig war
                gui.score += 10                                 #Erhoehe Score um 10
                guessed_right += 1                              #Und zaehle die richtigen Bilder hoch
            if guessed_number[1] == -1:                         #Sollte kein Bild gewaehlt worden sein wird eins aus dem imagepool gezogen
                if not pool:                                    #Sollte der Pool leer sein wird dieser neu aufgefuellt
                    pool = [0,0,1,1,2,2,3,3]
                choosen = random.choice(pool)
                pool.remove(choosen)
                gui.show_timeout()
            evaluation = gui.show_intertrial(choosen)
            eval_button = evaluation[0] #Auswahl der Evaluation
            eval_time = evaluation[1] #RT der Evaluation

            if((evaluation[0] < 2 and choosen == block_procedure[j][1]) or (evaluation[0] > 2 and choosen != block_procedure[j][1])): #Wenn die Selsteinschaetzung richtig
                    gui.score += 3                                                                                              #erhoehe Score um 3
            if guessed_number[1] > -1: #Info fuer logfile wenn Antwort gegeben wurde
                logtext = "{0} \t \t {1} \t \t \t {2} \t \t \t   {3:04.0f}  0 \t \t ".format(
                i+1,j+1,block_procedure[j][0],guessed_number[1]).expandtabs(4) + \
                "{0} \t \t \t \t {1} \t \t \t \t   {2} \t \t \t{3} \t \t   ".format(
                guessed_number[0]+1, gui.pictures.position+1, 4-eval_button, int(guessed_number[0]==gui.pictures.position)
                ).expandtabs(4) + \
                "{0:04.0f} \t  {1} \t \t \t {2} \t \t \t  {3} \t \t \t \t{4} \r\n".format(
                 eval_time, gui.pictures.last_shown_images[0][0]+1, gui.pictures.last_shown_images[0][1]+1,
                 gui.pictures.last_shown_images[1][0]+1, gui.pictures.last_shown_images[1][1]+1 ).expandtabs(4)
                logfile.write(logtext)
            else: #Info fuer logfile bei timeout
                logtext = "{0} \t \t {1} \t \t \t {2} \t \t \t   0 \t 1 \t \t ".format(
                            i+1,j+1,block_procedure[j][0]).expandtabs(4) + \
                            "{0} \t \t \t \t {1} \t \t \t \t   {2} \t \t \t3 \t \t   ".format(
                            choosen+1,gui.pictures.position+1,4-eval_button, eval_time).expandtabs(4) + \
                            "{0:04.0f} \t  {1} \t \t \t {2} \t \t \t  {3} \t \t \t \t{4} \r\n".format(
                             eval_time, gui.pictures.last_shown_images[0][0]+1, gui.pictures.last_shown_images[0][1]+1,
                             gui.pictures.last_shown_images[1][0]+1, gui.pictures.last_shown_images[1][1]+1 ).expandtabs(4)
                logfile.write(logtext)
            if not ((j+1)%(int(configs['Block']['main_length'])/2)): #Wenn die Haelfte eines Blockes erreicht ist
                if (2*guessed_right/float(configs['Block']['main_length']) < float(configs['Block']['increase_timeout'])): #Und die richtige anzahl kleiner der vorgegebenen Prozentzahl ist
                    timeout *= 1.1                                                                                    #Erhoehe timeout um 10%
                elif(2*guessed_right/float(configs['Block']['main_length']) > float(configs['Block']['decrease_timeout'])): #Und die richtige anzahl kleiner der vorgegebenen Prozentzahl ist
                    timeout *= 0.9                                                                                     #Verringere timeout um 10%
                guessed_right = 0
        max += 13*int(configs['Block']['main_length']) #Pro Versuch koennen zehn Punkte durch Bilder und drei durch Bewertung erreicht werden
        logfile2.write("Time for block{0}: {1} \r\n".format(i+1, round(time.time()-starttime,3)))
        logfile2.write("Current timeout: {0} \r\n".format(timeout))
    logfile2.write("\r\n \r\n \r\n \r\n")
    logfile2.write("Score: {0}\n".format(gui.score))
    logfile2.write("Color Schema: {0}\n".format(int(configs['General']['color_scheme'])))
    logfile2.write("trial: \t 1) congruent rule \t 2) incongruent rule \r\n")
    logfile2.write("evaluation: \t 1) probably not \t 2) maybe not \t 3) maybe yes \t 4) probably yes 5) no evaluation \r\n")
    logfile2.write("miss: \t 0) no miss \t 1) timeout ")
    logfile.close()
    logfile2.close()

def main():
    rules =  configparser.ConfigParser()
    configs = configparser.ConfigParser()
    rules.read('rules.cfg')
    configs.read('settings.cfg')
    gui = Gui(  str(configs['General']['input_keys']).replace(" ","").split(','),
                int(configs['General']['highscore']),
                int(configs['General']['picture_size']),
                float(configs['General']['evaluation_time']),
                int(configs['General']['color_scheme']))
    gui.show_rules()
    while gui.show_introduction():
        introduction(gui, configs)
    while gui.show_tryout():
        tryout(gui, configs)
    real_game(gui, configs)

    gui.show_end_of_game(max)


if __name__=="__main__":
    main()
    