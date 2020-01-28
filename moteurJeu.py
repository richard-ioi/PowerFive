import pygame
import time
import numpy as np

class MoteurJeu:
    def __init__(self):
        #self.joueur = Joueur()
        #self.ia = IA()
        self.grille = Grille()

    def Placer(self,jeton):
        if not self.grille.ColonnePleine():
            pass

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
        compteur1 = 0
        compteur2 = 0
        # Vérification diagonale 1
        for elmD1 in range(self.grille.hauteur):
            print(elmD1)
            try: caseDiag1 = self.grille.grille[jeton.x + elmD1][jeton.y + elmD1]
            except IndexError: pass
            try: caseDiag2 = self.grille.grille[jeton.x - elmD1][jeton.y + elmD1]
            except IndexError: pass
            if(caseDiag1 == jeton.idJoueur):
                compteur1 += 1           #Tant que notre case est à l'id du joueur on augmente le compteur
            if(caseDiag2 == jeton.idJoueur):
                compteur2 += 1           #Tant que notre case est à l'id du joueur on augmente le compteur
            if(compteur1 == 5 or compteur2 == 5):
                return jeton.idJoueur   #Si le compteur est a 5 le joueur id gagne
            elif(caseDiag1 != jeton.idJoueur and caseDiag2 != jeton.idJoueur):
                print("STOP")    #Si on a déjà changer de direction et qu'il y a une case différente le joueur ne gagne pas
                break
        print("###")
        compteur1 -= 1
        compteur2 -= 1
        for elmD2 in range(self.grille.hauteur):
            try: caseDiag1 = self.grille.grille[jeton.x - elmD2][jeton.y - elmD2]
            except IndexError: pass
            try: caseDiag2 = self.grille.grille[jeton.x + elmD2][jeton.y - elmD2]
            except IndexError: pass
            if(caseDiag1 == jeton.idJoueur):
                compteur1 += 1           #Tant que notre case est à l'id du joueur on augmente le compteur
            if(caseDiag2 == jeton.idJoueur):
                compteur2 += 1           #Tant que notre case est à l'id du joueur on augmente le compteur
            if(compteur1 == 5 or compteur2 == 5):
                return jeton.idJoueur   #Si le compteur est a 5 le joueur id gagne
            elif(caseDiag1 != jeton.idJoueur and caseDiag2 != jeton.idJoueur):
                print("STOP")    #Si on a déjà changer de direction et qu'il y a une case différente le joueur ne gagne pas
                break
        compteur1 = 0
        compteur2 = 0
        return 0

class Grille:
    def __init__(self):
                    #y  0 1 2 3 4 5 6 7  8     x
        self.grille = [[0,0,0,0,0,0,0,0,-1],  #0
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

    def CasesVides(self):
        casesVides = []
        for colonne in range(len(self.grille)):
            for elm in range(self.hauteur, -1, -1):
                if(self.grille[colonne][elm] == 0):
                    casesVides.append( (colonne, elm) )
                    break
        return casesVides
    
    def ColonnePleine(colonne):
        nbJeton = 0
        for jeton in colonne:
            if jeton = 1:
                nbJeton += 1
        return nbJeton == self.hauteur

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
    Jeton1 = Jeton(7,3)

    print("Coordonnées des cases vides: ",Grille1.CasesVides())
    Moteur1.Placer(Jeton1)
    print("Id du Joueur gagnant: ",Moteur1.Gagnant(Jeton1))
    print(Moteur1.grille.grille)
