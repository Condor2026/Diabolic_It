#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔥 DIABOLIC ITALIA v6.0 - OSINT ANALYTICS PLATFORM
Monitorización de criminalidad en Italia (versión estable)
"""

import os
import sys
import time
import json
import hashlib
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from flask import Flask, render_template_string, jsonify, request
from collections import defaultdict

# ============================================
# IDIOMA (selector al inicio - español por defecto)
# ============================================
IDIOMA_ACTUAL = None

TEXTOS = {
    'es': {
        'app_name': '🔥 DIABOLIC ITALIA',
        'elegir_idioma': 'Elige idioma / Scegli lingua: 1. Español  2. Italiano',
        'menu_title': 'MENÚ PRINCIPAL',
        'cmd_buscar': '🔍 Buscar noticias',
        'cmd_analisis': '📊 Ver análisis completo',
        'cmd_conexiones': '🔗 Ver conexiones entre incidentes',
        'cmd_evolucion': '📈 Ver evolución mensual',
        'cmd_web': '🌐 Iniciar servidor web',
        'cmd_ultimos': '📰 Ver últimos 20 incidentes',
        'cmd_exportar': '📥 Exportar datos (JSON/CSV)',
        'cmd_verificar': '🔍 Verificar periódicos',
        'cmd_tipos': '📊 Ver distribución por tipo',
        'cmd_salir': '🗑️ Salir',
        'stats_total': 'Total incidentes',
        'incidentes': 'incidentes',
        'fuentes': 'fuentes',
        'regiones': 'regiones',
        'servidor_web': 'Servidor web',
        'presiona_ctrl_c': 'Presiona Ctrl+C para volver al menú',
        'hasta_pronto': 'Hasta pronto',
        'opcion_invalida': 'Opción no válida'
    },
    'it': {
        'app_name': '🔥 DIABOLIC ITALIA',
        'elegir_idioma': 'Scegli lingua / Elige idioma: 1. Español  2. Italiano',
        'menu_title': 'MENU PRINCIPALE',
        'cmd_buscar': '🔍 Cerca notizie',
        'cmd_analisis': '📊 Analisi completa',
        'cmd_conexiones': '🔗 Connessioni tra incidenti',
        'cmd_evolucion': '📈 Evoluzione mensile',
        'cmd_web': '🌐 Avvia server web',
        'cmd_ultimos': '📰 Ultimi 20 incidenti',
        'cmd_exportar': '📥 Esporta dati (JSON/CSV)',
        'cmd_verificar': '🔍 Verifica giornali',
        'cmd_tipos': '📊 Distribuzione per tipo',
        'cmd_salir': '🗑️ Esci',
        'stats_total': 'Totale incidenti',
        'incidentes': 'incidenti',
        'fuentes': 'fonti',
        'regiones': 'regioni',
        'servidor_web': 'Server web',
        'presiona_ctrl_c': 'Premi Ctrl+C per tornare al menu',
        'hasta_pronto': 'Arrivederci',
        'opcion_invalida': 'Opzione non valida'
    }
}

def seleccionar_idioma():
    global IDIOMA_ACTUAL
    print("\n" + "="*60)
    print(TEXTOS['es']['elegir_idioma'])
    opc = input("➤ ")
    IDIOMA_ACTUAL = 'it' if opc == '2' else 'es'
    print(f"\n✅ Idioma seleccionado: {'Italiano' if IDIOMA_ACTUAL == 'it' else 'Español'}\n")

def t(clave):
    return TEXTOS[IDIOMA_ACTUAL].get(clave, clave)

# ============================================
# COLORES (para terminal)
# ============================================
class Color:
    ROJO = '\033[91m'
    ROJO_OSCURO = '\033[31m'
    VERDE = '\033[92m'
    AMARILLO = '\033[93m'
    AZUL = '\033[94m'
    MAGENTA = '\033[95m'
    CIAN = '\033[96m'
    GRIS = '\033[90m'
    BLANCO = '\033[97m'
    NEGRITA = '\033[1m'
    SUBRAYADO = '\033[4m'
    RESET = '\033[0m'
    FONDO_ROJO = '\033[41m'
    FONDO_VERDE = '\033[42m'
    FONDO_AMARILLO = '\033[43m'
    FONDO_AZUL = '\033[44m'

def cprint(texto, color=None, negrita=False, subrayado=False, fondo=False, fin='\n'):
    colores = {
        'rojo': Color.ROJO, 'rojo_oscuro': Color.ROJO_OSCURO,
        'verde': Color.VERDE, 'amarillo': Color.AMARILLO,
        'azul': Color.AZUL, 'magenta': Color.MAGENTA,
        'cian': Color.CIAN, 'gris': Color.GRIS, 'blanco': Color.BLANCO
    }
    col = colores.get(color, '')
    neg = Color.NEGRITA if negrita else ''
    sub = Color.SUBRAYADO if subrayado else ''
    fondo_color = ''
    if fondo:
        if color == 'rojo':
            fondo_color = Color.FONDO_ROJO
        elif color == 'verde':
            fondo_color = Color.FONDO_VERDE
        elif color == 'amarillo':
            fondo_color = Color.FONDO_AMARILLO
        elif color == 'azul':
            fondo_color = Color.FONDO_AZUL
    print(f"{fondo_color}{neg}{sub}{col}{texto}{Color.RESET}", end=fin)

# ============================================
# CONFIGURACIÓN - Periódicos de Italia (70+ fuentes)
# ============================================
VERSION = "6.0"
PUERTO = 5013
ARCHIVO = 'diabolic_italia.json'
ARCHIVO_ESTADO = 'estado_periodicos_italia.json'
PAGINAS_BUSQUEDA = 10
TIEMPO_ESPERA = 1.2
TIMEOUT = 18

# User-Agents modernos (20+)
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Android 14; Mobile; rv:123.0) Gecko/123.0 Firefox/123.0',
    'Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

# Lista completa de periódicos italianos (70+)
PERIODICOS_BASE = [
    # NACIONALES FUERTES (Cronaca Nera / Cronache)
    {'nombre': 'Corriere della Sera Cronache', 'url': 'https://www.corriere.it/cronache/', 'base': 'https://www.corriere.it', 'zona': 'Italia', 'activo': True},
    {'nombre': 'Corriere della Sera Cronaca Nera', 'url': 'https://www.corriere.it/argomenti/cronaca-nera/', 'base': 'https://www.corriere.it', 'zona': 'Italia', 'activo': True},
    {'nombre': 'La Repubblica Cronaca', 'url': 'https://www.repubblica.it/cronaca/', 'base': 'https://www.repubblica.it', 'zona': 'Italia', 'activo': True},
    {'nombre': 'Il Fatto Quotidiano Cronaca Nera', 'url': 'https://www.ilfattoquotidiano.it/cronaca-nera/', 'base': 'https://www.ilfattoquotidiano.it', 'zona': 'Italia', 'activo': True},
    {'nombre': 'Il Giornale Cronaca Nera', 'url': 'https://www.ilgiornale.it/sezioni/cronaca-nera-167457.html', 'base': 'https://www.ilgiornale.it', 'zona': 'Italia', 'activo': True},
    {'nombre': 'La Stampa Cronaca', 'url': 'https://www.lastampa.it/cronaca/', 'base': 'https://www.lastampa.it', 'zona': 'Italia', 'activo': True},
    {'nombre': 'Il Messaggero', 'url': 'https://www.ilmessaggero.it/', 'base': 'https://www.ilmessaggero.it', 'zona': 'Italia', 'activo': True},
    {'nombre': 'ANSA Cronaca', 'url': 'https://www.ansa.it/sito/notizie/cronaca/cronaca.shtml', 'base': 'https://www.ansa.it', 'zona': 'Italia', 'activo': True},
    {'nombre': 'Adnkronos Cronaca', 'url': 'https://www.adnkronos.com/cronaca/', 'base': 'https://www.adnkronos.com', 'zona': 'Italia', 'activo': True},
    {'nombre': 'TGCOM24', 'url': 'https://www.tgcom24.mediaset.it/', 'base': 'https://www.tgcom24.mediaset.it', 'zona': 'Italia', 'activo': True},
    {'nombre': 'Sky TG24', 'url': 'https://tg24.sky.it/', 'base': 'https://tg24.sky.it', 'zona': 'Italia', 'activo': True},
    {'nombre': 'RaiNews', 'url': 'https://www.rainews.it/', 'base': 'https://www.rainews.it', 'zona': 'Italia', 'activo': True},
    {'nombre': 'Il Sole 24 Ore', 'url': 'https://www.ilsole24ore.com/', 'base': 'https://www.ilsole24ore.com', 'zona': 'Italia', 'activo': True},
    {'nombre': 'Libero Quotidiano', 'url': 'https://www.liberoquotidiano.it/', 'base': 'https://www.liberoquotidiano.it', 'zona': 'Italia', 'activo': True},
    {'nombre': 'La Verità', 'url': 'https://www.laverita.info/', 'base': 'https://www.laverita.info', 'zona': 'Italia', 'activo': True},
    {'nombre': 'Today.it', 'url': 'https://www.today.it/', 'base': 'https://www.today.it', 'zona': 'Italia', 'activo': True},
    {'nombre': 'Virgilio Notizie Cronaca', 'url': 'https://www.virgilio.it/notizie/cronaca/cronaca-nera/', 'base': 'https://www.virgilio.it', 'zona': 'Italia', 'activo': True},
    {'nombre': 'Il Resto del Carlino', 'url': 'https://www.ilrestodelcarlino.it/', 'base': 'https://www.ilrestodelcarlino.it', 'zona': 'Italia', 'activo': True},
    {'nombre': 'La Nazione', 'url': 'https://www.lanazione.it/', 'base': 'https://www.lanazione.it', 'zona': 'Italia', 'activo': True},
    {'nombre': 'Il Gazzettino', 'url': 'https://www.ilgazzettino.it/', 'base': 'https://www.ilgazzettino.it', 'zona': 'Italia', 'activo': True},
    {'nombre': 'Il Mattino', 'url': 'https://www.ilmattino.it/', 'base': 'https://www.ilmattino.it', 'zona': 'Italia', 'activo': True},
    {'nombre': 'Corriere dello Sport (cronaca)', 'url': 'https://www.corrieredellosport.it/', 'base': 'https://www.corrieredellosport.it', 'zona': 'Italia', 'activo': True},

    # REGIONALES Y LOCALES
    {'nombre': 'Corriere Milano', 'url': 'https://milano.corriere.it/', 'base': 'https://milano.corriere.it', 'zona': 'Lombardia', 'activo': True},
    {'nombre': 'Repubblica Milano', 'url': 'https://milano.repubblica.it/', 'base': 'https://milano.repubblica.it', 'zona': 'Lombardia', 'activo': True},
    {'nombre': 'Il Giorno', 'url': 'https://www.ilgiorno.it/', 'base': 'https://www.ilgiorno.it', 'zona': 'Lombardia', 'activo': True},
    {'nombre': 'MilanoToday', 'url': 'https://www.milanotoday.it/', 'base': 'https://www.milanotoday.it', 'zona': 'Lombardia', 'activo': True},
    {'nombre': 'BergamoToday', 'url': 'https://www.bergamotoday.it/', 'base': 'https://www.bergamotoday.it', 'zona': 'Lombardia', 'activo': True},
    {'nombre': 'BresciaToday', 'url': 'https://www.bresciatoday.it/', 'base': 'https://www.bresciatoday.it', 'zona': 'Lombardia', 'activo': True},
    {'nombre': 'LeccoToday', 'url': 'https://www.leccotoday.it/', 'base': 'https://www.leccotoday.it', 'zona': 'Lombardia', 'activo': True},
    {'nombre': 'Prima Lodi', 'url': 'https://www.primalodi.it/', 'base': 'https://www.primalodi.it', 'zona': 'Lombardia', 'activo': True},
    {'nombre': 'Repubblica Roma', 'url': 'https://roma.repubblica.it/', 'base': 'https://roma.repubblica.it', 'zona': 'Lazio', 'activo': True},
    {'nombre': 'Il Messaggero Roma', 'url': 'https://www.ilmessaggero.it/roma/', 'base': 'https://www.ilmessaggero.it', 'zona': 'Lazio', 'activo': True},
    {'nombre': 'RomaToday', 'url': 'https://www.romatoday.it/', 'base': 'https://www.romatoday.it', 'zona': 'Lazio', 'activo': True},
    {'nombre': 'Repubblica Veneto', 'url': 'https://www.repubblica.it/veneto/', 'base': 'https://www.repubblica.it', 'zona': 'Veneto', 'activo': True},
    {'nombre': 'Corriere del Veneto', 'url': 'https://corrieredelveneto.corriere.it/', 'base': 'https://corrieredelveneto.corriere.it', 'zona': 'Veneto', 'activo': True},
    {'nombre': 'VeneziaToday', 'url': 'https://www.veneziatoday.it/', 'base': 'https://www.veneziatoday.it', 'zona': 'Veneto', 'activo': True},
    {'nombre': 'VeronaToday', 'url': 'https://www.veronatoday.it/', 'base': 'https://www.veronatoday.it', 'zona': 'Veneto', 'activo': True},
    {'nombre': 'VicenzaToday', 'url': 'https://www.vicenzatoday.it/', 'base': 'https://www.vicenzatoday.it', 'zona': 'Veneto', 'activo': True},
    {'nombre': 'TrevisoToday', 'url': 'https://www.trevisotoday.it/', 'base': 'https://www.trevisotoday.it', 'zona': 'Veneto', 'activo': True},
    {'nombre': 'PadovaOggi', 'url': 'https://www.padovaoggi.it/', 'base': 'https://www.padovaoggi.it', 'zona': 'Veneto', 'activo': True},
    {'nombre': 'Repubblica Bologna', 'url': 'https://bologna.repubblica.it/', 'base': 'https://bologna.repubblica.it', 'zona': 'Emilia-Romagna', 'activo': True},
    {'nombre': 'Il Resto del Carlino Bologna', 'url': 'https://www.ilrestodelcarlino.it/bologna/', 'base': 'https://www.ilrestodelcarlino.it', 'zona': 'Emilia-Romagna', 'activo': True},
    {'nombre': 'BolognaToday', 'url': 'https://www.bolognatoday.it/', 'base': 'https://www.bolognatoday.it', 'zona': 'Emilia-Romagna', 'activo': True},
    {'nombre': 'Repubblica Firenze', 'url': 'https://firenze.repubblica.it/', 'base': 'https://firenze.repubblica.it', 'zona': 'Toscana', 'activo': True},
    {'nombre': 'La Nazione Firenze', 'url': 'https://www.lanazione.it/firenze/', 'base': 'https://www.lanazione.it', 'zona': 'Toscana', 'activo': True},
    {'nombre': 'FirenzeToday', 'url': 'https://www.firenzetoday.it/', 'base': 'https://www.firenzetoday.it', 'zona': 'Toscana', 'activo': True},
    {'nombre': 'PisaToday', 'url': 'https://www.pisatoday.it/', 'base': 'https://www.pisatoday.it', 'zona': 'Toscana', 'activo': True},
    {'nombre': 'LivornoToday', 'url': 'https://www.livornotoday.it/', 'base': 'https://www.livornotoday.it', 'zona': 'Toscana', 'activo': True},
    {'nombre': 'Il Tirreno', 'url': 'https://www.iltirreno.it/', 'base': 'https://www.iltirreno.it', 'zona': 'Toscana', 'activo': True},
    {'nombre': 'Repubblica Napoli', 'url': 'https://napoli.repubblica.it/', 'base': 'https://napoli.repubblica.it', 'zona': 'Campania', 'activo': True},
    {'nombre': 'Il Mattino Napoli', 'url': 'https://www.ilmattino.it/napoli/', 'base': 'https://www.ilmattino.it', 'zona': 'Campania', 'activo': True},
    {'nombre': 'NapoliToday', 'url': 'https://www.napolitoday.it/', 'base': 'https://www.napolitoday.it', 'zona': 'Campania', 'activo': True},
    {'nombre': 'Cronache di Napoli', 'url': 'https://www.cronachenapoli.it/', 'base': 'https://www.cronachenapoli.it', 'zona': 'Campania', 'activo': True},
    {'nombre': 'Giornale di Sicilia', 'url': 'https://gds.it/', 'base': 'https://gds.it', 'zona': 'Sicilia', 'activo': True},
    {'nombre': 'Repubblica Palermo', 'url': 'https://palermo.repubblica.it/', 'base': 'https://palermo.repubblica.it', 'zona': 'Sicilia', 'activo': True},
    {'nombre': 'PalermoToday', 'url': 'https://www.palermotoday.it/', 'base': 'https://www.palermotoday.it', 'zona': 'Sicilia', 'activo': True},
    {'nombre': 'SiracusaToday', 'url': 'https://www.siracusatoday.it/', 'base': 'https://www.siracusatoday.it', 'zona': 'Sicilia', 'activo': True},
    {'nombre': 'Live Sicilia', 'url': 'https://livesicilia.it/cronaca/', 'base': 'https://livesicilia.it', 'zona': 'Sicilia', 'activo': True},
    {'nombre': 'La Sicilia', 'url': 'https://www.lasicilia.it/cronaca/', 'base': 'https://www.lasicilia.it', 'zona': 'Sicilia', 'activo': True},
    {'nombre': 'La Stampa Torino', 'url': 'https://www.lastampa.it/torino/', 'base': 'https://www.lastampa.it', 'zona': 'Piemonte', 'activo': True},
    {'nombre': 'TorinoToday', 'url': 'https://www.torinotoday.it/', 'base': 'https://www.torinotoday.it', 'zona': 'Piemonte', 'activo': True},
    {'nombre': 'GenovaToday', 'url': 'https://www.genovatoday.it/', 'base': 'https://www.genovatoday.it', 'zona': 'Liguria', 'activo': True},
    {'nombre': 'Corriere Adriatico', 'url': 'https://www.corriereadriatico.it/', 'base': 'https://www.corriereadriatico.it', 'zona': 'Marche', 'activo': True},
    {'nombre': 'Il Centro (Abruzzo)', 'url': 'https://www.ilcentro.it/', 'base': 'https://www.ilcentro.it', 'zona': 'Abruzzo', 'activo': True},
    {'nombre': 'La Nuova Sardegna', 'url': 'https://www.lanuovasardegna.it/', 'base': 'https://www.lanuovasardegna.it', 'zona': 'Sardegna', 'activo': True},
    {'nombre': "L'Unione Sarda", 'url': 'https://www.unionesarda.it/', 'base': 'https://www.unionesarda.it', 'zona': 'Sardegna', 'activo': True},
    {'nombre': "L'Adige (Trentino)", 'url': 'https://www.ladige.it/', 'base': 'https://www.ladige.it', 'zona': 'Trentino', 'activo': True},
    {'nombre': 'Alto Adige', 'url': 'https://www.altoadige.it/', 'base': 'https://www.altoadige.it', 'zona': 'Trentino', 'activo': True},
    {'nombre': 'Il Piccolo (Trieste)', 'url': 'https://www.ilpiccolo.it/', 'base': 'https://www.ilpiccolo.it', 'zona': 'Friuli', 'activo': True},
    {'nombre': 'Messaggero Veneto', 'url': 'https://messaggeroveneto.gelocal.it/', 'base': 'https://messaggeroveneto.gelocal.it', 'zona': 'Friuli', 'activo': True},
    {'nombre': 'Gazzetta di Parma', 'url': 'https://www.gazzettadiparma.it/', 'base': 'https://www.gazzettadiparma.it', 'zona': 'Emilia-Romagna', 'activo': True},
    {'nombre': 'Quotidiano di Puglia', 'url': 'https://www.quotidianodipuglia.it/', 'base': 'https://www.quotidianodipuglia.it', 'zona': 'Puglia', 'activo': True},
    {'nombre': 'Gazzetta del Mezzogiorno', 'url': 'https://www.lagazzettadelmezzogiorno.it/', 'base': 'https://www.lagazzettadelmezzogiorno.it', 'zona': 'Puglia', 'activo': True},
]

REGIONES = ['Italia', 'Lombardia', 'Lazio', 'Veneto', 'Emilia-Romagna', 'Toscana', 'Campania', 'Sicilia', 'Piemonte', 'Liguria', 'Marche', 'Abruzzo', 'Sardegna', 'Trentino', 'Friuli', 'Puglia']
ISLAS = REGIONES

# ============================================
# LÉXICO CRIMINAL ITALIANO (ampliado)
# ============================================
DELITOS_ITALIANI = [
    'furto', 'furti', 'ladro', 'rapina', 'truffa', 'violenza', 'aggressione',
    'narcotraffico', 'droga', 'cocaina', 'marijuana', 'omicidio', 'ucciso', 'assassinio',
    'sparatoria', 'estorsione', 'usura', 'riciclaggio', 'corruzione', 'concussione',
    'abuso d\'ufficio', 'peculato', 'mafia', 'camorra', 'ndrangheta', 'cosa nostra',
    'sacra corona unita', 'stidda', 'associazione mafiosa', 'spaccio', 'stupro',
    'violenza sessuale', 'maltrattamenti', 'pedofilia', 'colpo', 'bottino'
]
DELITOS = DELITOS_ITALIANI

# ============================================
# TIPOS DE DELITO
# ============================================
TIPOS_DELITO = {
    'furto': {'icono': '💰', 'color': '#8b0000'},
    'violenza': {'icono': '👊', 'color': '#ff0000'},
    'narcotraffico': {'icono': '💊', 'color': '#4b0082'},
    'truffa': {'icono': '📄', 'color': '#8b6b00'},
    'omicidio': {'icono': '💀', 'color': '#000000'},
    'sessuale': {'icono': '⚠️', 'color': '#660066'},
    'mafia': {'icono': '🐙', 'color': '#990000'},
    'corruzione': {'icono': '💼', 'color': '#cc6600'},
    'altro': {'icono': '❓', 'color': '#666666'}
}

# ============================================
# DETECTOR AUTOMÁTICO DE URLs (MEJORADO)
# ============================================
class DetectorURLs:
    def __init__(self):
        self.archivo_estado = ARCHIVO_ESTADO
        self.estado = self.cargar_estado()
        self.posibles_paths = [
            'cronaca', 'cronaca/', 'cronache', 'cronache/', 'notizie', 'notizie/',
            'cronaca-nera', 'cronaca-nera/', 'criminalita', 'criminalita/',
            'giustizia', 'giustizia/', 'polizia', 'polizia/', 'malavita', 'mafia',
            'camorra', 'ndrangheta', 'omicidi', 'omicidi/'
        ]

    def cargar_estado(self):
        if os.path.exists(self.archivo_estado):
            try:
                with open(self.archivo_estado, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def guardar_estado(self):
        with open(self.archivo_estado, 'w', encoding='utf-8') as f:
            json.dump(self.estado, f, indent=2)

    def encontrar_url_correcta(self, periodico):
        dominio = periodico['base']
        nombre = periodico['nombre']
        if nombre in self.estado and self.estado[nombre].get('url'):
            url_guardada = self.estado[nombre]['url']
            try:
                r = requests.get(url_guardada, timeout=TIMEOUT, headers={'User-Agent': random.choice(USER_AGENTS)})
                if r.status_code == 200:
                    return url_guardada
            except:
                pass
        for path in self.posibles_paths:
            url = f"{dominio}/{path}"
            try:
                r = requests.get(url, timeout=TIMEOUT, headers={'User-Agent': random.choice(USER_AGENTS)})
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    texto = soup.get_text().lower()
                    if any(d in texto for d in DELITOS) or 'cronaca' in texto or 'omicidio' in texto:
                        self.estado[nombre] = {'url': url, 'path': path}
                        self.guardar_estado()
                        return url
            except:
                continue
        return None

    def verificar_todos(self, periodicos):
        cprint(f"\n{'='*70}", 'rojo', negrita=True)
        cprint(f"🔍 VERIFICANDO {len(periodicos)} PERIÓDICOS", 'rojo', negrita=True, fondo=True)
        cprint(f"{'='*70}", 'rojo', negrita=True)
        verificados = []
        activos = 0
        for p in periodicos:
            cprint(f"\n📰 {p['nombre']} ", 'amarillo', negrita=True, fin='')
            try:
                r = requests.get(p['url'], timeout=TIMEOUT, headers={'User-Agent': random.choice(USER_AGENTS)})
                if r.status_code == 200:
                    p['activo'] = True
                    cprint(f"✅ OK", 'verde')
                    activos += 1
                else:
                    nueva_url = self.encontrar_url_correcta(p)
                    if nueva_url:
                        p['url'] = nueva_url
                        p['activo'] = True
                        cprint(f"✅ NUEVA URL", 'verde')
                        activos += 1
                    else:
                        p['activo'] = False
                        cprint(f"❌ No encontrada", 'rojo')
            except:
                nueva_url = self.encontrar_url_correcta(p)
                if nueva_url:
                    p['url'] = nueva_url
                    p['activo'] = True
                    cprint(f"✅ NUEVA URL", 'verde')
                    activos += 1
                else:
                    p['activo'] = False
                    cprint(f"❌ Error conexión", 'rojo')
            verificados.append(p)
            time.sleep(0.8)
        cprint(f"\n{'='*70}", 'verde', negrita=True)
        cprint(f"📊 ACTIVOS: {activos} de {len(periodicos)}", 'verde', negrita=True)
        cprint(f"{'='*70}", 'verde', negrita=True)
        return verificados

# ============================================
# GESTOR DE DATOS
# ============================================
class GestorDatos:
    def __init__(self):
        self.archivo = ARCHIVO
        self.datos = self.cargar()
        self.detector = DetectorURLs()

    def cargar(self):
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {'incidentes': [], 'ultima_actualizacion': None}
        return {'incidentes': [], 'ultima_actualizacion': None}

    def guardar(self):
        self.datos['ultima_actualizacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(self.datos, f, indent=2, ensure_ascii=False)

    def agregar_incidentes(self, nuevos):
        ids_existentes = {inc['id'] for inc in self.datos['incidentes']}
        contador = 0
        for n in nuevos:
            if n['id'] not in ids_existentes:
                self.datos['incidentes'].append(n)
                contador += 1
        if contador:
            self.guardar()
        return contador

    def detectar_tipo(self, texto):
        texto_lower = texto.lower()
        # Mafia y asociaciones criminales
        if any(p in texto_lower for p in ['mafia', 'camorra', 'ndrangheta', 'cosa nostra', 'sacra corona unita', 'stidda', 'associazione mafiosa', '416 bis']):
            return 'mafia'
        # Corrupción y abusos
        if any(p in texto_lower for p in ['corruzione', 'concussione', 'abuso d\'ufficio', 'peculato', 'voto di scambio']):
            return 'corruzione'
        # Narcotráfico
        if any(p in texto_lower for p in ['narcotraffico', 'droga', 'cocaina', 'marijuana', 'spaccio', 'traffico di stupefacenti', 'contrabbando']):
            return 'narcotraffico'
        # Robos y hurtos
        if any(p in texto_lower for p in ['furto', 'furti', 'ladro', 'rapina', 'colpo', 'bottino']):
            return 'furto'
        # Violencia
        if any(p in texto_lower for p in ['violenza', 'aggressione', 'accoltellamento', 'sparatoria', 'tiroteo']):
            return 'violenza'
        # Estafas
        if any(p in texto_lower for p in ['truffa', 'truffe', 'estorsione', 'usura']):
            return 'truffa'
        # Homicidios
        if any(p in texto_lower for p in ['omicidio', 'assassinio', 'ucciso', 'morto ammazzato']):
            return 'omicidio'
        # Delitos sexuales
        if any(p in texto_lower for p in ['stupro', 'violenza sessuale', 'pedofilia', 'maltrattamenti']):
            return 'sessuale'
        return 'altro'

    def estadisticas(self, incidentes=None):
        if incidentes is None:
            incidentes = self.datos['incidentes']
        stats = {
            'total': len(incidentes),
            'islas': defaultdict(int),
            'tipos': defaultdict(int),
            'fuentes': defaultdict(int),
            'municipios': defaultdict(int),
            'ultimos_7dias': 0,
            'ultimos_30dias': 0,
            'ultimos_90dias': 0,
            'tendencia': {}
        }
        hoy = datetime.now()
        hace_7d = (hoy - timedelta(days=7)).strftime('%Y-%m-%d')
        hace_30d = (hoy - timedelta(days=30)).strftime('%Y-%m-%d')
        hace_90d = (hoy - timedelta(days=90)).strftime('%Y-%m-%d')
        for inc in incidentes:
            if inc.get('isla'):
                stats['islas'][inc['isla']] += 1
            if inc.get('tipo'):
                stats['tipos'][inc['tipo']] += 1
            if inc.get('fuente'):
                stats['fuentes'][inc['fuente']] += 1
            fecha = inc.get('fecha', '')
            if fecha >= hace_7d:
                stats['ultimos_7dias'] += 1
            if fecha >= hace_30d:
                stats['ultimos_30dias'] += 1
            if fecha >= hace_90d:
                stats['ultimos_90dias'] += 1
            if fecha and len(fecha) >= 7:
                mes = fecha[:7]
                stats['tendencia'][mes] = stats['tendencia'].get(mes, 0) + 1
        return stats

    def evolucion_mensual(self):
        meses = {}
        for inc in self.datos['incidentes']:
            if inc.get('fecha') and len(inc['fecha']) >= 7:
                mes = inc['fecha'][:7]
                meses[mes] = meses.get(mes, 0) + 1
        return dict(sorted(meses.items()))


# ============================================
# EXTRACTOR DE NOTICIAS (CON BARRA DE PROGRESO)
# ============================================
class ExtractorNoticias:
    def __init__(self, periodicos):
        self.periodicos = periodicos
        self.session = requests.Session()
        self.user_agents = USER_AGENTS
        self.session.headers.update({'User-Agent': random.choice(self.user_agents)})
        self.cache_paginacion = {}
        self.timeout = TIMEOUT

    def _generar_url_pagina(self, url_base, pagina):
        dominio = url_base.split('/')[2] if '//' in url_base else url_base
        if dominio in self.cache_paginacion:
            formato = self.cache_paginacion[dominio]
            return formato.format(pagina=pagina)
        formatos = [
            f"{url_base}pagina/{{pagina}}/", f"{url_base}?page={{pagina}}", f"{url_base}{{pagina}}/",
            f"{url_base}page/{{pagina}}/", f"{url_base}index.php?page={{pagina}}", f"{url_base}listado?pag={{pagina}}",
            f"{url_base}?pag={{pagina}}", f"{url_base}?p={{pagina}}"
        ]
        for formato in formatos:
            url = formato.format(pagina=pagina)
            try:
                r = self.session.get(url, timeout=self.timeout)
                if r.status_code == 200 and len(r.text) > 500:
                    self.cache_paginacion[dominio] = formato
                    return url
            except:
                continue
        return None

    def buscar_todo(self, paginas=10):
        cprint(f"\n{'='*80}", 'rojo', negrita=True)
        cprint(f"🔥 BÚSQUEDA EN {len(self.periodicos)} PERIÓDICOS", 'rojo', negrita=True, fondo=True)
        cprint(f"{'='*80}", 'rojo', negrita=True)

        todas = []
        periodicos_activos = [p for p in self.periodicos if p.get('activo', True)]
        total_activos = len(periodicos_activos)
        if total_activos == 0:
            cprint(f"\n⚠️ No hay periódicos activos. Ejecuta verificación primero.", 'amarillo')
            return todas

        cprint(f"\n📊 Periódicos activos: {total_activos}\n", 'cian')

        # Barra de progreso
        for idx, periodico in enumerate(periodicos_activos, 1):
            porcentaje = (idx / total_activos) * 100
            barra = '█' * int(porcentaje // 2) + '░' * (50 - int(porcentaje // 2))
            sys.stdout.write(f"\r   📰 Progreso: [{barra}] {idx}/{total_activos} ({porcentaje:.1f}%)")
            sys.stdout.flush()

            cprint(f"\n📰 {periodico['nombre']}", 'amarillo', negrita=True)
            cprint(f"   Región: {periodico['zona']}", 'gris')

            encontrados = 0
            for pagina in range(1, paginas + 1):
                url = self._generar_url_pagina(periodico['url'], pagina)
                if not url:
                    if pagina == 1:
                        cprint(f"   📄 Página {pagina}... ✗ No accesible", 'rojo')
                    else:
                        cprint(f"   📄 Página {pagina}... ✗ No hay más", 'amarillo')
                    break
                try:
                    cprint(f"   📄 Página {pagina}... ", 'gris', fin='')
                    r = self.session.get(url, timeout=self.timeout)
                    if r.status_code == 200:
                        soup = BeautifulSoup(r.text, 'html.parser')
                        articulos = []
                        articulos.extend(soup.find_all('article'))
                        articulos.extend(soup.find_all('div', class_=lambda x: x and ('article' in x or 'noticia' in x)))
                        articulos.extend(soup.find_all('h2'))
                        encontrados_pagina = 0
                        for art in articulos[:20]:
                            titulo_elem = art.find(['h2', 'h3']) if art.name != 'h2' else art
                            if not titulo_elem:
                                continue
                            titulo = titulo_elem.get_text().strip()
                            if len(titulo) < 20:
                                continue
                            titulo_lower = titulo.lower()
                            if any(d in titulo_lower for d in DELITOS):
                                region = periodico['zona']
                                for r in REGIONES:
                                    if r.lower() in titulo_lower:
                                        region = r
                                        break
                                fecha_elem = art.find('time')
                                fecha = datetime.now().strftime('%Y-%m-%d')
                                if fecha_elem and fecha_elem.get('datetime'):
                                    fecha = fecha_elem.get('datetime')[:10]
                                gestor_temp = GestorDatos()
                                tipo = gestor_temp.detectar_tipo(titulo)
                                todas.append({
                                    'id': hashlib.md5(f"{titulo}_{periodico['nombre']}".encode()).hexdigest()[:16],
                                    'titulo': titulo[:300],
                                    'fecha': fecha,
                                    'isla': region,
                                    'tipo': tipo,
                                    'fuente': periodico['nombre']
                                })
                                encontrados_pagina += 1
                                encontrados += 1
                        cprint(f"✓ {encontrados_pagina}", 'verde')
                        if encontrados_pagina == 0 and pagina > 1:
                            break
                    elif r.status_code == 404:
                        cprint(f"✗ No existe (404)", 'amarillo')
                        break
                    else:
                        cprint(f"✗ Error {r.status_code}", 'rojo')
                except Exception as e:
                    cprint(f"✗ Error", 'rojo')
                time.sleep(TIEMPO_ESPERA)
            time.sleep(0.5)

        print()  # salto de línea después de la barra

        # Eliminar duplicados
        unicos = {}
        for n in todas:
            key = n['id']
            if key not in unicos:
                unicos[key] = n

        cprint(f"\n{'='*80}", 'verde', negrita=True)
        cprint(f"📊 TOTAL: {len(unicos)} noticias únicas de {total_activos} periódicos activos", 'verde', negrita=True)
        cprint(f"{'='*80}", 'verde', negrita=True)

        return list(unicos.values())

# ============================================
# HTML TEMPLATE (versión corregida)
# ============================================

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>🔥 DIABOLIC ITALIA v{{ version }}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #0a0a0a; color: #fff; font-family: 'Segoe UI', Arial; padding: 20px; }
        .container { max-width: 1400px; margin: 0 auto; }
        @keyframes neonPulse {
            0% { text-shadow: 0 0 5px #00ff00, 0 0 10px #00cc00; opacity: 1; }
            100% { text-shadow: 0 0 2px #00ff00, 0 0 5px #00cc00; opacity: 0.9; }
        }
        .neon-header { font-family: 'Arial Black', sans-serif; font-size: 3.5em; color: #fff; animation: neonPulse 1.5s infinite alternate; text-align: center; margin-bottom: 20px; }
        .header { background: linear-gradient(135deg, #1a1a1a, #330000, #660000); padding: 30px; border-radius: 30px; text-align: center; margin-bottom: 30px; box-shadow: 0 0 40px rgba(0,150,0,0.3); border: 1px solid #00aa00; }
        .version-badge { background: black; color: #00ff00; padding: 5px 20px; border-radius: 50px; display: inline-block; margin-top: 10px; font-family: monospace; }
        .stats-header { display: flex; justify-content: center; gap: 20px; margin: 20px 0; flex-wrap: wrap; }
        .stat-header-item { background: rgba(0,0,0,0.7); padding: 10px 25px; border-radius: 50px; border: 1px solid #00aa00; font-weight: bold; }
        .btn { background: #006600; color: white; border: none; padding: 15px 40px; border-radius: 50px; font-size: 1.2em; cursor: pointer; margin: 10px; border: 2px solid #00aa00; font-weight: bold; }
        .btn:hover { background: #008800; transform: scale(1.02); }
        .config-btn { background: #1a1a1a; color: #00ffaa; border: 2px solid #006600; padding: 12px 25px; border-radius: 40px; cursor: pointer; margin: 10px; display: inline-flex; align-items: center; gap: 10px; text-decoration: none; font-weight: bold; }
        .config-btn:hover { background: #006600; color: white; }
        .filtros { display: flex; gap: 10px; justify-content: center; margin: 20px 0; flex-wrap: wrap; }
        .filtro-btn { background: #1a1a1a; color: white; border: 2px solid #006600; padding: 10px 20px; border-radius: 30px; text-decoration: none; font-weight: bold; }
        .filtro-btn:hover, .filtro-btn.activo { background: #006600; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }
        .stat-card { background: #1a1a1a; padding: 25px; border-radius: 15px; border-left: 8px solid #00aa00; text-align: center; box-shadow: 0 0 10px rgba(0,150,0,0.2); }
        .stat-number { font-size: 3em; color: #00ff00; font-weight: bold; }
        .analysis-section { background: #1a1a1a; border-radius: 20px; padding: 25px; margin: 30px 0; border: 1px solid #006600; }
        .section-title { color: #00ff00; font-size: 1.8em; margin-bottom: 20px; border-bottom: 2px solid #006600; padding-bottom: 10px; font-family: monospace; }
        .chart-bar-bg { width: 100%; height: 25px; background: #2a2a2a; border-radius: 12px; margin: 10px 0; overflow: hidden; }
        .chart-bar-fill { height: 100%; background: linear-gradient(90deg, #006600, #00aa00); border-radius: 12px; transition: width 0.5s; }
        .chart-label { display: flex; justify-content: space-between; color: #ccffcc; margin: 5px 0; font-weight: bold; }
        .incidente-card { background: #1a1a1a; margin: 15px 0; padding: 20px; border-radius: 12px; border-left: 10px solid #00aa00; transition: 0.2s; }
        .incidente-card:hover { background: #2a2a2a; }
        .incidente-titolo { font-size: 1.2em; font-weight: bold; margin-bottom: 10px; color: #fff; }
        .incidente-meta { color: #aaa; display: flex; gap: 20px; flex-wrap: wrap; margin-top: 8px; font-size: 0.9em; }
        .regione-badge { background: #006600; color: white; padding: 3px 12px; border-radius: 20px; font-size: 0.9em; font-weight: bold; }
        .footer { text-align: center; margin-top: 40px; padding: 20px; background: #1a1a1a; border-radius: 15px; color: #006600; border: 1px solid #006600; }
        a { text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="neon-header">🔥 DIABOLIC ITALIA 🔥</h1>
            <div class="version-badge">v{{ version }} · Porta {{ puerto }}</div>
            <div class="stats-header">
                <div class="stat-header-item">📊 {{ total_incidenti }} incidenti</div>
                <div class="stat-header-item">📰 {{ total_fonti }} fonti</div>
                <div class="stat-header-item">🏛️ {{ total_regioni }} regioni</div>
            </div>
        </div>
        <div style="text-align: center;">
            <form action="/aggiorna" method="post" style="display: inline;"><button class="btn">🔥 AGGIORNA</button></form>
            <a href="/esporta/json" class="config-btn">📥 JSON</a>
            <a href="/esporta/csv" class="config-btn">📥 CSV</a>
        </div>
        <div class="filtros">
            <a href="/" class="filtro-btn {% if filtro == 'tutti' %}activo{% endif %}">TUTTI</a>
            <a href="/filtro/7d" class="filtro-btn {% if filtro == '7d' %}activo{% endif %}">7 GIORNI</a>
            <a href="/filtro/30d" class="filtro-btn {% if filtro == '30d' %}activo{% endif %}">30 GIORNI</a>
            <a href="/filtro/90d" class="filtro-btn {% if filtro == '90d' %}activo{% endif %}">90 GIORNI</a>
        </div>
        <div class="stats-grid">
            <div class="stat-card"><div>TOTALE</div><div class="stat-number">{{ stats.totale }}</div></div>
            <div class="stat-card"><div>ULTIMI 7gg</div><div class="stat-number">{{ stats.ultimi_7gg }}</div></div>
            <div class="stat-card"><div>ULTIMI 30gg</div><div class="stat-number">{{ stats.ultimi_30gg }}</div></div>
            <div class="stat-card"><div>ULTIMI 90gg</div><div class="stat-number">{{ stats.ultimi_90gg }}</div></div>
        </div>
        <div class="analysis-section">
            <div class="section-title">📍 PER REGIONE</div>
            {% set totale_regioni = stats.regioni.values()|sum %}
            {% for regione, quantita in stats.regioni.items() %}
            <div class="chart-label"><span>🇮🇹 {{ regione }}</span><span>{{ quantita }} ({{ (quantita / totale_regioni * 100)|round(1) }}%)</span></div>
            <div class="chart-bar-bg"><div class="chart-bar-fill" style="width: {{ (quantita / totale_regioni * 100) }}%;"></div></div>
            {% endfor %}
        </div>
        <div class="analysis-section">
            <div class="section-title">🔍 TIPO DI REATO</div>
            {% set totale_tipi = stats.tipi.values()|sum %}
            {% for tipo, quantita in stats.tipi.items() %}
            {% set dati = TIPOS_DELITO.get(tipo, {'icono': '❓', 'colore': '#666'}) %}
            <div class="chart-label"><span><span style="color: {{ dati.colore }};">{{ dati.icono }}</span> {{ tipo|upper }}</span><span>{{ quantita }} ({{ (quantita / totale_tipi * 100)|round(1) }}%)</span></div>
            <div class="chart-bar-bg"><div class="chart-bar-fill" style="width: {{ (quantita / totale_tipi * 100) }}%;"></div></div>
            {% endfor %}
        </div>
        <div class="analysis-section">
            <div class="section-title">📰 ULTIMI INCIDENTI ({{ incidenti|length }})</div>
            {% for inc in incidenti[:25] %}
            {% set tipo_colore = TIPOS_DELITO.get(inc.tipo, {'colore': '#666'}).colore %}
            <div class="incidente-card" style="border-left-color: {{ tipo_colore }};">
                <div class="incidente-titolo">{{ inc.titolo }}</div>
                <div class="incidente-meta">
                    <span class="regione-badge">🏛️ {{ inc.regione or '?' }}</span>
                    <span>📅 {{ inc.data }}</span>
                    <span>📰 {{ inc.fonte }}</span>
                    <span>🔍 {{ inc.tipo|upper }}</span>
                </div>
            </div>
            {% endfor %}
        </div>
        <div class="footer">
            <p>🔥 DIABOLIC ITALIA v{{ version }} · {{ periodici_attivi }} FONTI ATTIVE · 100% LEGALE</p>
            <p style="font-size:0.8em; color:#666;">"Un grande potere comporta una grande responsabilità"</p>
        </div>
    </div>
</body>
</html>
'''

# ============================================
# APP FLASK
# ============================================
app = Flask(__name__)

@app.route('/')
def home():
    global gestore, IDIOMA_ACTUAL
    incidenti = gestore.dati['incidenti']
    stats = gestore.statistiche()
    periodici_attivi = len([p for p in PERIODICOS_BASE if p.get('activo', True)])
    return render_template_string(
        HTML_TEMPLATE,
        version=VERSION,
        puerto=PUERTO,
        stats=stats,
        incidenti=incidenti[::-1],
        total_incidenti=stats['total'],
        total_fonti=len(stats['fuentes']),
        total_regioni=len(stats['islas']),
        periodici_attivi=periodici_attivi,
        TIPOS_DELITO=TIPOS_DELITO,
        filtro='tutti'
    )

@app.route('/filtro/<periodo>')
def filtro(periodo):
    global gestore, IDIOMA_ACTUAL
    incidenti = gestore.dati['incidenti']
    oggi = datetime.now()
    if periodo == '7d':
        limite = (oggi - timedelta(days=7)).strftime('%Y-%m-%d')
        incidenti = [i for i in incidenti if i.get('fecha', '') >= limite]
    elif periodo == '30d':
        limite = (oggi - timedelta(days=30)).strftime('%Y-%m-%d')
        incidenti = [i for i in incidenti if i.get('fecha', '') >= limite]
    elif periodo == '90d':
        limite = (oggi - timedelta(days=90)).strftime('%Y-%m-%d')
        incidenti = [i for i in incidenti if i.get('fecha', '') >= limite]
    stats = gestore.statistiche(incidenti)
    periodici_attivi = len([p for p in PERIODICOS_BASE if p.get('activo', True)])
    return render_template_string(
        HTML_TEMPLATE,
        version=VERSION,
        puerto=PUERTO,
        stats=stats,
        incidenti=incidenti[::-1],
        total_incidenti=stats['total'],
        total_fonti=len(stats['fuentes']),
        total_regioni=len(stats['islas']),
        periodici_attivi=periodici_attivi,
        TIPOS_DELITO=TIPOS_DELITO,
        filtro=periodo
    )

@app.route('/aggiorna', methods=['POST'])
def aggiorna():
    global gestore
    cprint(f"\n{'='*80}", 'rojo', negrita=True)
    cprint(f"🔥 AGGIORNAMENTO NOTIZIE", 'rojo', negrita=True, fondo=True)
    cprint(f"{'='*80}", 'rojo', negrita=True)
    periodici = gestore.detector.verificar_todos(PERIODICOS_BASE)
    estrattore = ExtractorNoticias(periodici)
    nuove = estrattore.buscar_todo(pagine=PAGINAS_BUSQUEDA)
    aggiunte = gestore.agregar_incidentes(nuove)
    cprint(f"\n{'='*80}", 'verde', negrita=True)
    cprint(f"✅ {aggiunte} NUOVE NOTIZIE", 'verde', negrita=True, fondo=True)
    cprint(f"{'='*80}", 'verde', negrita=True)
    return home()

@app.route('/esporta/json')
def esporta_json():
    global gestore
    return jsonify(gestore.datos)

@app.route('/esporta/csv')
def esporta_csv():
    global gestore
    import csv
    from io import StringIO
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Titolo', 'Data', 'Regione', 'Tipo', 'Fonte'])
    for inc in gestore.dati['incidenti']:
        cw.writerow([inc['titolo'], inc['fecha'], inc.get('isla', ''), inc.get('tipo', ''), inc['fuente']])
    return si.getvalue()

# ============================================
# MENÚ TERMINAL (10 comandos)
# ============================================
def menu():
    global gestor
    while True:
        print(f"\n{Color.ROJO}{'═'*90}{Color.RESET}")
        print(f"{Color.FONDO_ROJO}{Color.NEGRITA}{t('app_name')} v{VERSION} - PUERTO {PUERTO}{Color.RESET}")
        print(f"{Color.ROJO}{'═'*90}{Color.RESET}")

        stats = gestor.estadisticas()
        periodicos_activos = len([p for p in PERIODICOS_BASE if p.get('activo', True)])

        print(f"\n{Color.VERDE}📊 {t('stats_total')}: {stats['total']} {t('incidentes')}{Color.RESET}")
        if stats['total'] > 0:
            pct_7d = round((stats['ultimos_7dias'] / stats['total'] * 100), 1)
        else:
            pct_7d = 0
        print(f"   ⚡ Últimos 7 días: {stats['ultimos_7dias']} ({pct_7d}% del total)")
        print(f"   🔥 Últimos 30 días: {stats['ultimos_30dias']}")
        print(f"   📆 Últimos 90 días: {stats['ultimos_90dias']}")
        print(f"   🏛️ Regiones activas: {len(stats['islas'])}")
        print(f"   📰 {t('fuentes')}: {periodicos_activos}")

        print(f"\n{Color.AMARILLO}📋 {t('menu_title')}:{Color.RESET}")
        print(f"{Color.ROJO}[1]{Color.RESET} {t('cmd_buscar')}")
        print(f"{Color.ROJO}[2]{Color.RESET} {t('cmd_analisis')}")
        print(f"{Color.ROJO}[3]{Color.RESET} {t('cmd_conexiones')}")
        print(f"{Color.ROJO}[4]{Color.RESET} {t('cmd_evolucion')}")
        print(f"{Color.ROJO}[5]{Color.RESET} {t('cmd_web')}")
        print(f"{Color.ROJO}[6]{Color.RESET} {t('cmd_ultimos')}")
        print(f"{Color.ROJO}[7]{Color.RESET} {t('cmd_exportar')}")
        print(f"{Color.ROJO}[8]{Color.RESET} {t('cmd_verificar')}")
        print(f"{Color.ROJO}[9]{Color.RESET} {t('cmd_tipos')}")
        print(f"{Color.ROJO}[10]{Color.RESET} {t('cmd_salir')}")

        op = input(f"\n{Color.ROJO}➤ Opción: {Color.RESET}")

        if op == '1':
            periodicos = gestor.detector.verificar_todos(PERIODICOS_BASE)
            extractor = ExtractorNoticias(periodicos)
            nuevas = extractor.buscar_todo(paginas=PAGINAS_BUSQUEDA)
            agregadas = gestor.agregar_incidentes(nuevas)
            cprint(f"\n✅ {agregadas} nuevas noticias", 'verde', negrita=True)
            input(f"\n{Color.GRIS}Enter para continuar...{Color.RESET}")

        elif op == '2':
            stats = gestor.estadisticas()
            print(f"\n{Color.ROJO}{'═'*70}{Color.RESET}")
            print(f"{Color.AMARILLO}📊 ANÁLISIS COMPLETO{Color.RESET}")
            print(f"{Color.ROJO}{'═'*70}{Color.RESET}")

            print(f"\n{Color.VERDE}📈 TENDENCIAS:{Color.RESET}")
            print(f"   Total histórico: {stats['total']}")
            if stats['total'] > 0:
                pct_7d = round((stats['ultimos_7dias'] / stats['total'] * 100), 1)
                pct_30d = round((stats['ultimos_30dias'] / stats['total'] * 100), 1)
                pct_90d = round((stats['ultimos_90dias'] / stats['total'] * 100), 1)
            else:
                pct_7d = pct_30d = pct_90d = 0
            print(f"   Últimos 7 días: {stats['ultimos_7dias']} ({pct_7d}%)")
            print(f"   Últimos 30 días: {stats['ultimos_30dias']} ({pct_30d}%)")
            print(f"   Últimos 90 días: {stats['ultimos_90dias']} ({pct_90d}%)")

            print(f"\n{Color.VERDE}📍 DISTRIBUCIÓN POR REGIONES:{Color.RESET}")
            for reg, cant in sorted(stats['islas'].items(), key=lambda x: x[1], reverse=True):
                pct = round((cant / stats['total'] * 100), 1) if stats['total'] > 0 else 0
                print(f"   {reg}: {cant} ({pct}%)")

            print(f"\n{Color.VERDE}🔍 DISTRIBUCIÓN POR TIPO:{Color.RESET}")
            for tipo, cant in sorted(stats['tipos'].items(), key=lambda x: x[1], reverse=True):
                pct = round((cant / stats['total'] * 100), 1) if stats['total'] > 0 else 0
                print(f"   {tipo.upper()}: {cant} ({pct}%)")

            input(f"\n{Color.GRIS}Enter para continuar...{Color.RESET}")

        elif op == '3':
            print(f"\n{Color.ROJO}{'═'*70}{Color.RESET}")
            print(f"{Color.AMARILLO}🔗 CONEXIONES ENTRE INCIDENTES{Color.RESET}")
            print(f"{Color.ROJO}{'═'*70}{Color.RESET}")

            incidentes = gestor.datos['incidentes'][-150:]
            if len(incidentes) < 10:
                print(f"{Color.GRIS}   Datos insuficientes. Realiza más búsquedas.{Color.RESET}")
                input(f"\n{Color.GRIS}Enter...{Color.RESET}")
                continue

            grupos = defaultdict(list)
            hace_30d = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            for inc in incidentes:
                if inc.get('fecha', '') >= hace_30d:
                    clave = (inc.get('tipo', 'otro'), inc.get('isla', 'Desconocida'))
                    grupos[clave].append(inc)

            patrones = 0
            for (tipo, region), lista in grupos.items():
                if len(lista) >= 3:
                    print(f"\n{Color.ROJO}🔥 PATRÓN: {len(lista)} {tipo.upper()} en {region}{Color.RESET}")
                    for inc in sorted(lista, key=lambda x: x['fecha'], reverse=True)[:3]:
                        print(f"   • {inc['fecha']}: {inc['titulo'][:80]}...")
                    fechas = [inc['fecha'] for inc in lista]
                    if fechas:
                        try:
                            dias = (datetime.now() - datetime.strptime(min(fechas), '%Y-%m-%d')).days
                            if dias > 0:
                                freq = round(len(lista) / dias, 1)
                                print(f"   ⚡ Frecuencia: {freq} incidentes/día")
                        except:
                            pass
                    patrones += 1

            print(f"\n{Color.AMARILLO}🔍 PALABRAS CLAVE DESTACADAS:{Color.RESET}")
            palabras_clave = ['mafia', 'camorra', 'ndrangheta', 'omicidio', 'droga', 'cocaina', 'estorsione', 'spaccio']
            for palabra in palabras_clave:
                relacionados = [inc for inc in incidentes if palabra in inc['titulo'].lower()]
                if len(relacionados) >= 2:
                    print(f"\n   {Color.ROJO}• {palabra.upper()}: {len(relacionados)} incidentes{Color.RESET}")
                    for inc in relacionados[:2]:
                        print(f"     - {inc['fecha']} ({inc['isla']}): {inc['titulo'][:60]}...")

            if patrones == 0:
                print(f"\n{Color.GRIS}   No se detectaron patrones significativos en los últimos 30 días.{Color.RESET}")

            input(f"\n{Color.GRIS}Enter...{Color.RESET}")

        elif op == '4':
            evolucion = gestor.evolucion_mensual()
            print(f"\n{Color.ROJO}{'═'*70}{Color.RESET}")
            print(f"{Color.AMARILLO}📈 EVOLUCIÓN MENSUAL{Color.RESET}")
            print(f"{Color.ROJO}{'═'*70}{Color.RESET}")
            for mes, cant in list(evolucion.items())[-12:]:
                print(f"   {mes}: {cant} incidentes")
            if not evolucion:
                print("   No hay datos suficientes.")
            input(f"\n{Color.GRIS}Enter...{Color.RESET}")

        elif op == '5':
            cprint(f"\n🌐 {t('servidor_web')}: http://localhost:{PUERTO}", 'verde', negrita=True)
            cprint(f"   {t('presiona_ctrl_c')}", 'gris')
            app.run(host='0.0.0.0', port=PUERTO, debug=False)

        elif op == '6':
            incidentes = gestor.datos['incidentes'][-20:][::-1]
            print(f"\n{Color.ROJO}{'═'*70}{Color.RESET}")
            print(f"{Color.AMARILLO}📰 ÚLTIMOS 20 INCIDENTES{Color.RESET}")
            print(f"{Color.ROJO}{'═'*70}{Color.RESET}")
            for i, inc in enumerate(incidentes, 1):
                print(f"\n{Color.ROJO}{i:2d}.{Color.RESET} {inc['titulo'][:100]}...")
                print(f"      {inc['fecha']} | {inc.get('isla', '?')} | {inc['fuente']} | {inc.get('tipo', '?')}")
            if not incidentes:
                print("   No hay incidentes registrados.")
            input(f"\n{Color.GRIS}Enter...{Color.RESET}")

        elif op == '7':
            with open('export_italia.json', 'w', encoding='utf-8') as f:
                json.dump(gestor.datos, f, indent=2, ensure_ascii=False)
            with open('export_italia.csv', 'w', encoding='utf-8') as f:
                f.write("Título,Fecha,Región,Tipo,Fuente\n")
                for inc in gestor.datos['incidentes']:
                    f.write(f"{inc['titulo'][:100].replace(',', ' ')},{inc['fecha']},{inc.get('isla','')},{inc.get('tipo','')},{inc['fuente']}\n")
            cprint(f"\n✅ Exportados export_italia.json y export_italia.csv", 'verde')
            input(f"\n{Color.GRIS}Enter...{Color.RESET}")

        elif op == '8':
            gestor.detector.verificar_todos(PERIODICOS_BASE)
            input(f"\n{Color.GRIS}Enter...{Color.RESET}")

        elif op == '9':
            stats = gestor.estadisticas()
            print(f"\n{Color.ROJO}{'═'*70}{Color.RESET}")
            print(f"{Color.AMARILLO}📊 DISTRIBUCIÓN POR TIPO{Color.RESET}")
            print(f"{Color.ROJO}{'═'*70}{Color.RESET}")
            for tipo, cant in sorted(stats['tipos'].items(), key=lambda x: x[1], reverse=True):
                pct = round((cant / stats['total'] * 100), 1) if stats['total'] > 0 else 0
                barra = '█' * int(pct // 2) + '░' * (50 - int(pct // 2))
                print(f"   {tipo}: [{barra}] {cant} ({pct}%)")
            input(f"\n{Color.GRIS}Enter...{Color.RESET}")

        elif op == '10':
            cprint(f"\n👋 {t('hasta_pronto')}", 'rojo', negrita=True)
            break

        else:
            cprint(f"\n❌ {t('opcion_invalida')}", 'rojo')
            time.sleep(1)


# ============================================
# MAIN
# ============================================
if __name__ == '__main__':
    seleccionar_idioma()

    print(f"""
{Color.ROJO}
╔══════════════════════════════════════════════════════════════════╗
║  🔥 DIABOLIC ITALIA v{VERSION} - 70+ PERIÓDICOS 🔥                       ║
║  ⚡ CRONACA NERA · MAFIA · NARCOTRAFFICO · VIOLENZA               ║
║  🏛️ TODAS LAS REGIONES · 70+ FUENTES · ALERTAS EN TIEMPO REAL      ║
║                                         - By Condor2026          ║
║                                            •SpectrumSecurity•    ║
╚══════════════════════════════════════════════════════════════════╝
{Color.RESET}""")
    print(f"{Color.GRIS}🕷️  \"Un gran poder conlleva una gran responsabilidad\" - Spider-Man{Color.RESET}")
    print(f"{Color.GRIS}⚖️  Uso ético y legal. Solo datos públicos.{Color.RESET}")
    print(f"{Color.CIAN}🔥 Especializado en: cronaca nera, omicidi, mafia, camorra,{Color.RESET}")
    print(f"{Color.CIAN}   ndrangheta, narcotraffico, rapine e crimine organizzato.{Color.RESET}")

    gestor = GestorDatos()
    stats = gestor.estadisticas()
    print(f"{Color.VERDE}📊 Incidentes en base: {stats['total']}{Color.RESET}")
    print(f"{Color.AMARILLO}⏳ Última actualización: {gestor.datos.get('ultima_actualizacion', 'Nunca')}{Color.RESET}")

    print(f"\n{Color.CIAN}¿Cómo quieres ejecutar?{Color.RESET}")
    print(f"{Color.ROJO}1.{Color.RESET} Modo terminal (10 comandos)")
    print(f"{Color.ROJO}2.{Color.RESET} Modo web directo")

    modo = input(f"\n{Color.ROJO}➤ Elige: {Color.RESET}")

    if modo == '2':
        cprint(f"\n🌐 {t('servidor_web')}: http://localhost:{PUERTO}", 'verde', negrita=True)
        cprint(f"   {t('presiona_ctrl_c')}", 'gris')
        app.run(host='0.0.0.0', port=PUERTO, debug=True)
    else:
        menu()
