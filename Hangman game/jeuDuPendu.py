

from random import randint
import sqlite3
from tkinter import *
from tkinter import colorchooser
from formes import *
from PIL import Image, ImageTk



class ZoneAffichage(Canvas):

    def __init__(self, parent, largeur, hauteur):

        # Initialiser la classe parentale
        Canvas.__init__(self, parent, width=largeur, height=hauteur)

        # Liste des composantes
        self.__composants = []

        # Nb de mauvais essais
        self.__nbEssais = 0


        # Dessiner le bonhomme pendu

        # Base, Poteau, Traverse, Corde
        self.__composants.append(Rectangle(self, 50,  270, 200,  26, "brown"))
        self.__composants.append(Rectangle(self, 87,   83,  26, 200, "brown"))
        self.__composants.append(Rectangle(self, 87,   70, 150,  26, "brown"))
        self.__composants.append(Rectangle(self, 183,  67,  10,  40, "brown"))

        # Tete, Tronc
        self.__composants.append(Rectangle(self, 188, 120,  20,  20, "black"))
        self.__composants.append(Rectangle(self, 175, 143,  26,  60, "black"))

        # Bras gauche et droit
        self.__composants.append(Rectangle(self, 133, 150,  40,  10, "black"))
        self.__composants.append(Rectangle(self, 203, 150,  40,  10, "black"))

        # Jambes gauche et droite
        self.__composants.append(Rectangle(self, 175, 205,  10,  40, "black"))
        self.__composants.append(Rectangle(self, 191, 205,  10,  40, "black"))


    def incNbEssais(self):

        # Incrémenter le nombre de mauvais essais
        self.__nbEssais = min(10, self.__nbEssais + 1)

        # Rendre visible le composant
        self.__composants[self.__nbEssais - 1].setState('normal')


    def decrNbEssais(self):

        # Décrémenter le nombre de mauvais essais
        self.__nbEssais = max(0, self.__nbEssais - 1)

        # Rendre invisible le composant
        self.__composants[self.__nbEssais].setState('hidden')
        

    def getElementsPoutre(self):

        # Les 4 premiers élements
        return self.__composants[:4]

    
    def getElementsBonhomme(self):

        # Les 6 derniers élements
        return self.__composants[4:]


    def reinitialiser(self):

        # Remettre le compteur à 0
        self.__nbEssais = 0

        # Et cacher tous les composants
        for i in range(10):
            self.__composants[i].setState('hidden')



class ToucheClavier(Button):

    def __init__(self, parent, fenetre, lettre):

        # Initialiser la classe parentale
        Button.__init__(self, parent, text=lettre, highlightbackground='#ececec')

        # Enregistrer la lettre
        self.__lettre = lettre

        # Et la fenêtre parentale
        self.__fen = fenetre

        # De base, la touche est désactivée
        self.config(state=DISABLED, command=self.cliquer)


    def cliquer(self):

        # Désactiver la touche
        self.config(state=DISABLED)
        print("La touche '" + self.__lettre + "' a été cliquée.")

        # Faire appel à la methode de la fenêtre principale en passant la lettre
        self.__fen.traitementLettre(self.__lettre)



