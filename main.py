import tkinter
import math

def main():
    fichier = open("test.txt", "r")
    ligne = fichier.readline()
    
    liste = eval(ligne)
    print(liste)
    n = build(liste)
    print(n)
    if type(n) is not Poid:
        n.setDistance()
    
    fenetre = tkinter.Tk()
    canvas = tkinter.Canvas(fenetre,width=800, height=600, background="white")
    canvas.pack()
    canvas.update()
    afficher(canvas, n)
    fenetre.mainloop()
    
    fichier.close()
    
def build(l):
	n = Noeud()
	if type(l[0]) is int:
	    n.gauche = Poid(l[0])
	elif type(l[0]) is list:
	    n.gauche = build(l[0])
	if len(l) < 2:
	    return n.gauche
	
	if type(l[1]) is int:
	    n.droit = Poid(l[1])
	elif type(l[1]) is list:
	    n.droit = build(l[1])
	return n

def afficher(canvas, n):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    canvas.delete("all")
    echelle = 0.5
    echellePoid = (min(width, height)*0.8//len(n))//n.maximum()
    echelleH = height*0.8//n.profondeurMax()
    
    if type(n) is Poid:
        canvas.create_line(width//2, 0, width//2, height*0.2)
        longueur = echellePoid*n.valeur
        canvas.create_oval(width//2 - longueur//2, height*0.2, width//2 + longueur//2, height*0.2+longueur)
    else:
    	canvas.create_line(width*n.valeur, 0, width*n.valeur, height*0.1)
    	dessineNoeud(canvas, n, width//2, height*0.1, echelle, echellePoid, echelleH)
    
    canvas.update()
    
    
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
    else:
        dessineNoeud(canvas, n.droit, xD, y+echelleH, echelle*echelle, echellePoid, echelleH)
    if type(n.gauche) is Poid:
        longueur = echellePoid*n.gauche.valeur
        canvas.create_oval(xG-longueur//2, y+echelleH, xG+longueur//2, y+echelleH+longueur)
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
        
    def profondeurMax(self):
        g = self.gauche.profondeurMax()
        d = self.droit.profondeurMax()
        if g > d:
            return g+1
        else:
            return d+1


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
    
    def profondeurMax(self):
        return 1
