import pygame
import os
from moteurJeu import *
from Joueur import Joueur
from affichage import Animation

pygame.init()

GrilleDeJeu = Grille()
MoteurDeJeu = MoteurJeu(GrilleDeJeu)
JoueurH = Joueur()
#JetonActuel = None

screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Test Animation Forggy")
imageTest = pygame.image.load(os.path.join("data","graphismes","test.png"))
AnimTest = Animation(screen,"froggy\char.png",0,24,2)


while True:
    event = pygame.event.Event(pygame.USEREVENT)
    pygame.event.pump()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
    screen.blit(imageTest,(600,10))
    pygame.display.flip()
    
    if( pygame.mouse.get_pressed() ):
        AnimTest.play = True
        print("CLIC DE LA SOURIS")
    if( AnimTest.play ):
        AnimTest.update(AnimTest.x_pos,AnimTest.y_pos)
        AnimTest.affiche(50,50)
        print("ANIMATION FROGGY")
    

    #posSouris = JoueurH.CliqueSouris(event, MOUSEBUTTONDOWN)
    #MoteurDeJeu.Placer(posSouris)