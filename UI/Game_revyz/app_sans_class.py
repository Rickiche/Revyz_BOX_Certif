import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton, QStatusBar,
                             QMenuBar, QAction, QMessageBox, QStackedWidget)
from PyQt5.QtCore import Qt

# Variables globales
champ_nom = None
etiquette_resultat = None
barre_etat = None
fenetre = None
stacked_widget = None  # Conteneur de pages
page_principale = None           # Page principale (index 0)
page1 = None           # Page 1 (accessible via Fenetre1) (index 1)
page2 = None           # Page 2 (accessible via Fen2) (index 2)

def on_click_saluer():
    """Fonction appelée quand on clique sur 'Dire bonjour !'"""
    global champ_nom, etiquette_resultat, barre_etat

    nom = champ_nom.text().strip()
    if not nom:
        etiquette_resultat.setText("Veuillez entrer un nom !")
        barre_etat.showMessage("Nom vide", 2000)
    else:
        etiquette_resultat.setText(f"Bonjour, {nom} ! 👋")
        barre_etat.showMessage(f"A salué {nom}", 2000)

def afficher_a_propos():
    """Fonction appelée quand on clique sur 'À propos'"""
    QMessageBox.about(
        fenetre,
        "À propos de Mon App",
        "Ceci est une application d'exemple PyQt5.\n\n"
        "Elle démontre une fenêtre principale avec des menus, "
        "une saisie, des boutons et des messages d'état."
    )

def ouvrir_page1():
    """Ouvre la page 1 (via Fenetre1)"""
    global stacked_widget
    stacked_widget.setCurrentIndex(1)  # Index 1 = page1
    barre_etat.showMessage("Page 1 ouverte", 2000)

def ouvrir_page2():
    """Ouvre la page 2 (via Fen2)"""
    global stacked_widget
    # On appelle ecrire_message avec "Page 2 ouverte" comme argument
    message = ecrire_message("Page 2 ouverte")
    stacked_widget.setCurrentIndex(2)  # Index 2 = page2
    barre_etat.showMessage(message, 2000)  # On affiche le message retourné

def retourner_page_principale():
    """Retourne à la page principale"""
    global stacked_widget
    stacked_widget.setCurrentIndex(0)  # Index 0 = page_principale
    barre_etat.showMessage("Retour à la page principale", 2000)

def ecrire_message(msg):
    """Fonction qui traite et formate un message"""
    if msg == "":
        msg = "Message vide"
        # Exemple de traitement supplémentaire
        msg = msg + " OK"
    else:
        # On peut ajouter un traitement personnalisé ici
        msg = f"📝 {msg}"
    return msg

