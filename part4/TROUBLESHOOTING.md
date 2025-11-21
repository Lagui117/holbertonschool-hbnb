 Guide de Dpannage - HBnB Part 

 Problèmes Frquents et Solutions

 Erreur CORS

 Symptôme
```
Access to fetch at 'http://localhost:/api/v/places' from origin 'http://localhost:' 
has been blocked by CORS policy
```

 Solutions

. Vrifier que Flask-CORS est install
```bash
cd /workspaces/holbertonschool-hbnb/part
pip install flask-cors
```

. Vrifier que CORS est import dans Part 
```python
 Dans part/app/__init__.py
from flask_cors import CORS

 Dans la fonction create_app()
CORS(app, resources={r"/api/": {"origins": ""}})
```

. Redmarrer l'API
```bash
 Arrêter l'API (Ctrl+C)
 Relancer
cd /workspaces/holbertonschool-hbnb/part
python run.py
```

---

 "Failed to load places"

 Symptôme
Message d'erreur sur la page d'accueil, aucune place affiche.

 Solutions

. Vrifier que l'API fonctionne
```bash
curl http://localhost:/api/v/places
```

. Vrifier les logs de l'API
```bash
 Dans le terminal où l'API tourne
 Regarder s'il y a des erreurs
```

. Crer des places de test
```bash
 Via Swagger UI
 Ouvrir http://localhost:/
 Se connecter (bouton Authorize)
 POST /api/v/places
```

. Vrifier la configuration de l'URL
```javascript
// Dans scripts.js, ligne 
const API_BASE_URL = 'http://localhost:/api/v';
// Assurez-vous que l'URL est correcte
```

---

 Login ne fonctionne pas

 Symptôme
Erreur "Login failed" même avec les bons identifiants.

 Solutions

. Vrifier que l'utilisateur existe
```bash
 Crer un utilisateur admin
cd /workspaces/holbertonschool-hbnb/part
python create_first_admin.py
```

. Tester le login via curl
```bash
curl -X POST http://localhost:/api/v/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin"}'
```

. Vrifier la console du navigateur
```
F  Console  Regarder les erreurs
```

. Vrifier les cookies
```
F  Application  Cookies  http://localhost:
```

---

 Cookie non cr après login

 Symptôme
Login russit mais le bouton reste "Login" au lieu de "Logout".

 Solutions

