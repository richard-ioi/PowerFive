import pygame
import numpy as np

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
        for ligne in range(len(self.grille)):
            for elm in range(self.hauteur, -1, -1):
                if(self.grille[ligne][elm] == 0):
                    casesVides.append( (ligne, elm) )
                    break
        return casesVides


if __name__ == "__main__":
    Grille1 = Grille()
    print(Grille1.CasesVides())