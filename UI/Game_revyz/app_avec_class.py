import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton, QStatusBar,
                             QMenuBar, QAction, QMessageBox)
from PyQt5.QtCore import Qt

class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mon App - Améliorée")
        self.resize(500, 250)
        self.move(300, 50)

        # Créer le widget central et la mise en page
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        mise_en_page = QVBoxLayout()
        widget_central.setLayout(mise_en_page)

        # Ajouter les widgets
        self.etiquette = QLabel("Entrez votre nom :")
        mise_en_page.addWidget(self.etiquette)

        self.champ_nom = QLineEdit()
        self.champ_nom.setPlaceholderText("Votre nom ici")
        mise_en_page.addWidget(self.champ_nom)

        self.bouton_saluer = QPushButton("Dire bonjour !")
        self.bouton_saluer.clicked.connect(self.on_click_saluer)
        mise_en_page.addWidget(self.bouton_saluer)

        self.etiquette_resultat = QLabel("")
        self.etiquette_resultat.setAlignment(Qt.AlignCenter)
        mise_en_page.addWidget(self.etiquette_resultat)

        # Ajouter un espaceur pour pousser les widgets vers le haut (optionnel)
        mise_en_page.addStretch()

        # Configurer la barre d'état
        self.barre_etat = QStatusBar()
        self.setStatusBar(self.barre_etat)
        self.barre_etat.showMessage("Prêt")

        # Configurer la barre de menu
        self.creer_barre_menu()

    def creer_barre_menu(self):
        barre_menu = self.menuBar()

        # Menu Fichier
        menu_fichier = barre_menu.addMenu("&Fichier")
        action_quitter = QAction("&Quitter", self)
        action_quitter.setShortcut("Ctrl+Q")
        action_quitter.triggered.connect(self.close)
        menu_fichier.addAction(action_quitter)

        # Menu Aide
        menu_aide = barre_menu.addMenu("&Aide")
        action_a_propos = QAction("&À propos", self)
        action_a_propos.triggered.connect(self.afficher_a_propos)
        menu_aide.addAction(action_a_propos)

    def on_click_saluer(self):
        nom = self.champ_nom.text().strip()
        if not nom:
            self.etiquette_resultat.setText("Veuillez entrer un nom !")
            self.barre_etat.showMessage("Nom vide", 2000)
        else:
            self.etiquette_resultat.setText(f"Bonjour, {nom} ! 👋")
            self.barre_etat.showMessage(f"A salué {nom}", 2000)

    def afficher_a_propos(self):
        QMessageBox.about(
            self,
            "À propos de Mon App",
            "Ceci est une application d'exemple PyQt5.\n\n"
            "Elle démontre une fenêtre principale avec des menus, "
            "une saisie, des boutons et des messages d'état."
        )

if __name__ == "__main__":
    # Vérifier s'il existe déjà une instance de QApplication
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    fenetre = FenetrePrincipale()
    fenetre.show()

    sys.exit(app.exec_())