from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QProgressBar,
    QMessageBox, QDialog, QGridLayout
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPalette, QColor

from game import Game
from player import Player


class RulesDialog(QDialog):
    """Fenêtre modale pour afficher les règles"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Règles du jeu")
        self.setFixedSize(500, 550)
        self.setModal(True)
        
        # Layout principal
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Titre
        titre = QLabel("RÈGLES DU JEU DU 21")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin: 10px;")
        layout.addWidget(titre)
        
        # Contenu
        regles = """
        <b>BUT DU JEU</b><br>
        Le jeu commence avec <b>21 points</b>.<br><br>
        
        <b>DÉROULEMENT</b><br>
        • À ton tour, sélectionne un bouton (1, 2 ou 3) avec les <b>flèches du clavier</b>.<br>
        • Appuie sur <b>Entrée</b> pour valider ton choix.<br>
        • L'ordinateur joue automatiquement après toi.<br>
        • Celui qui prend le <b>DERNIER point</b> perd la partie !<br><br>
        
        <b>CONTROLES</b><br>
        • <b>← → ↑ ↓</b> : naviguer entre les boutons<br>
        • <b>Entrée</b> : valider le choix<br>
        • <b>R</b> : nouvelle partie (raccourci)<br><br>
        
        <b>ASTUCE</b><br>
        Pour gagner, laisse toujours un <b>multiple de 4</b> à ton adversaire !<br>
        <span style="color: #e67e22; font-size: 20px; font-weight: bold;">
        (4, 8, 12, 16 ou 20)
        </span>
        """
        
        content = QLabel(regles)
        content.setAlignment(Qt.AlignLeft)
        content.setWordWrap(True)
        content.setStyleSheet("font-size: 16px; line-height: 1.6; padding: 10px;")
        layout.addWidget(content)
        
        # Bouton fermer
        btn_fermer = QPushButton("Fermer")
        btn_fermer.clicked.connect(self.accept)
        btn_fermer.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 30px;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        layout.addWidget(btn_fermer, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)
    
    def keyPressEvent(self, event):
        """Gère les touches dans la popup"""
        if event.key() == Qt.Key_Escape:
            self.accept()
        super().keyPressEvent(event)


class MainWindow(QMainWindow):
    """Fenêtre principale du jeu"""
    
    def __init__(self):
        super().__init__()
        
        # Initialisation du jeu et du joueur
        self.game = Game()
        self.player = Player()
        
        # Variables pour la sélection
        self.bouton_selectionne = 1
        
        # Timer pour le délai de l'ordinateur
        self.timer_ordinateur = QTimer()
        self.timer_ordinateur.setSingleShot(True)
        self.timer_ordinateur.timeout.connect(self.jouer_coup_ordinateur)
        
        # Configuration de la fenêtre
        self.setWindowTitle("Jeu du 21")
        self.setFixedSize(600, 750)
        self.setStyleSheet("background-color: #f0f0f0;")
        
        # Création de l'interface
        self.init_ui()
        
        # Démarrer le jeu
        self.nouvelle_partie()
    
    def init_ui(self):
        """Crée tous les widgets de l'interface"""
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # --- Titre ---
        titre = QLabel("JEU DU 21")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("font-size: 36px; font-weight: bold; color: #2c3e50;")
        main_layout.addWidget(titre)
        
        # Sous-titre
        sous_titre = QLabel("Celui qui prend le dernier point perd")
        sous_titre.setAlignment(Qt.AlignCenter)
        sous_titre.setStyleSheet("font-size: 14px; color: #7f8c8d; margin-bottom: 10px;")
        main_layout.addWidget(sous_titre)
        
        # --- Indicateur de tour ---
        self.tour_indicator = QLabel("Chargement...")
        self.tour_indicator.setAlignment(Qt.AlignCenter)
        self.tour_indicator.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                border-radius: 10px;
                background-color: #d5f5e3;
                color: #27ae60;
            }
        """)
        main_layout.addWidget(self.tour_indicator)
        
        # --- Points ---
        points_layout = QVBoxLayout()
        points_layout.setSpacing(5)
        
        label_points = QLabel("Points restants :")
        label_points.setAlignment(Qt.AlignCenter)
        label_points.setStyleSheet("font-size: 18px; color: #34495e;")
        points_layout.addWidget(label_points)
        
        self.points_number = QLabel("21")
        self.points_number.setAlignment(Qt.AlignCenter)
        self.points_number.setStyleSheet("""
            QLabel {
                font-size: 80px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        points_layout.addWidget(self.points_number)
        
        main_layout.addLayout(points_layout)
        
        # --- Barre de progression ---
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                height: 25px;
                border-radius: 15px;
                background-color: #ecf0f1;
            }
            QProgressBar::chunk {
                border-radius: 15px;
                background-color: #27ae60;
            }
        """)
        main_layout.addWidget(self.progress_bar)
        
        # --- Message ---
        self.message_label = QLabel("A toi de jouer !")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #2c3e50;
                padding: 10px;
                min-height: 60px;
            }
        """)
        main_layout.addWidget(self.message_label)
        
        # --- Boutons de jeu (1, 2, 3) ---
        boutons_layout = QHBoxLayout()
        boutons_layout.setSpacing(20)
        
        self.btn_1 = self.creer_bouton_jeu("1", "1 point", "#3498db")
        self.btn_2 = self.creer_bouton_jeu("2", "2 points", "#2ecc71")
        self.btn_3 = self.creer_bouton_jeu("3", "3 points", "#e67e22")
        
        boutons_layout.addWidget(self.btn_1)
        boutons_layout.addWidget(self.btn_2)
        boutons_layout.addWidget(self.btn_3)
        
        main_layout.addLayout(boutons_layout)
        
        # --- Aide clavier ---
        aide_label = QLabel(
            "<b>← → ↑ ↓</b> pour naviguer &nbsp;&nbsp;|&nbsp;&nbsp; <b>Entrée</b> pour valider"
        )
        aide_label.setAlignment(Qt.AlignCenter)
        aide_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #7f8c8d;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 10px;
            }
        """)
        main_layout.addWidget(aide_label)
        
        # --- Boutons action ---
        action_layout = QHBoxLayout()
        action_layout.setSpacing(15)
        
        btn_rejouer = QPushButton("Nouvelle partie")
        btn_rejouer.clicked.connect(self.nouvelle_partie)
        btn_rejouer.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px 25px;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """)
        action_layout.addWidget(btn_rejouer)
        
        btn_regles = QPushButton("Règles")
        btn_regles.clicked.connect(self.afficher_regles)
        btn_regles.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px 25px;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        action_layout.addWidget(btn_regles)
        
        main_layout.addLayout(action_layout)
        
        # --- Statistiques ---
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(30)
        
        self.victoires_label = QLabel("Victoires : 0")
        self.victoires_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #27ae60;")
        stats_layout.addWidget(self.victoires_label, alignment=Qt.AlignCenter)
        
        self.defaites_label = QLabel("Défaites : 0")
        self.defaites_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #e74c3c;")
        stats_layout.addWidget(self.defaites_label, alignment=Qt.AlignCenter)
        
        main_layout.addLayout(stats_layout)
        
        central_widget.setLayout(main_layout)
    
    def creer_bouton_jeu(self, texte, sous_texte, couleur):
        """
        Crée un bouton de jeu
        Paramètres : texte (str), sous_texte (str), couleur (str)
        Retourne : QPushButton
        """
        bouton = QPushButton()
        bouton.setFixedSize(100, 100)
        bouton.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                border: 4px solid #bdc3c7;
                border-radius: 15px;
                font-size: 32px;
                font-weight: bold;
                color: #2c3e50;
            }}
            QPushButton:hover:!disabled {{
                transform: translateY(-3px);
                border-color: {couleur};
            }}
            QPushButton:disabled {{
                opacity: 0.4;
            }}
            QPushButton.selected {{
                border-color: {couleur};
                box-shadow: 0 0 0 4px rgba({self.hex_to_rgb(couleur)}, 0.3);
                transform: scale(1.05);
                background-color: {self.get_light_color(couleur)};
            }}
        """)
        
        # Layout interne du bouton
        layout = QVBoxLayout()
        layout.setSpacing(2)
        
        label = QLabel(texte)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 32px; font-weight: bold; color: #2c3e50; background: transparent;")
        layout.addWidget(label)
        
        sub_label = QLabel(sous_texte)
        sub_label.setAlignment(Qt.AlignCenter)
        sub_label.setStyleSheet("font-size: 12px; color: #7f8c8d; background: transparent;")
        layout.addWidget(sub_label)
        
        bouton.setLayout(layout)
        
        # Stocker la valeur
        bouton.setProperty("valeur", int(texte))
        
        # Connecter le clic
        bouton.clicked.connect(lambda: self.clic_bouton(int(texte)))
        
        return bouton
    
    def hex_to_rgb(self, hex_color):
        """
        Convertit une couleur hexadécimale en RGB
        Paramètre : hex_color (str) - "#3498db"
        Retourne : str - "52, 152, 219"
        """
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"{r}, {g}, {b}"
    
    def get_light_color(self, hex_color):
        """
        Retourne une version claire d'une couleur
        Paramètre : hex_color (str) - "#3498db"
        Retourne : str - "#ebf5fb"
        """
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # Mélanger avec du blanc (ajouter 180)
        r = min(255, r + 180)
        g = min(255, g + 180)
        b = min(255, b + 180)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def mettre_a_jour_affichage(self):
        """Met à jour l'affichage complet"""
        # Points
        self.points_number.setText(str(self.game.total))
        
        # Barre de progression
        progression = (21 - self.game.total) / 21 * 100
        self.progress_bar.setValue(int(progression))
        
        # Couleur de la barre
        if self.game.total > 14:
            couleur = "#27ae60"
        elif self.game.total > 7:
            couleur = "#f1c40f"
        else:
            couleur = "#e74c3c"
        
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                height: 25px;
                border-radius: 15px;
                background-color: #ecf0f1;
            }}
            QProgressBar::chunk {{
                border-radius: 15px;
                background-color: {couleur};
            }}
        """)
        
        # Effet danger si peu de points
        if self.game.total <= 3:
            self.points_number.setStyleSheet("""
                QLabel {
                    font-size: 80px;
                    font-weight: bold;
                    color: #e74c3c;
                }
            """)
        else:
            self.points_number.setStyleSheet("""
                QLabel {
                    font-size: 80px;
                    font-weight: bold;
                    color: #2c3e50;
                }
            """)
        
        # Statistiques
        self.victoires_label.setText(f"Victoires : {self.player.get_victoires()}")
        self.defaites_label.setText(f"Défaites : {self.player.get_defaites()}")
        
        # Message
        self.message_label.setText(self.game.message)
    
    def mettre_a_jour_statut(self):
        """Met à jour l'indicateur de tour"""
        if self.game.est_termine:
            self.tour_indicator.setText("Partie terminée")
            self.tour_indicator.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 10px;
                    background-color: #f2f3f4;
                    color: #7f8c8d;
                }
            """)
            self.desactiver_boutons()
        elif self.game.joueur_actuel == 'joueur':
            self.tour_indicator.setText("Ton tour ! (sélectionne un bouton)")
            self.tour_indicator.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 10px;
                    background-color: #d5f5e3;
                    color: #27ae60;
                }
            """)
            self.activer_boutons()
        else:
            self.tour_indicator.setText("Ordinateur réfléchit...")
            self.tour_indicator.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 10px;
                    background-color: #fdebd0;
                    color: #e67e22;
                }
            """)
            self.desactiver_boutons()
        
        self.mettre_a_jour_affichage()
    
    def activer_boutons(self):
        """Active les boutons de jeu"""
        self.btn_1.setEnabled(True)
        self.btn_2.setEnabled(True)
        self.btn_3.setEnabled(True)
        self.selectionner_bouton(self.bouton_selectionne)
    
    def desactiver_boutons(self):
        """Désactive les boutons de jeu"""
        self.btn_1.setEnabled(False)
        self.btn_2.setEnabled(False)
        self.btn_3.setEnabled(False)
        self.btn_1.setProperty("selected", False)
        self.btn_2.setProperty("selected", False)
        self.btn_3.setProperty("selected", False)
        self.btn_1.setStyleSheet(self.btn_1.styleSheet())
        self.btn_2.setStyleSheet(self.btn_2.styleSheet())
        self.btn_3.setStyleSheet(self.btn_3.styleSheet())
    
    def selectionner_bouton(self, valeur):
        """Sélectionne visuellement un bouton"""
        self.bouton_selectionne = valeur
        
        # Enlever la sélection de tous
        for btn in [self.btn_1, self.btn_2, self.btn_3]:
            btn.setProperty("selected", False)
            btn.setStyleSheet(btn.styleSheet())
        
        # Sélectionner le bon bouton
        if valeur == 1:
            self.btn_1.setProperty("selected", True)
            self.btn_1.setStyleSheet(self.btn_1.styleSheet())
        elif valeur == 2:
            self.btn_2.setProperty("selected", True)
            self.btn_2.setStyleSheet(self.btn_2.styleSheet())
        elif valeur == 3:
            self.btn_3.setProperty("selected", True)
            self.btn_3.setStyleSheet(self.btn_3.styleSheet())
    
    def clic_bouton(self, valeur):
        """Gère le clic sur un bouton"""
        self.bouton_selectionne = valeur
        self.selectionner_bouton(valeur)
        self.valider_choix()
    
    def valider_choix(self):
        """Valide le choix du joueur"""
        if self.game.est_termine or self.game.joueur_actuel != 'joueur':
            return
        
        self.jouer_coup_joueur(self.bouton_selectionne)
    
    def jouer_coup_joueur(self, retrait):
        """Joue le coup du joueur"""
        resultat = self.game.jouer_coup_joueur(retrait)
        
        if 'erreur' in resultat:
            self.message_label.setText(resultat['erreur'])
            return
        
        # Mettre à jour l'affichage
        self.mettre_a_jour_statut()
        
        # Vérifier si le joueur a perdu
        if resultat.get('termine', False):
            self.player.ajouter_defaite()
            self.mettre_a_jour_affichage()
            return
        
        # Lancer le tour de l'ordinateur après un délai
        self.timer_ordinateur.start(800)
    
    def jouer_coup_ordinateur(self):
        """Joue le coup de l'ordinateur"""
        resultat = self.game.jouer_coup_ordinateur()
        
        if 'erreur' in resultat:
            self.message_label.setText(resultat['erreur'])
            return
        
        # Mettre à jour l'affichage
        self.mettre_a_jour_statut()
        
        # Vérifier si l'ordinateur a perdu
        if resultat.get('termine', False):
            self.player.ajouter_victoire()
            self.mettre_a_jour_affichage()
    
    def nouvelle_partie(self):
        """Réinitialise la partie"""
        self.game.reinitialiser()
        self.bouton_selectionne = 1
        self.mettre_a_jour_statut()
        self.activer_boutons()
        self.selectionner_bouton(1)
        self.timer_ordinateur.stop()
    
    def afficher_regles(self):
        """Affiche les règles dans une fenêtre modale"""
        dialog = RulesDialog(self)
        dialog.exec_()
    
    def keyPressEvent(self, event):
        """Gère les événements clavier"""
        
        # Vérifier si une popup est ouverte (RulesDialog)
        # On utilise findChild pour détecter la popup
        if self.findChild(RulesDialog) is not None:
            # Si la popup est ouverte, on bloque toutes les touches
            # Sauf Échap qui est géré par la popup elle-même
            if event.key() == Qt.Key_Escape:
                # Fermer la popup (déjà géré par RulesDialog)
                pass
            return  # On bloque tout le reste
        
        # Navigation entre les boutons (flèches)
        if event.key() in (Qt.Key_Left, Qt.Key_Up):
            if not self.game.est_termine and self.game.joueur_actuel == 'joueur':
                nouveau = max(1, self.bouton_selectionne - 1)
                if nouveau != self.bouton_selectionne:
                    self.bouton_selectionne = nouveau
                    self.selectionner_bouton(nouveau)
            event.accept()
            return
        
        elif event.key() in (Qt.Key_Right, Qt.Key_Down):
            if not self.game.est_termine and self.game.joueur_actuel == 'joueur':
                nouveau = min(3, self.bouton_selectionne + 1)
                if nouveau != self.bouton_selectionne:
                    self.bouton_selectionne = nouveau
                    self.selectionner_bouton(nouveau)
            event.accept()
            return
        
        # Validation avec Entrée
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.valider_choix()
            event.accept()
            return
        
        # R pour nouvelle partie (raccourci)
        elif event.key() == Qt.Key_R:
            self.nouvelle_partie()
            event.accept()
            return
        
        super().keyPressEvent(event)