!/bin/bash

 Script de validation de la structure Part 

echo "==================================="
echo "  Validation HBnB Part  Structure"
echo "==================================="
echo ""

 Couleurs
GREEN='\[;m'
RED='\[;m'
NC='\[m'  No Color

 Compteurs
passed=
failed=

 Fonction de test
test_file() {
    if [ -f "$" ]; then
        echo -e "${GREEN}${NC} $ existe"
        ((passed++))
    else
        echo -e "${RED}${NC} $ manquant"
        ((failed++))
    fi
}

test_dir() {
    if [ -d "$" ]; then
        echo -e "${GREEN}${NC} Dossier $ existe"
        ((passed++))
    else
        echo -e "${RED}${NC} Dossier $ manquant"
        ((failed++))
    fi
}

 Vrifier la structure
echo "Structure de fichiers :"
echo "----------------------"
test_file "/workspaces/holbertonschool-hbnb/part/index.html"
test_file "/workspaces/holbertonschool-hbnb/part/login.html"
test_file "/workspaces/holbertonschool-hbnb/part/place.html"
test_file "/workspaces/holbertonschool-hbnb/part/add_review.html"
test_file "/workspaces/holbertonschool-hbnb/part/styles.css"
test_file "/workspaces/holbertonschool-hbnb/part/scripts.js"
test_file "/workspaces/holbertonschool-hbnb/part/README.md"
test_file "/workspaces/holbertonschool-hbnb/part/QUICKSTART.md"
test_dir "/workspaces/holbertonschool-hbnb/part/assets"
test_file "/workspaces/holbertonschool-hbnb/part/assets/logo.svg"

echo ""
echo "Vrification du contenu :"
echo "------------------------"

 Vrifier les classes CSS importantes
if grep -q "\.place-card" /workspaces/holbertonschool-hbnb/part/styles.css; then
    echo -e "${GREEN}${NC} Classe .place-card trouve dans styles.css"
    ((passed++))
else
    echo -e "${RED}${NC} Classe .place-card manquante"
    ((failed++))
fi

if grep -q "\.login-button" /workspaces/holbertonschool-hbnb/part/styles.css; then
    echo -e "${GREEN}${NC} Classe .login-button trouve dans styles.css"
    ((passed++))
else
    echo -e "${RED}${NC} Classe .login-button manquante"
    ((failed++))
fi

if grep -q "\.details-button" /workspaces/holbertonschool-hbnb/part/styles.css; then
    echo -e "${GREEN}${NC} Classe .details-button trouve dans styles.css"
    ((passed++))
else
    echo -e "${RED}${NC} Classe .details-button manquante"
    ((failed++))
fi

 Vrifier les fonctions JavaScript importantes
if grep -q "function.login" /workspaces/holbertonschool-hbnb/part/scripts.js; then
    echo -e "${GREEN}${NC} Fonction login trouve dans scripts.js"
    ((passed++))
else
    echo -e "${RED}${NC} Fonction login manquante"
    ((failed++))
fi

if grep -q "getCookie\|setCookie" /workspaces/holbertonschool-hbnb/part/scripts.js; then
    echo -e "${GREEN}${NC} Gestion des cookies trouve dans scripts.js"
    ((passed++))
else
    echo -e "${RED}${NC} Gestion des cookies manquante"
    ((failed++))
fi

if grep -q "API_BASE_URL" /workspaces/holbertonschool-hbnb/part/scripts.js; then
    echo -e "${GREEN}${NC} Configuration API trouve dans scripts.js"
    ((passed++))
else
    echo -e "${RED}${NC} Configuration API manquante"
    ((failed++))
fi

 Vrifier CORS dans Part 
if grep -q "flask_cors" /workspaces/holbertonschool-hbnb/part/app/__init__.py; then
    echo -e "${GREEN}${NC} CORS configur dans Part "
    ((passed++))
else
    echo -e "${RED}${NC} CORS non configur dans Part "
    ((failed++))
fi

echo ""
echo "==================================="
echo "Rsultats :"
echo -e "${GREEN} Passs : $passed${NC}"
echo -e "${RED} Échous : $failed${NC}"
echo "==================================="

if [ $failed -eq  ]; then
    echo -e "${GREEN}Tous les tests sont passs !${NC}"
    exit 
else
    echo -e "${RED}Certains tests ont chou.${NC}"
    exit 
fi
