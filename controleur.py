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
        #verif ligne
        for i in range(len(ligne)):
            caseLigne = ligne[i]
            if caseLigne==jeton.idJoueur:
                compteurL+=1
            else:
                compteurL=0
            if compteurL==5:
                print("Win Ligne")
                return jeton.idJoueur
        #verif colonne
        for i in range(len(colonne)):
            caseColonne = colonne[i]
            if caseColonne==jeton.idJoueur:
                compteurC+=1
            else:
                compteurC=0
            if compteurC==5:
                print("Win Colonne")
                return jeton.idJoueur
        #verif diag1
        for i in range(len(diag1)):
            caseDiag1 = diag1[i]
            if caseDiag1==jeton.idJoueur:
                compteurD1+=1
            else:
                compteurD1=0
            if compteurD1==5:
                print("Win Diag1")
                return jeton.idJoueur
        #verif diag2
        for i in range(len(diag2)):
            caseDiag2 = diag2[i]
            if caseDiag2==jeton.idJoueur:
                compteurD2+=1
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
        self.lastCoup = (0,0)
        self.nbSimul = 0
        self.mMscore = (0,0)
        self.mMgain = 0

    def IAPlay(self):
        coupPossibles = self.moteurJeu.grille.CasesVides()
        if( self.difficulty == "easy" ):
            randomCoup = random.randrange(len(coupPossibles))
            self.moteurJeu.Placer(coupPossibles[randomCoup][0], self.idIA)
        elif( self.difficulty == "difficile" ):
            self.moteurJeu.Placer(self.MinMax(2)[1], self.idIA) #Jouer le meilleur coup retourné par MinMax
            #self.nbSimul = 0
        else:
            listeCoups=[]
            for coup in coupPossibles:
                if( self.difficulty == "normal" ):
                    listeCoups.append(self.ScoreCoup(coup,2))
            #print(listeCoups)
            coupIA=max(listeCoups, key=lambda score: score[0])
            self.moteurJeu.Placer(coupIA[1], self.idIA)

    def ScoreCoup(self, coup, idJoueur):  #Retourne le score du coup placé en parametre
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
            if( compteurJ2 == 5 ): score = 500
            elif( compteurJ1 == 4 ): score = 70
            elif( compteurJ2 == 4 ): score = 60
            elif( compteurJ1 == 3 ): score = 50
            elif( compteurJ2 == 3 ): score = 40
            elif( compteurJ1 == 2 ): score = 30
            elif( compteurJ2 == 2 ): score = 20

        else:
            compteurJ1 -= 1
            if( compteurJ1 == 5 ): score = 500
            elif( compteurJ2 == 4 ): score = 70
            elif( compteurJ1 == 4 ): score = 60
            elif( compteurJ2 == 3 ): score = 50
            elif( compteurJ1 == 3 ): score = 40
            elif( compteurJ2 == 2 ): score = 30
            elif( compteurJ1 == 2 ): score = 20
        #print(ligne)

        self.moteurJeu.grille.grillePrincipal[coup[0]][coup[1]] = 0
        return score

    def MinMax(self, idJoueur, nbSimul=0, dernierCoup=None): #Doit retourner le meilleur coup à jouer pour l'ia
    #CHANGER LA FONCTION POUR NE PLUS UTILLISER LES (SCORE) MAIS SEULEMENT LES GAINS = LES NOTES
    
        #Si il y a un gagnant ou qu'on est à la profondeur 3: return la "note" de l'état du jeu, soit un tuple (score,None)
        if( dernierCoup != None ):
            jeton = Jeton(idJoueur, dernierCoup[0], dernierCoup[1]) #On creer un jeton temporaire pour determiner si il y a un gagnant pour le dernier coup joué
            self.moteurJeu.grille.grillePrincipal[dernierCoup[0]][dernierCoup[1]] = idJoueur #On rejoue le dernier coup
            gagnant = self.moteurJeu.Gagnant(jeton)
            self.moteurJeu.grille.grillePrincipal[dernierCoup[0]][dernierCoup[1]] = 0 #On annule ce coup
            if( gagnant != 0 or nbSimul >= 2 ):
                #print("coup:",dernierCoup," ",gagnant," ",nbSimul)
                return self.Note()

        #On détermine les coups disponibles sur la grille de jeu et on instencie de la liste des notes
        coupsPossibles = self.moteurJeu.grille.CasesVides()
        notes = []

        #Pour chaque coup possible on va:
        #Jouer le coup, calculer le score par une récurrence de minmax sur l'autre joueur en incrémentant la profondeur (nbSimul), stocker dans les notes (le gain, le score, le coup associé), annuler le coup
        for coupPossible in coupsPossibles:
            self.moteurJeu.grille.grillePrincipal[coupPossible[0]][coupPossible[1]] = idJoueur
            if( idJoueur == 2 ):
                newMinMax = self.MinMax(1, nbSimul+1, coupPossible) #Ce qu'on obtient par la récurence de MinMax, soit un tuple ( (score), coup )
                #print("#J1##",newMinMax)
                score = newMinMax[0]
                gain = score[1] - score[0] #gain = score ia - score humain
            else:
                newMinMax = self.MinMax(2, nbSimul+1, coupPossible) #Ce qu'on obtient par la récurence de MinMax, soit un tuple ( (score), coup )
                #print("#J2##",newMinMax)
                score = newMinMax[0]
                gain = score[0] - score[1] #gain = score humain - score ia

            notes.append( (gain, score, coupPossible[0]) ) #Soit [0]:gain, [1]:(score), [2]:coup associé
            self.moteurJeu.grille.grillePrincipal[coupPossible[0]][coupPossible[1]] = 0

        #On retourne enfin le score et le coup du tuple de notes qui possède le gain maximal, soit ( (score),coup) du gain max, pour pouvoir récupérer le score dans la récurrence et jouer le meilleur coup dans IAPlay()
        print(" ")
        print(notes)
        noteMax = max( notes, key=lambda gain:gain[0] ) #Tuple de notes qui possède le gain maximal
        print(noteMax)
        return ( noteMax[1], noteMax[2] )


    def Note(self): #Doit retourner un tuple ((scoreH max,scoreIA max), None) pour etre "utilisé" dans MinMax()
        #On instencie les coups disponibles et les listes des scores pour l'ia et pour l'humain qui contiendra des tuples (score, coup associé)
        coupsDispo  = self.moteurJeu.grille.CasesVides()
        scoresIA = []
        scoresH = []

        #Pour chaque coup possible on va:
        #Avec la fonction ScoreCoup(), calculer le score pour ce coup pour l'ia et l'ajouter à scoresIA, calculer le score pour ce coup pour l'humain et l'ajouter à scoresH
        for coup in coupsDispo:
            scoresIA.append( self.ScoreCoup(coup, 2)[0] )
            scoresH.append( self.ScoreCoup(coup, 1)[0] )

        #On retourne un tuple ( (max de scoresH, max de scoresIA), None )
        return (  ( max(scoresH), max(scoresIA) ), None  )


    """def MinMax(self, idJoueur, nbSimul=0, dernierCoup=None): #Doit retourner le meilleur coup à jouer pour l'ia

        #Si il y a un gagnant ou qu'on est à la profondeur 3: return la "note" de l'état du jeu, soit un tuple (score,None)
        if( dernierCoup != None ):
            jeton = Jeton(idJoueur, dernierCoup[0], dernierCoup[1]) #On creer un jeton temporaire pour determiner si il y a un gagnant pour le dernier coup joué
            self.moteurJeu.grille.grillePrincipal[dernierCoup[0]][dernierCoup[1]] = idJoueur #On rejoue le dernier coup
            gagnant = self.moteurJeu.Gagnant(jeton)
            self.moteurJeu.grille.grillePrincipal[dernierCoup[0]][dernierCoup[1]] = 0 #On annule ce coup
            if( gagnant != 0 or nbSimul >= 3 ):
                #print("coup:",dernierCoup," ",gagnant," ",nbSimul)
                return self.Note()

        #On détermine les coups disponibles sur la grille de jeu et on instencie de la liste des notes
        coupsPossibles = self.moteurJeu.grille.CasesVides()
        notes = []

        #Pour chaque coup possible on va:
        #Jouer le coup, calculer le score par une récurrence de minmax sur l'autre joueur en incrémentant la profondeur (nbSimul), stocker dans les notes (le gain, le score, le coup associé), annuler le coup
        for coupPossible in coupsPossibles:
            self.moteurJeu.grille.grillePrincipal[coupPossible[0]][coupPossible[1]] = idJoueur
            if( idJoueur == 2 ):
                newMinMax = self.MinMax(1, nbSimul+1, coupPossible) #Ce qu'on obtient par la récurence de MinMax, soit un tuple ( (score), coup )
                #print("#J1##",newMinMax)
                score = newMinMax[0]
                gain = score[1] - score[0] #gain = score ia - score humain
            else:
                newMinMax = self.MinMax(2, nbSimul+1, coupPossible) #Ce qu'on obtient par la récurence de MinMax, soit un tuple ( (score), coup )
                #print("#J2##",newMinMax)
                score = newMinMax[0]
                gain = score[0] - score[1] #gain = score humain - score ia

            notes.append( (gain, score, coupPossible[0]) ) #Soit [0]:gain, [1]:(score), [2]:coup associé
            self.moteurJeu.grille.grillePrincipal[coupPossible[0]][coupPossible[1]] = 0

        #On retourne enfin le score et le coup du tuple de notes qui possède le gain maximal, soit ( (score),coup) du gain max, pour pouvoir récupérer le score dans la récurrence et jouer le meilleur coup dans IAPlay()
        print(" ")
        print(notes)
        noteMax = max( notes, key=lambda gain:gain[0] ) #Tuple de notes qui possède le gain maximal
        print(noteMax)
        return ( noteMax[1], noteMax[2] )


    def Note(self): #Doit retourner un tuple ((scoreH max,scoreIA max), None) pour etre "utilisé" dans MinMax()
        #On instencie les coups disponibles et les listes des scores pour l'ia et pour l'humain qui contiendra des tuples (score, coup associé)
        coupsDispo  = self.moteurJeu.grille.CasesVides()
        scoresIA = []
        scoresH = []

        #Pour chaque coup possible on va:
        #Avec la fonction ScoreCoup(), calculer le score pour ce coup pour l'ia et l'ajouter à scoresIA, calculer le score pour ce coup pour l'humain et l'ajouter à scoresH
        for coup in coupsDispo:
            scoresIA.append( self.ScoreCoup(coup, 2)[0] )
            scoresH.append( self.ScoreCoup(coup, 1)[0] )

        #On retourne un tuple ( (max de scoresH, max de scoresIA), None )
        return (  ( max(scoresH), max(scoresIA) ), None  )"""
        