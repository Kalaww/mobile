#!/usr/bin/python3.3
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import math

#Initialise le mobile et l'affiche
def startMobile():
    global mobile
    if type(mobile) is not Poids:
        mobile.setDistance()
    dessine()

#Lit un fichier et reconnais le format, renvoi le mobile contruit
def lireFichier():
    global mobile
    global status
    try:
        nomFichier = askopenfilename(title="Ouvrir un fichier", filetypes=[("fichiers txt",".txt"),("tous fichiers",".*")])
        fichier = open(nomFichier, "r")
    except IOError:
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
        if construction == DIFFEQUI:
            mobile = constrParDiffEquilibre(l)
        elif construction == PPARFAIT:
           mobile = constrPresqueParfaite(l)
        elif construction == MAXGAUCHE:
            mobile = constrParMaxGauche(l)
        elif construction == MAXDROIT:
            mobile = constrParMaxDroit(l)
        elif construction == MINGAUCHE:
            mobile = constrParMinGauche(l)
        elif construction == MINDROIT:
            mobile = constrParMinDroit(l)
    status.set("Fichier chargé : {}".format(nomFichier))
    startMobile()

#Sauvegarde le mobile dans le fichier
def saveMobile():
    global mobile
    nomFichier = asksaveasfilename(title="Sauvegarder un mobile", filetypes=[("fichiers txt",".txt"),("tous fichiers",".*")])
    fichier = open(nomFichier, "w")
    fichier.write(str(mobile))
    fichier.close()

#Sauvegarde de la liste des poids d'un mobile dans un fichier
def saveList():
    global mobile
    nomFichier = asksaveasfilename(title="Sauvegarder un mobile", filetypes=[("fichiers txt",".txt"),("tous fichiers",".*")])
    fichier = open(nomFichier, "w")
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
    
    if len(l) == 0:
        showwarning("Erreur", "La liste de poids est vide")
        return n
    elif len(l) == 1:
        n = Poids(l[0])
        return n
    n.gauche = Poids(l[0])
    n.droit = Poids(l[1])
    
    for i in range(2, len(l)):
        n = n.constrParDiffEquilibre(l[i])
    
    return n

#Construit le mobile de façon a ce que le noeud isGauche est la valeur isMax des noeud fils
def constrExtreme(l, isMax, isGauche):
    n = Noeud()
    l.sort()
    if not isMax:
        l.reverse()
    
    if len(l) == 0:
        showwarning("Erreur", "La liste de poids est vide")
        return n
    elif len(l) == 1:
        n = Poids(l[0])
        return n
    else:
        n.droit = Poids(l[0])
        n.gauche = Poids(l[1])
    
    for i in range(2,len(l)):
        if not isGauche:
            tmp = Noeud()
            tmp.droit = Poids(l[i])
            tmp.gauche = n
            n = tmp
        else:
            tmp = Noeud()
            tmp.gauche = Poids(l[i])
            tmp.droit = n
            n = tmp
    return n

#Construit le mobile le plus équilibrée possible avec une marge d'erreur minimale   
def constrPresqueParfaite(l):
    n = Noeud()
    if len(l) == 0:
        showwarning("Erreur", "La liste de poids est vide")
        return n
    elif len(l) == 1:
        n = Poids(l[0])
        return n
    else:
        demi = sum(l)//2
        b = False
        for i in range(demi):
            b = n.constrPresqueParfaite(l, list(), 0, i)
            if b:
                break
        if not b:
            showwarning("Erreur", "Il n'y a pas de solution pour construire un arbre presque parfait avec ces valeurs")
            return None
        else:
            print("Construit avec un pas de ",i)
            return n

