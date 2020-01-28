import pygame
import os
from moteurJeu import *
from joueur import Joueur
from affichage import Animation

pygame.init()
Clock = pygame.time.Clock()
done = False

GrilleDeJeu = Grille()
MoteurDeJeu = MoteurJeu(GrilleDeJeu, Clock)
JoueurH = Joueur()
#JetonActuel = None

screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Test Animation Forggy")
AnimTest = Animation(screen,"froggy\char.png",0,24,5)


while not done:
    Clock.tick(60)
    FPS = Clock.get_fps()
    print(FPS)
    event = pygame.event.Event(pygame.USEREVENT)
    pygame.event.pump()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    pygame.display.flip()
    
    if( pygame.mouse.get_pressed() ):
        AnimTest.play = True
        #print("CLIC DE LA SOURIS")
    if( AnimTest.play ):
        #print("First ",AnimTest.speed)
        AnimTest.update(AnimTest.x_pos,AnimTest.y_pos)
        AnimTest.affiche(1000,520,Clock)
        #print("Then ",AnimTest.speed)
        #print("ANIMATION FROGGY")
    
    print(pygame)
            
    

    #posSouris = JoueurH.CliqueSouris(event, MOUSEBUTTONDOWN)
    #MoteurDeJeu.Placer(posSouris)
