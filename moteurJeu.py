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
        if (not self.grille.ColonnePleine(self.grille.grillePrincipal[colonne]) and not self.interface.lacher):
            caseDispo = self.grille.CaseVideColonne(colonne)
            rectCase = None
            for rect in self.interface.rectList:
                if rect["coord"] == caseDispo:
                    rectCase = rect["rect"]
            jeton = Jeton(idJoueur)
            self.grille.grillePrincipal[ colonne ][ caseDispo[1] ] = jeton
            #jetonRect = jeton.sprite.get_rect(center = rectCase.center)
            self.interface.lacherJeton(jeton, rectCase, (colonne,caseDispo) )
            jeton.x = caseDispo[0]
            jeton.y = caseDispo[1]
            print("Gagnant : Joueur ",self.Gagnant(jeton))
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
            if( self.grille.grillePrincipal[jeton.x][elmC] != None ):
                if( self.grille.grillePrincipal[jeton.x][elmC].idJoueur == jeton.idJoueur ):
                    compteur += 1
                else:
                    compteur = 0
                    break
                if compteur == 5:
                    return jeton.idJoueur
        compteur = 0
        # Vérificaion ligne
        for elmL in range(self.grille.largeur):
            if( self.grille.grillePrincipal[elmL][jeton.y] != None ):
                if( self.grille.grillePrincipal[elmL][jeton.y].idJoueur == jeton.idJoueur ):
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
            try: jetonCaseDiag1 = self.grille.grillePrincipal[jeton.x + elmD1][jeton.y + elmD1]
            except IndexError: pass
            try: jetonCaseDiag2 = self.grille.grillePrincipal[jeton.x - elmD1][jeton.y + elmD1]
            except IndexError: pass
            if(jetonCaseDiag1 != None):
                if(jetonCaseDiag1.idJoueur == jeton.idJoueur):
                    print("11: ",jetonCaseDiag1.idJoueur)
                    print("diag1 compteur1: ",compteur1)
                    compteur1 += 1           #Tant que notre case est à l'id du joueur on augmente le compteur
            if(jetonCaseDiag2 != None):
                if(jetonCaseDiag2.idJoueur == jeton.idJoueur):
                    print("12: ",jetonCaseDiag2.idJoueur)
                    print("diag1 compteur2: ",compteur2)
                    compteur2 += 1           #Tant que notre case est à l'id du joueur on augmente le compteur
            if(compteur1 == 5 or compteur2 == 5):
                return jeton.idJoueur   #Si le compteur est a 5 le joueur id gagne
            elif(jetonCaseDiag1 != None and jetonCaseDiag2 != None):
                if(jetonCaseDiag1.idJoueur != jeton.idJoueur and jetonCaseDiag2.idJoueur != jeton.idJoueur):
                    break
            else: break
        compteur1 -= 1
        compteur2 -= 1
        for elmD2 in range(self.grille.hauteur):
            try: jetonCaseDiag1 = self.grille.grillePrincipal[jeton.x - elmD2][jeton.y - elmD2]
            except IndexError: pass
            try: jetonCaseDiag2 = self.grille.grillePrincipal[jeton.x + elmD2][jeton.y - elmD2]
            except IndexError: pass
            if(jetonCaseDiag1 != None):
                if(jetonCaseDiag1.idJoueur == jeton.idJoueur):
                    print("21: ",jetonCaseDiag1.idJoueur)
                    print("diag2 compteur1: ",compteur1)
                    compteur1 += 1           #Tant que notre case est à l'id du joueur on augmente le compteur
            if(jetonCaseDiag2 != None):
                if(jetonCaseDiag2.idJoueur == jeton.idJoueur):
                    print("22: ",jetonCaseDiag2.idJoueur)
                    print("diag2 compteur2: ",compteur1)
                    compteur2 += 1           #Tant que notre case est à l'id du joueur on augmente le compteur
            if(compteur1 == 5 or compteur2 == 5):
                return jeton.idJoueur   #Si le compteur est a 5 le joueur id gagne
            elif(jetonCaseDiag1 != None and jetonCaseDiag2 != None):
                if(jetonCaseDiag1.idJoueur != jeton.idJoueur and jetonCaseDiag2.idJoueur != jeton.idJoueur):   #Si on a déjà changer de direction et qu'il y a une case différente le joueur ne gagne pas
                    break
            else: break
        compteur1 = 0
        compteur2 = 0
        return 0
