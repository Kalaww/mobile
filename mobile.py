#!/usr/bin/python3.3
from tkinter import *
from tkinter.messagebox import *
import math

#Initialise le mobile et l'affiche
def startMobile(mobile):
    if type(mobile) is not Poids:
        mobile.setDistance()
    draw(canvas, mobile)

#Lit un fichier et reconnais le format, renvoi le mobile contruit
def lireFichier():
    global mobile
    nom = nomFichier.get()
    fichier = open(nom, "r")
    if fichier == None:
        showwarning("Echec", "Aucun fichier de ce nom est présent")
        return
    lignes = fichier.readlines()
    fichier.close()
    if len(lignes) == 0:
        showwarning("Echec", "Le fichier est vide")
        return
    if len(lignes) == 1:
        l = eval(lignes[0])
        mobile = constrMobile(l)
    else:
        l = list()
        for i in lignes:
            k = i[:-1]
            if len(k) > 0:
                l.append(int(k))
        mobile = constrParDiffEquilibre(l)
    
    startMobile(mobile)

#Sauvegarde le mobile dans le fichier
def saveMobile():
    global mobile
    nom = nomFichierSave.get()
    fichier = open(nom, "w")
    fichier.write(str(mobile))
    print("TEST : {}".format(mobile))
    fichier.close()

#Sauvegarde de la liste des poids d'un mobile dans un fichier
def saveList():
    global mobile
    nom = nomFichierSave.get()
    fichier = open(nom, "w")
    l = mobile.toList()
    for i in l:
        fichier.write(str(i)+"\n")
    fichier.write("\n")
    fichier.close()

#Construit le mobile selon une liste d'un mobile déjà formé
def constrMobile(l):
	n = Noeud()
	if type(l[0]) is int:
	    n.gauche = Poids(l[0])
	elif type(l[0]) is list:
	    n.gauche = constrMobile(l[0])
	if len(l) < 2:
	    return n.gauche
	
	if type(l[1]) is int:
	    n.droit = Poids(l[1])
	elif type(l[1]) is list:
	    n.droit = constrMobile(l[1])
	return n

#Construit le mobile selon un algorithme d'arbre équilibré d'une profondeur minimale
def constrParDiffEquilibre(l):
    n = Noeud()
    if len(l) < 2:
        n = Poids(l[0])
        return n
    n.gauche = Poids(l[0])
    n.droit = Poids(l[1])
    
    for i in range(2, len(l)):
        n = n.constrParDiffEquilibre(l[i])
    
    return n

