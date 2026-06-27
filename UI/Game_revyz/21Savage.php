<?php
class Game {
    private $total;
    private $joueurActuel;
    private $estTermine;
    private $message;
    
    public function __construct() {
        $this->total = 21;
        $this->joueurActuel = 'joueur';
        $this->estTermine = false;
        $this->message = 'À ton tour !';
    }
    
    public function getTotal() {
        return $this->total;
    }
    
    
    public function getJoueurActuel() {
        return $this->joueurActuel;
    }
    
    
    public function estTermine() {
        return $this->estTermine;
    }
    
    
    public function getMessage() {
        return $this->message;
    }
    
    public function jouerCoupJoueur($retrait) {
        if ($this->joueurActuel !== 'joueur') {
            return ['erreur' => 'Ce n\'est pas ton tour !'];
        }
        
        if ($retrait < 1 || $retrait > 3) {
            return ['erreur' => 'Tu dois retirer 1, 2 ou 3 points !'];
        }
        
        if ($retrait > $this->total) {
            return ['erreur' => "Il ne reste que {$this->total} points !"];
        }
        
        // Le joueur retire des points
        $this->total -= $retrait;
        $this->message = "✅ Tu as retiré {$retrait} points.";
        
        // Vérifie si le joueur a perdu
        if ($this->total == 0) {
            $this->estTermine = true;
            $this->message = "💀 Tu as pris le dernier point... TU PERDS !";
            return ['succes' => true, 'estTermine' => true, 'message' => $this->message];
        }
        
        // Passe le tour à l'ordinateur
        $this->joueurActuel = 'ordinateur';
        return ['succes' => true, 'estTermine' => false, 'message' => $this->message];
    }
    
    
    public function reinitialiser() {
        $this->total = 21;
        $this->joueurActuel = 'joueur';
        $this->estTermine = false;
        $this->message = '🔄 Nouvelle partie ! À ton tour !';
    }
    
    /**
     * Sauvegarde l'état du jeu en session
     */
    public function sauvegarder() {
        $_SESSION['game'] = [
            'total' => $this->total,
            'joueurActuel' => $this->joueurActuel,
            'estTermine' => $this->estTermine,
            'message' => $this->message
        ];
    }
    
    /**
     * Charge l'état du jeu depuis la session
     */
    public static function charger() {
        if (isset($_SESSION['game'])) {
            $data = $_SESSION['game'];
            $game = new self();
            $game->total = $data['total'];
            $game->joueurActuel = $data['joueurActuel'];
            $game->estTermine = $data['estTermine'];
            $game->message = $data['message'];
            return $game;
        }
        return new self();
    }
}
?>