#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################ Jeu #####################

class Jeu:
    def __init__(self, nom_fichier):
        self.grotte = []                                               
        self.lemmings = []                            # Liste pour stocker les lemmings
        with open(nom_fichier, "r", encoding = "utf-8") as fichier:      #Ouverture du fichier et transformation en liste d'instances de Case
            for ligne in fichier:
                ligne = ligne.strip()
                ligne_de_cases = [Case(caractere) for caractere in ligne]
                self.grotte.append(ligne_de_cases)

    def __getitem__(self, i):                  
        return self.grotte[i]

    def affiche(self):
        """Affiche la grotte avec les lemmmings s'il y en a"""
        for ligne in self.grotte:
            print(''.join(str(case) for case in ligne))


    def ajoute1lemming(self):
        """Ajoute un lemming a l'entrée de la grotte (on considere cette derniere toujours au meme endroit)"""
        if self.grotte[0][3].est_libre():
            lem = Lemming(self, 0, 3)
            self.lemmings.append(lem)
            self.grotte[0][3].arrive(lem)

    def tour(self):
        """Fait réaliser une action a chaque instance de Lemming dans la liste"""
        print("")
        for lems in self.lemmings:
            lems.action()
        self.affiche()
        print("")


    def demarre(self):
        """Fait derouler le jeu selon les entrées réalisées par l'utilisateur"""
        inpt = None
        self.affiche()
        print("")
        print(" - Saisir 'q' pour quitter le jeu")
        print(" - Saisir 'l' pour ajouter un lemming")
        print(" - Saisir 'n' pour choisir de combien de fois vous voulez faire avancer le jeu")
        print(" - Saisir nimporte quelle autre touche pour faire avancer le jeu une fois")
        while True:
            while True:
                print("")
                inpt = input("-------------------------> Votre choix : ")
                if inpt != "":
                    break
                else:
                    print("Ce choix est invalide")
            if inpt == "q":
                print("Merci d'avoir joué!")
                break
            elif inpt == "l":
                print("")
                self.ajoute1lemming()
                self.affiche()
            elif inpt == "n":
                while True:
                    nb = input("-------------------------> Choisissez un nombre de tours : ")
                    for _ in range(int(nb)):
                        self.tour()
                    break
            else:
                self.tour()

################# Lemming ######################

class Lemming:
    
    def __init__(self, j, l, c):
        self.j = j
        self.l = l
        self.d = 1
        self.c = c

    def __str__(self):
        if self.d == 1:
            return ">"
        elif self.d == -1:
            return "<"
        else:
            return "Erreur de direction"

    def deplace(self, l, c):
        """Si la case indiquée est libre, copie le lemming sur cette case"""
        if self.j[l][c].est_libre():
            self.j[l][c].arrive(self)
            return True
        else:
            return False

    def action(self):
        """Deplace ou fait changer de direction le lemming, en le copiant sur le prochain emplacement et supprimant son emplacement actuel"""
        if self.d == 1:
            if self.deplace(self.l + 1, self.c):
                self.j[self.l][self.c].enleve()
                self.l += 1
            elif self.deplace(self.l, self.c + 1):
                self.j[self.l][self.c].enleve()
                self.c += 1
            else:
                self.d = -1
        elif self.d == -1:
            if self.deplace(self.l + 1, self.c):
                self.j[self.l][self.c].enleve()
                self.l += 1
            elif self.deplace(self.l, self.c-1):
                self.j[self.l][self.c].enleve()
                self.c -= 1
            else:
                self.d = 1


    def retire(self):
        """Retire le lemming de la liste des lemmings du jeu"""
        self.j.lemmings.remove(self)
        
#################### Case #####################

class Case:
    
    def __init__(self, caractere):
        assert caractere == " " or caractere == "#" or caractere == "0", "Valeur incorrecte"
        self.terrain = caractere
        self.lem = None

    def __str__(self):
        if self.lem is not None:
            return str(self.lem)
        else:
            return self.terrain

    def est_libre(self):
        """Renvoie True si la case est libre ou est la sortie et False sinon"""
        return (self.terrain == " " or self.terrain == "0") and self.lem is None

    def enleve(self):
        """Enleve le lemming de la case"""
        self.lem = None

    def arrive(self, lem):
        """Si la case est la sortie, retire le lemming, sinon la case acceuille le lemming"""
        if self.terrain == "0":
            lem.retire()
        else:
            self.lem = lem

def game():
    print("3 cartes sont disponibles.")
    choix = int(input("Sur quelle carte voulez vous jouer?:"))
    