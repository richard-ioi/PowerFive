#! /usr/bin/env python3

"""
    Fichier principal initialisant l'ensemble des classes du jeu.
"""

import pygame
import os
from moteurJeu import *
from modeles import *
from vue import *

pygame.init()
Clock = pygame.time.Clock()
done = False

largeurFenetre = 1280
hauteurFenetre = 720
Fenetre = pygame.display.set_mode( (largeurFenetre, hauteurFenetre) )
pygame.display.set_caption("PowerFive")
combat=1
music_pinguTheme = os.path.join("data","sons","pingu_theme.wav")
pygame.mixer.music.load(music_pinguTheme)
pygame.mixer.music.play(loops=-1,start=0.0)

AnimBase = { "Sheriff": Animation(Fenetre, os.path.join("sheriff", "char.png"), 0, 42, 5, True, 62, 64),
             "Froggy": Animation(Fenetre, os.path.join("froggy", "char.png"), 0, 24, 5),
             "Weasel": Animation(Fenetre, os.path.join("weasel", "char.png"), 0, 13, 5, True, 62, 72),
             "Jurassy": Animation(Fenetre, os.path.join("jurassy", "char.png"), 0, 13, 5, True, 62, 72),
             "Pingu": Animation(Fenetre, os.path.join("pingu","char.png"), 0,27,5,True,62,96),
             "PinguBad": Animation(Fenetre, os.path.join("pingu","char_bad.png"), 0,33,5,True,62,96) }
AnimSpec = {}
AnimSaloon = { "Saloon1": Animation(Fenetre, os.path.join("saloon","saloon1.png"), 0,10,5,False,428,240), 
             "Saloon2": Animation(Fenetre, os.path.join("saloon","saloon2.png"), 0,10,5,False,428,240),
             "Saloon3": Animation(Fenetre, os.path.join("saloon","saloon3.png"), 0,10,5,False,428,240),
             "Saloon4": Animation(Fenetre, os.path.join("saloon","saloon4.png"), 0,10,5,False,428,240),
             "Saloon5": Animation(Fenetre, os.path.join("saloon","saloon5.png"), 0,10,5,False,428,240)}

GrilleDeJeu = Grille()
MoteurDeJeu = MoteurJeu(GrilleDeJeu, Clock)
InterfaceJeu = Interface(Fenetre, largeurFenetre, hauteurFenetre, GrilleDeJeu, AnimBase, AnimSpec,combat)
self.saloon= ObketAnimMultiple(0,0,self.AnimSaloon, self.animBase,"Saloon")
Joueur = Joueur()
Jeton = Jeton(0,1)
    
#imageJeton = scale(pygame.image.load(os.path.join("data","graphismes","jeton_jaune.png")), (32*4,32*4))
#posJeton = -10

while not done:
    Clock.tick(60)
    FPS = Clock.get_fps()
    #print(FPS)
    event = pygame.event.Event(pygame.USEREVENT)
    pygame.event.pump()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    pygame.display.flip()
    
    #posJeton += 5

    #Affichage
    #screen.blit(imageJeton,(screenLargeur//2-imageJeton.get_width()//2-4 , posJeton))
    InterfaceJeu.Affichage()
