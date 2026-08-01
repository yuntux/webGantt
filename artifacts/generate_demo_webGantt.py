"""
Script d'automatisation de démonstration vidéo - Projet WebGantt

Ce script permet de générer une vidéo de démonstration en combinant :
1. Narration audio (Kokoro TTS, local et gratuit)
2. Capture vidéo automatisée (Playwright)
3. Montage automatique (MoviePy)

ETAPES DE LA PRODUCION APPUYEE SUR UN LLM :
--------------------------------------------
Pré-requis : l'application est développée, le jeu de données de démo existe, 
la documentation du projet est rédigée.

1. Envoyer au LLM la documentation du projet : "J'ai construit une web app locale 
qui tient dans un fichier HTML. Je veux générer une vidéo de démonstration de 1 à 2 minutes
 avec une voix off en anglais. Voici la documentation du projet en PJ.
 Rédige moi le tableau de minutage de la démonstration avec les 3 colonnes suivantes :
 1/ le minutage 2/ l'action à réaliser visuellement par l'utilisateur 3/ le texte de la
  voix off "

2. Envoyer au LLM le tableau de minutage généré par le LLM, ainsi que ce sript, 
et lui demander : "Voici le tableau de minutage, adapte le script python ci-joint 
pour qu'il corresponde au tableau de minutage et aux actions à réaliser. 
Les sélecteurs CSS doivent être des placeholder à remplacer par les vrais "clics" 
à l'étape suivante."

3. Envoyer au LLM : "Voici le script de génération vidéo ainsi que le fichier de HTML
de l'application ciblée par la démo, ainsi que le fichier demo. Adapte le script pour 
intégrer les sélecteurs CSS et les actions à réaliser."

INSTALLATION DES DEPENDANCES :
------------------------------
# Dépendances système : ffmpeg (requis par MoviePy), polices DejaVu (page de garde), espeak-ng (fallback phonémisation Kokoro)
sudo apt update && sudo apt install -y python3-pip python3-venv ffmpeg fonts-dejavu-core espeak-ng

# Dépendances Python
pip install playwright moviepy kokoro soundfile numpy --break-system-packages

# Navigateur Chromium pour Playwright + ses dépendances système
playwright install --with-deps chromium


EXECUTION DU SCRIPT :
---------------------
# Mode complet (capture Playwright + génération audio Kokoro + montage)
python3 generate_demo_webgantt.py

# Mode montage seul (réutilise la dernière capture vidéo, ne relance pas Playwright)
python3 generate_demo_webgantt.py --assemble-only



STRUCTURE DU SCRIPT :
--------------------
- CONFIGURATION : Chemins, URL locale de l'app WebGantt, réglages Kokoro.
- AUDIO : Génération des segments WAV à partir du dictionnaire 'script_segments'
          via Kokoro (aucune clé API, aucun quota).
- CAPTURE :
    - Injection d'un curseur rouge (JS) pour la visibilité des clics.
    - SyncNarrator : Classe assurant que l'audio et la vidéo restent synchronisés.
    - Logique métier : Parcours utilisateur automatisé dans WebGantt.
      ⚠️  Les sélecteurs CSS ci-dessous sont des PLACEHOLDERS (TODO) à remplacer
          par les vrais sélecteurs de webGantt.html une fois qu'on les aura identifiés.
- MONTAGE :
    - create_title_card : Génère une slide d'intro.
    - assemble : Assemble les clips et mixe l'audio en respectant les timestamps réels.

"""
import os
import asyncio
import time
import subprocess
import sys
import hashlib
import json
import socket
from datetime import datetime
from pathlib import Path

import moviepy as mp
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont

# --- CONFIGURATION GÉNÉRALE ---
BASE_DIR = Path(__file__).parent.absolute()
ROOT_DIR = BASE_DIR.parent
AUDIO_DIR = BASE_DIR / "temp_audio"
VIDEO_DIR = BASE_DIR / "temp_video"
AUDIO_DIR.mkdir(exist_ok=True)
VIDEO_DIR.mkdir(exist_ok=True)

WEBGANTT_HTML_PATH = ROOT_DIR / "webGantt.html"
EXAMPLE_GAN_PATH = ROOT_DIR / "specs/001-ganttproject-features/assets/example.gan"

# WebGantt est 100% client-side : pas de backend à démarrer.
# On peut ouvrir le fichier directement en file:// avec Playwright.
BASE_URL = f"file://{WEBGANTT_HTML_PATH}"

# --- CONFIGURATION DE L'APPLICATION (page de garde) ---
APP_SETTINGS = {
    "title": "webGantt",
    "subtitle": "A lightweight, 100% browser-based\nGantt chart application",
    "bg_color": (255, 255, 255),     # Blanc
    "accent_color": (9, 105, 218),   # Bleu
    "footer_tagline": "Open Source \u2022 No install \u2022 No server",
    # Pas de backend/frontend à lancer : WebGantt tourne dans un seul fichier HTML.
    "services": [],
}

# --- CONFIGURATION KOKORO ONNX (TTS local, gratuit) ---
KOKORO_LANG = "en-us"        # Langue : "en-us", "en-gb", "fr-fr"...
KOKORO_VOICE = "am_adam"     # Voix : "am_adam" (EN-US), "af_bella" (EN-US), "ff_siwis" (FR-FR)...
KOKORO_SAMPLE_RATE = 24000

