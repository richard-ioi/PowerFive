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
        self.coordGrilleBack = ( self.largeur//2 - self.grille.dimSprites[0]//2 - 8, self.hauteur//2 - self.grille.dimSprites[1]//2 - 8 )
        self.coordGrilleTop = ( self.largeur//2 - self.grille.dimSprites[0]//2 , self.hauteur//2 - self.grille.dimSprites[1]//2 )
        self.rectList = self.InitRect(self.coordGrilleBack)
        self.animBase = animBase
        self.animSpec = animSpec
    
    def Affichage(self):
        """
            Méthode exécutant les procédure d'affichages sur l'écran
        """
        self.fenetre.fill([255,255,255])
        self.fenetre.blit( self.grille.sprites["back"], self.coordGrilleBack )
        self.fenetre.blit( self.grille.sprites["top"], self.coordGrilleTop )
        
        #!! rectList a ajouter

        #for animation in self.animBase.values():
            #animation.play = True

        self.animBase["Sheriff"].play = True
        self.animBase["Pingu"].play = True

        for animation in list(self.animBase.values()) + list(self.animSpec.values()):
            #print(animation.play)
            if animation.play:
                animation.update( animation.x_pos, animation.y_pos )
                if animation == self.animBase["Sheriff"]:
                    animation.affiche(50,720-64*3-50)
                if animation == self.animBase["Froggy"]:
                    animation.affiche(1000,520)
                if animation == self.animBase["Weasel"]:
                    animation.affiche(1000,0)
                if animation == self.animBase["Jurassy"]:
                    animation.affiche(1000,250)
                if animation == self.animBase["Pingu"]:
                    animation.affiche(1280-62*3-50,720-96*3-50)
                if animation == self.animBase["PinguBad"]:
                    animation.affiche(50,300)

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

    def InitRect(self, coordGrille):
        #Rect pour les cases de la grille
        xGrille = coordGrille[0]
        yGrille = coordGrille[1]
        rectList = [
            {"coord":(0, 0),  "rect": pygame.Rect(xGrille+10, yGrille+18, 60, 68)},
            {"coord":(1, 0),  "rect": pygame.Rect(70, 18, 60, 68)},
            {"coord":(2, 0),  "rect": pygame.Rect(130, 18, 60, 68)},
            {"coord":(3, 0),  "rect": pygame.Rect(190, 18, 60, 68)},
            {"coord":(4, 0),  "rect": pygame.Rect(250, 18, 60, 68)},
            {"coord":(5, 0),  "rect": pygame.Rect(310, 18, 60, 68)},
            {"coord":(6, 0),  "rect": pygame.Rect(370, 18, 60, 68)},
            {"coord":(7, 0),  "rect": pygame.Rect(430, 18, 60, 68)},
            {"coord":(8, 0),  "rect": pygame.Rect(490, 18, 60, 68)},
            {"coord":(0, 1),  "rect": pygame.Rect(10, 86, 60, 68)},
            {"coord":(1, 1),  "rect": pygame.Rect(70, 86, 60, 68)},
            {"coord":(2, 1),  "rect": pygame.Rect(130, 86, 60, 68)},
            {"coord":(3, 1),  "rect": pygame.Rect(190, 86, 60, 68)},
            {"coord":(4, 1),  "rect": pygame.Rect(250, 86, 60, 68)},
            {"coord":(5, 1),  "rect": pygame.Rect(310, 86, 60, 68)},
            {"coord":(6, 1),  "rect": pygame.Rect(370, 86, 60, 68)},
            {"coord":(7, 1),  "rect": pygame.Rect(430, 86, 60, 68)},
            {"coord":(8, 1),  "rect": pygame.Rect(490, 86, 60, 68)},
            {"coord":(0, 2),  "rect": pygame.Rect(10, 154, 60, 68)},
            {"coord":(1, 2),  "rect": pygame.Rect(70, 154, 60, 68)},
            {"coord":(2, 2),  "rect": pygame.Rect(130, 154, 60, 68)},
            {"coord":(3, 2),  "rect": pygame.Rect(190, 154, 60, 68)},
            {"coord":(4, 2),  "rect": pygame.Rect(250, 154, 60, 68)},
            {"coord":(5, 2),  "rect": pygame.Rect(310, 154, 60, 68)},
            {"coord":(6, 2),  "rect": pygame.Rect(370, 154, 60, 68)},
            {"coord":(7, 2),  "rect": pygame.Rect(430, 154, 60, 68)},
            {"coord":(8, 2),  "rect": pygame.Rect(490, 154, 60, 68)},
            {"coord":(0, 3),  "rect": pygame.Rect(10, 222, 60, 68)},
            {"coord":(1, 3),  "rect": pygame.Rect(70, 222, 60, 68)},
            {"coord":(2, 3),  "rect": pygame.Rect(130, 222, 60, 68)},
            {"coord":(3, 3),  "rect": pygame.Rect(190, 222, 60, 68)},
            {"coord":(4, 3),  "rect": pygame.Rect(250, 222, 60, 68)},
            {"coord":(5, 3),  "rect": pygame.Rect(310, 222, 60, 68)},
            {"coord":(6, 3),  "rect": pygame.Rect(370, 222, 60, 68)},
            {"coord":(7, 3),  "rect": pygame.Rect(430, 222, 60, 68)},
            {"coord":(8, 3),  "rect": pygame.Rect(490, 222, 60, 68)},
            {"coord":(0, 4),  "rect": pygame.Rect(10, 290, 60, 68)},
            {"coord":(1, 4),  "rect": pygame.Rect(70, 290, 60, 68)},
            {"coord":(2, 4),  "rect": pygame.Rect(130, 290, 60, 68)},
            {"coord":(3, 4),  "rect": pygame.Rect(190, 290, 60, 68)},
            {"coord":(4, 4),  "rect": pygame.Rect(250, 290, 60, 68)},
            {"coord":(5, 4),  "rect": pygame.Rect(310, 290, 60, 68)},
            {"coord":(6, 4),  "rect": pygame.Rect(370, 290, 60, 68)},
            {"coord":(7, 4),  "rect": pygame.Rect(430, 290, 60, 68)},
            {"coord":(8, 4),  "rect": pygame.Rect(490, 290, 60, 68)},
            {"coord":(0, 5),  "rect": pygame.Rect(10, 358, 60, 68)},
            {"coord":(1, 5),  "rect": pygame.Rect(70, 358, 60, 68)},
            {"coord":(2, 5),  "rect": pygame.Rect(130, 358, 60, 68)},
            {"coord":(3, 5),  "rect": pygame.Rect(190, 358, 60, 68)},
            {"coord":(4, 5),  "rect": pygame.Rect(250, 358, 60, 68)},
            {"coord":(5, 5),  "rect": pygame.Rect(310, 358, 60, 68)},
            {"coord":(6, 5),  "rect": pygame.Rect(370, 358, 60, 68)},
            {"coord":(7, 5),  "rect": pygame.Rect(430, 358, 60, 68)},
            {"coord":(8, 5),  "rect": pygame.Rect(490, 358, 60, 68)},
            {"coord":(0, 6),  "rect": pygame.Rect(10, 426, 60, 68)},
            {"coord":(1, 6),  "rect": pygame.Rect(70, 426, 60, 68)},
            {"coord":(2, 6),  "rect": pygame.Rect(130, 426, 60, 68)},
            {"coord":(3, 6),  "rect": pygame.Rect(190, 426, 60, 68)},
            {"coord":(4, 6),  "rect": pygame.Rect(250, 426, 60, 68)},
            {"coord":(5, 6),  "rect": pygame.Rect(310, 426, 60, 68)},
            {"coord":(6, 6),  "rect": pygame.Rect(370, 426, 60, 68)},
            {"coord":(7, 6),  "rect": pygame.Rect(430, 426, 60, 68)},
            {"coord":(8, 6),  "rect": pygame.Rect(490, 426, 60, 68)},
            {"coord":(0, 7),  "rect": pygame.Rect(10, 494, 60, 68)},
            {"coord":(1, 7),  "rect": pygame.Rect(70, 494, 60, 68)},
            {"coord":(2, 7),  "rect": pygame.Rect(130, 494, 60, 68)},
            {"coord":(3, 7),  "rect": pygame.Rect(190, 494, 60, 68)},
            {"coord":(4, 7),  "rect": pygame.Rect(250, 494, 60, 68)},
            {"coord":(5, 7),  "rect": pygame.Rect(310, 494, 60, 68)},
            {"coord":(6, 7),  "rect": pygame.Rect(370, 494, 60, 68)},
            {"coord":(7, 7),  "rect": pygame.Rect(430, 494, 60, 68)},
            {"coord":(8, 7),  "rect": pygame.Rect(490, 494, 60, 68)}
        ]
        return rectList

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
