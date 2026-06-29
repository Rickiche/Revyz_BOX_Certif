<?php
session_start();

class Game {
    private $total;
    private $joueurActuel;
    private $estTermine;
    private $message;
    private $victoires;
    private $defaites;
    
    public function __construct() {
        $this->total = 21;
        $this->joueurActuel = 'joueur';
        $this->estTermine = false;
        $this->message = '👤 À ton tour !';
        $this->victoires = 0;
        $this->defaites = 0;
    }
    
    // --- Méthodes de persistance ---
    public static function charger() {
        if (isset($_SESSION['game'])) {
            return unserialize($_SESSION['game']);
        }
        return new Game();
    }
    
    public function sauvegarder() {
        $_SESSION['game'] = serialize($this);
    }
    
    // --- Getters ---
    public function getTotal() { return $this->total; }
    public function getJoueurActuel() { return $this->joueurActuel; }
    public function estTermine() { return $this->estTermine; }
    public function getMessage() { return $this->message; }
    public function getVictoires() { return $this->victoires; }
    public function getDefaites() { return $this->defaites; }
    
    // --- Action joueur ---
    public function jouerCoupJoueur($retrait) {
        if ($this->estTermine) {
            return ['erreur' => 'La partie est terminée !'];
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
        
        $this->total -= $retrait;
        $this->message = "✅ Tu as retiré {$retrait} points.";
        
        if ($this->total == 0) {
            $this->estTermine = true;
            $this->defaites++;
            $this->message = "💀 Tu as pris le dernier point... TU PERDS !";
            return ['succes' => true, 'termine' => true];
        }
        
        $this->joueurActuel = 'ordinateur';
        $this->message .= "\n🤔 L'ordinateur réfléchit...";
        return ['succes' => true, 'termine' => false];
    }
    
    // --- Action ordinateur ---
    public function jouerCoupOrdinateur() {
        if ($this->estTermine) {
            return ['erreur' => 'La partie est terminée !'];
        }
        if ($this->joueurActuel !== 'ordinateur') {
            return ['erreur' => 'Ce n\'est pas le tour de l\'ordinateur !'];
        }
        
        // Stratégie : laisser un multiple de 4 si possible, sinon retirer aléatoirement entre 1 et 3
        $restant = $this->total;
        if ($restant <= 3) {
            // Si le total est 1, 2 ou 3, l'ordi en retire le maximum (pour gagner)
            $retrait = $restant; 
        } else {
            $mod = $restant % 4;
            if ($mod == 0) {
                // Si déjà multiple de 4, retrait aléatoire (mais on préfère 1,2,3)
                $retrait = rand(1, 3);
            } else {
                $retrait = $mod; // on retire le reste pour laisser un multiple de 4
            }
            // On s'assure que le retrait ne dépasse pas 3
            if ($retrait > 3) $retrait = 3;
            // Et qu'on ne retire pas plus que le total
            if ($retrait > $restant) $retrait = $restant;
        }
        
        $this->total -= $retrait;
        $this->message = "🤖 L'ordinateur a retiré {$retrait} points.";
        
        if ($this->total == 0) {
            $this->estTermine = true;
            $this->victoires++;
            $this->message = "🎉 L'ordinateur a pris le dernier point... TU GAGNES !";
            return ['succes' => true, 'termine' => true];
        }
        
        $this->joueurActuel = 'joueur';
        $this->message .= "\n👤 À ton tour !";
        return ['succes' => true, 'termine' => false];
    }
    
    // --- Réinitialisation ---
    public function reinitialiser() {
        $this->total = 21;
        $this->joueurActuel = 'joueur';
        $this->estTermine = false;
        $this->message = '🔄 Nouvelle partie ! À ton tour !';
    }
}

// ============================================
// TRAITEMENT DES ACTIONS
// ============================================

$game = Game::charger();
$action = isset($_POST['action']) ? $_POST['action'] : '';

if ($action === 'reinitialiser') {
    $game->reinitialiser();
    $game->sauvegarder();
    header('Location: ' . $_SERVER['PHP_SELF']);
    exit;
}

if ($action === 'jouer' && isset($_POST['retrait'])) {
    $retrait = (int)$_POST['retrait'];
    $resultat = $game->jouerCoupJoueur($retrait);
    if (isset($resultat['erreur'])) {
        // On garde le message d'erreur mais on ne change pas l'état
        $game->sauvegarder();
        header('Location: ' . $_SERVER['PHP_SELF']);
        exit;
    }
    // Si le jeu n'est pas terminé, c'est au tour de l'ordinateur
    if (!$resultat['termine']) {
        $game->sauvegarder(); // sauvegarde avant le tour ordi
        // On recharge le jeu pour éviter les problèmes de référence
        $game = Game::charger();
        $resultatOrdi = $game->jouerCoupOrdinateur();
        // On ignore les erreurs éventuelles (normalement pas)
        $game->sauvegarder();
    } else {
        $game->sauvegarder();
    }
    header('Location: ' . $_SERVER['PHP_SELF']);
    exit;
}

// Affichage des règles (popup)
if ($action === 'regles') {
    header('Content-Type: text/html');
    ?>
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>📖 Règles du jeu</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <div class="rules-modal">
            <h1>📖 RÈGLES DU JEU DU 21</h1>
            <div class="rules-content">
                <h2>🎯 BUT DU JEU</h2>
                <p>Le jeu commence avec <strong>21 points</strong>.</p>
                
                <h2>🔄 DÉROULEMENT</h2>
                <ul>
                    <li>À ton tour, tu peux retirer <strong>1, 2 ou 3 points</strong>.</li>
                    <li>L'ordinateur fait de même.</li>
                    <li>Celui qui prend le <strong>DERNIER point</strong> perd la partie !</li>
                </ul>
                
                <h2>💡 ASTUCE</h2>
                <p>Pour gagner, laisse toujours un <strong>multiple de 4</strong> à ton adversaire !</p>
                <p class="astuce">(4, 8, 12, 16 ou 20)</p>
                
                <h2>🎮 BONNE CHANCE !</h2>
            </div>
            <button onclick="window.close()" class="btn btn-fermer">Fermer</button>
        </div>
    </body>
    </html>
    <?php
    exit;
}

// ============================================
// AFFICHAGE (HTML)
// ============================================

// Récupération des données pour l'affichage (après rechargement)
$game = Game::charger(); // on recharge pour être sûr
$total = $game->getTotal();
$joueurActuel = $game->getJoueurActuel();
$estTermine = $game->estTermine();
$message = $game->getMessage();
$victoires = $game->getVictoires();
$defaites = $game->getDefaites();

$progression = (21 - $total) / 21 * 100;
if ($total > 14) $couleur = '#27ae60';
elseif ($total > 7) $couleur = '#f1c40f';
else $couleur = '#e74c3c';

$boutonsDesactives = ($estTermine || $joueurActuel !== 'joueur') ? 'disabled' : '';

?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎲 Jeu du 21</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1 class="title">🎲 JEU DU 21</h1>
        