. Vrifier que vous servez via HTTP (pas file://)
```bash
 Les cookies ne fonctionnent pas avec file://
 Utiliser un serveur HTTP
python -m http.server 
```

. Vrifier le code JavaScript
```javascript
// Ouvrir la console
document.cookie
// Devrait afficher : "token=eyJ..."
```

. Vider le cache et les cookies
```
Ctrl+Shift+Delete  Cocher "Cookies"  Effacer
```

---

 "Cannot add review" / Erreur 

 Symptôme
Impossible d'ajouter une review, erreur Unauthorized.

 Solutions

. Vrifier que vous êtes connect
```javascript
// Console du navigateur
document.cookie
// Devrait contenir "token="
```

. Vrifier que le token est valide
```bash
 Le token expire peut-être
 Se reconnecter
```

. Vrifier les headers de la requête
```
F  Network  Cliquer sur la requête POST review
 Headers  Vrifier "Authorization: Bearer ..."
```

---

 Reviews ne s'affichent pas

 Symptôme
La section reviews est vide même s'il y en a.

 Solutions

. Vrifier la rponse API
```bash
curl http://localhost:/api/v/places/<PLACE_ID>
 Vrifier que "reviews" est prsent dans la rponse
```

. Vrifier la console
```
F  Console  Regarder s'il y a des erreurs JavaScript
```

. Vrifier le format des reviews
```javascript
// Les reviews doivent avoir cette structure :
{
  "id": "...",
  "text": "...",
  "rating": ,
  "user_name": "...",
  "created_at": "..."
}
```

---

 Filtre de prix ne fonctionne pas

 Symptôme
Slectionner un filtre ne change rien.

 Solutions

. Vrifier la console
```
F  Console  Regarder les erreurs
```

. Vrifier que les places ont un prix
```javascript
// Console
console.log(allPlaces);
// Vrifier que price_per_night ou price est prsent
```

. Recharger la page
```
Ctrl+F (hard refresh)
```

---

 Le design ne s'affiche pas

 Symptôme
Page sans style, texte brut.

 Solutions

. Vrifier que styles.css est charg
```
F  Network  Filtrer CSS  Vrifier styles.css
```

. Vrifier le chemin
```html
<!-- Dans les fichiers HTML -->
<link rel="stylesheet" href="styles.css">
<!-- Le fichier doit être à la racine de part/ -->
```

. Vider le cache
```
Ctrl+Shift+Delete
```

---

 JavaScript ne fonctionne pas

 Symptôme
Aucune interaction, page statique.

 Solutions

. Vrifier la console
```
F  Console  Regarder les erreurs de syntaxe
```

. Vrifier que scripts.js est charg
```
F  Network  Filtrer JS  Vrifier scripts.js
```

. Vrifier le chemin
```html
<!-- Dans les fichiers HTML -->
<script src="scripts.js"></script>
<!-- Doit être avant </body> -->
```

---

 Logo ne s'affiche pas

 Symptôme
Icône casse à la place du logo.

 Solutions

. Vrifier que le fichier existe
```bash
ls /workspaces/holbertonschool-hbnb/part/assets/logo.svg
```

. Crer un logo de remplacement
```html
<!-- Dans les fichiers HTML, remplacer par du texte -->
<h>HBnB</h>
<!-- Au lieu de -->
<img src="assets/logo.svg" alt="HBnB Logo" class="logo">
```

---

 Port djà utilis

 Symptôme
```
OSError: [Errno ] Address already in use
```

 Solutions

. Trouver le processus
```bash
 Pour l'API (port )
lsof -i :
 Pour le frontend (port )
lsof -i :
```

. Tuer le processus
```bash
kill - <PID>
```

. Utiliser un autre port
```bash
 Pour le frontend
python -m http.server 

 Modifier API_BASE_URL dans scripts.js si ncessaire
```

---

 Base de donnes vide

 Symptôme
Aucune donne n'apparat.

 Solutions

. Vrifier la base de donnes
```bash
cd /workspaces/holbertonschool-hbnb/part
ls instance/
 Devrait contenir development.db
```

. Crer des donnes via Swagger
```
. Ouvrir http://localhost:/
. Crer un user
. Se connecter (Authorize)
. Crer des amenities
. Crer des places
```

---

 Outils de Dbogage

 Console du Navigateur
```javascript
// Vrifier l'authentification
console.log('Token:', getCookie('token'));
console.log('Authenticated:', isAuthenticated());

// Vrifier les places charges
console.log('All places:', allPlaces);

// Tester une requête API
apiRequest('/places').then(console.log);
```

 Network Tab
```
F  Network  All
- Voir toutes les requêtes HTTP
- Vrifier les status codes (, , , etc.)
- Vrifier les headers
- Voir les rponses JSON
```

 Application Tab
```
F  Application
- Cookies : Voir les cookies stocks
- Local Storage : (non utilis dans ce projet)
- Session Storage : (non utilis dans ce projet)
```

---

 Checklist de Diagnostic

Avant de demander de l'aide, vrifier :

- [ ] L'API Part  est-elle lance ? (`http://localhost:`)
- [ ] Le serveur frontend est-il lanc ? (`http://localhost:`)
- [ ] Flask-CORS est-il install ?
- [ ] Y a-t-il des erreurs dans la console du navigateur ?
- [ ] Y a-t-il des erreurs dans le terminal de l'API ?
- [ ] Les cookies sont-ils activs dans le navigateur ?
- [ ] La base de donnes contient-elle des donnes ?
- [ ] Les chemins des fichiers CSS/JS sont-ils corrects ?
- [ ] Le cache du navigateur a-t-il t vid ?

---

 Support

Si le problème persiste :

. Redmarrage complet
   ```bash
    Arrêter tout (Ctrl+C partout)
   cd /workspaces/holbertonschool-hbnb/part
   ./start.sh
   ```

. Logs dtaills
   ```bash
    Voir les logs backend
   tail -f /tmp/hbnb_backend.log
   
    Voir les logs frontend
   tail -f /tmp/hbnb_frontend.log
   ```

. Reset complet
   ```bash
    Supprimer la base de donnes
   rm /workspaces/holbertonschool-hbnb/part/instance/development.db
   
    Relancer
   cd /workspaces/holbertonschool-hbnb/part
   python run.py
    La DB sera recre
   ```

Bonne chance ! 
