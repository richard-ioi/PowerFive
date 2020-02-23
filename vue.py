#! /usr/bin/env python3

"""
    Module regroupant les vues du jeu.
"""

import pygame
import os
import time
import xml.etree.ElementTree as ET
from pygame.transform import scale

class Interface:
    """
        Classe constituant l'interface du jeu.
    """
    def __init__(self, fenetre, largeur, hauteur, grille, animBase, animSpec, mode, ennemi=None, musics=None, personnage=None):
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
        self.coordGrilleBack = ( self.largeur//2 - self.grille.dimSprites[0]//2, self.hauteur//2 - self.grille.dimSprites[1]//2 - 8 +29 )
        self.coordGrilleTop = ( self.largeur//2 - self.grille.dimSprites[0]//2 , self.hauteur//2 - self.grille.dimSprites[1]//2 +29 )
        self.rectColonne, self.rectList = self.InitRect()
        self.animBase = animBase
        self.animSpec = animSpec
        self.moteurJeu = None
        self.musics = musics

        self.tourJoueur = True
        self.jetonsPlaces = []
        self.lacherInfos = (0,0)
        self.lacher = False
        self.distance = 0
        self.plusOuMoins = -1
        self.tremble = 0
        self.yTremble = 0
        #self.imgSaloon = scale(pygame.image.load(os.path.join("data","graphismes","saloon.png")),(1280,720))

        self.plusOuMoins = 1
        self.tremble = 0
        self.yTremble = 0
        
        self.compteur=0
        self.texteFini=False
        self.texteFinal=""
        self.texteFinal2=""
        self.texteFinal3=""
        self.texteSuite=""
        self.dialogueFini=False

        self.compteurJeton=0
        self.reinitialise=False

        self.mode=mode
        self.ennemi = ennemi
        self.personnage = personnage

        self.background = scale(pygame.image.load(os.path.join("data","graphismes","saloon","saloon_clone.png")),(1278,720))
        self.tableAnimation = Animation(self.fenetre, os.path.join("table_animation.png"),0,32,4,True,428,17,None,3,True,0,669)
        #self.tableAnimation = Animation(self.fenetre, os.path.join("table_animation.png"),0,32,10,True,428,17,None,4,True,-213,631)

        self.scoreIA=0
        self.scoreJoueur=0

        self.dialogueIA=0

        self.panneauScore= scale(pygame.image.load(os.path.join("data","graphismes","scores","panneau_score.png")),(177,69))
        self.panneauIA = scale(pygame.image.load(os.path.join("data","graphismes","scores","IA0.png")),(180,180))
        self.panneauJoueur= scale(pygame.image.load(os.path.join("data","graphismes","scores","Joueur0.png")),(180,180))

        self.changementIA1 = Animation(self.fenetre, os.path.join("scores","changement_IA1.png"),0,18,2,True,43,45,None,4,True,1000,0)
        self.changementIA2 = Animation(self.fenetre, os.path.join("scores","changement_IA2.png"),0,18,2,True,43,45,None,4,True,1000,0)
        self.changementIA3 = Animation(self.fenetre, os.path.join("scores","changement_IA3.png"),0,18,2,True,43,45,None,4,True,1000,0)
        self.changementJoueur1 = Animation(self.fenetre, os.path.join("scores","changement_Joueur1.png"),0,18,2,True,43,45,None,4,True,100,0)
        self.changementJoueur2 = Animation(self.fenetre, os.path.join("scores","changement_Joueur2.png"),0,18,2,True,43,45,None,4,True,100,0)
        self.changementJoueur3 = Animation(self.fenetre, os.path.join("scores","changement_Joueur3.png"),0,18,2,True,43,45,None,4,True,100,0)

        self.changementIAFini=True
        self.changementJoueurFini=True


        self.flashOppacite = 0
        self.startFlash = False

        self.cadreTexte = scale(pygame.image.load(os.path.join("data","graphismes","cadre_texte.png")),(242,61*4))
        self.police = pygame.font.Font(None,20)

        self.regle1 = self.police.render("Vous devez battre votre adversaire",True,pygame.Color("#000000"))
        self.regle2 = self.police.render("en réalisant un alignement de 5",True,pygame.Color("#000000"))
        self.regle3 = self.police.render("pions jaune en ligne, colonne ou ",True,pygame.Color("#000000"))
        self.regle4 = self.police.render("diagonale.",True,pygame.Color("#000000"))

        self.regle5 = self.police.render("Attention le joueur adverse ne doit",True,pygame.Color("#000000"))
        self.regle6 = self.police.render("pas y parvenir avant vous !",True,pygame.Color("#000000"))

        self.regle7 = self.police.render("Votre barre de compétence se ",True,pygame.Color("#000000"))
        self.regle8 = self.police.render("remplit lorsque vous jouez un coup.",True,pygame.Color("#000000"))
        
        self.regle9 = self.police.render("Lorque la barre est remplie, appuyez",True,pygame.Color("#000000"))
        self.regle10 = self.police.render("sur le bouton ULTIMATE afin de",True,pygame.Color("#000000"))
        self.regle11 = self.police.render("déclancher votre compétence qui est",True,pygame.Color("#000000"))
        self.regle12 = self.police.render("d'inverser les couleurs au prochain",True,pygame.Color("#000000"))
        self.regle13 = self.police.render("coup ! ",True,pygame.Color("#000000"))
        

    def Reinitialiser(self):
        #On réinitialise la grille de jeu après 1sec
        time.sleep(2)
        self.tourJoueur = True
        self.grille.Reinitialiser()
        self.jetonsPlaces = []
        self.reinitialise=True

    def afficheTexte(self,idJoueur,aTexte):
        if idJoueur==1:
            img=scale(pygame.image.load(os.path.join("data","graphismes","speech_gauche.png")),(62*4,23*4))
            x=180
            y=400+29
        elif idJoueur==2:
            img=scale(pygame.image.load(os.path.join("data","graphismes","speech_droite.png")),(62*4,23*4))
            x=815
            y=400+29

        texteRendu = self.police.render(self.texteFinal,True,pygame.Color("#000000"))
        texteRendu2 = self.police.render(self.texteFinal2,True,pygame.Color("#000000"))
        texteRendu3 = self.police.render(self.texteFinal3,True,pygame.Color("#000000"))
        texteSuiteRendu = self.police.render(self.texteSuite,True,pygame.Color("#000000"))
        
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
                        self.texteSuite=""
                        self.texteFinal=""
                        self.texteFinal2=""
                        self.texteFinal3=""
                        self.texteFini=False

        elif self.compteur==len(aTexte):
            for event in pygame.event.get():
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        self.texteSuite=""
                        self.texteFinal=""
                        self.texteFinal2=""
                        self.texteFinal3=""
                        self.texteFini=False
                        self.dialogueFini=True
                        self.dialogueIA+=1
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
    

    def updateJetonsPlaces(self):
        """
            Méthode mettant à jour la liste des jetons à placé
        """
        temp = self.grille.CasesPleines()
        for elm in temp:
            xGrille, yGrille = elm[1], elm[2]
            case = self.rectList[xGrille + yGrille * 9]["rect"] # Pour (1,2) --> 1 + 2*9 = elm n°19
            xFenetre, yFenetre = case.center[0] - elm[0].sprite.get_width() // 2, case.y + 8
            if (elm[0], xFenetre, yFenetre) not in self.jetonsPlaces:
                self.jetonsPlaces.append( (elm[0], xFenetre, yFenetre) )

    
    def Affichage(self):
        """
            Méthode exécutant les procédure d'affichages sur l'écran
        """
        self.plusOuMoins *= -1
        if(self.tremble > 0): 
            self.yTremble = self.plusOuMoins * 2
            self.tremble -= 1
        else: self.yTremble = 0


        self.fenetre.blit(self.background,(0,0))
        self.fenetre.blit( self.grille.sprites["back"], (self.coordGrilleBack[0], self.coordGrilleBack[1]+self.yTremble) )
        #pygame.draw.rect(self.fenetre,(75,36,27),(0,680,1280,720))

        self.fenetre.blit(self.cadreTexte,(975,170))
        self.fenetre.blit(self.regle1,(982,180))
        self.fenetre.blit(self.regle2,(982,195))
        self.fenetre.blit(self.regle3,(982,210))
        self.fenetre.blit(self.regle4,(982,225))
        self.fenetre.blit(self.regle5,(982,250))
        self.fenetre.blit(self.regle6,(982,265))

        self.fenetre.blit(self.regle7,(982,280+10))
        self.fenetre.blit(self.regle8,(982,295+10))

        self.fenetre.blit(self.regle9,(982,310+20))
        self.fenetre.blit(self.regle10,(982,325+20))
        self.fenetre.blit(self.regle11,(982,340+20))
        self.fenetre.blit(self.regle12,(982,355+20))
        self.fenetre.blit(self.regle13,(982,370+20))

        self.fenetre.blit(self.panneauScore,(550,0))
        
        if(self.changementJoueurFini):
            self.fenetre.blit(self.panneauJoueur,(100,0))
        if(self.changementIAFini):
            self.fenetre.blit(self.panneauIA,(1000,0))

        if (self.changementIAFini==False):
            if (self.scoreIA==1):
                self.changementIA1.affiche(self.changementIA1.coordx,self.changementIA1.coordy)
                if(self.changementIA1.done): self.changementIAFini=True
            elif (self.scoreIA==2):
                self.changementIA2.affiche(self.changementIA2.coordx,self.changementIA2.coordy)
                if(self.changementIA2.done): self.changementIAFini=True
            elif (self.scoreIA==3):
                self.changementIA3.affiche(self.changementIA3.coordx,self.changementIA3.coordy)
                if(self.changementIA2.done): self.changementIAFini=True
        
        elif (self.changementJoueurFini==False):
            if (self.scoreJoueur==1):
                self.changementJoueur1.affiche(self.changementJoueur1.coordx,self.changementJoueur1.coordy)
                if(self.changementJoueur1.done): self.changementJoueurFini=True
            elif (self.scoreJoueur==2):
                self.changementJoueur2.affiche(self.changementJoueur2.coordx,self.changementJoueur2.coordy)
                if(self.changementJoueur2.done): self.changementJoueurFini=True
            elif (self.scoreJoueur==3):
                self.changementJoueur3.affiche(self.changementJoueur3.coordx,self.changementJoueur3.coordy)
                if(self.changementJoueur3.done): self.changementJoueurFini=True

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
            jeton.speed += jeton.acceleration
            self.distance += jeton.speed
            if( yJeton < derniereCaseY ):
                self.fenetre.blit(jeton.sprite, (colonneXCenter-jeton.sprite.get_width()//2, yJeton) )
            else:
                yJeton = derniereCaseY+2
                self.distance = 0
                self.updateJetonsPlaces()
                self.tourJoueur = not self.tourJoueur
                self.lacher = False
                self.tremble = 4
                gagnant = self.moteurJeu.Gagnant(jeton)
                if(gagnant != 0):
                    if (gagnant==1):
                        self.scoreJoueur+=1
                        self.dialogueIA=2
                        print("")
                        print("Vous gagnez un point !")
                        print("Score : "+str(self.scoreJoueur)+" - "+str(self.scoreIA))
                        print("")
                        self.changementJoueurFini=False
                        self.panneauJoueur = scale(pygame.image.load(os.path.join("data","graphismes","scores","Joueur"+str(self.scoreJoueur)+".png")),(180,180))

                    elif (gagnant==2):
                        self.scoreIA+=1
                        self.dialogueIA=1
                        print("")
                        print("Votre adversaire gagne un point !")
                        print("Score : "+str(self.scoreJoueur)+" - "+str(self.scoreIA))
                        print("")
                        self.changementIAFini=False
                        self.panneauIA = scale(pygame.image.load(os.path.join("data","graphismes","scores","IA"+str(self.scoreIA)+".png")),(180,180))

                    #if(self.changementJoueur1.done and self.changementJoueur2.done and self.changementJoueur3.done and self.changementIA1.done and self.changementIA2.done and self.changementIA3.done):
                    self.Reinitialiser()
                    self.reinitialise=False
        
        for jeton in self.jetonsPlaces:
            self.fenetre.blit(jeton[0].sprite, (jeton[1], jeton[2]))
    
        self.tableAnimation.affiche(self.tableAnimation.coordx,self.tableAnimation.coordy)

        self.fenetre.blit( self.grille.sprites["top"], (self.coordGrilleTop[0], self.coordGrilleTop[1]+self.yTremble) )

        self.animBase["sheriff"].play = True
        self.animBase[self.ennemi].play = True

        for animation in list(self.animBase.values()) + list(self.animSpec.values()):
            #if animation == self.animBase["Bouton"]: print(animation," ",animation.done)
            if animation.play:
                if self.animBase["Bouton"]:
                    animation.affiche(animation.coordx,animation.coordy,True)
                else:
                    animation.affiche(animation.coordx,animation.coordy)

        #self.FlashScreen()
        #self.fenetre.fill(pygame.Color(255,0,0,10))
        
    def FlashScreen(self, speed=50):
        if( self.startFlash ): 
            self.flashOppacite += speed
        else: self.flashOppacite -= speed
        if( self.flashOppacite <= 0 ): self.flashOppacite = 0
        elif( self.flashOppacite > 200 ): self.startFlash = False

    def AffichageSaloon(self, animSaloon):
        for animation in list (animSaloon.values()):
            if animation.play:
                animation.affiche(0,0)

    def AttentePlacement(self,posSouris,idJoueur,inverse=False):
        if(not self.lacher and (idJoueur == 1 or inverse)):
            if( self.coordGrilleBack[0] <= posSouris[0] and posSouris[0] <= self.coordGrilleBack[0]+self.grille.sprites["back"].get_width()  ):
                rectColonne = pygame.Rect(0,0,0,0)
                for rect in self.rectColonne:
                    if rect["rect"].collidepoint((posSouris[0]-5,posSouris[1])):
                        rectColonne = rect["rect"]
                        break
                if(idJoueur == 1): jetonSprite = scale( pygame.image.load( os.path.join("data","graphismes","jeton_jaune.png") ), (10*4,12*4) )
                else: jetonSprite = scale( pygame.image.load( os.path.join("data","graphismes","jeton_rouge.png") ), (10*4,12*4) )
                posXColonne = rectColonne.x + rectColonne.w - jetonSprite.get_width()//2-10
                self.fenetre.blit( jetonSprite, (posXColonne-jetonSprite.get_width()//2,17+29) )

    def lacherJeton(self, jeton, rectCase, coordCase):
        self.musics.playSound("Jetons",isRandom=True)
        self.lacher = True
        self.lacherInfos = (jeton,rectCase,coordCase)
    
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
    def __init__(self, screen, idJoueur, nomPerso, nbSprites, vitesseSprite, largeur, hauteur, x , y, ia=None):
        self.fenetre=screen
        self.idJoueur = idJoueur
        self.nomPerso = nomPerso
        self.dialogue = Dialogue("data/dialogues/saloon.xml").getDialogues(nomPerso)
        self.palette = os.path.join(nomPerso, "char.png")
        self.animation = Animation(self.fenetre, self.palette , 0, nbSprites, vitesseSprite, True, largeur, hauteur, None, 3, False, x, y)
        self.ia = ia


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