        <div class="points-container">
            <p class="points-label">Points restants :</p>
            <div class="points-number"><?= $total ?></div>
        </div>
        
        <div class="progress-container">
            <div class="progress-bar" style="width: <?= 100 - $progression ?>%; background-color: <?= $couleur ?>;"></div>
        </div>
        
        <div class="message-container">
            <p class="message"><?= nl2br($message) ?></p>
        </div>
        
        <div class="buttons-container">
            <button onclick="jouer(1)" <?= $boutonsDesactives ?> class="btn btn-1">1</button>
            <button onclick="jouer(2)" <?= $boutonsDesactives ?> class="btn btn-2">2</button>
            <button onclick="jouer(3)" <?= $boutonsDesactives ?> class="btn btn-3">3</button>
        </div>
        
        <div class="buttons-container" style="margin-top: 15px;">
            <button onclick="nouvellePartie()" class="btn btn-rejouer">🔄 Nouvelle partie</button>
            <button onclick="afficherRegles()" class="btn btn-regles">📖 Règles</button>
        </div>
        
        <div class="stats-container">
            <span class="stat victoires">🏆 Victoires : <?= $victoires ?></span>
            <span class="stat defaites">💀 Défaites : <?= $defaites ?></span>
        </div>
    </div>
    
    <script>
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
            window.open('?action=regles', 'Règles', 'width=550,height=650,scrollbars=yes');
        }
    </script>
</body>
</html>