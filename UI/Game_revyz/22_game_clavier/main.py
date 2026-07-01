import sys
from PyQt5.QtWidgets import QApplication
from window import MainWindow


def main():
    """Fonction principale"""
    app = QApplication(sys.argv)
    
    # Style global
    app.setStyle('Fusion')
    
    # Création et affichage de la fenêtre
    window = MainWindow()
    window.show()
    
    # Exécution de l'application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()