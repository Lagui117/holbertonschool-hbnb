#!/bin/bash

# Script de démarrage automatique pour HBnB Part 4
# Lance l'API backend et le serveur front-end

echo "========================================="
echo "   HBnB - Démarrage de l'Application"
echo "========================================="
echo ""

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Vérifier les dépendances
echo -e "${BLUE}[1/4]${NC} Vérification des dépendances..."

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Erreur : Python 3 n'est pas installé${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Python 3 trouvé"

# Vérifier Flask-CORS
cd /workspaces/holbertonschool-hbnb/part3
if ! python3 -c "import flask_cors" 2>/dev/null; then
    echo -e "${YELLOW}⚠${NC} Flask-CORS non installé, installation..."
    pip install flask-cors > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} Flask-CORS installé"
    else
        echo -e "${RED}Erreur lors de l'installation de Flask-CORS${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓${NC} Flask-CORS trouvé"
fi

# Vérifier les autres dépendances Part 3
if [ -f requirements.txt ]; then
    echo -e "${BLUE}[2/4]${NC} Installation des dépendances Part 3..."
    pip install -r requirements.txt > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} Dépendances Part 3 installées"
    else
        echo -e "${YELLOW}⚠${NC} Certaines dépendances n'ont pas pu être installées"
    fi
else
    echo -e "${YELLOW}⚠${NC} Fichier requirements.txt non trouvé dans Part 3"
fi

# Vérifier la base de données
echo -e "${BLUE}[3/4]${NC} Vérification de la base de données..."
if [ -f instance/development.db ]; then
    echo -e "${GREEN}✓${NC} Base de données trouvée"
else
    echo -e "${YELLOW}⚠${NC} Base de données non trouvée, elle sera créée au démarrage"
fi

# Créer les fichiers PID pour gérer les processus
BACKEND_PID_FILE="/tmp/hbnb_backend.pid"
FRONTEND_PID_FILE="/tmp/hbnb_frontend.pid"

# Fonction pour nettoyer les processus à l'arrêt
cleanup() {
    echo ""
    echo -e "${YELLOW}Arrêt des serveurs...${NC}"
    
    if [ -f "$BACKEND_PID_FILE" ]; then
        BACKEND_PID=$(cat "$BACKEND_PID_FILE")
        kill $BACKEND_PID 2>/dev/null
        rm -f "$BACKEND_PID_FILE"
        echo -e "${GREEN}✓${NC} API Backend arrêtée"
    fi
    
    if [ -f "$FRONTEND_PID_FILE" ]; then
        FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")
        kill $FRONTEND_PID 2>/dev/null
        rm -f "$FRONTEND_PID_FILE"
        echo -e "${GREEN}✓${NC} Serveur Frontend arrêté"
    fi
    
    echo -e "${GREEN}Au revoir !${NC}"
    exit 0
}

# Capturer Ctrl+C
trap cleanup SIGINT SIGTERM

# Lancer l'API Backend (Part 3)
echo -e "${BLUE}[4/4]${NC} Démarrage de l'API Backend (Port 5000)..."
cd /workspaces/holbertonschool-hbnb/part3
python3 run.py > /tmp/hbnb_backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > "$BACKEND_PID_FILE"

# Attendre que l'API démarre
sleep 3

# Vérifier que l'API est bien lancée
if kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${GREEN}✓${NC} API Backend démarrée (PID: $BACKEND_PID)"
    echo -e "   ${BLUE}→${NC} http://localhost:5000"
else
    echo -e "${RED}✗${NC} Erreur lors du démarrage de l'API"
    echo -e "   Voir les logs : cat /tmp/hbnb_backend.log"
    exit 1
fi

# Lancer le serveur Frontend (Part 4)
echo -e "${BLUE}Démarrage du serveur Frontend (Port 8000)...${NC}"
cd /workspaces/holbertonschool-hbnb/part4
python3 -m http.server 8000 > /tmp/hbnb_frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > "$FRONTEND_PID_FILE"

# Attendre que le serveur démarre
sleep 2

# Vérifier que le frontend est bien lancé
if kill -0 $FRONTEND_PID 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Serveur Frontend démarré (PID: $FRONTEND_PID)"
    echo -e "   ${BLUE}→${NC} http://localhost:8000"
else
    echo -e "${RED}✗${NC} Erreur lors du démarrage du serveur Frontend"
    cleanup
    exit 1
fi

echo ""
echo "========================================="
echo -e "${GREEN}✓ Application HBnB démarrée !${NC}"
echo "========================================="
echo ""
echo -e "${BLUE}URLs disponibles :${NC}"
echo -e "  Frontend : ${YELLOW}http://localhost:8000${NC}"
echo -e "  API      : ${YELLOW}http://localhost:5000${NC}"
echo -e "  Swagger  : ${YELLOW}http://localhost:5000/${NC}"
echo ""
echo -e "${BLUE}Identifiants de test :${NC}"
echo -e "  Email    : ${YELLOW}admin@example.com${NC}"
echo -e "  Password : ${YELLOW}admin${NC}"
echo ""
echo -e "${BLUE}Logs :${NC}"
echo -e "  Backend  : tail -f /tmp/hbnb_backend.log"
echo -e "  Frontend : tail -f /tmp/hbnb_frontend.log"
echo ""
echo -e "${YELLOW}Appuyez sur Ctrl+C pour arrêter les serveurs${NC}"
echo ""

# Attendre indéfiniment (jusqu'à Ctrl+C)
while true; do
    # Vérifier que les processus tournent toujours
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo -e "${RED}✗ L'API Backend s'est arrêtée${NC}"
        cleanup
        exit 1
    fi
    
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo -e "${RED}✗ Le serveur Frontend s'est arrêté${NC}"
        cleanup
        exit 1
    fi
    
    sleep 5
done
