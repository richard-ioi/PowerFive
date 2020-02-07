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
            if( compteurJ2 == 5 ): score = 100
            elif( compteurJ1 == 4 ): score = 70
            elif( compteurJ2 == 4 ): score = 60
            elif( compteurJ1 == 3 ): score = 50
            elif( compteurJ2 == 3 ): score = 40
            elif( compteurJ1 == 2 ): score = 30
            elif( compteurJ2 == 2 ): score = 20

        else:
            compteurJ1 -= 1
            if( compteurJ1 == 5 ): score = 100
            elif( compteurJ2 == 4 ): score = 70
            elif( compteurJ1 == 4 ): score = 60
            elif( compteurJ2 == 3 ): score = 50
            elif( compteurJ1 == 3 ): score = 40
            elif( compteurJ2 == 2 ): score = 30
            elif( compteurJ1 == 2 ): score = 20
        #print(ligne)

        self.moteurJeu.grille.grillePrincipal[coup[0]][coup[1]] = 0
        return score

    def MinMax(self, idJoueur, nbSimul=0): #DIFFICULTE: DIFFICILE
        coupPossibles = self.moteurJeu.grille.CasesVides()
        notes = []
        score = (0,0)
        gain = 0

        """if partieterminee ou nbSimul > 2:
            return score"""
        #IDEE POUR AMELIORER: Somme du gain max au niv 0 + gain max du niv 1 + gain max du niv 2 + gain niv 3 (avec Note())
        jeton = Jeton(idJoueur,self.lastCoup[0],self.lastCoup[1])
        gagnant = self.moteurJeu.Gagnant(jeton)
        if( gagnant != 0 or nbSimul >= 3 ):
            note = self.Note(gagnant, self.lastCoup, idJoueur)
            return (note[0], self.lastCoup, note[1])

        for coupPossible in coupPossibles:
            self.moteurJeu.grille.grillePrincipal[coupPossible[0]][coupPossible[1]] = idJoueur
            if(nbSimul == 0): self.lastCoup = coupPossible
            if(idJoueur==2):
                #notes.append(self.ScoreCoup(coupPossible, 2))
                #print(f"Joueur : {idJoueur}")
                score = self.MinMax( 1, nbSimul+1 )[2]
                gain = score[1]-score[0]
            else:
                #print(f"Joueur : {idJoueur}")
                #notes.append(self.ScoreCoup(coupPossible, 1))
                score = self.MinMax( 2, nbSimul+1 )[2]
                gain = score[0]-score[1]

            notes.append( (gain, coupPossible, score) )
            self.moteurJeu.grille.grillePrincipal[coupPossible[0]][coupPossible[1]] = 0
        print("Joueur {} : {}".format(idJoueur,notes))
        print(" ")

        noteOpti = max(notes, key=lambda gain:gain[0])
        return (noteOpti[0],noteOpti[1][0],noteOpti[2])


    def Note(self, gagnant, coup, idJoueur, nbSimul=0):
        self.moteurJeu.grille.grillePrincipal[coup[0]][coup[1]] = idJoueur

        if(gagnant == 1): return (-500, (500,0))
        elif(gagnant == 2): return (500, (0,500))
        """if idJoueur == 2:
            if(gagnant == 1): return (-500, (500,0))
            elif(gagnant == 2): return (500, (0,500))
        else: 
            if(gagnant == 1): return (500, (500,0))
            elif(gagnant == 2): return (-500, (0,500))"""

        coupPossibles = self.moteurJeu.grille.CasesVides()
        notesIA = []
        notesH = []
        for coupPossible in coupPossibles:
            notesIA.append(self.ScoreCoup(coupPossible, 2))
            notesH.append(self.ScoreCoup(coupPossible, 1))
        self.moteurJeu.grille.grillePrincipal[coup[0]][coup[1]] = 0

        maxIA = max(notesIA, key=lambda score: score[0])
        maxH = max(notesH, key=lambda score: score[0])
        return (maxIA[0] - maxH[0], (maxH[0],maxIA[0]))

"""def MinMax(self, idJoueur, nbSimul): #DIFFICULTE: DIFFICILE
coupPossibles = self.moteurJeu.grille.CasesVides()
notesIA = []
notesH = []

if partieterminee ou nbSimul > 2:
    return score

if( nbSimul >= 3 ):

for coupPossible in coupPossibles:
    print(coupPossible," Simul n°: ",self.nbSimul)
    self.moteurJeu.grille.grillePrincipal[coupPossible[0]][coupPossible[1]] = idJoueur
    if(idJoueur==2):
        #score = self.ScoreCoup(coupPossible, 2)[0]
        notesIA.append(self.ScoreCoup(coupPossible, 2))   #Ajoute (score du coup, le coup correspondant) a la liste de l'ia
        if(self.nbSimul < 3):
            self.nbSimul += 1
            #Appel de MinMax pour l'autre joueur
            notesH.append(self.MinMax(1, nbSimul + 1)[:2])
        else:
            self.nbSimul = 0 
            self.moteurJeu.grille.grillePrincipal[coupPossible[0]][coupPossible[1]] = 0
            continue
    else:
        notesH.append(self.ScoreCoup(coupPossible, 1))    #Ajoute (score du coup, le coup correspondant) a la liste de l'humain
        if(self.nbSimul < 3):
            self.nbSimul += 1
            #Appel de MinMax pour l'autre joueur
            notesIA.append(self.MinMax(2)[:2])
        else:
            self.nbSimul = 0 
            self.moteurJeu.grille.grillePrincipal[coupPossible[0]][coupPossible[1]] = 0
            continue
    self.moteurJeu.grille.grillePrincipal[coupPossible[0]][coupPossible[1]] = 0

maxIA = max(notesIA, key=lambda scoreIA: scoreIA[0])
maxH = max(notesH, key=lambda scoreH: scoreH[0])
#retourner (le max des notes IA ,  le coup associé ,  le max des notesIA - le max des notesH) si idJoueur = 2
#retourner (le max des notes Humain ,  le coup associé,  le max des notesH - le max des notesIA) si idJoueur = 1
if(idJoueur == 2): return ( maxIA[0], maxIA[1], maxIA[0]-maxH[0] )
else: return ( maxH[0], maxH[1], maxH[0]-maxIA[0] )"""

