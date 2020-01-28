import pygame

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

