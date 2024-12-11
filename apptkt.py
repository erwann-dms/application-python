import os
import hashlib

products = []
users_db_file = "users.csv"
products_file = "produits.csv"

def charger_donnees():
    global products
    if os.path.exists(products_file):
        with open(products_file, "r") as file:
            next(file)
            for line in file:
                nom, prix, quantite = line.strip().split(",")
                try:
                    products.append({"nom": nom, "prix": float(prix), "quantite": int(quantite)})
                except ValueError:
                    print(f"Erreur lors de la conversion des données: {line.strip()}")
        print("Données chargées depuis le fichier.")
    else:
        print("Aucun fichier existant pour charger.")

def sauvegarder_donnees():
    with open(products_file, "w") as file:
        for produit in products:
            file.write(f"{produit['nom']},{produit['prix']},{produit['quantite']}\n")
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

def recherche_binaire(terme):
    products_sorted = sorted(products, key=lambda x: x['nom'].lower())
    low, high = 0, len(products_sorted) - 1
    while low <= high:
        mid = (low + high) // 2
        if products_sorted[mid]['nom'].lower() == terme.lower():
            return products_sorted[mid]
        elif products_sorted[mid]['nom'].lower() < terme.lower():
            low = mid + 1
        else:
            high = mid - 1
    return None

def rechercher_produit_binaire():
    terme = input("Entrez le terme de recherche : ")
    produit = recherche_binaire(terme)
    if produit:
        print(f"Produit trouvé : {produit}")
    else:
        print("Aucun produit trouvé.")

def tri_bulles_par_prix():
    for i in range(len(products)):
        for j in range(0, len(products) - i - 1):
            if products[j]['prix'] > products[j + 1]['prix']:
                products[j], products[j + 1] = products[j + 1], products[j]
    afficher_produits()

def tri_bulles_par_quantite():
    for i in range(len(products)):
        for j in range(0, len(products) - i - 1):
            if products[j]['quantite'] > products[j + 1]['quantite']:
                products[j], products[j + 1] = products[j + 1], products[j]
    afficher_produits()

def tri_rapide_par_prix(products):
    if len(products) <= 1:
        return products
    pivot = products[len(products) // 2]['prix']
    left = [p for p in products if p['prix'] < pivot]
    middle = [p for p in products if p['prix'] == pivot]
    right = [p for p in products if p['prix'] > pivot]
    return tri_rapide_par_prix(left) + middle + tri_rapide_par_prix(right)

def tri_rapide_par_quantite(products):
    if len(products) <= 1:
        return products
    pivot = products[len(products) // 2]['quantite']
    left = [p for p in products if p['quantite'] < pivot]
    middle = [p for p in products if p['quantite'] == pivot]
    right = [p for p in products if p['quantite'] > pivot]
    return tri_rapide_par_quantite(left) + middle + tri_rapide_par_quantite(right)

def menu():
    while True:
        print("\nMenu :")
        print("1. Afficher la liste des produits")
        print("2. Ajouter un produit")
        print("3. Supprimer un produit")
        print("4. Rechercher un produit")
        print("5. Sauvegarder les données")
        print("6. Charger les données")
        print("7. Trier les produits par prix (tri à bulles)")
        print("8. Trier les produits par quantité (tri à bulles)")
        print("9. Trier les produits par prix (tri rapide)")
        print("10. Trier les produits par quantité (tri rapide)")
        print("11. Rechercher un produit (binaire)")
        print("12. Quitter")
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
            tri_bulles_par_prix()
        elif choix == "8":
            tri_bulles_par_quantite()
        elif choix == "9":
            products[:] = tri_rapide_par_prix(products)
            afficher_produits()
        elif choix == "10":
            products[:] = tri_rapide_par_quantite(products)
            afficher_produits()
        elif choix == "11":
            rechercher_produit_binaire()
        elif choix == "12":
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
        with open(users_db_file, "a") as file:
            file.write(f"{utilisateur},{mot_hache}\n")
    else:
        with open(users_db_file, "w") as file:
            file.write("utilisateur,mot_hache\n")
            file.write(f"{utilisateur},{mot_hache}\n")
    
    print("Utilisateur enregistré avec succès.")

if __name__ == "__main__":
    charger_donnees()
    menu()
