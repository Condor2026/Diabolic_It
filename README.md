```markdown
# 🔥 DIABOLIC ITALIA v6.0

![Version](https://img.shields.io/badge/version-6.0-red)
![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green)
![OSINT](https://img.shields.io/badge/OSINT-Passivo%20%7C%20Analitico-blueviolet)
![GitHub release](https://img.shields.io/badge/release-v6.0-brightgreen)
![GitHub last commit](https://img.shields.io/github/last-commit/Condor2026/Diabolic_Italia)
![GitHub code size](https://img.shields.io/github/languages/code-size/Condor2026/Diabolic_Italia)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
![Made with Flask](https://img.shields.io/badge/Made%20with-Flask-black)
![Termux](https://img.shields.io/badge/Termux-Supported-blue)
![Linux](https://img.shields.io/badge/Linux-Supported-green)
![GitHub stars](https://img.shields.io/github/stars/Condor2026/Diabolic_Italia?style=social)
![GitHub forks](https://img.shields.io/github/forks/Condor2026/Diabolic_Italia?style=social)

**DIABOLIC ITALIA** è uno strumento OSINT passivo e analitico progettato per monitorare automaticamente oltre 70 giornali digitali italiani (nazionali, regionali e locali), estraendo e processando notizie di cronaca nera per rilevare modelli criminali, tendenze geografiche e connessioni tra incidenti.

Nasce con una filosofia chiara: *“Un grande potere comporta una grande responsabilità”*. Per questo il suo design dà priorità alla trasparenza, all’etica e al rispetto della privacy.

---

## 📌 Indice

- [🔍 Cos’è DIABOLIC?](#-cosè-diabolic)
- [⚙️ Caratteristiche principali](#️-caratteristiche-principali)
- [🛠️ Tecnologia e architettura](#️-tecnologia-e-architettura)
- [📥 Installazione e uso](#-installazione-e-uso)
- [🖥️ Modalità terminale (10 comandi)](#️-modalità-terminale-10-comandi)
- [🌐 Modalità web interattiva](#-modalità-web-interattiva)
- [📰 Fonti monitorate](#-fonti-monitorate)
- [🧠 Tipo di OSINT e metodologia](#-tipo-di-osint-e-metodologia)
- [⚖️ Etica, legalità e protezione dei dati](#️-etica-legalità-e-protezione-dei-dati)
- [🤝 Contributi e futuro](#-contributi-e-futuro)
- [📜 Licenza](#-licenza)

---

## 🔍 Cos’è DIABOLIC?

DIABOLIC automatizza il processo di *scraping* delle notizie di cronaca nera dai media italiani. Invece di leggere decine di giornali ogni giorno, lo strumento:

- **Estrae** automaticamente titoli, date, fonti e posizioni geografiche (regione) da notizie relative a reati.
- **Classifica** gli incidenti in categorie (furto, truffa, narcotraffico, violenza, omicidio, mafia, ecc.).
- **Archivia** i dati localmente in formato JSON, senza conservare alcun dato personale.
- **Analizza** le tendenze temporali (7, 30, 90 giorni) e le distribuzioni per regione e tipo di reato.
- **Rileva connessioni** tra incidenti: stessa zona, date vicine, stesso modus operandi (colpo, estorsione, ecc.) che possono indicare la stessa organizzazione criminale.
- **Visualizza** i risultati tramite un’interfaccia web interattiva con grafici a barre e filtri dinamici.
- **Esporta** i dati in CSV o JSON per analisi esterne.

---

## ⚙️ Caratteristiche principali

### 🔁 Rotazione dello User‑Agent
Evita i blocchi da parte dei giornali simulando diversi browser e versioni ad ogni richiesta.

### 🧠 Impaginazione intelligente
Prova automaticamente fino a 12 diversi formati di paginazione (`/pagina/2`, `?page=2`, `?offset=2`, ecc.) e ricorda quello funzionante per ogni dominio.

### 🔎 Rilevatore automatico di URL
Se un URL di un giornale smette di funzionare, il sistema cerca percorsi alternativi (`/cronaca`, `/cronache`, `/notizie`, `/cronaca-nera`, ecc.) e aggiorna la configurazione.

### 📊 Classificazione avanzata dei reati
Utilizza un ampio elenco di parole chiave, inclusi i termini della criminalità italiana (mafia, camorra, ’ndrangheta, estorsione, spaccio, ecc.). È facilmente estendibile.

### 🔗 Connessioni tra incidenti
- Per tipo e regione (es. 5 furti in Lombardia in 7 giorni).
- Per modus operandi (rileva la ripetizione di termini come “colpo” o “estorsione”).
- Frequenza temporale (incidenti/giorno).

### 🌐 Interfaccia web interattiva
- Grafici a barre per regione e tipo di reato.
- Filtri per periodo (ultimi 7, 30, 90 giorni).
- Elenco degli ultimi 20 incidenti.
- Pulsanti per aggiornare i dati ed esportare in JSON/CSV.

### 🖥️ Menù terminale completo
10 comandi che consentono di eseguire tutte le funzioni senza dover aprire il browser.

---

## 🛠️ Tecnologia e architettura

- **Linguaggio**: Python 3.8+
- **Framework web**: Flask (server leggero)
- **Scraping**: Requests + BeautifulSoup4
- **Archiviazione**: JSON locale (nessun database esterno)
- **Struttura modulare**:
  - `DetectorURLs`: verifica e corregge gli URL dei giornali.
  - `GestorDatos`: carica, salva e processa gli incidenti.
  - `ExtractorNoticias`: scraping con rotazione User‑Agent e paginazione intelligente.
- **Colori nel terminale**: codici ANSI.

---

## 📥 Installazione e uso

### Su Termux (Android)
```bash
pkg update && pkg upgrade -y
pkg install python git -y
pip install requests beautifulsoup4 flask
git clone https://github.com/Condor2026/Diabolic_Italia
cd Diabolic_Italia
python Diabolic_Italia.py
```

### Su Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install python3 python3-pip git -y
pip3 install requests beautifulsoup4 flask
git clone https://github.com/Condor2026/Diabolic_Italia
cd Diabolic_Italia
python3 Diabolic_Italia.py
```

