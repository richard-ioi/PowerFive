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
        compteurD2=O
        colonne=EtatPlacemet()["colonne"]
        ligne=EtatPlacemet()["ligne"]
        diag1=EtatPlacemet()["diag1"]
        diag2=EtatPlacemet()["diag2"]
        for i in range(9):
            try: caseDiag1 = diag1[i]
            except IndexError: caseDiag1=0
            try: caseDiag2 = diag2[i]
            except IndexError: caseDiag2=0
            caseLigne = ligne[i]
            caseColonne = ligne[i]
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
        listeCoups=[]
        for coup in coupPossibles:
            listeCoups.append(ScoreCoup(coup))
        coupIA=max(listeCoups, key=lambda score: score[0])
        self.MoteurJeu.Placer(coupIA[1][0], self.idIA)
        
    def ScoreCoup(self, coup):
        self.moteurJeu.grille.RemplirCase(coup[1],2)
        dicoEtat = self.moteurJeu.EtatPlacement(coup,2)
        scores = []
        #Calcul du score
        
        for paquet in range(5):
            compteurJ1 = compteurJ2 = compteur0 = 0
            for case in range(paquet, paquet+5):
                caseLigne = dicoEtat["ligne"][case]
                """caseColonne = dicoEtat["colonne"][case]
                caseDiag1 = dicoEtat["diag1"][case]
                caseDiag2 = dicoEtat["diag2"][case]"""
                if( caseLigne == 2 ):
                    compteur0 = compteurJ1 = 0
                    compteurJ2 += 1
                elif( caseLigne == 1):
                    compteur0 = compteurJ2 = 0
                    compteurJ1 += 1
                elif( caseLigne == 0):
                    compteur0 += 1
                    if( compteur0 >= 4):
                        compteurJ1 = compteurJ2 = 0
                else:
                    compteur0 = compteurJ1 = compteurJ2 = 0

                #Cas simples (pas de blocage)
                if( compteurJ2 == 5 ):
                    scores.append(100)
                elif( compteurJ2 == 4 and compteurJ1 == 0 ):
                    scores.append(60)
                elif( compteurJ2 == 3 and compteurJ1 == 0 ):
                    scores.append(40)
                elif( compteurJ2 == 2 and compteurJ1 == 0 ):
                    scores.append(20)
                #Cas complexes (avec blocage)
                if( compteurJ1 == 4 and compteurJ2 == 1 ):
                    scores.append(70)
                if( compteurJ1 == 3 and compteurJ2 != 0 ):
                    scores.append(50)
                if( compteurJ1 == 2 and compteurJ2 != 0 ):
                    scores.append(30)
            

        self.moteurJeu.grille.grillePrincipal[coup[0]][coup[1]] = 0
        return ( max(scores), coup[0] )

    """def CalculScore():
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