# --- SEGMENTS DE VOIX OFF (script de la démo) ---
script_segments = [
    {
        "id": "01_intro",
        "text": "Meet WebGantt — a Gantt chart app that lives entirely in your browser. No install, no server, no backend. Just open the HTML file, and you're ready to plan. WebGantt speaks the same language as GanttProject, the open source project management tool used for over twenty years."
    },
    {
        "id": "02_open_file",
        "text": "Click Open, pick a dot-gan file, and your entire project — tasks, resources, dependencies — loads instantly."
    },
    {
        "id": "03_wbs",
        "text": "On the left, the Work Breakdown Structure lets you build your task hierarchy. Add a task, indent it to create a phase, drag and drop to reorder. Double-click any field to edit it inline."
    },
    {
        "id": "04_dependencies",
        "text": "On the right, the timeline brings your schedule to life. Link tasks to create dependencies, and watch WebGantt recalculate the entire schedule automatically when something shifts."
    },
    {
        "id": "05_critical_path",
        "text": "Turn on the critical path to see exactly which tasks control your deadline. Zoom in for a detailed daily view, or zoom out to see months and years at a glance."
    },
    {
        "id": "06_resources",
        "text": "Switch to the Resources tab to manage your team, assign workloads, and instantly spot overallocation with color-coded alerts."
    },
    {
        "id": "07_save_darkmode",
        "text": "When you're done, hit Save to export a fully compatible dot-gan file — ready to reopen in GanttProject, with nothing lost. And with one click, switch to dark mode for those late-night planning sessions."
    },
    {
        "id": "08_outro",
        "text": "WebGantt: your project, your browser."
    },
]


# --- SERVICES (conservé pour compatibilité future si un serveur local est ajouté) ---
def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(("127.0.0.1", port)) == 0


