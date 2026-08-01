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

# --- CONFIGURATION GÉNÉRALE ---
BASE_DIR = Path(__file__).parent.absolute()
ROOT_DIR = BASE_DIR.parent
AUDIO_DIR = BASE_DIR / "temp_audio"
VIDEO_DIR = BASE_DIR / "temp_video"
AUDIO_DIR.mkdir(exist_ok=True)
VIDEO_DIR.mkdir(exist_ok=True)

# TODO : adapter ce chemin vers ton fichier webGantt.html réel
WEBGANTT_HTML_PATH = ROOT_DIR / "webGantt.html"
# TODO : adapter ce chemin vers le fichier .gan d'exemple à charger dans la démo
EXAMPLE_GAN_PATH = ROOT_DIR / "specs/001-ganttproject-features/assets/example.gan"

# WebGantt est 100% client-side : pas de backend à démarrer.
# On peut ouvrir le fichier directement en file:// avec Playwright.
BASE_URL = f"file://{WEBGANTT_HTML_PATH}"

# --- CONFIGURATION DE L'APPLICATION (page de garde) ---
APP_SETTINGS = {
    "title": "WebGantt",
    "subtitle": "A lightweight, 100% browser-based\nGantt chart application",
    "bg_color": (24, 32, 43),        # Bleu nuit
    "accent_color": (76, 175, 175),  # Teal
    "footer_tagline": "Open Source \u2022 No install \u2022 No server",
    # Pas de backend/frontend à lancer : WebGantt tourne dans un seul fichier HTML.
    "services": [],
}

# --- CONFIGURATION KOKORO (TTS local, gratuit) ---
KOKORO_LANG = "a"            # 'a' = American English, 'b' = British English
KOKORO_VOICE = "am_michael"  # voix masculine US ; alternatives : "af_heart", "af_bella", "bf_emma"...
KOKORO_SAMPLE_RATE = 24000

