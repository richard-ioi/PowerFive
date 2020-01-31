#! /usr/bin/env python3

import pygame
import os
from moteurJeu import *
from modeles import *
from vue import *

"""
    Fichier principal initialisant l'ensemble des classes du jeu.
"""

class Main:

    def __init__(self):
        self.initJeu()
    
    def initJeu(self):
        pygame.init()
        self.Clock = pygame.time.Clock()
        self.fps = 60
        self.largeur = 1280
        self.hauteur = 720
        self.titre = "PowerFive"
        self.fenetre = pygame.display.set_mode( (self.largeur, self.hauteur) )
        #self.music = Sons("pingu_theme.wav")
        self.animBase = { "Sheriff": Animation(self.fenetre, os.path.join("sheriff", "char.png"), 0, 42, 7, True, 62, 64),
                          "Froggy": Animation(self.fenetre, os.path.join("froggy", "char.png"), 0, 24, 5),
                          "Weasel": Animation(self.fenetre, os.path.join("weasel", "char.png"), 0, 13, 5, True, 62, 72),
                          "Jurassy": Animation(self.fenetre, os.path.join("jurassy", "char.png"), 0, 13, 5, True, 62, 72),
                          "Pingu": Animation(self.fenetre, os.path.join("pingu","char.png"), 0,27,5,True,62,96),
                          "PinguBad": Animation(self.fenetre, os.path.join("pingu","char_bad.png"), 0,33,5,True,62,96) }
        self.animSpec = {}
        self.grille = Grille()
        self.interface = Interface(self.fenetre, self.largeur, self.hauteur, self.grille, self.animBase, self.animSpec)
        self.moteur = MoteurJeu(self.interface, self.grille, self.Clock)
    
    def mainLoop(self):
        while True:
            self.Clock.tick(self.fps)
            pygame.display.set_caption(self.titre)

            posSouris = pygame.mouse.get_pos()
            
            if self.interface.tourJoueur:
                idJoueur = 1
            else:
                idJoueur = 2

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for rect in self.interface.rectColonne:
                        if rect["rect"].collidepoint( (posSouris[0]-5, posSouris[1]) ):
                            self.moteur.Placer(rect["colonne"], idJoueur)

            self.interface.Affichage()
            self.interface.AttentePlacement(posSouris, idJoueur)

            pygame.display.update()

if __name__ == "__main__":
    jeu = Main().mainLoop()