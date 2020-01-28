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
                                     #x
        self.grilleAttente = [ [0],  #0
                               [0],  #1
                               [0],  #2
                               [0],  #3
                               [0],  #4
                               [0],  #5
                               [0],  #6
                               [0],  #7
                               [0] ] #8
                             #y  0 1 2 3 4 5 6 7  8     x
        self.grillePrincipal = [[0,0,0,0,0,0,0,0,-1],  #0
                                [0,0,0,0,0,0,0,0,-1],  #1
                                [0,0,0,0,0,0,0,0,-1],  #2
                                [0,0,0,0,0,0,0,0,-1],  #3
                                [0,0,0,0,0,0,0,0,-1],  #4
                                [0,0,0,0,0,0,0,0,-1],  #5
                                [0,0,0,0,0,0,0,0,-1],  #6
                                [0,0,0,0,1,1,1,1,-1],  #7
                                [0,0,0,0,0,0,0,0,-1]]  #8
        self.largeur = 9
        self.hauteur = 8
        self.image = scale(pygame.image.load(os.path.join("data","graphismes","grille.png")), (150*4,150*4))
        self.imageBack = scale(pygame.image.load(os.path.join("data","graphismes","grille_back.png")), (150*4,150*4))
        self.largeurImage = self.image.get_width()
        self.hauteurImage = self.image.get_height()

    def CasesVides(self):
        """
            Méthode donnant l'ensemble des cases vides disponible dans la grille.

            Return:
                Une liste de tuples contenant la la colonne et le contenue de la case.
        """
        casesVides = []
        for colonne in range(len(self.grillePrincipal)):
            for elm in range(self.hauteur, -1, -1):
                if(self.grillePrincipal[colonne][elm] == 0):
                    casesVides.append( (colonne, elm) )
                    break
        return casesVides
    
    def NbJetonColonne(self,colonne):
        """
            Méthode donnant le nombre de jetons dans la colonne donnée en paramètre.

            Args:
                colonne: Indice de la colonne à analyser.

            Return:
                Le nombre de jeton de la colonne
        """
        nbJeton = 0
        for jeton in colonne:
            if jeton == 1:
                nbJeton += 1
        return nbJeton
    
    def ColonnePleine(self,colonne):
        """
            Méthode booléenne indiquant si la colonne est pleine.

            Args:
                colonne : Indice de la colonne à analyser.
            
            Return:
                Un booléen
        """
        return NbJetonColonne == self.hauteur

class Jeton:
    """
        Classe représentant les jetons du jeu.
    """
    def __init__(self, x, y, idJ):
        """
            Constructeur de la classe.

            Args:
                x: coordonnée horizontale du jeton
                y: coordonnée verticale du jeton
                idJoueur: Identifiant du joueur
                image: Sprite du jeton
        """
        self.x = x
        self.y = y
        self.idJoueur = idJ
        self.image = 0