if __name__ == "__main__":
    # Vérifier s'il existe déjà une instance de QApplication
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    # --- Créer la fenêtre principale ---
    fenetre = QMainWindow()
    fenetre.setWindowTitle("Mon App - Avec plusieurs pages")
    fenetre.resize(500, 250)
    fenetre.move(300, 50)

    # --- Créer le widget central QStackedWidget pour gérer les pages ---
    widget_central = QWidget()
    fenetre.setCentralWidget(widget_central)
    
    # Layout principal qui contiendra le stacked widget
    layout_principal = QVBoxLayout()
    widget_central.setLayout(layout_principal)
    
    # Créer le QStackedWidget
    stacked_widget = QStackedWidget()
    layout_principal.addWidget(stacked_widget)

    # ========== PAGE PRINCIPALE : Page principale (contenu original) ==========
    page_principale = QWidget()
    mise_en_page_principale = QVBoxLayout()
    page_principale.setLayout(mise_en_page_principale)

    etiquette = QLabel("Entrez votre nom :")
    mise_en_page_principale.addWidget(etiquette)

    champ_nom = QLineEdit()
    champ_nom.setPlaceholderText("Votre nom ici")
    mise_en_page_principale.addWidget(champ_nom)

    bouton_saluer = QPushButton("Dire bonjour !")
    bouton_saluer.clicked.connect(on_click_saluer)
    mise_en_page_principale.addWidget(bouton_saluer)

    etiquette_resultat = QLabel("")
    etiquette_resultat.setAlignment(Qt.AlignCenter)
    mise_en_page_principale.addWidget(etiquette_resultat)

    mise_en_page_principale.addStretch()  # espaceur
    
    # Ajouter la page principale au stacked widget (index 0)
    stacked_widget.addWidget(page_principale)

    # ========== PAGE 1 : Page accessible via Fenetre1 ==========
    page1 = QWidget()
    mise_en_page1 = QVBoxLayout()
    page1.setLayout(mise_en_page1)

    # Titre de la page
    titre_page1 = QLabel("✨ Bienvenue sur la Page 1 ✨")
    titre_page1.setAlignment(Qt.AlignCenter)
    titre_page1.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
    mise_en_page1.addWidget(titre_page1)

    # Description
    description1 = QLabel(
        "Ceci est la page 1 !\n\n"
        "Accessible via le menu 'Fenetre1'."
    )
    description1.setAlignment(Qt.AlignCenter)
    mise_en_page1.addWidget(description1)

    # Bouton pour revenir à la page principale
    bouton_retour1 = QPushButton("⬅ Retour à la page principale")
    bouton_retour1.clicked.connect(retourner_page_principale)
    mise_en_page1.addWidget(bouton_retour1)

    mise_en_page1.addStretch()
    
    # Ajouter la page 1 au stacked widget (index 1)
    stacked_widget.addWidget(page1)

    # ========== PAGE 2 : Page accessible via Fen2 ==========
    page2 = QWidget()
    mise_en_page2 = QVBoxLayout()
    page2.setLayout(mise_en_page2)

    # Titre de la page
    titre_page2 = QLabel("🚀 Bienvenue sur la Page 2 🚀")
    titre_page2.setAlignment(Qt.AlignCenter)
    titre_page2.setStyleSheet("font-size: 18px; font-weight: bold; color: #e74c3c;")
    mise_en_page2.addWidget(titre_page2)

    # Description
    description2 = QLabel(
        "Ceci est la page 2 !\n\n"
        "Accessible directement via le menu 'Fen2'."
    )
    description2.setAlignment(Qt.AlignCenter)
    mise_en_page2.addWidget(description2)

    # Bouton pour revenir à la page principale
    bouton_retour2 = QPushButton("⬅ Retour à la page principale")
    bouton_retour2.clicked.connect(retourner_page_principale)
    mise_en_page2.addWidget(bouton_retour2)

    mise_en_page2.addStretch()
    
    # Ajouter la page 2 au stacked widget (index 2)
    stacked_widget.addWidget(page2)

    # Afficher la page principale par défaut
    stacked_widget.setCurrentIndex(0)

    # --- Configurer la barre d'état ---
    barre_etat = QStatusBar()
    fenetre.setStatusBar(barre_etat)
    barre_etat.showMessage("Prêt")

    # --- Configurer la barre de menu ---
    barre_menu = fenetre.menuBar()

    # Menu Fichier
    menu_fichier = barre_menu.addMenu("&Fichier")
    action_quitter = QAction("&Quitter", fenetre)
    action_quitter.setShortcut("Ctrl+Q")
    action_quitter.triggered.connect(fenetre.close)
    menu_fichier.addAction(action_quitter)

    # Menu Fenetre1 (avec sous-menu)
    menu_fen1 = barre_menu.addMenu("&Fenetre1")
    action_ouvrir_page1 = QAction("&Ouvrir la page 1", fenetre)
    action_ouvrir_page1.triggered.connect(ouvrir_page1)
    menu_fen1.addAction(action_ouvrir_page1)

    # Menu Fen2 (direct, sans sous-menu)
    action_ouvrir_page2 = QAction("&Fen2", fenetre)
    action_ouvrir_page2.triggered.connect(ouvrir_page2)
    barre_menu.addAction(action_ouvrir_page2)

    # Menu Aide
    menu_aide = barre_menu.addMenu("&Aide")
    action_a_propos = QAction("&À propos", fenetre)
    action_a_propos.triggered.connect(afficher_a_propos)
    menu_aide.addAction(action_a_propos)

    # --- Afficher et lancer ---
    fenetre.show()
    sys.exit(app.exec_())