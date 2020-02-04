#! /usr/bin/env python3

import pygame
import os
import sys
from controleur import *
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
        """self.music = Jukebox( musics = { "Pingu": os.path.join("data", "musiques", "pingu_theme.wav",
                                         "Devil Pingu": os.path.join("data", "musiques", "devil_pingu_theme.wav" },
                              sounds = { "Explosion": pygame.mixer.Sound( os.path.join("data", "sons", "explosion.wav") ),
                                         "Succes": pygame.mixer.Sound( os.path.join("data", "sons", "succes.wav") ) } )
        self.music.playMusic("Pingu")"""
        self.animBase = { "Sheriff": Animation(self.fenetre, os.path.join("sheriff", "char.png"), 0, 42, 7, True, 62, 64),
                          "Froggy": Animation(self.fenetre, os.path.join("froggy", "char.png"), 0, 24, 5),
                          "Weasel": Animation(self.fenetre, os.path.join("weasel", "char.png"), 0, 13, 5, True, 62, 72),
                          "Jurassy": Animation(self.fenetre, os.path.join("jurassy", "char.png"), 0, 13, 5, True, 62, 72),
                          "Pingu": Animation(self.fenetre, os.path.join("pingu","char.png"), 0,27,5,True,62,96),
                          "PinguBad": Animation(self.fenetre, os.path.join("pingu","char_bad.png"), 0,33,5,True,62,96) }

        self.animBoutonUlti = [ Animation(self.fenetre, os.path.join("ultimate","ultimate1.png"),0,1,1,True,56,47,None,3,True),
                        Animation(self.fenetre, os.path.join("ultimate","ultimateboucle0.png"),0,12,2,False,56,47),
                        Animation(self.fenetre, os.path.join("ultimate","ultimateboucle.png"),0,12,3,True,56,47) ]

        self.animMana = [ 
                        Animation(self.fenetre, os.path.join("mana","mana0.png"),0,1,1,True,80,13,None,2,True),
                        Animation(self.fenetre, os.path.join("mana","mana1.png"),0,1,1,True,80,13,None,2,True),
                        Animation(self.fenetre, os.path.join("mana","mana2.png"),0,1,1,True,80,13,None,2,True),
                        Animation(self.fenetre, os.path.join("mana","mana3.png"),0,1,1,True,80,13,None,2,True), 
                        Animation(self.fenetre, os.path.join("mana","mana4.png"),0,1,1,True,80,13,None,2,True),
                        Animation(self.fenetre, os.path.join("mana","mana5.png"),0,1,1,True,80,13,None,2,True),
                        Animation(self.fenetre, os.path.join("mana","mana6.png"),0,1,1,True,80,13,None,2,True),
                        Animation(self.fenetre, os.path.join("mana","mana7.png"),0,1,1,True,80,13,None,2,True),
                        Animation(self.fenetre, os.path.join("mana","mana8.png"),0,1,1,True,80,13,None,2,True),
                        Animation(self.fenetre, os.path.join("mana","mana9.png"),0,1,1,True,80,13,None,2,True),
                        Animation(self.fenetre, os.path.join("mana","mana10.png"),0,1,1,True,80,13,None,2,True),
                        Animation(self.fenetre, os.path.join("mana","mana11.png"),0,1,1,True,80,13,None,2,True),
                        Animation(self.fenetre, os.path.join("mana","mana12.png"),0,1,1,True,80,13,None,2,True),
                        Animation(self.fenetre, os.path.join("mana","mana13.png"),0,1,1,True,80,13,None,2,True),
                        Animation(self.fenetre, os.path.join("mana","mana14.png"),0,1,1,True,80,13,None,2,True),
                        Animation(self.fenetre, os.path.join("mana","mana15.png"),0,1,1,True,80,13,None,2,True),
                        Animation(self.fenetre, os.path.join("mana","mana16.png"),0,1,1,True,80,13,None,2,True),
                        Animation(self.fenetre, os.path.join("mana","mana17.png"),0,1,1,True,80,13,None,2,True),
                        Animation(self.fenetre, os.path.join("mana","mana18.png"),0,1,1,True,80,13,None,2,True),
                        Animation(self.fenetre, os.path.join("mana","mana19.png"),0,1,1,True,80,13,None,2,True),
                        Animation(self.fenetre, os.path.join("mana","mana20.png"),0,1,1,True,80,13,None,2,True),
                        Animation(self.fenetre, os.path.join("mana","mana_full.png"),0,7,5,True,78,12,None,2,True),
                        Animation(self.fenetre, os.path.join("mana","mana_deremplissage.png"),0,21,2,False,80,12,None,2,True),
                        ]

        self.animSpec = {}
        self.grille = Grille()
        self.interface = Interface(self.fenetre, self.largeur, self.hauteur, self.grille, self.animBase, self.animSpec)
        self.moteur = MoteurJeu(self.interface, self.grille, self.Clock)
        self.ia = IA(self.moteur)
        self.posSouris = (0,0)
        self.idJoueur = 1
        self.barreMana = ObjetAnimMultiple(85,50,self.animMana,self.animBase,"Mana")
        self.boutonUlti = ObjetAnimMultiple(85,240,self.animBoutonUlti,self.animBase)
        self.dialogue = Dialogue("data/dialogues/saloon.xml")
        self.compteurMana=0
        self.manaFull=False
        self.compteurManaVide=0
    
    def mainLoop(self):
        while True:
            self.Clock.tick(self.fps)
            pygame.display.set_caption(self.titre)

            self.moteur.lacher=False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.interface.compteur==0:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        
                        if( self.boutonUlti.currentAnim.rect.collidepoint(self.posSouris) ):
                            self.boutonUlti.clicked = True

                        for rect in self.interface.rectColonne:
                            if rect["rect"].collidepoint( (self.posSouris[0]-5, self.posSouris[1]) ):
                                self.moteur.Placer(rect["colonne"],self.idJoueur)
                                self.boutonUlti.Reinitialiser()
                                self.manaFull=False
                                print(self.grille)

            if self.compteurManaVide!=0:
                self.compteurMana-=1

            if self.compteurManaVide==0 and self.compteurMana==22:
                self.compteurMana=0
                self.compteurManaVide=0
                self.barreMana.Reinitialiser()
                
            if(self.interface.tourJoueur): self.idJoueur = 1
            else: self.idJoueur = 2
            self.posSouris = pygame.mouse.get_pos()
            if(not self.interface.tourJoueur): self.ia.IAPlay()
            #Affichage
            self.boutonUlti.updateCurrentAnim(condition=self.boutonUlti.clicked and self.manaFull)
            self.barreMana.updateCurrentAnim(condition=(self.moteur.lacher) and (self.idJoueur==1) and(self.compteurMana<21))
            if (self.compteurMana==21):
                self.manaFull=True
            if (self.moteur.lacher) and (self.idJoueur==1) and(self.compteurMana<22):
                self.compteurMana+=1
            if (self.boutonUlti.clicked and self.compteurMana==21):
                self.barreMana.updateCurrentAnim(condition=True)
                self.compteurManaVide=22
            self.interface.Affichage()
            self.interface.AttentePlacement(self.posSouris,self.idJoueur)
            
            if(self.interface.dialogueFini==False):
                self.interface.afficheTexte(2,self.dialogue.getDialogues("Pingu")[0])
                #self.interface.afficheTexte(1,"Moi j'suis l'Sheriff !")
            pygame.display.update()

if __name__ == "__main__":
    jeu = Main().mainLoop()