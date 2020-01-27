import tkinter
from tkinter import messagebox
import random
import time
import numpy as np

#################################################################################
#
#  Parametres du jeu

canvas = None   # zone de dessin

#Grille[0][0] désigne la case en haut à gauche
#Grille[2][0] désigne la case en haut à droite
#Grille[0][2] désigne la case en bas à gauche

Grille = []
           
Scores = [0,0]   # score du joueur 1 (Humain) et 2 (IA)

TourJoueur = True

def Initialisation():
    global Grille
    time.sleep(1.5)
    Grille = [ [0,0,0], 
               [0,0,0], 
               [0,0,0] ] # attention les lignes représentent les colonnes de la grille
    Affiche()

#



###############################################################################
#
# gestion du joueur humain et de l'IA
# VOTRE CODE ICI 

def Play(x,y):
    if not Grille[x][y]:
        Grille[x][y] = 1
        Affiche(DetectionGagnant())
        time.sleep(0.25)
        TourJoueur = False
        IAPlay()

def CasesDisponibles():
    return [(i, j) for i, col in enumerate(Grille) for j, elm in enumerate(col) if elm == 0]

def IAPlay():
    # caseDispo = CasesDisponibles()
    # idAlea = random.randrange( len(caseDispo) )
    # caseAleat = caseDispo[idAlea]
    caseOpti = JoueurSimule(2)
    Grille[ caseOpti[1][0] ][ caseOpti[1][1] ] = 2
    Affiche(DetectionGagnant())
    time.sleep(0.5)
    TourJoueur = True

def JoueurSimule(idJoueur):
    if DetectionGagnant() != 0:
        return (CalculScore(), None)
    listeCoups = CasesDisponibles()
    if len(listeCoups) == 9:
        return (None, (0,0))
    resultats = []
    for coup in listeCoups:
        Grille[ coup[0] ][ coup[1] ] = idJoueur
        if idJoueur == 2:
            score = JoueurSimule(1)[0]
            gain = score[1] - score[0]
        else:
            score = JoueurSimule(2)[0]
            gain = score[0] - score[1]
        resultats.append( (gain, score, coup) )
        Grille[ coup[0] ][ coup[1] ] = 0
    resOpti = max(resultats, key=lambda resultat: resultat[0])
    return (resOpti[1], resOpti[2])

def CalculScore():
    gagnant = DetectionGagnant()
    if gagnant == 1:
        return (1,0)
    elif gagnant == 2:
        return (0,1)
    else:
        return(0,0)

def MatchNul(sommesLignes):
    nbLigneBloquee = 0
    for somme in sommesLignes:
        if somme in [5,6,9]:
            nbLigneBloquee += 1
    if nbLigneBloquee == len(sommesLignes):
        return True
    else:
        return False

def DetectionGagnant():
    smColone0, smColone1, smColone2 = sum(np.array(Grille[0])**2), sum(np.array(Grille[1])**2), sum(np.array(Grille[2])**2)
    smLigne0=smLigne1=smLigne2=smDiag0=smDiag1 = 0
    for i in range(len(Grille)):
        smLigne0 += Grille[i][0]**2
        smLigne1 += Grille[i][1]**2
        smLigne2 += Grille[i][2]**2
        smDiag0 += Grille[i][i]**2
        smDiag1 += Grille[i][len(Grille)-1-i]**2
    sommes = [ smColone0, smColone1, smColone2,
               smLigne0, smLigne1, smLigne2,
               smDiag0, smDiag1 ]
    if(3 in sommes ):
        return 1
    elif (12 in sommes):
        return 2
    elif (MatchNul(sommes)):
        return 3
    else:
        return 0
    
################################################################################
#    
# Dessine la grille de jeu

def Affiche(PartieGagnee = 0):
        ## DOC canvas : http://tkinter.fdex.eu/doc/caw.html
        canvas.delete("all")
        
        fillgrille = "blue"
        fillcoul = 'gray'
        
        if (PartieGagnee == 1):
            fillgrille = fillcoul="red"
            Scores[0] += 1
        elif (PartieGagnee == 2):
            fillgrille = fillcoul="yellow"
            Scores[1] += 1
        elif (PartieGagnee == 3):
            fillgrille = fillcoul = "white"
        
        for i in range(4):
            canvas.create_line(i*100,0,i*100,300,fill=fillgrille, width="4" )
            canvas.create_line(0,i*100,300,i*100,fill=fillgrille, width="4" )
            
        for x in range(3):
            for y in range(3):
                xc = x * 100 
                yc = y * 100 
                if ( Grille[x][y] == 1):
                    canvas.create_line(xc+10,yc+10,xc+90,yc+90,fill="red", width="4" )
                    canvas.create_line(xc+90,yc+10,xc+10,yc+90,fill="red", width="4" )
                if ( Grille[x][y] == 2):
                    canvas.create_oval(xc+10,yc+10,xc+90,yc+90,outline="yellow", width="4" )
        
        msg = 'SCORES : ' + str(Scores[0]) + '-' + str(Scores[1])
        canvas.create_text(150,400, font=('Helvetica', 30), text = msg, fill=fillcoul)
        canvas.update()   #force la mise a jour de la zone de dessin

        if (PartieGagnee):
            #time.sleep(1.5)
            Initialisation()
        
  
####################################################################################
#
#  fnt appelée par un clic souris sur la zone de dessin

def MouseClick(event):
    global TourJoueur
    if TourJoueur:
        window.focus_set()
        x = event.x // 100  # convertit une coordonée pixel écran en coord grille de jeu
        y = event.y // 100
        if ( (x<0) or (x>2) or (y<0) or (y>2) ) : return
        
        
        print("clicked at", x,y)
        
        Play(x,y)  # gestion du joueur humain et de l'IA

#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

# fenetre
window = tkinter.Tk()
window.geometry("300x500") 
window.title('Mon Super Jeu')
window.protocol("WM_DELETE_WINDOW", lambda : window.destroy())
window.bind("<Button-1>", MouseClick)

#zone de dessin
WIDTH = 300
HEIGHT = 500
canvas = tkinter.Canvas(window, width=WIDTH , height=HEIGHT, bg="#000000")
canvas.place(x=0,y=0)
Initialisation()
 
# active la fenetre 
window.mainloop()


  


    
        

      
 

