import pygame
import numpy as np

class MoteurJeu:
    def __init__(self):
        #self.joueur = Joueur()
        #self.ia = IA()
        self.grille = Grille()

    def Placer(self,jeton):
        self.grille.grille[jeton.x][jeton.y] = jeton.idJoueur
        print("Jeton placé en (",jeton.x,",",jeton.y,")")
    
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
                return jeton.idJoueur
        compteur = 0
        # Vérificaion ligne
        for elmL in range(self.grille.largeur):
            if( self.grille.grille[elmL][jeton.y] == jeton.idJoueur ):
                compteur += 1
            else:
                compteur = 0
            if compteur == 5:
                return jeton.idJoueur
        compteur = 0
        # Vérification diagonale 1
        dirX = 1
        dirY = 1
        for elmD1 in range(self.grille.hauteur):
            case = self.grille.grille[jeton.x + elmD1*dirX][jeton.y + elmD1*dirY]
            if(case == jeton.idJoueur):
                compteur += 1           #Tant que notre case est à l'id du joueur on augmente le compteur
            else:
                dirX = -1               #Si on a une case différente on change de direction de la diagonale
                dirY = -1
            if(compteur == 5):
                return jeton.idJoueur   #Si le compteur est a 5 le joueur id gagne
            elif(dirX == -1 and dirY == -1 and case != jeton.idJoueur):
                compteur = 0            #Si on a déjà changer de direction et qu'il y a une case différente le joueur ne gagne pas
                break
        compteur = 0
        dirX = 1
        dirY = -1
        for elmD2 in range(self.grille.hauteur):
            case = self.grille.grille[jeton.x + elmD2*dirX][jeton.y + elmD2*dirY]
            if(case == jeton.idJoueur):
                compteur += 1           #Tant que notre case est à l'id du joueur on augmente le compteur
            else:
                dirX = -1               #Si on a une case différente on change de direction de la diagonale
                dirY = 1
            if(compteur == 5):
                return jeton.idJoueur   #Si le compteur est a 5 le joueur id gagne
            elif(dirX == -1 and dirY == 1 and case != jeton.idJoueur):
                compteur = 0            #Si on a déjà changer de direction et qu'il y a une case différente le joueur ne gagne pas
                break

class Grille:
    def __init__(self):
        self.grille = [[0,0,0,0,0,0,0,1,-1],
                       [0,0,0,0,0,0,0,1,-1],
                       [0,0,0,0,0,0,0,0,-1],
                       [0,0,0,0,0,0,0,1,-1],
                       [0,0,0,0,0,0,0,1,-1],
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

class Jeton: 
    #Classe Jeton très temporaire juste pour tester le bon fonctionnement de MoteurJeu
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.idJoueur = 1


#Test des classes et de leurs méthodes
if __name__ == "__main__":
    Grille1 = Grille()
    Moteur1 = MoteurJeu()
    Jeton1 = Jeton(2,7)

    print("Coordonnées des cases vides: ",Grille1.CasesVides())
    Moteur1.Placer(Jeton1)
    print("Id du Joueur gagnant: ",Moteur1.Gagnant(Jeton1))
