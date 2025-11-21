!/bin/bash

 Script de dmarrage automatique pour HBnB Part 
 Lance l'API backend et le serveur front-end

echo "========================================="
echo "   HBnB - Dmarrage de l'Application"
echo "========================================="
echo ""

 Couleurs
GREEN='\[;m'
BLUE='\[;m'
YELLOW='\[;m'
RED='\[;m'
NC='\[m'  No Color

 Vrifier les dpendances
echo -e "${BLUE}[/]${NC} Vrification des dpendances..."

 Vrifier Python
if ! command -v python &> /dev/null; then
    echo -e "${RED}Erreur : Python  n'est pas install${NC}"
    exit 
fi
echo -e "${GREEN}${NC} Python  trouv"

 Vrifier Flask-CORS
cd /workspaces/holbertonschool-hbnb/part
if ! python -c "import flask_cors" >/dev/null; then
    echo -e "${YELLOW}${NC} Flask-CORS non install, installation..."
    pip install flask-cors > /dev/null >&
    if [ $? -eq  ]; then
        echo -e "${GREEN}${NC} Flask-CORS install"
    else
        echo -e "${RED}Erreur lors de l'installation de Flask-CORS${NC}"
        exit 
    fi
else
    echo -e "${GREEN}${NC} Flask-CORS trouv"
fi

 Vrifier les autres dpendances Part 
if [ -f requirements.txt ]; then
    echo -e "${BLUE}[/]${NC} Installation des dpendances Part ..."
    pip install -r requirements.txt > /dev/null >&
    if [ $? -eq  ]; then
        echo -e "${GREEN}${NC} Dpendances Part  installes"
    else
        echo -e "${YELLOW}${NC} Certaines dpendances n'ont pas pu être installes"
    fi
else
    echo -e "${YELLOW}${NC} Fichier requirements.txt non trouv dans Part "
fi

 Vrifier la base de donnes
echo -e "${BLUE}[/]${NC} Vrification de la base de donnes..."
if [ -f instance/development.db ]; then
    echo -e "${GREEN}${NC} Base de donnes trouve"
else
    echo -e "${YELLOW}${NC} Base de donnes non trouve, elle sera cre au dmarrage"
fi

 Crer les fichiers PID pour grer les processus
BACKEND_PID_FILE="/tmp/hbnb_backend.pid"
FRONTEND_PID_FILE="/tmp/hbnb_frontend.pid"

 Fonction pour nettoyer les processus à l'arrêt
cleanup() {
    echo ""
    echo -e "${YELLOW}Arrêt des serveurs...${NC}"
    
    if [ -f "$BACKEND_PID_FILE" ]; then
        BACKEND_PID=$(cat "$BACKEND_PID_FILE")
        kill $BACKEND_PID >/dev/null
        rm -f "$BACKEND_PID_FILE"
        echo -e "${GREEN}${NC} API Backend arrête"
    fi
    
    if [ -f "$FRONTEND_PID_FILE" ]; then
        FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")
        kill $FRONTEND_PID >/dev/null
        rm -f "$FRONTEND_PID_FILE"
        echo -e "${GREEN}${NC} Serveur Frontend arrêt"
    fi
    
    echo -e "${GREEN}Au revoir !${NC}"
    exit 
}

 Capturer Ctrl+C
trap cleanup SIGINT SIGTERM

 Lancer l'API Backend (Part )
echo -e "${BLUE}[/]${NC} Dmarrage de l'API Backend (Port )..."
cd /workspaces/holbertonschool-hbnb/part
python run.py > /tmp/hbnb_backend.log >& &
BACKEND_PID=$!
echo $BACKEND_PID > "$BACKEND_PID_FILE"

 Attendre que l'API dmarre
sleep 

 Vrifier que l'API est bien lance
if kill - $BACKEND_PID >/dev/null; then
    echo -e "${GREEN}${NC} API Backend dmarre (PID: $BACKEND_PID)"
    echo -e "   ${BLUE}${NC} http://localhost:"
else
    echo -e "${RED}${NC} Erreur lors du dmarrage de l'API"
    echo -e "   Voir les logs : cat /tmp/hbnb_backend.log"
    exit 
fi

 Lancer le serveur Frontend (Part )
echo -e "${BLUE}Dmarrage du serveur Frontend (Port )...${NC}"
cd /workspaces/holbertonschool-hbnb/part
python -m http.server  > /tmp/hbnb_frontend.log >& &
FRONTEND_PID=$!
echo $FRONTEND_PID > "$FRONTEND_PID_FILE"

 Attendre que le serveur dmarre
sleep 

 Vrifier que le frontend est bien lanc
if kill - $FRONTEND_PID >/dev/null; then
    echo -e "${GREEN}${NC} Serveur Frontend dmarr (PID: $FRONTEND_PID)"
    echo -e "   ${BLUE}${NC} http://localhost:"
else
    echo -e "${RED}${NC} Erreur lors du dmarrage du serveur Frontend"
    cleanup
    exit 
fi

echo ""
echo "========================================="
echo -e "${GREEN} Application HBnB dmarre !${NC}"
echo "========================================="
echo ""
echo -e "${BLUE}URLs disponibles :${NC}"
echo -e "  Frontend : ${YELLOW}http://localhost:${NC}"
echo -e "  API      : ${YELLOW}http://localhost:${NC}"
echo -e "  Swagger  : ${YELLOW}http://localhost:/${NC}"
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

 Attendre indfiniment (jusqu'à Ctrl+C)
while true; do
     Vrifier que les processus tournent toujours
    if ! kill - $BACKEND_PID >/dev/null; then
        echo -e "${RED} L'API Backend s'est arrête${NC}"
        cleanup
        exit 
    fi
    
    if ! kill - $FRONTEND_PID >/dev/null; then
        echo -e "${RED} Le serveur Frontend s'est arrêt${NC}"
        cleanup
        exit 
    fi
    
    sleep 
done
