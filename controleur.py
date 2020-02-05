#! /usr/bin/env python3

"""
    Module regroupant les contrôleurs du jeu.
"""

import pygame
import os
import random
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
        self.interface.moteurJeu = self
        self.grille = grille
        self.clock = clock
        self.lacher=False

    
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
                if rect["coord"] == (colonne, caseDispo):
                    rectCase = rect["rect"]
            jeton = Jeton(idJoueur)
            self.grille.grillePrincipal[ colonne ][ caseDispo ] = jeton.idJoueur
            #jetonRect = jeton.sprite.get_rect(center = rectCase.center)
            self.interface.lacherJeton(jeton, rectCase, (colonne,caseDispo) )
            if self.interface.lacher:
                self.lacher=True
            jeton.x = colonne
            jeton.y = caseDispo
            #print(jeton)
    
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
                print("Win colonne")
                return jeton.idJoueur
        compteur = 0
        # Vérificaion ligne
        for elmL in range(self.grille.largeur):
            if( self.grille.grillePrincipal[elmL][jeton.y] == jeton.idJoueur ):
                compteur += 1
            else:
                compteur = 0
            if compteur == 5:
                print("Win Ligne")
                return jeton.idJoueur
        compteur = 0
        compteur1 = 0
        compteur2 = 0
        # Vérification diagonale 1
        for elmD1 in range(self.grille.hauteur):
            #print(elmD1)
            try: caseDiag1 = self.grille.grillePrincipal[jeton.x + elmD1][jeton.y + elmD1]
            except IndexError: caseDiag1 = 0
            try: caseDiag2 = self.grille.grillePrincipal[jeton.x - elmD1][jeton.y + elmD1]
            except IndexError: caseDiag2 = 0
            if(caseDiag1 == jeton.idJoueur):
                compteur1 += 1           #Tant que notre case est à l'id du joueur on augmente le compteur
            if(caseDiag2 == jeton.idJoueur):
                compteur2 += 1           #Tant que notre case est à l'id du joueur on augmente le compteur
            #print("1 ",compteur1," 2 ",compteur2)
            if(compteur1 == 5 or compteur2 == 5):
                print("Win Diag1")
                return jeton.idJoueur   #Si le compteur est a 5 le joueur id gagne
            elif(caseDiag1 != jeton.idJoueur and caseDiag2 != jeton.idJoueur):
                #print("STOP")    #Si on a déjà changer de direction et qu'il y a une case différente le joueur ne gagne pas
                break
        #print("###")
        compteur1 -= 1
        compteur2 -= 1
        for elmD2 in range(self.grille.hauteur):
            try: caseDiag1 = self.grille.grillePrincipal[jeton.x - elmD2][jeton.y - elmD2]
            except IndexError: caseDiag1 = 0
            try: caseDiag2 = self.grille.grillePrincipal[jeton.x + elmD2][jeton.y - elmD2]
            except IndexError: caseDiag2 = 0
            #POUR LE SCORE DU COUP


            #POUR LE GAGNANT
            if(caseDiag1 == jeton.idJoueur):
                compteur1 += 1           #Tant que notre case est à l'id du joueur on augmente le compteur
            if(caseDiag2 == jeton.idJoueur):
                compteur2 += 1           #Tant que notre case est à l'id du joueur on augmente le compteur
            if(compteur1 == 5 or compteur2 == 5):
                print("Win Diag2")
                return jeton.idJoueur   #Si le compteur est a 5 le joueur id gagne
            elif(caseDiag1 != jeton.idJoueur and caseDiag2 != jeton.idJoueur):
                #print("STOP")    #Si on a déjà changer de direction et qu'il y a une case différente le joueur ne gagne pas
                break
        compteur1 = 0
        compteur2 = 0
        return 0


class Jukebox:
    """
        Classe permettant la manipulation de la musique et des sons du jeu.
    """

    def __init__(self, musics, sounds):
        self.musics = musics
        self.sounds = sounds
        self.currentMusic = self.musics["Pingu"]
    
    def exist(self, titre):
        return titre in self.musics.keys() or titre in self.sounds.keys()

    def playMusic(self, music, loop = -1, start = 0.0):
        if music != self.currentMusic and self.exist(music):
            pygame.mixer.music.load(self.musics[music])
            pygame.mixer.music.play(loops = loop, start = start)
    
    def playSound(self, sound):
        if self.exist(sound):
            self.sounds.play()


class IA:
    def __init__(self, moteurJeu):
        self.idIA = 2
        self.moteurJeu = moteurJeu

    def IAPlay(self):
        coupPossibles = self.moteurJeu.grille.CasesVides()
        randomCoup = random.randrange(len(coupPossibles))
        self.moteurJeu.Placer( coupPossibles[randomCoup][0], self.idIA )
        
    """def ScoreCoup(self, coup):
        self.moteurJeu.grille.RemplirCase(coup[1],2)
        #Calcul du score
        for caseLigne in range(self.moteurJeu.grille.largeur):
            def
        self.moteurJeu.grille.grillePrincipal[coup[0]][coup[1]] = 0
        return ( score, colonne )

    def CalculScore():
        gagnant = MoteurJeu.Gagnant(Jeton)
        if gagnant == 1:
            return (1,0)
        elif gagnant == 2:
            return (0,1)
        else:
            return(0,0)

    def Simulation(self,jeton):
        if self.MoteurJeu.Gagnant(jeton):
            return (CalculScore(), None)
        L=self.grille.CasesVides()
        resultat=[]
        for K in L:
            self.grille[K[0]][K[1]]=jeton.idJoueur
            if jeton.idJoueur==2:
                score = Simulation(1)[0]
                gain = score[1] - score[0]
            else:
                score = Simulation(2)[0]
                gain = score[0] - score[1]
            resultat.append((score,gain,K))
            self.grille[K[0]][K[1]]=0
        gainmax=max(resultat, key=lambda res: res[1])
        return (gainmax[0], gainmax[2])"""