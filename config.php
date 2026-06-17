<?php
$host = "localhost";
$db_name = "revyz_box_erick";
$username = "root";
$password = "";

try {
    $pdo = new PDO("mysql:host=$host;dbname=$db_name;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    echo json_encode(["error" => "Connexion échouée : " . $e->getMessage()]);
    exit;
}

function ajouterUtilisateur($pdo, $nom, $prenom, $pseudo, $mot_de_passe)
{
    $sql = "INSERT INTO utilisateurs (nom, prenom, pseudo, mot_de_passe) VALUES (:nom, :prenom, :pseudo, :mot_de_passe)";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([
        ':nom' => $nom,
        ':prenom' => $prenom,
        ':pseudo' => $pseudo,
        ':mot_de_passe' => password_hash($mot_de_passe, PASSWORD_DEFAULT)
    ]);
    return $pdo->lastInsertId();
}

function modifierUtilisateur($pdo, $id, $nom, $prenom, $pseudo)
{
    $sql = "UPDATE utilisateurs SET nom = :nom, prenom = :prenom, pseudo = :pseudo WHERE id = :id";
    $stmt = $pdo->prepare($sql);
    return $stmt->execute([
        ':id' => $id,
        ':nom' => $nom,
        ':prenom' => $prenom,
        ':pseudo' => $pseudo
    ]);
}

function modifierMotDePasse($pdo, $id, $nouveauMotDePasse)
{
    $sql = "UPDATE utilisateurs SET mot_de_passe = :mot_de_passe WHERE id = :id";
    $stmt = $pdo->prepare($sql);
    return $stmt->execute([
        ':id' => $id,
        ':mot_de_passe' => password_hash($nouveauMotDePasse, PASSWORD_DEFAULT)
    ]);
}

function listerUtilisateurs($pdo) {
    $sql = "SELECT u.*, s.nom AS statut_nom 
            FROM utilisateurs u
            LEFT JOIN statuts s ON u.id_statut = s.id_statut
            ORDER BY u.id DESC";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}
?>