---

## 🖥️ Modalità terminale (10 comandi)

All’avvio di `Diabolic_Italia.py` compare il menù principale:

```
╔════════════════════════════════════════════════════╗
║              M E N Ú   P R I N C I P A L           ║
╚════════════════════════════════════════════════════╝
[1] 🔍 Cerca notizie
[2] 📊 Analisi completa
[3] 🔗 Connessioni tra incidenti
[4] 📈 Evoluzione mensile
[5] 🌐 Avvia server web
[6] 📰 Ultimi 20 incidenti
[7] 📥 Esporta dati (JSON/CSV)
[8] 🔍 Verifica giornali
[9] 📊 Distribuzione per tipo
[0] 🗑️ Esci
```

Ogni opzione esegue l’azione corrispondente e mostra i risultati direttamente nel terminale.

---

## 🌐 Modalità web interattiva

L’opzione `[5]` avvia un server Flask locale (di solito su `http://localhost:5013`). Dal browser puoi:

- Visualizzare grafici a barre interattivi.
- Filtrare per regione e tipo di reato.
- Consultare l’elenco degli incidenti.
- Esportare i dati in CSV o JSON con un clic.

---

## 📰 Fonti monitorate

Lo strumento monitora oltre **70 giornali digitali italiani**, tra cui:

