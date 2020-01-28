import pygame
import os
from pygame.transform import scale

class MoteurJeu:
    
    def __init__(self, grille, clock):
        #self.joueur = Joueur()
        #self.ia = IA()
        self.grille = grille
        self.clock = clock
    
    # A tester
    def Placer(self,jeton):
        colonneJeton = self.grille.hauteur - self.grille.NbJetonColonne(jeton.x) -1
        if not self.grille.ColonnePleine():
            self.grille.grilleAttente[jeton.x] = jeton.idJoueur
        self.grille.grille[jeton.x][colonneJeton] = jeton.idJoueur
        print("Jeton placé en (",jeton.x,",",colonneJeton,")")
    
    def Gagnant(self, jeton):
        compteur = 0
        # Vérification colonne
        for elmC in range(jeton.y, self.grille.hauteur, 1):
            if( self.grille.grillePrincipal[jeton.x][elmC] == jeton.idJoueur ):
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