# --- SEGMENTS DE VOIX OFF (script de la démo) ---
script_segments = [
    {
        "id": "01_intro",
        "text": "Meet WebGantt — a Gantt chart app that lives entirely in your browser. No install, no server, no backend. Just open the HTML file, and you're ready to plan."
    },
    {
        "id": "02_open_file",
        "text": "WebGantt speaks the same language as GanttProject, the open source project management tool used for over twenty years. Click Open, pick a dot-gan file, and your entire project — tasks, resources, dependencies — loads instantly."
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
        "text": "WebGantt: your project, your browser, no strings attached."
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


# --- AUDIO (Kokoro, local, gratuit) ---
def generate_audio():
    print("🎙️ Phase Audio Kokoro (local, gratuit, sans clé API)...")
    try:
        from kokoro import KPipeline
        import soundfile as sf
        pipeline = KPipeline(lang_code=KOKORO_LANG)
    except Exception as e:
        print(f"  ❌ Erreur import Kokoro : {e}")
        print("     -> pip install kokoro soundfile numpy --break-system-packages")
        return {s['id']: 5.0 for s in script_segments}, {}

    import numpy as np

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
            generator = pipeline(segment['text'], voice=KOKORO_VOICE)
            audio_chunks = [audio for _, _, audio in generator]
            audio_full = np.concatenate(audio_chunks) if len(audio_chunks) > 1 else audio_chunks[0]
            sf.write(str(path), audio_full, KOKORO_SAMPLE_RATE)
            durations[segment['id']] = len(audio_full) / KOKORO_SAMPLE_RATE
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
            # TODO : remplacer par le vrai sélecteur du bouton "Open"
            btn_open = "TODO_SELECTOR_OPEN_BUTTON"
            # TODO : remplacer par le vrai sélecteur de l'<input type="file">
            input_file = "TODO_SELECTOR_FILE_INPUT"
            try:
                await move_cursor(page, btn_open)
                await page.evaluate("window.clickCursor()")
                await page.click(btn_open, timeout=5000)
                await page.set_input_files(input_file, str(EXAMPLE_GAN_PATH))
                await asyncio.sleep(1.5)
            except Exception as e:
                print(f"  ⚠️  Sélecteurs 'Open' non renseignés/incorrects, étape ignorée ({e})")
            await narrator.end(padding=1.0)

            # --- 03. WBS : ajout de tâche, indentation, édition inline ---
            await narrator.start("03_wbs")
            print("🎬 Manipulation du WBS (ajout, indentation, édition)")
            btn_add_task = "TODO_SELECTOR_ADD_TASK_BUTTON"
            btn_indent = "TODO_SELECTOR_INDENT_BUTTON"
            task_name_cell = "TODO_SELECTOR_TASK_NAME_CELL"
            try:
                await move_cursor(page, btn_add_task)
                await page.evaluate("window.clickCursor()")
                await page.click(btn_add_task, timeout=5000)
                await asyncio.sleep(1)

                await move_cursor(page, btn_indent)
                await page.evaluate("window.clickCursor()")
                await page.click(btn_indent, timeout=5000)
                await asyncio.sleep(1)

                await move_cursor(page, task_name_cell)
                await page.dblclick(task_name_cell, timeout=5000)
                await asyncio.sleep(1.5)
            except Exception as e:
                print(f"  ⚠️  Sélecteurs WBS non renseignés/incorrects, étape ignorée ({e})")
            await narrator.end(padding=1.0)

            # --- 04. Dépendances entre tâches ---
            await narrator.start("04_dependencies")
            print("🎬 Création d'une dépendance (Link)")
            task_row_1 = "TODO_SELECTOR_TASK_ROW_1"
            task_row_2 = "TODO_SELECTOR_TASK_ROW_2"
            btn_link = "TODO_SELECTOR_LINK_BUTTON"
            try:
                await move_cursor(page, task_row_1)
                await page.click(task_row_1, timeout=5000)
                await page.keyboard.down("Control")
                await move_cursor(page, task_row_2)
                await page.click(task_row_2, timeout=5000)
                await page.keyboard.up("Control")

                await move_cursor(page, btn_link)
                await page.evaluate("window.clickCursor()")
                await page.click(btn_link, timeout=5000)
                await asyncio.sleep(1.5)
            except Exception as e:
                print(f"  ⚠️  Sélecteurs Dépendances non renseignés/incorrects, étape ignorée ({e})")
            await narrator.end(padding=1.0)

            # --- 05. Chemin critique + zoom ---
            await narrator.start("05_critical_path")
            print("🎬 Activation du chemin critique et zoom")
            btn_critical_path = "TODO_SELECTOR_CRITICAL_PATH_BUTTON"
            btn_zoom_in = "TODO_SELECTOR_ZOOM_IN_BUTTON"
            btn_zoom_out = "TODO_SELECTOR_ZOOM_OUT_BUTTON"
            try:
                await move_cursor(page, btn_critical_path)
                await page.evaluate("window.clickCursor()")
                await page.click(btn_critical_path, timeout=5000)
                await asyncio.sleep(1)

                await move_cursor(page, btn_zoom_in)
                await page.click(btn_zoom_in, timeout=5000)
                await asyncio.sleep(0.8)
                await page.click(btn_zoom_out, timeout=5000)
                await asyncio.sleep(0.8)
            except Exception as e:
                print(f"  ⚠️  Sélecteurs Zoom/Chemin critique non renseignés/incorrects, étape ignorée ({e})")
            await narrator.end(padding=1.0)

            # --- 06. Ressources ---
            await narrator.start("06_resources")
            print("🎬 Onglet Ressources")
            tab_resources = "TODO_SELECTOR_RESOURCES_TAB"
            try:
                await move_cursor(page, tab_resources)
                await page.evaluate("window.clickCursor()")
                await page.click(tab_resources, timeout=5000)
                await asyncio.sleep(2)
            except Exception as e:
                print(f"  ⚠️  Sélecteur Ressources non renseigné/incorrect, étape ignorée ({e})")
            await narrator.end(padding=1.0)

            # --- 07. Save + dark mode ---
            await narrator.start("07_save_darkmode")
            print("🎬 Sauvegarde et bascule Dark Mode")
            btn_save = "TODO_SELECTOR_SAVE_BUTTON"
            btn_theme = "TODO_SELECTOR_THEME_TOGGLE"
            try:
                await move_cursor(page, btn_save)
                await page.evaluate("window.clickCursor()")
                await page.click(btn_save, timeout=5000)
                await asyncio.sleep(1)

                await move_cursor(page, btn_theme)
                await page.evaluate("window.clickCursor()")
                await page.click(btn_theme, timeout=5000)
                await asyncio.sleep(1.5)
            except Exception as e:
                print(f"  ⚠️  Sélecteurs Save/Thème non renseignés/incorrects, étape ignorée ({e})")
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


def create_title_card(duration):
    """Génère le clip vidéo de la page de garde en utilisant APP_SETTINGS."""
    print(f"🎨 Création de la page de garde ({duration:.1f}s)...")

    bg_clip = mp.ColorClip(size=(1920, 1080), color=APP_SETTINGS["bg_color"]).with_duration(duration)

    try:
        title_clip = mp.TextClip(
            text=APP_SETTINGS["title"].upper(),
            font="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            font_size=120,
            color="white"
        ).with_duration(duration).with_position(("center", 200))

        subtitle_clip = mp.TextClip(
            text=APP_SETTINGS["subtitle"],
            font="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            font_size=50,
            color="white",
            text_align="center"
        ).with_duration(duration).with_position(("center", 380))
    except Exception:
        title_clip = subtitle_clip = mp.ColorClip(size=(1, 1), color=(0, 0, 0, 0)).with_duration(duration)

    try:
        accent_box = mp.ColorClip(size=(800, 10), color=APP_SETTINGS["accent_color"]).with_duration(duration).with_position(("center", 520))

        footer_clip = mp.TextClip(
            text=APP_SETTINGS["footer_tagline"],
            font="/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
            font_size=36,
            color="white"
        ).with_duration(duration).with_position(("center", 800))

        return mp.CompositeVideoClip([bg_clip, title_clip, subtitle_clip, accent_box, footer_clip], size=(1920, 1080))
    except Exception:
        return mp.CompositeVideoClip([bg_clip, title_clip], size=(1920, 1080))


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


if __name__ == "__main__":
    asyncio.run(main())
