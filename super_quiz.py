
# -*- coding: utf-8 -*-
"""
Created on Sun May 26 13:50:11 2019
@author: MASTOWOLF
"""

from tkinter import *

class SuperQuizz:
    def __init__(self, root: Tk):
        self.compteur = 0
        self.root = root
        self.current_window = None  # Reference to the current question window
        self.root.title('SUPER QUIZZ')
        self.root.resizable(width=False, height=False)
        self.init_main_window()

    def init_main_window(self):
        can = Canvas(self.root, width=300, height=150)
        label = Label(self.root, text="Prêt pour un quizz de folie ???\n\n Cliquer pour commencer\n\n ATTENTION CLIQUER AUTOUR DE LA REPONSE")
        label.pack()
        can.pack()
        
        can.bind("<Button-1>", self.start_quizz, add="+")

        b1 = Button(self.root, height=2, width=12, text="Quitter", command=self.root.destroy)
        b1.pack(side=BOTTOM, padx=5, pady=5)

        b2 = Button(self.root, height=35, width=35, bitmap='info', command=self.information)
        b2.pack(side=BOTTOM, padx=5, pady=5, anchor=CENTER)

    def information(self):
        Mafenetre = Tk()
        Mafenetre.title('A quoi ça sert ?')
        Mafenetre.geometry('500x200')
        Label1 = Label(Mafenetre,
                       text="Bonjour tout le monde !\n\n Ce programme a pour but de faire un quizz!!!",
                       font="Times 12",
                       fg="black")
        Label1.pack()
        Mafenetre.mainloop()

    def start_quizz(self, event):
        self.root.destroy()
        self.next_question1()

    def next_question1(self):
        self.create_question_window('QUELLE EST LA COULEUR DU CHEVAL BLANC ?',
                                    'yellow',
                                    ['Blanc', 'Vert', '8', 'noir'],
                                    [(125, 125), (375, 125), (125, 375), (375, 375)],
                                    self.check_answer1)

    def check_answer1(self, event):
        if (0 < event.x < 250) and (0 < event.y < 250):
            self.compteur += 5
        self.next_question2()

    def next_question2(self):
        self.destroy_current_window()
        self.create_question_window('Calcule 10+20 = ?',
                                    'red',
                                    ['1000', '1548', '56', '30'],
                                    [(125, 125), (375, 125), (125, 375), (375, 375)],
                                    self.check_answer2)

    def check_answer2(self, event):
        if (250 < event.x < 500) and (250 < event.y < 500):
            self.compteur += 5
        self.next_question3()

    def next_question3(self):
        self.destroy_current_window()
        self.create_question_window('La capitale de la France ?',
                                    'blue',
                                    ['TOKYO', 'PARIS', 'LONDRES', 'CHICAGO'],
                                    [(125, 125), (375, 125), (125, 375), (375, 375)],
                                    self.check_answer3)

    def check_answer3(self, event):
        if (250 < event.x < 500) and (0 < event.y < 250):
            self.compteur += 5
        self.next_question4()

    def next_question4(self):
        self.destroy_current_window()
        self.create_question_window('Forme de la fonction affine',
                                    'green',
                                    ['ax^2+bx+x', '1/x', 'ax+b', 'ax'],
                                    [(125, 125), (375, 125), (125, 375), (375, 375)],
                                    self.final_score)

    def final_score(self, event):
        if (0 < event.x < 500) and (250 < event.y < 500):
            self.compteur += 5
        self.show_final_score()

    def show_final_score(self):
        self.destroy_current_window()
        Fe = Tk()
        Fe.title('SCORE TOTAL')
        can = Canvas(Fe, width=200, height=200, bg='white')
        can.pack()
        label = Label(Fe, text=f"Votre score est {self.compteur} sur 20")
        label.pack()

    def create_question_window(self, title, bg_color, answers, positions, callback):
        self.current_window = Tk()
        self.current_window.title(title)
        can = Canvas(self.current_window, width=500, height=500, bg=bg_color)
        can.pack()
        for answer, pos in zip(answers, positions):
            Label(self.current_window, text=answer).place(x=pos[0], y=pos[1], anchor='center')
        can.create_line(0, 250, 500, 250)
        can.create_line(250, 0, 250, 500)
        can.bind("<Button-1>", callback, add="+")

    def destroy_current_window(self):
        if self.current_window:
            self.current_window.destroy()
            self.current_window = None

def main():
    root = Tk()
    app = SuperQuizz(root)
    root.mainloop()

if __name__ == "__main__":
    main()
