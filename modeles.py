import pygame
import os
from pygame.transform import scale

class Grille:
    def __init__(self):
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
        casesVides = []
        for colonne in range(len(self.grillePrincipal)):
            for elm in range(self.hauteur, -1, -1):
                if(self.grillePrincipal[colonne][elm] == 0):
                    casesVides.append( (colonne, elm) )
                    break
        return casesVides
    
    def NbJetonColonne(self,colonne):
        nbJeton = 0
        for jeton in colonne:
            if jeton == 1:
                nbJeton += 1
        return nbJeton
    
    def ColonnePleine(self,colonne):
        return NbJetonColonne == self.hauteur

class Jeton: 
    def __init__(self, x, y, idJ):
        self.x = x
        self.y = y
        self.idJoueur = idJ
        self.image = 0