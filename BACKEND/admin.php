<?php
require_once '../config.php';

// Gestion des actions
$message = '';
$messageType = '';

// Ajout d'un utilisateur
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {
    if ($_POST['action'] === 'add') {
        if (!empty($_POST['nom']) && !empty($_POST['prenom']) && !empty($_POST['pseudo']) && !empty($_POST['mot_de_passe'])) {
            $id = ajouterUtilisateur($pdo, $_POST['nom'], $_POST['prenom'], $_POST['pseudo'], $_POST['mot_de_passe']);
            if ($id) {
                $message = "Utilisateur ajouté avec succès !";
                $messageType = "success";
            } else {
                $message = "Erreur lors de l'ajout de l'utilisateur.";
                $messageType = "danger";
            }
        } else {
            $message = "Tous les champs sont requis.";
            $messageType = "danger";
        }
    }
    
    // Modification d'un utilisateur
    elseif ($_POST['action'] === 'edit') {
        if (!empty($_POST['id']) && !empty($_POST['nom']) && !empty($_POST['prenom']) && !empty($_POST['pseudo'])) {
            $result = modifierUtilisateur($pdo, $_POST['id'], $_POST['nom'], $_POST['prenom'], $_POST['pseudo']);
            if ($result) {
                $message = "Utilisateur modifié avec succès !";
                $messageType = "success";
            } else {
                $message = "Erreur lors de la modification.";
                $messageType = "danger";
            }
        } else {
            $message = "Tous les champs sont requis.";
            $messageType = "danger";
        }
    }
    
    // Modification du mot de passe
    elseif ($_POST['action'] === 'change_password') {
        if (!empty($_POST['id']) && !empty($_POST['nouveau_mot_de_passe'])) {
            $result = modifierMotDePasse($pdo, $_POST['id'], $_POST['nouveau_mot_de_passe']);
            if ($result) {
                $message = "Mot de passe modifié avec succès !";
                $messageType = "success";
            } else {
                $message = "Erreur lors de la modification du mot de passe.";
                $messageType = "danger";
            }
        } else {
            $message = "Le nouveau mot de passe est requis.";
            $messageType = "danger";
        }
    }
    
    // Suppression d'un utilisateur
    elseif ($_POST['action'] === 'delete') {
        if (!empty($_POST['id'])) {
            $sql = "DELETE FROM utilisateurs WHERE id = :id";
            $stmt = $pdo->prepare($sql);
            $result = $stmt->execute([':id' => $_POST['id']]);
            if ($result) {
                $message = "Utilisateur supprimé avec succès !";
                $messageType = "success";
            } else {
                $message = "Erreur lors de la suppression.";
                $messageType = "danger";
            }
        }
    }
}

// Récupération de la liste des utilisateurs avec la fonction de listing (déjà dans config.php)
$utilisateurs = listerUtilisateurs($pdo);

// Récupération d'un utilisateur pour modification
$editUser = null;
if (isset($_GET['edit'])) {
    $sql = "SELECT * FROM utilisateurs WHERE id = :id";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([':id' => $_GET['edit']]);
    $editUser = $stmt->fetch(PDO::FETCH_ASSOC);
}

