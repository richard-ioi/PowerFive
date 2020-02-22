#! /usr/bin/env python3

"""
    Module regroupant les différentes structures de données du jeu.
"""

import pygame
import os
import random
from pygame.transform import scale
import copy

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
        self.grilleSauvegarde = None
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
    
    def CasesPleines(self):
        jetonsPLaces = []
        for x, colonne in enumerate(self.grillePrincipal):
            for y, jeton in enumerate(colonne):
                if jeton == 1 or jeton == 2:
                    jetonsPLaces.append( (jeton, x, y) )
        return jetonsPLaces

        #return [(jeton, x, y) for y, colonne in enumerate(self.grillePrincipal) for x, jeton in enumerate(colonne) if jeton == 1 or jeton == 2]

    def EtatPlacement(self, x, y):

        # Récupération colonne
        colonne = []
        for elmC in range(0, self.hauteur, 1):
            colonne.append(self.grillePrincipal[x][elmC])

        # Récupération ligne
        ligne = []
        for elmL in range(self.largeur):
            ligne.append(self.grillePrincipal[elmL][y])

        ### Récupération diagonales
        diag0, diag1 = [], []
        diag0_s, diag1_s = {}, {}
        
        ## Diagonale \
        # Calcul case la plus à gauche
        if y >= x: # début sur |
            diag0_s["start"] = (0, y-x)
        if y < x: # début sur --
            diag0_s["start"] = (x-y, 0)

        # Calcul case la plus à droite
        if y <= x-1: # début sur |
            diag0_s["stop"] = ((self.largeur-1), (self.largeur -1) - (x-y))
        if y > x-1: # début sur --
            diag0_s["stop"] = ((self.hauteur-1) - (y-x), self.hauteur-1)

        ## Diagonale /
        # Calcul case la plus à gauche
        if x+y <= 6: # début sur |
            diag1_s["start"] = (0, y+x)
        if x+y > 6: # début sur --
            diag1_s["start"] = (x+y - (self.hauteur-1), self.hauteur -1)
        
        #Calcul case la plus à droite
        if x+y >= 8: # début sur |
            diag1_s["stop"] = ((self.largeur-1), x+y - self.hauteur)
        if x+y < 8: # début sur --
            diag1_s["stop"] = (x+y, 0)
        
        for elmD0 in range(diag0_s["stop"][0] - diag0_s["start"][0] + 1):
            #print(str(diag0_s["start"][0] + elmD0)+' '+str(diag0_s["start"][1] + elmD0))
            diag0.append(self.grillePrincipal[ diag0_s["start"][0] + elmD0 ][ diag0_s["start"][1] + elmD0 ])
        
        for elmD1 in range(diag1_s["stop"][0] - diag1_s["start"][0] + 1):
            diag1.append(self.grillePrincipal[ diag1_s["start"][0] + elmD1 ][ diag1_s["start"][1] - elmD1 ])
        
        return {"ligne" : ligne, "colonne": colonne, "diag1": diag0, "diag2": diag1}
            
    def ColonnePleine(self, colonne):
        """
            Méthode booléenne indiquant si la colonne est pleine.

            Args:
                colonne : Indice de la colonne à analyser.
            
            Return:
                Un booléen
        """
        return self.NbJetonColonne(colonne) == self.hauteur+1
    
    def SauvegarderGrille(self):
        copy.deepcopy(self.grillePrincipal, self.grilleSauvegarde)

    def RemplirCase(self, jeton, colonne):
        """
            Méthode remplissant une case de la grille

            Arg:
                jeton: Jeton devant être placé dans la grille.
        """
        self.SauvegarderGrille()
        case = self.CasesVides()[colonne][1]
        self.grillePrincipal[colonne][case] = jeton
    
    def PurgerColonne(self, colonne):
        """
            Méthode retirant les cases vides entre les jetons.

            Args:
                colonne: Indice de la colonne à purger
        """
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
        self.SauvegarderGrille()
        for i, colonne in enumerate(self.grillePrincipal):
            for j, case in enumerate(colonne):
                if case == 1:
                    self.grillePrincipal[i][j] = 2
                if case == 2:
                    self.grillePrincipal[i][j] = 1
    
    def EjecterDernierJeton(self, colonne):
        self.SauvegarderGrille()
        self.grillePrincipal[colonne] = [0] + self.grillePrincipal[colonne][:-2] + [-1]
    
    def EjecterJetonAleat(self):
        self.SauvegarderGrille()
        colonne = random.randrange(len(self.grillePrincipal))
        if self.hauteur - self.CaseVideColonne(colonne) > 1:
            case = random.randrange( self.CaseVideColonne(colonne) +1, self.hauteur  )
            self.grillePrincipal[colonne][case] = 0
        else:
            self.EjecterJetonAleat()
        self.PurgerColonne(colonne)
    
    def EjecterJetonsAleat(self, n = 2):
        self.SauvegarderGrille()
        for i, colonne in enumerate(self.grillePrincipal):
            k = random.randint(1, n)
            cases = random.choices(range(len(colonne) - 1), k=k)
            print(cases)
            for j in cases:
                self.grillePrincipal[i][j] = 0
            self.PurgerColonne(i)
    
    def MelangerJetons(self):
        self.SauvegarderGrille()
        random.shuffle(self.grillePrincipal)
        for colonne in range(len(self.grillePrincipal)):
            self.PurgerColonne(colonne)
    
    def Reinitialiser(self):
        self.grillePrincipal = [[0,0,0,0,0,0,0,0,-1],  #0
                                [0,0,0,0,0,0,0,0,-1],  #1
                                [0,0,0,0,0,0,0,0,-1],  #2
                                [0,0,0,0,0,0,0,0,-1],  #3
                                [0,0,0,0,0,0,0,0,-1],  #4
                                [0,0,0,0,0,0,0,0,-1],  #5
                                [0,0,0,0,0,0,0,0,-1],  #6
                                [0,0,0,0,0,0,0,0,-1],  #7
                                [0,0,0,0,0,0,0,0,-1]]  #8
        self.SauvegarderGrille()

