# 🔥 DIABOLIC ITALIA v6.0

[![Version](https://img.shields.io/badge/version-6.0-red)](https://github.com/Condor2026/Diabolic_Italia)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-green)](https://python.org)
[![OSINT](https://img.shields.io/badge/OSINT-Passive-blueviolet)](https://es.wikipedia.org/wiki/OSINT)
[![Termux](https://img.shields.io/badge/Termux-Compatible-orange)](https://termux.com)
[![Linux](https://img.shields.io/badge/Linux-Compatible-lightgrey)](https://linux.org)

**DIABOLIC ITALIA** es una herramienta OSINT pasiva y analítica diseñada para **monitorizar automáticamente más de 70 periódicos digitales italianos** (nacionales, regionales y locales), extrayendo y procesando noticias de sucesos para detectar patrones delictivos, tendencias geográficas y conexiones entre incidentes.

Nace con una filosofía clara: *“Un gran poder conlleva una gran responsabilidad”*. Por eso su diseño prioriza la transparencia, la ética y el respeto a la privacidad.

---

## 📌 Índice

- [🔍 ¿Qué hace DIABOLIC?](#-qué-hace-diabolic)
- [⚙️ Características clave](#️-características-clave)
- [🛠️ Tecnología y arquitectura](#️-tecnología-y-arquitectura)
- [📥 Instalación y uso](#-instalación-y-uso)
- [🖥️ Modo terminal (10 comandos)](#️-modo-terminal-10-comandos)
- [🌐 Modo web interactivo](#-modo-web-interactivo)
- [📰 Fuentes monitorizadas](#-fuentes-monitorizadas)
- [🧠 Tipo de OSINT y metodología](#-tipo-de-osint-y-metodología)
- [⚖️ Ética, legalidad y protección de datos](#️-ética-legalidad-y-protección-de-datos)
- [🤝 Contribuciones y futuro](#-contribuciones-y-futuro)
- [📜 Licencia](#-licencia)

---

## 🔍 ¿Qué hace DIABOLIC?

DIABOLIC automatiza el proceso de scraping de noticias de sucesos de medios italianos. En lugar de leer decenas de periódicos cada día, la herramienta:

- **Extrae** automáticamente titulares, fechas, fuentes y ubicaciones geográficas (región) de noticias relacionadas con delitos.
- **Clasifica** los incidentes en categorías (furto, truffa, narcotraffico, violenza, omicidio, mafia, etc.).
- **Almacena** los datos localmente en formato JSON, sin guardar ningún dato personal.
- **Analiza** tendencias temporales (7, 30, 90 días) y distribuciones por región y tipo de delito.
- **Detecta conexiones** entre incidentes: misma zona, fechas cercanas, mismo modus operandi (colpo, estorsione, etc.) que pueden indicar una misma organización criminal.
- **Visualiza** los resultados mediante una interfaz web interactiva con gráficos de barras y filtros dinámicos.
- **Exporta** los datos a CSV o JSON para análisis externos.

---

## ⚙️ Características clave

### 🔁 Rotación de User‑Agent
Evita bloqueos de los periódicos simulando diferentes navegadores y versiones en cada petición.

### 🧠 Paginación inteligente
Prueba automáticamente hasta 12 formatos diferentes de paginación (`/pagina/2`, `?page=2`, `?offset=2`, etc.) y recuerda el que funciona para cada dominio.

### 🔎 Detector automático de URLs
Si una URL de un periódico deja de funcionar, el sistema busca rutas alternativas (`/cronaca`, `/cronache`, `/notizie`, `/cronaca-nera`, etc.) y actualiza la configuración.

### 📊 Clasificación avanzada de delitos
Utiliza una lista amplia de palabras clave, incluyendo jerga italiana (mafia, camorra, ndrangheta, estorsione, spaccio, etc.). Se puede extender fácilmente.

### 🔗 Conexiones entre incidentes
- **Por tipo y región** (ej. 5 furti in Lombardia in 7 giorni).
- **Por modus operandi** (detecta repetición de términos como “colpo” o “estorsione”).
- **Frecuencia temporal** (incidenti/giorno).

### 🌐 Interfaz web interactiva
- Gráficos de barras por región y tipo de delito.
- Filtros por período (últimos 7, 30, 90 días).
- Lista de los últimos 20 incidentes.
- Botones para actualizar datos y exportar JSON/CSV.

### 🖥️ Menú terminal completo
10 comandos que permiten ejecutar todas las funciones sin necesidad de abrir el navegador.

---

## 🛠️ Tecnología y arquitectura

- **Lenguaje**: Python 3.8+
- **Framework web**: Flask (servidor ligero)
- **Scraping**: Requests + BeautifulSoup4
- **Almacenamiento**: JSON local (sin bases de datos externas)
- **Estructura modular**:
  - `DetectorURLs`: verifica y corrige URLs de periódicos.
  - `GestorDatos`: carga, guarda y procesa los incidentes.
  - `ExtractorNoticias`: scraping con rotación de User‑Agent y paginación inteligente.
- **Colores en terminal**: Códigos ANSI.

---

## 📥 Instalación y uso

### En Termux (Android)

```bash
pkg update && pkg upgrade -y
pkg install python git -y
pip install requests beautifulsoup4 flask
git clone https://github.com/Condor2026/Diabolic_Italia
cd Diabolic_Italia
python Diabolic_Italia.py
```

En Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install python3 python3-pip git -y
pip3 install requests beautifulsoup4 flask
git clone https://github.com/Condor2026/Diabolic_Italia
cd Diabolic_Italia
python3 Diabolic_Italia.py
```

---

🖥️ Modo terminal (10 comandos)

Al ejecutar Diabolic_Italia.py aparece un menú con las siguientes opciones:

```
╔════════════════════════════════════════════════════╗
║              M E N Ú   P R I N C I P A L           ║
╚════════════════════════════════════════════════════╝
[1] 🔍 Buscar noticias
[2] 📊 Ver análisis completo
[3] 🔗 Ver conexiones entre incidentes
[4] 📈 Ver evolución mensual
[5] 🌐 Iniciar servidor web
[6] 📰 Ver últimos 20 incidentes
[7] 📥 Exportar datos (JSON/CSV)
[8] 🔍 Verificar periódicos
[9] 📊 Ver distribución por tipo
[0] 🗑️ Salir
```

Cada opción ejecuta la acción correspondiente y muestra los resultados en la terminal.

---

🌐 Modo web interactivo

La opción [5] lanza un servidor Flask local (por defecto en http://localhost:5013). Desde el navegador podrás:

· Ver gráficos de barras interactivos.
· Filtrar por región y tipo de delito.
· Consultar la lista de incidentes.
· Exportar los datos a CSV o JSON con un clic.

---

📰 Fuentes monitorizadas

La herramienta rastrea más de 70 periódicos digitales italianos, incluyendo:

· Nacionales: Corriere della Sera (Cronaca, Cronaca Nera), La Repubblica (Cronaca), Il Fatto Quotidiano (Cronaca Nera), Il Giornale (Cronaca Nera), La Stampa, Il Messaggero, ANSA, Adnkronos, TGCOM24, Sky TG24, RaiNews, Il Sole 24 Ore, Libero, La Verità, Today.it, Virgilio Notizie, Il Resto del Carlino, La Nazione, Il Gazzettino, Il Mattino.
· Regionales: Corriere Milano, Repubblica Milano, MilanoToday, BergamoToday, BresciaToday, LeccoToday, Prima Lodi, Repubblica Roma, RomaToday, Repubblica Veneto, Corriere del Veneto, VeneziaToday, VeronaToday, VicenzaToday, TrevisoToday, PadovaOggi, Repubblica Bologna, BolognaToday, Repubblica Firenze, FirenzeToday, PisaToday, LivornoToday, Il Tirreno, Repubblica Napoli, NapoliToday, Cronache di Napoli, Giornale di Sicilia, Repubblica Palermo, PalermoToday, SiracusaToday, Live Sicilia, La Sicilia, La Stampa Torino, TorinoToday, GenovaToday, Corriere Adriatico, Il Centro (Abruzzo), La Nuova Sardegna, L'Unione Sarda, L'Adige, Alto Adige, Il Piccolo, Messaggero Veneto, Gazzetta di Parma, Quotidiano di Puglia, Gazzetta del Mezzogiorno.

La lista completa se puede consultar/editando dentro del script (PERIODICOS_BASE).

---

🧠 Tipo de OSINT y metodología

· OSINT Pasivo: No interactúa con los sistemas de los periódicos más allá de lo que un usuario normal haría.
· Extracción selectiva: Solo recoge información de sucesos (cronaca nera, giustizia, polizia).
· Anonimización: No almacena datos personales de los implicados, solo el lugar, fecha y tipo de delito.
· Enfoque analítico: No se limita a recopilar noticias, sino que busca patrones que puedan ayudar a entender la delincuencia en Italia.

---

⚖️ Ética, legalidad y protección de datos

DIABOLIC ITALIA respeta estrictamente la legalidad italiana y europea:

· Solo accede a contenido público y no requiere autenticación.
· No almacena información personal (nombres, DNI, direcciones, etc.).
· El código es abierto y transparente.
· Se recomienda utilizar la herramienta únicamente con fines académicos, periodísticos o de investigación criminal legítima.

⚠️ ADVERTENCIA LEGAL
Esta herramienta es exclusivamente para fines educativos y de investigación legítima. No debe utilizarse para acosar, doxear, realizar actividades ilegales o violar la privacidad de las personas. El autor no se responsabiliza del mal uso. El usuario es el único responsable de cumplir con las leyes de su país.

---

🤝 Contribuciones y futuro

Las contribuciones son bienvenidas. Puedes:

· Reportar errores en Issues.
· Ampliar la lista de periódicos o regiones.
· Mejorar el detector automático de URLs.
· Añadir nuevas categorías de delitos.
· Optimizar el análisis de conexiones.

---

📜 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

---

🙏 Agradecimientos

· BeautifulSoup4 – scraping.
· Flask – interfaz web.
· Inspiración: proyectos OSINT como Sherlock, Maigret.
· Comunidad de investigación OSINT en Italia.

⭐ ¡Si te gusta el proyecto, no olvides darle una estrella en GitHub!

```
---
