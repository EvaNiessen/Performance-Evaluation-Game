#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from psychopy import visual
import imutils
import numpy as np
from random import randint, choice
import cv2 as cv
import time
import os

class Bildgenerator:
    
    def __init__(self, color_scheme):
        if color_scheme == 1:                           #Setzt die decode_tabelle der Farbcodes:
            self.color_decode = [0,1,2,3]               #Die 1. Zahl im Array gibt die Position des blauen Bildes an
        elif color_scheme == 2:                         #Die 2. Zahl im Array gibt die Position des gruenen Bildes an
            self.color_decode = [3,2,1,0]               #Die 3. Zahl im Array gibt die Position des roten Bildes an
        elif color_scheme == 3:                         #Die 4. Zahl im Array gibt die Position des gelben Bildes an
            self.color_decode = [2,0,3,1]
        elif color_scheme == 4:
            self.color_decode = [1,3,0,2]
        self.last_shown_images = [[], []]               #Speichert die letzen beiden gezeigten Bilder in zwei Listen
                                                        #Dabei enthält eine Liste zwei Einträge: Einen Integer fuer Form und einen fuer Farbe
        self.position = 0
        self.image_pool = [[],[],[],[]]
        self.initialize_image_pool()
        self.set_option()
    
    def initialize_image_pool(self):
        image_pool =[[],[],[],[]]
        for i in range(0,4):
            for j in range(1,9):
                if i == 0:
                    self.image_pool[0].append("Ball"+str(j))
                elif i == 1:
                    self.image_pool[1].append("Eis"+str(j))
                elif i == 2:
                    self.image_pool[2].append("Stuhl"+str(j))
                elif i == 3:
                    self.image_pool[3].append("Vogel"+str(j))
        
    def set_option(self):
        '''Creates the answer option pictures and writes them to Bilder/tmp''' 
        for i in range(0,4):
            img = cv.imread("Bilder/"+self.image_pool[i][0]+".jpg",cv.IMREAD_COLOR)
            img = self.colorize_img(img, i)
            reduction = 10
            img = img.astype(np.float32)
            img = cv.resize(img, (190,190), interpolation = cv.INTER_AREA)
            img = cv.copyMakeBorder(img, reduction, reduction, reduction, reduction, cv.BORDER_CONSTANT, value=(255,255,255))
            cv.imwrite("Bilder/tmp/option"+str(i)+".jpg", img)
        
    def set_image1(self,form, color):
        image1 = []
        image1.append(form)
        image1.append(color)
        self.last_shown_images[0] = image1
        
    def set_image2(self,form, color):
        image2 = []
        image2.append(form)
        image2.append(color)
        self.last_shown_images[1] = image2        
        
    def swap_images(self):
        self.last_shown_images[0], self.last_shown_images[1] = self.last_shown_images[1], self.last_shown_images[0]    

    def concatenate_second_img(self, img1, form_pool, color_pool):
        form=choice(form_pool)                          #Waehlt zufaellig eine Form aus
        art=randint(1,len(self.image_pool[form])-1)
        img2 = cv.imread("Bilder/"+self.image_pool[form][art]+".jpg", cv.IMREAD_COLOR)
        color_pool.remove(form)                        #Entfernt die zugehörige Farbe der Form, damit das zweite Bild keines der unteren matcht
        color = choice(color_pool)
        img2 = self.colorize_img(img2, color) #Faerbt das Bild random mit einer der uebrig gebliebenden Farben
        img2 = Bildgenerator.rotate_img(img2)
        
        self.set_image2(form, color)
        if randint(0,1):
            img1 = np.concatenate((img1, img2), axis=1)
        else:
            self.swap_images()
            img1 = np.concatenate((img2, img1), axis=1)
        cv.imwrite("Bilder/tmp/target.jpg", img1)

    
    def set_target(self, rule, picture):
        '''Selects randomly which method is used to set the target, with lower level the pictures will more often be exactly like
        one picture(instead of missmatching one picture)'''
        self.position = picture
        if rule == 1:
            self.set_target1()
            return 1
        elif rule==2:
            self.set_target2()
            return 2
     
    def set_target2(self):
        '''Generates one target picture with two pictures(only one picture is completly dissmatching)'''
        pool = [0, 1, 2, 3]
        pool.remove(self.position)  
        form1 = choice(pool)        #Zufaelliges Auswaehlen zweier Formen,
        pool.remove(form1)          #welche nicht zu der Antwort passen
        form2 = choice(pool)        #und entfernen aus dem pool,
        pool.remove(form2)          #damit das Bild nicht die selbe Form und Farbe hat wie eines der Antwortbilder
        color1 = pool[0]            #Weist die letzte Farbe dem ersten Bild zu
        color2 = form1              #Und die Farbe der Form des ersten Bildes dem zweiten Bild
        art=randint(1,len(self.image_pool[form1])-1)
        target1 = cv.imread("Bilder/"+self.image_pool[form1][art]+".jpg")
        target1 = self.colorize_img(target1, color1)
        art=randint(1,len(self.image_pool[form2])-1)
        target2 = cv.imread("Bilder/"+self.image_pool[form2][art]+".jpg")
        target2 = self.colorize_img(target2, color2)
        target2 = Bildgenerator.reduce_img_size(target2)
        target1 = Bildgenerator.reduce_img_size(target1)
        target2 = Bildgenerator.rotate_img(target2)
        target1 = Bildgenerator.rotate_img(target1)
        self.set_image1(form1, color1)
        self.set_image2(form2, color2)
        if randint(0,1):
            target1 = np.concatenate((target1, target2), axis=1) #Fuegt die Bilder an der vertikalen Achse zusammen
        else:
            self.swap_images()
            target1 = np.concatenate((target2, target1), axis=1)
        cv.imwrite("Bilder/tmp/target.jpg", target1)
        
    def set_target1(self):
        '''Generates one target picture with two pictures(only one picture is completly matching)'''
        color_pool = [0, 1, 2, 3]
        form_pool = [0, 1, 2, 3]
        art=randint(1,len(self.image_pool[self.position])-1)      #Waehlt zufaellig eine Art der gegeben Form aus
        form_pool.remove(self.position)
        target = cv.imread("Bilder/"+self.image_pool[self.position][art]+".jpg",cv.IMREAD_COLOR)
        color_pool.remove(self.position)
        self.set_image1(self.position, self.position)
        target = self.colorize_img(target,self.position) #Da der Farbcode der Optionbilder aufsteigend durchnummeriert wird
        target = Bildgenerator.rotate_img(target)
        self.concatenate_second_img(target, form_pool, color_pool) #Fuegt die Bilder an der vertikalen Achse zusammen

    def colorize_img(self, img, color_code):
        '''Colorize the image to the given color code'''
        #Invertiert alle Bilder und setzt dann den entsprechenden Farbkanal auf null und invertiert das Bild dann wieder
        img = ((255,255,255)-img)
        img[:,:,:] /= 128                       #Setzt alle pixel die invertiert ueber 128 liegen auf 1 alle anderen auf 0, somit werden alle Werte die im Bild dunkel waren 1 alle hellen 0
        if color_code == self.color_decode[0]:                      #Blau
            img[:,:,0] *= (255-207)              #(255-RGB-Werte, da diese am ende noch einmal invertiert werden
            img[:,:,1] *= (255-82)
            img[:,:,2] *= (255-21)
        elif color_code ==  self.color_decode[1]:                    #Gruen
            img[:,:,0] *= (255-27)              #(255-RGB-Werte, da diese am ende noch einmal invertiert werden
            img[:,:,1] *= (255-179)
            img[:,:,2] *= (255-42)
        elif color_code ==  self.color_decode[2]:                    #Rot
            img[:,:,0] *= (255-39)              #(255-RGB-Werte, da diese am ende noch einmal invertiert werden
            img[:,:,1] *= (255-11)
            img[:,:,2] *= (255-222)
        elif color_code ==  self.color_decode[3]:                    #Gelb
            img[:,:,0] *= (255-16)                 #(255-RGB-Werte, da diese am ende noch einmal invertiert werden
            img[:,:,1] *= (255-226)
            img[:,:,2] *= (255-242)
        img = ((255,255,255)-img)
        return img

    @staticmethod
    def rotate_img(img):
        '''Returns the given picture rotated by a random degree between -90 and 90 degrees'''
        img = img.astype(np.float32)
        img = ((255,255,255)-img)
        img = imutils.rotate_bound(img,randint(-40,40))
        img = cv.resize(img, (285,285))                     #sqrt(2)*200(groesst moegliche laenge bei 200 pixel grossen bildern)
        img = ((255,255,255)-img)
        return img
        
    @staticmethod
    def reduce_img_size(img):
        '''Returns a random reduced image of the given picture'''
        reduction = randint(10,60)
        dim = ((200-reduction*2), (200-reduction*2))
        img = img.astype(np.float32)
        img = cv.resize(img, dim, interpolation = cv.INTER_AREA)    #Reduziert das auf die gegebene Dimension
        img = cv.copyMakeBorder(img, reduction, reduction, reduction, reduction, cv.BORDER_CONSTANT, value=(255,255,255)) #Und fügt dann einen Rand hinzu
        return img
        
        