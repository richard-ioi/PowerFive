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

largeurFenetre = 1280
hauteurFenetre = 720
Fenetre = pygame.display.set_mode( (largeurFenetre, hauteurFenetre) )
pygame.display.set_caption("PowerFive")

music_pinguTheme = os.path.join("data","sons","pingu_theme.wav")
pygame.mixer.music.load(music_pinguTheme)
pygame.mixer.music.play(loops=-1,start=0.0)

AnimBase = { "Sheriff": Animation(Fenetre, os.path.join("sheriff", "char.png"), 0, 42, 7, True, 62, 64),
             "Froggy": Animation(Fenetre, os.path.join("froggy", "char.png"), 0, 24, 5),
             "Jurassy": Animation(Fenetre, os.path.join("jurassy", "char.png"), 0, 13, 5, True, 62, 72),
             "Pingu": Animation(Fenetre, os.path.join("pingu","char.png"), 0,27,5,True,62,96),
             "Weasel": Animation(Fenetre, os.path.join("weasel","char.png"),0,13,7,True,62,72),
             "PinguBad": Animation(Fenetre, os.path.join("pingu","char_bad.png"), 0,33,5,True,62,96),
             "Ultimatebouton": Animation(Fenetre, os.path.join("ultimate","ultimate1.png"),0,1,1,True,56,46,None,3,True),
             "Ultimateboucle": Animation(Fenetre, os.path.join("ultimate","ultimateboucle.png"),0,12,3,True,56,46),
             "Ultimateboucle0": Animation(Fenetre, os.path.join("ultimate","ultimateboucle0.png"),0,12,3,False,56,46) }

AnimSpec = { "test":Animation(Fenetre, os.path.join("sheriff", "char.png"), 0, 42, 7, True, 62, 64) }

GrilleDeJeu = Grille()
InterfaceJeu = Interface(Fenetre, largeurFenetre, hauteurFenetre, GrilleDeJeu, AnimBase, AnimSpec)
MoteurDeJeu = MoteurJeu(InterfaceJeu, GrilleDeJeu, Clock)

Joueur = Joueur()

posSouris = (0,0)

boutonUlti_animActuel = AnimBase["Ultimatebouton"]
AnimSpec.update(bouton=boutonUlti_animActuel, bouton2=AnimBase["Ultimateboucle0"])
print(AnimSpec)

while True:
    Clock.tick(60)
    FPS = Clock.get_fps()
    #print(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if( AnimBase["Ultimatebouton"].rect.collidepoint(posSouris) ):
                print("Button pressed")
                boutonUlti_animActuel.play = False
                boutonUlti_animActuel = AnimBase["Ultimateboucle0"]
                AnimSpec["bouton"] = boutonUlti_animActuel
                AnimSpec["bouton"].play = True
            for rect in InterfaceJeu.rectColonne:
                if rect["rect"].collidepoint(posSouris):
                    MoteurDeJeu.Placer(rect["colonne"],1)
    
    posSouris = pygame.mouse.get_pos()
    
    
    #posJeton += 5
    InterfaceJeu.AttentePlacement(posSouris)
    #Affichage
    InterfaceJeu.Affichage()
    #screen.blit(imageJeton,(screenLargeur//2-imageJeton.get_width()//2-4 , posJeton))
    pygame.display.update()