def wait_for_service(service_config):
    """Conservé au cas où WebGantt serait un jour servi via un petit serveur HTTP local.
    Aujourd'hui APP_SETTINGS['services'] est vide donc cette fonction n'est jamais appelée."""
    import requests
    name = service_config["name"]
    port = service_config["port"]
    url = service_config.get("check_url")

    print(f"⏳ Attente de {name} sur le port {port}...")
    for i in range(40):
        if is_port_open(port):
            if url:
                try:
                    resp = requests.get(url, timeout=2)
                    if resp.status_code == 200:
                        print(f"  ✅ {name} opérationnel.")
                        return True
                except Exception:
                    pass
            else:
                print(f"  ✅ {name} (port ouvert).")
                return True

        if i % 5 == 0:
            print(f"🚀 [Tentative {i // 5 + 1}] Lancement de {name}...")
            subprocess.Popen(
                service_config["cmd"],
                cwd=str(service_config["cwd"]),
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        time.sleep(3)
    return False


# --- AUDIO (Kokoro ONNX, local, gratuit) ---
def generate_audio():
    print("🎙️ Phase Audio Kokoro ONNX (local, gratuit, sans clé API)...")
    try:
        from kokoro_onnx import Kokoro
        import soundfile as sf
        kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
    except Exception as e:
        print(f"  ❌ Erreur import Kokoro ONNX : {e}")
        print("     -> pip install kokoro-onnx soundfile")
        print("     -> wget https://github.com/thewhitetulip/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx")
        print("     -> wget https://github.com/thewhitetulip/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin")
        return {s['id']: 5.0 for s in script_segments}, {}

    durations = {}
    paths_map = {}
    for segment in script_segments:
        text_hash = hashlib.md5(segment['text'].encode()).hexdigest()
        path = AUDIO_DIR / f"{segment['id']}_{text_hash}.wav"

        # Nettoyage des anciens fichiers pour cet ID si le texte a changé
        for old_file in AUDIO_DIR.glob(f"{segment['id']}_*.wav"):
            if old_file.name != path.name:
                old_file.unlink()

        if path.exists() and path.stat().st_size > 0:
            try:
                info = sf.info(str(path))
                durations[segment['id']] = info.frames / info.samplerate
                paths_map[segment['id']] = path
                print(f"  ✅ {segment['id']} (cache : {durations[segment['id']]:.1f}s)")
                continue
            except Exception:
                pass

        print(f"  🎙️ Génération {segment['id']} (nouveau texte détecté)")
        try:
            samples, sample_rate = kokoro.create(segment['text'], voice=KOKORO_VOICE, lang=KOKORO_LANG)
            sf.write(str(path), samples, sample_rate)
            durations[segment['id']] = len(samples) / sample_rate
            paths_map[segment['id']] = path
            print(f"    -> OK ({durations[segment['id']]:.1f}s)")
        except Exception as e:
            print(f"    ❌ Échec : {e}")
            durations[segment['id']] = 5.0
    return durations, paths_map


# --- UTILITAIRES CAPTURE ---
async def install_cursor(page):
    """Injections du code JS pour le curseur (définition des fonctions et style)."""
    js_code = """
    window.setupFakeCursor = function() {
        if (document.getElementById('fake-cursor')) return;
        const cursor = document.createElement('div');
        cursor.id = 'fake-cursor';
        cursor.style.position = 'absolute';
        cursor.style.zIndex = '99999';
        cursor.style.width = '20px';
        cursor.style.height = '20px';
        cursor.style.borderRadius = '50%';
        cursor.style.backgroundColor = 'red';
        cursor.style.border = '2px solid white';
        cursor.style.pointerEvents = 'none';
        cursor.style.transition = 'all 0.5s ease-out';
        cursor.style.boxShadow = '0 0 10px rgba(0,0,0,0.5)';
        cursor.style.left = '0px';
        cursor.style.top = '0px';
        document.body.appendChild(cursor);

        window.moveCursor = (x, y) => {
          cursor.style.left = (x - 10) + 'px';
          cursor.style.top = (y - 10) + 'px';
        };

        window.clickCursor = () => {
          cursor.style.transform = 'scale(0.8)';
          cursor.style.backgroundColor = 'orange';
          setTimeout(() => {
            cursor.style.transform = 'scale(1)';
            cursor.style.backgroundColor = 'red';
          }, 200);
        };
    };
    window.setupFakeCursor();
    """
    await page.add_init_script(js_code)
    try:
        await page.evaluate(js_code)
    except Exception:
        pass


async def move_cursor(page, selector=None, x=None, y=None):
    """Déplace le pointeur rouge vers un élément ou des coordonnées."""
    await page.evaluate("if(window.setupFakeCursor) window.setupFakeCursor();")

    if selector:
        try:
            box = await page.locator(selector).first.bounding_box()
            if box:
                x = box['x'] + box['width'] / 2
                y = box['y'] + box['height'] / 2
        except Exception:
            pass

    if x is not None and y is not None:
        try:
            await page.evaluate(f"if(window.moveCursor) window.moveCursor({x}, {y})")
            await asyncio.sleep(0.6)
        except Exception:
            pass


async def smooth_scroll(page, distance, duration=1.0):
    """Défilement fluide pour le rendu vidéo."""
    steps = 10
    for _ in range(steps):
        await page.mouse.wheel(0, distance / steps)
        await asyncio.sleep(duration / steps)


# --- CAPTURE ---
async def capture(durations):
    print("🎥 Phase Capture Vidéo (Playwright)...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            record_video_dir=str(VIDEO_DIR),
            viewport={'width': 1920, 'height': 1080},
            record_video_size={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        await install_cursor(page)

        start_capture_time = time.time()

        def get_v_time():
            return time.time() - start_capture_time

        class SyncNarrator:
            """Gère la synchronisation entre les actions de capture et la narration audio."""

            def __init__(self, durations, time_func):
                self.durations = durations
                self.get_v_time = time_func
                self.current_id = None
                self.start_v_time = 0
                self.timestamps = {}

            async def start(self, segment_id):
                if self.current_id:
                    raise RuntimeError(
                        f"❌ ERREUR SYNCHRO : Impossible de démarrer '{segment_id}' car "
                        f"'{self.current_id}' est encore en cours. Appelez .end() d'abord."
                    )
                if segment_id not in self.durations:
                    print(f"⚠️  Attention : ID audio '{segment_id}' inconnu.")
                    return
                self.current_id = segment_id
                self.start_v_time = self.get_v_time()
                self.timestamps[segment_id] = self.start_v_time
                print(f"🎙️ [Sync Start] {segment_id} à {self.start_v_time:.1f}s")

            async def end(self, padding=0.5):
                if not self.current_id:
                    return
                duration = self.durations.get(self.current_id, 5.0)
                target_end = self.start_v_time + duration + padding
                now = self.get_v_time()
                if now < target_end:
                    wait_time = target_end - now
                    print(f"⏳ [Sync Wait] Pause de {wait_time:.1f}s pour finir '{self.current_id}'...")
                    while self.get_v_time() < target_end:
                        await asyncio.sleep(0.1)
                else:
                    print(f"✅ [Sync OK] '{self.current_id}' terminé avant la fin de l'action.")
                self.current_id = None

        narrator = SyncNarrator(durations, get_v_time)
        page.on("dialog", lambda dialog: print(f"💬 Dialogue : {dialog.message}") or asyncio.create_task(dialog.accept()))

        start_capture_time = time.time()

        try:
            print("🎬 Navigation vers WebGantt...")
            await page.goto(BASE_URL, wait_until="load", timeout=30000)

            # --- 01. Intro ---
            await narrator.start("01_intro")
            await narrator.end(padding=1.5)

            # --- 02. Ouverture d'un fichier .gan ---
            await narrator.start("02_open_file")
            print("🎬 Ouverture du fichier .gan d'exemple")
            try:
                # 1. Montrer le clic sur le bouton "Ouvrir"
                try:
                    btn_open = page.locator("#btn-open")
                    if await btn_open.count() > 0:
                        await move_cursor(page, "#btn-open")
                        await page.evaluate("window.clickCursor()")
                        print("  ✅ Bouton 'Ouvrir' cliqué")
                        await asyncio.sleep(0.8)
                except Exception as e:
                    print(f"  ⚠️  Bouton Ouvrir : {e}")

                # 2. Charger le fichier XML directement via JavaScript (méthode fiable)
                with open(EXAMPLE_GAN_PATH, 'r', encoding='utf-8') as f:
                    xml_content = f.read()

                # Charger le contenu via state.loadXML (appel direct)
                await page.evaluate(f"""
                    (async () => {{
                        try {{
                            // Charger le XML directement dans l'état
                            state.loadXML(`{xml_content.replace(chr(96), chr(96) + chr(96))}`);
                            document.getElementById('btn-save').style.display = 'inline-block';

                            // Sauvegarder dans la DB (optionnel)
                            if (window.saveProjectStateToDB) {{
                                await window.saveProjectStateToDB(`{xml_content.replace(chr(96), chr(96) + chr(96))}`, null);
                            }}
                            console.log("✅ Projet chargé via Playwright");
                        }} catch(err) {{
                            console.error("❌ Erreur lors du chargement :", err);
                        }}
                    }})();
                """)

                # Attendre que le projet se charge
                await asyncio.sleep(2.5)
                print(f"  ✅ Projet chargé depuis {EXAMPLE_GAN_PATH.name}")

                # 3. Scroll pour voir la structure complète
                await page.evaluate("document.querySelector('#wbs-container, .wbs-container') && document.querySelector('#wbs-container, .wbs-container').scrollBy(0, 100)")
                await asyncio.sleep(0.8)
            except Exception as e:
                print(f"  ⚠️  Erreur lors de l'ouverture du fichier : {e}")
            await narrator.end(padding=1.0)

            # --- 03. WBS : ajout, indentation, édition, drag-and-drop ---
            await narrator.start("03_wbs")
            print("🎬 Manipulation du WBS (ajout, indentation, édition, drag-and-drop)")
            try:
                # 1. Ajouter une tâche
                await move_cursor(page, "#btn-add-task")
                await page.evaluate("window.clickCursor()")
                await page.click("#btn-add-task", timeout=5000)
                print("  ✅ Tâche ajoutée")
                await asyncio.sleep(1.2)

                # 2. Ajouter une deuxième tâche
                await move_cursor(page, "#btn-add-task")
                await page.evaluate("window.clickCursor()")
                await page.click("#btn-add-task", timeout=5000)
                print("  ✅ Deuxième tâche ajoutée")
                await asyncio.sleep(0.8)

                # 3. Indenter la deuxième tâche pour créer une phase
                try:
                    indent_btn = page.locator("#btn-indent")
                    if await indent_btn.count() > 0:
                        await move_cursor(page, "#btn-indent")
                        await page.evaluate("window.clickCursor()")
                        await indent_btn.click(timeout=3000)
                        print("  ✅ Tâche indentée (phase créée)")
                        await asyncio.sleep(1.2)
                except Exception as e:
                    print(f"  ⚠️  Indentation : {e}")

                # 4. Double-clic pour éditer le nom de la tâche inline
                try:
                    wbs_rows = page.locator("#wbs-content > div[id^='wbs-row-']")
                    count = await wbs_rows.count()
                    if count > 0:
                        last_row = wbs_rows.nth(count - 1)
                        # Double-clic sur la ligne pour ouvrir la modale
                        await last_row.dblclick(timeout=3000)
                        print("  ✅ Double-clic pour édition (modale ouverte)")
                        await asyncio.sleep(1.5)

                        # Fermer la modale
                        try:
                            await page.keyboard.press("Escape")
                            print("  ✅ Modale fermée")
                        except:
                            pass
                except Exception as e:
                    print(f"  ⚠️  Double-clic édition : {e}")

                await asyncio.sleep(0.8)

                # 5. Scroll pour voir la hiérarchie créée
                wbs_container = page.locator("#wbs-container, .wbs-container, [class*='wbs']").first
                if await wbs_container.count() > 0:
                    await page.evaluate("document.querySelector('#wbs-container, .wbs-container, [class*=wbs]').scrollBy(0, 150)")
                    print("  ✅ Hiérarchie des tâches visible")
                await asyncio.sleep(1)

                # 6. Drag-and-drop : réorganiser les tâches
                try:
                    wbs_rows = page.locator("#wbs-content > div[id^='wbs-row-']")
                    row_count = await wbs_rows.count()
                    if row_count >= 2:
                        source_row = wbs_rows.nth(row_count - 2)
                        target_row = wbs_rows.nth(row_count - 1)

                        source_box = await source_row.bounding_box()
                        target_box = await target_row.bounding_box()

                        if source_box and target_box:
                            # Afficher le curseur au point de départ
                            await move_cursor(page, None, source_box['x'] + source_box['width'] / 2,
                                            source_box['y'] + source_box['height'] / 2)
                            await page.evaluate("window.clickCursor()")
                            await asyncio.sleep(0.4)

                            # Drag-and-drop
                            await page.mouse.down()
                            await asyncio.sleep(0.4)
                            await move_cursor(page, None, target_box['x'] + target_box['width'] / 2,
                                            target_box['y'] - 20)
                            await asyncio.sleep(0.3)
                            await page.mouse.up()
                            print("  ✅ Drag-and-drop pour réorganiser")
                            await asyncio.sleep(1.2)
                except Exception as e:
                    print(f"  ⚠️  Drag-and-drop : {e}")

            except Exception as e:
                print(f"  ⚠️  Erreur WBS : {e}")
            await narrator.end(padding=1.0)

            # --- 04. Dépendances entre tâches ---
            await narrator.start("04_dependencies")
            print("🎬 Création de dépendances entre tâches")
            modal_opened = False
            try:
                # Cliquer sur le bouton détails (loupe) de la deuxième tâche
                detail_buttons = page.locator("#wbs-content button:has-text('🔍'), #wbs-content button[title*='caractéristiques']")
                if await detail_buttons.count() >= 2:
                    # Cliquer sur le deuxième bouton (deuxième tâche)
                    second_task_btn = detail_buttons.nth(1)
                    await move_cursor(page, None, (await second_task_btn.bounding_box() or {}).get('x', 100) + 10,
                                    (await second_task_btn.bounding_box() or {}).get('y', 100) + 10)
                    await page.evaluate("window.clickCursor()")
                    await second_task_btn.click(timeout=3000)
                    print("  ✅ Modale de détails de tâche ouverte")
                    modal_opened = True
                    await asyncio.sleep(1)

                    # Cliquer sur l'onglet Prédécesseurs
                    try:
                        pred_tab = page.locator(".td-tab-btn[data-target='td-tab-predecessors']")
                        if await pred_tab.count() > 0:
                            await pred_tab.click(timeout=2000)
                            print("  ✅ Onglet Prédécesseurs ouvert")
                            await asyncio.sleep(0.8)

                            # Ajouter un prédécesseur (sélectionner une tâche)
                            try:
                                pred_dropdown = page.locator("select, [id*='predecessor'], [id*='depend']").first
                                if await pred_dropdown.count() > 0:
                                    await pred_dropdown.click(timeout=2000)
                                    await asyncio.sleep(0.5)

                                    # Sélectionner une option du dropdown
                                    options = page.locator("option")
                                    if await options.count() > 1:
                                        # Sélectionner la deuxième option (première tâche)
                                        await options.nth(1).click(timeout=2000)
                                        print("  ✅ Prédécesseur sélectionné")
                                        await asyncio.sleep(0.5)

                                        # Cliquer sur le bouton "Ajouter"
                                        add_btn = page.locator("button:has-text('Ajouter')").first
                                        if await add_btn.count() > 0:
                                            await add_btn.click(timeout=2000)
                                            print("  ✅ Dépendance ajoutée")
                            except Exception as e:
                                print(f"  ⚠️  Ajout prédécesseur : {e}")
                    except Exception as e:
                        print(f"  ⚠️  Onglet prédécesseurs : {e}")
            except Exception as e:
                print(f"  ⚠️  Création de dépendance : {e}")
            finally:
                # TOUJOURS fermer la modale si elle a été ouverte
                if modal_opened:
                    try:
                        await page.keyboard.press("Escape")
                        await asyncio.sleep(0.5)
                        print("  ✅ Modale fermée")
                    except:
                        pass

            # Montrer le diagramme Gantt se recalculer automatiquement avec les dépendances
            try:
                # Scroll vers le haut pour voir le WBS et le Gantt ensemble
                await page.evaluate("window.scrollTo(0, 0)")
                await asyncio.sleep(0.8)

                # Montrer le Gantt chart avec les dépendances visibles
                gantt_container = page.locator(".gantt-container, [id*='gantt'], svg[class*='gantt']").first
                if await gantt_container.count() > 0:
                    # Scroll à droite pour voir plus des barres de Gantt
                    await page.evaluate("document.querySelector('.gantt-container, [id*=gantt], svg[class*=gantt]') && document.querySelector('.gantt-container, [id*=gantt], svg[class*=gantt]').scrollBy(150, 0)")
                    print("  ✅ Gantt chart avec dépendances visible (recalculé automatiquement)")
                    await asyncio.sleep(2)  # Attendre plus longtemps pour voir le résultat

                    # Scroll un peu plus pour voir les connexions entre tâches
                    await page.evaluate("document.querySelector('.gantt-container, [id*=gantt], svg[class*=gantt]') && document.querySelector('.gantt-container, [id*=gantt], svg[class*=gantt]').scrollBy(100, 0)")
                    print("  ✅ Connexions entre tâches visibles")
                    await asyncio.sleep(1)
            except Exception as e:
                print(f"  ⚠️  Gantt chart : {e}")
            await asyncio.sleep(0.5)
            await narrator.end(padding=1.0)

            # --- 05. Chemin critique + zoom avant/arrière ---
            await narrator.start("05_critical_path")
            print("🎬 Activation du chemin critique et zoom")
            try:
                # 1. Cliquer sur le bouton "Afficher le chemin critique"
                try:
                    btn_cp = page.locator("#btn-critical-path")
                    if await btn_cp.count() > 0:
                        await move_cursor(page, "#btn-critical-path")
                        await page.evaluate("window.clickCursor()")
                        await btn_cp.click(timeout=3000)
                        print("  ✅ Chemin critique activé")
                    await asyncio.sleep(1.5)
                except Exception as e:
                    print(f"  ⚠️  Chemin critique : {e}")

                # 2. Zoom avant pour voir le détail
                try:
                    zoom_in_btn = page.locator("#btn-zoom-in")
                    if await zoom_in_btn.count() > 0:
                        await move_cursor(page, "#btn-zoom-in")
                        await page.evaluate("window.clickCursor()")
                        await zoom_in_btn.click(timeout=2000)
                        print("  ✅ Zoom avant appliqué (vue détaillée)")
                        await asyncio.sleep(1.5)
                except Exception as e:
                    print(f"  ⚠️  Zoom avant : {e}")

                # 3. Montrer le détail du chemin critique
                await page.evaluate("document.querySelector('.gantt-container, .gantt-pane, svg[class*=gantt]') && document.querySelector('.gantt-container, .gantt-pane, svg[class*=gantt]').scrollBy(150, 0)")
                print("  ✅ Chemin critique visible en détail (vue quotidienne)")
                await asyncio.sleep(1.2)

                # 4. Zoom arrière pour voir l'ensemble du projet
                try:
                    zoom_out_btn = page.locator("#btn-zoom-out")
                    if await zoom_out_btn.count() > 0:
                        await move_cursor(page, "#btn-zoom-out")
                        await page.evaluate("window.clickCursor()")
                        await zoom_out_btn.click(timeout=2000)
                        print("  ✅ Zoom arrière appliqué (vue d'ensemble)")
                        await asyncio.sleep(1.5)
                except Exception as e:
                    print(f"  ⚠️  Zoom arrière : {e}")

                # 5. Montrer la vue d'ensemble avec chemin critique
                await page.evaluate("document.querySelector('.gantt-container, .gantt-pane, svg[class*=gantt]') && document.querySelector('.gantt-container, .gantt-pane, svg[class*=gantt]').scrollBy(100, 0)")
                print("  ✅ Vue d'ensemble du projet avec chemin critique")
                await asyncio.sleep(1.5)
            except Exception as e:
                print(f"  ⚠️  Erreur chemin critique : {e}")
            await narrator.end(padding=1.0)

            # --- 06. Ressources : gestion d'équipe et assignation ---
            await narrator.start("06_resources")
            print("🎬 Gestion des ressources et assignation de charges")
            try:
                # 1. Basculer sur l'onglet Ressources (DIV avec class view-tab)
                found_tab = False
                try:
                    # L'onglet Ressources est un DIV avec data-target="res-main-container"
                    res_tab = page.locator(".view-tab[data-target='res-main-container']")
                    if await res_tab.count() > 0:
                        bbox = await res_tab.bounding_box()
                        if bbox:
                            await move_cursor(page, None, bbox['x'] + bbox['width'] / 2, bbox['y'] + bbox['height'] / 2)
                            await page.evaluate("window.clickCursor()")
                            await res_tab.click(timeout=3000)
                            print("  ✅ Vue Ressources activée")
                            found_tab = True
                except Exception as e:
                    print(f"  ⚠️  Onglet Ressources : {e}")

                if found_tab:
                    await asyncio.sleep(2)  # Attendre que le contenu se rende

                    # 2. Montrer la liste des ressources disponibles
                    res_list = page.locator("[class*='res-wbs'], #res-wbs-content, [data-testid*='resource']").first
                    if await res_list.count() > 0:
                        await page.evaluate("document.querySelector('[class*=res-wbs], #res-wbs-content, [data-testid*=resource]') && document.querySelector('[class*=res-wbs], #res-wbs-content, [data-testid*=resource]').scrollBy(0, 120)")
                        print("  ✅ Ressources d'équipe visibles")
                        await asyncio.sleep(1)

                    # 3. Scroll à droite pour voir la charge de travail
                    gantt_res = page.locator(".res-gantt, [class*='res-gantt'], svg[class*='resource']").first
                    if await gantt_res.count() > 0:
                        await page.evaluate("document.querySelector('.res-gantt, [class*=res-gantt], svg[class*=resource]') && document.querySelector('.res-gantt, [class*=res-gantt], svg[class*=resource]').scrollBy(100, 0)")
                        print("  ✅ Diagramme de charge visible")
                        await asyncio.sleep(1.2)

                    # 4. Ouvrir la modale d'une tâche pour assigner une ressource
                    modal_opened_res = False
                    try:
                        detail_btns = page.locator("[id*='res-wbs'] button:has-text('🔍'), [id*='res-wbs'] button[title*='caractéristiques']")
                        if await detail_btns.count() > 0:
                            first_detail_btn = detail_btns.first
                            bbox = await first_detail_btn.bounding_box()
                            if bbox:
                                await move_cursor(page, None, bbox['x'] + 10, bbox['y'] + 10)
                                await page.evaluate("window.clickCursor()")
                                await first_detail_btn.click(timeout=3000)
                                print("  ✅ Modale de tâche ouverte pour assignation")
                                modal_opened_res = True
                                await asyncio.sleep(1.2)

                                # 5. Aller à l'onglet Ressources de la modale
                                try:
                                    res_modal_tab = page.locator(".td-tab-btn[data-target='td-tab-resources'], button:has-text('Ressources')").first
                                    if await res_modal_tab.count() > 0:
                                        await res_modal_tab.click(timeout=2000)
                                        print("  ✅ Onglet Ressources de la tâche ouvert")
                                        await asyncio.sleep(1)

                                        # Montrer la table d'assignation
                                        alloc_table = page.locator("table [class*='allocation'], [id*='allocations']").first
                                        if await alloc_table.count() > 0:
                                            print("  ✅ Assignations de ressources visibles")
                                except:
                                    pass
                    except Exception as e:
                        print(f"  ⚠️  Assignation ressource : {e}")
                    finally:
                        # Fermer la modale si elle est ouverte
                        if modal_opened_res:
                            try:
                                await page.keyboard.press("Escape")
                                await asyncio.sleep(0.5)
                                print("  ✅ Modale fermée")
                            except:
                                pass

                    # 6. Montrer le diagramme des ressources (à droite de la liste)
                    print("  ✅ Onglet Ressources visible avec assignations")
                    # Attendre que le SVG du diagramme se rende
                    await asyncio.sleep(2)

                    # Vérifier que le SVG du diagramme est visible
                    try:
                        svg_chart = page.locator("#res-gantt-content svg, [id*='res-gantt'] svg").first
                        if await svg_chart.count() > 0:
                            print("  ✅ SVG du diagramme détecté")
                        await asyncio.sleep(0.5)
                    except:
                        pass

                    # Scroll à droite pour montrer le "Resource Chart" (diagramme des ressources)
                    try:
                        # Scroll horizontal dans le conteneur du diagramme
                        await page.evaluate("document.querySelector('#res-gantt-content').scrollBy(300, 0)")
                        print("  ✅ Diagramme des ressources visible (charge par ressource)")
                        await asyncio.sleep(1.5)

                        # Scroll un peu plus pour voir le timeline complet
                        await page.evaluate("document.querySelector('#res-gantt-content').scrollBy(200, 0)")
                        print("  ✅ Timeline des ressources visible")
                        await asyncio.sleep(1)
                    except Exception as e:
                        print(f"  ⚠️  Diagramme ressources : {e}")

                else:
                    # Fallback
                    await page.evaluate("window.scrollBy(0, 200)")
                    print("  ✅ Scroll vers ressources")
                    await asyncio.sleep(1.5)

            except Exception as e:
                print(f"  ⚠️  Erreur Ressources : {e}")
            await narrator.end(padding=1.0)

            # --- 07. Sauvegarde et Dark Mode ---
            await narrator.start("07_save_darkmode")
            print("🎬 Sauvegarde du fichier et bascule en Dark Mode")
            try:
                # 0. Retourner à la vue Gantt depuis Ressources
                try:
                    gantt_tabs = [
                        "button:has-text('Gantt')",
                        "button:has-text('Gantt des')",
                        "#tab-gantt",
                        "button[data-view='gantt']"
                    ]
                    for selector in gantt_tabs:
                        try:
                            tab = page.locator(selector).first
                            if await tab.count() > 0:
                                await move_cursor(page, selector)
                                await page.evaluate("window.clickCursor()")
                                await tab.click(timeout=2000)
                                print("  ✅ Retour à Gantt pour sauvegarder")
                                await asyncio.sleep(1)
                                break
                        except:
                            pass
                except Exception as e:
                    print(f"  ⚠️  Retour à Gantt : {e}")

                # 1. Scroll pour s'assurer que la toolbar est visible
                await page.evaluate("window.scrollTo(0, 0)")
                await asyncio.sleep(0.8)

                # 2. Cliquer sur le bouton Sauvegarder
                btn_save = page.locator("#btn-save")
                await btn_save.wait_for(timeout=3000)
                await move_cursor(page, "#btn-save")
                await page.evaluate("window.clickCursor()")
                await btn_save.click()
                print("  ✅ Fichier sauvegardé (export .gan compatible)")
                await asyncio.sleep(2)  # Montrer le succès de la sauvegarde

                # 3. Montrer l'interface Light Mode un moment
                await page.evaluate("document.querySelector('.gantt-container, [id*=gantt]') && document.querySelector('.gantt-container, [id*=gantt]').scrollBy(100, 0)")
                await asyncio.sleep(1.2)

                # 4. Basculer vers Dark Mode
                try:
                    btn_theme = page.locator("#btn-theme-toggle")
                    if await btn_theme.count() > 0:
                        await move_cursor(page, "#btn-theme-toggle")
                        await page.evaluate("window.clickCursor()")
                        await btn_theme.click(timeout=2000)
                        print("  ✅ Dark Mode activé")
                        await asyncio.sleep(1.5)  # Montrer l'interface en Dark Mode

                        # 5. Montrer le Gantt en Dark Mode
                        await page.evaluate("document.querySelector('.gantt-container, [id*=gantt]') && document.querySelector('.gantt-container, [id*=gantt]').scrollBy(100, 0)")
                        print("  ✅ Interface Dark Mode avec Gantt visible")
                        await asyncio.sleep(1.8)

                        # 6. Scroll pour montrer plus du projet en Dark Mode
                        await page.evaluate("window.scrollBy(0, 150)")
                        print("  ✅ Structure du projet visible en Dark Mode")
                        await asyncio.sleep(1.5)
                    else:
                        print("  ⚠️  Bouton Dark Mode non trouvé")
                        await asyncio.sleep(1.5)
                except Exception as e:
                    print(f"  ⚠️  Dark Mode : {e}")
                    await asyncio.sleep(1.5)

            except Exception as e:
                print(f"  ⚠️  Erreur Save/Thème : {e}")
            await narrator.end(padding=1.0)

            # --- 08. Outro ---
            await narrator.start("08_outro")
            await asyncio.sleep(1)
            await narrator.end(padding=1.5)

        except Exception as e:
            print(f"  ❌ Erreur critique pendant la capture : {e}")

        await context.close()
        video_path = await page.video.path()
        return video_path, narrator.timestamps


def create_logo_image(size=200):
    """Crée le logo WebGantt fidèle au SVG (Gantt chart dans un carré bleu arrondi)."""
    from PIL import Image, ImageDraw

    # Créer une image avec le logo WebGantt
    img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))  # Transparent
    draw = ImageDraw.Draw(img)

    # Fond bleu avec coins arrondis (rayon = 20% de la taille)
    radius = int(size * 0.2)
    draw.rounded_rectangle(
        [(0, 0), (size, size)],
        radius=radius,
        fill=(9, 105, 218, 255)  # Bleu #0969da
    )

    # Barres blanches fidèles au SVG (taille de 0-100)
    # Scale : chaque coord SVG * (size/100)
    scale = size / 100.0
    bar_radius = int(5 * scale)  # rx=5 dans le SVG

    # Barre 1: x='15' y='25' width='45' height='15'
    draw.rounded_rectangle(
        [(15 * scale, 25 * scale), (60 * scale, 40 * scale)],
        radius=bar_radius,
        fill=(255, 255, 255, 255)
    )

    # Barre 2: x='35' y='50' width='50' height='15'
    draw.rounded_rectangle(
        [(35 * scale, 50 * scale), (85 * scale, 65 * scale)],
        radius=bar_radius,
        fill=(255, 255, 255, 255)
    )

    # Barre 3: x='25' y='75' width='30' height='15'
    draw.rounded_rectangle(
        [(25 * scale, 75 * scale), (55 * scale, 90 * scale)],
        radius=bar_radius,
        fill=(255, 255, 255, 255)
    )

    return img


def create_title_card(duration):
    """Génère la page de garde complète avec PIL + MoviePy."""
    print(f"🎨 Création de la page de garde ({duration:.1f}s)...")

    # Créer une image PIL complète (1920x1080)
    title_img = Image.new('RGB', (1920, 1080), color=APP_SETTINGS["bg_color"])
    draw = ImageDraw.Draw(title_img)

    # Charger les polices (utiliser DejaVuSans-Bold qui ressemble à Inter)
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 140)
    except:
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 140)
        except:
            title_font = ImageFont.load_default()

    try:
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 44)
    except:
        subtitle_font = ImageFont.load_default()

    try:
        footer_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf", 38)
    except:
        footer_font = ImageFont.load_default()

    # 1. Logo (créé avec PIL, puis inséré comme image)
    logo_img = create_logo_image(size=220)
    title_img.paste(logo_img, (250, 280), logo_img)

    # 2. Titre principal "WebGantt"
    title_text = APP_SETTINGS["title"]
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = 550
    title_y = 300
    draw.text((title_x, title_y), title_text, fill=(24, 32, 43), font=title_font)

    # 3. Sous-titre (multi-ligne)
    subtitle_text = APP_SETTINGS["subtitle"]
    subtitle_lines = subtitle_text.split('\n')
    line_height = 50
    subtitle_y = 550
    for line in subtitle_lines:
        line_bbox = draw.textbbox((0, 0), line, font=subtitle_font)
        line_width = line_bbox[2] - line_bbox[0]
        line_x = (1920 - line_width) // 2
        draw.text((line_x, subtitle_y), line, fill=(80, 80, 80), font=subtitle_font)
        subtitle_y += line_height

    # 4. Barre accent (couleur bleue)
    bar_width = 1000
    bar_x = (1920 - bar_width) // 2
    bar_y = 780
    bar_height = 8
    draw.rectangle(
        [(bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height)],
        fill=APP_SETTINGS["accent_color"]
    )

    # 5. Footer
    footer_text = APP_SETTINGS["footer_tagline"]
    footer_bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    footer_width = footer_bbox[2] - footer_bbox[0]
    footer_x = (1920 - footer_width) // 2
    footer_y = 850
    draw.text((footer_x, footer_y), footer_text, fill=(120, 120, 120), font=footer_font)

    # Sauvegarder l'image
    title_card_path = AUDIO_DIR / "title_card.png"
    title_img.save(title_card_path)
    print(f"  ✅ Page de garde générée avec PIL")

    # Créer le clip vidéo à partir de l'image
    return mp.ImageClip(str(title_card_path)).with_duration(duration)


