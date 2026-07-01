import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton, QStatusBar,
                             QMenuBar, QAction, QMessageBox, QStackedWidget)
from PyQt5.QtCore import Qt

# ========== CLASSE ECRIRE ==========
class Ecrire:
    """Classe qui gère le traitement et le formatage des messages"""
    
    @staticmethod
    def ecrire_message(msg):
        """Fonction qui traite et formate un message"""
        if msg == "":
            msg = "Message vide"
        else:
            # On peut ajouter un traitement personnalisé ici
            msg = msg + " OK"
        return msg
    
    @staticmethod
    def formater_titre(titre):
        """Formate un titre avec des décorations"""
        return f"{titre}"
    
    @staticmethod
    def formater_sous_titre(sous_titre):
        """Formate un sous-titre"""
        return f"{sous_titre}"


# ========== CLASSE UI ==========
class UI:
    """Classe qui gère l'interface utilisateur et les interactions"""
    
    def __init__(self):
        """Initialise les variables de l'interface"""
        self.champ_nom = None
        self.etiquette_resultat = None
        self.barre_etat = None
        self.fenetre = None
        self.stacked_widget = None
        self.page_principale = None
        self.page1 = None
        self.page2 = None
        
        # Instance de la classe Ecrire pour l'utiliser dans cette classe
        self.ecrire = Ecrire()
    
    def on_click_saluer(self):
        """Fonction appelée quand on clique sur 'Dire bonjour !'"""
        nom = self.champ_nom.text().strip()
        if not nom:
            self.etiquette_resultat.setText("Veuillez entrer un nom !")
            self.barre_etat.showMessage("Nom vide", 2000)
        else:
            self.etiquette_resultat.setText(f"Bonjour, {nom} !")
            self.barre_etat.showMessage(f"A salué {nom}", 2000)
    
    def afficher_a_propos(self):
        """Fonction appelée quand on clique sur 'À propos'"""
        QMessageBox.about(
            self.fenetre,
            "À propos de Mon App",
            "Ceci est une application d'exemple PyQt5.\n\n"
            "Elle démontre une fenêtre principale avec des menus, "
            "une saisie, des boutons et des messages d'état."
        )
    
    def ouvrir_page1(self):
        """Ouvre la page 1 (via Fenetre1)"""
        self.stacked_widget.setCurrentIndex(1)  # Index 1 = page1
        # Utilisation de la classe Ecrire pour formater le message
        message = Ecrire.ecrire_message("Page 1 ouverte")
        self.barre_etat.showMessage(message, 2000)
    
    def ouvrir_page2(self):
        """Ouvre la page 2 (via Fenetre2)"""
        self.stacked_widget.setCurrentIndex(2)  # Index 2 = page2
        # Utilisation de la classe Ecrire pour formater le message
        message = Ecrire.ecrire_message("Page 2 ouverte")
        self.barre_etat.showMessage(message, 2000)
    
    def retourner_page_principale(self):
        """Retourne à la page principale"""
        self.stacked_widget.setCurrentIndex(0)  # Index 0 = page_principale
        message = Ecrire.ecrire_message("Retour à la page principale")
        self.barre_etat.showMessage(message, 2000)
    
    def creer_interface(self):
        """Crée et configure toute l'interface utilisateur"""
        
        # --- Créer la fenêtre principale ---
        self.fenetre = QMainWindow()
        self.fenetre.setWindowTitle("Mon App - Avec plusieurs pages")
        self.fenetre.resize(500, 250)
        self.fenetre.move(300, 50)
        
        # --- Créer le widget central QStackedWidget pour gérer les pages ---
        widget_central = QWidget()
        self.fenetre.setCentralWidget(widget_central)
        
        # Layout principal qui contiendra le stacked widget
        layout_principal = QVBoxLayout()
        widget_central.setLayout(layout_principal)
        
        # Créer le QStackedWidget
        self.stacked_widget = QStackedWidget()
        layout_principal.addWidget(self.stacked_widget)
        
        # --- Créer toutes les pages ---
        self.creer_page_principale()
        self.creer_page1()
        self.creer_page2()
        
        # Afficher la page principale par défaut
        self.stacked_widget.setCurrentIndex(0)
        
        # --- Configurer la barre d'état ---
        self.barre_etat = QStatusBar()
        self.fenetre.setStatusBar(self.barre_etat)
        message = Ecrire.ecrire_message("Prêt")
        self.barre_etat.showMessage(message, 2000)
        
        # --- Configurer la barre de menu ---
        self.creer_menu()
    
    def creer_page_principale(self):
        """Crée la page principale avec le formulaire de saisie"""
        self.page_principale = QWidget()
        mise_en_page = QVBoxLayout()
        self.page_principale.setLayout(mise_en_page)
        
        etiquette = QLabel("Entrez votre nom :")
        mise_en_page.addWidget(etiquette)
        
        self.champ_nom = QLineEdit()
        self.champ_nom.setPlaceholderText("Votre nom ici")
        mise_en_page.addWidget(self.champ_nom)
        
        bouton_saluer = QPushButton("Dire bonjour !")
        bouton_saluer.clicked.connect(self.on_click_saluer)
        mise_en_page.addWidget(bouton_saluer)
        
        self.etiquette_resultat = QLabel("")
        self.etiquette_resultat.setAlignment(Qt.AlignCenter)
        mise_en_page.addWidget(self.etiquette_resultat)
        
        mise_en_page.addStretch()  # espaceur
        
        # Ajouter la page principale au stacked widget (index 0)
        self.stacked_widget.addWidget(self.page_principale)
    
    def creer_page1(self):
        """Crée la page 1 (accessible via Fenetre1)"""
        self.page1 = QWidget()
        mise_en_page = QVBoxLayout()
        self.page1.setLayout(mise_en_page)
        
        # Titre de la page
        titre_page1 = QLabel(Ecrire.formater_titre("Bienvenue sur la Page 1"))
        titre_page1.setAlignment(Qt.AlignCenter)
        titre_page1.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        mise_en_page.addWidget(titre_page1)
        
        # Description
        description1 = QLabel(
            "Ceci est la page 1 !\n\n"
            "Accessible via le menu 'Fenetre1'."
        )
        description1.setAlignment(Qt.AlignCenter)
        mise_en_page.addWidget(description1)
        
        # Bouton pour revenir à la page principale
        bouton_retour1 = QPushButton("⬅ Retour à la page principale")
        bouton_retour1.clicked.connect(self.retourner_page_principale)
        mise_en_page.addWidget(bouton_retour1)
        
        mise_en_page.addStretch()
        
        # Ajouter la page 1 au stacked widget (index 1)
        self.stacked_widget.addWidget(self.page1)
    
    def creer_page2(self):
        """Crée la page 2 (accessible via Fenetre2)"""
        self.page2 = QWidget()
        mise_en_page = QVBoxLayout()
        self.page2.setLayout(mise_en_page)
        
        # Titre de la page
        titre_page2 = QLabel(Ecrire.formater_titre("Bienvenue sur la Page 2"))
        titre_page2.setAlignment(Qt.AlignCenter)
        titre_page2.setStyleSheet("font-size: 18px; font-weight: bold; color: #e74c3c;")
        mise_en_page.addWidget(titre_page2)
        
        # Description
        description2 = QLabel(
            "Ceci est la page 2 !\n\n"
            "Accessible directement via le menu 'Fenetre2'."
        )
        description2.setAlignment(Qt.AlignCenter)
        mise_en_page.addWidget(description2)
        
        # Bouton pour revenir à la page principale
        bouton_retour2 = QPushButton("⬅ Retour à la page principale")
        bouton_retour2.clicked.connect(self.retourner_page_principale)
        mise_en_page.addWidget(bouton_retour2)
        
        mise_en_page.addStretch()
        
        # Ajouter la page 2 au stacked widget (index 2)
        self.stacked_widget.addWidget(self.page2)
    
    def creer_menu(self):
        """Crée la barre de menu"""
        barre_menu = self.fenetre.menuBar()
        
        # Menu Fichier
        menu_fichier = barre_menu.addMenu("&Fichier")
        action_quitter = QAction("&Quitter", self.fenetre)
        action_quitter.setShortcut("Ctrl+Q")
        action_quitter.triggered.connect(self.fenetre.close)
        menu_fichier.addAction(action_quitter)
        
        # Menu Fenetre1 (avec sous-menu)
        menu_fen1 = barre_menu.addMenu("&Fenetre1")
        action_ouvrir_page1 = QAction("&Ouvrir la page 1", self.fenetre)
        action_ouvrir_page1.triggered.connect(self.ouvrir_page1)
        menu_fen1.addAction(action_ouvrir_page1)
        
        # Menu Fenetre2 (direct, sans sous-menu)
        action_ouvrir_page2 = QAction("&Fenetre2", self.fenetre)
        action_ouvrir_page2.triggered.connect(self.ouvrir_page2)
        barre_menu.addAction(action_ouvrir_page2)
        
        # Menu Aide
        menu_aide = barre_menu.addMenu("&Aide")
        action_a_propos = QAction("&À propos", self.fenetre)
        action_a_propos.triggered.connect(self.afficher_a_propos)
        menu_aide.addAction(action_a_propos)
    
    def lancer(self):
        """Lance l'application"""
        self.creer_interface()
        self.fenetre.show()


# ========== PROGRAMME PRINCIPAL ==========
if __name__ == "__main__":
    # Vérifier s'il existe déjà une instance de QApplication
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    # Créer une instance de l'interface
    interface = UI()
    
    # Lancer l'application
    interface.lancer()
    
    sys.exit(app.exec_())