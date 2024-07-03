# -*- coding: utf-8 -*-
"""
Created on Sat May 30 23:02:22 2020

@author: MASTOWOLF
"""

from random import *
import numpy as np
import unicodedata
from time import *
from tkinter import * 

start_time=time()
#clean les codes svp tout en francais, mot à la place de line... M devient P

#########IMPORT DES BANQUES#################

#banque4 : 74K mots

def supprimerRep(fichier):
    tabl=[]
    tabl.append(fichier[0])
    for i in range(1,len(fichier)):
        if fichier[i-1]!=fichier[i]:
            tabl.append(fichier[i])
    return tabl

def filtrage1(fichier):
    tabl=[]
    for ligne in fichier:
        mot=u''
        lettre=ligne[0]
        ind=0
        while lettre!=' ':
            mot+=lettre
            ind+=1
            lettre=ligne[ind]
        tabl.append(mot)
    return tabl

#banque6 : 300K mots

def supaccent(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def remove(banques):
    nouvellesBanques=[]
    for fichier in banques:
        nouvelleBanque=[]
        for mot in fichier:
            mot2=u''
            for lettre in mot:
                if lettre in dictionnaireFrancais:
                    mot2+=lettre
            nouvelleBanque.append(mot2)
        nouvellesBanques.append(nouvelleBanque)
    return nouvellesBanques


def filtrage2(banques,alphabet):
    nouvellesBanques=[]
    for fichier in banques:
        nouvelleBanque=[]
        for mot in fichier:
            mot2=u''
            for lettre in mot:
                if lettre in alphabet:
                    mot2+=lettre
            if len(mot2)>0: #certaines lignes peuvent ne contenir qu'un caractère, et il peut ne pas être dans l'alphabet. 
                nouvelleBanque.append(mot2) #après filtrage, la ligne serait de longueur nulle. On ne la prend pas.
        nouvellesBanques.append(nouvelleBanque)
    return nouvellesBanques

#Banque7: 400K mots, sans accents
file7=[]
with open(r"dico3.txt", "rt", encoding='utf_8') as ligne:
    for lettre in ligne:
        lettre=lettre.lower() #les mots de cette banque sont tous en majuscule
        file7.append(lettre)
 

#Banque8: 200K mots anglais
file8=open(r"english.txt", "rt", encoding='utf_8')
file8=file8.readlines()

#Banque9: 60K mots italiens
file9=open(r"italian.txt", "rt", encoding='utf_8')
file9=file9.readlines()

#Banque16: 50K mots finnois
file16=open(r"finnish.txt", "rt", encoding='utf_8')
file16=file16.readlines()
file16=filtrage1(file16) 

#Banque17: 50K mots norvégiens
file17=open(r"norwegian.txt", "rt", encoding='utf_8')
file17=file17.readlines()
file17=filtrage1(file17) 

#Banque18: 50K mots polonais
file18=open(r"polish.txt", "rt", encoding='utf_8')
file18=file18.readlines()
file18=filtrage1(file18) 

#Banque19: 50K mots portugais
file19=open(r"portuguese.txt", "rt", encoding='utf_8')
file19=file19.readlines()
file19=filtrage1(file19)

#Banque20: 50K mots serbes
file20=open(r"serbian.txt", "rt", encoding='utf_8')
file20=file20.readlines()
file20=filtrage1(file20)

#Banque21: 50K mots suédois
file21=open(r"swedish.txt", "rt", encoding='utf_8')
file21=file21.readlines()
file21=filtrage1(file21)


################# ALPHABET LATIN #################

def alphabetLatin():
    dictionnaire={}
    for i in range(97,123): #lettres de a à z
        dictionnaire[chr(i)]=i-97
    for i in range(224,254):
        dictionnaire[chr(i)]=i-198 #toutes les lettres accentuées
    del(dictionnaire['÷']) #il y a ce caractère sépcial au milieu des lettres accentuées
    return dictionnaire

alphabetLatin=alphabetLatin()
#alphabetLatin[a] renvoie 0

def alphabetInverse(dictionnaire):
    inverse = {}
    for cle in dictionnaire:
        valeur = dictionnaire[cle]
        inverse[valeur]=cle
    return inverse

alphabetLatinInverse=alphabetInverse(alphabetLatin)
#alphabetLatinInverse[0] renvoie a

alphabet=alphabetLatin

##############DICTIONNAIRE FRANCAIS########################

def dictionnaireFrancais():
    dictionnaire={}
    for i in range(97,123):
        dictionnaire[chr(i)]=i-97
    for i in range(224,254):
        dictionnaire[chr(i)]=i-198
    del(dictionnaire['÷'])
    return dictionnaire

dictionnaireFrancais=dictionnaireFrancais()

def dictionnaireInverse(dictionnaire):
    inverse = {}
    for cle in dictionnaire:
        valeur = dictionnaire[cle]
        inverse[valeur]=cle
    return inverse
def conversionAlphabet(alphabet):
    tab=[]
    for lettre in alphabet:
        tab.append(lettre)
    return tab

alphabetConverti=conversionAlphabet(alphabet)
dictionnaireFrancaisInverse=dictionnaireInverse(dictionnaireFrancais)

###ENLEVER \n A LA FIN DE CHAQUE MOT DE CHAQUE LISTE DE MOTS########

banques=[file7,file8,file9,file16,file17,file18,file19,file20,file21]

file7=filtrage2(banques,alphabetLatin)[0]
file8=filtrage2(banques,alphabetLatin)[1] #anglais
file9=filtrage2(banques,alphabetLatin)[2] #italien
file16=filtrage2(banques,alphabetLatin)[3] #finnois
file17=filtrage2(banques,alphabetLatin)[4] #norvégien
file18=filtrage2(banques,alphabetLatin)[5] #polonais
file19=filtrage2(banques,alphabetLatin)[6] #portuguais
file20=filtrage2(banques,alphabetLatin)[7] #serbe
file21=filtrage2(banques,alphabetLatin)[8] #suédois



##########FONCTIONS CREANT LES MATRICES DE COMPTAGE#######################
def matriceProbaPosition1(file,placeLettre,alphabet):
    if placeLettre==0 : #cas particulier: tableau (matrice1D) de probas pour les lettres en 1ère place
        comptage1=np.zeros(55)
        comptageTot1=0
        for ligne in file: 
            l=ligne[0]  #on parcourt la première de chaque mot
            i=alphabet[l]
            comptage1[i]+=1 #on compte les différentes lettres 
            comptageTot1+=1 #on compte le nombre de lettres totales
        P=[comptage1[i]/comptageTot1 for i in range(0,55)] #normalisation
    else : 
        P=np.zeros((55,55))
        comptageTot=np.zeros(55)
        for ligne in file:
            if placeLettre<len(ligne)-1: 
                i=ligne[placeLettre-1] #lettre d'avant
                j=ligne[placeLettre] #lettre étudiée
                i=alphabet[i] #numéro associé à la lettre d'avant
                j=alphabet[j] #numéro associé à la lettre étudiée
                P[i][j]+=1 #on compte les lettres
                comptageTot[i]+=1 #on compte les lettres totales
        for i in range(len(comptageTot)):
            if comptageTot[i]!=0:
                P[i]=P[i]/comptageTot[i] #on convertit en probabilités
    return P


def matricesStockés(nombreDeLettres,file,alphabet): #cette fonction sert à ne pas recalculer les matrices pour chaque 
    Mstocks=[matriceProbaPosition1(file,i,alphabet) for i in range(nombreDeLettres-1)] #génération de mots
    Mstocks.append(PFin) #il faut prendre 
    return Mstocks #la matrice de la DERNIERE lettre et non celle qui correspond à la lettre à la place nombreDeLettres


#On essaye maintenant de combiner nos 2 méthodes les plus efficaces, on utilise le processus de chaine de markov
#avec des matrices prenant en compte les 2 lettres d'avant

def matriceProbaPosition2(file,placeLettre,mot,alphabet) :
    if placeLettre==0 or placeLettre==1 :
        M=matriceProbaPosition1(file, placeLettre,alphabet) #pour les deux premières lettres le code ne change pas, on peut
                                                               #on peut utiliser la fonction de matrice précédente
    else :
        M=np.zeros(55)
        comptageTot=0
        for ligne in file :
            if 0<placeLettre<len(ligne)-1 or placeLettre==-1 and 3<=len(ligne) :#je vérifie que je reste bien dans mon mot
                                    # la condition -1 sert lors de la matrice de la dernière lettre
                i=ligne[placeLettre-1] #lettre d'avant
                if i==mot[-1] : # je regarde si la lettre d'avant est égale à la dernière lettre actuelle de mon mot
                    j=ligne[placeLettre-2]
                    if j==mot[-2] : # de meme pour la lettre d'encore avant
                        lettre=ligne[placeLettre] 
                        k=alphabet[lettre] #numéro associé à la lettre analysée
                        M[k]+=1
                        comptageTot+=1
        if comptageTot !=0 :
            M=[M[i]/comptageTot for i in range(55)] #normalisation
    return M 

def genererMotMarkov2(fichier,nombreDeLettres,alphabet):
    lettre=np.random.choice(alphabetConverti,1,p=matriceProbaPosition2(fichier,0,[],alphabet))[0] 
    mot= lettre #1ère lettre
    ind=alphabet[lettre] #la 2ème lettre se génère comme dans genererMarkov1
    lettre=np.random.choice(alphabetConverti,1,p=matriceProbaPosition2(fichier,1,mot,alphabet)[ind])[0]
    mot+=lettre
    for i in range(2,nombreDeLettres-1 ) :
        M=matriceProbaPosition2(fichier,i,mot,alphabet) #On recalcule des matrices différentes ( en fait des listes) à chaque fois
        mot+=np.random.choice(alphabetConverti,1,p=M)[0]
    M=matriceProbaPosition2(fichier,-1,mot,alphabet) # on traite la dernière lettre à part
    mot+=np.random.choice(alphabetConverti,1,p=M)[0]
    return mot



def FR():
    file= file7
    try:
        saisi=int(e.get())
        saisi2=int(e2.get())
        output.delete('1.0',END)
        if (saisi<=15):
            for i in range(saisi2):
                defe=genererMotMarkov2(file,saisi,alphabet)
                saut='\n'
                output.insert(END,defe)
                output.insert(END,saut)
            msg = "Création Terminée Française"
            output.insert(END,saut)
            output.insert(END,msg)
        else:
            output.delete('1.0',END)
            defe = "Mots trop long désolé, veuillez respectez la limite de 17 lettres "
            output.insert(END,defe)
            
    except :
        output.delete('1.0',END)
        defe = "Vous n'avez pas entré de chiffre ! MACHINE ERROR 404"
        output.insert(END,defe)


def EN():
    file= file8
    ################### GENERATION DE MOTS #####################
    try:
        saisi=int(e.get())
        saisi2=int(e2.get())
        output.delete('1.0',END)
        if (saisi<=15):
            for i in range(saisi2):
                defe=genererMotMarkov2(file,saisi,alphabet)
                saut='\n'
                output.insert(END,defe)
                output.insert(END,saut)
            msg = "Création Terminée Anglaise"
            output.insert(END,saut)
            output.insert(END,msg)
        else:
            output.delete('1.0',END)
            defe = "Mots trop long désolé, veuillez respectez la limite de 17 lettres "
            output.insert(END,defe)
            
    except :
        output.delete('1.0',END)
        defe = "Vous n'avez pas entré de chiffre ! MACHINE ERROR 404"
        output.insert(END,defe)



def IT():
    file= file9
    try:
        saisi=int(e.get())
        saisi2=int(e2.get())
        output.delete('1.0',END)
        if (saisi<=15):
            for i in range(saisi2):
                defe=genererMotMarkov2(file,saisi,alphabet)
                saut='\n'
                output.insert(END,defe)
                output.insert(END,saut)
            msg = "Création Terminée Italienne"
            output.insert(END,saut)
            output.insert(END,msg)
        else:
            output.delete('1.0',END)
            defe = "Mots trop long désolé, veuillez respectez la limite de 17 lettres "
            output.insert(END,defe)
            
    except :
        output.delete('1.0',END)
        defe = "Vous n'avez pas entré de chiffre ! MACHINE ERROR 404"
        output.insert(END,defe)

def POR():
    file= file19
    ################### GENERATION DE MOTS #####################
    try:
        saisi=int(e.get())
        saisi2=int(e2.get())
        output.delete('1.0',END)
        if (saisi<=15):
            for i in range(saisi2):
                defe=genererMotMarkov2(file,saisi,alphabet)
                saut='\n'
                output.insert(END,defe)
                output.insert(END,saut)
            msg = "Création Terminée Portugaise "
            output.insert(END,saut)
            output.insert(END,msg)
        else:
            output.delete('1.0',END)
            defe = "Mots trop long désolé, veuillez respectez la limite de 17 lettres "
            output.insert(END,defe)
            
    except :
        output.delete('1.0',END)
        defe = "Vous n'avez pas entré de chiffre ! MACHINE ERROR 404"
        output.insert(END,defe)

def SER():
    file= file20
    try:
        saisi=int(e.get())
        saisi2=int(e2.get())
        output.delete('1.0',END)
        if (saisi<=15):
            for i in range(saisi2):
                defe=genererMotMarkov2(file,saisi,alphabet)
                saut='\n'
                output.insert(END,defe)
                output.insert(END,saut)
            msg = "Création Terminée Serbe"
            output.insert(END,saut)
            output.insert(END,msg)
        else:
            output.delete('1.0',END)
            defe = "Mots trop long désolé, veuillez respectez la limite de 17 lettres "
            output.insert(END,defe)
            
    except :
        output.delete('1.0',END)
        defe = "Vous n'avez pas entré de chiffre ! MACHINE ERROR 404"
        output.insert(END,defe)


def SUE():
    file= file21
    ################### GENERATION DE MOTS #####################
    try:
        saisi=int(e.get())
        saisi2=int(e2.get())
        output.delete('1.0',END)
        if (saisi<=15):
            for i in range(saisi2):
                defe=genererMotMarkov2(file,saisi,alphabet)
                saut='\n'
                output.insert(END,defe)
                output.insert(END,saut)
            msg = "Création Terminée Suédoise"
            output.insert(END,saut)
            output.insert(END,msg)
        else:
            output.delete('1.0',END)
            defe = "Mots trop long désolé, veuillez respectez la limite de 17 lettres "
            output.insert(END,defe)
            
    except :
        output.delete('1.0',END)
        defe = "Vous n'avez pas entré de chiffre ! MACHINE ERROR 404"
        output.insert(END,defe)

def FIN():
    file= file21
    ################### GENERATION DE MOTS #####################
    try:
        saisi=int(e.get())
        saisi2=int(e2.get())
        output.delete('1.0',END)
        if (saisi<=15):
            for i in range(saisi2):
                defe=genererMotMarkov2(file,saisi,alphabet)
                saut='\n'
                output.insert(END,defe)
                output.insert(END,saut)
            msg = "Création Terminée Finoise"
            output.insert(END,saut)
            output.insert(END,msg)
        else:
            output.delete('1.0',END)
            defe = "Mots trop long désolé, veuillez respectez la limite de 17 lettres "
            output.insert(END,defe)
            
    except :
        output.delete('1.0',END)
        defe = "Vous n'avez pas entré de chiffre ! MACHINE ERROR 404"
        output.insert(END,defe)

def NOR():
    file= file21
    ################### GENERATION DE MOTS #####################
    try:
        saisi=int(e.get())
        saisi2=int(e2.get())
        output.delete('1.0',END)
        if (saisi<=15):
            for i in range(saisi2):
                defe=genererMotMarkov2(file,saisi,alphabet)
                saut='\n'
                output.insert(END,defe)
                output.insert(END,saut)
            msg = "Création Terminée Norvégienne"
            output.insert(END,saut)
            output.insert(END,msg)
        else:
            output.delete('1.0',END)
            defe = "Mots trop long désolé, veuillez respectez la limite de 17 lettres "
            output.insert(END,defe)
            
    except :
        output.delete('1.0',END)
        defe = "Vous n'avez pas entré de chiffre ! MACHINE ERROR 404"
        output.insert(END,defe)

        
def information(): # FONCTION DU BOUTON INFO
    Mafenetre = Tk()
    Mafenetre.iconbitmap('point.ico')
    Mafenetre.title('Mais à quoi ça sert ?')
    Mafenetre.geometry('600x200')
    Label1 = Label(Mafenetre,
                   text = "Bonjour tout le monde !\n\n Ce programme a pour but de créer des mots cohérents avec la langue choisie!!!\n Il faut cliquer avec la souris sur les boutons de la fenêtre pour valider vos choix !\n Attention à bien rentrer des chiffres et pas des mots !\n Si vous affichez beaucoup de mots, il faudra scroller vers le bas!\n La limite du nombre de lettre est fixée à 15 et est justifiée dans le notebook. \n\n Bonne Création !",
                   font="Times 12",
                   fg = "black" )
    Label1.pack()
    Mafenetre.mainloop()  
    
print("Temps d execution avant ouverture fenêtre: %s secondes ---" % (time() - start_time))
############# CREATION DE LA PREMIERE FENETRE ET DES PARAMETRES ###############
Fenetre = Tk() # Création de la Fenetre principale == structure
Fenetre.title("MACHINE A INVENTER DES MOTS")
Fenetre.configure(background='black') #Configuration de la Fenetre 
Fenetre.resizable(width=False,height=False) # Pour garder la taille désirée
Label(Fenetre, text="Nombre de lettres", bg="black",fg='white',font='none 12 bold').grid(row=0,column=0,sticky='')#Texte pour formuler des demandes claires à l'utilisateur
Label(Fenetre, text="Nombre de mots", bg="black",fg='white',font='none 12 bold').grid(row=0,column=1,sticky='')
e = Entry(Fenetre, width=5,borderwidth=5,bg='white') # Pour que l'utilisateur puisse entrer le nombre de lettres 
e.grid(row=1,column=0,sticky='')
e2 = Entry(Fenetre, width=5,borderwidth=5,bg='white')# Pour que l'utilisateur puisse entrer le nombre de mots 
e2.grid(row=1,column=1,sticky='')

Label(Fenetre, text="Choix de la langue", bg="black",fg='white',font='none 12 bold').grid(row=2,column=0,sticky='')

Button(Fenetre, text="FRANCAIS", width=10, command=FR).grid(row=3,column=0,sticky=W) # Construction des boutons
Button(Fenetre, text="PORTUGUAIS", width=10, command=POR).grid(row=4,column=0,sticky=W)
Button(Fenetre, text="FINLANDE", width=10, command=FIN).grid(row=5,column=0,sticky=W)

Button(Fenetre, text="ANGLAIS", width=10, command=EN).grid(row=3,column=1,sticky=W)
Button(Fenetre, text="SERBE", width=10, command=SER).grid(row=4,column=1,sticky=W)
Button(Fenetre, text="NORVEGIEN", width=10, command=NOR).grid(row=5,column=1,sticky=W)

Button(Fenetre, text="ITALIEN", width=10, command=IT).grid(row=6,column=0,sticky=W)
Button(Fenetre, text="SUEDOIS", width=10, command=SUE).grid(row=6,column=1,sticky=W)

Label(Fenetre, text="AFFICHAGE DES MOTS : ", bg='black', fg='white', font='none 12 bold').grid(row=7, column=0, sticky='')
output = Text(Fenetre, width=50 , height=10, wrap= WORD, background='white') # Création de la zone d'affichage
output.grid(row=8,column=0,columnspan=2, sticky='') # Caractérstiques liées à sa construction par la méthode grid
photo = PhotoImage(file="machine.png")
Label(Fenetre, image = photo, bg='black').grid(row=8,column=3,sticky='')#Commande pour placer l'image sur la fenêtre
Label (Fenetre, text ="Cliquer pour Sortir : ", bg='black', fg='white', font='none 12 bold' ).grid(row=9,column=0, sticky = W)
Button(Fenetre,width=10, text='Au Revoir', command=Fenetre.destroy).grid(row=9,column=1,sticky=W)
Button(Fenetre, height=35, width=35, bitmap='info', command=information).grid(row=9,column=4,sticky=E)


Fenetre.mainloop()

print("Temps d execution total : %s secondes ---" % (time() - start_time))