# --- MONTAGE ---
def assemble(video_path, durations, audio_paths, timestamps):
    print("🎬 Phase Montage Final...")
    if not os.path.exists(video_path):
        print("  ❌ Fichier vidéo source introuvable.")
        return

    full_video = mp.VideoFileClip(video_path)

    intro_audio_dur = durations.get("01_intro", 5.0)
    intro_total_dur = intro_audio_dur + 1.5
    intro_animation = create_title_card(intro_total_dur)

    # Pas de "saut temporel" pour cette démo (contrairement au projet ARIA qui attendait
    # une réponse LLM) : on concatène simplement la page de garde et la capture complète.
    rest_of_video = full_video.subclipped(intro_total_dur, full_video.duration)
    video = mp.concatenate_videoclips([intro_animation, rest_of_video])

    # --- AUDIO ---
    audio_clips = []
    last_audio_end = 0
    overlaps_detected = []

    for sid, t_start in timestamps.items():
        p = audio_paths.get(sid)
        if p and p.exists():
            if t_start < last_audio_end:
                drift = last_audio_end - t_start
                overlaps_detected.append(f"{sid} (décalé de {drift:.2f}s)")
                actual_start = last_audio_end
            else:
                actual_start = t_start

            print(f"  🔊 Calage {sid} à {actual_start:.1f}s")
            a_clip = mp.AudioFileClip(str(p)).with_start(actual_start)
            audio_clips.append(a_clip)
            last_audio_end = actual_start + a_clip.duration + 0.8

    if overlaps_detected:
        print("\n" + "!" * 60)
        print("⚠️  ALERTE SYNCHRO : Des chevauchements audio ont été évités !")
        for msg in overlaps_detected:
            print(f"   - {msg}")
        print("💡 Conseil : Augmentez les temps d'attente (asyncio.sleep) dans capture().")
        print("!" * 60 + "\n")

    if audio_clips:
        video_with_audio = video.with_audio(mp.CompositeAudioClip(audio_clips))
        if last_audio_end > video.duration:
            print(f"⚠️  ATTENTION : L'audio dépasse la vidéo de {last_audio_end - video.duration:.1f}s. Ajout d'un freeze frame.")
            last_frame = video.get_frame(video.duration - 0.05)
            freeze_duration = last_audio_end - video.duration + 1.0
            freeze_clip = mp.ImageClip(last_frame).with_duration(freeze_duration).with_start(video.duration)
            video = mp.CompositeVideoClip([video_with_audio, freeze_clip])
        else:
            video = video_with_audio

    out_name = f"DEMO_WEBGANTT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    out = BASE_DIR / out_name
    print(f"💾 Génération de {out}...")
    video.write_videofile(str(out), codec="libx264", audio_codec="aac", fps=24)
    print(f"✨ TERMINÉ ! Fichier : {out}")