- **Nazionali**: Corriere della Sera (Cronaca, Cronaca Nera), La Repubblica (Cronaca), Il Fatto Quotidiano (Cronaca Nera), Il Giornale (Cronaca Nera), La Stampa, Il Messaggero, ANSA, Adnkronos, TGCOM24, Sky TG24, RaiNews, Il Sole 24 Ore, Libero, La Verità, Today.it, Virgilio Notizie, Il Resto del Carlino, La Nazione, Il Gazzettino, Il Mattino.
- **Regionali/locale**: Corriere Milano, Repubblica Milano, MilanoToday, BergamoToday, BresciaToday, LeccoToday, Prima Lodi, Repubblica Roma, RomaToday, Repubblica Veneto, Corriere del Veneto, VeneziaToday, VeronaToday, VicenzaToday, TrevisoToday, PadovaOggi, Repubblica Bologna, BolognaToday, Repubblica Firenze, FirenzeToday, PisaToday, LivornoToday, Il Tirreno, Repubblica Napoli, NapoliToday, Cronache di Napoli, Giornale di Sicilia, Repubblica Palermo, PalermoToday, SiracusaToday, Live Sicilia, La Sicilia, La Stampa Torino, TorinoToday, GenovaToday, Corriere Adriatico, Il Centro (Abruzzo), La Nuova Sardegna, L'Unione Sarda, L'Adige, Alto Adige, Il Piccolo, Messaggero Veneto, Gazzetta di Parma, Quotidiano di Puglia, Gazzetta del Mezzogiorno.

L’elenco completo è consultabile/modificabile all’interno dello script (`PERIODICOS_BASE`).

---

## 🧠 Tipo di OSINT e metodologia

- **OSINT passivo**: non interagisce con i sistemi dei giornali oltre ciò che farebbe un utente normale.
- **Estrazione selettiva**: raccoglie solo informazioni di cronaca nera, giustizia e polizia.
- **Anonimizzazione**: non conserva dati personali delle persone coinvolte, solo luogo, data e tipo di reato.
- **Approccio analitico**: non si limita a raccogliere notizie, ma cerca modelli che possano aiutare a comprendere la criminalità in Italia.

---

## ⚖️ Etica, legalità e protezione dei dati

DIABOLIC ITALIA rispetta rigorosamente le leggi italiane ed europee:

- Accede solo a contenuti pubblici e non richiede autenticazione.
- Non conserva informazioni personali (nomi, indirizzi, codici fiscali, ecc.).
- Il codice è aperto e trasparente.
- Si raccomanda di utilizzare lo strumento esclusivamente per scopi accademici, giornalistici o di ricerca legittima.

### ⚠️ Avvertenza legale
Questo strumento è esclusivamente a fini educativi e di ricerca legittima. Non deve essere utilizzato per molestare, *doxare*, svolgere attività illegali o violare la privacy delle persone. L’autore non si assume alcuna responsabilità per un uso improprio. L’utente è l’unico responsabile del rispetto delle leggi del proprio paese.

---

## 🤝 Contributi e futuro

I contributi sono benvenuti. Puoi:

- Segnalare errori tramite Issues.
- Ampliare l’elenco dei giornali o delle regioni.
- Migliorare il rilevatore automatico di URL.
- Aggiungere nuove categorie di reati.
- Ottimizzare l’analisi delle connessioni.

---

## 📜 Licenza

Questo progetto è distribuito sotto **GNU General Public License v3.0 (GPLv3)**.  
Ciò significa che:

- Puoi usare, studiare, condividere e modificare il software liberamente.
- Se distribuisci versioni modificate, **devi rilasciarle con la stessa licenza**.
- **Non puoi renderlo proprietario**; qualsiasi opera derivata deve rimanere open source.
- Il software viene fornito “così com’è”, senza garanzie (consultare il file `LICENSE` per i dettagli).

Consulta il file [`LICENSE`](LICENSE) per il testo completo della licenza.

---

## 🙏 Ringraziamenti

- BeautifulSoup4 – per lo scraping.
- Flask – per l’interfaccia web.
- Ispirazione da progetti OSINT come Sherlock e Maigret.
- Comunità di ricerca OSINT in Italia.

⭐ **Se il progetto ti piace, non dimenticare di lasciare una stella su GitHub!**
```
