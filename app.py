import pandas as pd
import os
import hashlib
import requests
import tkinter as tk
from tkinter import messagebox


products = []
users_db_file = "users.csv"
products_file = "produits.csv"


def charger_donnees():
    global products
    if os.path.exists(products_file):
        products = pd.read_csv(products_file).to_dict('records')
        print("Données chargées depuis le fichier CSV.")
    else:
        print("Aucun fichier existant pour charger.")


def sauvegarder_donnees():
    df = pd.DataFrame(products)
    df.to_csv(products_file, index=False)
    print("Données sauvegardées dans 'produits.csv'.")

def afficher_produits():
    if not products:
        print("La liste est vide.")
    else:
        print("\nListe des produits :")
        for produit in products:
            print(f"Nom : {produit['nom']}, Prix : {produit['prix']}, Quantité : {produit['quantite']}")


def ajouter_produit():
    try:
        nom = input("Entrez le nom du produit : ")
        prix = float(input("Entrez le prix : "))
        quantite = int(input("Entrez la quantité : "))
        products.append({"nom": nom, "prix": prix, "quantite": quantite})
        print("Produit ajouté avec succès!")
    except ValueError:
        print("Erreur : Valeurs invalides.")


def supprimer_produit():
    nom = input("Entrez le nom du produit à supprimer : ")
    global products
    products = [p for p in products if p['nom'].lower() != nom.lower()]
    print("Produit supprimé avec succès!")


def rechercher_produit():
    terme = input("Entrez le terme de recherche : ")
    resultats = [p for p in products if terme.lower() in p['nom'].lower()]
    if resultats:
        print("\nRésultats de la recherche :")
        for produit in resultats:
            print(produit)
    else:
        print("Aucun produit trouvé.")

def menu():
    while True:
        print("\nMenu :")
        print("1. Afficher la liste des produits")
        print("2. Ajouter un produit")
        print("3. Supprimer un produit")
        print("4. Rechercher un produit")
        print("5. Sauvegarder les données")
        print("6. Charger les données")
        print("7. Quitter")
        choix = input("Votre choix : ")

        if choix == "1":
            afficher_produits()
        elif choix == "2":
            ajouter_produit()
        elif choix == "3":
            supprimer_produit()
        elif choix == "4":
            rechercher_produit()
        elif choix == "5":
            sauvegarder_donnees()
        elif choix == "6":
            charger_donnees()
        elif choix == "7":
            print("Fermeture du programme...")
            sauvegarder_donnees()
            break
        else:
            print("Choix invalide.")

def generer_hachage_motdepasse(mot_de_passe):
    sel = os.urandom(16).hex()
    mot_hache = hashlib.sha256((mot_de_passe + sel).encode()).hexdigest()
    return f"{sel}${mot_hache}"


def enregistrer_utilisateur():
    utilisateur = input("Entrez votre nom d'utilisateur : ")
    mot_de_passe = input("Entrez votre mot de passe : ")
    mot_hache = generer_hachage_motdepasse(mot_de_passe)
    
    if os.path.exists(users_db_file):
        df = pd.read_csv(users_db_file)
    else:
        df = pd.DataFrame(columns=["utilisateur", "mot_hache"])
        
    df = df.append({"utilisateur": utilisateur, "mot_hache": mot_hache}, ignore_index=True)
    df.to_csv(users_db_file, index=False)
    print("Utilisateur enregistré avec succès.")

if __name__ == "__main__":
    charger_donnees()
    menu()
