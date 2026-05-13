#!/bin/bash

# ============================================
# INSTALLER DI DIABOLIC ITALIA v6.0
# OSINT passivo per l'analisi della criminalità
# ============================================

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Funzione per stampare intestazioni
print_header() {
    clear
    echo -e "${RED}══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}${BOLD}   🔥 DIABOLIC ITALIA v6.0 - INSTALLER AUTOMATICO 🔥   ${NC}"
    echo -e "${RED}══════════════════════════════════════════════════════════════════${NC}"
    echo ""
}

# Funzione per stampare messaggi di successo
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Funzione per stampare errori
error() {
    echo -e "${RED}❌ $1${NC}"
}

# Funzione per stampare avvisi
warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

# Funzione per stampare info
info() {
    echo -e "${CYAN}➡️ $1${NC}"
}

# Rilevazione del sistema operativo
detect_os() {
    if command -v pkg &> /dev/null; then
        OS="termux"
        success "Sistema rilevato: Termux (Android)"
    elif command -v apt &> /dev/null; then
        OS="linux"
        success "Sistema rilevato: Linux (Debian/Ubuntu)"
    else
        error "Sistema non supportato. Questo installer funziona solo su Termux o Linux con apt."
        exit 1
    fi
}

# Installazione dipendenze di sistema
install_system_deps() {
    info "Aggiornamento pacchetti e installazione dipendenze di sistema..."
    if [ "$OS" == "termux" ]; then
        pkg update -y
        pkg upgrade -y
        pkg install -y python git
    else
        sudo apt update -y
        sudo apt upgrade -y
        sudo apt install -y python3 python3-pip git
    fi
    success "Dipendenze di sistema installate"
}

# Installazione dipendenze Python
install_python_deps() {
    info "Installazione dipendenze Python (requests, beautifulsoup4, flask)..."
    if [ "$OS" == "termux" ]; then
        pip install requests beautifulsoup4 flask
    else
        pip3 install requests beautifulsoup4 flask
    fi
    if [ $? -eq 0 ]; then
        success "Dipendenze Python installate"
    else
        error "Errore nell'installazione delle dipendenze Python"
        exit 1
    fi
}

# Clonazione del repository (se non esiste)
clone_repo() {
    REPO_URL="https://github.com/Condor2026/Diabolic_Italia"
    REPO_DIR="Diabolic_Italia"
    if [ -d "$REPO_DIR" ]; then
        warning "La directory $REPO_DIR esiste già. Salto la clonazione."
        cd "$REPO_DIR"
    else
        info "Clonazione del repository da GitHub..."
        git clone "$REPO_URL" "$REPO_DIR"
        if [ $? -eq 0 ]; then
            success "Repository clonato con successo"
            cd "$REPO_DIR"
        else
            error "Impossibile clonare il repository. Verifica la connessione a Internet."
            exit 1
        fi
    fi
}

# Creazione del file requirements.txt se non esiste
create_requirements() {
    if [ ! -f "requirements.txt" ]; then
        info "Creazione del file requirements.txt..."
        cat > requirements.txt << EOF
# Dipendenze per DIABOLIC ITALIA v6.0
# Installa con: pip install -r requirements.txt

requests>=2.25.0
beautifulsoup4>=4.9.3
flask>=2.0.0
EOF
        success "File requirements.txt creato"
    else
        info "File requirements.txt già presente"
    fi
}

# Permessi di esecuzione per lo script principale
set_permissions() {
    if [ -f "Diabolic_Italia.py" ]; then
        chmod +x Diabolic_Italia.py
        success "Permessi di esecuzione impostati"
    else
        warning "File Diabolic_Italia.py non trovato. Assicurati che lo script principale sia nella directory."
    fi
}

# Messaggio finale
print_footer() {
    echo ""
    echo -e "${GREEN}══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}${BOLD}              INSTALLAZIONE COMPLETATA CON SUCCESSO!              ${NC}"
    echo -e "${GREEN}══════════════════════════════════════════════════════════════════${NC}"
    echo ""
    info "Per eseguire DIABOLIC ITALIA:"
    echo -e "   cd ${YELLOW}Diabolic_Italia${NC}"
    echo -e "   python ${YELLOW}Diabolic_Italia.py${NC}   (o python3 su Linux)"
    echo ""
    info "Se vuoi eseguire subito lo script:"
    echo -e "   ${CYAN}cd Diabolic_Italia && python Diabolic_Italia.py${NC}"
    echo ""
    echo -e "${RED}${BOLD}🕷️  \"Un grande potere comporta una grande responsabilità\"${NC}"
    echo -e "${RED}   - Spider-Man${NC}"
    echo ""
}

# Main
main() {
    print_header
    detect_os
    install_system_deps
    install_python_deps
    clone_repo
    create_requirements
    set_permissions
    print_footer
}

# Esecuzione
main
