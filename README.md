# SoftDesk Support API

API RESTful de suivi de problèmes techniques (issue tracking) pour des clients
B2B, développée avec Django REST Framework.

Elle permet de gérer des **projets**, leurs **contributeurs**, les **problèmes**
(issues) et les **commentaires**, avec une authentification par **JWT** et un
système de permissions respectant les exigences **OWASP**, **RGPD** et
**green code**.

## Fonctionnalités

- Authentification par **JSON Web Token** (JWT).
- Inscription ouverte, avec **vérification de l'âge** (≥ 15 ans, RGPD) et choix
  de consentement (`can_be_contacted`, `can_data_be_shared`).
- Gestion des **projets** : un utilisateur qui crée un projet en devient l'auteur
  et le premier contributeur.
- Gestion des **contributeurs** : seul l'auteur d'un projet peut ajouter ou
  retirer des contributeurs.
- Gestion des **issues** et **comments** : visibles par tous les contributeurs du
  projet, modifiables/supprimables uniquement par leur auteur.
- **RGPD** : chaque utilisateur ne peut consulter, modifier ou supprimer que son
  propre profil (droit d'accès, de rectification et à l'oubli).
- **Green code** : pagination des listes pour limiter la charge serveur.

## Stack technique

- Python 3.14
- Django
- Django REST Framework
- djangorestframework-simplejwt (JWT)
- Pipenv (gestion des dépendances)
- SQLite (base de données de développement)

## Installation

### Prérequis

- Python 3.14 installé
- Pipenv installé (`pip install pipenv`)

### Étapes

1. Cloner le dépôt puis se placer dans le dossier du projet :

   ```bash
   git clone <url-du-repo>
   cd SoftDesk
   ```

2. Installer les dépendances et créer l'environnement virtuel :

   ```bash
   pipenv install
   ```

3. Activer l'environnement virtuel :

   ```bash
   pipenv shell
   ```

4. Appliquer les migrations (création de la base de données) :

   ```bash
   python manage.py migrate
   ```

5. Lancer le serveur de développement :

   ```bash
   python manage.py runserver
   ```

L'API est alors disponible sur `http://127.0.0.1:8000/`.

## Authentification

L'API utilise des tokens JWT. Pour accéder aux endpoints protégés :

1. **Obtenir un token** — `POST /api/token/`

   ```json
   {
       "username": "votre_username",
       "password": "votre_password"
   }
   ```

   La réponse contient un token `access` et un token `refresh`.

2. **Utiliser le token** — ajouter l'en-tête à chaque requête protégée :

   ```
   Authorization: Bearer <access_token>
   ```

3. **Rafraîchir un token expiré** — `POST /api/token/refresh/`

   ```json
   {
       "refresh": "<refresh_token>"
   }
   ```

## Points de terminaison (endpoints)

| Méthode | URL | Description | Accès |
|---|---|---|---|
| POST | `/api/users/` | Inscription | Public |
| GET | `/api/users/` | Son propre profil | Authentifié |
| GET/PUT/PATCH/DELETE | `/api/users/{id}/` | Gérer son profil | Propriétaire |
| POST | `/api/token/` | Obtenir un token | Public |
| POST | `/api/token/refresh/` | Rafraîchir le token | Public |
| GET/POST | `/api/projects/` | Lister / créer un projet | Contributeur |
| GET/PUT/PATCH/DELETE | `/api/projects/{id}/` | Détail d'un projet | Contributeur (lecture) / Auteur (écriture) |
| GET/POST | `/api/contributors/` | Lister / ajouter un contributeur | Contributeur (lecture) / Auteur du projet (écriture) |
| GET/DELETE | `/api/contributors/{id}/` | Détail d'un contributeur | Contributeur (lecture) / Auteur du projet (écriture) |
| GET/POST | `/api/issues/` | Lister / créer une issue | Contributeur |
| GET/PUT/PATCH/DELETE | `/api/issues/{id}/` | Détail d'une issue | Contributeur (lecture) / Auteur (écriture) |
| GET/POST | `/api/comments/` | Lister / créer un commentaire | Contributeur |
| GET/PUT/PATCH/DELETE | `/api/comments/{id}/` | Détail d'un commentaire | Contributeur (lecture) / Auteur (écriture) |

### Filtrage

- `GET /api/issues/?project_id=<id>` — issues d'un projet
- `GET /api/contributors/?project_id=<id>` — contributeurs d'un projet
- `GET /api/comments/?issue_id=<id>` — commentaires d'une issue

## Tests des endpoints

Tous les endpoints peuvent être testés avec **Postman**, `curl`, ou l'interface
navigable de Django REST Framework.
</content>
</invoke>
