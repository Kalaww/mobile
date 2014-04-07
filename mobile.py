#!/usr/bin/python3.3
from tkinter import *
from tkinter.messagebox import *
import math

def startMobile(mobile):
    if type(mobile) is not Poid:
        mobile.setDistance()
    afficher(canvas, mobile)

#Lit un fichier et reconnais le format, renvoi le mobile contruit
def lireFichier():
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

#Construit le mobile selon une liste d'un mobile déjà formé
def constrMobile(l):
	n = Noeud()
	if type(l[0]) is int:
	    n.gauche = Poid(l[0])
	elif type(l[0]) is list:
	    n.gauche = constrMobile(l[0])
	if len(l) < 2:
	    return n.gauche
	
	if type(l[1]) is int:
	    n.droit = Poid(l[1])
	elif type(l[1]) is list:
	    n.droit = constrMobile(l[1])
	return n

def constrParDiffEquilibre(l):
    n = Noeud()
    if len(l) < 2:
        n = Poid(l[0])
        return n
    n.gauche = Poid(l[0])
    n.droit = Poid(l[1])
    
    for i in range(2, len(l)):
        n = n.constrParDiffEquilibre(l[i])
    
    return n

#Affiche le mobile n dans la zone de dessin
def afficher(canvas, n):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    canvas.delete("all")
    echelle = 0.5
    echellePoid = (min(width, height)*0.8//len(n))//n.maximum()
    echelleH = height*0.8//n.profondeur()
    
    if type(n) is Poid:
        canvas.create_line(width//2, 0, width//2, height*0.2)
        longueur = echellePoid*n.valeur
        canvas.create_oval(width//2 - longueur//2, height*0.2, width//2 + longueur//2, height*0.2+longueur)
    else:
    	canvas.create_line(width*n.valeur, 0, width*n.valeur, height*0.1)
    	dessineNoeud(canvas, n, width//2, height*0.1, echelle, echellePoid, echelleH)
    
    canvas.update()
    
#Dessine un noeud de l'arbre représentant le mobile n dans la zone de dessin
def dessineNoeud(canvas, n, x, y, echelle, echellePoid, echelleH):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    xG = x - width*echelle*n.valeur
    xD = xG+echelle*width
    canvas.create_line(xG, y, xD, y)
    canvas.create_line(xG, y, xG, y+echelleH)
    canvas.create_line(xD, y, xD, y+echelleH)
    
    if type(n.droit) is Poid:
        longueur = echellePoid*n.droit.valeur
        canvas.create_oval(xD-longueur//2, y+echelleH, xD+longueur//2, y+echelleH+longueur)
        canvas.create_text(xD, y+echelleH+longueur//2, text=str(n.droit))
    else:
        dessineNoeud(canvas, n.droit, xD, y+echelleH, echelle*echelle, echellePoid, echelleH)
    if type(n.gauche) is Poid:
        longueur = echellePoid*n.gauche.valeur
        canvas.create_oval(xG-longueur//2, y+echelleH, xG+longueur//2, y+echelleH+longueur)
        canvas.create_text(xG, y+echelleH+longueur//2, text=str(n.gauche))
    else:
        dessineNoeud(canvas, n.gauche, xG, y+echelleH, echelle*echelle, echellePoid, echelleH)
    

#### NOEUD ####
class Noeud:
    
    def __init__(self):
        self.valeur = 0
        self.gauche = None
        self.droit = None
    
    def __str__(self):
        return "("+str(self.gauche)+","+str(self.droit)+")"
    
    def __getattr__(self, nom):
        print("Pas d'attribut ",nom," dans un objet Poid")
        
    def peser(self):
        return self.gauche.peser() + self.droit.peser()
    
    def setDistance(self):
        if type(self.gauche) is Noeud:
            self.gauche.setDistance()
        if type(self.droit) is Noeud:
            self.droit.setDistance()
        self.valeur = self.droit.peser() / (self.gauche.peser()+self.droit.peser())
        print("VALEUR = {}".format(+self.valeur))
    
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
            n.droit = Poid(v)
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


#### POID ####
class Poid(Noeud):
    
    def __init__(self, v):
        self.valeur = v
    
    def __str__(self):
        return str(self.valeur)
    
    def __getattr__(self, nom):
        print("Pas d'attribut ",nom," dans un objet Poid")
    
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
        p.droit = Poid(v)
        return p
        

#### MAIN ####

if __name__ == "__main__":
    #mobile
    mobile = Noeud()

    #création de la fenêtre
    fenetre = Tk()

    #création de la zone de paramétrage
    param = Frame(fenetre, borderwidth=2)
    param.pack(pady=10)
    labelFichier = Label(param, text="Nom du fichier")
    labelFichier.pack(side=LEFT, padx=5)
    nomFichier = StringVar()
    entreeFichier = Entry(param, textvariable=nomFichier)
    entreeFichier.pack(side=LEFT, padx=5)
    boutonFichier = Button(param, text="Charger", command=lireFichier)
    boutonFichier.pack(side=LEFT, padx=5)

    #création du canvas
    canvas = Canvas(fenetre,width=800, height=600, background="white")
    canvas.pack()
    canvas.update()

    fenetre.mainloop()
