#! /usr/bin/env python3

"""
    Module regroupant les différentes structures de données du jeu.
"""

import pygame
import os
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
                         "back": scale(pygame.image.load(os.path.join("data","graphismes","grille_back.png")), (140*4,141*4)) }
        self.dimSprites = ( self.sprites["top"].get_width(), self.sprites["top"].get_height() )

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
                if(self.grillePrincipal[colonne][case] == None):
                    casesVides.append( (colonne, case) )
                    break
        return casesVides

    def CaseVideColonne(self,colonne):
        """
            Méthode donnant l'ensemble des cases vides disponible dans la grille.

            Return:
                Une liste de tuples contenant l'index des colonnes et des cases disponibles.
        """
        for case in range(self.hauteur, -1, -1):
            if(self.grillePrincipal[colonne][case] == 0):
                return (colonne, case)
    
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
        self.grillePrincipal[colonne][case] = Jeton(idJoueur)

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