// Récupération d'un utilisateur pour changement de mot de passe
$passwordUser = null;
if (isset($_GET['change_password'])) {
    $sql = "SELECT * FROM utilisateurs WHERE id = :id";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([':id' => $_GET['change_password']]);
    $passwordUser = $stmt->fetch(PDO::FETCH_ASSOC);
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Administration - Gestion des utilisateurs</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar -->
            <nav class="col-md-3 col-lg-2 d-md-block bg-dark sidebar min-vh-100">
                <div class="position-sticky pt-3">
                    <div class="text-center mb-4">
                        <img src="https://via.placeholder.com/80x80?text=Logo" alt="Logo" class="rounded-circle mb-2">
                        <h5 class="text-white">Administration</h5>
                        <p class="text-white-50">Gestion des utilisateurs</p>
                    </div>
                    <ul class="nav flex-column">
                        <li class="nav-item">
                            <a class="nav-link active text-white" href="admin.php">
                                <i class="fas fa-users me-2"></i> Utilisateurs
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link text-white-50" href="#">
                                <i class="fas fa-chart-line me-2"></i> Statistiques
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link text-white-50" href="#">
                                <i class="fas fa-cog me-2"></i> Paramètres
                            </a>
                        </li>
                    </ul>
                </div>
            </nav>

            <!-- Main content -->
            <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
                <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                    <h1 class="h2">
                        <i class="fas fa-users me-2"></i>Gestion des utilisateurs
                    </h1>
                    <div class="btn-toolbar mb-2 mb-md-0">
                        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addUserModal">
                            <i class="fas fa-plus me-2"></i>Ajouter un utilisateur
                        </button>
                    </div>
                </div>

                <!-- Alert messages -->
                <?php if ($message): ?>
                    <div class="alert alert-<?= $messageType ?> alert-dismissible fade show" role="alert">
                        <i class="fas fa-<?= $messageType === 'success' ? 'check-circle' : 'exclamation-triangle' ?> me-2"></i>
                        <?= htmlspecialchars($message) ?>
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                <?php endif; ?>

                <!-- Compteur d'utilisateurs -->
                <div class="row mb-3">
                    <div class="col-md-3">
                        <div class="card bg-primary text-white">
                            <div class="card-body">
                                <h5 class="card-title">Total utilisateurs</h5>
                                <h2 class="mb-0"><?= count($utilisateurs) ?></h2>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Users table -->
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead class="table-dark">
                            <tr>
                                <th>ID</th>
                                <th>Nom</th>
                                <th>Prénom</th>
                                <th>Pseudo</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php if (empty($utilisateurs)): ?>
                                <tr>
                                    <td colspan="5" class="text-center">Aucun utilisateur trouvé</td>
                                </tr>
                            <?php else: ?>
                                <?php foreach ($utilisateurs as $user): ?>
                                    <tr>
                                        <td><?= htmlspecialchars($user['id']) ?></td>
                                        <td><?= htmlspecialchars($user['nom']) ?></td>
                                        <td><?= htmlspecialchars($user['prenom']) ?></td>
                                        <td><?= htmlspecialchars($user['pseudo']) ?></td>
                                        <td>
                                            <div class="btn-group" role="group">
                                                <a href="?edit=<?= $user['id'] ?>" class="btn btn-sm btn-warning">
                                                    <i class="fas fa-edit"></i> Modifier
                                                </a>
                                                <a href="?change_password=<?= $user['id'] ?>" class="btn btn-sm btn-info">
                                                    <i class="fas fa-key"></i> Mot de passe
                                                </a>
                                                <button type="button" class="btn btn-sm btn-danger" data-bs-toggle="modal" data-bs-target="#deleteModal<?= $user['id'] ?>">
                                                    <i class="fas fa-trash"></i> Supprimer
                                                </button>
                                            </div>

                                            <!-- Delete Modal -->
                                            <div class="modal fade" id="deleteModal<?= $user['id'] ?>" tabindex="-1">
                                                <div class="modal-dialog">
                                                    <div class="modal-content">
                                                        <div class="modal-header bg-danger text-white">
                                                            <h5 class="modal-title">
                                                                <i class="fas fa-exclamation-triangle me-2"></i>Confirmer la suppression
                                                            </h5>
                                                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                                        </div>
                                                        <div class="modal-body">
                                                            Êtes-vous sûr de vouloir supprimer l'utilisateur 
                                                            <strong><?= htmlspecialchars($user['prenom'] . ' ' . $user['nom']) ?></strong> ?
                                                            <br><br>
                                                            Cette action est irréversible.
                                                        </div>
                                                        <div class="modal-footer">
                                                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
                                                            <form method="POST" style="display: inline;">
                                                                <input type="hidden" name="action" value="delete">
                                                                <input type="hidden" name="id" value="<?= $user['id'] ?>">
                                                                <button type="submit" class="btn btn-danger">Supprimer</button>
                                                            </form>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </td>
                                    </tr>
                                <?php endforeach; ?>
                            <?php endif; ?>
                        </tbody>
                    </table>
                </div>

                <!-- Add User Modal -->
                <div class="modal fade" id="addUserModal" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header bg-primary text-white">
                                <h5 class="modal-title">
                                    <i class="fas fa-user-plus me-2"></i>Ajouter un utilisateur
                                </h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <form method="POST">
                                <div class="modal-body">
                                    <input type="hidden" name="action" value="add">
                                    <div class="mb-3">
                                        <label for="nom" class="form-label">Nom *</label>
                                        <input type="text" class="form-control" id="nom" name="nom" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="prenom" class="form-label">Prénom *</label>
                                        <input type="text" class="form-control" id="prenom" name="prenom" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="pseudo" class="form-label">Pseudo *</label>
                                        <input type="text" class="form-control" id="pseudo" name="pseudo" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="mot_de_passe" class="form-label">Mot de passe *</label>
                                        <input type="password" class="form-control" id="mot_de_passe" name="mot_de_passe" required>
                                    </div>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
                                    <button type="submit" class="btn btn-primary">Ajouter</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>

                <!-- Edit User Modal -->
                <?php if ($editUser): ?>
                    <div class="modal fade show" id="editUserModal" tabindex="-1" style="display: block; background: rgba(0,0,0,0.5);" aria-modal="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header bg-warning">
                                    <h5 class="modal-title">
                                        <i class="fas fa-user-edit me-2"></i>Modifier l'utilisateur
                                    </h5>
                                    <a href="admin.php" class="btn-close"></a>
                                </div>
                                <form method="POST">
                                    <div class="modal-body">
                                        <input type="hidden" name="action" value="edit">
                                        <input type="hidden" name="id" value="<?= $editUser['id'] ?>">
                                        <div class="mb-3">
                                            <label for="nom" class="form-label">Nom *</label>
                                            <input type="text" class="form-control" id="nom" name="nom" value="<?= htmlspecialchars($editUser['nom']) ?>" required>
                                        </div>
                                        <div class="mb-3">
                                            <label for="prenom" class="form-label">Prénom *</label>
                                            <input type="text" class="form-control" id="prenom" name="prenom" value="<?= htmlspecialchars($editUser['prenom']) ?>" required>
                                        </div>
                                        <div class="mb-3">
                                            <label for="pseudo" class="form-label">Pseudo *</label>
                                            <input type="text" class="form-control" id="pseudo" name="pseudo" value="<?= htmlspecialchars($editUser['pseudo']) ?>" required>
                                        </div>
                                    </div>
                                    <div class="modal-footer">
                                        <a href="admin.php" class="btn btn-secondary">Annuler</a>
                                        <button type="submit" class="btn btn-warning">Modifier</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                <?php endif; ?>

                <!-- Change Password Modal -->
                <?php if ($passwordUser): ?>
                    <div class="modal fade show" id="passwordModal" tabindex="-1" style="display: block; background: rgba(0,0,0,0.5);" aria-modal="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header bg-info text-white">
                                    <h5 class="modal-title">
                                        <i class="fas fa-key me-2"></i>Changer le mot de passe
                                    </h5>
                                    <a href="admin.php" class="btn-close"></a>
                                </div>
                                <form method="POST">
                                    <div class="modal-body">
                                        <input type="hidden" name="action" value="change_password">
                                        <input type="hidden" name="id" value="<?= $passwordUser['id'] ?>">
                                        <div class="mb-3">
                                            <label class="form-label">Utilisateur :</label>
                                            <input type="text" class="form-control" value="<?= htmlspecialchars($passwordUser['prenom'] . ' ' . $passwordUser['nom']) ?>" disabled>
                                        </div>
                                        <div class="mb-3">
                                            <label for="nouveau_mot_de_passe" class="form-label">Nouveau mot de passe *</label>
                                            <input type="password" class="form-control" id="nouveau_mot_de_passe" name="nouveau_mot_de_passe" required>
                                        </div>
                                        <div class="mb-3">
                                            <label for="confirm_password" class="form-label">Confirmer le mot de passe *</label>
                                            <input type="password" class="form-control" id="confirm_password" required>
                                            <div class="invalid-feedback">Les mots de passe ne correspondent pas</div>
                                        </div>
                                    </div>
                                    <div class="modal-footer">
                                        <a href="admin.php" class="btn btn-secondary">Annuler</a>
                                        <button type="submit" class="btn btn-info" id="submitPassword">Changer</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                    <script>
                        document.getElementById('confirm_password').addEventListener('keyup', function() {
                            const password = document.getElementById('nouveau_mot_de_passe').value;
                            const confirm = this.value;
                            const submitBtn = document.getElementById('submitPassword');
                            if (password === confirm && password !== '') {
                                this.classList.remove('is-invalid');
                                submitBtn.disabled = false;
                            } else {
                                this.classList.add('is-invalid');
                                submitBtn.disabled = true;
                            }
                        });
                    </script>
                <?php endif; ?>
            </main>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>