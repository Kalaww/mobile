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
    l = list()
    mobile.toList(l)
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

#Affiche le mobile n dans la zone de dessin
def afficher(canvas, n):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    canvas.delete("all")
    echellePoids = width//largeurArbre(n)
    echelleH = height*0.8//n.profondeur()
    
    if type(n) is Poids:
        canvas.create_line(width//2, 0, width//2, height*0.2)
        longueur = echellePoids*n.valeur
        canvas.create_oval(width//2 - longueur//2, height*0.2, width//2 + longueur//2, height*0.2+longueur)
    else:
    	canvas.create_line(width*n.valeur, 0, width*n.valeur, height*0.1)
    	dessineNoeud(canvas, n, width//2, height*0.1, echellePoids, echelleH)
    
    canvas.update()
    
#Dessine un noeud de l'arbre représentant le mobile n dans la zone de dessin
def dessineNoeud(canvas, n, x, y, echellePoids, echelleH):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    largeurNoeud = n.largeurNoeud(echellePoids)
    xG = x - largeurNoeud*n.valeur//2
    xD = xG + largeurNoeud//2
    canvas.create_line(xG, y, xD, y)
    canvas.create_line(xG, y, xG, y+echelleH)
    canvas.create_line(xD, y, xD, y+echelleH)
    
    if type(n.droit) is Poids:
        longueur = echellePoids*n.droit.valeur
        canvas.create_oval(xD-longueur//2, y+echelleH, xD+longueur//2, y+echelleH+longueur)
        canvas.create_text(xD, y+echelleH+longueur//2, text=str(n.droit))
    else:
        dessineNoeud(canvas, n.droit, xD, y+echelleH, echellePoids, echelleH)
    if type(n.gauche) is Poids:
        longueur = echellePoids*n.gauche.valeur
        canvas.create_oval(xG-longueur//2, y+echelleH, xG+longueur//2, y+echelleH+longueur)
        canvas.create_text(xG, y+echelleH+longueur//2, text=str(n.gauche))
    else:
        dessineNoeud(canvas, n.gauche, xG, y+echelleH, echellePoids, echelleH)

#Affiche le mobile n dans la zone de dessin
def afficherPhysique(canvas, n):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    canvas.delete("all")
    echellePoids = min(height,width)*0.4//max(largeurArbre(n), n.profondeur())
    echelleH = height*0.8//n.profondeur()
    
    if type(n) is Poids:
        canvas.create_line(width//2, 0, width//2, height*0.2)
        longueur = echellePoids*n.valeur
        canvas.create_oval(width//2 - longueur//2, height*0.2, width//2 + longueur//2, height*0.2+longueur)
    else:
    	canvas.create_line(width*n.valeur, 0, width*n.valeur, (int)(height*0.1))
    	dessineNoeudPhysique(canvas, n, width//2, (int)(height*0.1), echellePoids, echellePoids)
    
    canvas.update()

#Dessine un noeud de l'arbre représentant le mobile n dans la zone de dessin
def dessineNoeudPhysique(canvas, n, x, y, echellePoids, echelleH):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    
    rayon = n.largeurNoeud(echellePoids)//4
    masse = n.masse()*echellePoids
    print(" RAYON {0} : MASSE {1}".format(rayon, masse))
    angle = math.asin(masse/rayon)
    print("ANGLE : {0} {1}".format(angle, angle*180//math.pi))
    
    xG = x - (int)(rayon*math.cos(angle))
    yG = y - (int)(rayon*math.sin(angle))
    print("TEST : {}".format(rayon*math.sin(angle)))
    
    print(x,",",y," - ", xG,",", yG)
    
    xD = (int)(xG+2*(xG-x))
    yD = (int)(yG+2*(yG-y))
    
    canvas.create_line(xG, yG, xD, yD)
    canvas.create_line(xG, yG, xG, yG+echelleH)
    canvas.create_line(xD, yD, xD, yD+echelleH)
    
    if type(n.droit) is Poids:
        longueur = echellePoids*n.droit.valeur
        canvas.create_oval(xD-longueur//2, yD+echelleH, xD+longueur//2, yD+echelleH+longueur)
        canvas.create_text(xD, yD+echelleH+longueur//2, text=str(n.droit))
    else:
        dessineNoeudPhysique(canvas, n.droit, xD, yD+echelleH, echellePoids, echelleH)
    if type(n.gauche) is Poids:
        longueur = echellePoids*n.gauche.valeur
        canvas.create_oval(xG-longueur//2, yG+echelleH, xG+longueur//2, yG+echelleH+longueur)
        canvas.create_text(xG, yG+echelleH+longueur//2, text=str(n.gauche))
    else:
        dessineNoeudPhysique(canvas, n.gauche, xG, yG+echelleH, echellePoids, echelleH)

def largeurArbre(n):
    l = list()
    n.toList(l)
    return sum(l)
    
def draw(canvas, n):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    
    hauteur = n.maximum()
    n.coordPhysique()
    
    drawNoeud(canvas, n, width//2, 0, hauteur)
    
def drawNoeud(canvas, n, x, y, hauteur):
    
    if type(n) is Poids:
        canvas.create_oval(x - n.valeur//2, y, x + n.valeur//2, y + n.valeur)
    else:
        canvas.create_line(x + n.gauche.x, y + n.gauche.y, x + n.droit.x, y + n.droit.y)
        canvas.create_line(x + n.gauche.x, y + n.gauche.y, x + n.gauche.x, y + n.gauche.y + hauteur)
        canvas.create_line(x + n.droit.x, y + n.droit.y, x + n.droit.x, y + n.droit.y + hauteur)
        drawNoeud(canvas, n.gauche, x + n.gauche.x, y + n.gauche.y, hauteur)
        drawNoeud(canvas, n.droit, x + n.droit.x, y + n.droit.y, hauteur)

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
        
    def peser(self):
        return self.gauche.peser() + self.droit.peser()
    
    def setDistance(self):
        if type(self.gauche) is Noeud:
            self.gauche.setDistance()
        if type(self.droit) is Noeud:
            self.droit.setDistance()
        self.valeur = self.droit.peser() / (self.gauche.peser()+self.droit.peser())
    
    def maximum(self):
        g = self.gauche.maximum()
        d = self.droit.maximum()
        if g > d:
            return g
        else:
            return d
    
    def __len__(self):
        return len(self.gauche) + len(self.droit)
        
    def profondeur(self):
        g = self.gauche.profondeur()
        d = self.droit.profondeur()
        if g > d:
            return g+1
        else:
            return d+1
    
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
    
    def toList(self, l):
        self.gauche.toList(l)
        self.droit.toList(l)
    
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
        
    def masse(self):
        g = self.gauche.peser()
        d = self.droit.peser()
        return g-d
    
    def coordPhysique(self):
        rayon = self.largeurNoeud()//4+1
        masse = self.masse()
        print("RAYON :{0}  MASSE :{1}".format(rayon, masse))
        angle = math.asin(masse)
        
        self.coordG.x = (int)(rayon*math.cos(angle))
        self.coordG.y = (int)(rayon*math.sin(angle))
        
        self.coordD.x = -self.coordG.x
        self.coordD.y = -self.coordG.y
        
        if type(self.gauche) is not Poids:
            self.gauche.coordPhysique()
        
        if type(self.droit) is not Poids:
            self.droit.coordPhysique()


#### POID ####
class Poids(Noeud):
    
    def __init__(self, v):
        self.valeur = v
        self.coord = Coord()
    
    def __str__(self):
        return str(self.valeur)
    
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
    
    def toList(self, l):
        l.append(self.valeur)

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
