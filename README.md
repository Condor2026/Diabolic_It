# 🔥 DIABOLIC ITALIA v6.0

**Version 6.0 | License: MIT | Python 3.11 | OSINT: Passivo | Termux | Linux**

---

## DIABOLIC ITALIA è uno strumento OSINT passivo e analitico
che monitorizza automaticamente 30+ quotidiani digitali italiani
(Sicilia, Sardegna, Italia continentale) per rilevare,
classificare e visualizzare pattern criminali.

Non memorizza dati personali, solo titoli, date e regioni.
Filosofia: *"Un grande potere comporta una grande responsabilità"*

---

### 📌 Indice
- [🔍 Cosa fa DIABOLIC?](#-cosa-fa-diabolic)
- [⚙️ Caratteristiche chiave](#️-caratteristiche-chiave)
- [🛠️ Tecnologia e architettura](#️-tecnologia-e-architettura)
- [📥 Installazione e uso](#-installazione-e-uso)
- [🖥️ Modalità terminale (10 comandi)](#️-modalità-terminale-10-comandi)
- [🌐 Modalità web interattiva](#-modalità-web-interattiva)
- [📰 Fonti monitorizzate](#-fonti-monitorizzate)
- [🏛️ Regioni coperte](#️-regioni-coperte)
- [🧠 Lessico criminale italiano](#-lessico-criminale-italiano)
- [🧠 Tipo di OSINT e metodologia](#-tipo-di-osint-e-metodologia)
- [⚖️ Etica, legalità e protezione dei dati](#️-etica-legalità-e-protezione-dei-dati)
- [🤝 Contributi e futuro](#-contributi-e-futuro)
- [📜 Licenza](#-licenza)

---

### 🔍 Cosa fa DIABOLIC?

DIABOLIC automatizza lo scraping di notizie di cronaca
da media locali e nazionali italiani.

Invece di leggere decine di quotidiani ogni giorno,
lo strumento:

- Estrae titoli, date, fonti e regione da notizie di reati.
- Classifica gli incidenti in categorie
  (furto, truffa, narcotraffico, violenza, omicidio, mafia...).
- Memorizza i dati localmente in JSON, senza dati personali.
- Analizza tendenze temporali (7, 30, 90 giorni)
  e distribuzioni per regione e tipo di reato.
- Rileva connessioni tra incidenti:
  stessa zona, date vicine, stesso modus operandi
  (es. "colpo", "estorsione", "spaccio").
- Visualizza risultati con interfaccia web interattiva
  e grafici dinamici.
- Esporta dati in CSV o JSON.

---

### ⚙️ Caratteristiche chiave

🔁 **Rotazione User-Agent**
Evita blocchi simulando browser diversi.

🧠 **Paginazione intelligente**
Prova 12 formati di paginazione (/pagina/2, ?page=2...)
e ricorda quello funzionante per ogni dominio.

🔎 **Rilevatore automatico di URL**
Se un URL non funziona, cerca percorsi alternativi
(/cronaca, /notizie, /attualita...).

📊 **Classificazione avanzata**
Lista di parole chiave italiane
(mafia, camorra, ndrangheta, estorsione, usura...).

🔗 **Connessioni tra incidenti**
Per tipo e regione, per modus operandi,
frequenza temporale (incidenti/giorno).

🌐 **Interfaccia web interattiva**
Grafici per regione e tipo di reato.
Filtri per periodo (7, 30, 90 giorni).
Lista degli ultimi 20 incidenti.
Bottoni per aggiornare ed esportare JSON/CSV.

🖥️ **Menu terminale completo**
10 comandi per eseguire tutto senza browser.

🌍 **Multilingua**
Supporto italiano e spagnolo (selettore all'avvio).

---

### 🛠️ Tecnologia e architettura

- **Linguaggio:** Python 3.8+
- **Web framework:** Flask
- **Scraping:** Requests + BeautifulSoup4
- **Archiviazione:** JSON locale
- **Moduli principali:**
  - `DetectorURLs`: verifica e corregge URL.
  - `GestorDatos`: carica, salva e processa incidenti.
  - `ExtractorNoticias`: scraping con rotazione
    e paginazione intelligente.
- **Colori terminale:** Codici ANSI.

---

### 📥 Installazione e uso

#### Su Termux (Android)
```bash
pkg update && pkg upgrade -y
pkg install python git -y
pip install requests beautifulsoup4 flask
git clone https://github.com/Condor2026/Diabolic_Italia
cd Diabolic_Italia
python Diabolic_Italia.py