#Dessine l'arbre du mobile sur le canvas à l'échelle
def draw(canvas, n):
    canvas.delete("all")
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    
    hauteur = n.maximum()
    n.calculCoord()
    echelleW = width // n.largeurMax()
    echelleH = height // n.hauteurMax()
    echelle = min(echelleW, echelleH)*0.9
    
    drawNoeud(canvas, n, width//2, 0, hauteur)
    canvas.scale("all", width//2, 0, echelle, echelle)
    canvas.update()

#Dessine le noeud sur le canvas à la position x,y
def drawNoeud(canvas, n, x, y, hauteur):
    canvas.create_line(x, y, x, y + hauteur)
    
    if type(n) is Poids:
        canvas.create_oval(x - n.valeur//2, y + hauteur - n.valeur//2, x + n.valeur//2, y + hauteur + n.valeur//2, fill=colorNoeud(n.valeur, hauteur))
        canvas.create_text(x, y + hauteur, text=str(n))
    else:
        canvas.create_line(x + n.coordG.x, y + hauteur + n.coordG.y, x + n.coordD.x, y + hauteur + n.coordD.y)
        drawNoeud(canvas, n.gauche, x + n.coordG.x, y + n.coordG.y + hauteur, hauteur)
        drawNoeud(canvas, n.droit, x + n.coordD.x, y + n.coordD.y + hauteur, hauteur)

#Defini une couleur en hexadecimal en fonction de la valeur
def colorNoeud(valeur, maximum):
    a = valeur*15//maximum
    b = (a + 5)%16
    c = (a + 10)%16
    r = ""
    if a == 10:
        r = r+"a"
    elif a == 11:
        r = r+"b"
    elif a == 12:
        r = r+"c"
    elif a == 13:
        r = r+"d"
    elif a == 14:
        r = r+"e"
    elif a == 15:
        r = r+"f"
    else:
        r = r+str(a)
    
    if b == 10:
        r = r+"a"
    elif b == 11:
        r = r+"b"
    elif b == 12:
        r = r+"c"
    elif b == 13:
        r = r+"d"
    elif b == 14:
        r = r+"e"
    elif b == 15:
        r = r+"f"
    else:
        r = r+str(b)
    
    if c == 10:
        r = r+"a"
    elif c == 11:
        r = r+"b"
    elif c == 12:
        r = r+"c"
    elif c == 13:
        r = r+"d"
    elif c == 14:
        r = r+"e"
    elif c == 15:
        r = r+"f"
    else:
        r = r+str(c)
    return "#"+r

#### NOEUD ####
class Noeud:
    
    def __init__(self):
        self.valeur = 0
        self.gauche = None
        self.droit = None
        self.coordG = Coord()
        self.coordD = Coord()
    
    def __str__(self):
        return "["+str(self.gauche)+","+str(self.droit)+"]"
    
    def __getattr__(self, nom):
        print("Pas d'attribut ",nom," dans un objet Poids")
    
    #Poids total de l'arbre
    def peser(self):
        return self.gauche.peser() + self.droit.peser()
    
    #Distance du sous arbre gauche selon les moments de torsion
    def setDistance(self):
        if type(self.gauche) is Noeud:
            self.gauche.setDistance()
        if type(self.droit) is Noeud:
            self.droit.setDistance()
        self.valeur = self.droit.peser() / (self.gauche.peser()+self.droit.peser())
    
    #Poids max de l'arbre
    def maximum(self):
        g = self.gauche.maximum()
        d = self.droit.maximum()
        if g > d:
            return g
        else:
            return d
    
    def __len__(self):
        return len(self.gauche) + len(self.droit)
    
    #Profondeur de l'arbre   
    def profondeur(self):
        g = self.gauche.profondeur()
        d = self.droit.profondeur()
        if g > d:
            return g+1
        else:
            return d+1
    
    #Construit le mobile selon un algorithme d'arbre équilibré d'une profondeur minimale
    def constrParDiffEquilibre(self, v):
        poidG = self.gauche.peser()
        poidD = self.droit.peser()
        if v >= (poidG+poidD):
            n = Noeud()
            n.gauche = self
            n.droit = Poids(v)
            return n
        if poidG == poidD:
            if self.gauche.profondeur() > self.droit.profondeur():
                self.droit = self.droit.constrParDiffEquilibre(v)
            else:
                self.gauche = self.gauche.constrParDiffEquilibre(v)
        elif poidG > poidD :
            self.droit = self.droit.constrParDiffEquilibre(v)
        else:
            self.gauche = self.gauche.constrParDiffEquilibre(v)
        return self
    
    #Liste des poids
    def toList(self):
        return self.gauche.toList().extend(self.droit.toList())
    
    #Largeur du noeud
    def largeurNoeud(self):
        g = 0
        d = 0
        if type(self.gauche) is Poids:
            g = self.gauche.valeur
        else:
            g = self.gauche.largeurNoeud()
        
        if type(self.droit) is Poids:
            d = self.droit.valeur
        else:
            d = self.droit.largeurNoeud()
        
        return g+d
    
    #Masse de noeud : difference des poids
    def masse(self):
        g = self.gauche.peser()
        d = self.droit.peser()
        return g-d
    
    #Calcul des coordonnees pour le cas des moments de torsion
    def calculCoord(self):
        largeur = self.largeurNoeud()//2
        self.coordG.x = -largeur*self.valeur
        self.coordG.y = 0
        self.coordD.x = self.coordG.x + largeur
        self.coordD.y = 0
        
        if type(self.gauche) is not Poids:
            self.gauche.calculCoord()
        
        if type(self.droit) is not Poids:
            self.droit.calculCoord()
    
    #Calcul des coordonnees pour le cas prise en compte des valeurs des poids
    def calculCoordPhysique(self):
        rayon = self.largeurNoeud()//4+1
        masse = self.masse()
        print("RAYON :{0}  MASSE :{1}".format(rayon, masse))
        angle = math.asin(masse)
        
        self.coordG.x = (int)(rayon*math.cos(angle))
        self.coordG.y = (int)(rayon*math.sin(angle))
        
        self.coordD.x = -self.coordG.x
        self.coordD.y = -self.coordG.y
        
        if type(self.gauche) is not Poids:
            self.gauche.calculCoordPhysique()
        
        if type(self.droit) is not Poids:
            self.droit.calculCoordPhysique()
    
    #Largeur de l'arbre
    def largeurMax(self):
        return - self.gauche.largeurMaxGauche() + self.droit.largeurMaxDroit()
    
    #Largeur du côté gauche
    def largeurMaxGauche(self):
        return self.coordG.x + self.gauche.largeurMaxGauche()
    
    #Largeur du côté droit
    def largeurMaxDroit(self):
        return self.coordD.x + self.droit.largeurMaxDroit()
    
    #Hauteur de l'arbre
    def hauteurMax(self):
        maximum = self.maximum()
        return maximum * self.profondeur() + maximum//2

#### POID ####
class Poids(Noeud):
    
    def __init__(self, v):
        self.valeur = v +1
        self.coord = Coord()
    
    def __str__(self):
        return str(self.valeur-1)
    
    def __getattr__(self, nom):
        print("Pas d'attribut ",nom," dans un objet Poids")
    
    def peser(self):
        return self.valeur
    
    def maximum(self):
        return self.valeur
    
    def __len__(self):
        return 1
    
    def profondeur(self):
        return 1
    
    def constrParDiffEquilibre(self, v):
        p = Noeud()
        p.gauche = self
        p.droit = Poids(v)
        return p
    
    def toList(self):
        return [self.valeur-1]
        
    def largeurMaxGauche(self):
        return -self.valeur//2
    
    def largeurMaxDroit(self):
        return self.valeur//2

class Coord:
    def __init__(self):
        self.x = 0
        self.y = 0
        

#### MAIN ####

if __name__ == "__main__":
    #mobile
    mobile = Noeud()

    #création de la fenêtre
    fenetre = Tk()

    #création de la zone de paramétrage
    param = Frame(fenetre, borderwidth=2)
    param.pack(pady=10)
    paramLecture = LabelFrame(param, borderwidth=2, text="Charger un fichier")
    paramLecture.pack(side=LEFT, padx=10)
    paramSave = LabelFrame(param, borderwidth=2, text="Sauvegarder un mobile")
    paramSave.pack(side=LEFT, padx=10)
    
    #Zone de lecture d'un fichier
    labelFichier = Label(paramLecture, text="Nom du fichier")
    labelFichier.pack(side=LEFT, padx=10, pady=10)
    nomFichier = StringVar()
    entreeFichier = Entry(paramLecture, textvariable=nomFichier)
    entreeFichier.pack(side=LEFT, padx=10, pady=10)
    boutonFichier = Button(paramLecture, text="Charger", command=lireFichier)
    boutonFichier.pack(side=LEFT, padx=10, pady=10)
    
    #Zone de sauvegarde d'un mobile
    labelFichierSave = Label(paramSave, text="Nom du fichier")
    labelFichierSave.pack(side=LEFT, padx=10, pady=10)
    nomFichierSave = StringVar()
    entreeFichierSave = Entry(paramSave, textvariable=nomFichierSave)
    entreeFichierSave.pack(side=LEFT, padx=10, pady=10)
    boutonFichierSave = Button(paramSave, text="Sauvegarder", command=saveMobile)
    boutonFichierSave.pack(side=LEFT, padx=10, pady=10)

    #création du canvas
    canvas = Canvas(fenetre,width=800, height=600, background="white")
    canvas.pack()
    canvas.update()

    fenetre.mainloop()
