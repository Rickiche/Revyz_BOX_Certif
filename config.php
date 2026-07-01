<?php
// config.php

$host = "localhost";
$db_name = "revyz_box_erick";
$username = "root";
$password = "";

try {
    $pdo = new PDO("mysql:host=$host;dbname=$db_name;charset=utf8mb4", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    die("Erreur de connexion : " . $e->getMessage());
}

/**
 * Ajouter un utilisateur
 */
function ajouterUtilisateur($pdo, $nom, $prenom, $pseudo, $mot_de_passe, $id_statut = 2) {
    // Vérifier que le statut existe
    $sql_check = "SELECT id_statut FROM statuts WHERE id_statut = :id_statut";
    $stmt_check = $pdo->prepare($sql_check);
    $stmt_check->execute([':id_statut' => $id_statut]);
    $statutExiste = $stmt_check->fetch(PDO::FETCH_ASSOC);
    
    if (!$statutExiste) {
        // Si le statut n'existe pas, on le met à 2 (Utilisateur) par défaut
        $id_statut = 2;
    }
    
    $sql = "INSERT INTO utilisateurs (nom, prenom, pseudo, mot_de_passe, id_statut) 
            VALUES (:nom, :prenom, :pseudo, :mot_de_passe, :id_statut)";
    $stmt = $pdo->prepare($sql);
    $result = $stmt->execute([
        ':nom' => $nom,
        ':prenom' => $prenom,
        ':pseudo' => $pseudo,
        ':mot_de_passe' => password_hash($mot_de_passe, PASSWORD_DEFAULT),
        ':id_statut' => $id_statut
    ]);
    return $result ? $pdo->lastInsertId() : false;
}

/**
 * Lister tous les utilisateurs avec leur statut
 */
function listerUtilisateurs($pdo) {
    $sql = "SELECT u.*, s.nom AS statut_nom 
            FROM utilisateurs u
            LEFT JOIN statuts s ON u.id_statut = s.id_statut
            ORDER BY u.id ASC";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

/**
 * Modifier un utilisateur (sans statut ni mot de passe - pour compatibilité)
 */
function modifierUtilisateur($pdo, $id, $nom, $prenom, $pseudo) {
    $sql = "UPDATE utilisateurs 
            SET nom = :nom, prenom = :prenom, pseudo = :pseudo
            WHERE id = :id";
    $stmt = $pdo->prepare($sql);
    return $stmt->execute([
        ':id' => $id,
        ':nom' => $nom,
        ':prenom' => $prenom,
        ':pseudo' => $pseudo
    ]);
}

/**
 * Modifier un utilisateur (complet avec statut et mot de passe optionnel)
 */
function modifierUtilisateurComplet($pdo, $id, $nom, $prenom, $pseudo, $id_statut, $nouveauMotDePasse = null) {
    // Vérifier que le statut existe
    $sql_check = "SELECT id_statut FROM statuts WHERE id_statut = :id_statut";
    $stmt_check = $pdo->prepare($sql_check);
    $stmt_check->execute([':id_statut' => $id_statut]);
    $statutExiste = $stmt_check->fetch(PDO::FETCH_ASSOC);
    
    if (!$statutExiste) {
        $id_statut = 2;
    }
    
    if ($nouveauMotDePasse !== null && !empty($nouveauMotDePasse)) {
        // Avec changement de mot de passe
        $sql = "UPDATE utilisateurs 
                SET nom = :nom, 
                    prenom = :prenom, 
                    pseudo = :pseudo, 
                    id_statut = :id_statut,
                    mot_de_passe = :mot_de_passe
                WHERE id = :id";
        $stmt = $pdo->prepare($sql);
        return $stmt->execute([
            ':id' => $id,
            ':nom' => $nom,
            ':prenom' => $prenom,
            ':pseudo' => $pseudo,
            ':id_statut' => $id_statut,
            ':mot_de_passe' => password_hash($nouveauMotDePasse, PASSWORD_DEFAULT)
        ]);
    } else {
        // Sans changement de mot de passe
        $sql = "UPDATE utilisateurs 
                SET nom = :nom, 
                    prenom = :prenom, 
                    pseudo = :pseudo, 
                    id_statut = :id_statut
                WHERE id = :id";
        $stmt = $pdo->prepare($sql);
        return $stmt->execute([
            ':id' => $id,
            ':nom' => $nom,
            ':prenom' => $prenom,
            ':pseudo' => $pseudo,
            ':id_statut' => $id_statut
        ]);
    }
}
?>