#! /usr/bin/env python3

"""
    Module regroupant les contrôleurs du jeu.
"""

import pygame
import os
import random
from pygame.transform import scale
from modeles import Jeton,Grille

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
            self.grille.grillePrincipal[ colonne ][ caseDispo[1] ] = jeton.idJoueur
            #jetonRect = jeton.sprite.get_rect(center = rectCase.center)
            self.interface.lacherJeton(jeton, rectCase, (colonne,caseDispo) )
            jeton.x = caseDispo[0]
            jeton.y = caseDispo[1]
            #print(jeton)
    
    def Gagnant(self, jeton):
        compteurL=0
        compteurC=0
        compteurD1=0
        compteurD2=0
        EP = self.grille.EtatPlacement(jeton.x, jeton.y)
        colonne=EP["colonne"]
        ligne=EP["ligne"]
        diag1=EP["diag1"]
        diag2=EP["diag2"]
        for i in range(9):
            try: caseDiag1 = diag1[i]
            except IndexError: caseDiag1=0
            try: caseDiag2 = diag2[i]
            except IndexError: caseDiag2=0
            caseLigne = ligne[i]
            try: caseColonne = colonne[i]
            except IndexError: caseColonne=0
            #verif ligne
            if caseLigne==jeton.idJoueur:
                compteurL+=1
            else:
                compteurL=0
            if compteurL==5:
                print("Win Ligne")
                return jeton.idJoueur
            #verif colonne
            if caseColonne==jeton.idJoueur:
                compteurC+=1
            else:
                compteurC=0
            if compteurC==5:
                print("Win Colonne")
                return jeton.idJoueur
            #verif diag1
            if caseDiag1==jeton.idJoueur:
                compteurD1+=1
            else:
                compteurD1=0
            if compteurD1==5:
                print("Win Diag1")
                return jeton.idJoueur
            #verif diag2
            if caseDiag2==jeton.idJoueur:
                compteurD2=1
            else:
                compteurD2=0
            if compteurD2==5:
                print("Win Diag2")
                return jeton.idJoueur
        #par défaut
        return 0

class Jukebox:
    """
        Classe permettant la manipulation de la musique et des sons du jeu.
    """

    def __init__(self, musics, sounds=None):
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
    def __init__(self, moteurJeu, difficulty):
        self.idIA = 2
        self.moteurJeu = moteurJeu
        self.difficulty = difficulty

    def IAPlay(self):
        coupPossibles = self.moteurJeu.grille.CasesVides()
        if( self.difficulty == "easy" ):
            randomCoup = random.randrange(len(coupPossibles))
            self.moteurJeu.Placer(coupPossibles[randomCoup][0], self.idIA)
        else:
            listeCoups=[]
            for coup in coupPossibles:
                if( self.difficulty == "normal" ):
                    listeCoups.append(self.ScoreCoup(coup,2))
                elif( self.difficulty == "difficile" ):
                    listeCoups.append(self.MinMax(coup))
            print(listeCoups)
            coupIA=max(listeCoups, key=lambda score: score[0])
            #print(coupIA[0])
            self.moteurJeu.Placer(coupIA[1], self.idIA)

    def ScoreCoup(self, coup, idJoueur):
        scores=[]
        scores.append(self.ScoreCompteur(coup,"ligne",idJoueur))
        scores.append(self.ScoreCompteur(coup,"colonne",idJoueur))
        scores.append(self.ScoreCompteur(coup,"diag1",idJoueur))
        scores.append(self.ScoreCompteur(coup,"diag2",idJoueur))
        return ( max(scores),coup[0] )
            
    def ScoreCompteur(self, coup, stringEtat, ID):
        #print(stringEtat)
        self.moteurJeu.grille.grillePrincipal[coup[0]][coup[1]] = 2
        score = 15
        #Calcul du score
        EP=self.moteurJeu.grille.EtatPlacement(coup[0], coup[1])
        ligne=EP[stringEtat]
        compteurJ2 = compteurJ1 = 0
        #Compteur pour J2
        if stringEtat!='colonne':
            k=0
        else:
            k=1
        for i2 in range(coup[k], len(ligne), 1):
            #vers les i++
            try: case = ligne[i2]
            except IndexError: case = -1
            if( case == 2 ): compteurJ2 += 1
            elif(i2 != coup[k]): break
        for j2 in range(coup[k], -1, -1):
            #vers les j--
            try: case = ligne[j2]
            except IndexError: case = -1
            if( case == 2 ): compteurJ2 += 1
            elif(j2 != coup[k]) : break

        #Compteur pour J1
        for i1 in range(coup[k], len(ligne), 1):
            #vers les i++
            #print(coup," ",i1," ",ligne[i1])
            try: case = ligne[i1]
            except IndexError: case = -1
            if( case == 1 ): compteurJ1 += 1
            elif( i1 != coup[k] ): break
        for j1 in range(coup[k], -1, -1):
            #vers les j--
            try: case = ligne[j1]
            except IndexError: case = -1
            if( case == 1 ): compteurJ1 += 1
            elif( j1 != coup[k] ): break
        #print(coup," ",ligne," J1: ",compteurJ1," J2: ",compteurJ2 )

        #Conditions de scores
        #print("J1: ",compteurJ1," J2: ",compteurJ2 )
        if ID==2:
            compteurJ2 -= 1
            if( compteurJ2 == 5 ): score = 100
            elif( compteurJ1 == 4 ): score = 70
            elif( compteurJ2 == 4 ): score = 60
            elif( compteurJ1 == 3 ): score = 50
            elif( compteurJ2 == 3 ): score = 40
            elif( compteurJ1 == 2 ): score = 30
            elif( compteurJ2 == 2 ): score = 20

        else:
            compteurJ1 -= 1
            if( compteurJ2 == 5 ): score = 100
            elif( compteurJ1 == 4 ): score = 70
            elif( compteurJ2 == 4 ): score = 60
            elif( compteurJ1 == 3 ): score = 50
            elif( compteurJ2 == 3 ): score = 40
            elif( compteurJ1 == 2 ): score = 30
            elif( compteurJ2 == 2 ): score = 20
        #print(ligne)

        self.moteurJeu.grille.grillePrincipal[coup[0]][coup[1]] = 0
        return score


    def MinMax(self, coup): #DIFFICULTE: DIFFICILE
        """jeton = Jeton()
        gagnant = self.moteurJeu.Gagnant(jeton)
        if(gagnant == 1): return -500
        elif(gagnant == 2): return 500"""
        self.moteurJeu.grille.grillePrincipal[coup[0]][coup[1]] = 2
        notesIA = []
        notesH = []
        coupPossibles = self.moteurJeu.grille.CasesVides()
        for coupPossible in coupPossibles:
            notesIA.append(self.ScoreCoup(coupPossible, 2))
            notesH.append(self.ScoreCoup(coupPossible, 1))
        self.moteurJeu.grille.grillePrincipal[coup[0]][coup[1]] = 0
        return ( max(notesIA, key=lambda score: score[0])[0] - max(notesH, key=lambda score: score[0])[0], coup[0] )