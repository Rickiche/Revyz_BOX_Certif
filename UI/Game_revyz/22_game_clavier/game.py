import random

class Game:
    def __init__(self):
        """
        Initialise une nouvelle partie
        """
        self.total = 21
        self.joueur_actuel = 'joueur'  # 'joueur' ou 'ordinateur'
        self.est_termine = False
        self.dernier_coup = None
        self.message = "A toi de jouer !"
    
    def get_total(self):
        """Retourne le nombre de points restants"""
        return self.total
    
    def get_joueur_actuel(self):
        """Retourne le joueur actuel"""
        return self.joueur_actuel
    
    def est_termine(self):
        """Retourne True si la partie est terminée"""
        return self.est_termine
    
    def get_message(self):
        """Retourne le message actuel"""
        return self.message
    
    def get_dernier_coup(self):
        """Retourne le dernier coup joué"""
        return self.dernier_coup
    
    def jouer_coup_joueur(self, retrait):
        """
        Joue un coup pour le joueur
        Paramètre : retrait (1, 2 ou 3)
        Retourne : dict avec le résultat
        """
        # Vérifications
        if self.est_termine:
            return {'erreur': 'Partie terminée !'}
        
        if self.joueur_actuel != 'joueur':
            return {'erreur': "Ce n'est pas ton tour !"}
        
        if retrait < 1 or retrait > 3:
            return {'erreur': 'Choisis 1, 2 ou 3 !'}
        
        if retrait > self.total:
            return {'erreur': f"Il reste {self.total} points !"}
        
        # Action
        self.total -= retrait
        self.dernier_coup = retrait
        self.message = f"Tu as retiré {retrait} point{'s' if retrait > 1 else ''}"
        
        # Vérification de défaite
        if self.total == 0:
            self.est_termine = True
            self.message = "Tu as pris le dernier point... TU PERDS !"
            return {'succes': True, 'termine': True}
        
        # Passage à l'ordinateur
        self.joueur_actuel = 'ordinateur'
        self.message += "\nL'ordinateur réfléchit..."
        return {'succes': True, 'termine': False}
    
    def jouer_coup_ordinateur(self):
        """
        Joue le coup de l'ordinateur avec stratégie
        Retourne : dict avec le résultat
        """
        # Vérifications
        if self.est_termine:
            return {'erreur': 'Partie terminée !'}
        
        if self.joueur_actuel != 'ordinateur':
            return {'erreur': "Ce n'est pas le tour de l'ordinateur !"}
        
        # Stratégie : laisser un multiple de 4
        reste = self.total % 4
        
        if reste == 0:
            # L'ordinateur est en difficulté : retire au hasard
            retrait = random.randint(1, min(3, self.total))
        else:
            # L'ordinateur laisse un multiple de 4
            retrait = min(reste, self.total)
        
        # Action
        self.total -= retrait
        self.dernier_coup = retrait
        self.message = f"L'ordinateur a retiré {retrait} point{'s' if retrait > 1 else ''}"
        
        # Vérification de victoire
        if self.total == 0:
            self.est_termine = True
            self.message = "L'ordinateur a pris le dernier point... TU GAGNES !"
            return {'succes': True, 'termine': True}
        
        # Passage au joueur
        self.joueur_actuel = 'joueur'
        self.message += "\nA toi de jouer !"
        return {'succes': True, 'termine': False}
    
    def reinitialiser(self):
        """
        Réinitialise la partie (conserve les statistiques)
        """
        self.total = 21
        self.joueur_actuel = 'joueur'
        self.est_termine = False
        self.dernier_coup = None
        self.message = "Nouvelle partie ! A toi de jouer !"