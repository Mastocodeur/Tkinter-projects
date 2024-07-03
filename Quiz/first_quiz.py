# -*- coding: utf-8 -*-
"""
Created on Sun May 26 13:50:11 2019
@author: MASTOWOLF
"""
################ Bibliothèque utilisée pour le programme ######################

from tkinter import * 

############# CREATION DE LA PREMIERE FENETRE ET DES PARAMETRES ###############
############# avec boutons(voir lignes 140-144)

compteur=0 
Fenetre = Tk()
Fenetre.title('SUPER QUIZZ')
Fenetre.resizable(width=False,height=False) # Pour garder la taille désirée 
can = Canvas(Fenetre,width=300,height=150)

label=Label(Fenetre)
def ta_fonction():
    label['text']="Prêt pour un quizz de folie ???\n\n Cliquer pour commencer\n\n ATTENTION CLIQUER AUTOUR DE LA REPONSE"
ta_fonction()
label.pack()
can.pack()

######################### FONCTIONS UTILISEES DANS LE PROGRAMME ###############

def information(): # FONCTION DU BOUTON INFO
    Mafenetre = Tk()
    Mafenetre.title('A quoi ça sert ?')
    Mafenetre.geometry('500x200')
    Label1 = Label(Mafenetre,
                   text = "Bonjour tout le monde !\n\n Ce programme a pour but de faire un quizz!!!",
                   font="Times 12",
                   fg = "black" )
    Label1.pack()
    Mafenetre.mainloop()

def QUIZZ(event): # FONCTION PRINCIPALE DU QUIZZ + WIDGETS
    if (event):
        Fenetre.destroy() #DESTRUCTION DE LA FENETRE PRINCIPALE APRES AVOIR CLIQUER
        Fenetr = Tk()
        Fenetr.title('QUELLE EST LA COULEUR DU CHEVAL BLANC ?')
        can = Canvas(Fenetr,width=500,height=500,bg='yellow')
        Reponse1 = Label(Fenetr, text='Blanc')
        Reponse2 = Label(Fenetr, text='Vert')
        Reponse3 = Label(Fenetr, text='8')
        Reponse4 = Label(Fenetr, text='noir')
        Reponse1.place(x=125, y=125, anchor='center')
        Reponse2.place(x=375, y=125, anchor='center')
        Reponse3.place(x=125, y=375, anchor='center')
        Reponse4.place(x=375, y=375, anchor='center')
        ligne1 = can.create_line(0, 250, 500, 250)
        ligne = can.create_line(250,0,250,500)
        can.pack()
        def SUITE(event): #ANALYSE LA REPONSE ET DEROULE LA SUITE DU QUIZZ
            if ((0 <event.x < 250) and (0 < event.y < 250)): #ZONE DE LA BONNE REPONSE
                global compteur
                compteur+=5
            if (event): # POUR PASSER A LA QUESTION SUIVANTE
                Fenetr.destroy()
                Fenet =Tk()
                Fenet.title('Calcule 10+20  = ? ')
                can = Canvas(Fenet,width=500,height=500,bg='red')
                Reponse1 = Label(Fenet, text='1000')
                Reponse2 = Label(Fenet, text='1548')
                Reponse3 = Label(Fenet, text='56')
                Reponse4 = Label(Fenet, text='30')
                Reponse1.place(x=125, y=125, anchor='center')
                Reponse2.place(x=375, y=125, anchor='center')
                Reponse3.place(x=125, y=375, anchor='center')
                Reponse4.place(x=375, y=375, anchor='center')
                ligne2 = can.create_line(0, 250, 500, 250)
                ligne3 = can.create_line(250,0,250,500)
                can.pack()
                print(compteur)
                def SUITE2(event):
                    if ((250 <event.x < 500 ) and (250 <event.y < 500)):
                        global compteur
                        compteur+=5
                    if (event):
                        Fenet.destroy()
                        Fene = Tk()
                        Fene.title('La capitale de la France ?')
                        can = Canvas(Fene,width=500,height=500,bg='blue')
                        Reponse1 = Label(Fene, text='TOKYO')
                        Reponse2 = Label(Fene, text='PARIS')
                        Reponse3 = Label(Fene, text='LONDRES')
                        Reponse4 = Label(Fene, text='CHICAGO')
                        Reponse1.place(x=125, y=125, anchor='center')
                        Reponse2.place(x=375, y=125, anchor='center')
                        Reponse3.place(x=125, y=375, anchor='center')
                        Reponse4.place(x=375, y=375, anchor='center')
                        ligne2 = can.create_line(0, 250, 500, 250)
                        ligne3 = can.create_line(250,0,250,500)
                        can.pack()
                        print(compteur)
                        def SUITE3(event):
                            if ((250 <event.x < 500 ) and (0 <event.y < 250)):
                                global compteur
                                compteur+=5
                            if(event):
                                Fene.destroy()
                                Fen =Tk()
                                Fen.title('Forme de la fonction affine')
                                can = Canvas(Fen,width=500,height=500,bg='green')
                                Reponse1 = Label(Fen, text='ax^2+bx+x')
                                Reponse2 = Label(Fen, text='1/x')
                                Reponse3 = Label(Fen, text='ax+b')
                                Reponse4 = Label(Fen, text='ax')
                                Reponse1.place(x=125, y=125, anchor='center')
                                Reponse2.place(x=375, y=125, anchor='center')
                                Reponse3.place(x=125, y=375, anchor='center')
                                Reponse4.place(x=375, y=375, anchor='center')
                                ligne2 = can.create_line(0, 250, 500, 250)
                                ligne3 = can.create_line(250,0,250,500)
                                can.pack()
                                print(compteur)
                                def CONCLU(event): # FENETRE FINALE AVEC SCORE FINAL
                                    if ((0 <event.x < 500 ) and (250 <event.y<500)):
                                        global compteur
                                        compteur+=5
                                    if(event):
                                        Fen.destroy()
                                        Fe =Tk()
                                        Fe.title('SCORE TOTAL')
                                        can = Canvas(Fe,width=200,height=200,bg='white')
                                        can.pack()
                                        label=Label(Fe) #ECRITURE DANS LA FENETRE
                                        def ta_fonction2(): #ECRITURE DU MESSAGE
                                            label['text']=("Votre score est",compteur,"sur 20")
                                        ta_fonction2() # APPEL DE LA FONCTION POUR FAIRE APPARAITRE LE MESSAGE
                                        label.pack()
                                        print(compteur)
                                can.bind("<Button-1>",CONCLU,add="+")          
                        can.bind("<Button-1>",SUITE3,add="+") 
                can.bind("<Button-1>",SUITE2,add="+") 
        can.bind("<Button-1>",SUITE,add="+") #LIE LE CLIC DE LA SOURIS AUX FONCTIONS DEFINI CI DESSUS
can.bind("<Button-1>",QUIZZ,add="+")

# Button 1 == clic gauche de la souris 

b1=Button(Fenetre, height=2, width=12 ,text="Quitter",command=Fenetre.destroy)
b1.pack(side=BOTTOM, padx=5, pady=5)

b2=Button(Fenetre, height=35, width=35, bitmap='info', command=information)
b2.pack(side=BOTTOM, padx=5, pady=5,anchor=CENTER)

Fenetre.mainloop() # PERMET LA VISUALISATION DE LA FENETRE 