#Dessine l'arbre du mobile sur le canvas à l'échelle
def dessine():
    global canvas
    global mobile
    canvas.delete("all")
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    
    hauteur = mobile.maximum()
    if affichage == CLASSIC:
        mobile.calculCoord()
    elif affichage == PHYSIQUE:
        mobile.calculCoordPhysique()
    echelleW = width // mobile.largeurMax()
    echelleH = height // mobile.hauteurMax()
    echelle = min(echelleW, echelleH)
    
    dessineNoeud(mobile, width//2, 0, hauteur)
    canvas.scale("all", width//2, 0, echelle, echelle)
    canvas.update()

#Dessine le noeud sur le canvas à la position x,y
def dessineNoeud(n, x, y, hauteur):
    global canvas
    canvas.create_line(x, y, x, y + hauteur)
    
    if type(n) is Poids:
        canvas.create_oval(x - n.valeur/2, y + hauteur - n.valeur/2, x + n.valeur/2, y + hauteur + n.valeur/2, fill=colorNoeud(n.valeur, hauteur))
        canvas.create_text(x, y + hauteur, text=str(n))
    else:
        canvas.create_line(x + n.coordG.x, y + hauteur + n.coordG.y, x + n.coordD.x, y + hauteur + n.coordD.y)
        dessineNoeud(n.gauche, x + n.coordG.x, y + n.coordG.y + hauteur, hauteur)
        dessineNoeud(n.droit, x + n.coordD.x, y + n.coordD.y + hauteur, hauteur)

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

#Redessine le mobile selon l'affichage en parametre
def setAffichage(param):
    global affichage
    affichage = param
    if mobile != None :
        dessine()

#Reconstruit le mobile selon la contruction en parametre
def setConstruction(param):
    global construction
    global mobile
    old = construction
    construction = param
    if mobile != None and param != old:
        l = mobile.toList()
        if construction == DIFFEQUI:
            mobile = constrParDiffEquilibre(l)
        elif construction  == PPARFAIT:
            mobile = constrPresqueParfaite(l)
        elif construction == MAXGAUCHE:
            mobile = constrExtreme(l, True, True)
        elif construction == MAXDROIT:
            mobile = constrExtreme(l, True, False)
        elif construction == MINGAUCHE:
            mobile = constrExtreme(l, False, True)
        elif construction == MINDROIT:
            mobile = constrExtreme(l, False, False)
        startMobile()

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
    
    #Construit le mobile le plus équilibré possible récursivement suivant une marge d'erreur donnée
    def constrPresqueParfaite(self, l, save, i, pas):
        if len(l) == 2:
            self.gauche = Poids(l[0])
            self.droit = Poids(l[1])
            return True
        demi = sum(l)//2
        for k in range(i, len(l)):
            if sum(save) + l[k] <= demi+pas:
                save.append(l[k])
            if sum(save) >= demi-pas and sum(save) <= demi+pas:
                bg = False
                bd = False
                if len(save) == 1 :
                    self.gauche = Poids(save[0])
                    bg = True
                else:
                    self.gauche = Noeud()
                    bg = self.gauche.constrPresqueParfaite(save, list(), 0, pas)
                saveOp = [ z for z in l]
                for z in save:
                    saveOp.remove(z)
                if len(saveOp) == 1:
                    self.droit = Poids(saveOp[0])
                    bd = True
                else:
                    self.droit = Noeud()
                    bd = self.droit.constrPresqueParfaite(saveOp, list(), 0, pas)
                if bd and bg:
                    return True
                save.pop(len(save)-1)
        boo = False
        if i < len(l)-1:
            boo = self.constrPresqueParfaite(l, list(), i+1, pas)
        return boo
                
        
        
    
    #Liste des poids
    def toList(self):
        l = self.gauche.toList()
        l.extend(self.droit.toList())
        return l
    
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
        rayon = self.largeurNoeud()/4
        masse = self.masse()/2
        if math.fabs(masse) > rayon:
            angle = math.asin(masse/math.fabs(masse))
        else:
            angle = math.asin(masse/rayon)
           
        self.coordG.x = (-rayon)*math.cos(angle)
        self.coordG.y = rayon*math.sin(angle)
        
        self.coordD.x = -self.coordG.x
        self.coordD.y = -self.coordG.y
        
        if type(self.gauche) is not Poids:
            self.gauche.calculCoordPhysique()
        
        if type(self.droit) is not Poids:
            self.droit.calculCoordPhysique()
    
    #Largeur de l'arbre
    def largeurMax(self):
        g = self.gauche.largeurMaxGauche() + self.coordG.x
        d = self.droit.largeurMaxDroit() + self.coordD.x
        return - g + d
    
    #Largeur du côté gauche
    def largeurMaxGauche(self):
        return self.coordG.x + self.gauche.largeurMaxGauche()
    
    #Largeur du côté droit
    def largeurMaxDroit(self):
        return self.coordD.x + self.droit.largeurMaxDroit()
    
    #Hauteur de l'arbre
    def hauteurMax(self):
        hauteur = self.maximum()
        return self.hauteurMaxRec(hauteur)
    
    def hauteurMaxRec(self, hauteur):
        d = self.coordD.y + self.droit.hauteurMaxRec(hauteur)
        g = self.coordG.y + self.gauche.hauteurMaxRec(hauteur)
        return hauteur + max(d,g)
        

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
    
    def toList(self):
        return [self.valeur]
    
    def largeurMaxGauche(self):
        return -self.valeur//2
    
    def largeurMaxDroit(self):
        return self.valeur//2
    
    def hauteurMax(self):
        hauteur = self.maximum()
        return self.hauteurMaxRec(hauteur)
    
    def hauteurMaxRec(self, hauteur):
        return hauteur + self.valeur//2

class Coord:
    def __init__(self):
        self.x = 0
        self.y = 0
        

#### MAIN ####

if __name__ == "__main__":
    #variables
    CLASSIC = 0
    PHYSIQUE = 1
    affichage = CLASSIC
    
    DIFFEQUI = 0
    MAXGAUCHE = 1
    MAXDROIT = 2
    MINGAUCHE = 3
    MINDROIT = 4
    PPARFAIT = 5
    construction = DIFFEQUI
    
    #mobile
    mobile = None

    #création de la fenêtre
    fenetre = Tk()
    fenetre.geometry("800x600")
    
    #création du menu
    menu = Menu(fenetre)
    
    menufichier = Menu(menu)
    menufichier.add_command(label="Ouvrir",command=lireFichier)
    menufichier.add_command(label="Sauvegarder mobile",command=saveMobile)
    menufichier.add_command(label="Sauvegarder liste des poids",command=saveList)
    menufichier.add_command(label="Quitter",command=fenetre.destroy)
    menu.add_cascade(label="Fichier",menu=menufichier)
    
    menuaffichage = Menu(menu)
    menuaffichage.add_command(label="Affichage classique",command=lambda:setAffichage(CLASSIC))
    menuaffichage.add_command(label="Affichage physique",command=lambda:setAffichage(PHYSIQUE))
    menuaffichage.add_command(label="Reset",command=lambda:canvas.delete("all"))
    menu.add_cascade(label="Affichage",menu=menuaffichage)
    
    fenetre.config(menu=menu)

    #création de la zone de paramétrage
    param = Frame(fenetre, borderwidth=2)
    param.pack(side=TOP, fill=X)
    
    paramConstr = LabelFrame(param, text="Construction du mobile")
    paramConstr.pack(side=LEFT, padx=5)
    boutonConstrDiff = Button(paramConstr, text="Equilibré",command=lambda:setConstruction(DIFFEQUI))
    boutonConstrDiff.pack(side=LEFT, padx=5, pady=5)
    boutonConstrPP = Button(paramConstr, text="Presque parfait", command=lambda:setConstruction(PPARFAIT))
    boutonConstrPP.pack(side=LEFT, padx=5, pady=5)
    boutonConstrMaxG = Button(paramConstr, text="Max gauche", command=lambda:setConstruction(MAXGAUCHE))
    boutonConstrMaxG.pack(side=LEFT, padx=5, pady=5)
    boutonConstrMaxD = Button(paramConstr, text="Max droit", command=lambda:setConstruction(MAXDROIT))
    boutonConstrMaxD.pack(side=LEFT, padx=5, pady=5)
    boutonConstrMinG = Button(paramConstr, text="Min gauche", command=lambda:setConstruction(MINGAUCHE))
    boutonConstrMinG.pack(side=LEFT, padx=5, pady=5)
    boutonConstrMinD = Button(paramConstr, text="Min droit", command=lambda:setConstruction(MINDROIT))
    boutonConstrMinD.pack(side=LEFT, padx=5, pady=5)
    
    paramAff = LabelFrame(param, text="Affichage")
    paramAff.pack(side=LEFT, padx=5)
    imgClassic = PhotoImage(file="res/classic.gif")
    imgPhysique = PhotoImage(file="res/physique.gif")
    boutonAffClassic = Button(paramAff, command=lambda:setAffichage(CLASSIC), image=imgClassic)
    boutonAffClassic.pack(side=LEFT, padx=5, pady=5)
    boutonAffPhysique = Button(paramAff, command=lambda:setAffichage(PHYSIQUE), image=imgPhysique)
    boutonAffPhysique.pack(side=LEFT, padx=5, pady=5)

    #création du canvas
    canvas = Canvas(fenetre, background="white")
    canvas.pack(side=TOP, fill=BOTH, expand=1)
    canvas.update()
    
    #création de la barre de status
    status = StringVar()
    statusbar = Label(fenetre, textvariable=status, anchor=W)
    status.set("Aucun fichier chargé")
    statusbar.pack(side=BOTTOM, fill=X)

    fenetre.mainloop()
