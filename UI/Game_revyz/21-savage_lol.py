# ============================================
# JEU DU 21 - Version mathématique
# Règle : Chaque joueur retire 1, 2 ou 3 points.
# Celui qui prend le dernier point perd.
# ============================================

import random

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

# --- 1. Initialisation du jeu ---
total = 21  # Le nombre de points au départ
joueur_actuel = "joueur"  # Le joueur commence toujours

# --- 2. Boucle principale du jeu (fonction) ---
while total > 0:  # Tant qu'il reste des points
    print("\n" + "="*40)  # Une ligne de séparation pour la lisibilité
    print(f"Il reste {total} points.")  # Affiche le total actuel
    
    # --- 3. Tour du joueur (fonction) ---
    if joueur_actuel == "joueur":
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
        
        # Si le total atteint 0, le joueur a pris le dernier point -> il perd
        if total == 0:
            print("\n💀 Tu as pris le dernier point... TU PERDS !")
            break  # Sort de la boucle principale
        
        # Sinon, c'est au tour de l'ordinateur
        joueur_actuel = "ordinateur"
    
    # --- 4. Tour de l'ordinateur ---
    else:
        print("Tour de l'ordinateur...")
        
        # --- Stratégie de l'ordinateur ---
        # L'ordinateur cherche à laisser un multiple de 4 à l'adversaire
        # Pour cela, il doit retirer (total % 4) points
        # Sauf si (total % 4) == 0, alors il retire un nombre aléatoire (mais jamais 0)
        
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
            # Cas particulier : si retrait == 0, on le passe à 1 (mais normalement ça n'arrive pas)
            if retrait == 0:
                retrait = 1
        
        # On retire les points choisis par l'ordinateur
        total = total - retrait
        print(f"🤖 L'ordinateur a retiré {retrait} points.")
        
        # Si le total atteint 0, l'ordinateur a pris le dernier point -> il perd
        if total == 0:
            print("\n🎉 L'ordinateur a pris le dernier point... TU GAGNES !")
            break  # Sort de la boucle principale
        
        # Sinon, c'est au tour du joueur
        joueur_actuel = "joueur"

# --- 5. Fin du jeu ---
print("\n" + "="*40)
print("Partie terminée !")