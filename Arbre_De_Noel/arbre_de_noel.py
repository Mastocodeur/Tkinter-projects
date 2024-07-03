# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 22:03:06 2019

@author: MASTOWOLF
"""
import tkinter as tk

def arbre_de_noel(zone_dessin: tk.Canvas) -> None:
    """Draws a Christmas tree on the given canvas
    Parameters
    ----------
    zone_dessin : tk.Canvas
    """

    # Le  tronc
    zone_dessin.create_rectangle(220,500,280,400,fill="brown")

    # Premier étage
    zone_dessin.create_polygon(50,400,250,300,450,400,fill="green")

    #Deuxième étage
    zone_dessin.create_polygon(100,320,250,200,400,320,fill="green")

    # Troisième étage
    zone_dessin.create_polygon(150,220,250,100,350,220,fill="green")

    # Décoration
    zone_dessin.create_oval(40,420,60,400,fill="blue")
    zone_dessin.create_oval(440,420,460,400,fill="blue")
    zone_dessin.create_oval(90,340,110,320,fill="red")
    zone_dessin.create_oval(390,340,410,320,fill="red")
    zone_dessin.create_oval(140,240,160,220,fill="yellow")
    zone_dessin.create_oval(340,240,360,220,fill="yellow")
    
def main():
    Fenetre = tk.Tk()
    Fenetre.title('My Christmas Tree')
    zone_dessin = tk.Canvas(Fenetre,width=500,height=500,bg="orange",bd=10)
    zone_dessin.pack()
    b1 = tk.Button(Fenetre, height=2, width=12,  text ='Christmas Tree', command=lambda : arbre_de_noel(zone_dessin), activebackground='white')
    b1.pack(side=tk.LEFT, padx =250, pady =10)
    Fenetre.mainloop()

if __name__ == "__main__":
    main()