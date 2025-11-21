 HBnB - Partie : Simple Web Client

 Description

Interface web complète pour l'application HBnB, dveloppe en HTML, CSS et JavaScript ES. Cette application front-end communique avec l'API REST dveloppe dans la Partie .

 Fonctionnalits

 . Authentification
- Connexion utilisateur via email et mot de passe
- Gestion des sessions avec JWT stock dans un cookie
- Protection des routes ncessitant une authentification
- Dconnexion avec suppression du token

 . Liste des Places
- Affichage de toutes les places disponibles
- Cartes visuelles avec informations essentielles
- Filtre de prix côt client (-$, -$, -$, $+)
- Navigation vers les dtails de chaque place

 . Dtails d'une Place
- Informations complètes (titre, description, prix, localisation)
- Dtails de l'hôte
- Liste des quipements (amenities)
- Affichage des reviews avec notes
- Bouton "Add Review" (visible uniquement si authentifi)

 . Ajout de Review
- Formulaire protg (authentification requise)
- Slection de note (- toiles)
- Zone de texte pour commentaire (minimum  caractères)
- Validation et messages d'erreur/succès
- Redirection automatique après succès

 Structure du Projet

```
part/
 index.html            Page principale - Liste des places
 login.html            Page de connexion
 place.html            Dtails d'une place
 add_review.html       Formulaire d'ajout de review
 styles.css            Styles CSS complets
 scripts.js            Logique JavaScript
 assets/
    logo.png          Logo de l'application
 README.md             Ce fichier
```

 Connexion avec l'API (Partie )

 Configuration

L'URL de base de l'API est dfinie dans `scripts.js` :
```javascript
const API_BASE_URL = 'http://localhost:/api/v';
```

 Endpoints Utiliss

| Mthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| POST | `/auth/login` | Connexion utilisateur | Non |
| GET | `/places` | Liste des places | Non |
| GET | `/places/<id>` | Dtails d'une place | Non |
| GET | `/users/<id>` | Informations utilisateur | Non |
| POST | `/places/<id>/reviews` | Ajouter une review | Oui |

 Gestion de l'Authentification

Le token JWT est :
- Stock dans un cookie nomm `token`
- Envoy dans le header `Authorization: Bearer <token>`
- Automatiquement supprim en cas de rponse 

 Installation et Dmarrage

 Prrequis
- API Part  fonctionnelle et lance sur `http://localhost:`
- Navigateur web moderne (Chrome, Firefox, Edge, Safari)

 Étapes

. Lancer l'API backend (Partie ) :
```bash
cd ../part
python run.py
```

. Activer CORS sur l'API :
Dans `part/app/__init__.py`, ajouter :
```python
from flask_cors import CORS

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app)   Activer CORS pour toutes les routes
     ... reste du code
```

Installer flask-cors si ncessaire :
```bash
pip install flask-cors
```

. Servir les fichiers front-end :

Option A - Python HTTP Server :
```bash
cd part
python -m http.server 
```

Option B - Node.js HTTP Server :
```bash
cd part
npx http-server -p 
```

Option C - Live Server (VS Code Extension)
- Installer l'extension "Live Server"
- Clic droit sur `index.html`  "Open with Live Server"

. Accder à l'application :
Ouvrir dans le navigateur : `http://localhost:`

 Tester l'Application

 . Test de Connexion

Crer un utilisateur admin (si pas djà fait) :
```bash
cd ../part
python create_first_admin.py
```

Se connecter :
- Email : admin@example.com
- Password : admin

 . Test des Places
- Vrifier l'affichage de toutes les places
- Tester le filtre de prix
- Cliquer sur "View Details" pour voir une place

 . Test des Reviews
- Se connecter
- Accder aux dtails d'une place
- Cliquer sur "Add Review"
- Soumettre une review

 Design Responsive

L'application s'adapte à diffrentes tailles d'cran :
- Desktop : > px
- Tablet : px - px
- Mobile : < px

 Validation WC

Pour valider le HTML :
```bash
 Via le validateur en ligne
https://validator.w.org/

 Ou uploader directement les fichiers HTML
```

 Classes CSS Importantes

 Conformit aux spcifications

| Classe | Utilisation |
|--------|-------------|
| `.logo` | Logo dans le header |
| `.login-button` | Bouton de connexion |
| `.place-card` | Carte de place dans la liste |
| `.details-button` | Bouton "View Details" |
| `.place-details` | Container des dtails |
| `.place-info` | Informations de la place |
| `.review-card` | Carte d'une review |
| `.add-review-button` | Bouton "Add Review" |

 Scurit

- Échappement HTML pour prvenir les injections XSS
- Validation côt client des formulaires
- Gestion scurise des tokens JWT
- Protection des routes sensibles

  Debugging

 Vrifier les requêtes API
Ouvrir la console dveloppeur (F)  Onglet Network

 Vrifier les cookies
Console  Application  Cookies  http://localhost:

 Logs JavaScript
Tous les appels API sont loggs dans la console

 Notes Importantes

. CORS : L'API doit autoriser les requêtes depuis `http://localhost:`
. Cookies : Fonctionnent uniquement en HTTP/HTTPS, pas en `file://`
. Token : Expire selon la configuration de l'API (par dfaut  jours côt client)

 Compatibilit

- Chrome/Edge +
- Firefox +
- Safari +
- Opera +

 Support

En cas de problème :
. Vrifier que l'API Part  fonctionne
. Vrifier la console du navigateur pour les erreurs
. Vrifier que CORS est activ sur l'API
. Vrifier que le serveur HTTP sert bien les fichiers

 Auteur

guillaume watelet 
Projet HBnB - Holberton School
Partie  - Simple Web Client
