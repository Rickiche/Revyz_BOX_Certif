<?php
/**
 * JEU DU 21 - Version clavier (fleches)
 * ↑ = 1 point, ← = 2 points, → = 3 points
 * Celui qui prend le dernier point perd.
 */

// Demarrer la session
session_start();

// ============================================
// CLASSE GAME - Logique metier
// ============================================
class Game {
    private $total;
    private $joueurActuel;
    private $estTermine;
    private $message;
    private $victoires;
    private $defaites;
    private $dernierCoup;
    
    public function __construct() {
        $this->total = 21;
        $this->joueurActuel = 'joueur';
        $this->estTermine = false;
        $this->message = 'A ton tour ! Utilise les fleches : ↑(1) ←(2) →(3)';
        $this->victoires = 0;
        $this->defaites = 0;
        $this->dernierCoup = null;
    }
    
    // Getters
    public function getTotal() { return $this->total; }
    public function getJoueurActuel() { return $this->joueurActuel; }
    public function estTermine() { return $this->estTermine; }
    public function getMessage() { return $this->message; }
    public function getVictoires() { return $this->victoires; }
    public function getDefaites() { return $this->defaites; }
    public function getDernierCoup() { return $this->dernierCoup; }
    
    // Jouer un coup joueur
    public function jouerCoupJoueur($retrait) {
        // Verifications
        if ($this->estTermine) {
            return ['erreur' => 'Partie terminee !'];
        }
        if ($this->joueurActuel !== 'joueur') {
            return ['erreur' => 'Ce n\'est pas ton tour !'];
        }
        if ($retrait < 1 || $retrait > 3) {
            return ['erreur' => 'Choisis 1, 2 ou 3 !'];
        }
        if ($retrait > $this->total) {
            return ['erreur' => "Il reste {$this->total} points !"];
        }
        
        // Action
        $this->total -= $retrait;
        $this->dernierCoup = $retrait;
        $this->message = "Tu as retire {$retrait} point" . ($retrait > 1 ? 's' : '');
        
        // Verification
        if ($this->total == 0) {
            $this->estTermine = true;
            $this->defaites++;
            $this->message = "Tu as pris le dernier point... TU PERDS !";
            return ['succes' => true, 'termine' => true];
        }
        
        // Passage a l'ordinateur
        $this->joueurActuel = 'ordinateur';
        $this->message .= "\nL'ordinateur reflechit...";
        return ['succes' => true, 'termine' => false];
    }
    
    // Jouer coup ordinateur
    public function jouerCoupOrdinateur() {
        if ($this->estTermine) {
            return ['erreur' => 'Partie terminee !'];
        }
        if ($this->joueurActuel !== 'ordinateur') {
            return ['erreur' => 'Ce n\'est pas le tour de l\'ordinateur !'];
        }
        
        // Strategie : laisser un multiple de 4
        $reste = $this->total % 4;
        if ($reste == 0) {
            $retrait = rand(1, min(3, $this->total));
        } else {
            $retrait = min($reste, $this->total);
        }
        
        $this->total -= $retrait;
        $this->dernierCoup = $retrait;
        $this->message = "L'ordinateur a retire {$retrait} point" . ($retrait > 1 ? 's' : '');
        
        if ($this->total == 0) {
            $this->estTermine = true;
            $this->victoires++;
            $this->message = "L'ordinateur a pris le dernier point... TU GAGNES !";
            return ['succes' => true, 'termine' => true];
        }
        
        $this->joueurActuel = 'joueur';
        $this->message .= "\nA ton tour ! (↑=1, ←=2, →=3)";
        return ['succes' => true, 'termine' => false];
    }
    
    // Reinitialiser
    public function reinitialiser() {
        $this->total = 21;
        $this->joueurActuel = 'joueur';
        $this->estTermine = false;
        $this->message = 'Nouvelle partie ! A ton tour ! (↑=1, ←=2, →=3)';
        $this->dernierCoup = null;
    }
    
    // Sauvegarder en session
    public function sauvegarder() {
        $_SESSION['game'] = [
            'total' => $this->total,
            'joueurActuel' => $this->joueurActuel,
            'estTermine' => $this->estTermine,
            'message' => $this->message,
            'victoires' => $this->victoires,
            'defaites' => $this->defaites,
            'dernierCoup' => $this->dernierCoup
        ];
    }
    
