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
    def __init__(self, fenetre, largeur, hauteur, grille, animBase, animSpec):
        """
            Constructeur de la classe.

            Args:
                fenetre: Fenêtre pygame
                grille: Grille utilisé par le jeu
                animBase: Dictionnaire des Animations de base
                animSpec: Dictionnaire des Animations circonstancielles
        """
        #self.fenetre = pygame.display.set_mode( (largeur, hauteur) )
        #self.titre = pygame.display.set_caption(titre)
        self.fenetre = fenetre
        self.largeur = largeur
        self.hauteur = hauteur
        self.grille = grille
        self.animBase = animBase
        self.animSpec = animSpec
    
    def Affichage(self):
        """
            Méthode exécutant les procédure d'affichages sur l'écran
        """
        self.fenetre.fill([255,255,255])
        self.fenetre.blit( self.grille.sprites["back"], ( self.largeur//2 - self.grille.dimSprites[0]//2 - 8, self.hauteur//2 - self.grille.dimSprites[1]//2 - 8 ) )
        self.fenetre.blit( self.grille.sprites["top"], ( self.largeur//2 - self.grille.dimSprites[0]//2 , self.hauteur//2 - self.grille.dimSprites[1]//2 ) )
        
        for animation in self.animBase.values():
            animation.play = True

        for animation in list(self.animBase.values()) + list(self.animSpec.values()):
            if animation.play:
                animation.update( animation.x_pos, animation.y_pos )
                if animation == self.animBase["Froggy"]:
                    animation.affiche(1000,520)
                if animation == self.animBase["Wheatle"]:
                    animation.affiche(1000,0)
                if animation == self.animBase["Jurassy"]:
                    animation.affiche(1000,250)

        # if( self.AnimFroggy.play ):
        #     #print("First ",AnimTest.speed)
        #     self.AnimFroggy.update(self.AnimFroggy.x_pos,self.AnimFroggy.y_pos)
        #     self.AnimFroggy.affiche(1000,520)
        # if( self.AnimWheatle.play ):
        #     #print("First ",AnimTest.speed)
        #     self.AnimWheatle.update(self.AnimWheatle.x_pos,self.AnimWheatle.y_pos)
        #     self.AnimWheatle.affiche(1000,0)
        # if( self.AnimJurassy.play ):
        #     #print("First ",AnimTest.speed)
        #     self.AnimJurassy.update(self.AnimJurassy.x_pos,self.AnimJurassy.y_pos)
        #     self.AnimJurassy.affiche(1000,250)

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
        self.fenetre = screen
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
            self.fenetre.blit(sprite, (x,y))
            self.play_count += 1

class Personnage:
    """
        Classe représentant un personnage.
    """
    def __init__(self, idJoueur):
        self.idJoueur = idJoueur


class Joueur(Personnage):
    """
        Classe représentant un Personnage Joueur.
    """
    def __init__(self):
        """
            Constructeur de la classe.
        """
        super().__init__(1)
        self.posSouris = (0,0)

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

class PNJ(Personnage):
    """
        Classe représentant un Personnage Non Joueur.
    """
    def __init__(self):
        super().__init__(2)
