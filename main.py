#!/usr/bin/env python3
# coding: utf-8


import PIL
import os
from gi.repository import Gtk
from picamera import PiCamera
#from datetime import datetime
from time import sleep
from PIL import Image


adresse='/home/pi/Photobooth/resized/'
liste = os.listdir(adresse)
image=len(liste)


def capture(label):
    camera=PiCamera()
    galerie_window.hide ()
    camera.start_preview()
    camera.annotate_text = "Mettez vous en place..."
    sleep(2)
    camera.annotate_text = "Vous etes prets?"
    sleep(2)
    camera.annotate_text = "Souriez!"
    sleep(2)
    camera.annotate_text = ""
 
    filename = '/home/pi/Photobooth/photobooth/{}.jpg'.format(len(os.listdir(adresse))+1)
    camera.capture(filename)
    width = 600
    height = 360
    img = Image.open(filename)
    img = img.resize((width,height), PIL.Image.ANTIALIAS)
    resized_filename = '/home/pi/Photobooth/resized/{}.jpg'.format(len(os.listdir(adresse))+1)
    img.save(resized_filename)
    main_window.fullscreen()
    main_window.show_all()
    camera.close()
    
def when_right_button_is_clicked(label):
    '''
    Quand le bouton droit est cliqué on affiche la photo suivante
    '''
    global adresse
    global image
    liste = os.listdir(adresse)
    image+=1 #on incrémente le numero de la photo
    image=min(len(liste),image)#on limite a la dernière photo
    image1.set_from_file(adresse+str(image)+".jpg")


def when_left_button_is_clicked(label):
    '''
    Quand le bouton est cliqué on affiche la photo précédente
    '''
    global adresse
    global image
    liste = os.listdir(adresse)
    image-=1
    image=max(1,image)
    image1.set_from_file(adresse+str(image)+".jpg")
    
def when_return_button_is_clicked(label):
    '''
    Quand le bouton est cliqué on affiche la photo précédente
    '''    
    galerie_window.hide ()
    galerie_window.fullscreen()
    main_window.show_all()
    

def when_photo_button_is_clicked(label):
    '''
    Quand le bouton photo est cliqué 
    '''

def when_galerie_button_is_clicked(label):
    '''
    Quand le bouton est cliqué 
    '''
    global image
    
    liste = os.listdir(adresse)
    image=len(liste)
    
    image1.set_from_file(adresse+str(len(liste))+".jpg") #on commence en affichant la dernière photo prise
    main_window.hide ()
    galerie_window.fullscreen()
    galerie_window.show_all()
    


builder = Gtk.Builder()
builder.add_from_file('/home/pi/Photobooth/main.glade')  # Rentrez évidemment votre fichier, pas le miens!
main_window = builder.get_object('main_window')
galerie_window = builder.get_object('galerie_window')
# Peut se faire dans Glade mais je préfère le faire ici, à vous de voir
main_window.connect('delete-event', Gtk.main_quit)
galerie_window.connect('delete-event', Gtk.main_quit)

image1=builder.get_object('image1')


# Le handler
handler = {'photo': capture,'galerie': when_galerie_button_is_clicked,'right': when_right_button_is_clicked,'left': when_left_button_is_clicked,'return': when_return_button_is_clicked}
builder.connect_signals(handler)

main_window.fullscreen()
main_window.show_all()
Gtk.main()
