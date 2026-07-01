import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton, QStatusBar, QStackedWidget)
from PyQt5.QtCore import Qt

# ========== CLASSE TRAITEMENT METIER ==========
class Ecrire:
    """Classe simple pour traiter le texte (Logique métier)"""
    
    def valider_nom(self, nom):
        """Ajoute un suffixe si le nom est valide, sinon gère le vide"""
        if nom == "":
            return "Message vide"
        return nom + " OK"


# ========== CLASSE INTERFACE GRAPHIQUE ==========
class UI:
    """Classe qui gère la fenêtre et les boutons"""
    
    def __init__(self):
        # On crée l'outil de traitement de texte directement ici
        self.outil_ecrire = Ecrire()
        
    def creer_interface(self):
        # 1. Fenêtre principale
        self.fenetre = QMainWindow()
        self.fenetre.setWindowTitle("Application Étudiant Simple")
        self.fenetre.resize(400, 200)
        
        # 2. Le gestionnaire de pages (Stacked Widget)
        self.pages = QStackedWidget()
        self.fenetre.setCentralWidget(self.pages)
        
        # 3. Barre d'état (en bas)
        self.barre_etat = QStatusBar()
        self.fenetre.setStatusBar(self.barre_etat)
        self.barre_etat.showMessage("Prêt", 2000)
        
        # ---- PAGE 0 : ACCUEIL ----
        page0 = QWidget()
        layout0 = QVBoxLayout()
        
        self.champ_nom = QLineEdit()
        self.champ_nom.setPlaceholderText("Entrez votre nom ici")
        layout0.addWidget(self.champ_nom)
        
        bouton_valider = QPushButton("Valider le nom (Aller Page 1)")
        # Connexion du bouton à l'action
        bouton_valider.clicked.connect(self.action_bouton_valider)
        layout0.addWidget(bouton_valider)
        
        page0.setLayout(layout0)
        self.pages.addWidget(page0) # Index 0
        
        # ---- PAGE 1 : RÉSULTAT ----
        page1 = QWidget()
        layout1 = QVBoxLayout()
        
        self.texte_resultat = QLabel("")
        self.texte_resultat.setAlignment(Qt.AlignCenter)
        layout1.addWidget(self.texte_resultat)
        
        bouton_retour = QPushButton("⬅ Retour")
        bouton_retour.clicked.connect(self.action_retour)
        layout1.addWidget(bouton_retour)
        
        page1.setLayout(layout1)
        self.pages.addWidget(page1) # Index 1

    def action_bouton_valider(self):
        """Action déclenchée par le bouton de la page 0"""
        saisie = self.champ_nom.text().strip()
        
        # Utilisation de la classe "Ecrire" pour traiter la saisie
        resultat = self.outil_ecrire.valider_nom(saisie)
        
        # Mise à jour de l'affichage
        self.texte_resultat.setText(f"Résultat : {resultat}")
        self.barre_etat.showMessage(f"Nom enregistré : {saisie}", 2000)
        
        # Changement de page (Aller à la page 1)
        self.pages.setCurrentIndex(1)
        
    def action_retour(self):
        """Action pour revenir à l'accueil"""
        self.pages.setCurrentIndex(0)
        self.barre_etat.showMessage("Retour à l'accueil", 2000)

    def lancer(self):
        """Affiche la fenêtre"""
        self.creer_interface()
        self.fenetre.show()


# ========== PROGRAMME PRINCIPAL ==========
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Lancement global
    interface = UI()
    interface.lancer()
    
    sys.exit(app.exec_())