import pandas as pd
import os


products = []


def afficher_produits():
    if not products:
        print("La liste est vide.")
    else:
        print("\nListe des produits :")
        for produit in products:
            print(produit)


def ajouter_produit():
    nom = input("Entrez le nom du produit : ")
    try:
        prix = float(input("Entrez le prix : "))
        quantite = int(input("Entrez la quantité : "))
        products.append({"nom": nom, "prix": prix, "quantite": quantite})
        print("Produit ajouté avec succès!")
    except ValueError:
        print("Valeur incorrecte. Réessayez.")


def supprimer_produit():
    nom = input("Entrez le nom du produit à supprimer : ")
    global products
    products = [p for p in products if p['nom'].lower() != nom.lower()]
    print("Produit supprimé avec succès!")


def sauvegarder_donnees():
    df = pd.DataFrame(products)
    df.to_csv('produits.csv', index=False)
    print("Données sauvegardées dans 'produits.csv'.")


def charger_donnees():
    global products
    if os.path.exists('produits.csv'):
        products = pd.read_csv('produits.csv').to_dict('records')
        print("Données chargées depuis le fichier CSV.")
    else:
        print("Aucun fichier existant pour charger.")


def menu():
    while True:
        print("\nMenu :")
        print("1. Afficher les produits")
        print("2. Ajouter un produit")
        print("3. Supprimer un produit")
        print("4. Sauvegarder")
        print("5. Charger")
        print("6. Quitter")
        choix = input("Votre choix : ")

        if choix == "1":
            afficher_produits()
        elif choix == "2":
            ajouter_produit()
        elif choix == "3":
            supprimer_produit()
        elif choix == "4":
            sauvegarder_donnees()
        elif choix == "5":
            charger_donnees()
        elif choix == "6":
            print("Fermeture du programme...")
            break
        else:
            print("Choix invalide.")

import hashlib
import os

def generer_hachage_motdepasse(mot_de_passe):
    sel = os.urandom(16).hex()
    mot_hache = hashlib.sha256((mot_de_passe + sel).encode()).hexdigest()
    return f"{sel}${mot_hache}"

import requests


def verifier_compromis(email):
    try:
        url = f"https://api.pwnedpasswords.com/range/{email[:5]}"
        response = requests.get(url)

        if response.status_code == 200:
            print("Requête réussie.")
        else:
            print("Erreur API.")
    except Exception as e:
        print(f"Erreur : {e}")
import tkinter as tk
from tkinter import messagebox


def creer_interface():
    root = tk.Tk()
    root.title("Gestion de Produits")

    def afficher_produits_graphique():
        text = "\n".join([f"Nom : {p['nom']}, Prix : {p['prix']}, Quantité : {p['quantite']}" for p in products])
        produit_text.delete("1.0", tk.END)
        produit_text.insert(tk.END, text)

    tk.Label(root, text="Gestion de vos produits").pack()
    produit_text = tk.Text(root, height=15, width=50)
    produit_text.pack()

    btn_afficher = tk.Button(root, text="Afficher Produits", command=afficher_produits_graphique)
    btn_afficher.pack()

    root.mainloop()

charger_donnees()
menu()
creer_interface()
