 Guide de Dmarrage Rapide - HBnB Part 

 Lancer l'Application Complète

 Étape  : Prparer l'API (Backend - Part )

```bash
 Aller dans le dossier Part 
cd /workspaces/holbertonschool-hbnb/part

 Vrifier que Flask-CORS est install
pip install -r requirements.txt

 Lancer l'API
python run.py
```

L'API devrait être accessible sur : `http://...:`

 Étape  : Crer un utilisateur de test

Dans un autre terminal :

```bash
cd /workspaces/holbertonschool-hbnb/part
python create_first_admin.py
```

Ou crer manuellement via l'API :

```bash
curl -X POST http://localhost:/api/v/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

 Étape  : Lancer le Front-End (Part )

Dans un nouveau terminal :

```bash
cd /workspaces/holbertonschool-hbnb/part

 Option A : Python HTTP Server
python -m http.server 

 Option B : Node.js (si install)
npx http-server -p  -c-
```

 Étape  : Ouvrir l'Application

Ouvrir dans le navigateur : `http://localhost:`

 Scnarios de Test

 Test  : Navigation sans authentification

. Ouvrir `http://localhost:`
. Vrifier : Liste des places s'affiche
. Vrifier : Bouton "Login" visible dans le header
. Cliquer sur une place
. Vrifier : Dtails de la place s'affichent
. Vrifier : Bouton "Add Review" est CACHÉ

 Test  : Connexion

. Cliquer sur "Login" dans le header
. Entrer les identifiants :
   - Email : `admin@example.com` (ou votre email)
   - Password : `admin` (ou votre mot de passe)
. Cliquer sur "Login"
. Vrifier : Redirection vers index.html
. Vrifier : Bouton "Logout" apparat dans le header

 Test  : Filtre de prix

. Sur la page d'accueil (index.html)
. Slectionner "Filter by Price"  "$ - $"
. Vrifier : Seules les places ≤ $ s'affichent
. Tester les autres filtres ($-$, etc.)

 Test  : Ajouter une review (authentifi)

. Se connecter
. Aller sur les dtails d'une place
. Vrifier : Bouton "Add Review" est VISIBLE
. Cliquer sur "Add Review"
. Remplir le formulaire :
   - Rating : 
   - Review : "Excellent place, highly recommended!"
. Cliquer sur "Submit Review"
. Vrifier : Message de succès
. Vrifier : Redirection vers la page de la place
. Vrifier : La nouvelle review apparat

 Test  : Dconnexion

. Cliquer sur "Logout" dans le header
. Vrifier : Bouton redevient "Login"
. Vrifier : Essayer d'accder à add_review.html  redirection vers index

 Vrification des Cookies

 Dans Chrome/Edge :
. F  Application  Cookies  http://localhost:
. Vrifier : Cookie "token" prsent après login
. Vrifier : Cookie "token" supprim après logout

 Dans Firefox :
. F  Storage  Cookies  http://localhost:

  Rsolution des Problèmes Courants

 Problème : "CORS error" dans la console

Solution :
- Vrifier que `flask-cors` est install dans Part 
- Vrifier que l'import CORS est bien dans `part/app/__init__.py`
- Redmarrer l'API Part 

 Problème : "Failed to load places"

Vrifications :
```bash
 Tester l'API directement
curl http://localhost:/api/v/places

 Devrait retourner un JSON avec la liste des places
```

Si vide, crer des places de test via Swagger : `http://localhost:/`

 Problème : "Login failed"

Vrifications :
```bash
 Vrifier que l'utilisateur existe
curl http://localhost:/api/v/users

 Tester le login directement
curl -X POST http://localhost:/api/v/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin"}'
```

 Problème : "Cannot add review"

Vrifications :
. Vrifier que vous êtes connect (cookie token prsent)
. Ouvrir la console (F) et regarder les erreurs
. Vrifier que l'endpoint `/api/v/places/{id}/reviews` fonctionne

 Donnes de Test

 Crer des Places de Test

Via Swagger UI (`http://localhost:/`) ou :

```bash
 Se connecter et rcuprer le token
TOKEN=$(curl -X POST http://localhost:/api/v/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin"}' \
  | jq -r '.access_token')

 Crer une place
curl -X POST http://localhost:/api/v/places \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Beautiful Beach House",
    "description": "Amazing ocean view with private beach access",
    "price": ,
    "latitude": .,
    "longitude": -.
  }'
```

 Checklist de Validation

- [ ] L'API Part  fonctionne (port )
- [ ] Le front-end est servi (port )
- [ ] CORS est activ sur l'API
- [ ] Un utilisateur de test existe
- [ ] La page login.html s'affiche correctement
- [ ] La page index.html charge les places
- [ ] Le filtre de prix fonctionne
- [ ] Les dtails d'une place s'affichent
- [ ] Le login fonctionne et redirige
- [ ] Le cookie token est cr
- [ ] Le bouton "Add Review" apparat si connect
- [ ] L'ajout de review fonctionne
- [ ] Le logout supprime le cookie
- [ ] Le design est responsive

 Notes

- Le logo peut être remplac par `assets/logo.svg` (fourni)
- L'URL de l'API est configurable dans `scripts.js` (ligne )
- Les cookies expirent après  jours par dfaut
- Toutes les requêtes API sont logges dans la console

 Pour Aller Plus Loin

 Personnalisation :

. Changer l'URL de l'API :
   - Éditer `scripts.js`, ligne  : `const API_BASE_URL = 'https://votre-api.com/api/v';`

. Ajouter d'autres filtres :
   - Exemple : filtre par pays, par ville, par nombre de chambres

. Amliorer le design :
   - Modifier `styles.css` selon vos prfrences

. Ajouter des images aux places :
   - Utiliser un service comme Unsplash API ou stocker des URLs d'images

Bon dveloppement ! 
