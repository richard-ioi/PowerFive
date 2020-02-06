#! /usr/bin/env python3

"""
    Module regroupant les différentes structures de données du jeu.
"""

import pygame
import os
import random
from pygame.transform import scale

class Grille:
    """
        Classe permettant la manipulation de la grille du jeu et de son état.
    """
    def __init__(self):
        """
            Constructeur de la classe.
            
            Args:
                grilleAttente: Liste contenant les jetons en attente.
                grillePrincipal: Liste représentant la grille du jeu.
                largeur: Largeur de la grille.
                hauteur: Hauteur de la grille.
                image: Sprite de la grille de jeu.
                largeurImage: largeur du sprite.
                hauteurImage: hauteur du sprite.
        """
        """vide = Jeton(0)
        mur = Jeton(-1)
        self.grillePrincipal = [[None,None,None,None,None,None,None,None,mur],  #0
                                [None,None,None,None,None,None,None,None,mur],  #1
                                [None,None,None,None,None,None,None,None,mur],  #2
                                [None,None,None,None,None,None,None,None,mur],  #3
                                [None,None,None,None,None,None,None,None,mur],  #4
                                [None,None,None,None,None,None,None,None,mur],  #5
                                [None,None,None,None,None,None,None,None,mur],  #6
                                [None,None,None,None,None,None,None,None,mur],  #7
                                [None,None,None,None,None,None,None,None,mur]]  #8"""

                              #y 0 1 2 3 4 5 6 7  8     x
        self.grillePrincipal = [[0,0,0,0,0,0,0,0,-1],  #0
                                [0,0,0,0,0,0,0,0,-1],  #1
                                [0,0,0,0,0,0,0,0,-1],  #2
                                [0,0,0,0,0,0,0,0,-1],  #3
                                [0,0,0,0,0,0,0,0,-1],  #4
                                [0,0,0,0,0,0,0,0,-1],  #5
                                [0,0,0,0,0,0,0,0,-1],  #6
                                [0,0,0,0,0,0,0,0,-1],  #7
                                [0,0,0,0,0,0,0,0,-1]]  #8
        self.largeur = 9
        self.hauteur = 8
        self.sprites = { "top": scale(pygame.image.load(os.path.join("data","graphismes","grille.png")), (140*4,141*4)),
                         "back": scale(pygame.image.load(os.path.join("data","graphismes","grille_back.png")), (140*4,141*4)),
                         "ultimate1":scale(pygame.image.load(os.path.join("data","graphismes","ultimate","ultimate1.png")), (58*3,46*3)) }
        self.dimSprites = ( self.sprites["top"].get_width(), self.sprites["top"].get_height() )
        self.coupPossible = []

    def __str__(self):
        cases = [case for colonne in list(zip(*self.grillePrincipal)) for case in colonne]
        return """Grille(largeur={}, hauteur={})
 ___________________________________
| {} | {} | {} | {} | {} | {} | {} | {} | {} |
| {} | {} | {} | {} | {} | {} | {} | {} | {} |
| {} | {} | {} | {} | {} | {} | {} | {} | {} |
| {} | {} | {} | {} | {} | {} | {} | {} | {} |
| {} | {} | {} | {} | {} | {} | {} | {} | {} |
| {} | {} | {} | {} | {} | {} | {} | {} | {} |
| {} | {} | {} | {} | {} | {} | {} | {} | {} |
| {} | {} | {} | {} | {} | {} | {} | {} | {} |
 ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
        """.format(self.largeur, self.hauteur, *cases)

    
    def CasesVides(self):
        """
            Méthode donnant l'ensemble des cases vides disponible dans la grille.

            Return:
                Une liste de tuples contenant l'index des colonnes et des cases disponibles.
        """
        casesVides = []
        for colonne in range(len(self.grillePrincipal)):
            for case in range(self.hauteur, -1, -1):
                if(self.grillePrincipal[colonne][case] == 0):
                    casesVides.append( (colonne, case) )
                    break
        #self.coupPossible = casesVides
        return casesVides

    def CaseVideColonne(self, colonne, inv = True):
        """
            Méthode donnant l'ensemble des cases vides disponible dans la grille.

            Return:
                Une liste de tuples contenant l'index des colonnes et des cases disponibles.
        """
        if inv:
            for case in range(self.hauteur, -1, -1):
                if(self.grillePrincipal[colonne][case] == 0):
                    return case
        else:
            for case in range(0, self.hauteur + 1):
                if(self.grillePrincipal[colonne][case] != 0):
                    return case - 1
    
    def NbJetonColonne(self, colonne):
        """
            Méthode donnant le nombre de jetons dans la colonne donnée en paramètre.

            Args:
                colonne: Indice de la colonne à analyser.

            Return:
                Le nombre de jeton de la colonne
        """
        nbJeton = 0
        for jeton in colonne:
            if jeton != 0:
                nbJeton += 1
        return nbJeton
    
    def ColonnePleine(self, colonne):
        """
            Méthode booléenne indiquant si la colonne est pleine.

            Args:
                colonne : Indice de la colonne à analyser.
            
            Return:
                Un booléen
        """
        return self.NbJetonColonne(colonne) == self.hauteur+1

    def RemplirCase(self, colonne, idJoueur):
        """
            Méthode remplissant une case de la grille

            Arg:
                jeton: Jeton devant être placé dans la grille.
        """
        case = self.CasesVides()[colonne][1]
        self.grillePrincipal[colonne][case] = idJoueur
    
    def PurgerColonne(self, colonne):
        debut = self.CaseVideColonne(colonne, inv = False) + 1
        caseUtile = self.grillePrincipal[colonne][debut:]
        if 0 in caseUtile:
            while 0 in caseUtile:
                caseUtile.remove(0)
            nbZero = len(self.grillePrincipal[colonne]) - len(caseUtile)
            colonnePurgee = [0]
            colonnePurgee *= nbZero
            colonnePurgee += caseUtile
            self.grillePrincipal[colonne] = colonnePurgee[:]
        
    def InverserJeton(self):
        for i, colonne in enumerate(self.grillePrincipal):
            for j, case in enumerate(colonne):
                if case == 1:
                    self.grillePrincipal[i][j] = 2
                if case == 2:
                    self.grillePrincipal[i][j] = 1
    
    def EjecterDernierJeton(self, colonne):
        self.grillePrincipal[colonne] = [0] + self.grillePrincipal[colonne][:-2] + [-1]
    
    def EjecterJetonAleat(self):
        colonne = random.randrange(len(self.grillePrincipal))
        if self.hauteur - self.CaseVideColonne(colonne) > 1:
            case = random.randrange( self.CaseVideColonne(colonne) +1, self.hauteur  )
            self.grillePrincipal[colonne][case] = 0
        else:
            self.EjecterJetonAleat()
        self.PurgerColonne(colonne)
    
    def EjecterJetonsAleat(self, n = 2):
        for i, colonne in enumerate(self.grillePrincipal):
            k = random.randint(1, n)
            cases = random.choices(range(len(colonne) - 1), k=k)
            print(cases)
            for j in cases:
                self.grillePrincipal[i][j] = 0
            self.PurgerColonne(i)
    
    def MelangerJetons(self):
        random.shuffle(self.grillePrincipal)
        for colonne in range(len(self.grillePrincipal)):
            self.PurgerColonne(colonne)

