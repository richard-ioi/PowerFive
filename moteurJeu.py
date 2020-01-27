import pygame
import numpy as np

class MoteurJeu:
    def __init__(self):
        self.joueur = Joueur()
        self.ia = IA()
        self.grille = Grille()
    
    def Gagnant(self, jeton):
        compteur = 0
        # Vérification colonne
        for elmC in range(jeton.y, self.grille.hauteur, 1):
            if( self.grille.grille[jeton.x][elmC] == jeton.idJoueur ):
                compteur += 1
            else:
                compteur = 0
                break
            if compteur == 5:
                return idJoueur
        compteur = 0
        # Vérificaion ligne
        for elmL in range(self.grille.largeur):
            if( self.grille.grille[elmL][jeton.y] == jeton.idJoueur ):
                compteur += 1
            else:
                compteur = 0
            if compteur == 5:
                return idJoueur
        #Vérification diagonale


class Grille:
    def __init__(self):
        self.grille = [[0,0,0,0,0,0,0,0,-1],
                       [0,0,0,0,0,0,0,0,-1],
                       [0,0,0,0,0,0,0,0,-1],
                       [0,0,0,0,0,0,0,0,-1],
                       [0,0,0,0,0,0,0,0,-1],
                       [0,0,0,0,0,0,0,0,-1],
                       [0,0,0,0,0,0,0,0,-1],
                       [0,0,0,0,0,0,0,0,-1],
                       [0,0,0,0,0,0,0,0,-1]]
        self.largeur = 9
        self.hauteur = 8

    def CasesVides(self):
        casesVides = []
        for colonne in range(len(self.grille)):
            for elm in range(self.hauteur, -1, -1):
                if(self.grille[colonne][elm] == 0):
                    casesVides.append( (colonne, elm) )
                    break
        return casesVides


if __name__ == "__main__":
    Grille1 = Grille()
    print(Grille1.CasesVides())
