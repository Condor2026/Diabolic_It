# 📍 Hoja de ruta de DIABOLIC (IT)

Este documento describe las fases de desarrollo planificadas para **DIABOLIC IT**, una herramienta OSINT diseñada para el contexto italiano. Dado que es un proyecto en su etapa inicial, esta hoja de ruta establece los pasos clave para construir, verificar y expandir la herramienta.
La hoja de ruta es orientativa y puede ajustarse según las necesidades de la comunidad y los principios éticos del proyecto.

---

## 🟢 Fase 1: Configuración Inicial y Estructura Base

- [ ] **Estructura del repositorio**:
  - Crear el repositorio `Diabolic_IT` en GitHub.
  - Configurar plantillas para issues y PRs, archivo `.gitignore` y `requirements.txt`.

- [ ] **Configuración del entorno de desarrollo**:
  - Establecer la estructura de directorios (`src/`, `data/`, `tests/`, `docs/`).
  - Implementar la configuración central y el menú principal interactivo en la terminal, adaptando la interfaz al idioma local.

- [ ] **Implementación de componentes base**:
  - Codificar el `GestorDatos` (JSON) y el `DetectorURLs` (paths iniciales para `cronaca`, `succesi`, `attualita`).
  - Desarrollar el `ExtractorNoticias` (peticiones HTTP, rotación de User-Agent, lista de `agenti_utente`).

---

## 🟡 Fase 2: Fuentes de Información y Scraping

### 2.1 Identificación de fuentes
- [ ] Investigar y listar los principales periódicos de cada región de Italia (Corriere della Sera, La Repubblica, La Stampa, Il Sole 24 Ore, etc.).
- [ ] Priorizar fuentes según relevancia, acceso y seguridad.

### 2.2 Configuración y pruebas de scraping
- [ ] Incorporar las URLs de los periódicos regionales en la lista `FONTI_BASE`.
- [ ] Implementar un sistema de verificación automática de URLs para mantener las fuentes actualizadas.
- [ ] Realizar pruebas exhaustivas para asegurar la extracción correcta de datos y afinar la paginación inteligente.
- [ ] Implementar un sistema de logs para monitorizar errores.

---

## 🟠 Fase 3: Análisis y Clasificación de Datos

### 3.1 Diccionario de delitos en italiano
- [ ] Crear y refinar un diccionario de términos relacionados con delitos (`PAROLE_CHIAVE`), adaptado al léxico criminal italiano (por ejemplo, 'rapina', 'estorsione', 'omicidio', 'spaccio', 'stalking', 'riciclaggio', 'mafia', 'Camorra', 'Ndrangheta').
- [ ] Ampliar la lista de palabras clave con términos de la jerga criminal regional para mejorar la detección.

### 3.2 Reglas de clasificación
- [ ] Desarrollar la función `classifica_tipo()` y el mapeo a `TIPI_DELITTO`.
- [ ] Definir el formato de salida de los datos (por ejemplo, `titolo`, `data`, `regione`, `tipo`, `fonte`).

### 3.3 Mejoras en la detección de patrones
- [ ] Expandir la opción de conexiones entre incidentes para reflejar las particularidades de la criminalidad organizada en Italia (detectar cadenas de mando, relaciones entre clanes, etc.).
- [ ] Refinar los algoritmos de agrupación por modus operandi y frecuencia temporal.

---

## 🔴 Fase 4: Interfaz Web y Despliegue

### 4.1 Plantilla HTML/CSS
- [ ] Diseñar una interfaz de usuario responsive en italiano, con los mismos parámetros de filtrado (`ultimi_7_giorni`, `ultimi_30_giorni`, `ultimi_90_giorni`) y gráficos interactivos.

### 4.2 Integración y pruebas del servidor web
- [ ] Vincular la interfaz con el backend (`app.route`), los datos y las funciones de exportación.
- [ ] Realizar pruebas de integración para garantizar la estabilidad de la comunicación entre el frontend y el backend.
- [ ] Ejecutar pruebas de usabilidad para validar la experiencia de usuario en un entorno local.

### 4.3 Preparación para el despliegue
- [ ] Revisar y actualizar la documentación para usuarios y desarrolladores.
- [ ] Crear documentación en formato PDF (manual de uso) para la versión inicial.
- [ ] Planificar y ejecutar las pruebas finales de integración y aceptación.

---

## 📌 Notas sobre la metodología de desarrollo

- **La hoja de ruta es un documento vivo**: A medida que se completen las tareas, se añadirán nuevas ideas y se priorizarán las funcionalidades.
- **Ética y transparencia**: Todo el desarrollo se realizará bajo los mismos principios éticos de las otras versiones de DIABOLIC, con estricto respeto a la privacidad, sin almacenar datos personales y promoviendo la transparencia.
- **Comunidad**: Se fomentarán las contribuciones abiertas. Las nuevas ideas se gestionarán a través de los *issues* de GitHub.

---

*Última actualización: mayo 2026*  
**SpectrumSecurity** – *OSINT ético al servicio de la ciudadanía* 🔥