class Jeton:
    """
        Classe représentant les jetons du jeu.
    """
    def __init__(self, idJoueur):
        """
            Constructeur de la classe.

            Args:
                col: colonne du jeton dans la grille
                case: case du jeton
                idJoueur: Identifiant du joueur
                image: Sprite du jeton
        """
        self.idJoueur = idJoueur
        self.x = 0
        self.y = 0
        self.sprite = scale( pygame.image.load( os.path.join("data","graphismes","jeton_jaune.png") ), (10*4,12*4) ) if idJoueur == 1 \
                     else scale( pygame.image.load( os.path.join("data","graphismes","jeton_rouge.png") ), (10*4,12*4) )
        self.speed = 2
        self.acceleration = 1.5
        self.visible = False
    
    def __str__(self):
        return str(self.idJoueur)
    
    def __repr__(self):
        return "Jeton({}, {})".format(self.idJoueur, self.visible)
    
    def deplacer(self, coord):
        pass

class ObjetAnimMultiple:
    """Classe ObjetAnimMultiple qui permet de gerer les differents etats, par exemple pour un bouton,
    notamment les changement d'animation avec updateCurrentAnim()"""

    def __init__(self,posX,posY,animList,listGlobale,name="Bouton"):
        self.posX = posX
        self.posY = posY
        self.animList = animList
        self.idAnim = 0
        self.currentAnim = self.animList[self.idAnim]
        self.name = name
        self.listGlobale = listGlobale
        self.listGlobale.update( {self.name:self.currentAnim} )
        self.clicked = False

    def Reinitialiser(self):
        for anim in self.animList:
            anim.Reinitialiser()
        self.idAnim = 0
        self.currentAnim = self.animList[self.idAnim]
        self.listGlobale.update( {self.name:self.currentAnim} )
        self.listGlobale[self.name].play = True
        self.clicked = False

    def selectAnim(self, indice):
        self.currentAnim = self.animList[indice]
        #self.currentAnim.creerRect(self.posX, self.posY)
        self.listGlobale.update( {self.name:self.currentAnim} )
        self.listGlobale[self.name].play = True

    def updateCurrentAnim(self, condition=True, conditions=None, indice=-1):
        #Update l'animation courante pour la suivante dans la liste d'animation, selon une condition en parametre
        if(self.idAnim >= len(self.animList)-1): self.idAnim = len(self.animList)-1
        else:
            if(conditions != None): condition = conditions[self.idAnim] # PROBLEME!!! Les conditions ne s'update pas !
            if( indice != -1 ):
                self.selectAnim(indice)
            if not self.currentAnim.isLoop :
                if condition and self.currentAnim.done:
                    self.idAnim += 1
            elif self.currentAnim.isLoop:
                if condition:
                    self.idAnim += 1
        self.currentAnim = self.animList[self.idAnim]
        self.listGlobale.update( {self.name:self.currentAnim} )
        self.listGlobale[self.name].play = True




"""if __name__ == "__main__":
    maGrille = Grille()
    monJeton = Jeton(1, 1)
    print(maGrille.CasesVides())
    print("(" + str(monJeton.colonne) + "," +  str(monJeton.case) + ")")
    maGrille.RemplirCase(monJeton)
    print(maGrille.CasesVides())
    print("(" + str(monJeton.colonne) + "," +  str(monJeton.case) + ")")
    print(str(maGrille))"""
