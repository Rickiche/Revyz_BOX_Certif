// ============================================
// ETAT DU JEU
// ============================================
const game = {
    total: 21,
    joueurActuel: 'joueur', // 'joueur' ou 'ordinateur'
    estTermine: false,
    victoires: 0,
    defaites: 0,
    dernierCoup: null,
    boutonSelectionne: 1 // 1, 2 ou 3
};

// ============================================
// REFERENCES DOM
// ============================================
const elements = {
    pointsNumber: document.getElementById('pointsNumber'),
    progressBar: document.getElementById('progressBar'),
    message: document.getElementById('message'),
    tourIndicator: document.getElementById('tourIndicator'),
    victoires: document.getElementById('victoires'),
    defaites: document.getElementById('defaites'),
    btn1: document.getElementById('btn1'),
    btn2: document.getElementById('btn2'),
    btn3: document.getElementById('btn3'),
    rulesPopup: document.getElementById('rulesPopup'),
    gameContainer: document.getElementById('gameContainer')
};

const boutons = [elements.btn1, elements.btn2, elements.btn3];

// ============================================
// FONCTIONS D'AFFICHAGE
// ============================================

/**
 * Met a jour l'affichage du total et de la barre de progression
 */
function mettreAJourAffichage() {
    // Total
    elements.pointsNumber.textContent = game.total;

    // Barre de progression
    const progression = (21 - game.total) / 21 * 100;
    let couleur;
    if (game.total > 14) couleur = '#27ae60';
    else if (game.total > 7) couleur = '#f1c40f';
    else couleur = '#e74c3c';

    elements.progressBar.style.width = (100 - progression) + '%';
    elements.progressBar.style.backgroundColor = couleur;

    // Effet danger si peu de points
    if (game.total <= 3) {
        elements.pointsNumber.classList.add('points-danger');
    } else {
        elements.pointsNumber.classList.remove('points-danger');
    }

    // Statistiques
    elements.victoires.textContent = 'Victoires : ' + game.victoires;
    elements.defaites.textContent = 'Defaites : ' + game.defaites;
}

/**
 * Met a jour l'indicateur de tour et le message
 */
function mettreAJourStatut() {
    const indicator = elements.tourIndicator;
    const message = elements.message;

    if (game.estTermine) {
        indicator.className = 'tour-indicator tour-termine';
        indicator.textContent = 'Partie terminee';
    } else if (game.joueurActuel === 'joueur') {
        indicator.className = 'tour-indicator tour-joueur';
        indicator.textContent = 'Ton tour ! (selectionne un bouton)';
        message.textContent = 'Choisis 1, 2 ou 3 points avec les fleches, puis valide avec Espace';
    } else {
        indicator.className = 'tour-indicator tour-ordinateur';
        indicator.textContent = 'Ordinateur reflechit...';
        message.textContent = "L'ordinateur joue...";
    }

    // Desactiver/activer les boutons
    const desactiver = game.estTermine || game.joueurActuel !== 'joueur';
    boutons.forEach(btn => {
        btn.disabled = desactiver;
    });

    // Si les boutons sont desactives, enlever la selection
    if (desactiver) {
        boutons.forEach(btn => btn.classList.remove('selected'));
    } else {
        // Sinon, selectionner le bouton actuel
        selectionnerBouton(game.boutonSelectionne);
    }
}

/**
 * Selectionne visuellement un bouton
 * @param {number} valeur - 1, 2 ou 3
 */
function selectionnerBouton(valeur) {
    // Enlever la selection de tous les boutons
    boutons.forEach(btn => btn.classList.remove('selected'));

    // Selectionner le bon bouton
    const btn = document.querySelector('.game-btn[data-value="' + valeur + '"]');
    if (btn && !btn.disabled) {
        btn.classList.add('selected');
    }
}

// ============================================
// LOGIQUE DU JEU
// ============================================

/**
 * Joue un coup pour le joueur
 * @param {number} retrait - 1, 2 ou 3
 */
function jouerCoupJoueur(retrait) {
    if (game.estTermine || game.joueurActuel !== 'joueur') {
        return;
    }

    if (retrait > game.total) {
        elements.message.textContent = 'Il ne reste que ' + game.total + ' points !';
        return;
    }

    // Retirer les points
    game.total -= retrait;
    game.dernierCoup = retrait;

    // Verifier la defaite
    if (game.total === 0) {
        game.estTermine = true;
        game.defaites++;
        elements.message.textContent = 'Tu as pris le dernier point... TU PERDS !';
        mettreAJourAffichage();
        mettreAJourStatut();
        return;
    }

    // Passer a l'ordinateur
    game.joueurActuel = 'ordinateur';
    elements.message.textContent = 'Tu as retire ' + retrait + ' point' + (retrait > 1 ? 's' : '');
    mettreAJourAffichage();
    mettreAJourStatut();

    // Jouer le coup de l'ordinateur apres un court delai
    setTimeout(jouerCoupOrdinateur, 800);
}

