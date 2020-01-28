import pygame
from moteurJeu import MoteurJeu,Grille

class Jeton: 
    def __init__(self, x, y, idJ):
        self.x = x
        self.y = y
        self.idJoueur = idJ
        self.image = 0

class Joueur:

    def __init__(self):
        self.posSouris = (0,0)
        self.idJoueur = 1

    def CliqueSouris(self,event,boutonSouris):
        if event.type == boutonSouris:
            self.posSouris = event.pos
            return self.posSouris

class IA:
    def __init__(self,grille):
        self.idJoueur = 2
        self.grille=grille

    def Simulation(self,ID):
        if self.moteurJeu.Gagnant(jeton):
            return
        L=self.grille.CasesVides()
        resultat=[]
        for K in L:
            self.grille[K[0]][K[1]]=ID
            if ID==2:
                score = Simulation(1)[0]
                gain = score[1] - score[0]
            else:
                score = Simulation(2)[0]
                gain = score[0] - score[1]
            resultat.append((score,gain,K))
            self.grille[K[0]][K[1]]=0
        gainmax=max(resultat, key=lambda res: res[1])
        return (gainmax[0], gainmax[2])
