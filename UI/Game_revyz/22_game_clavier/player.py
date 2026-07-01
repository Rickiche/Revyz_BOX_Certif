class Player:
    def __init__(self, nom="Joueur"):
        """
        Initialise un nouveau joueur
        Paramètre : nom (str) - Nom du joueur
        """
        self.nom = nom
        self.victoires = 0
        self.defaites = 0
    
    def get_nom(self):
        """Retourne le nom du joueur"""
        return self.nom
    
    def get_victoires(self):
        """Retourne le nombre de victoires"""
        return self.victoires
    
    def get_defaites(self):
        """Retourne le nombre de défaites"""
        return self.defaites
    
    def ajouter_victoire(self):
        """Ajoute une victoire au compteur"""
        self.victoires += 1
    
    def ajouter_defaite(self):
        """Ajoute une défaite au compteur"""
        self.defaites += 1
    
    def reinitialiser_stats(self):
        """Réinitialise les statistiques"""
        self.victoires = 0
        self.defaites = 0