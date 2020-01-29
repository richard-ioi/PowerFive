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
        self.sprites = { "top": scale(pygame.image.load(os.path.join("data","graphismes","grille.png")), (150*4,150*4)),
                         "back": scale(pygame.image.load(os.path.join("data","graphismes","grille_back.png")), (150*4,150*4)) }
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
                if(self.grillePrincipal[colonne][case] == 0):
                    casesVides.append( (colonne, case) )
                    break
        return casesVides
    
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
            if jeton == 1:
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
        return self.NbJetonColonne(colonne) == self.hauteur

    def RemplirCase(self, jeton):
        """
            Méthode remplissant une case de la grille

            Arg:
                jeton: Jeton devant être placé dans la grille.
        """
        case = self.CasesVides()[jeton.colonne][1]
        self.grillePrincipal[jeton.colonne][case] = jeton.idJoueur
        jeton.case = case - 1

class Jeton:
    """
        Classe représentant les jetons du jeu.
    """
    def __init__(self, colonne, idJoueur):
        """
            Constructeur de la classe.

            Args:
                col: colonne du jeton dans la grille
                case: case du jeton
                idJoueur: Identifiant du joueur
                image: Sprite du jeton
        """
        self.colonne = colonne
        self.case = 0
        self.idJoueur = idJoueur
        self.sprite = scale( pygame.image.load( os.path.join("data","graphismes","jeton_jaune.png") ), (32*4,32*4) )
        self.visible = False
    
    def __str__(self):
        return "Jeton({}, {}, {})".format(colonne,case,idJoueur)
    
    def deplacer(self, coord):
        pass


if __name__ == "__main__":
    maGrille = Grille()
    monJeton = Jeton(1, 1)
    print(maGrille.CasesVides())
    print("(" + str(monJeton.colonne) + "," +  str(monJeton.case) + ")")
    maGrille.RemplirCase(monJeton)
    print(maGrille.CasesVides())
    print("(" + str(monJeton.colonne) + "," +  str(monJeton.case) + ")")
    print(str(maGrille))