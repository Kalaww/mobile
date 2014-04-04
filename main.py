import tkinter

def main():
    fichier = open("test.txt", "r")
    ligne = fichier.readline()
    
    liste = eval(ligne)
    print(liste)
    n = build(liste)
    print(n)
    n.setDistance()
    
    fenetre = tkinter.Tk()
    canvas = tkinter.Canvas(fenetre,width=400, height=400, background="white")
    canvas.pack()
    canvas.update()
    afficher(canvas, n)
    fenetre.mainloop()
    
    fichier.close()
    
def build(l):
	n = Noeud()
	if type(l[0]) is int:
	    print("0 est un int")
	    n.gauche = Poid(l[0])
	elif type(l[0]) is list:
	    n.gauche = build(l[0])
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
    hauteur = height*0.1
    dessineNoeud(canvas, n, width//2, height*0.1, echelle, hauteur)
    
    canvas.update()
    
    
def dessineNoeud(canvas, n, x, y, echelle, hauteur):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    xS = x - width*echelle//2
    canvas.create_line(xS, y, xS+width*echelle, y)
    canvas.create_line(xS, y, xS, y+hauteur)
    canvas.create_line(xS+width*echelle, y, xS+width*echelle, y+hauteur)
    
    if type(n.gauche) is Poid:
    
    
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


class Poid:
    
    def __init__(self, v):
        self.valeur = v
    
    def __str__(self):
        return str(self.valeur)
    
    def __getattr__(self, nom):
        print("Pas d'attribut ",nom," dans un objet Poid")
    
    def peser(self):
        return self.valeur
