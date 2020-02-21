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
        self.fps = 30
        self.largeur = 1280
        self.hauteur = 720
        self.titre = "PowerFive"
        self.favicon = pygame.image.load('data/graphismes/favicon.png')
        pygame.display.set_icon(self.favicon)
        self.fenetre = pygame.display.set_mode( (self.largeur, self.hauteur) )

        self.music = Jukebox( musics = { "Pingu": os.path.join("data", "musiques", "pingu_theme.wav"),
                                         "Battle": os.path.join("data", "musiques", "battle_theme_full.wav") },
                              sounds = { "Jetons": [ pygame.mixer.Sound(os.path.join("data", "sons", "jeton0.wav")),
                                                    pygame.mixer.Sound(os.path.join("data", "sons", "jeton1.wav")),
                                                    pygame.mixer.Sound(os.path.join("data", "sons", "jeton2.wav")) ] } )

        self.sheriff=Personnage(self.fenetre,2,"sheriff",42,7,62,64,50,720-64*3-50)
        self.froggy=Personnage(self.fenetre,2,"froggy",24,5,62,64,1000,720-72*3-50)
        self.weasel=Personnage(self.fenetre,2,"weasel",13,5,62,72,1000,720-72*3-50)
        self.jurassy=Personnage(self.fenetre,2,"jurassy",13,5,62,72,1000,720-72*3-50)
        self.pingu=Personnage(self.fenetre,2,"pingu",27,5,62,96,1280-62*3-50,720-96*3-50)
        self.pingu_bad=Personnage(self.fenetre,2,"pingu_bad",33,5,62,96,1280-62*3-50,720-96*3-50)

        self.animBase = { "sheriff": self.sheriff.animation,
                          "froggy": self.froggy.animation,
                          "weasel": self.weasel.animation,
                          "jurassy": self.jurassy.animation,
                          "pingu": self.pingu.animation,
                          "pingu_bad": self.pingu_bad.animation }

        self.animBoutonUlti = [ Animation(self.fenetre, os.path.join("ultimate","ultimate1.png"),0,1,1,True,56,47,None,3,True,80+5,250-10),
                        Animation(self.fenetre, os.path.join("ultimate","ultimateboucle0.png"),0,12,2,False,56,47,None,3,True,80+5,250-10),
                        Animation(self.fenetre, os.path.join("ultimate","ultimateboucle.png"),0,12,3,True,56,47,None,3,True,80+5,250-10) ]

        self.animMana = [ 
                        Animation(self.fenetre, os.path.join("mana","mana0.png"),0,1,1,True,80,13,None,2,True,90,215),
                        Animation(self.fenetre, os.path.join("mana","mana1.png"),0,1,1,True,80,13,None,2,True,90,215),
                        Animation(self.fenetre, os.path.join("mana","mana2.png"),0,1,1,True,80,13,None,2,True,90,215),
                        Animation(self.fenetre, os.path.join("mana","mana3.png"),0,1,1,True,80,13,None,2,True,90,215), 
                        Animation(self.fenetre, os.path.join("mana","mana4.png"),0,1,1,True,80,13,None,2,True,90,215),
                        Animation(self.fenetre, os.path.join("mana","mana5.png"),0,1,1,True,80,13,None,2,True,90,215),
                        Animation(self.fenetre, os.path.join("mana","mana6.png"),0,1,1,True,80,13,None,2,True,90,215),
                        Animation(self.fenetre, os.path.join("mana","mana7.png"),0,1,1,True,80,13,None,2,True,90,215),
                        Animation(self.fenetre, os.path.join("mana","mana8.png"),0,1,1,True,80,13,None,2,True,90,215),
                        Animation(self.fenetre, os.path.join("mana","mana9.png"),0,1,1,True,80,13,None,2,True,90,215),
                        Animation(self.fenetre, os.path.join("mana","mana10.png"),0,1,1,True,80,13,None,2,True,90,215),
                        Animation(self.fenetre, os.path.join("mana","mana11.png"),0,1,1,True,80,13,None,2,True,90,215),
                        Animation(self.fenetre, os.path.join("mana","mana12.png"),0,1,1,True,80,13,None,2,True,90,215),
                        Animation(self.fenetre, os.path.join("mana","mana13.png"),0,1,1,True,80,13,None,2,True,90,215),
                        Animation(self.fenetre, os.path.join("mana","mana14.png"),0,1,1,True,80,13,None,2,True,90,215),
                        Animation(self.fenetre, os.path.join("mana","mana15.png"),0,1,1,True,80,13,None,2,True,90,215),
                        Animation(self.fenetre, os.path.join("mana","mana16.png"),0,1,1,True,80,13,None,2,True,90,215),
                        Animation(self.fenetre, os.path.join("mana","mana17.png"),0,1,1,True,80,13,None,2,True,90,215),
                        Animation(self.fenetre, os.path.join("mana","mana18.png"),0,1,1,True,80,13,None,2,True,90,215),
                        Animation(self.fenetre, os.path.join("mana","mana19.png"),0,1,1,True,80,13,None,2,True,90,215),
                        Animation(self.fenetre, os.path.join("mana","mana20.png"),0,1,1,True,80,13,None,2,True,90,215),
                        Animation(self.fenetre, os.path.join("mana","mana_full.png"),0,7,5,True,78,12,None,2,True,90,215),
                        Animation(self.fenetre, os.path.join("mana","mana_deremplissage.png"),0,21,2,False,80,12,None,2,True,90,215),
                        ]
        
        self.animSaloon = [ Animation(self.fenetre, os.path.join("saloon","saloon1.png"), 0,10,3,False,428,240,None,3,True,0,0), 
                        Animation(self.fenetre, os.path.join("saloon","saloon2.png"), 0,10,3,False,428,240,None,3,True,0,0),
                        Animation(self.fenetre, os.path.join("saloon","saloon3.png"), 0,10,3,False,428,240,None,3,True,0,0),
                        Animation(self.fenetre, os.path.join("saloon","saloon4.png"), 0,10,3,False,428,240,None,3,True,0,0),
                        Animation(self.fenetre, os.path.join("saloon","saloon5.png"), 0,10,3,False,428,240,None,3,True,0,0)
                        ]

        self.animSaloonVide = {"Saloon": None}
    
        self.animSpec = {}
        self.grille = Grille()
        self.listeInterfaces = [Interface(self.fenetre, self.largeur, self.hauteur, self.grille, self.animBase, self.animSpec, "saloon", "weasel", self.music),
                                Interface(self.fenetre, self.largeur, self.hauteur, self.grille, self.animBase, self.animSpec, "saloon", "jurassy", self.music)]
        self.interface = Interface(self.fenetre, self.largeur, self.hauteur, self.grille, self.animBase, self.animSpec, "saloon", "weasel", self.music)
        self.moteur = MoteurJeu(self.interface, self.grille, self.Clock)
        self.ia = IA(self.moteur,"normal")

        self.posSouris = (0,0)
        self.idJoueur = 1
        self.barreMana = ObjetAnimMultiple(85,50,self.animMana,self.animBase,"Mana")
        self.boutonUlti = ObjetAnimMultiple(85,240,self.animBoutonUlti,self.animBase)
        self.saloon = ObjetAnimMultiple(0,0,self.animSaloon,self.animSaloonVide,"Saloon")
        self.dialogue = Dialogue("data/dialogues/saloon.xml")
        self.compteurMana=0
        self.manaFull=False
        self.compteurManaVide=0
        self.seVide=False
        self.clicked=False
    
    def mainLoop(self,ennemi=None):
        self.music.playMusic("Battle")
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

            if(self.interface.tourJoueur): self.idJoueur = 1
            else: self.idJoueur = 2
            self.posSouris = pygame.mouse.get_pos()
            if(not self.interface.tourJoueur): self.ia.IAPlay()
            #Affichage
            self.boutonUlti.updateCurrentAnim(condition=self.boutonUlti.clicked and self.manaFull)


            #Gestion MANA
            self.barreMana.updateCurrentAnim(condition=(self.moteur.lacher) and (self.idJoueur==1) and (self.compteurMana<21))

            if (self.moteur.lacher) and (self.idJoueur==1) and (self.compteurMana<21): #Compteur à chaque fois que le joueur joue
                self.compteurMana+=1

            if self.compteurManaVide!=0: #Compteur pour laisser la mana se vider
                self.compteurManaVide-=1

            if (self.compteurMana==21): #Si le compteur == 21, la mana est pleine
                self.manaFull=True
            
            if self.boutonUlti.clicked: #Si jamais le bouton Ultimate a été clické une fois
                self.clicked=True

            if self.compteurMana==21 and self.seVide==False and (self.moteur.lacher==True) and (self.idJoueur==1) and self.clicked==True:
                    self.barreMana.updateCurrentAnim(condition=self.compteurMana==21)
                    self.compteurManaVide=32
                    self.seVide=True
                    self.clicked=False
                    print("DECOMPTE SE VIDE ENCLANCHE")

            if (self.interface.reinitialise):
                Main().saloonLoop()

            if (self.compteurManaVide==0 and self.seVide==True) or (self.interface.reinitialise==True):
                self.compteurMana=0
                self.compteurManaVide=0
                self.barreMana.Reinitialiser()
                self.interface.reinitialise=False
                self.seVide=False
                self.manaFull=False
                self.interface=self.listeInterfaces[1]
            #------------------Fin Gestion Mana

            #Bidouillage pour changer l'ennemi
            if(ennemi!=None):
                self.interface.ennemi=ennemi
            #------------------Fin du bidouillage

            #Gestion affichage
            self.interface.Affichage()
            self.interface.AttentePlacement(self.posSouris,self.idJoueur)
            #------------------Fin gestion affichage

            #Gestion dialogues
            if(self.interface.dialogueFini==False):
                self.interface.afficheTexte(2,self.getEnnemi(self.interface.ennemi).dialogue[0])
                #self.interface.afficheTexte(1,"Moi j'suis l'Sheriff !")
            #------------------Fin gestion dialogues
            
            pygame.display.update()

    def saloonLoop(self):
        self.music.playMusic("Pingu")
        rectWeasel = pygame.Rect(160,125,75,90)
        rectJurassy= pygame.Rect(1020,380,195,185)
        rectFroggy = pygame.Rect(180*3,15*3,60*3,57*3)
        while True:
            self.posSouris = pygame.mouse.get_pos()
            self.Clock.tick(self.fps)
            pygame.display.set_caption(self.titre)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if( rectJurassy.collidepoint(self.posSouris) ):
                        self.moteur = MoteurJeu(self.interface, self.grille, self.Clock)
                        print("clic jurassy")
                        Main().mainLoop("jurassy")

                    elif( rectWeasel.collidepoint(self.posSouris) ):
                        self.moteur = MoteurJeu(self.interface, self.grille, self.Clock)
                        print("clic weasel")
                        Main().mainLoop("weasel")

                    elif ( rectFroggy.collidepoint(self.posSouris) ):
                        self.moteur = MoteurJeu(self.interface, self.grille, self.Clock)
                        print("clic froggy")
                        Main().mainLoop("froggy")
            
            self.saloon.updateCurrentAnim(condition=True)
                                
            self.interface.AffichageSaloon(self.animSaloonVide)
            pygame.display.update()
        
    def menuLoop(self):
        police = pygame.font.Font(None,20)
        texteRendu = police.render("Jouer",True,pygame.Color("#FFFFFF"))
        while True :
            self.posSouris = pygame.mouse.get_pos()
            self.Clock.tick(self.fps)
            pygame.display.set_caption(self.titre)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                """if event.type == pygame.MOUSEBUTTONDOWN:
                    """
            self.fenetre.blit(texteRendu,(640,360))
                

    def getEnnemi(self, ennemi):
        if self.interface.ennemi==self.sheriff.nomPerso:
            return self.sheriff
        elif self.interface.ennemi==self.froggy.nomPerso:
            return self.froggy
        elif self.interface.ennemi==self.weasel.nomPerso:
            return self.weasel
        elif self.interface.ennemi==self.jurassy.nomPerso:
            return self.jurassy
        elif self.interface.ennemi==self.pingu.nomPerso:
            return self.pingu
        elif self.interface.ennemi==self.pingu_bad.nomPerso:
            return self.pingu_bad

    def getMode(self):
        return self.interface.mode

    def TestIA(self):
                              #y 0 1 2 3 4 5 6 7  8     x
        self.grillePrincipal = [[0,0,0,0,0,0,0,2,-1],  #0
                                [0,0,0,0,0,0,0,1,-1],  #1
                                [0,0,0,0,0,0,0,2,-1],  #2
                                [0,0,0,0,0,0,0,1,-1],  #3
                                [0,0,0,0,0,0,2,2,-1],  #4
                                [0,0,0,0,0,0,1,1,-1],  #5
                                [0,0,0,0,0,0,0,2,-1],  #6
                                [0,0,0,0,0,0,0,1,-1],  #7
                                [0,0,0,0,0,0,0,2,-1]]  #8
        note = self.ia.Note(0,(4,5),2)
        print(note)

if __name__ == "__main__":
    """if Main().getMode()=="menu":
        jeu=Main().menuLoop()"""
    """if Main().getMode()=="combat":
        jeu = Main().mainLoop()"""
    if Main().getMode()=="saloon":
        jeu = Main().saloonLoop()