async def main():
    script_start_time = time.time()
    print("⏱️  Démarrage du script...")

    assemble_only = "--assemble-only" in sys.argv
    meta_path = BASE_DIR / "last_meta.json"

    if not assemble_only:
        for svc in APP_SETTINGS["services"]:
            if not wait_for_service(svc):
                return

    durations, audio_paths = generate_audio()

    if assemble_only:
        if not meta_path.exists():
            print("  ❌ Aucun fichier 'last_meta.json' trouvé. Lancez une capture complète d'abord.")
            return

        print("⚡ Mode Montage Seul activé. Réutilisation de la dernière capture...")
        with open(meta_path, "r") as f:
            meta = json.load(f)
            t_marks = meta["timestamps"]
            v_path = meta.get("video_path")

        if not v_path or not os.path.exists(v_path):
            webms = list(VIDEO_DIR.glob("*.webm"))
            if not webms:
                print("  ❌ Aucune vidéo .webm trouvée dans temp_video/")
                return
            v_path = str(max(webms, key=os.path.getmtime))
            print(f"  🎬 Vidéo détectée : {v_path}")

        assemble(v_path, durations, audio_paths, t_marks)
    else:
        try:
            v_path, t_marks = await capture(durations)
            if v_path:
                with open(meta_path, "w") as f:
                    json.dump({
                        "video_path": v_path,
                        "timestamps": t_marks
                    }, f, indent=2)

                assemble(v_path, durations, audio_paths, t_marks)
        except Exception as e:
            print(f"❌ Échec global : {e}")
            import traceback
            traceback.print_exc()

    # Afficher le temps d'exécution
    elapsed_time = time.time() - script_start_time
    minutes, seconds = divmod(elapsed_time, 60)
    print("\n" + "="*60)
    print(f"✨ Script terminé en {int(minutes)}m {seconds:.1f}s ({elapsed_time:.1f}s total)")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