    // Charger depuis session
    public static function charger() {
        if (isset($_SESSION['game']) && is_array($_SESSION['game'])) {
            $data = $_SESSION['game'];
            
            $game = new self();
            $game->total = isset($data['total']) ? $data['total'] : 21;
            $game->joueurActuel = isset($data['joueurActuel']) ? $data['joueurActuel'] : 'joueur';
            $game->estTermine = isset($data['estTermine']) ? $data['estTermine'] : false;
            $game->message = isset($data['message']) ? $data['message'] : 'A ton tour !';
            $game->victoires = isset($data['victoires']) ? $data['victoires'] : 0;
            $game->defaites = isset($data['defaites']) ? $data['defaites'] : 0;
            $game->dernierCoup = isset($data['dernierCoup']) ? $data['dernierCoup'] : null;
            
            return $game;
        }
        
        return new self();
    }
}

// ============================================
// TRAITEMENT DES ACTIONS
// ============================================

$game = Game::charger();
$action = isset($_POST['action']) ? $_POST['action'] : '';

// Nouvelle partie
if ($action === 'reinitialiser') {
    $game->reinitialiser();
    $game->sauvegarder();
    header('Location: ' . $_SERVER['PHP_SELF']);
    exit;
}

// Jouer un coup
if ($action === 'jouer' && isset($_POST['retrait'])) {
    $retrait = intval($_POST['retrait']);
    $resultat = $game->jouerCoupJoueur($retrait);
    $game->sauvegarder();
    
    // Tour de l'ordinateur
    if (!$game->estTermine() && $game->getJoueurActuel() === 'ordinateur') {
        $game->jouerCoupOrdinateur();
        $game->sauvegarder();
    }
    
    header('Location: ' . $_SERVER['PHP_SELF']);
    exit;
}

// ============================================
// AFFICHAGE
// ============================================

$total = $game->getTotal();
$joueurActuel = $game->getJoueurActuel();
$estTermine = $game->estTermine();
$message = $game->getMessage();
$victoires = $game->getVictoires();
$defaites = $game->getDefaites();
$dernierCoup = $game->getDernierCoup();

// Barre de progression
$progression = (21 - $total) / 21 * 100;
if ($total > 14) $couleur = '#27ae60';
elseif ($total > 7) $couleur = '#f1c40f';
else $couleur = '#e74c3c';

