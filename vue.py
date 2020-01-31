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
        self.coordGrilleBack = ( self.largeur//2 - self.grille.dimSprites[0]//2, self.hauteur//2 - self.grille.dimSprites[1]//2 - 8 )
        self.coordGrilleTop = ( self.largeur//2 - self.grille.dimSprites[0]//2 , self.hauteur//2 - self.grille.dimSprites[1]//2 )
        self.rectColonne, self.rectList = self.InitRect()
        self.animBase = animBase
        self.animSpec = animSpec

        self.tourJoueur = True
        self.jetonsPlaces = []
        self.lacherInfos = (0,0)
        self.lacher = False
        self.distance = 0
        self.ultimatetat = 0
    
    def Affichage(self):
        """
            Méthode exécutant les procédure d'affichages sur l'écran
        """
        self.fenetre.fill([255,255,255])
        self.fenetre.blit( self.grille.sprites["back"], self.coordGrilleBack )

        if(self.lacher):
            rectCol = None
            jeton = self.lacherInfos[0]
            rectCase = self.lacherInfos[1]
            coordCase = self.lacherInfos[2]
            for rectC in self.rectColonne:
                if rectC["colonne"] == coordCase[0]:
                    rectCol = rectC["rect"]
            colonneXCenter = rectCol.center[0]
            derniereCaseY = rectCase.y + 8
            yJeton = rectCol.y+68-16-jeton.sprite.get_height() + self.distance
            if( yJeton < derniereCaseY ):
                self.fenetre.blit(jeton.sprite, (colonneXCenter-jeton.sprite.get_width()//2, yJeton) )
            else:
                #self.rebondJeton(derniereCaseY+2,jeton)
                yJeton = derniereCaseY+2
                self.distance = 0
                self.jetonsPlaces.append((jeton,(colonneXCenter-jeton.sprite.get_width()//2,yJeton)))
                self.tourJoueur = not self.tourJoueur
                self.lacher = False
            jeton.speed += jeton.acceleration
            self.distance += jeton.speed

        for iJeton in self.jetonsPlaces:
            self.fenetre.blit(iJeton[0].sprite, iJeton[1] )

        self.fenetre.blit( self.grille.sprites["top"], self.coordGrilleTop )

        #if (self.ultimatetat==0):
            #self.fenetre.blit( self.grille.sprites["ultimate1"], (80,250))
        #elif (self.ultimatetat==1):
            #self.animBase["Ultimateboucle0"].play= True
        #elif (self.ultimatetat==2)

        #for animation in self.animBase.values():
            #animation.play = True

        self.animBase["Sheriff"].play = True
        self.animBase["Pingu"].play = True
        #self.animBase["Weasel"].play = True
        #self.animBase["Ultimatebouton"].play = True

        for animation in list(self.animBase.values()) + list(self.animSpec.values()):
            #if animation == self.animBase["Bouton"]: print(animation," ",animation.done)
            if animation.play:
                animation.update( animation.x_pos, animation.y_pos )
                if animation == self.animBase["Sheriff"]:
                    animation.affiche(50,720-64*3-50)
                if animation == self.animBase["Froggy"]:
                    animation.affiche(1000,520)
                if animation == self.animBase["Weasel"]:
                    animation.affiche(1000,20)
                if animation == self.animBase["Jurassy"]:
                    animation.affiche(1000,250)
                if animation == self.animBase["Pingu"]:
                    animation.affiche(1280-62*3-50,720-96*3-50)
                if animation == self.animBase["PinguBad"]:
                    animation.affiche(50,300)
                if animation == self.animBase["Bouton"]:
                    animation.affiche(80+5,250-10 , nouveauRect=True)
                #AnimSpec
                """if animation == self.animSpec["bouton"]:
                    animation.affiche(80+5,250-10 , nouveauRect=True)
                if animation == self.animSpec["bouton2"]:
                    animation.affiche(80+5,250-10 , nouveauRect=True)"""

    def AttentePlacement(self,posSouris,idJoueur):
        if(not self.lacher):
            if( self.coordGrilleBack[0] <= posSouris[0] and posSouris[0] <= self.coordGrilleBack[0]+self.grille.sprites["back"].get_width()  ):
                rectColonne = pygame.Rect(0,0,0,0)
                for rect in self.rectColonne:
                    if rect["rect"].collidepoint((posSouris[0]-5,posSouris[1])):
                        rectColonne = rect["rect"]
                        break
                if(idJoueur == 1): jetonSprite = scale( pygame.image.load( os.path.join("data","graphismes","jeton_jaune.png") ), (10*4,12*4) )
                else: jetonSprite = scale( pygame.image.load( os.path.join("data","graphismes","jeton_rouge.png") ), (10*4,12*4) )
                posXColonne = rectColonne.x + rectColonne.w - jetonSprite.get_width()//2-10
                self.fenetre.blit( jetonSprite, (posXColonne-jetonSprite.get_width()//2,17) )


    def lacherJeton(self, jeton, rectCase, coordCase):
        self.lacher = True
        self.lacherInfos = (jeton,rectCase,coordCase)

    """def rebondJeton(self, yMax, jeton):
        jeton.acceleration = -2
        jeton.speed = -1"""
    
    def InitRect(self):
        xGrille, yGrille = self.coordGrilleBack[0], self.coordGrilleBack[1]
        rectColonne = [
            {"colonne": 0,  "rect": pygame.Rect(xGrille + 10, yGrille - 68, 60, 612)},
            {"colonne": 1,  "rect": pygame.Rect(xGrille + 70, yGrille - 68, 60, 612)},
            {"colonne": 2,  "rect": pygame.Rect(xGrille + 130, yGrille - 68, 60, 612)},
            {"colonne": 3,  "rect": pygame.Rect(xGrille + 190, yGrille - 68, 60, 612)},
            {"colonne": 4,  "rect": pygame.Rect(xGrille + 250, yGrille - 68, 60, 612)},
            {"colonne": 5,  "rect": pygame.Rect(xGrille + 310, yGrille - 68, 60, 612)},
            {"colonne": 6,  "rect": pygame.Rect(xGrille + 370, yGrille - 68, 60, 612)},
            {"colonne": 7,  "rect": pygame.Rect(xGrille + 430, yGrille - 68, 60, 612)},
            {"colonne": 8,  "rect": pygame.Rect(xGrille + 490, yGrille - 68, 60, 612)},
        ]
        rectList = [
            {"coord":(0, 0),  "rect": pygame.Rect(xGrille + 10, yGrille + 18, 60, 68)},
            {"coord":(1, 0),  "rect": pygame.Rect(xGrille + 70, yGrille + 18, 60, 68)},
            {"coord":(2, 0),  "rect": pygame.Rect(xGrille + 130, yGrille + 18, 60, 68)},
            {"coord":(3, 0),  "rect": pygame.Rect(xGrille + 190, yGrille + 18, 60, 68)},
            {"coord":(4, 0),  "rect": pygame.Rect(xGrille + 250, yGrille + 18, 60, 68)},
            {"coord":(5, 0),  "rect": pygame.Rect(xGrille + 310, yGrille + 18, 60, 68)},
            {"coord":(6, 0),  "rect": pygame.Rect(xGrille + 370, yGrille + 18, 60, 68)},
            {"coord":(7, 0),  "rect": pygame.Rect(xGrille + 430, yGrille + 18, 60, 68)},
            {"coord":(8, 0),  "rect": pygame.Rect(xGrille + 490, yGrille + 18, 60, 68)},
            {"coord":(0, 1),  "rect": pygame.Rect(xGrille + 10, yGrille + 86, 60, 68)},
            {"coord":(1, 1),  "rect": pygame.Rect(xGrille + 70, yGrille + 86, 60, 68)},
            {"coord":(2, 1),  "rect": pygame.Rect(xGrille + 130, yGrille + 86, 60, 68)},
            {"coord":(3, 1),  "rect": pygame.Rect(xGrille + 190, yGrille + 86, 60, 68)},
            {"coord":(4, 1),  "rect": pygame.Rect(xGrille + 250, yGrille + 86, 60, 68)},
            {"coord":(5, 1),  "rect": pygame.Rect(xGrille + 310, yGrille + 86, 60, 68)},
            {"coord":(6, 1),  "rect": pygame.Rect(xGrille + 370, yGrille + 86, 60, 68)},
            {"coord":(7, 1),  "rect": pygame.Rect(xGrille + 430, yGrille + 86, 60, 68)},
            {"coord":(8, 1),  "rect": pygame.Rect(xGrille + 490, yGrille + 86, 60, 68)},
            {"coord":(0, 2),  "rect": pygame.Rect(xGrille + 10, yGrille + 154, 60, 68)},
            {"coord":(1, 2),  "rect": pygame.Rect(xGrille + 70, yGrille + 154, 60, 68)},
            {"coord":(2, 2),  "rect": pygame.Rect(xGrille + 130, yGrille + 154, 60, 68)},
            {"coord":(3, 2),  "rect": pygame.Rect(xGrille + 190, yGrille + 154, 60, 68)},
            {"coord":(4, 2),  "rect": pygame.Rect(xGrille + 250, yGrille + 154, 60, 68)},
            {"coord":(5, 2),  "rect": pygame.Rect(xGrille + 310, yGrille + 154, 60, 68)},
            {"coord":(6, 2),  "rect": pygame.Rect(xGrille + 370, yGrille + 154, 60, 68)},
            {"coord":(7, 2),  "rect": pygame.Rect(xGrille + 430, yGrille + 154, 60, 68)},
            {"coord":(8, 2),  "rect": pygame.Rect(xGrille + 490, yGrille + 154, 60, 68)},
            {"coord":(0, 3),  "rect": pygame.Rect(xGrille + 10, yGrille + 222, 60, 68)},
            {"coord":(1, 3),  "rect": pygame.Rect(xGrille + 70, yGrille + 222, 60, 68)},
            {"coord":(2, 3),  "rect": pygame.Rect(xGrille + 130, yGrille + 222, 60, 68)},
            {"coord":(3, 3),  "rect": pygame.Rect(xGrille + 190, yGrille + 222, 60, 68)},
            {"coord":(4, 3),  "rect": pygame.Rect(xGrille + 250, yGrille + 222, 60, 68)},
            {"coord":(5, 3),  "rect": pygame.Rect(xGrille + 310, yGrille + 222, 60, 68)},
            {"coord":(6, 3),  "rect": pygame.Rect(xGrille + 370, yGrille + 222, 60, 68)},
            {"coord":(7, 3),  "rect": pygame.Rect(xGrille + 430, yGrille + 222, 60, 68)},
            {"coord":(8, 3),  "rect": pygame.Rect(xGrille + 490, yGrille + 222, 60, 68)},
            {"coord":(0, 4),  "rect": pygame.Rect(xGrille + 10, yGrille + 290, 60, 68)},
            {"coord":(1, 4),  "rect": pygame.Rect(xGrille + 70, yGrille + 290, 60, 68)},
            {"coord":(2, 4),  "rect": pygame.Rect(xGrille + 130, yGrille + 290, 60, 68)},
            {"coord":(3, 4),  "rect": pygame.Rect(xGrille + 190, yGrille + 290, 60, 68)},
            {"coord":(4, 4),  "rect": pygame.Rect(xGrille + 250, yGrille + 290, 60, 68)},
            {"coord":(5, 4),  "rect": pygame.Rect(xGrille + 310, yGrille + 290, 60, 68)},
            {"coord":(6, 4),  "rect": pygame.Rect(xGrille + 370, yGrille + 290, 60, 68)},
            {"coord":(7, 4),  "rect": pygame.Rect(xGrille + 430, yGrille + 290, 60, 68)},
            {"coord":(8, 4),  "rect": pygame.Rect(xGrille + 490, yGrille + 290, 60, 68)},
            {"coord":(0, 5),  "rect": pygame.Rect(xGrille + 10, yGrille + 358, 60, 68)},
            {"coord":(1, 5),  "rect": pygame.Rect(xGrille + 70, yGrille + 358, 60, 68)},
            {"coord":(2, 5),  "rect": pygame.Rect(xGrille + 130, yGrille + 358, 60, 68)},
            {"coord":(3, 5),  "rect": pygame.Rect(xGrille + 190, yGrille + 358, 60, 68)},
            {"coord":(4, 5),  "rect": pygame.Rect(xGrille + 250, yGrille + 358, 60, 68)},
            {"coord":(5, 5),  "rect": pygame.Rect(xGrille + 310, yGrille + 358, 60, 68)},
            {"coord":(6, 5),  "rect": pygame.Rect(xGrille + 370, yGrille + 358, 60, 68)},
            {"coord":(7, 5),  "rect": pygame.Rect(xGrille + 430, yGrille + 358, 60, 68)},
            {"coord":(8, 5),  "rect": pygame.Rect(xGrille + 490, yGrille + 358, 60, 68)},
            {"coord":(0, 6),  "rect": pygame.Rect(xGrille + 10, yGrille + 426, 60, 68)},
            {"coord":(1, 6),  "rect": pygame.Rect(xGrille + 70, yGrille + 426, 60, 68)},
            {"coord":(2, 6),  "rect": pygame.Rect(xGrille + 130, yGrille + 426, 60, 68)},
            {"coord":(3, 6),  "rect": pygame.Rect(xGrille + 190, yGrille + 426, 60, 68)},
            {"coord":(4, 6),  "rect": pygame.Rect(xGrille + 250, yGrille + 426, 60, 68)},
            {"coord":(5, 6),  "rect": pygame.Rect(xGrille + 310, yGrille + 426, 60, 68)},
            {"coord":(6, 6),  "rect": pygame.Rect(xGrille + 370, yGrille + 426, 60, 68)},
            {"coord":(7, 6),  "rect": pygame.Rect(xGrille + 430, yGrille + 426, 60, 68)},
            {"coord":(8, 6),  "rect": pygame.Rect(xGrille + 490, yGrille + 426, 60, 68)},
            {"coord":(0, 7),  "rect": pygame.Rect(xGrille + 10, yGrille + 494, 60, 68)},
            {"coord":(1, 7),  "rect": pygame.Rect(xGrille + 70, yGrille + 494, 60, 68)},
            {"coord":(2, 7),  "rect": pygame.Rect(xGrille + 130, yGrille + 494, 60, 68)},
            {"coord":(3, 7),  "rect": pygame.Rect(xGrille + 190, yGrille + 494, 60, 68)},
            {"coord":(4, 7),  "rect": pygame.Rect(xGrille + 250, yGrille + 494, 60, 68)},
            {"coord":(5, 7),  "rect": pygame.Rect(xGrille + 310, yGrille + 494, 60, 68)},
            {"coord":(6, 7),  "rect": pygame.Rect(xGrille + 370, yGrille + 494, 60, 68)},
            {"coord":(7, 7),  "rect": pygame.Rect(xGrille + 430, yGrille + 494, 60, 68)},
            {"coord":(8, 7),  "rect": pygame.Rect(xGrille + 490, yGrille + 494, 60, 68)}
        ]
        return rectColonne, rectList

class Animation:
    """
        Classe définissant les animations du jeu.
    """
    def __init__(self, screen, palette, y_sprite1, nb_sprites, speed=1, loop=True, width=62, height=64, nextAnim=None, coeffAgrandir=3, playAtStart=False):
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
        self.coeffAgrandir = coeffAgrandir
        self.playAtStart = playAtStart
        self.play = self.playAtStart
        self.play_count = 0
        self.update(self.x_pos,self.y_pos)
        self.rect = None
        self.done = False
        self.nextAnim = nextAnim

    def Reinitialiser(self):
        self.x_pos = 2
        self.play_count = 0
        self.done = False
        self.play = self.playAtStart

    def creerRect(self, x, y):
        self.rect = pygame.Rect(x, y, self.larg_sprite*self.coeffAgrandir, self.haut_sprite*self.coeffAgrandir)

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
            sprite = scale(sprite, (self.larg_sprite*self.coeffAgrandir,self.haut_sprite*self.coeffAgrandir))
            self.sprite_list.append(sprite)

    def affiche(self, x, y, nouveauRect=False):
        """
            Méhode affichant l'animation.

            Args:
                x:
                y: 
        """
        if nouveauRect:
            #Si on le demande on cree un Rect correspondant à l'image affichée
            self.creerRect(x,y)

        if self.play_count >= self.nb_sprites * self.speed:
            if self.isLoop:
                self.play_count = 0
            else:
                self.done = True
                self.play_count = 0
                self.play = False
                if(self.nextAnim != None): 
                    self.nextAnim.play = True
                    #self.nextAnim.affiche(x,y-200)
                    print("Affiche nextAnim")
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
