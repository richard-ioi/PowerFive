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
             "PinguBad": Animation(Fenetre, os.path.join("pingu","char_bad.png"), 0,33,5,True,62,96) }

AnimSpec = { "test":Animation(Fenetre, os.path.join("sheriff", "char.png"), 0, 42, 7, True, 62, 64) }

AnimBoutonUlti = [ Animation(Fenetre, os.path.join("ultimate","ultimate1.png"),0,1,1,True,56,46,None,3,True),
                   Animation(Fenetre, os.path.join("ultimate","ultimateboucle0.png"),0,12,2,False,56,46),
                   Animation(Fenetre, os.path.join("ultimate","ultimateboucle.png"),0,12,3,True,56,46) ]

GrilleDeJeu = Grille()
InterfaceJeu = Interface(Fenetre, largeurFenetre, hauteurFenetre, GrilleDeJeu, AnimBase, AnimSpec)
MoteurDeJeu = MoteurJeu(InterfaceJeu, GrilleDeJeu, Clock)

idJoueur = 0

posSouris = (0,0)

boutonUlti = ObjetAnimMultiple(85,240,AnimBoutonUlti,AnimBase)   #Creation du bouton d'ultime à partir de la classe Bouton
conditionsAnimBouton = [False,False,False]
print(GrilleDeJeu)

while True:
    Clock.tick(60)
    FPS = Clock.get_fps()
    #print(FPS)
    #print(boutonUlti.currentAnim.play)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if( boutonUlti.currentAnim.rect.collidepoint(posSouris) ):
                boutonUlti.clicked = True

            for rect in InterfaceJeu.rectColonne:
                if rect["rect"].collidepoint( (posSouris[0]-5, posSouris[1]) ):
                    MoteurDeJeu.Placer(rect["colonne"],idJoueur)
                    boutonUlti.Reinitialiser()
                    print(GrilleDeJeu)

    if(InterfaceJeu.tourJoueur): idJoueur = 1
    else: idJoueur = 2
    posSouris = pygame.mouse.get_pos()
    #Affichage
    boutonUlti.updateCurrentAnim(condition=boutonUlti.clicked)
    InterfaceJeu.Affichage()
    InterfaceJeu.AttentePlacement(posSouris,idJoueur)
    
    #screen.blit(imageJeton,(screenLargeur//2-imageJeton.get_width()//2-4 , posJeton))
    
    InterfaceJeu.afficheTexte(1,"YEEEEEEEEEEEHAW SALUT LA TEAM JE VIENS DEFONCER VOS SALES GUEULES ! OH TU FAIS QUOI LA? ESPECE DE SOUS MERDE JE VAIS TE DEFONCER LA GUEULE A COUP DE CLE A MOLETTE T'ES AUSSI MOCHE QUE GUILLAIME BAZIN")
    pygame.display.update()