class FenPrincipale(Tk):

    def __init__(self, cheminBDD):

        # Initialiser la fenêtre
        Tk.__init__(self)

        self.title("Jeu du pendu") # le titre de la fenêtre
        self.config(bg='#2687bc') # imposer la couleur du fond

        self.geometry('650x650+400+400') # dimensions et placement initials
        self.minsize(width=650, height=550) # dimensions minimales



        #
        # Quelques variables
        #

        # La référence à la fenêtre enfant
        self.__enfant = None

        # Liste des mots du fichier
        self.__mots = self.chargerMots()


        #
        # --- Variables qui tiennent compte de la progression du jeu ---

        # Le mot à chercher
        self.__motCourant = ""

        # Le mot à chercher en *, décrypté partiellement
        self.__motDecrypte = ""

        # Le compteur de mauvais essais
        self.__nbEssais = 0

        # Trace (LIFO) des actions du joueur
        self.__traceActions = []

        #
        # --- Gestion de joueurs et parties ---

        # La connection à la bdd SQL
        self.__conn = sqlite3.connect(cheminBDD)

        # Compteurs pour les IDs
        (self.__idMaxJoueur, self.__idMaxPartie) = self.chargerIDsMax()

        # ID du joueur actuel
        self.__idJoueurCourant = None



        #
        # Initialiser l'arbre de scène
        #

        #
        # --- La barre d'outils en haut contenant trois touches ---
        self.__barreOutils = Frame(self, bg='#2687bc')
        self.__barreOutils.pack(side=TOP)

        self.__barreOutils.update() # Bug macOs

        # La touche: 'Nouvelle Partie'
        self.__btnNouvPartie = Button(self.__barreOutils , text="Nouvelle Partie", highlightbackground='#2687bc')
        self.__btnNouvPartie.pack(side=LEFT, padx=7, pady=5)

        # La touche 'Changer Joueur'
        self.__btnChangerJoueur = Button(self.__barreOutils, text="Gestion de Joueurs", highlightbackground='#2687bc')
        self.__btnChangerJoueur.pack(side=LEFT, pady=5)



        # La touche 'Changer de Couleur'
        self.__btnCouleur = Menubutton(self.__barreOutils, text = 'Couleurs', highlightbackground='#2687bc')
        self.__btnCouleur.pack(side=LEFT, padx=7, pady=5)
        
        # Le Menu dont on peut choisir
        self.__menuCouleur = Menu(self.__btnCouleur)
        self.__menuCouleur.add_command(label = 'Couleur de la Poutre', command = self.setCouleurPoutre)
        self.__menuCouleur.add_command(label = 'Couleur du Bonhomme', command = self.setCouleurBonhomme)
        self.__menuCouleur.add_command(label = "Couleur de Fond du Dessin", command = self.setCouleurFond)
        
        self.__btnCouleur.config(menu=self.__menuCouleur)



        # La touche Undo
        self.__btnUndo = Button(self.__barreOutils, text="Retour Arrière", highlightbackground='#2687bc')
        self.__btnUndo.pack(side=LEFT, pady=5)

        # Bouton info
        self.__boutonInfo = Button(self.__barreOutils, height=20, width=35,  bitmap='info')
        self.__boutonInfo.pack(side=LEFT, padx=5, pady=5) 

        # La touche 'Quitter'
        self.__btnQuitter = Button(self.__barreOutils , text="Quitter", highlightbackground='#2687bc')
        self.__btnQuitter.pack(side=RIGHT, padx=7, pady=5)


        #
        # --- Le message en dessous des touches ---
        self.__msgTexte = StringVar(self)

        self.__msgLabel = Label(self, textvariable=self.__msgTexte, bg='white', fg='black')
        self.__msgLabel.pack(side=TOP, pady=5)

        # On commence anonyme
        self.setNomJoueurCourant(None)


        #
        # --- Le progrès du jeu ---

        # La zone d'affichage
        self.__zoneAffichage = ZoneAffichage(self, 500, 300)
        self.__zoneAffichage.pack(side=TOP, pady=5)

        # Le mot à décrouvrir
        self.__motTexte = StringVar(self, "Mot : ")
        self.__motLabel = Label(self, textvariable=self.__motTexte, bg='white', fg='black')
        self.__motLabel.pack(side=TOP, pady=5)

        # L'affichage des tentatives restantes
        self.__tentaTexte = StringVar(self, "Nombre de tentatives restantes: -")
        self.__tentaLabel = Label(self, textvariable = self.__tentaTexte, fg = 'black')
        self.__tentaLabel.pack(side=TOP, padx=5, pady=2)

        #
        # --- Le clavier ---
        self.__clavier = Frame(self, bg='#ececec')
        self.__clavier.pack(side=BOTTOM, pady=5)

        self.__touches = []

        # Initialiser toutes les 26 touches
        for i in range(26):

            # Trouver le caractère à l'index i
            c = chr(ord('A') + i)

            # Créer une touche, puis la placer dans le grid
            touche = ToucheClavier(self.__clavier, self, c)
            touche.config(width=9)
            touche.grid(row=(i // 7), column=(i%7 if i//7<3 else i%7+1), padx=4, pady=5)

            self.__touches.append(touche)
    


        #
        # Associer des actions aux élements graphiques
        #

        self.__btnNouvPartie.config(command=self.nouvellePartie)
        self.__btnChangerJoueur.config(command=self.gestionJoueur)
        self.__boutonInfo.config(command=self.information)
        self.__btnUndo.config(command=self.undo)
        self.__btnQuitter.config(command=self.destroy)

    
    def __del__(self):

        # Enregistrer les changements
        self.__conn.commit()

        # Fermer la connexion
        self.__conn.close()


    def fermetureEnfant(self):
        
        # Marquer comme fermée
        self.__enfant = None


    def nouvellePartie(self):

        # Tirer un mot au hasard
        self.__motCourant = self.__mots[randint(0, len(self.__mots) - 1)]
        print("Le mot est '" + self.__motCourant + "'.")

        # Initialiser le mot decrypté
        self.__motDecrypte = '＊' * len(self.__motCourant)
        self.__motTexte.set("Mot : " + self.__motDecrypte)

        self.__motLabel.update() # Bug macOs nécessite un update() manuel

        # Reinitialiser l'affichage de tentatives
        self.__tentaTexte.set("Nombre de tentatives restantes: 10")

        self.__tentaLabel.update() # Bug macOs nécessite un update() manuel

        # Remettre à zéro le compteur d'essais
        self.__nbEssais = 0

        # Vider le LIFO
        self.__traceActions = []

        # Réinitialiser la zone d'affichage
        self.__zoneAffichage.reinitialiser()

        # Dégriser toutes les touches
        for i in range(26):
            self.__touches[i].config(state=NORMAL)
        

    def traitementLettre(self, lettre):

        # Tracer le clic sur la lettre
        self.__traceActions.append(lettre)

        #
        # Mettre à jour le mot décrypté
        succes = False

        # Parcourir le mot, lettre par lettre
        for (i, c) in enumerate(self.__motCourant):
            if c == lettre:

                # Changer l'astérisque pour la lettre
                self.__motDecrypte = self.__motDecrypte[:i] + lettre + self.__motDecrypte[i+1:]

                # Le mot contient la lettre rentrée
                succes = True

        
        # Vérifier comment/si le jeu continue et actualiser l'affichage
        #

        if succes == True:
            # Vérifier si le mot a été trouvé
            
            if self.__motCourant == self.__motDecrypte:

                # Afficher un message de victoire
                self.__motTexte.set("Félicitations ! Vous avez trouvé le bon mot '" + self.__motCourant + 
                                    "', en vous trompant " + str(self.__nbEssais) + " fois!")

                self.__motLabel.update() # Bug macOs nécessite un update() manuel
                

                # et désactiver les touches
                self.desactiverTouches()

                # Vider le LIFO 
                self.__traceActions = []

                # Enfin, enregistrer la partie
                self.enregistrerPartie()

                return

            # Le mot n'a pas été trouvé mais une lettre

            # Afficher le nouveau mot décrypté
            self.__motTexte.set("Mot : " + self.__motDecrypte)

            self.__motLabel.update() # Bug macOs nécessite un update() manuel

        else: # succes == False

            # Actualiser la zone d'affichage
            self.__zoneAffichage.incNbEssais()

            # Incrémenter le compteur de mauvais essais
            self.__nbEssais += 1

            # Mettre à jour l'affichage de tentatives restantes
            self.__tentaTexte.set("Nombre de tentatives restantes: " + str(10 - self.__nbEssais))
            
            self.__tentaLabel.update() # Bug macOs nécessite un update() manuel


            if self.__nbEssais >= 10:
                # Afficher un message de défaite
                self.__motTexte.set("Vous avez perdu ! Le bon mot était '" + self.__motCourant + "'")

                self.__motLabel.update() # Bug macOs nécessite un update() manuel

                # et désactiver les touches
                self.desactiverTouches()

                # Vider le LIFO 
                self.__traceActions = []

                # Enfin, enregistrer la partie
                self.enregistrerPartie()


    def undo(self):
        
        # Si la trace est vide, abandonner
        if (len(self.__traceActions) == 0):
            return

        # Trouver la lettre qui a été cliquée
        lettre = self.__traceActions.pop()


        # Mettre à jour le mot décrypté

        succes = False

        # Parcourir le mot, lettre par lettre
        for (i, c) in enumerate(self.__motCourant):
            if c == lettre:

                # Changer cette fois-ci la lettre pour l'astérisque
                self.__motDecrypte = self.__motDecrypte[:i] + "＊" + self.__motDecrypte[i+1:]

                # Le mot contient la lettre rentrée
                succes = True


        # Mettre à jour l'affichage du mot décrypté
        self.__motTexte.set("Mot : " + self.__motDecrypte)

        self.__motLabel.update() # Bug macOs nécessite un update() manuel
        
        # Dégriser la touche
        self.__touches[ord(lettre) - ord('A')].config(state=NORMAL)

        # Si c'était une bonne tentative, il ne reste plus rien à faire
        if succes == True:
            return

        #
        # Dans le cas contraire, mettre à jour l'affichage du pendu ainsi que l'affichage des tentatives restantes

        # Cacher l'élement du pendu
        self.__zoneAffichage.decrNbEssais()

        # Décrémenter le nombre de mauvais esssais
        self.__nbEssais -= 1

        # Mettre à jour l'affichage de tentatives restantes
        self.__tentaTexte.set("Nombre de tentatives restantes: " + str(10 - self.__nbEssais))
            
        self.__tentaLabel.update() # Bug macOs nécessite un update() manuel


    def information(self): # FONCTION DU BOUTON INFO
        Mafenetre = Tk()
        Mafenetre.title('A quoi ça sert ?')
        Mafenetre.geometry('500x200')
        Mafenetre.iconbitmap('Hangman game/info.ico')
        Label1 = Label(Mafenetre,
                   text = 
                   "Bonjour tout le monde !\n\n Ce programme est un jeu du pendu ! \n\n Amusez vous !",
                   font="Times 12",
                   fg = "black" )
        Label1.pack()
        Mafenetre.mainloop()


    def enregistrerPartie(self):

        # Verifiér qu'il y a un joueur courant
        if self.__idJoueurCourant == None:
            return

        # Préparer la demande sql
        sql = 'INSERT INTO Parties (idpartie,idjoueur,mot,score) VALUES (?,?,?,?)'

        # Objet qui permet la requête sql
        curseur = self.__conn.cursor()

        # Préparer les variables à stocker
        idPartie = self.__idMaxPartie
        idJoueur = self.__idJoueurCourant
        mot = self.__motCourant
        score = 1.0 - (self.__motDecrypte.count("＊") / len(mot))

        #
        # --- Executer la requête sql ---

        try:
            curseur.execute(sql, (idPartie, idJoueur, mot, score))

            # Si réussi, incrémenter le compteur d'ID max.
            self.__idMaxPartie += 1

        except Exception as err:
            print("Une exception a été relévé: '" + str(err) + "', type d'exception: '" + type(err).__name__)
        
        # Enregistrer les changements
        self.__conn.commit()
        

    def chargerIDsMax(self):

        # Préparer les demandes sql
        sql1 = "SELECT MAX(idjoueur) FROM Joueurs"
        sql2 = "SELECT MAX(idpartie) FROM Parties"

        # Objet qui permet la requête sql
        curseur = self.__conn.cursor()

        # Les IDs sont initialisé à 0
        idMaxJoueur = 0
        idMaxPartie = 0


        #
        # --- Executer la première requête sql ---

        try:
            curseur.execute(sql1)

            try:
                idMaxJoueur = int(curseur.fetchone()[0])
            except:
                idMaxJoueur = 0

        except Exception as err:

            # Erreur si la bdd est vide car MAX n'a pas d'arguments
            # Dans ce cas, rien ne faire, on garde les IDs initiales

            if "wrong number of arguments to function MAX()" != str(err):
                print("Une exception a été relévé: '" + str(err) + "', type d'exception: '" + type(err).__name__)
        

        #
        # --- Executer la seconde requête sql ---

        try:
            curseur.execute(sql2)

            try:
                idMaxPartie = int(curseur.fetchone()[0])
            except:
                idMaxPartie = 0
            

        except Exception as err:

            # Comme en haut
            #if "wrong number of arguments to function MAX()" != str(err):
            print("Une exception a été relévé: '" + str(err) + "', type d'exception: '" + type(err).__name__)

        
        return (idMaxJoueur, idMaxPartie)


    def creerStructureBDD(self):

        # Préparer les demandes sql
        sql1 = "CREATE TABLE Joueurs (idjoueur int, pseudo varchar(255));"
        sql2 = "CREATE TABLE Parties (idpartie int, idjoueur int, mot varchar(255), score float);"

        # Objet qui permet la requête sql
        curseur = self.__conn.cursor()


        #
        # --- Executer la première requête sql ---

        try:
            curseur.execute(sql1)

        except Exception as err:
            print("Une exception a été relévé: '" + str(err) + "', type d'exception: '" + type(err).__name__)
        

        #
        # --- Executer la seconde requête sql ---

        try:
            curseur.execute(sql2)

        except Exception as err:
            print("Une exception a été relévé: '" + str(err) + "', type d'exception: '" + type(err).__name__)

        
    def chargerMots(self):

        # Accéder au fichier contenant les mots
        fichier = open("Hangman game/mots.txt", 'r')

        # Créer une liste
        return fichier.read().split('\n')


    def desactiverTouches(self):

        # Désactiver toutes les touches
        for touche in self.__touches:
            touche.config(state=DISABLED)


    def getCurseurBDD(self):
        return self.__conn.cursor()

    
    def getIdMaxJoueur(self):
        return self.__idMaxJoueur


    def setIdJoueurCourant(self, id):
        self.__idJoueurCourant = id


    def setCouleurPoutre(self):
        
        # Demander une couleur au joueur
        c = colorchooser.askcolor(title='Choisissez votre couleur')[1] 

        # Changer la couleur de chaque élement
        for e in self.__zoneAffichage.getElementsPoutre():
            e.setCouleur(c)


    def setCouleurBonhomme(self):

        # Demander une couleur au joueur
        c = colorchooser.askcolor(title='Choisissez votre couleur')[1] 

        # Changer la couleur de chaque élement
        for e in self.__zoneAffichage.getElementsBonhomme():
            e.setCouleur(c)


    def setCouleurFond(self):
        
        # Demander une couleur au joueur
        c = colorchooser.askcolor(title='Choisissez votre couleur')[1] 

        # Changer la couleur de la zone d'affichage
        self.__zoneAffichage.config(bg = c)


    def incrIdMaxJoueur(self):
        self.__idMaxJoueur += 1


    def setNomJoueurCourant(self, nom):

        if nom == None:

            # Mode anonyme - pas de joueur selectionné
            self.__msgTexte.set("Aucun joueur selectionné. Vous êtes anonyme")
        
        else:

            # Joueur selectionné
            self.__msgTexte.set("Bonjour " + nom + " !")

        self.__msgLabel.update() # Bug macOs nécessite un update() manuel


    def gestionJoueur(self):

        # Vérifier si la fenêtre existe déjà
        if self.__enfant == None:

            # Non -> créer un nouveau objet
            self.__enfant = FenGestionJoueur(self)

        else:

            # Oui -> l'activer
            self.__enfant.activer()
 




class FenGestionJoueur(Toplevel):

    def __init__(self, parent: FenPrincipale):

        # Initialiser la classe parentale
        super().__init__(parent)

        self.geometry('300x250') # dimensions initiales
        self.minsize(300, 250) # dimensions minimales


        
        #
        # VARIABLES
        #

        # Référence à la fenêtre enfant
        self.__enfant = None

        # Référence à la fenêtre parentale
        self.__parent = parent


        #
        # --- Gestion de Joueurs ---

        # Un dictionnaire contenant les joueurs 
        self.__joueursDict = self.chargerJoueursBDD()



        #
        # L'ARBRE DE SCÈNE
        #

        #
        # --- La barre en bas ---
        self.__frame = Frame(self)
        self.__frame.pack(side=BOTTOM, pady=5)

        # Touche 'Annuler'
        self.__btnAnnuler = Button(self.__frame, text="Annuler")
        self.__btnAnnuler.pack(side=LEFT)

        # Touche 'Créer Nouveau Joueur'
        self.__btnNouveau = Button(self.__frame, text="Créer un nouveau joueur")
        self.__btnNouveau.pack(side=LEFT, padx=2)

        # Touche 'Confirmer'
        self.__btnConfirmer = Button(self.__frame, text="Confirmer", default=ACTIVE, state=DISABLED)
        self.__btnConfirmer.pack(side=LEFT)


        #
        # --- La liste de joueurs ---

        # La demande de selection
        self.__choixTexte = Label(self, text="Selectionnez votre nom de joueur:")
        self.__choixTexte.pack(side=TOP)

        # La liste ou choisir
        self.__choixListe = StringVar(self, self.creerListeJoueurs())
        self.__choixListbox = Listbox(self, listvariable=self.__choixListe, height=5)
        self.__choixListbox.pack(side=TOP)

        #
        # ASSOCIER DES ACTIONS AUX ÉLEMENTS GRAPHIQUES
        #

        self.__btnAnnuler.config(command=self.destroy)
        self.__btnNouveau.config(command=self.saisieJoueur)
        self.__btnConfirmer.config(command=self.confirmer)
        
        # Enter = click sur 'Confirmer'
        self.bind("<Return>", lambda e: self.confirmer())

        # Dégriser 'Confirmer' dès qu'un élement est selectionné
        self.__choixListbox.bind("<<ListboxSelect>>", lambda e: self.__btnConfirmer.config(state=NORMAL))


    def activer(self):

        # Lever la fenêtre
        self.lift()

        # Capturer les évènements
        self.focus()


    def destroy(self):

        # Supprimer la référence auprès de la fenêtre parentale
        self.__parent.fermetureEnfant()

        # Et puis appeler la méthode parentale
        super().destroy()
        

    def fermetureEnfant(self):

        # Marquer comme fermée
        self.__enfant = None
    

    def confirmer(self):

        # Obtenir le choix du joueur
        choix = str(self.__choixListbox.get(ACTIVE))

        # Extraire l'ID
        choix = choix.removeprefix("ID ") # python >= 3.9 obligatoire
        choix = choix[:choix.find(" - ")]

        # Passer la selection à la fenêtre principale
        self.selectionJoueur(int(choix))

        # Fermer la fenêtre
        self.destroy()


    def selectionJoueur(self, id):
        
        # Passer l'ID à la fenêtre principale
        self.__parent.setIdJoueurCourant(id)

        # Passer le nom à la fenêtre principale
        self.__parent.setNomJoueurCourant(self.__joueursDict[id] if id != None else None)

        # Réinitialiser la partie
        self.__parent.nouvellePartie()


    def chargerJoueursBDD(self):

        # Préparer la demande sql
        sql = "SELECT idjoueur, pseudo FROM Joueurs"

        # Objet qui permet la requête sql
        curseur = self.__parent.getCurseurBDD()


        #
        # --- Essai de récupérer la liste de noms ---

        try:
            curseur.execute(sql)

        except sqlite3.OperationalError as err:

            # Probablement le tableau n'existe pas encore
            # Dans ce cas, (ré)créer la structure de la bdd

            if "no such table" in str(err):
                self.__parent.creerStructureBDD()

            else:
                print("Une exception a été relévé: '" + str(err) + "', type d'exception: '" + type(err).__name__)

                return None

        except Exception as err:
            print("Une exception a été relévé: '" + str(err) + "', type d'exception: '" + type(err).__name__)

            return None
        
        #
        # --- Succès ---

        # Stocker les pseudo par les ID uniques
        joueursDict = {}

        for element in curseur.fetchall():

            # ID = element[0], pseudo = element[1]
            joueursDict[element[0]] = element[1]
        
        return joueursDict


    def ajouterJoueurBDD(self, pseudo):

        # Préparer la demande sql
        sql = 'INSERT INTO Joueurs (idjoueur,pseudo) VALUES (?,?)'

        # Objet qui permet la requête sql
        curseur = self.__parent.getCurseurBDD()

        # L'ID que le joueur obtiendra
        id = self.__parent.getIdMaxJoueur() + 1
    
        try:
            # Executer la demande
            curseur.execute(sql, (id, pseudo))

            # Si réussi, incrémenter idMaxJoueur
            self.__parent.incrIdMaxJoueur()

            # Et ajouter le joueur à la bdd
            self.__joueursDict[id] = pseudo

        except Exception as err:
            print("Une exception a été relévé: '" + str(err) + "', type d'exception: '" + type(err).__name__)

            return None

        # Retourner l'ID du joueur
        return id


    def creerListeJoueurs(self):
        
        # A partir du dictionnaire créer une liste avec l'ID et le pseudo
        listeJoueurs = [ "ID " + str(id) + " - '" + pseudo for id, pseudo in self.__joueursDict.items()]

        return listeJoueurs


    def saisieJoueur(self):
        
        # Vérifier si la fenêtre existe déjà
        if self.__enfant == None:

            # Non -> créer un nouveau objet
            self.__enfant = FenSaisieJoueur(self)

        else:

            # Oui -> Activer la fenêtre
            self.__enfant.activer()





class FenSaisieJoueur(Toplevel):

    def __init__(self, parent: FenGestionJoueur):

        # Initialiser la classe parentale + la fenêtre
        super().__init__(parent)

        self.geometry('200x200')
        self.minsize(200, 200)



        #
        # VARIABLES
        #

        # Enregistrer la fenêtre parentale
        self.__parent = parent


        
        #
        # L'ARBRE DE SCÈNE
        #

        #
        # --- La barre en bas ---
        self.__frame = Frame(self)
        self.__frame.pack(side=BOTTOM, pady=5)

        # Touche 'Annuler'
        self.__btnAnnuler = Button(self.__frame, text="Annuler")
        self.__btnAnnuler.pack(side=LEFT)

        # Touche 'Confirmer'
        self.__btnConfirmer = Button(self.__frame, text="Confirmer", default=ACTIVE, state=DISABLED)
        self.__btnConfirmer.pack(side=LEFT)


        #
        # --- La zone de saisie ---

        # Un texte aus dessus du champ de saisie
        self.__saisieDemande = Label(self, text="Saisissez votre nom de joueur:")
        self.__saisieDemande.pack(side=TOP)

        # Le champ de saisie
        self.__saisieTexte = StringVar()
        self.__saisie = Entry(self, textvariable=self.__saisieTexte)
        self.__saisie.pack(side=TOP)
        self.__saisie.focus()
        

        #
        # ASSOCIER LES ACTIONS AUX ÉLEMENTS GRAPHIQUES

        self.__btnAnnuler.config(command=self.destroy)
        self.__btnConfirmer.config(command=self.confirmer)

        # (Dé-)griser la touche selon que il y a au moins une lettre ou non
        self.__saisieTexte.trace_add("write", lambda *args: self.verificationSaisie())

        # Enter = click sur 'Confirmer'
        self.bind("<Return>", lambda e: self.confirmer())

    
    def activer(self):
        
        # Lever la fenêtre
        self.lift()

        # Capturer les évènements
        self.focus()

        # Selectionner la zone de saisie
        self.__saisie.focus()

    
    def destroy(self):
        
        # Supprimer la référence auprès de la fenêtre parentale
        self.__parent.fermetureEnfant()

        # Et puis appeler la méthode parentale
        super().destroy()


    def confirmer(self):

        # Vérifier que l'utilisateur a rentré un pseudo
        if len(self.__saisieTexte.get()) == 0:
            return
        
        # Ajouter le joueur à la bdd
        id = self.__parent.ajouterJoueurBDD(self.__saisieTexte.get())

        # Selectionner le joueur comme joueur courant
        self.__parent.selectionJoueur(id)

        # Fermer les fenêtres
        self.__parent.destroy()


    def verificationSaisie(self):

        # Si la zone de saisie est vide, griser le bouton 'Confirmer'
        if len(self.__saisieTexte.get()) == 0:
            self.__btnConfirmer.config(state=DISABLED)

        else:
            self.__btnConfirmer.config(state=NORMAL)

        
class HomePage(Tk):
    
    def __init__(self,color):
        Tk.__init__(self)
        #Image de l'écran d'acceuil
        self.__color = color
        self.configure(bg = self.__color)
        self.__im = Image.open('Hangman game/pendujeuv.png')
        self.__logo = ImageTk.PhotoImage(self.__im, master=self) 
        # le logo doit être un attribut ou bien l'image est écrasée par le garbage collector et l'on obitent un canva vide
        self.__dessin = Canvas(self,width = self.__im.size[0], height = self.__im.size[1], bg = self.__color)
        self.__logo1 = self.__dessin.create_image(0,0,anchor = NW,  image = self.__logo)
        self.__dessin.pack()
        self.title('Acceuil')
        #Pour que les fenêtres apparaissent au milieu de l'écran de l'utilisateur peu importe
        #son écran
        self.longueur_ecran = self.winfo_screenwidth()
        self.largeur_ecran= self.winfo_screenheight()
        self.geometry('250x250' +"+"+ str(int((self.longueur_ecran-500)/2)) +"+"+ str(int((self.largeur_ecran-500)/2)))
        self.minsize(width=100, height=100)
        self.resizable(False,False)
        self.iconbitmap('Hangman game/jeu.ico')
        #bouton play
        self.__Frame = Frame(self, bg = self.__color)
        self.__Frame.pack()
        buttonPlay = Button(self.__Frame, text = 'Play', font = ('Courier',10), command = self.Play, bg = self.__color)
        buttonPlay.pack(padx = 10, pady = (10,0))
        
    def Play(self):
        self.destroy()
        registration = FenPrincipale("jeuDuPendu.db")
        registration.mainloop()
        
        
        

if __name__ == "__main__":
    hp = HomePage("white")
    hp.mainloop()