// Indicateur de tour
$estTourJoueur = ($joueurActuel === 'joueur' && !$estTermine);
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jeu du 21 - Clavier</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container" id="gameContainer">
        <!-- TITRE -->
        <h1 class="title">JEU DU 21</h1>
        
        <!-- STATUT DU TOUR -->
        <div class="tour-indicator <?= $estTourJoueur ? 'tour-joueur' : 'tour-ordinateur' ?>">
            <?php if ($estTermine): ?>
                Partie terminee
            <?php elseif ($joueurActuel === 'joueur'): ?>
                Ton tour ! (fleches)
            <?php else: ?>
                Ordinateur reflechit...
            <?php endif; ?>
        </div>
        
        <!-- POINTS -->
        <div class="points-container">
            <p class="points-label">Points restants :</p>
            <div class="points-number <?= $total <= 3 ? 'points-danger' : '' ?>">
                <?= $total ?>
            </div>
        </div>
        
        <!-- BARRE DE PROGRESSION -->
        <div class="progress-container">
            <div class="progress-bar" style="width: <?= 100 - $progression ?>%; background-color: <?= $couleur ?>;"></div>
        </div>
        
        <!-- DERNIER COUP -->
        <?php if ($dernierCoup !== null): ?>
        <div class="dernier-coup">
            Dernier coup : <strong><?= $dernierCoup ?></strong> point<?= $dernierCoup > 1 ? 's' : '' ?>
        </div>
        <?php endif; ?>
        
        <!-- MESSAGE -->
        <div class="message-container">
            <p class="message"><?= nl2br($message) ?></p>
        </div>
        
        <!-- BOUTONS ACTION -->
        <div class="buttons-container">
            <button onclick="nouvellePartie()" class="btn btn-rejouer">Nouvelle partie</button>
            <button onclick="afficherRegles()" class="btn btn-regles">Regles</button>
        </div>
        
        <!-- STATISTIQUES -->
        <div class="stats-container">
            <span class="stat victoires">Victoires : <?= $victoires ?></span>
            <span class="stat defaites">Defaites : <?= $defaites ?></span>
        </div>
    </div>
    
    <!-- POPUP REGLES (masquee par defaut) -->
    <div id="rulesPopup" class="rules-overlay" style="display:none;">
        <div class="rules-modal">
            <h1 class="rules-title">REGLES DU JEU DU 21</h1>
            <div class="rules-content">
                <h2>BUT DU JEU</h2>
                <p>Le jeu commence avec <strong>21 points</strong>.</p>
                
                <h2>DEROULEMENT</h2>
                <ul>
                    <li>A ton tour, utilise les <strong>fleches du clavier</strong> :</li>
                    <li style="list-style:none; text-align:center; margin:15px 0;">
                        <span style="background:#3498db; color:white; padding:10px 20px; border-radius:8px;">↑ = 1 point</span>
                        <span style="background:#2ecc71; color:white; padding:10px 20px; border-radius:8px;">← = 2 points</span>
                        <span style="background:#e67e22; color:white; padding:10px 20px; border-radius:8px;">→ = 3 points</span>
                    </li>
                    <li>L'ordinateur joue automatiquement.</li>
                    <li>Celui qui prend le <strong>DERNIER point</strong> perd la partie !</li>
                </ul>
                
                <h2>ASTUCE</h2>
                <p>Pour gagner, laisse toujours un <strong>multiple de 4</strong> a ton adversaire !</p>
                <p class="astuce">(4, 8, 12, 16 ou 20)</p>
                
                <h2>BONNE CHANCE !</h2>
            </div>
            <button onclick="fermerRegles()" class="btn btn-fermer">Fermer</button>
        </div>
    </div>
    
    <!-- JAVASCRIPT -->
    <script>
        // --- GESTION DU CLAVIER ---
        document.addEventListener('keydown', function(event) {
            // Verifie si la popup est ouverte
            const popup = document.getElementById('rulesPopup');
            if (popup.style.display === 'block') {
                // Si la popup est ouverte, on bloque les fleches
                if (['ArrowUp', 'ArrowLeft', 'ArrowRight'].includes(event.key)) {
                    event.preventDefault();
                }
                return;
            }
            
            // Empêche le defilement de la page avec les fleches
            if (['ArrowUp', 'ArrowLeft', 'ArrowRight'].includes(event.key)) {
                event.preventDefault();
            }
            
            // Verifie si le jeu est termine ou si c'est le tour de l'ordinateur
            const estTermine = <?= json_encode($estTermine) ?>;
            const joueurActuel = <?= json_encode($joueurActuel) ?>;
            
            if (estTermine || joueurActuel !== 'joueur') {
                // Effet visuel pour indiquer que ce n'est pas le moment
                document.getElementById('gameContainer').style.transform = 'scale(0.98)';
                setTimeout(() => {
                    document.getElementById('gameContainer').style.transform = 'scale(1)';
                }, 200);
                return;
            }
            
            // Associe les fleches aux retraits
            let retrait = null;
            switch(event.key) {
                case 'ArrowUp':
                    retrait = 1;
                    break;
                case 'ArrowLeft':
                    retrait = 2;
                    break;
                case 'ArrowRight':
                    retrait = 3;
                    break;
                default:
                    return;
            }
            
            // Anime le chiffre
            const points = document.querySelector('.points-number');
            points.style.transform = 'scale(1.3)';
            points.style.color = '#e74c3c';
            setTimeout(() => {
                points.style.transform = 'scale(1)';
                points.style.color = '';
            }, 300);
            
            // Envoie la requete
            jouer(retrait);
        });
        
        // --- FONCTIONS ---
        function jouer(retrait) {
            const form = document.createElement('form');
            form.method = 'POST';
            
            const actionInput = document.createElement('input');
            actionInput.type = 'hidden';
            actionInput.name = 'action';
            actionInput.value = 'jouer';
            
            const retraitInput = document.createElement('input');
            retraitInput.type = 'hidden';
            retraitInput.name = 'retrait';
            retraitInput.value = retrait;
            
            form.appendChild(actionInput);
            form.appendChild(retraitInput);
            document.body.appendChild(form);
            form.submit();
        }
        
        function nouvellePartie() {
            const form = document.createElement('form');
            form.method = 'POST';
            
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'action';
            input.value = 'reinitialiser';
            
            form.appendChild(input);
            document.body.appendChild(form);
            form.submit();
        }
        
        function afficherRegles() {
            document.getElementById('rulesPopup').style.display = 'flex';
        }
        
        function fermerRegles() {
            document.getElementById('rulesPopup').style.display = 'none';
        }
        
        // Fermer la popup en cliquant a l'exterieur
        document.getElementById('rulesPopup').addEventListener('click', function(event) {
            if (event.target === this) {
                fermerRegles();
            }
        });
        
        // --- ANIMATION D'ATTENTE ---
        <?php if ($joueurActuel === 'joueur' && !$estTermine): ?>
        let clignote = true;
        setInterval(() => {
            const message = document.querySelector('.message');
            if (message) {
                message.style.opacity = clignote ? '1' : '0.5';
                clignote = !clignote;
            }
        }, 1000);
        <?php endif; ?>
    </script>
</body>
</html>