class Jeton:
    """
        Classe représentant les jetons du jeu.
    """
    def __init__(self, idJoueur, x=0, y=0):
        """
            Constructeur de la classe.

            Args:
                col: colonne du jeton dans la grille
                case: case du jeton
                idJoueur: Identifiant du joueur
                image: Sprite du jeton
        """
        self.idJoueur = idJoueur
        self.x = x
        self.y = y
        self.sprite = scale( pygame.image.load( os.path.join("data","graphismes","jeton_jaune.png") ), (10*4,12*4) ) if idJoueur == 1 \
                     else scale( pygame.image.load( os.path.join("data","graphismes","jeton_rouge.png") ), (10*4,12*4) )
        self.speed = 2
        self.acceleration = 1.5
        self.visible = False
    
    def __str__(self):
        return str(self.idJoueur)
    
    def __repr__(self):
        return "Jeton({}, {})".format(self.idJoueur, self.visible)
    
    def __eq__(self, other):
        return self.idJoueur == other
    
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
        if (self.idAnim >= len(self.animList)-1 and condition and self.currentAnim.done and not self.currentAnim.isLoop):
            self.Reinitialiser()
        elif(self.idAnim >= len(self.animList)-1): 
            self.idAnim = len(self.animList)-1
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




if __name__ == "__main__":
    maGrille = Grille()
    monJeton = Jeton(1, 1)
    print(maGrille.CasesVides())
    print("(" + str(monJeton.x) + "," +  str(monJeton.y) + ")")
    maGrille.RemplirCase(monJeton, 2)
    print(maGrille.CasesVides())
    print("(" + str(monJeton.x) + "," +  str(monJeton.y) + ")")
    print(str(maGrille))
    print(maGrille.CasesPleines())
