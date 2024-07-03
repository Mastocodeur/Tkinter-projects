# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 16:37:36 2019

@author: Rem's
"""

# TP 

############## Importation des bibliothèques #####################

from tkinter import *

####################### QUESTION 1 ###############################

Fenetre = Tk()
Fenetre.title('My Pratical Lab')
Fenetre.resizable(width=False,height=False) # Pour garder la taille désirée 
can = Canvas(Fenetre,width=600,height=300,bg="grey")

ligne1 = can.create_line(300, 0, 300, 300)
rond1 = can.create_oval(100,100,200,200,fill="white")
rond2 = can.create_oval(400,100,500,200,fill="black")

######################  QUESTION 2 ###############################

def ChangerDeCouleur(event):
    if ((400 <event.x < 500 ) and (100 <event.y < 200)):
        can.configure(background="#00FD2A") #Couleur HTML pour la consigne
    else :
        can.configure(background="grey")       

def Changer_couleur(event):
    if ((100 <event.x < 200 ) and (100 <event.y < 200)):
        can.configure(background="#FD0000") #Couleur HTML pour la consigne

can.bind("<Button-1>",ChangerDeCouleur,add="+")
can.bind("<Button-1>", Changer_couleur,add="+")

######################  QUESTION 3 ###############################

cpt=0
def Efface(event):
    global cpt
    if(not((100 <event.x < 200 ) and (100 <event.y < 200))
            and not((400 <event.x < 500 ) and (100 <event.y < 200))):
        cpt+=1
        if (cpt==3): 
           Fenetre.destroy()
            
can.bind("<Button-1>",Efface,add="+")   
 
######################  QUESTION 4 = DM ###############################
       
def Rond1(event):
    if ((100 <event.x < 200 ) and (100 <event.y < 200)):
        can.itemconfigure(rond1, fill='black')
        can.itemconfigure(rond2, fill='white')
        can.update()
        
def Rond2(event):
    if ((400 <event.x < 500 ) and (100 <event.y < 200)):
        can.itemconfigure(rond1, fill='white')
        can.itemconfigure(rond2, fill='black')
        can.update()            

can.bind("<Button-3>",Rond1,add="+")
can.bind("<Button-3>",Rond2,add="+") 

############ COMMANDES LIES A LA SURVIE DE LA FENETRE #################     

can.pack()
Fenetre.mainloop()
