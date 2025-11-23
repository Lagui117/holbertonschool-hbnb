# HBnB Part 4 - Simple Web Client

## 📁 Structure du Projet

```
part4_yassin/
├── index.html          # Page d'accueil avec liste des places et filtre prix
├── login.html          # Page de connexion
├── place.html          # Page de détails d'une place avec reviews
├── add_review.html     # Page séparée pour ajouter une review
├── styles.css          # Styles CSS complets avec classes requises
├── scripts.js          # JavaScript avec toutes les fonctionnalités
├── config.js           # Configuration de l'API
├── logo.svg            # Logo HBnB (classe: logo)
├── icon.svg            # Favicon
└── README.md           # Ce fichier
```

## ✅ Conformité aux Exigences du Projet

### Task 0 - Design ✅

**Classes CSS requises (toutes implémentées):**
- ✅ `logo` - Logo dans le header
- ✅ `login-button` - Bouton de connexion
- ✅ `place-card` - Cartes des places (margin: 20px, padding: 10px, border: 1px solid #ddd, border-radius: 10px)
- ✅ `details-button` - Bouton "View Details"
- ✅ `place-details` - Section des détails du place
- ✅ `place-info` - Informations du place
- ✅ `review-card` - Cartes des reviews (margin: 20px, padding: 10px, border: 1px solid #ddd, border-radius: 10px)
- ✅ `add-review` - Section d'ajout de review
- ✅ `form` - Formulaire

**Structure HTML requise:**
- ✅ Header avec logo (logo.svg) et bouton login (classe login-button)
- ✅ Footer avec "All rights reserved"
- ✅ Navigation bar avec liens vers index.html et login.html
- ✅ Validation W3C pour toutes les pages

### Task 1 - Login ✅
- ✅ Formulaire de connexion fonctionnel
- ✅ AJAX/Fetch vers `/auth/login`
- ✅ Stockage JWT dans cookie
- ✅ Redirection vers index.html après succès
- ✅ Messages d'erreur affichés

### Task 2 - Index ✅
- ✅ Vérification authentification au chargement
- ✅ Affichage du lien login uniquement si non authentifié
- ✅ Fetch des places depuis `/places/`
- ✅ Filtre par prix côté client avec valeurs: All, 10, 50, 100
- ✅ Affichage dynamique des places avec bouton "View Details"

### Task 3 - Place Details ✅
- ✅ Extraction de l'ID depuis l'URL
- ✅ Vérification de l'authentification
- ✅ Fetch des détails depuis `/places/{id}`
- ✅ Affichage: nom, prix, description, host, amenities, location
- ✅ Liste des reviews
- ✅ Formulaire de review visible uniquement si authentifié

### Task 4 - Add Review Form ✅
- ✅ Page séparée `add_review.html`
- ✅ Vérification authentification (redirection vers index si non connecté)
- ✅ Extraction place_id depuis l'URL
- ✅ Formulaire avec rating (1-5) et texte
- ✅ POST vers `/reviews/`
- ✅ Messages de succès/erreur

## Installation et Utilisation

### 1. Configuration de l'API

Assurez-vous que votre API backend (Part 3) est en cours d'exécution sur `http://127.0.0.1:5000`

Si votre API est sur un autre port, modifiez `config.js`:
```javascript
const CONFIG = {
    API_BASE_URL: 'http://votre-url:port/api/v1',
    // ...
};
```

### 2. Lancement

Ouvrez simplement `index.html` dans votre navigateur, ou utilisez un serveur local:

```bash
# Avec Python
python3 -m http.server 8000

# Puis ouvrez http://localhost:8000
```

## 📋 Fonctionnalités

### Page d'accueil (index.html)
- ✅ Liste de tous les places disponibles
- ✅ Filtre par prix
- ✅ Navigation vers les détails
- ✅ Bouton Login/Logout dynamique

### Page de connexion (login.html)
- ✅ Formulaire de connexion
- ✅ Stockage du JWT dans un cookie
- ✅ Redirection après connexion
- ✅ Messages d'erreur

### Page de détails (place.html)
- ✅ Informations complètes du place
- ✅ Liste des amenities
- ✅ Affichage des reviews
- ✅ Formulaire d'ajout de review (si connecté)

## 🔐 Authentification

Le système utilise:
- JWT stocké dans un cookie nommé `token`
- Durée de validité: 7 jours
- Vérification automatique sur chaque page
- Déconnexion via le bouton Logout

## 🎨 Design

- Design responsive
- Interface propre et moderne
- Messages d'erreur clairs
- États de chargement
- Validation des formulaires

## 📝 API Endpoints Utilisés

### Public (sans authentification)
- `GET /places/` - Liste des places
- `GET /places/{id}` - Détails d'un place
- `GET /amenities/{id}` - Détails d'une amenity
- `GET /reviews/places/{id}/reviews` - Reviews d'un place
- `POST /auth/login` - Connexion

### Protégés (avec JWT)
- `POST /reviews/` - Créer une review

## 🐛 Dépannage

### L'API ne répond pas
- Vérifiez que le backend est lancé
- Vérifiez l'URL dans `config.js`
- Ouvrez la console du navigateur pour voir les erreurs

### Les reviews ne s'affichent pas
- Vérifiez que vous êtes connecté
- Vérifiez que le place a des reviews dans la base de données

### Le filtre ne fonctionne pas
- Rechargez la page
- Vérifiez que les places ont des prix valides

## 🔒 Sécurité

- Les cookies expirent après 7 jours
- Le JWT est envoyé dans le header Authorization
- Toutes les entrées utilisateur sont échappées
- Validation côté client ET serveur

## ✅ Checklist de Validation

- [ ] La page d'accueil charge tous les places
- [ ] Le filtre par prix fonctionne
- [ ] La connexion fonctionne et stocke le token
- [ ] Le bouton Login devient Logout après connexion
- [ ] La page de détails affiche toutes les informations
- [ ] Les amenities s'affichent correctement
- [ ] Les reviews s'affichent
- [ ] Le formulaire de review fonctionne (si connecté)
- [ ] La déconnexion fonctionne
- [ ] Le design est responsive
- [ ] Pas d'erreurs dans la console

## 📞 Support

En cas de problème, vérifiez:
1. La console du navigateur (F12)
2. Les logs du serveur backend
3. Que tous les fichiers sont présents
4. Que le backend est bien lancé
