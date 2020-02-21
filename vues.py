#! /usr/bin/env python3

"""
    Module regroupant les vues du jeu.
"""

import pygame
import os
import time
import xml.etree.ElementTree as ET
from abc import ABCMeta, abstractmethod

class Interface(metaclass = ABCMeta):
    """
        Classe primaire d'interface du jeu
    """
    def __init__(self, fenetre, background, musics = None):
        """
            Constructeur de la classe.

            Args:
                fenetre: Fenêtre pygame
                background: arrière plan du l'interface
        """
        self.fenetre = fenetre
        self.largeur = fenetre.get_width()
        self.hauteur = fenetre.get_height()
        self.background = pygame.transform.scale(background, (1280, 720))
        self.musics = musics
    
    @abstractmethod
    def affiche(self):
        pass

class Bouton:
    """
        Classe définissant un bouton d'interface
    """
    def __init__(self, x, y, action, sprite):
        """
            Constructeur de la classe.

            Args:
                action: action réaliser par le bouton (nom d'une fonction)
        """
        self.x = x
        self.y = y
        modAction, funcAction = action.split(".", 1)
        self.action = getattr(modAction, funcAction)
        self.sprite = sprite

    def estClique(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                return self.sprite.get_rect().collindepoint(x, y)
    
    def faireAction(self):
        if self.estClique():
            self.action()


class InterfaceMenu(Interface):
    """
        Classe définissant l'interface du menu du jeu
    """
    def __init__(self, fenetre, background, boutons):
        """
            Constructeur de la classe.

            Args:
                fenetre; Fenêtre pygame
                background: arrière plan de l'interface
                bontons: ensemble des boutons du jeu
        """
    
    def affiche(self):
        pass

class InterfaceRPG(Interface):
    """
        Classe définissant l'interface RPG du jeu
    """
    def __init__(self, fenetre, background, animSaloon, musics = None):
        super().__init__(fenetre, background, musics)
        self.animSaloon = animSaloon
    
    def affiche(self):
        self.fenetre.blit(self.background, (0,0))
        
        for animation in animation.values():
            if animation.play:
                animation.affiche(0,0)


class InterfacePlateau(Interface):
    """
        Classe définissant l'interface de duel du jeu
    """
    def __init__(self, fenetre, background, grille, animBase, animSpec, ennemie, musics=None,):
        super().__init__(fenetre, background, musics)
        self.grille = grille
        self.coordGrilleAvant = ( self.largeur//2 - self.grille.dimSprites[0]//2 , self.hauteur//2 - self.grille.dimSprites[1]//2 )
        self.coordGrilleArriere = ( self.largeur//2 - self.grille.dimSprites[0]//2, self.hauteur//2 - self.grille.dimSprites[1]//2 - 8 )
        self.rectColonne, self.rectList = self.initRect()
        self.tremblement = 0
        self.coefTremblement = -1
        self.lacher = False
        self.infosLacher = None
        self.tourJoueur = True
        self.animBase, self.animSpec = animBase, animSpec
        self.ennemie = ennemie
    
    def affiche(self):
        self.trembler()

        self.fenetre.blit(self.background, (0,0))
        self.fenetre.blit( self.grille.sprites["arriere"], (self.coordGrilleArriere[0], self.coordGrilleArriere[1] + self.tremblement))

        if self.lacher:
            self.deplacementJeton()
        
        for case in self.grille.CasesPleines():
            self.fenetre.blit(case[0].sprite, (case[1], case[2]))
        
        self.fenetre.blit( self.grille.sprites["avant"], (self.coordGrilleAvant[0], self.coordGrilleAvant[1] + self.tremblement) )

        self.animBase["sheriff"].play = True
        self.animBase[self.ennemi].play = True

        for animation in list(self.animBase.values()) + list(self.animSpec.values()):
            #if animation == self.animBase["Bouton"]: print(animation," ",animation.done)
            if animation.play:
                if self.animBase["Bouton"]:
                    animation.affiche(animation.coordx,animation.coordy,True)
                else:
                    animation.affiche(animation.coordx,animation.coordy)

    def afficheTexte(self,idJoueur,aTexte):
        if idJoueur==1:
            img=scale(pygame.image.load(os.path.join("data","graphismes","speech_gauche.png")),(62*4,23*4))
            x=180
            y=400
        elif idJoueur==2:
            img=scale(pygame.image.load(os.path.join("data","graphismes","speech_droite.png")),(62*4,23*4))
            x=815
            y=400

        police = pygame.font.Font(None,20)
        texteRendu = police.render(self.texteFinal,True,pygame.Color("#000000"))
        texteRendu2 = police.render(self.texteFinal2,True,pygame.Color("#000000"))
        texteRendu3 = police.render(self.texteFinal3,True,pygame.Color("#000000"))
        texteSuiteRendu = police.render(self.texteSuite,True,pygame.Color("#000000"))
        
        if self.compteur!=len(aTexte):
            if (self.texteFini!=True):
                self.texteFini=False
                if(texteRendu.get_width()<=(62-9)*4):
                    self.texteFinal+=aTexte[self.compteur]
                elif((texteRendu.get_width()>=((62-9)*4)) and (texteRendu2.get_width()<(62-9)*4)):
                    if (aTexte[self.compteur]!=' ' and (texteRendu2.get_width()<5)):
                        self.texteFinal+="-"
                    self.texteFinal2+=aTexte[self.compteur]
                elif (texteRendu2.get_width()>=((62-9)*4) and texteRendu3.get_width()<(62-9)*4):
                    if (aTexte[self.compteur]!=' ' and (texteRendu3.get_width()<5)):
                        self.texteFinal2+="-"
                    self.texteFinal3+=aTexte[self.compteur]
                elif (texteRendu3.get_width()>=(62-9)*4):
                    self.texteSuite = "suite"
                    self.texteFini=True
                if (texteRendu3.get_width()<(62-9)*4):
                    self.compteur+=1

            elif (self.texteFini):
                for event in pygame.event.get():
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        print("ENTREE")
                        self.texteSuite=""
                        self.texteFinal=""
                        self.texteFinal2=""
                        self.texteFinal3=""
                        self.texteFini=False

        elif self.compteur==len(aTexte):
            for event in pygame.event.get():
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        print("ENTREE")
                        self.texteSuite=""
                        self.texteFinal=""
                        self.texteFinal2=""
                        self.texteFinal3=""
                        self.texteFini=False
                        self.dialogueFini=True
                        self.compteur=0
        """else:
            self.compteur=0
            self.texteSuite=""
            self.texteFinal=""
            self.texteFinal2=""
            self.texteFinal3="""""

        self.fenetre.blit(img, (x,y))
        self.fenetre.blit(texteRendu,(x+10,y+10))
        self.fenetre.blit(texteRendu2,(x+10,y+25))
        self.fenetre.blit(texteRendu3,(x+10,y+40))
        self.fenetre.blit(texteSuiteRendu,(x+(62-7)*4,y+55))

    def attentePlacement(self, posSouris, idJoueur):
        if(not self.lacher and idJoueur == 1):
            if( self.coordGrilleArriere[0] <= posSouris[0] and posSouris[0] <= self.coordGrilleArriere[0]+self.grille.sprites["arriere"].get_width()  ):
                rectColonne = pygame.Rect(0,0,0,0)
                for rect in self.rectColonne:
                    if rect["rect"].collidepoint((posSouris[0]-5,posSouris[1])):
                        rectColonne = rect["rect"]
                        break
                #if(idJoueur == 1): jetonSprite = scale( pygame.image.load( os.path.join("data","graphismes","jeton_jaune.png") ), (10*4,12*4) )
                #else: jetonSprite = scale( pygame.image.load( os.path.join("data","graphismes","jeton_rouge.png") ), (10*4,12*4) )
                jetonSprite = scale( pygame.image.load( os.path.join("data","graphismes","jeton_jaune.png") ), (10*4,12*4) )
                posXColonne = rectColonne.x + rectColonne.w - jetonSprite.get_width()//2-10
                self.fenetre.blit( jetonSprite, (posXColonne-jetonSprite.get_width()//2,17) )
    
    def lacherJeton(self, jeton, rectCase, coordCase):
        self.musics.playSound("Jeton", isRandom = True)
        self.lacher = True
        self.infosLacher = {"jeton": jeton, "case": rectCase, "coord": coordCase}
    
    def deplacementJeton(self):
        rectCol = None
        for rect in self.rectColonne:
            if rect["colonne"] == self.infosLacher["coord"][0]:
                rectCol = rect["rect"]
        centreLargeurColonne = rectCol.center[0]
        coordYCase = self.infosLacher["case"].y + 8
        coordYJeton = rectCol.y + 68 - 16 - self.infosLacher["jeton"].sprite.get_height() + self.distance
        self.infosLacher["jeton"].speed += self.infosLacher["jeton"].acceleration
        self.distance += jeton.speed
        if coordYJeton < coordYCase:
            self.fenetre.blit(self.infosLacher["jeton"].sprite, (centreLargeurColonne - self.infosLacher["jeton"].get_width // 2, coordYJeton))
        else:
            coordYJeton = coordYCase + 2
            self.distance = 0
            self.tourJoueur = not self.tourJoueur
            self.lacher = False
            gagnant = self.moteurJeur.gagnant(self.infosLacher["jeton"])
            if gagnant != 0:
                self.reinitialiser()
            self.trembler()

    def trembler(self, intensite = 4):
        self.coefTremblement *= -1
        if intensite > 0:
            self.tremblement = self.coefTremblement * 2
            self.tremblement -= 1
    
    def reinitialiser(self):
        #On réinitialise la grille de jeu après 1sec
        time.sleep(1)
        self.tourJoueur = True
        self.grille.Reinitialiser()
        self.reinitialise=True
        
    def initRect(self):
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
    def __init__(self, screen, palette, y_sprite1, nb_sprites, speed=1, loop=True, width=62, height=64, nextAnim=None, coeffAgrandir=3, playAtStart=False,coordx=0,coordy=0):
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
        self.coordx=coordx
        self.coordy=coordy
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

class Dialogue:
    """
        Classe représentant un dialogue
    """
    def __init__(self, fichier):
        self.fichier = fichier
        self.root = ET.parse(self.fichier).getroot()
    
    def getDialogues(self, nomPerso):
        dialogues = []
        for dial in self.root.find(f"./personnage[@nom='{nomPerso}']").getchildren():
            dialogues.append(dial.text.strip())
        return dialogues

class Personnage:
    """
        Classe représentant un personnage.
    """
    def __init__(self, screen, idJoueur, nomPerso, nbSprites, vitesseSprite, largeur, hauteur, x ,y):
        self.fenetre=screen
        self.idJoueur = idJoueur
        self.nomPerso = nomPerso
        self.dialogue = Dialogue("data/dialogues/saloon.xml").getDialogues(nomPerso)
        self.palette = os.path.join(nomPerso, "char.png")
        self.animation = Animation(self.fenetre, self.palette , 0, nbSprites, vitesseSprite, True, largeur, hauteur, None, 3, False,x,y)


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