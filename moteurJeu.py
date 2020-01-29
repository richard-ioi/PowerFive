#! /usr/bin/env python3

"""
    Module regroupant les contrôleurs du jeu.
"""

import pygame
import os
from pygame.transform import scale
from modeles import Jeton

class MoteurJeu:
    """
        Classe regroupant les méthodes effectuant toute les actions disponibles du jeu.
    """
    def __init__(self, interface, grille, clock):
        """
            Constructeur de la classe.

            Args:
                grille: Objet Grille utilisé et manipulé par le jeu
                clock: Horloge pygame du jeu.
        """
        #self.joueur = Joueur()
        #self.ia = IA()
        self.interface = interface
        self.grille = grille
        self.clock = clock
    
    # A tester
    def Placer(self, colonne, idJoueur):
        """
            Méthode permettant la placement d'un jeton dans la grille.

            Args:
                jeton: Jeton à placer dans la grille
        """
        if not self.grille.ColonnePleine(self.grille.grillePrincipal[colonne]):
            caseDispo = self.grille.CasesVides()[colonne]
            rectCase = None
            for rect in self.interface.rectList:
                if rect["coord"] == caseDispo:
                    rectCase = rect["rect"]
            jeton = Jeton(idJoueur)
            self.grille.grillePrincipal[ colonne ][ caseDispo[1] ] = jeton
            jetonRect = jeton.sprite.get_rect(center = rectCase.center)
            self.interface.lacherJeton(jeton, (colonne,caseDispo) )
        else:
            print("Vous ne pouvez pas placer de jetons dans cette colonne.")
    
    def Gagnant(self, jeton):
        """
            Méthode permttant de déterminer s'il y a un gagnant.
            Elle vérifie la colonne, la diagonale et la ligne ou se trouve la jeton.

            Args:
                jeton: Jeton servant de référentiel pour la vérification.
        """
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
            if( self.grille.grillePrincipal[elmL][jeton.y] == jeton.idJoueur ):
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
            try: caseDiag1 = self.grille.grillePrincipal[jeton.x + elmD1][jeton.y + elmD1]
            except IndexError: pass
            try: caseDiag2 = self.grille.grillePrincipal[jeton.x - elmD1][jeton.y + elmD1]
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
            try: caseDiag1 = self.grille.grillePrincipal[jeton.x - elmD2][jeton.y - elmD2]
            except IndexError: pass
            try: caseDiag2 = self.grille.grillePrincipal[jeton.x + elmD2][jeton.y - elmD2]
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
