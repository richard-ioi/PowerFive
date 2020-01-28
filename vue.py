#! /usr/bin/env python3

"""
    Module regroupant les vues du jeu.
"""

import pygame
import os
from pygame.transform import scale

class Interface:
    """
        Classe constituant l'interface du jeu.
    """
    def __init__(self,screen,grilleJeu):
        """
            Constructeur de la classe.

            Args:
                screen: Objet d'affichage du module pygame
                grilleJeu: Objet Grille utilisé par le jeu
        """
        self.screen = screen
        self.grilleJeu = grilleJeu
        self.AnimFroggy = Animation(screen,"froggy/char.png",0,24,5)
        self.AnimWheatle = Animation(screen,"weasel/char.png",0,13,5,True,62,72)
        self.AnimJurassy = Animation(screen,"jurassy/char.png",0,13,5,True,62,72)

    def Affichage(self):
        """
            Méthode exécutant les procédure d'affichages sur l'écran
        """
        screenLargeur = 1280
        screenHauteur = 720
        self.screen.fill([255,255,255])
        self.screen.blit(self.grilleJeu.imageBack,(screenLargeur//2-self.grilleJeu.largeurImage//2-8 , screenHauteur//2-self.grilleJeu.hauteurImage//2-8))
        self.screen.blit(self.grilleJeu.image,(screenLargeur//2-self.grilleJeu.largeurImage//2 , screenHauteur//2-self.grilleJeu.hauteurImage//2))
        
        self.AnimFroggy.play = self.AnimWheatle.play = self.AnimJurassy.play = True

        if( self.AnimFroggy.play ):
            #print("First ",AnimTest.speed)
            self.AnimFroggy.update(self.AnimFroggy.x_pos,self.AnimFroggy.y_pos)
            self.AnimFroggy.affiche(1000,520)
        if( self.AnimWheatle.play ):
            #print("First ",AnimTest.speed)
            self.AnimWheatle.update(self.AnimWheatle.x_pos,self.AnimWheatle.y_pos)
            self.AnimWheatle.affiche(1000,0)
        if( self.AnimJurassy.play ):
            #print("First ",AnimTest.speed)
            self.AnimJurassy.update(self.AnimJurassy.x_pos,self.AnimJurassy.y_pos)
            self.AnimJurassy.affiche(1000,250)

class Animation:
    """
        Classe définissant les animations du jeu.
    """
    def __init__(self, screen, palette, y_sprite1, nb_sprites, speed=1, loop=True, width=62, height=64):
        """
            Constructeur de la classe

            Args:
                screen: Ecran du jeu
                palette: Palette de sprites à animer
                y_sprites1: 
                nb_sprites: 
                speed: Intervalle de temps entre chaque frames de l'animation
                loop: Booléen permettant de jouer en boucle l'animation
                width: Largeur des sprites
                height: Hauteur des sprites
        """
        self.screen = screen
        self.palette_name = palette
        self.palette = pygame.image.load(os.path.join("data","graphismes",self.palette_name))
        self.x_pos = 2
        self.y_pos = y_sprite1
        self.larg_sprite = width
        self.haut_sprite = height
        self.nb_sprites = nb_sprites
        self.sprite_list = []
        self.speed = speed
        self.isLoop = loop
        self.play = False
        self.play_count = 0
        self.update(self.x_pos,self.y_pos)

    def update(self, x_sprites=1, y_sprites=1):
        """
            Méthode mettant à jour l'animation

            Args:
                x_sprites: 
                y_sprites: 
        """
        self.x_pos = x_sprites
        self.y_pos = y_sprites
        self.sprite_list = []
        for i_sprite in range(self.nb_sprites):
            #print(x_sprites+(self.larg_sprite+1)*i_sprite)
            sprite = self.palette.subsurface(x_sprites+(self.larg_sprite+2)*i_sprite, y_sprites, self.larg_sprite-1, self.haut_sprite-1)
            #if self.palette_name == "microman_sprites.png":
            sprite = scale(sprite, (self.larg_sprite*3,self.haut_sprite*3))
            self.sprite_list.append(sprite)

    def affiche(self, x, y):
        """
            Méhode affichant l'animation.

            Args:
                x:
                y: 
        """
        #print(new_speed)
        if self.play_count >= self.nb_sprites * self.speed:
            if self.isLoop:
                self.play_count = 0
            else:
                self.play_count = 0
                self.play = False
        if self.play:
            sprite = self.sprite_list[self.play_count//self.speed]
            self.screen.blit(sprite, (x,y))
            self.play_count += 1

class Joueur:
    """
        Classe représentant un joueur.
    """
    def __init__(self):
        """
            Constructeur de la classe.
        """
        self.posSouris = (0,0)
        self.idJoueur = 1

    def CliqueSouris(self,event,boutonSouris):
        """
            Méthode récupérant le clic de sourit du joueur.

            Args:
                event: évènement pygame
                boutonSouris: 
        """
        if event.type == boutonSouris:
            self.posSouris = event.pos
            return self.posSouris