/**
 * Joue le coup de l'ordinateur (strategie)
 */
function jouerCoupOrdinateur() {
    if (game.estTermine || game.joueurActuel !== 'ordinateur') {
        return;
    }

    // Strategie : laisser un multiple de 4
    const reste = game.total % 4;
    let retrait;
    if (reste === 0) {
        retrait = Math.floor(Math.random() * Math.min(3, game.total)) + 1;
    } else {
        retrait = Math.min(reste, game.total);
    }

    game.total -= retrait;
    game.dernierCoup = retrait;

    // Verifier la victoire
    if (game.total === 0) {
        game.estTermine = true;
        game.victoires++;
        elements.message.textContent = "L'ordinateur a pris le dernier point... TU GAGNES !";
        mettreAJourAffichage();
        mettreAJourStatut();
        return;
    }

    // Passer au joueur
    game.joueurActuel = 'joueur';
    elements.message.textContent = "L'ordinateur a retire " + retrait + ' point' + (retrait > 1 ? 's' : '') +
        '. A toi de jouer !';
    mettreAJourAffichage();
    mettreAJourStatut();
}

/**
 * Valide le choix du joueur (appele par Espace ou Entree)
 */
function validerChoix() {
    if (game.estTermine || game.joueurActuel !== 'joueur') {
        return;
    }
    jouerCoupJoueur(game.boutonSelectionne);
}

/**
 * Nouvelle partie
 */
function nouvellePartie() {
    game.total = 21;
    game.joueurActuel = 'joueur';
    game.estTermine = false;
    game.dernierCoup = null;
    game.boutonSelectionne = 1;

    elements.message.textContent = 'Nouvelle partie ! A toi de jouer !';
    mettreAJourAffichage();
    mettreAJourStatut();
    selectionnerBouton(1);
}

// ============================================
// GESTION DU CLAVIER
// ============================================

document.addEventListener('keydown', function(event) {
    // Si la popup est ouverte, on bloque les touches
    if (elements.rulesPopup.classList.contains('active')) {
        if (event.key === 'Escape') {
            fermerRegles();
        }
        return;
    }

    // Navigation entre les boutons
    if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(event.key)) {
        event.preventDefault();

        if (game.estTermine || game.joueurActuel !== 'joueur') {
            return;
        }

        let nouveau = game.boutonSelectionne;

        if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
            nouveau = Math.max(1, game.boutonSelectionne - 1);
        } else if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
            nouveau = Math.min(3, game.boutonSelectionne + 1);
        }

        if (nouveau !== game.boutonSelectionne) {
            game.boutonSelectionne = nouveau;
            selectionnerBouton(nouveau);
            // Effet sonore visuel
            const btn = document.querySelector('.game-btn[data-value="' + nouveau + '"]');
            if (btn) {
                btn.style.transform = 'scale(0.95)';
                setTimeout(() => { btn.style.transform = ''; }, 150);
            }
        }
    }

    // Valider avec Entree
    if (event.key === 'Enter') {
        event.preventDefault();
        validerChoix();
    }

    // Raccourci : R pour reinitialiser
    if (event.key === 'r' || event.key === 'R') {
        nouvellePartie();
    }
});

// ============================================
// GESTION DES CLICS SOURIS
// ============================================

// Clic sur un bouton : le selectionne et valide
boutons.forEach(btn => {
    btn.addEventListener('click', function() {
        if (this.disabled) return;
        const valeur = parseInt(this.dataset.value);
        game.boutonSelectionne = valeur;
        selectionnerBouton(valeur);
        validerChoix();
    });
});

// ============================================
// POPUP REGLES
// ============================================

/**
 * Affiche la popup des regles
 */
function afficherRegles() {
    elements.rulesPopup.classList.add('active');
}

/**
 * Ferme la popup des regles
 */
function fermerRegles() {
    elements.rulesPopup.classList.remove('active');
}

// Fermer la popup en cliquant a l'exterieur
elements.rulesPopup.addEventListener('click', function(event) {
    if (event.target === this) {
        fermerRegles();
    }
});

// ============================================
// INITIALISATION
// ============================================

// Demarrer le jeu
nouvellePartie();

// Focus sur la page pour capter les evenements clavier
document.body.focus();

// Afficher les controles dans la console
console.log('=== JEU DU 21 ===');
console.log('Controles:');
console.log('  ← → ↑ ↓ : naviguer entre les boutons');
console.log('  Espace / Entree : valider le choix');
console.log('  R : nouvelle partie');
console.log('=================');