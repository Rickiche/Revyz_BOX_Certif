# ============================================
# JEU DU 21 - Version mathématique
# Règle : Chaque joueur retire 1, 2 ou 3 points.
# Celui qui prend le dernier point perd.
# ============================================

from tkinter import *
import random

# --- FONCTION POUR AFFICHER LES RÈGLES ---
def afficher_regles():
    """Affiche les règles du jeu dans la console"""
    print("="*50)
    print("LE JEU DU 21 !")
    print("="*50)
    print("\n📖 RÈGLES DU JEU :")
    print("Le jeu commence avec 21 points, chacun son tour, toi et l'ordinateur pouvez retirer 1, 2 ou 3 points." \
    " Celui qui prend le DERNIER point perd la partie. " \
    "\nPour gagner, il faut forcer l'adversaire à prendre le dernier point.")
    print("\n💡 ASTUCE : Laisse toujours un multiple de 4 à ton adversaire !")
    print("   (4, 8, 12, 16 ou 20) pour être sûr de gagner.")
    print("\n" + "="*50)
    input("Appuie sur ENTRÉE pour commencer la partie...")
    print("\n" * 2)

# --- FONCTION D'INITIALISATION ---
def initialiser_jeu():
    """
    Initialise les variables du jeu
    Retourne : tuple (total, joueur_actuel)
    """
    total = 21  # Le nombre de points au départ
    joueur_actuel = "joueur"  # Le joueur commence toujours
    return total, joueur_actuel

# --- FONCTION POUR LE TOUR DU JOUEUR ---
def tour_joueur(total):
    """
    Gère le tour du joueur
    Paramètre : total (le nombre de points restants)
    Retourne : tuple (nouveau_total, joueur_suivant, jeu_termine)
    """
    print("\n" + "="*40)
    print(f"Il reste {total} points.")
    print("À ton tour !")
    
    # Boucle pour s'assurer que le joueur entre un nombre valide
    while True:
        try:
            retrait = int(input("Combien veux-tu enlever ? (1, 2 ou 3) : "))
            # Vérifie si le nombre est entre 1 et 3
            if 1 <= retrait <= 3:
                # Vérifie qu'on ne retire pas plus que ce qui reste
                if retrait <= total:
                    break  # Sort de la boucle si tout est bon
                else:
                    print(f"❌ Il ne reste que {total} points, tu ne peux pas en retirer {retrait} !")
            else:
                print("❌ Tu dois choisir 1, 2 ou 3 !")
        except ValueError:  # Si l'utilisateur entre autre chose qu'un nombre
            print("❌ Entre un nombre valide !")
    
    # On retire les points choisis par le joueur
    total = total - retrait
    print(f"✅ Tu as retiré {retrait} points.")
    
    # Vérifie si le joueur a perdu
    if total == 0:
        print("\n💀 Tu as pris le dernier point... TU PERDS !")
        return total, None, True  # Jeu terminé
    
    # Sinon, c'est au tour de l'ordinateur
    return total, "ordinateur", False



# CLASSE DE L'INTERFACE GRAPHIQUE
class Interface21:
    def __init__(self):
        self.total = 21
        self.joueur_actuel = "joueur"
        self.jeu_termine = False
        self.tour_ordinateur_en_cours = False
        self.afficher_regles()
        self.creer_widget()

    def creer_widget(self):
        fenetre = Tk()





# --- FONCTION POUR LE TOUR DE L'ORDINATEUR ---
def tour_ordinateur(total):
    """
    Gère le tour de l'ordinateur avec sa stratégie
    Paramètre : total (le nombre de points restants)
    Retourne : tuple (nouveau_total, joueur_suivant, jeu_termine)
    """
    print("\n" + "="*40)
    print(f"Il reste {total} points.")
    print("Tour de l'ordinateur...")
    
    # --- Stratégie de l'ordinateur ---
    # L'ordinateur cherche à laisser un multiple de 4 à l'adversaire
    reste = total % 4  # Calcule le reste de la division par 4
    
    if reste == 0:
        # Si le total est déjà un multiple de 4, l'ordinateur est en difficulté
        # Il retire 1, 2 ou 3 au hasard
        retrait = random.randint(1, 3)
        # Mais il ne doit pas retirer plus que ce qui reste
        if retrait > total:
            retrait = total
    else:
        # Sinon, il retire exactement ce qu'il faut pour laisser un multiple de 4
        retrait = reste
        # Cas particulier : si retrait == 0, on le passe à 1 (normalement ça n'arrive pas)
        if retrait == 0:
            retrait = 1
    
    # On retire les points choisis par l'ordinateur
    total = total - retrait
    print(f"🤖 L'ordinateur a retiré {retrait} points.")
    
    # Vérifie si l'ordinateur a perdu
    if total == 0:
        print("\n🎉 L'ordinateur a pris le dernier point... TU GAGNES !")
        return total, None, True  # Jeu terminé
    
    # Sinon, c'est au tour du joueur
    return total, "joueur", False

# --- FONCTION POUR JOUER UNE PARTIE ---
def jouer_partie():
    """
    Fonction principale qui gère le déroulement d'une partie complète
    """
    # Initialisation
    total, joueur_actuel = initialiser_jeu()
    jeu_termine = False
    
    # Boucle principale du jeu
    while not jeu_termine and total > 0:
        if joueur_actuel == "joueur":
            total, joueur_actuel, jeu_termine = tour_joueur(total)
        else:  # ordinateur
            total, joueur_actuel, jeu_termine = tour_ordinateur(total)
    
    # --- Fin du jeu ---
    print("\n" + "="*40)
    print("Partie terminée !")
    return jeu_termine  # Retourne True si la partie s'est bien terminée

# --- FONCTION POUR DEMANDER UNE REVANCHE ---
def demander_revanche():
    """
    Demande au joueur s'il veut rejouer
    Retourne : True si le joueur veut rejouer, False sinon
    """
    print("\n" + "="*40)
    reponse = input("Veux-tu rejouer ? (o/n) : ").lower()
    while reponse not in ['o', 'n', 'oui', 'non']:
        print("❌ Réponds par 'o' (oui) ou 'n' (non) !")
        reponse = input("Veux-tu rejouer ? (o/n) : ").lower()
    
    return reponse in ['o', 'oui']

# --- PROGRAMME PRINCIPAL ---
def main():
    """
    Fonction principale du programme
    Gère l'affichage des règles et les parties successives
    """
    # Affiche les règles
    afficher_regles()
    
    # Boucle principale pour les parties
    continuer = True
    while continuer:
        # Joue une partie
        jouer_partie()
        
        # Demande si le joueur veut rejouer
        continuer = demander_revanche()
    
    print("\n" + "="*40)
    print("Merci d'avoir joué ! À bientôt ! 🎲")

# --- LANCEMENT DU PROGRAMME ---
if __name__ == "__main__":
    main()