"""jeton = Jeton(idJoueur,coup[0],coup[1])
self.moteurJeu.grille.grillePrincipal[coup[0]][coup[1]] = jeton.idJoueur
gagnant = self.moteurJeu.Gagnant(jeton)
#print(self.nbSimul)
if(gagnant == 1): return (-500, coup[0], (500,0))
elif(gagnant == 2): return (500, coup[0], (0,500))
elif(self.nbSimul >= 3):
    return (self.mMgain, coup[0], self.mMscore)
self.nbSimul += 1
self.moteurJeu.grille.grillePrincipal[coup[0]][coup[1]] = 0
coupPossibles = self.moteurJeu.grille.CasesVides()
notes = []
jeton = None
gagnant = 0
if(self.nbSimul >= 3):
    return (self.mMgain, 0, self.mMscore)
else:
    for coupPossible in coupPossibles:
        print(self.nbSimul)
        self.moteurJeu.grille.grillePrincipal[coupPossible[0]][coupPossible[1]] = idJoueur
        jeton = Jeton(idJoueur,coupPossible[0],coupPossible[1])
        gagnant = self.moteurJeu.Gagnant(jeton)
        #print(self.nbSimul)
        if(gagnant == 1): return (-500, coupPossible[0], (500,0))
        elif(gagnant == 2): return (500, coupPossible[0], (0,500))
        else:
            if(idJoueur==2):
                #notes.append(self.ScoreCoup(coupPossible, 2))
                self.mMscore = self.MinMax(1)[2]
                self.mMgain = self.mMscore[1]-self.mMscore[0]
            else:
                #notes.append(self.ScoreCoup(coupPossible, 1))
                self.mMscore = self.MinMax(2)[2]
                self.mMgain = self.mMscore[0]-self.mMscore[1]
            notes.append( (self.mMgain, coupPossible, self.mMscore) )
            self.moteurJeu.grille.grillePrincipal[coupPossible[0]][coupPossible[1]] = 0
            print(notes)
self.nbSimul += 1
noteOpti = max(notes, key=lambda gain:gain[0])
return (noteOpti[0],noteOpti[1][0],noteOpti[2])"""

"""def Simulation(idJoueur):
if( DetectionGagnant() != 0 ):
    return (CalculScore(), None)
coupsPossibles = CasesLibres()
if( len(coupsPossibles) == 9 ):
    return ( None, (0,0) )
resultats = []
for k in coupsPossibles:
    Grille[k[0]][k[1]] = idJoueur
    if(idJoueur == 1):
        score = Simulation(2)[0]     #Tuple de score ex: (0,1)
        gain = score[0] - score[1]   #Gain ex: 0-1=-1
    else:
        score = Simulation(1)[0]     #Tuple de score ex: (0,1)
        gain = score[1] - score[0]   #Gain ex: 1-0=1
    resultats.append((score,gain,k))   #On ajoute le score (0) le gain (1) et son coup associé (2) aux résultats
    Grille[k[0]][k[1]] = 0           #On efface le coup que l'on a testé
gainMax = max( resultats, key=lambda gain: gain[1] )
return (gainMax[0],gainMax[2])"""

"""def MinMax(self, coup, idJoueur): #DIFFICULTE: DIFFICILE
jeton = Jeton(idJoueur)
self.moteurJeu.grille.grillePrincipal[coup[0]][coup[1]] = jeton.idJoueur
gagnant = self.moteurJeu.Gagnant(jeton)
if(gagnant == 1): return (-500, coup[0])
elif(gagnant == 2): return (500, coup[0])
elif(self.nbSimul == 3): 
    self.nbSimul = 0
    return
coupPossibles = self.moteurJeu.grille.CasesVides()
notesIA = []
notesH = []
for coupPossible in coupPossibles:
    notesIA.append(self.ScoreCoup(coupPossible, 2))
    notesH.append(self.ScoreCoup(coupPossible, 1))
    print(notesIA)
    print(notesH)
    print("#####")
print(" ")
self.moteurJeu.grille.grillePrincipal[coup[0]][coup[1]] = 0
self.nbSimul += 1
return ( max(notesIA, key=lambda score: score[0])[0] - max(notesH, key=lambda score: score[0])[0], coup[0] )"""