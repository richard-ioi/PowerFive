#! /usr/bin/env python3

"""
    Module définissant les modèles du jeu
"""

import pygame, os, random, copy

class Jeton:
    """
        Classe représentant les jetons du jeu.
    """
    
    nbJetons = 0
    
    def __init__(self, idJoueur, x=0, y=0):
        """
            Constructeur de la classe.

            Args:
                col: colonne du jeton dans la grille
                case: case du jeton
                idJoueur: Identifiant du joueur
                image: Sprite du jeton
        """
        self.idJoueur = idJoueur
        self.x = x
        self.y = y
        self.numero = Jeton.nbJetons
        
        self.vitesse = 2
        self.acceleration = 1.5
        self.visible = False
        self.sprite = pygame.transform.scale( pygame.image.load( os.path.join("data","graphismes","jeton_jaune.png") ), (10*4,12*4) ) if idJoueur == 1 \
                     else pygame.transform.scale( pygame.image.load( os.path.join("data","graphismes","jeton_rouge.png") ), (10*4,12*4) )
    
    def __repr__(self):
        return "Jeton({}, {})".format(self.idJoueur, self.visible)
    
    def __eq__(self, other):
        return self.idJoueur == other

class Grille:
    """
        Classe représentant la grille du jeu et regroupant ses méthodes de manipulations.
    """

    def __init__(self):
        """
            Constructeur de la classe.

            Args:
                grillePrincipal: Liste 2D représentant la grille du jeu.
                largeur: Largeur de la grille.
                hauteur: Hauteur de la grille.
                sprites: Sprites de la grille de jeu.
                dimSprites: Dimensions des sprites
        """
                               #y 0 1 2 3 4 5 6 7  8     x
        self.grillePrincipal = [ [0,0,0,0,0,0,0,0,-1],  #0
                                 [0,0,0,0,0,0,0,0,-1],  #1
                                 [0,0,0,0,0,0,0,0,-1],  #2
                                 [0,0,0,0,0,0,0,0,-1],  #3
                                 [0,0,0,0,0,0,0,0,-1],  #4
                                 [0,0,0,0,0,0,0,0,-1],  #5
                                 [0,0,0,0,0,0,0,0,-1],  #6
                                 [0,0,0,0,0,0,0,0,-1],  #7
                                 [0,0,0,0,0,0,0,0,-1] ] #8
        self.grilleSauvegarde = None
        self.largeur = 9
        self.hauteur = 8
        self.sprites = {
            "avant": pygame.transform.scale(pygame.image.load(os.path.join("data","graphismes","grille.png")), (140*4,141*4)),
            "arriere": pygame.transform.scale(pygame.image.load(os.path.join("data","graphismes","grille_back.png")), (140*4,141*4)),
            "ultimate1":pygame.transform.scale(pygame.image.load(os.path.join("data","graphismes","ultimate","ultimate1.png")), (58*3,46*3))
        }
        self.dimSprites = ( self.sprites["top"].get_width(), self.sprites["top"].get_height() )

        def __str__(self):
            """
                Méthode de représentation en chaine de caractère de la grille.

                Return:
                    Une chaine de caractères.
            """
            cases = [case for colonne in list( zip(*self.grillePrincipal) ) for case in colonne]
            return """Grille(largeur={}, hauteur={})
 ___________________________________
| {} | {} | {} | {} | {} | {} | {} | {} | {} |
| {} | {} | {} | {} | {} | {} | {} | {} | {} |
| {} | {} | {} | {} | {} | {} | {} | {} | {} |
| {} | {} | {} | {} | {} | {} | {} | {} | {} |
| {} | {} | {} | {} | {} | {} | {} | {} | {} |
| {} | {} | {} | {} | {} | {} | {} | {} | {} |
| {} | {} | {} | {} | {} | {} | {} | {} | {} |
| {} | {} | {} | {} | {} | {} | {} | {} | {} |
 ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
            """.format(self.largeur, self.hauteur, *cases)

        def casesVides(self):
            """
                Méthode donnant l'ensemble des cases vides disponible dans la grille.

                Return:
                    Une liste de tuples contenant l'index des colonnes et des cases disponibles.
            """
            casesVides = []
            for colonne in range( len(self.grillePrincipal) ):
                for case in range(self.hauteur, -1, -1):
                    if(self.grillePrincipal[colonne][case] == 0):
                        casesVides.append( (colonne, case) )
                        break
            return casesVides
        
        def caseVideColonne(self, colonne, inv = True):
            """
                Méthode donnant l'ensemble des cases vides disponible dans la grille.

                Args:
                    colonne: Colonne à parcourir.
                    inv: Booléen indiquant si le parcours doit être fait de bas en haut.

                Return:
                    Une liste de tuples contenant l'index des colonnes et des cases disponibles.
            """
            if inv:
                for case in range(self.hauteur, -1, -1):
                    if(self.grillePrincipal[colonne][case] == 0):
                        return case
            else:
                for case in range(0, self.hauteur + 1):
                    if(self.grillePrincipal[colonne][case] != 0):
                        return case - 1
            
        def nbJetonColonne(self, colonne):
            """
                Méthode donnant le nombre de jetons dans la colonne donnée en paramètre.

                Args:
                    colonne: Indice de la colonne à analyser.

                Return:
                    Le nombre de jeton de la colonne
            """
            nbJeton = 0
            for jeton in colonne:
                if jeton != 0:
                    nbJeton += 1
            return nbJeton
        
        def casesPleines(self):
            return [(jeton, x, y) for y, colonne in enumerate(self.grillePrincipal) for x, jeton in enumerate(colonne) if jeton == 1 or jeton == 2]
        
        def etatPlacement(self, x, y):
            """
                Méthode indiquant l'état de la grille à une position donné au niveau
                de la ligne, de la colonne et des diagonales.

                Args:
                    x: Position en abscisse
                    y: position en ordonnée
                
                Return:
                    Une dictionnaire contenant la colonne, la ligne et les diagonales de la case.
            """

            # Récupération colonne
            colonne = []
            for elmC in range(0, self.hauteur, 1):
                colonne.append(self.grillePrincipal[x][elmC])

            # Récupération ligne
            ligne = []
            for elmL in range(self.largeur):
                ligne.append(self.grillePrincipal[elmL][y])

            ### Récupération diagonales
            diag0, diag1 = [], []
            diag0_s, diag1_s = {}, {}
            
            ## Diagonale \
            # Calcul case la plus à gauche
            if y >= x: # début sur |
                diag0_s["start"] = (0, y-x)
            if y < x: # début sur --
                diag0_s["start"] = (x-y, 0)

            # Calcul case la plus à droite
            if y <= x-1: # début sur |
                diag0_s["stop"] = ((self.largeur-1), (self.largeur -1) - (x-y))
            if y > x-1: # début sur --
                diag0_s["stop"] = ((self.hauteur-1) - (y-x), self.hauteur-1)

            ## Diagonale /
            # Calcul case la plus à gauche
            if x+y <= 6: # début sur |
                diag1_s["start"] = (0, y+x)
            if x+y > 6: # début sur --
                diag1_s["start"] = (x+y - (self.hauteur-1), self.hauteur -1)
            
            #Calcul case la plus à droite
            if x+y >= 8: # début sur |
                diag1_s["stop"] = ((self.largeur-1), x+y - self.hauteur)
            if x+y < 8: # début sur --
                diag1_s["stop"] = (x+y, 0)
            
            for elmD0 in range(diag0_s["stop"][0] - diag0_s["start"][0] + 1):
                #print(str(diag0_s["start"][0] + elmD0)+' '+str(diag0_s["start"][1] + elmD0))
                diag0.append(self.grillePrincipal[ diag0_s["start"][0] + elmD0 ][ diag0_s["start"][1] + elmD0 ])
            
            for elmD1 in range(diag1_s["stop"][0] - diag1_s["start"][0] + 1):
                diag1.append(self.grillePrincipal[ diag1_s["start"][0] + elmD1 ][ diag1_s["start"][1] - elmD1 ])
            
            return {"ligne" : ligne, "colonne": colonne, "diag1": diag0, "diag2": diag1}
        
        def colonnePleine(self, colonne):
            """
                Méthode booléenne indiquant si la colonne est pleine.

                Args:
                    colonne : Indice de la colonne à analyser.
                
                Return:
                    Un booléen
            """
            return self.NbJetonColonne(colonne) == self.hauteur+1

        def sauvegarderGrille(self):
            copy.deepcopy(self.grillePrincipal, self.grilleSauvegarde)
        
        def remplirCase(self, colonne, idJoueur):
            """
                Méthode remplissant une case de la grille

                Arg:
                    jeton: Jeton devant être placé dans la grille.
            """
            self.sauvegarderGrille()
            case = self.CasesVides()[colonne][1]
            self.grillePrincipal[colonne][case] = idJoueur
        
        def purgerColonne(self, colonne):
            """
                Méthode retirant les cases vides entre les jetons.

                Args:
                    colonne: Indice de la colonne à purger
            """
            debut = self.CaseVideColonne(colonne, inv = False) + 1
            caseUtile = self.grillePrincipal[colonne][debut:]
            if 0 in caseUtile:
                while 0 in caseUtile:
                    caseUtile.remove(0)
                nbZero = len(self.grillePrincipal[colonne]) - len(caseUtile)
                colonnePurgee = [0]
                colonnePurgee *= nbZero
                colonnePurgee += caseUtile
                self.grillePrincipal[colonne] = colonnePurgee[:]
            
        def inverserJeton(self):
            self.sauvegarderGrille()
            for i, colonne in enumerate(self.grillePrincipal):
                for j, case in enumerate(colonne):
                    if case == 1:
                        self.grillePrincipal[i][j] = 2
                    if case == 2:
                        self.grillePrincipal[i][j] = 1
        
        def ejecterDernierJeton(self, colonne):
            self.sauvegarderGrille()
            self.grillePrincipal[colonne] = [0] + self.grillePrincipal[colonne][:-2] + [-1]
        
        def ejecterJetonAleat(self):
            self.sauvegarderGrille()
            colonne = random.randrange(len(self.grillePrincipal))
            if self.hauteur - self.CaseVideColonne(colonne) > 1:
                case = random.randrange( self.CaseVideColonne(colonne) +1, self.hauteur  )
                self.grillePrincipal[colonne][case] = 0
            else:
                self.EjecterJetonAleat()
            self.PurgerColonne(colonne)
        
        def ejecterJetonsAleat(self, n = 2):
            self.sauvegarderGrille()
            for i, colonne in enumerate(self.grillePrincipal):
                k = random.randint(1, n)
                cases = random.choices(range(len(colonne) - 1), k=k)
                print(cases)
                for j in cases:
                    self.grillePrincipal[i][j] = 0
                self.PurgerColonne(i)
        
        def melangerJetons(self):
            self.sauvegarderGrille()
            random.shuffle(self.grillePrincipal)
            for colonne in range(len(self.grillePrincipal)):
                self.PurgerColonne(colonne)
        
        def reinitialiser(self):
            self.grillePrincipal = [[0,0,0,0,0,0,0,0,-1],  #0
                                    [0,0,0,0,0,0,0,0,-1],  #1
                                    [0,0,0,0,0,0,0,0,-1],  #2
                                    [0,0,0,0,0,0,0,0,-1],  #3
                                    [0,0,0,0,0,0,0,0,-1],  #4
                                    [0,0,0,0,0,0,0,0,-1],  #5
                                    [0,0,0,0,0,0,0,0,-1],  #6
                                    [0,0,0,0,0,0,0,0,-1],  #7
                                    [0,0,0,0,0,0,0,0,-1]]  #8
            self.sauvegarderGrille()
