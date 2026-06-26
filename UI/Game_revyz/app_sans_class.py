import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton, QStatusBar,
                             QMenuBar, QAction, QMessageBox)
from PyQt5.QtCore import Qt

# Variables globales (déclarées au niveau du module)
champ_nom = None
etiquette_resultat = None
barre_etat = None
fenetre = None

def on_click_saluer():
    """Fonction appelée quand on clique sur 'Dire bonjour !'"""
    global champ_nom, etiquette_resultat, barre_etat   # Ces variables sont modifiées

    nom = champ_nom.text().strip()
    if not nom:
        etiquette_resultat.setText("Veuillez entrer un nom !")
        barre_etat.showMessage("Nom vide", 2000)
    else:
        etiquette_resultat.setText(f"Bonjour, {nom} ! 👋")
        barre_etat.showMessage(f"A salué {nom}", 2000)

def afficher_a_propos():
    """Fonction appelée quand on clique sur 'À propos'"""
    # On lit fenetre (pas de modification) → pas besoin de global
    QMessageBox.about(
        fenetre,
        "À propos de Mon App",
        "Ceci est une application d'exemple PyQt5.\n\n"
        "Elle démontre une fenêtre principale avec des menus, "
        "une saisie, des boutons et des messages d'état."
    )

if __name__ == "__main__":
    # Pas de déclaration 'global' ici : on est au niveau du module,
    # les variables sont déjà globales et on peut leur assigner directement.

    # Vérifier s'il existe déjà une instance de QApplication
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    # --- Créer la fenêtre principale ---
    fenetre = QMainWindow()
    fenetre.setWindowTitle("Mon App - Améliorée (sans classe)")
    fenetre.resize(500, 250)
    fenetre.move(300, 50)

    # --- Créer le widget central et la mise en page ---
    widget_central = QWidget()
    fenetre.setCentralWidget(widget_central)
    mise_en_page = QVBoxLayout()
    widget_central.setLayout(mise_en_page)

    # --- Ajouter les widgets ---
    etiquette = QLabel("Entrez votre nom :")
    mise_en_page.addWidget(etiquette)

    champ_nom = QLineEdit()
    champ_nom.setPlaceholderText("Votre nom ici")
    mise_en_page.addWidget(champ_nom)

    bouton_saluer = QPushButton("Dire bonjour !")
    bouton_saluer.clicked.connect(on_click_saluer)
    mise_en_page.addWidget(bouton_saluer)

    etiquette_resultat = QLabel("")
    etiquette_resultat.setAlignment(Qt.AlignCenter)
    mise_en_page.addWidget(etiquette_resultat)

    mise_en_page.addStretch()  # espaceur

    # --- Configurer la barre d'état ---
    barre_etat = QStatusBar()
    fenetre.setStatusBar(barre_etat)
    barre_etat.showMessage("Prêt")

    # --- Configurer la barre de menu ---
    barre_menu = fenetre.menuBar()

    menu_fichier = barre_menu.addMenu("&Fichier")
    action_quitter = QAction("&Quitter", fenetre)
    action_quitter.setShortcut("Ctrl+Q")
    action_quitter.triggered.connect(fenetre.close)
    menu_fichier.addAction(action_quitter)

    menu_aide = barre_menu.addMenu("&Aide")
    action_a_propos = QAction("&À propos", fenetre)
    action_a_propos.triggered.connect(afficher_a_propos)
    menu_aide.addAction(action_a_propos)

    # --- Afficher et lancer ---
    fenetre.show()
    sys.exit(app.exec_())