import requests
import os
import re
import concurrent.futures
import json
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Definisce il percorso della cartella dello script e della cartella principale
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.dirname(script_dir)

def headers_to_extvlcopt(headers):
    """Converte un dizionario di header in una lista di stringhe #EXTVLCOPT per VLC."""
    vlc_opts = []
    for key, value in headers.items():
        # VLC usa nomi di header in minuscolo
        vlc_opts.append(f'#EXTVLCOPT:http-{key.lower()}={value}')
    return vlc_opts

def merger_playlist():
    # Codice del primo script qui
    # Aggiungi il codice del tuo script "merger_playlist.py" in questa funzione.
    # Ad esempio:
    print("Eseguendo il merger_playlist.py...")
    import requests
    import os
    from dotenv import load_dotenv
    import re

    def parse_m3u_for_sorting(file_path):
        """Legge un file M3U e restituisce una lista di tuple (nome_canale, righe_canale)"""
        channels = []
        if not os.path.exists(file_path):
            print(f"[AVVISO] File non trovato, impossibile ordinarlo: {file_path}")
            return channels
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith('#EXTINF:'):
                channel_name_match = re.search(r',(.+)', line)
                channel_name = channel_name_match.group(1).strip() if channel_name_match else "SenzaNome"
                
                # Un canale può avere più righe (es. #EXTVLCOPT)
                channel_block = [line]
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('#EXTINF:'):
                    channel_block.append(lines[i].strip())
                    i += 1
                channels.append((channel_name, channel_block))
            else:
                i += 1
        return channels
        
    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    NOMEREPO = os.getenv("NOMEREPO", "").strip()
    NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
    
    # Percorsi o URL delle playlist M3U8
    url_vavoo = os.path.join(output_dir, "vavoo.m3u")
    url_dlhd = os.path.join(output_dir, "dlhd.m3u")
    url_mpd = os.path.join(output_dir, "mpd.m3u")
    url_eventi = os.path.join(output_dir, "eventi_dlhd.m3u")
    url_sportsonline = os.path.join(output_dir, "sportsonline.m3u")
    url_streamed = os.path.join(output_dir, "streamed.m3u")
    url6 = "https://raw.githubusercontent.com/Brenders/Pluto-TV-Italia-M3U/main/PlutoItaly.m3u"
    
    # Funzione per scaricare o leggere una playlist
    def download_playlist(source, append_params=False, exclude_group_title=None):
        if source.startswith("http"):
            response = requests.get(source, timeout=30)
            response.raise_for_status()
            playlist = response.text
        else:
            with open(source, 'r', encoding='utf-8') as f:
                playlist = f.read()
        
        # Rimuovi intestazione iniziale
        playlist = '\n'.join(line for line in playlist.split('\n') if not line.startswith('#EXTM3U'))
    
        if exclude_group_title:
            playlist = '\n'.join(line for line in playlist.split('\n') if exclude_group_title not in line)
    
        return playlist
    
    # 1. Unisci e ordina i canali italiani (Vavoo e Daddylive)
    print("Unione e ordinamento dei canali italiani (Vavoo, Daddylive & MPD)...")
    vavoo_channels = parse_m3u_for_sorting(url_vavoo)
    dlhd_channels = parse_m3u_for_sorting(url_dlhd)
    mpd_channels = parse_m3u_for_sorting(url_mpd)
    
    all_italian_channels = vavoo_channels + dlhd_channels + mpd_channels
    all_italian_channels.sort(key=lambda x: x[0].lower()) # Ordina per nome canale
    
    sorted_italian_playlist = ""
    for _, channel_block in all_italian_channels:
        sorted_italian_playlist += "\n".join(channel_block) + "\n"

    # 2. Scarica le altre playlist
    print("Download delle altre playlist...")
    
    canali_daddy_flag = os.getenv("CANALI_DADDY", "no").strip().lower()
    if canali_daddy_flag == "si":
        playlist_eventi = download_playlist(url_eventi, append_params=True)
    else:
        print("[INFO] Skipping eventi_dlhd.m3u8 in merger_playlist as CANALI_DADDY is not 'si'.")
        playlist_eventi = ""

    playlist_sportsonline = download_playlist(url_sportsonline)
    playlist_streamed = download_playlist(url_streamed)
    playlist_pluto = download_playlist(url6)
    
    # 3. Unisci tutte le playlist (con i canali italiani ordinati all'inizio)
    lista = sorted_italian_playlist + "\n" + playlist_eventi + "\n" + playlist_sportsonline + "\n" + playlist_streamed + "\n" + playlist_pluto
    
    # Aggiungi intestazione EPG
    lista = f'#EXTM3U url-tvg="https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/refs/heads/main/epg.xml"\n' + lista
    
    # Salva la playlist
    output_filename = os.path.join(output_dir, "lista.m3u")
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(lista)
    
    print(f"Playlist combinata salvata in: {output_filename}")
    
# Funzione per il primo script (merger_playlist.py)
def merger_playlistworld():
    # Codice del primo script qui
    # Aggiungi il codice del tuo script "merger_playlist.py" in questa funzione.
    # Ad esempio:
    print("Eseguendo il merger_playlistworld.py...")
    import requests
    import os
    from dotenv import load_dotenv
    import re

    def parse_m3u_for_sorting(file_path):
        """Legge un file M3U e restituisce una lista di tuple (nome_canale, righe_canale)"""
        channels = []
        if not os.path.exists(file_path):
            print(f"[AVVISO] File non trovato, impossibile ordinarlo: {file_path}")
            return channels
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith('#EXTINF:'):
                channel_name_match = re.search(r',(.+)', line)
                channel_name = channel_name_match.group(1).strip() if channel_name_match else "SenzaNome"
                
                channel_block = [line]
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('#EXTINF:'):
                    channel_block.append(lines[i].strip())
                    i += 1
                channels.append((channel_name, channel_block))
            else:
                i += 1
        return channels
        
    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    NOMEREPO = os.getenv("NOMEREPO", "").strip()
    NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
    
    # Percorsi o URL delle playlist M3U8
    url_vavoo = os.path.join(output_dir, "vavoo.m3u")
    url_dlhd = os.path.join(output_dir, "dlhd.m3u")
    url_mpd = os.path.join(output_dir, "mpd.m3u")
    url_eventi = os.path.join(output_dir, "eventi_dlhd.m3u")
    url_sportsonline = os.path.join(output_dir, "sportsonline.m3u")
    url_streamed = os.path.join(output_dir, "streamed.m3u")
    url5 = "https://raw.githubusercontent.com/Brenders/Pluto-TV-Italia-M3U/main/PlutoItaly.m3u"
    url_world = os.path.join(output_dir, "world.m3u")
    
    # Funzione per scaricare o leggere una playlist
    def download_playlist(source, append_params=False, exclude_group_title=None):
        if source.startswith("http"):
            response = requests.get(source, timeout=30)
            response.raise_for_status()
            playlist = response.text
        else:
            with open(source, 'r', encoding='utf-8') as f:
                playlist = f.read()
        
        # Rimuovi intestazione iniziale
        playlist = '\n'.join(line for line in playlist.split('\n') if not line.startswith('#EXTM3U'))
    
        if exclude_group_title:
            playlist = '\n'.join(line for line in playlist.split('\n') if exclude_group_title not in line)
    
        return playlist
    
    # 1. Unisci e ordina i canali italiani (Vavoo e Daddylive)
    print("Unione e ordinamento dei canali italiani (Vavoo, Daddylive & MPD)...")
    vavoo_channels = parse_m3u_for_sorting(url_vavoo)
    dlhd_channels = parse_m3u_for_sorting(url_dlhd)
    mpd_channels = parse_m3u_for_sorting(url_mpd)
    
    all_italian_channels = vavoo_channels + dlhd_channels + mpd_channels
    all_italian_channels.sort(key=lambda x: x[0].lower()) # Ordina per nome canale
    
    sorted_italian_playlist = ""
    for _, channel_block in all_italian_channels:
        sorted_italian_playlist += "\n".join(channel_block) + "\n"

    # 2. Scarica le altre playlist
    print("Download delle altre playlist...")
    
    canali_daddy_flag = os.getenv("CANALI_DADDY", "no").strip().lower()
    if canali_daddy_flag == "si":
        playlist_eventi = download_playlist(url_eventi, append_params=True)
    else:
        print("[INFO] Skipping eventi_dlhd.m3u8 in merger_playlistworld as CANALI_DADDY is not 'si'.")
        playlist_eventi = ""

    playlist_sportsonline = download_playlist(url_sportsonline)
    playlist_streamed = download_playlist(url_streamed)
    playlist_pluto = download_playlist(url5)
    playlist_world = download_playlist(url_world, exclude_group_title="Italy")
    # 3. Unisci tutte le playlist
    lista = sorted_italian_playlist + "\n" + playlist_eventi + "\n" + playlist_sportsonline + "\n" + playlist_streamed + "\n" + playlist_pluto + "\n" + playlist_world
    
    # Aggiungi intestazione EPG
    lista = f'#EXTM3U url-tvg="https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/refs/heads/main/epg.xml"\n' + lista
    
    # Salva la playlist
    output_filename = os.path.join(output_dir, "lista.m3u")
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(lista)
    
    print(f"Playlist combinata salvata in: {output_filename}")

# Funzione per il secondo script (epg_merger.py)
def epg_merger():
    # Codice del secondo script qui
    # Aggiungi il codice del tuo script "epg_merger.py" in questa funzione.
    # Ad esempio:
    print("Eseguendo l'epg_merger.py...")
    # Il codice che avevi nello script "epg_merger.py" va qui, senza modifiche.
    import requests
    import gzip
    import os
    import xml.etree.ElementTree as ET
    import io

    # URL dei file GZIP o XML da elaborare
    urls_gzip = [
        'https://www.open-epg.com/files/italy1.xml',
        'https://www.open-epg.com/files/italy2.xml',
        'https://www.open-epg.com/files/italy3.xml',
        'https://www.open-epg.com/files/italy4.xml',
        'https://epgshare01.online/epgshare01/epg_ripper_IT1.xml.gz'
    ]

    # File di output
    output_xml = os.path.join(output_dir, 'epg.xml')

    # URL remoto di it.xml
    url_it = 'https://raw.githubusercontent.com/matthuisman/i.mjh.nz/master/PlutoTV/it.xml'

    # Disabilita gli avvisi per le richieste non verificate
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

    # File eventi_dlhd locale
    path_eventi_dlhd = os.path.join(output_dir, 'eventi_dlhd.xml')

    def download_and_parse_xml(url):
        """Scarica un file .xml o .gzip e restituisce l'ElementTree."""
        try:
            # Aggiunto verify=False per ignorare gli errori SSL
            response = requests.get(url, timeout=30, verify=False)
            response.raise_for_status()

            # Prova a decomprimere come GZIP
            try:
                with gzip.open(io.BytesIO(response.content), 'rb') as f_in:
                    xml_content = f_in.read()
            except (gzip.BadGzipFile, OSError):
                # Non Ã¨ un file gzip, usa direttamente il contenuto
                xml_content = response.content

            return ET.ElementTree(ET.fromstring(xml_content))
        except requests.exceptions.RequestException as e:
            print(f"Errore durante il download da {url} (verifica SSL disabilitata): {e}")
        except ET.ParseError as e:
            print(f"Errore nel parsing del file XML da {url}: {e}")
        return None

    # Creare un unico XML vuoto
    root_finale = ET.Element('tv')
    tree_finale = ET.ElementTree(root_finale)

    # Processare ogni URL
    for url in urls_gzip:
        tree = download_and_parse_xml(url)
        if tree is not None:
            root = tree.getroot()
            for element in root:
                root_finale.append(element)

    # Check CANALI_DADDY flag before processing eventi_dlhd.xml
    canali_daddy_flag = os.getenv("CANALI_DADDY", "no").strip().lower()
    if canali_daddy_flag == "si":
        # Aggiungere eventi_dlhd.xml da file locale
        if os.path.exists(path_eventi_dlhd):
            try:
                tree_eventi_dlhd = ET.parse(path_eventi_dlhd)
                root_eventi_dlhd = tree_eventi_dlhd.getroot()
                for programme in root_eventi_dlhd.findall(".//programme"):
                    root_finale.append(programme)
            except ET.ParseError as e:
                print(f"Errore nel parsing del file eventi_dlhd.xml: {e}")
        else:
            print(f"File non trovato: {path_eventi_dlhd}")
    else:
        print("[INFO] Skipping eventi_dlhd.xml in epg_merger as CANALI_DADDY is not 'si'.")

    # Aggiungere it.xml da URL remoto
    tree_it = download_and_parse_xml(url_it)
    if tree_it is not None:
        root_it = tree_it.getroot()
        for programme in root_it.findall(".//programme"):
            root_finale.append(programme)
    else:
        print(f"Impossibile scaricare o analizzare il file it.xml da {url_it}")

    # Funzione per pulire attributi
    def clean_attribute(element, attr_name):
        if attr_name in element.attrib:
            old_value = element.attrib[attr_name]
            new_value = old_value.replace(" ", "").lower()
            element.attrib[attr_name] = new_value

    # Pulire gli ID dei canali
    for channel in root_finale.findall(".//channel"):
        clean_attribute(channel, 'id')

    # Pulire gli attributi 'channel' nei programmi
    for programme in root_finale.findall(".//programme"):
        clean_attribute(programme, 'channel')

    # Salvare il file XML finale
    with open(output_xml, 'wb') as f_out:
        tree_finale.write(f_out, encoding='utf-8', xml_declaration=True)
    print(f"File XML salvato: {output_xml}")

    # Salvare anche il file GZIP
    output_gz = os.path.join(output_dir, 'epg.xml.gz')
    with gzip.open(output_gz, 'wb') as f_gz:
        tree_finale.write(f_gz, encoding='utf-8', xml_declaration=True)
    print(f"File GZIP salvato: {output_gz}")
             
# Funzione per il terzo script (eventi_dlhd_m3u8_generator.py)
def eventi_dlhd_m3u8_generator_world():
    # Codice del terzo script qui
    # Aggiungi il codice del tuo script "eventi_dlhd_m3u8_generator.py" in questa funzione.
    print("Eseguendo l'eventi_dlhd_m3u8_generator.py...")
    # Il codice che avevi nello script "eventi_dlhd_m3u8_generator.py" va qui, senza modifiche.
    import json
    import re
    import requests
    import urllib.parse # Consolidato
    from datetime import datetime, timedelta
    from dateutil import parser
    import os
    from dotenv import load_dotenv
    from PIL import Image, ImageDraw, ImageFont
    import io # Aggiunto per encoding URL
    import time
    
    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    LINK_DADDY = os.getenv("LINK_DADDY", "").strip() or "https://dlhd.dad"
    JSON_FILE = os.path.join(script_dir, "daddyliveSchedule.json")
    OUTPUT_FILE = os.path.join(output_dir, "eventi_dlhd.m3u")
    HEADERS = { 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36" 
    } 
     
    HTTP_TIMEOUT = 10 
    session = requests.Session() 
    session.headers.update(HEADERS) 
    # Definisci current_time e three_hours_in_seconds per la logica di caching
    current_time = time.time()
    three_hours_in_seconds = 3 * 60 * 60
    
    def clean_category_name(name): 
        # Rimuove tag html come </span> o simili 
        return re.sub(r'<[^>]+>', '', name).strip()
        
    def clean_tvg_id(tvg_id):
        """
        Pulisce il tvg-id rimuovendo caratteri speciali, spazi e convertendo tutto in minuscolo
        """
        # import re # 're' Ã¨ giÃ  importato a livello di funzione
        # Rimuove caratteri speciali comuni mantenendo solo lettere e numeri
        cleaned = re.sub(r'[^a-zA-Z0-9À-ÿ]', '', tvg_id)
        return cleaned.lower()
     
    def search_logo_for_event(event_name): 
        """ 
        Cerca un logo per l'evento specificato utilizzando un motore di ricerca 
        Restituisce l'URL dell'immagine trovata o None se non trovata 
        """ 
        try: 
            # Rimuovi eventuali riferimenti all'orario dal nome dell'evento
            # Cerca pattern come "Team A vs Team B (20:00)" e rimuovi la parte dell'orario
            clean_event_name = re.sub(r'\s*\(\d{1,2}:\d{2}\)\s*$', '', event_name)
            # Se c'ÃÂ¨ un ':', prendi solo la parte dopo
            if ':' in clean_event_name:
                clean_event_name = clean_event_name.split(':', 1)[1].strip()
            
            # Verifica se l'evento contiene "vs" o "-" per identificare le due squadre
            teams = None
            if " vs " in clean_event_name:
                teams = clean_event_name.split(" vs ")
            elif " VS " in clean_event_name:
                teams = clean_event_name.split(" VS ")
            elif " VS. " in clean_event_name:
                teams = clean_event_name.split(" VS. ")
            elif " vs. " in clean_event_name:
                teams = clean_event_name.split(" vs. ")
            
            # Se abbiamo identificato due squadre, cerchiamo i loghi separatamente
            if teams and len(teams) == 2:
                team1 = teams[0].strip()
                team2 = teams[1].strip()
                
                print(f"[🔍] Ricerca logo per Team 1: {team1}")
                logo1_url = search_team_logo(team1)
                
                print(f"[🔍] Ricerca logo per Team 2: {team2}")
                logo2_url = search_team_logo(team2)
                
                # Se abbiamo trovato entrambi i loghi, creiamo un'immagine combinata
                if logo1_url and logo2_url:
                    # Scarica i loghi e l'immagine VS
                    try:
                        from os.path import exists, getmtime
                        
                        # Crea la cartella logos se non esiste
                        logos_dir = os.path.join(output_dir, "logos")
                        os.makedirs(logos_dir, exist_ok=True)
                        
                        # Verifica se l'immagine combinata esiste giÃÂ  e non ÃÂ¨ obsoleta
                        relative_logo_path = os.path.join("logos", f"{team1}_vs_{team2}.png")
                        absolute_output_filename = os.path.join(output_dir, relative_logo_path)
                        if exists(absolute_output_filename):
                            file_age = current_time - os.path.getmtime(absolute_output_filename)
                            if file_age <= three_hours_in_seconds:
                                print(f"[✓] Utilizzo immagine combinata esistente: {absolute_output_filename}")
                                
                                # Carica le variabili d'ambiente per GitHub
                                NOMEREPO = os.getenv("NOMEREPO", "").strip()
                                NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
                                
                                # Se le variabili GitHub sono disponibili, restituisci l'URL raw di GitHub
                                if NOMEGITHUB and NOMEREPO:
                                    github_raw_url = f"https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/main/{relative_logo_path}"
                                    print(f"[✓] URL GitHub generato per logo esistente: {github_raw_url}")
                                    return github_raw_url
                                else:
                                    # Altrimenti restituisci il percorso locale
                                    return absolute_output_filename
                        
                        # Scarica i loghi
                        img1, img2 = None, None
                        
                        if logo1_url:
                            try:
                                # Aggiungi un User-Agent simile a un browser
                                logo_headers = {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                                }
                                response1 = requests.get(logo1_url, headers=logo_headers, timeout=10)
                                response1.raise_for_status() # Controlla errori HTTP
                                if 'image' in response1.headers.get('Content-Type', '').lower():
                                    img1 = Image.open(io.BytesIO(response1.content))
                                    print(f"[✓] Logo1 scaricato con successo da: {logo1_url}")
                                else:
                                    print(f"[!] URL logo1 ({logo1_url}) non è un'immagine (Content-Type: {response1.headers.get('Content-Type')}).")
                                    logo1_url = None # Invalida URL se non è un'immagine
                            except requests.exceptions.RequestException as e_req:
                                print(f"[!] Errore scaricando logo1 ({logo1_url}): {e_req}")
                                logo1_url = None
                            except Exception as e_pil: # Errore specifico da PIL durante Image.open
                                print(f"[!] Errore PIL aprendo logo1 ({logo1_url}): {e_pil}")
                                logo1_url = None
                        
                        if logo2_url:
                            try:
                                # Aggiungi un User-Agent simile a un browser
                                logo_headers = {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                                }
                                response2 = requests.get(logo2_url, headers=logo_headers, timeout=10)
                                response2.raise_for_status() # Controlla errori HTTP
                                if 'image' in response2.headers.get('Content-Type', '').lower():
                                    img2 = Image.open(io.BytesIO(response2.content))
                                    print(f"[✓] Logo2 scaricato con successo da: {logo2_url}")
                                else:
                                    print(f"[!] URL logo2 ({logo2_url}) non è un'immagine (Content-Type: {response2.headers.get('Content-Type')}).")
                                    logo2_url = None # Invalida URL se non è un'immagine
                            except requests.exceptions.RequestException as e_req:
                                print(f"[!] Errore scaricando logo2 ({logo2_url}): {e_req}")
                                logo2_url = None
                            except Exception as e_pil: # Errore specifico da PIL durante Image.open
                                print(f"[!] Errore PIL aprendo logo2 ({logo2_url}): {e_pil}")
                                logo2_url = None
                        
                        # Carica l'immagine VS (assicurati che esista nella directory corrente)
                        vs_path = os.path.join(script_dir, "vs.png")
                        if exists(vs_path):
                            img_vs = Image.open(vs_path)
                            # Converti l'immagine VS in modalitÃÂ  RGBA se non lo ÃÂ¨ giÃÂ 
                            if img_vs.mode != 'RGBA':
                                img_vs = img_vs.convert('RGBA')
                        else:
                            # Crea un'immagine di testo "VS" se il file non esiste
                            img_vs = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
                            from PIL import ImageDraw, ImageFont
                            draw = ImageDraw.Draw(img_vs)
                            try:
                                font = ImageFont.truetype("arial.ttf", 40)
                            except:
                                font = ImageFont.load_default()
                            draw.text((30, 30), "VS", fill=(255, 0, 0), font=font)
                        
                        # Procedi con la combinazione solo se entrambi i loghi sono stati caricati con successo
                        if not (img1 and img2):
                            print(f"[!] Impossibile caricare entrambi i loghi come immagini valide per la combinazione. Logo1 caricato: {bool(img1)}, Logo2 caricato: {bool(img2)}.")
                            raise ValueError("Uno o entrambi i loghi non sono stati caricati correttamente.") # Questo forzerÃ  l'except sottostante
                        
                        # Ridimensiona le immagini a dimensioni uniformi
                        size = (150, 150)
                        img1 = img1.resize(size)
                        img2 = img2.resize(size)
                        img_vs = img_vs.resize((100, 100))
                        
                        # Assicurati che tutte le immagini siano in modalitÃÂ  RGBA per supportare la trasparenza
                        if img1.mode != 'RGBA':
                            img1 = img1.convert('RGBA')
                        if img2.mode != 'RGBA':
                            img2 = img2.convert('RGBA')
                        
                        # Crea una nuova immagine con spazio per entrambi i loghi e il VS
                        combined_width = 300
                        combined = Image.new('RGBA', (combined_width, 150), (255, 255, 255, 0))
                        
                        # Posiziona le immagini con il VS sovrapposto al centro
                        # Posiziona il primo logo a sinistra
                        combined.paste(img1, (0, 0), img1)
                        # Posiziona il secondo logo a destra
                        combined.paste(img2, (combined_width - 150, 0), img2)
                        
                        # Posiziona il VS al centro, sovrapposto ai due loghi
                        vs_x = (combined_width - 100) // 2
                        
                        # Crea una copia dell'immagine combinata prima di sovrapporre il VS
                        # Questo passaggio ÃÂ¨ importante per preservare i dettagli dei loghi sottostanti
                        combined_with_vs = combined.copy()
                        combined_with_vs.paste(img_vs, (vs_x, 25), img_vs)
                        
                        # Usa l'immagine con VS sovrapposto
                        combined = combined_with_vs
                        
                        # Salva l'immagine combinata
                        combined.save(absolute_output_filename)
                        
                        print(f"[✓] Immagine combinata creata: {absolute_output_filename}")
                        
                        # Carica le variabili d'ambiente per GitHub
                        NOMEREPO = os.getenv("NOMEREPO", "").strip()
                        NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
                        
                        # Se le variabili GitHub sono disponibili, restituisci l'URL raw di GitHub
                        if NOMEGITHUB and NOMEREPO:
                            github_raw_url = f"https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/main/{relative_logo_path}"
                            print(f"[✓] URL GitHub generato: {github_raw_url}")
                            return github_raw_url
                        else:
                            # Altrimenti restituisci il percorso assoluto
                            return absolute_output_filename
                        
                    except Exception as e:
                        print(f"[!] Errore nella creazione dell'immagine combinata: {e}")
                        # Se fallisce, restituisci solo il primo logo trovato
                        return logo1_url or logo2_url
                
                # Se non abbiamo trovato entrambi i loghi, restituisci quello che abbiamo
                return logo1_url or logo2_url
            if ':' in event_name:
                # Usa la parte prima dei ":" per la ricerca
                prefix_name = event_name.split(':', 1)[0].strip()
                print(f"[🔍] Tentativo ricerca logo con prefisso: {prefix_name}")
                
                # Prepara la query di ricerca con il prefisso
                search_query = urllib.parse.quote(f"{prefix_name} logo")
                
                # Utilizziamo l'API di Bing Image Search con parametri migliorati
                search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent+filterui:aspect-square&form=IRFLTR"
                
                headers = { 
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Cache-Control": "max-age=0",
                    "Connection": "keep-alive"
                } 
                
                response = requests.get(search_url, headers=headers, timeout=10)
                
                if response.status_code == 200: 
                    # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
                    patterns = [
                        r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                        r'"murl":"(https?://[^"]+)"',
                        r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                        r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                        r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, response.text)
                        if matches and len(matches) > 0:
                            # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                            for match in matches:
                                if '.png' in match.lower() or '.svg' in match.lower():
                                    print(f"[✓] Logo trovato con prefisso: {match}")
                                    return match
                            # Se non troviamo PNG o SVG, prendi il primo risultato
                            print(f"[✓] Logo trovato con prefisso: {matches[0]}")
                            return matches[0]
            
            # Se non riusciamo a identificare le squadre e il prefisso non ha dato risultati, procedi con la ricerca normale
            print(f"[🔍] Ricerca standard per: {clean_event_name}")
            
            
            # Se non riusciamo a identificare le squadre, procedi con la ricerca normale
            # Prepara la query di ricerca piÃÂ¹ specifica
            search_query = urllib.parse.quote(f"{clean_event_name} logo")
            
            # Utilizziamo l'API di Bing Image Search con parametri migliorati
            search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent+filterui:aspect-square&form=IRFLTR"
            
            headers = { 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive"
            } 
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200: 
                # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
                patterns = [
                    r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                    r'"murl":"(https?://[^"]+)"',
                    r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                    r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                    r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, response.text)
                    if matches and len(matches) > 0:
                        # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                        for match in matches:
                            if '.png' in match.lower() or '.svg' in match.lower():
                                return match
                        # Se non troviamo PNG o SVG, prendi il primo risultato
                        return matches[0]
                
                # Metodo alternativo: cerca JSON incorporato nella pagina
                json_match = re.search(r'var\s+IG\s*=\s*(\{.+?\});\s*', response.text)
                if json_match:
                    try:
                        # Estrai e analizza il JSON
                        json_str = json_match.group(1)
                        # Pulisci il JSON se necessario
                        json_str = re.sub(r'([{,])\s*([a-zA-Z0-9_]+):', r'\1"\2":', json_str)
                        data = json.loads(json_str)
                        
                        # Cerca URL di immagini nel JSON
                        if 'images' in data and len(data['images']) > 0:
                            for img in data['images']:
                                if 'murl' in img:
                                    return img['murl']
                    except Exception as e:
                        print(f"[!] Errore nell'analisi JSON: {e}")
                
                print(f"[!] Nessun logo trovato per '{clean_event_name}' con i pattern standard")
                
                # Ultimo tentativo: cerca qualsiasi URL di immagine nella pagina
                any_img = re.search(r'(https?://[^"\']+\.(?:png|jpg|jpeg|svg|webp))', response.text)
                if any_img:
                    return any_img.group(1)
                    
        except Exception as e: 
            print(f"[!] Errore nella ricerca del logo per '{event_name}': {e}") 
        
        # Se non troviamo nulla, restituiamo None 
        return None

    def search_team_logo(team_name):
        """
        Funzione dedicata alla ricerca del logo di una singola squadra
        """
        try:
            # Prepara la query di ricerca specifica per la squadra
            search_query = urllib.parse.quote(f"{team_name} logo")
            
            # Utilizziamo l'API di Bing Image Search con parametri migliorati
            search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent+filterui:aspect-square&form=IRFLTR"
            
            headers = { 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive"
            } 
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200: 
                # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
                patterns = [
                    r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                    r'"murl":"(https?://[^"]+)"',
                    r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                    r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                    r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, response.text)
                    if matches and len(matches) > 0:
                        # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                        for match in matches:
                            if '.png' in match.lower() or '.svg' in match.lower():
                                return match
                        # Se non troviamo PNG o SVG, prendi il primo risultato
                        return matches[0]
                
                # Metodo alternativo: cerca JSON incorporato nella pagina
                json_match = re.search(r'var\s+IG\s*=\s*(\{.+?\});\s*', response.text)
                if json_match:
                    try:
                        # Estrai e analizza il JSON
                        json_str = json_match.group(1)
                        # Pulisci il JSON se necessario
                        json_str = re.sub(r'([{,])\s*([a-zA-Z0-9_]+):', r'\1"\2":', json_str)
                        data = json.loads(json_str)
                        
                        # Cerca URL di immagini nel JSON
                        if 'images' in data and len(data['images']) > 0:
                            for img in data['images']:
                                if 'murl' in img:
                                    return img['murl']
                    except Exception as e:
                        print(f"[!] Errore nell'analisi JSON: {e}")
                
                print(f"[!] Nessun logo trovato per '{team_name}' con i pattern standard")
                
                # Ultimo tentativo: cerca qualsiasi URL di immagine nella pagina
                any_img = re.search(r'(https?://[^"\']+\.(?:png|jpg|jpeg|svg|webp))', response.text)
                if any_img:
                    return any_img.group(1)
                    
        except Exception as e: 
            print(f"[!] Errore nella ricerca del logo per '{team_name}': {e}") 
        
        # Se non troviamo nulla, restituiamo None 
        return None
     
    def get_stream_from_channel_id(channel_id): 
        # Restituisce direttamente l'URL .php
        embed_url = f"{LINK_DADDY}/watch.php?id={channel_id}" 
        print(f"URL .php per il canale Daddylive {channel_id}.")
        return embed_url
     
    # def clean_category_name(name): # Rimossa definizione duplicata
    #     # Rimuove tag html come </span> o simili
    #     return re.sub(r'<[^>]+>', '', name).strip()
     
    def extract_channels_from_json(path): 
        keywords = {"italy", "rai", "italia", "it", "uk", "tnt", "usa", "tennis channel", "tennis stream", "la"} 
        now = datetime.now()  # ora attuale completa (data+ora) 
        yesterday_date = (now - timedelta(days=1)).date() # Data di ieri
     
        with open(path, "r", encoding="utf-8") as f: 
            data = json.load(f) 
     
        categorized_channels = {} 
     
        for date_key, sections in data.items(): 
            date_part = date_key.split(" - ")[0] 
            try: 
                date_obj = parser.parse(date_part, fuzzy=True).date() 
            except Exception as e: 
                print(f"[!] Errore parsing data '{date_part}': {e}") 
                continue 
            
            # Determina se processare questa data
            process_this_date = False
            is_yesterday_early_morning_event_check = False

            if date_obj == now.date():
                process_this_date = True
            elif date_obj == yesterday_date:
                process_this_date = True
                is_yesterday_early_morning_event_check = True # Flag per eventi_dlhd di ieri mattina presto
            else:
                # Salta date che non sono nÃ© oggi nÃ© ieri
                continue

            if not process_this_date:
                continue
     
            for category_raw, event_items in sections.items(): 
                category = clean_category_name(category_raw)
                # Salta la categoria TV Shows
                if category.lower() == "tv shows":
                    continue
                if category not in categorized_channels: 
                    categorized_channels[category] = [] 
     
                for item in event_items: 
                    time_str = item.get("time", "00:00") # Orario originale dal JSON
                    event_title = item.get("event", "Evento") 
     
                    try: 
                        # Parse orario evento originale (dal JSON)
                        original_event_time_obj = datetime.strptime(time_str, "%H:%M").time()

                        # Costruisci datetime completo dell'evento con la sua data originale
                        # e l'orario originale, poi applica il timedelta(hours=2) (per "correzione timezone?")
                        # Questo event_datetime_adjusted Ã¨ quello che viene usato per il filtro "meno di 2 ore fa" per oggi
                        # e per il nome del canale.
                        event_datetime_adjusted_for_display_and_filter = datetime.combine(date_obj, original_event_time_obj) + timedelta(hours=2)

                        if is_yesterday_early_morning_event_check:
                            # Filtro per eventi_dlhd di ieri mattina presto (00:00 - 04:00, ora JSON)
                            start_filter_time = datetime.strptime("00:00", "%H:%M").time()
                            end_filter_time = datetime.strptime("04:00", "%H:%M").time()
                            # Confronta l'orario originale dell'evento
                            if not (start_filter_time <= original_event_time_obj <= end_filter_time):
                                # Evento di ieri, ma non nell'intervallo 00:00-04:00 -> salto
                                continue
                        else: # eventi_dlhd di oggi
                            # Controllo: includi solo se l'evento Ã¨ iniziato da meno di 2 ore
                            # Usa event_datetime_adjusted_for_display_and_filter che ha giÃ  il +2h
                            if now - event_datetime_adjusted_for_display_and_filter > timedelta(hours=2):
                                # Evento di oggi iniziato da piÃ¹ di 2 ore -> salto
                                continue
                        
                        time_formatted = event_datetime_adjusted_for_display_and_filter.strftime("%H:%M")
                    except Exception as e_time:
                        print(f"[!] Errore parsing orario '{time_str}' per evento '{event_title}' in data '{date_key}': {e_time}")
                        time_formatted = time_str # Fallback
     
                    for ch in item.get("channels", []): 
                        channel_name = ch.get("channel_name", "") 
                        channel_id = ch.get("channel_id", "") 
     
                        words = set(re.findall(r'\b\w+\b', channel_name.lower())) 
                        if keywords.intersection(words): 
                            tvg_name = f"{event_title} ({time_formatted})" 
                            categorized_channels[category].append({ 
                                "tvg_name": tvg_name, 
                                "channel_name": channel_name, 
                                "channel_id": channel_id,
                                "event_title": event_title  # Aggiungiamo il titolo dell'evento per la ricerca del logo
                            }) 
     
        return categorized_channels 
     
    def generate_m3u_from_schedule(json_file, output_file): 
        categorized_channels = extract_channels_from_json(json_file) 

        with open(output_file, "w", encoding="utf-8") as f: 
            f.write("#EXTM3U\n") 

            # Controlla se ci sono eventi_dlhd prima di aggiungere il canale DADDYLIVE
            has_events = any(channels for channels in categorized_channels.values())
            
            if has_events:
                # Aggiungi il canale iniziale/informativo solo se ci sono eventi_dlhd
                f.write(f'#EXTINF:-1 tvg-name="DADDYLIVE" group-title="Eventi Live DLHD",DADDYLIVE\n')
                f.write("https://example.com.m3u8\n\n")
            else:
                print("[ℹ️] Nessun evento trovato, canale DADDYLIVE non aggiunto.")

            for category, channels in categorized_channels.items(): 
                if not channels: 
                    continue 
          
                for ch in channels: 
                    tvg_name = ch["tvg_name"] 
                    channel_id = ch["channel_id"] 
                    event_title = ch["event_title"]  # Otteniamo il titolo dell'evento
                    channel_name = ch["channel_name"]
                    
                    # Cerca un logo per questo evento
                    # Rimuovi l'orario dal titolo dell'evento prima di cercare il logo
                    clean_event_title = re.sub(r'\s*\(\d{1,2}:\d{2}\)\s*$', '', event_title)
                    print(f"[🔍] Ricerca logo per: {clean_event_title}") 
                    logo_url = search_logo_for_event(clean_event_title)
                    logo_attribute = f' tvg-logo="{logo_url}"' if logo_url else ''
     
                    try: 
                        # Cerca lo stream .m3u8 nei siti specificati
                        stream = get_stream_from_channel_id(channel_id)
                                                    
                        if stream: 
                            cleaned_event_id = clean_tvg_id(event_title) # Usa event_title per tvg-id
                            f.write(f'#EXTINF:-1 tvg-id="{cleaned_event_id}" tvg-name="{category} | {tvg_name}"{logo_attribute} group-title="Eventi Live DLHD",{category} | {tvg_name}\n')
                            # Aggiungi EXTHTTP headers per canali daddy (esclusi .php)
                            if "ava.karmakurama.com" in stream and not stream.endswith('.php'):
                                daddy_headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1", "Referrer": "https://ava.karmakurama.com/", "Origin": "https://ava.karmakurama.com"}
                                vlc_opt_lines = headers_to_extvlcopt(daddy_headers)
                                for line in vlc_opt_lines:
                                    f.write(f'{line}\n')
                            f.write(f'{stream}\n\n')
                            print(f"[✓] {tvg_name}" + (f" (logo trovato)" if logo_url else " (nessun logo trovato)")) 
                        else: 
                            print(f"[✗] {tvg_name} - Nessuno stream trovato") 
                    except Exception as e: 
                        print(f"[!] Errore su {tvg_name}: {e}") 
     
    # Esegui la generazione quando la funzione viene chiamata
    generate_m3u_from_schedule(JSON_FILE, OUTPUT_FILE)

# Funzione per il terzo script (eventi_dlhd_m3u8_generator.py)
def eventi_dlhd_m3u8_generator():
    # Codice del terzo script qui
    # Aggiungi il codice del tuo script "eventi_dlhd_m3u8_generator.py" in questa funzione.
    print("Eseguendo l'eventi_dlhd_m3u8_generator.py...")
    # Il codice che avevi nello script "eventi_dlhd_m3u8_generator.py" va qui, senza modifiche.
    import json 
    import re 
    import requests 
    from urllib.parse import quote 
    from datetime import datetime, timedelta 
    from dateutil import parser 
    import urllib.parse
    import os
    from dotenv import load_dotenv
    from PIL import Image, ImageDraw, ImageFont
    import io
    import urllib.parse # Aggiunto per encoding URL
    import time

    # Carica le variabili d'ambiente dal file .env
    load_dotenv()
    LINK_DADDY = os.getenv("LINK_DADDY", "").strip() or "https://dlhd.dad"
    JSON_FILE = os.path.join(script_dir, "daddyliveSchedule.json") # Cache in scripts
    OUTPUT_FILE = os.path.join(output_dir, "eventi_dlhd.m3u") # Output in main dir
     
    HEADERS = { 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36" 
    } 
     
    HTTP_TIMEOUT = 10 
    session = requests.Session() 
    session.headers.update(HEADERS) 
    # Definisci current_time e three_hours_in_seconds per la logica di caching
    current_time = time.time()
    three_hours_in_seconds = 3 * 60 * 60
    
    def clean_category_name(name): 
        # Rimuove tag html come </span> o simili 
        return re.sub(r'<[^>]+>', '', name).strip()
        
    def clean_tvg_id(tvg_id):
        """
        Pulisce il tvg-id rimuovendo caratteri speciali, spazi e convertendo tutto in minuscolo.
        """
        import re
        # Rimuove caratteri speciali comuni mantenendo solo lettere e numeri
        cleaned = re.sub(r'[^a-zA-Z0-9À-ÿ]', '', tvg_id)
        return cleaned.lower()
     
    def search_logo_for_event(event_name): 
        """ 
        Cerca un logo per l'evento specificato utilizzando un motore di ricerca 
        Restituisce l'URL dell'immagine trovata o None se non trovata 
        """ 
        try: 
            # Rimuovi eventuali riferimenti all'orario dal nome dell'evento
            # Cerca pattern come "Team A vs Team B (20:00)" e rimuovi la parte dell'orario
            clean_event_name = re.sub(r'\s*\(\d{1,2}:\d{2}\)\s*$', '', event_name)
            # Se c'è un ':', prendi solo la parte dopo
            if ':' in clean_event_name:
                clean_event_name = clean_event_name.split(':', 1)[1].strip()
            
            # Verifica se l'evento contiene "vs" o "-" per identificare le due squadre
            teams = None
            if " vs " in clean_event_name:
                teams = clean_event_name.split(" vs ")
            elif " VS " in clean_event_name:
                teams = clean_event_name.split(" VS ")
            elif " VS. " in clean_event_name:
                teams = clean_event_name.split(" VS. ")
            elif " vs. " in clean_event_name:
                teams = clean_event_name.split(" vs. ")
            
            # Se abbiamo identificato due squadre, cerchiamo i loghi separatamente
            if teams and len(teams) == 2:
                team1 = teams[0].strip()
                team2 = teams[1].strip()
                
                print(f"[🔍] Ricerca logo per Team 1: {team1}")
                logo1_url = search_team_logo(team1)
                
                print(f"[🔍] Ricerca logo per Team 2: {team2}")
                logo2_url = search_team_logo(team2)
                
                # Se abbiamo trovato entrambi i loghi, creiamo un'immagine combinata
                if logo1_url and logo2_url:
                    # Scarica i loghi e l'immagine VS
                    try:
                        from os.path import exists, getmtime
                        
                        # Crea la cartella logos se non esiste
                        logos_dir = os.path.join(output_dir, "logos")
                        os.makedirs(logos_dir, exist_ok=True)
                        
                        # Verifica se l'immagine combinata esiste giÃÂ  e non ÃÂ¨ obsoleta
                        relative_logo_path = os.path.join("logos", f"{team1}_vs_{team2}.png")
                        absolute_output_filename = os.path.join(output_dir, relative_logo_path)
                        if exists(absolute_output_filename):
                            file_age = current_time - os.path.getmtime(absolute_output_filename)
                            if file_age <= three_hours_in_seconds:
                                print(f"[✓] Utilizzo immagine combinata esistente: {absolute_output_filename}")
                                
                                # Carica le variabili d'ambiente per GitHub
                                NOMEREPO = os.getenv("NOMEREPO", "").strip()
                                NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
                                
                                # Se le variabili GitHub sono disponibili, restituisci l'URL raw di GitHub
                                if NOMEGITHUB and NOMEREPO:
                                    github_raw_url = f"https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/main/{relative_logo_path}"
                                    print(f"[✓] URL GitHub generato per logo esistente: {github_raw_url}")
                                    return github_raw_url
                                else:
                                    # Altrimenti restituisci il percorso locale
                                    return absolute_output_filename
                        
                        # Scarica i loghi
                        img1, img2 = None, None
                        
                        if logo1_url:
                            try:
                                # Aggiungi un User-Agent simile a un browser
                                logo_headers = {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                                }
                                response1 = requests.get(logo1_url, headers=logo_headers, timeout=10)
                                response1.raise_for_status() # Controlla errori HTTP
                                if 'image' in response1.headers.get('Content-Type', '').lower():
                                    img1 = Image.open(io.BytesIO(response1.content))
                                    print(f"[✓] Logo1 scaricato con successo da: {logo1_url}")
                                else:
                                    print(f"[!] URL logo1 ({logo1_url}) non è un'immagine (Content-Type: {response1.headers.get('Content-Type')}).")
                                    logo1_url = None # Invalida URL se non è un'immagine
                            except requests.exceptions.RequestException as e_req:
                                print(f"[!] Errore scaricando logo1 ({logo1_url}): {e_req}")
                                logo1_url = None
                            except Exception as e_pil: # Errore specifico da PIL durante Image.open
                                print(f"[!] Errore PIL aprendo logo1 ({logo1_url}): {e_pil}")
                                logo1_url = None
                        
                        if logo2_url:
                            try:
                                # Aggiungi un User-Agent simile a un browser
                                logo_headers = {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                                }
                                response2 = requests.get(logo2_url, headers=logo_headers, timeout=10)
                                response2.raise_for_status() # Controlla errori HTTP
                                if 'image' in response2.headers.get('Content-Type', '').lower():
                                    img2 = Image.open(io.BytesIO(response2.content))
                                    print(f"[✓] Logo2 scaricato con successo da: {logo2_url}")
                                else:
                                    print(f"[!] URL logo2 ({logo2_url}) non è un'immagine (Content-Type: {response2.headers.get('Content-Type')}).")
                                    logo2_url = None # Invalida URL se non è un'immagine
                            except requests.exceptions.RequestException as e_req:
                                print(f"[!] Errore scaricando logo2 ({logo2_url}): {e_req}")
                                logo2_url = None
                            except Exception as e_pil: # Errore specifico da PIL durante Image.open
                                print(f"[!] Errore PIL aprendo logo2 ({logo2_url}): {e_pil}")
                                logo2_url = None
                        
                        # Carica l'immagine VS (assicurati che esista nella directory corrente)
                        vs_path = os.path.join(script_dir, "vs.png")
                        if exists(vs_path):
                            img_vs = Image.open(vs_path)
                            # Converti l'immagine VS in modalitÃÂ  RGBA se non lo ÃÂ¨ giÃÂ 
                            if img_vs.mode != 'RGBA':
                                img_vs = img_vs.convert('RGBA')
                        else:
                            # Crea un'immagine di testo "VS" se il file non esiste
                            img_vs = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
                            from PIL import ImageDraw, ImageFont
                            draw = ImageDraw.Draw(img_vs)
                            try:
                                font = ImageFont.truetype("arial.ttf", 40)
                            except:
                                font = ImageFont.load_default()
                            draw.text((30, 30), "VS", fill=(255, 0, 0), font=font)
                        
                        # Procedi con la combinazione solo se entrambi i loghi sono stati caricati con successo
                        if not (img1 and img2):
                            print(f"[!] Impossibile caricare entrambi i loghi come immagini valide per la combinazione. Logo1 caricato: {bool(img1)}, Logo2 caricato: {bool(img2)}.")
                            raise ValueError("Uno o entrambi i loghi non sono stati caricati correttamente.") # Questo forzerÃ  l'except sottostante
                        
                        # Ridimensiona le immagini a dimensioni uniformi
                        size = (150, 150)
                        img1 = img1.resize(size)
                        img2 = img2.resize(size)
                        img_vs = img_vs.resize((100, 100))
                        
                        # Assicurati che tutte le immagini siano in modalitÃÂ  RGBA per supportare la trasparenza
                        if img1.mode != 'RGBA':
                            img1 = img1.convert('RGBA')
                        if img2.mode != 'RGBA':
                            img2 = img2.convert('RGBA')
                        
                        # Crea una nuova immagine con spazio per entrambi i loghi e il VS
                        combined_width = 300
                        combined = Image.new('RGBA', (combined_width, 150), (255, 255, 255, 0))
                        
                        # Posiziona le immagini con il VS sovrapposto al centro
                        # Posiziona il primo logo a sinistra
                        combined.paste(img1, (0, 0), img1)
                        # Posiziona il secondo logo a destra
                        combined.paste(img2, (combined_width - 150, 0), img2)
                        
                        # Posiziona il VS al centro, sovrapposto ai due loghi
                        vs_x = (combined_width - 100) // 2
                        
                        # Crea una copia dell'immagine combinata prima di sovrapporre il VS
                        # Questo passaggio ÃÂ¨ importante per preservare i dettagli dei loghi sottostanti
                        combined_with_vs = combined.copy()
                        combined_with_vs.paste(img_vs, (vs_x, 25), img_vs)
                        
                        # Usa l'immagine con VS sovrapposto
                        combined = combined_with_vs
                        
                        # Salva l'immagine combinata
                        combined.save(absolute_output_filename)
                        
                        print(f"[✓] Immagine combinata creata: {absolute_output_filename}")
                        
                        # Carica le variabili d'ambiente per GitHub
                        NOMEREPO = os.getenv("NOMEREPO", "").strip()
                        NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
                        
                        # Se le variabili GitHub sono disponibili, restituisci l'URL raw di GitHub
                        if NOMEGITHUB and NOMEREPO:
                            github_raw_url = f"https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/main/{relative_logo_path}"
                            print(f"[✓] URL GitHub generato: {github_raw_url}")
                            return github_raw_url
                        else:
                            # Altrimenti restituisci il percorso assoluto
                            return absolute_output_filename
                        
                    except Exception as e:
                        print(f"[!] Errore nella creazione dell'immagine combinata: {e}")
                        # Se fallisce, restituisci solo il primo logo trovato
                        return logo1_url or logo2_url
                
                # Se non abbiamo trovato entrambi i loghi, restituisci quello che abbiamo
                return logo1_url or logo2_url
            if ':' in event_name:
                # Usa la parte prima dei ":" per la ricerca
                prefix_name = event_name.split(':', 1)[0].strip()
                print(f"[🔍] Tentativo ricerca logo con prefisso: {prefix_name}")
                
                # Prepara la query di ricerca con il prefisso
                search_query = urllib.parse.quote(f"{prefix_name} logo")
                
                # Utilizziamo l'API di Bing Image Search con parametri migliorati
                search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent+filterui:aspect-square&form=IRFLTR"
                
                headers = { 
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Cache-Control": "max-age=0",
                    "Connection": "keep-alive"
                } 
                
                response = requests.get(search_url, headers=headers, timeout=10)
                
                if response.status_code == 200: 
                    # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
                    patterns = [
                        r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                        r'"murl":"(https?://[^"]+)"',
                        r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                        r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                        r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, response.text)
                        if matches and len(matches) > 0:
                            # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                            for match in matches:
                                if '.png' in match.lower() or '.svg' in match.lower():
                                    print(f"[✓] Logo trovato con prefisso: {match}")
                                    return match
                            # Se non troviamo PNG o SVG, prendi il primo risultato
                            print(f"[✓] Logo trovato con prefisso: {matches[0]}")
                            return matches[0]
            
            # Se non riusciamo a identificare le squadre e il prefisso non ha dato risultati, procedi con la ricerca normale
            print(f"[🔍] Ricerca standard per: {clean_event_name}")
            
            
            # Se non riusciamo a identificare le squadre, procedi con la ricerca normale
            # Prepara la query di ricerca piÃÂ¹ specifica
            search_query = urllib.parse.quote(f"{clean_event_name} logo")
            
            # Utilizziamo l'API di Bing Image Search con parametri migliorati
            search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent+filterui:aspect-square&form=IRFLTR"
            
            headers = { 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive"
            } 
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200: 
                # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
                patterns = [
                    r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                    r'"murl":"(https?://[^"]+)"',
                    r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                    r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                    r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, response.text)
                    if matches and len(matches) > 0:
                        # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                        for match in matches:
                            if '.png' in match.lower() or '.svg' in match.lower():
                                return match
                        # Se non troviamo PNG o SVG, prendi il primo risultato
                        return matches[0]
                
                # Metodo alternativo: cerca JSON incorporato nella pagina
                json_match = re.search(r'var\s+IG\s*=\s*(\{.+?\});\s*', response.text)
                if json_match:
                    try:
                        # Estrai e analizza il JSON
                        json_str = json_match.group(1)
                        # Pulisci il JSON se necessario
                        json_str = re.sub(r'([{,])\s*([a-zA-Z0-9_]+):', r'\1"\2":', json_str)
                        data = json.loads(json_str)
                        
                        # Cerca URL di immagini nel JSON
                        if 'images' in data and len(data['images']) > 0:
                            for img in data['images']:
                                if 'murl' in img:
                                    return img['murl']
                    except Exception as e:
                        print(f"[!] Errore nell'analisi JSON: {e}")
                
                print(f"[!] Nessun logo trovato per '{clean_event_name}' con i pattern standard")
                
                # Ultimo tentativo: cerca qualsiasi URL di immagine nella pagina
                any_img = re.search(r'(https?://[^"\']+\.(?:png|jpg|jpeg|svg|webp))', response.text)
                if any_img:
                    return any_img.group(1)
                    
        except Exception as e: 
            print(f"[!] Errore nella ricerca del logo per '{event_name}': {e}") 
        
        # Se non troviamo nulla, restituiamo None 
        return None

    def search_team_logo(team_name):
        """
        Funzione dedicata alla ricerca del logo di una singola squadra
        """
        try:
            # Prepara la query di ricerca specifica per la squadra
            search_query = urllib.parse.quote(f"{team_name} logo")
            
            # Utilizziamo l'API di Bing Image Search con parametri migliorati
            search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent+filterui:aspect-square&form=IRFLTR"
            
            headers = { 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive"
            } 
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200: 
                # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
                patterns = [
                    r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                    r'"murl":"(https?://[^"]+)"',
                    r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                    r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                    r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, response.text)
                    if matches and len(matches) > 0:
                        # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                        for match in matches:
                            if '.png' in match.lower() or '.svg' in match.lower():
                                return match
                        # Se non troviamo PNG o SVG, prendi il primo risultato
                        return matches[0]
                
                # Metodo alternativo: cerca JSON incorporato nella pagina
                json_match = re.search(r'var\s+IG\s*=\s*(\{.+?\});\s*', response.text)
                if json_match:
                    try:
                        # Estrai e analizza il JSON
                        json_str = json_match.group(1)
                        # Pulisci il JSON se necessario
                        json_str = re.sub(r'([{,])\s*([a-zA-Z0-9_]+):', r'\1"\2":', json_str)
                        data = json.loads(json_str)
                        
                        # Cerca URL di immagini nel JSON
                        if 'images' in data and len(data['images']) > 0:
                            for img in data['images']:
                                if 'murl' in img:
                                    return img['murl']
                    except Exception as e:
                        print(f"[!] Errore nell'analisi JSON: {e}")
                
                print(f"[!] Nessun logo trovato per '{team_name}' con i pattern standard")
                
                # Ultimo tentativo: cerca qualsiasi URL di immagine nella pagina
                any_img = re.search(r'(https?://[^"\']+\.(?:png|jpg|jpeg|svg|webp))', response.text)
                if any_img:
                    return any_img.group(1)
                    
        except Exception as e: 
            print(f"[!] Errore nella ricerca del logo per '{team_name}': {e}") 
        
        # Se non troviamo nulla, restituiamo None 
        return None
     
    def get_stream_from_channel_id(channel_id): 
        # Restituisce direttamente l'URL .php
        embed_url = f"{LINK_DADDY}/watch.php?id={channel_id}" 
        print(f"URL .php per il canale Daddylive {channel_id}.")
        return embed_url
     
    def clean_category_name(name): 
        # Rimuove tag html come </span> o simili 
        return re.sub(r'<[^>]+>', '', name).strip() 
     
    def extract_channels_from_json(path): 
        keywords = {"italy", "rai", "italia", "it"} 
        now = datetime.now()  # ora attuale completa (data+ora) 
        yesterday_date = (now - timedelta(days=1)).date() # Data di ieri
     
        with open(path, "r", encoding="utf-8") as f: 
            data = json.load(f) 
     
        categorized_channels = {} 
     
        for date_key, sections in data.items(): 
            date_part = date_key.split(" - ")[0] 
            try: 
                date_obj = parser.parse(date_part, fuzzy=True).date() 
            except Exception as e: 
                print(f"[!] Errore parsing data '{date_part}': {e}") 
                continue 
     
            # filtro solo per eventi_dlhd del giorno corrente 
            if date_obj != now.date(): 
                continue 
     
            date_str = date_obj.strftime("%Y-%m-%d") 
     
            for category_raw, event_items in sections.items(): 
                category = clean_category_name(category_raw)
                # Salta la categoria TV Shows
                if category.lower() == "tv shows":
                    continue
                if category not in categorized_channels: 
                    categorized_channels[category] = [] 
     
                for item in event_items: 
                    time_str = item.get("time", "00:00") 
                    try: 
                        # Parse orario evento 
                        time_obj = datetime.strptime(time_str, "%H:%M") + timedelta(hours=2)  # correzione timezone? 
     
                        # crea datetime completo con data evento e orario evento 
                        event_datetime = datetime.combine(date_obj, time_obj.time()) 
     
                        # Controllo: includi solo se l'evento Ã¨ iniziato da meno di 2 ore 
                        if now - event_datetime > timedelta(hours=2): 
                            # Evento iniziato da piÃ¹ di 2 ore -> salto 
                            continue 
     
                        time_formatted = time_obj.strftime("%H:%M") 
                    except Exception: 
                        time_formatted = time_str 
     
                    event_title = item.get("event", "Evento") 
     
                    for ch in item.get("channels", []): 
                        channel_name = ch.get("channel_name", "") 
                        channel_id = ch.get("channel_id", "") 
     
                        words = set(re.findall(r'\b\w+\b', channel_name.lower())) 
                        if keywords.intersection(words): 
                            tvg_name = f"{event_title} ({time_formatted})" 
                            categorized_channels[category].append({ 
                                "tvg_name": tvg_name, 
                                "channel_name": channel_name, 
                                "channel_id": channel_id,
                                "event_title": event_title  # Aggiungiamo il titolo dell'evento per la ricerca del logo
                            }) 
     
        return categorized_channels 
     
    def generate_m3u_from_schedule(json_file, output_file): 
        categorized_channels = extract_channels_from_json(json_file) 

        with open(output_file, "w", encoding="utf-8") as f: 
            f.write("#EXTM3U\n") 

            # Controlla se ci sono eventi_dlhd prima di aggiungere il canale DADDYLIVE
            has_events = any(channels for channels in categorized_channels.values())
            
            if has_events:
                # Aggiungi il canale iniziale/informativo solo se ci sono eventi_dlhd
                f.write(f'#EXTINF:-1 tvg-name="DADDYLIVE" group-title="Eventi Live DLHD",DADDYLIVE\n')
                f.write("https://example.com.m3u8\n\n")
            else:
                print("[ℹ️] Nessun evento trovato, canale DADDYLIVE non aggiunto.")

            for category, channels in categorized_channels.items(): 
                if not channels: 
                    continue 
          
                for ch in channels: 
                    tvg_name = ch["tvg_name"] 
                    channel_id = ch["channel_id"] 
                    event_title = ch["event_title"]  # Otteniamo il titolo dell'evento
                    channel_name = ch["channel_name"]
                    
                    # Cerca un logo per questo evento
                    # Rimuovi l'orario dal titolo dell'evento prima di cercare il logo
                    clean_event_title = re.sub(r'\s*\(\d{1,2}:\d{2}\)\s*$', '', event_title)
                    print(f"[🔍] Ricerca logo per: {clean_event_title}") 
                    logo_url = search_logo_for_event(clean_event_title)
                    logo_attribute = f' tvg-logo="{logo_url}"' if logo_url else ''
     
                    try: 
                        # Cerca lo stream .m3u8 nei siti specificati
                        stream = get_stream_from_channel_id(channel_id)

                        if stream: 
                            cleaned_event_id = clean_tvg_id(event_title) # Usa event_title per tvg-id
                            f.write(f'#EXTINF:-1 tvg-id="{cleaned_event_id}" tvg-name="{category} | {tvg_name}"{logo_attribute} group-title="Eventi Live DLHD",{category} | {tvg_name}\n')
                            # Aggiungi EXTHTTP headers per canali daddy (esclusi .php)
                            if "ava.karmakurama.com" in stream and not stream.endswith('.php'):
                                daddy_headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1", "Referrer": "https://ava.karmakurama.com/", "Origin": "https://ava.karmakurama.com"}
                                vlc_opt_lines = headers_to_extvlcopt(daddy_headers)
                                for line in vlc_opt_lines:
                                    f.write(f'{line}\n')
                            f.write(f'{stream}\n\n')
                            print(f"[✓] {tvg_name}" + (f" (logo trovato)" if logo_url else " (nessun logo trovato)")) 
                        else: 
                            print(f"[✗] {tvg_name} - Nessuno stream trovato") 
                    except Exception as e: 
                        print(f"[!] Errore su {tvg_name}: {e}") 
     
    if __name__ == "__main__": 
        generate_m3u_from_schedule(JSON_FILE, OUTPUT_FILE)

# Funzione per il quarto script (schedule_extractor.py)
def schedule_extractor():
    # Codice del quarto script qui
    # Aggiungi il codice del tuo script "schedule_extractor.py" in questa funzione.
    print("Eseguendo lo schedule_extractor.py...")
    # Il codice che avevi nello script "schedule_extractor.py" va qui, senza modifiche.
    from playwright.sync_api import sync_playwright
    import os
    import json
    from datetime import datetime
    import re
    from bs4 import BeautifulSoup
    from dotenv import load_dotenv
    
    # Carica le variabili d'ambiente dal file .env
    load_dotenv()
    
    LINK_DADDY = os.getenv("LINK_DADDY", "").strip() or "https://dlhd.dad"
    
    def html_to_json(html_content):
        """Converte il contenuto HTML della programmazione in formato JSON."""
        soup = BeautifulSoup(html_content, 'html.parser')
        result = {}
    
        schedule_div = soup.find('div', id='schedule')
        if not schedule_div:
            print("AVVISO: Contenitore 'schedule' non trovato nel contenuto HTML!")
            return {}
    
        for day_div in schedule_div.find_all('div', class_='schedule__day'):
            day_title_tag = day_div.find('div', class_='schedule__dayTitle')
            if not day_title_tag:
                continue
            
            current_date = day_title_tag.text.strip()
            result[current_date] = {}
    
            for category_div in day_div.find_all('div', class_='schedule__category'):
                cat_header = category_div.find('div', class_='schedule__catHeader')
                if not cat_header:
                    continue
                
                current_category = cat_header.text.strip()
                result[current_date][current_category] = []
                
                category_body = category_div.find('div', class_='schedule__categoryBody')
                if not category_body:
                    continue

                for event_div in category_body.find_all('div', class_='schedule__event'):
                    event_header = event_div.find('div', class_='schedule__eventHeader')
                    if not event_header:
                        continue

                    time_span = event_header.find('span', class_='schedule__time')
                    event_title_span = event_header.find('span', class_='schedule__eventTitle')
                    
                    event_data = {
                        "time": time_span.text.strip() if time_span else "",
                        "event": event_title_span.text.strip() if event_title_span else "Evento Sconosciuto",
                        "channels": []
                    }

                    channels_div = event_div.find('div', class_='schedule__channels')
                    if channels_div:
                        for link in channels_div.find_all('a', href=re.compile(r'/watch\.php\?id=\d+')):
                            href = link.get('href', '')
                            channel_id_match = re.search(r'id=(\d+)', href)
                            if channel_id_match:
                                channel_id = channel_id_match.group(1)
                                channel_name = link.text.strip()
                                channel_name = re.sub(r'\s*CH-\d+$', '', channel_name).strip()

                                event_data["channels"].append({
                                    "channel_name": channel_name,
                                    "channel_id": channel_id
                                })
                    
                    result[current_date][current_category].append(event_data)
    
        return result
    
    def html_to_json_extra_schedule(html_content, result):
        """Aggiunge gli eventi_dlhd dalla sezione 'Extra Schedule' al risultato JSON."""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        extra_schedule_header = soup.find('h2', string=re.compile(r'Extra Schedule'))
        if not extra_schedule_header:
            print("AVVISO: Sezione 'Extra Schedule' non trovata.")
            return result

        schedule_div = extra_schedule_header.find_next_sibling('div', class_='schedule')
        if not schedule_div:
            print("AVVISO: Contenitore per 'Extra Schedule' non trovato.")
            return result

        for day_div in schedule_div.find_all('div', class_='schedule__day'):
            day_title_tag = day_div.find('div', class_='schedule__dayTitle')
            if not day_title_tag:
                continue
            
            current_date = day_title_tag.text.strip()
            if current_date not in result:
                result[current_date] = {}

            for event_div in day_div.find_all('div', class_='schedule__event'):
                event_header = event_div.find('div', class_='schedule__eventHeader')
                if not event_header:
                    continue

                time_span = event_header.find('span', class_='schedule__time')
                event_title_span = event_header.find('span', class_='schedule__eventTitle')
                
                if not time_span or not event_title_span:
                    continue

                event_title_text = event_title_span.text.strip()
                
                # Estrai la categoria dal titolo dell'evento, se presente
                category = "eventi_dlhd Extra" # Categoria di default
                if ":" in event_title_text:
                    parts = event_title_text.split(':', 1)
                    potential_category = parts[0].strip()
                    # Heuristica per decidere se è una categoria
                    if len(potential_category.split()) < 4 and not any(char.isdigit() for char in potential_category):
                         category = potential_category

                if category not in result[current_date]:
                    result[current_date][category] = []

                event_data = {
                    "time": time_span.text.strip(),
                    "event": event_title_text,
                    "channels": []
                }

                channels_div = event_div.find('div', class_='schedule__channels')
                if channels_div:
                    for link in channels_div.find_all('a', href=re.compile(r'/watchs2watch\.php\?id=')):
                        href = link.get('href', '')
                        # L'ID del canale è codificato in modo diverso qui, lo gestiamo come testo
                        channel_id = href.split('id=')[-1]
                        channel_name = link.text.strip()
                        channel_name = re.sub(r'\s*CH-\d+$', '', channel_name).strip()

                        event_data["channels"].append({
                            "channel_name": channel_name,
                            "channel_id": channel_id # Manteniamo l'ID complesso
                        })
                
                if event_data["channels"]:
                    result[current_date][category].append(event_data)

        return result

    def html_to_json_extra_backup_schedule(html_content, result):
        """Aggiunge gli eventi_dlhd dalla sezione 'Extra Schedule Backup' al risultato JSON."""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        extra_schedule_header = soup.find('h2', string=re.compile(r'Extra Schedule Backup'))
        if not extra_schedule_header:
            print("AVVISO: Sezione 'Extra Schedule Backup' non trovata.")
            return result

        schedule_div = extra_schedule_header.find_next_sibling('div', class_='schedule')
        if not schedule_div:
            print("AVVISO: Contenitore per 'Extra Schedule Backup' non trovato.")
            return result

        for day_div in schedule_div.find_all('div', class_='schedule__day'):
            day_title_tag = day_div.find('div', class_='schedule__dayTitle')
            if not day_title_tag:
                continue
            
            current_date = day_title_tag.text.strip()
            if current_date not in result:
                result[current_date] = {}

            for category_div in day_div.find_all('div', class_='schedule__category'):
                cat_header = category_div.find('div', class_='schedule__catHeader')
                if not cat_header:
                    continue
                
                current_category = cat_header.text.strip()
                if current_category not in result[current_date]:
                    result[current_date][current_category] = []

                category_body = category_div.find('div', class_='schedule__categoryBody')
                if not category_body:
                    continue

                for event_div in category_body.find_all('div', class_='schedule__event'):
                    event_header = event_div.find('div', class_='schedule__eventHeader')
                    if not event_header:
                        continue

                    time_span = event_header.find('span', class_='schedule__time')
                    event_title_span = event_header.find('span', class_='schedule__eventTitle')
                    
                    event_data = {
                        "time": time_span.text.strip() if time_span else "",
                        "event": event_title_span.text.strip() if event_title_span else "Evento Sconosciuto",
                        "channels": []
                    }

                    channels_div = event_div.find('div', class_='schedule__channels')
                    if channels_div:
                        for link in channels_div.find_all('a', href=re.compile(r'/watchextra\.php\?id=')):
                            href = link.get('href', '')
                            channel_id_match = re.search(r'id=(\d+)', href)
                            if channel_id_match:
                                channel_id = channel_id_match.group(1)
                                channel_name = link.text.strip()
                                channel_name = re.sub(r'\s*CH-\d+$', '', channel_name).strip()

                                event_data["channels"].append({
                                    "channel_name": channel_name,
                                    "channel_id": channel_id
                                })
                    
                    if event_data["channels"]:
                        result[current_date][current_category].append(event_data)

        return result

    def html_to_json_extra_sd_schedule(html_content, result):
        """Aggiunge gli eventi_dlhd dalla sezione 'Extra SD Stream Schedule' al risultato JSON."""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        extra_schedule_header = soup.find('h2', string=re.compile(r'Extra SD Stream Schedule'))
        if not extra_schedule_header:
            print("AVVISO: Sezione 'Extra SD Stream Schedule' non trovata.")
            return result

        schedule_div = extra_schedule_header.find_next_sibling('div', class_='schedule')
        if not schedule_div:
            print("AVVISO: Contenitore per 'Extra SD Stream Schedule' non trovato.")
            return result

        for day_div in schedule_div.find_all('div', class_='schedule__day'):
            day_title_tag = day_div.find('div', class_='schedule__dayTitle')
            if not day_title_tag:
                continue
            
            current_date = day_title_tag.text.strip()
            if current_date not in result:
                result[current_date] = {}

            for category_div in day_div.find_all('div', class_='schedule__category'):
                cat_header = category_div.find('div', class_='schedule__catHeader')
                if not cat_header:
                    continue
                
                current_category = cat_header.text.strip()
                if current_category not in result[current_date]:
                    result[current_date][current_category] = []

                category_body = category_div.find('div', class_='schedule__categoryBody')
                if not category_body:
                    continue

                for event_div in category_body.find_all('div', class_='schedule__event'):
                    event_header = event_div.find('div', class_='schedule__eventHeader')
                    if not event_header:
                        continue

                    time_span = event_header.find('span', class_='schedule__time')
                    event_title_span = event_header.find('span', class_='schedule__eventTitle')
                    
                    event_data = {
                        "time": time_span.text.strip() if time_span else "",
                        "event": event_title_span.text.strip() if event_title_span else "Evento Sconosciuto",
                        "channels": []
                    }

                    channels_div = event_div.find('div', class_='schedule__channels')
                    if channels_div:
                        for link in channels_div.find_all('a', href=re.compile(r'/watchsd\.php\?id=')):
                            href = link.get('href', '')
                            # L'ID del canale è una stringa, non un numero
                            channel_id = href.split('id=')[-1]
                            channel_name = link.text.strip()
                            channel_name = re.sub(r'\s*CH-[\w-]+$', '', channel_name).strip()

                            event_data["channels"].append({
                                "channel_name": channel_name,
                                "channel_id": channel_id
                            })
                    
                    if event_data["channels"]:
                        result[current_date][current_category].append(event_data)

        return result
    
    def modify_json_file(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        current_month = datetime.now().strftime("%B")
    
        # Questa logica non è più necessaria con la nuova struttura HTML
        # che fornisce già la data completa.
        # for date in list(data.keys()):
        #     match = re.match(r"(\w+\s\d+)(st|nd|rd|th)\s(\d{4})", date)
        #     if match:
        #         day_part = match.group(1)
        #         suffix = match.group(2)
        #         year_part = match.group(3)
        #         new_date = f"{day_part}{suffix} {current_month} {year_part}"
        #         data[new_date] = data.pop(date)
    
        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        
        print(f"File JSON modificato e salvato in {json_file_path}")
    
    def extract_schedule_container():
        url = f"{LINK_DADDY}/"
    
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_output = os.path.join(script_dir, "daddyliveSchedule.json")
    
        print(f"Accesso alla pagina {url} per estrarre il main-schedule-container...")
    
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
    
            max_attempts = 3
            for attempt in range(1, max_attempts + 1):
                try:
                    print(f"Tentativo {attempt} di {max_attempts}...")
                    page.goto(url)
                    print("Attesa per il caricamento completo...")
                    page.wait_for_timeout(10000)  # 10 secondi
    
                    schedule_content = page.evaluate("""() => {
                        const container = document.querySelector('body');
                        return container ? container.outerHTML : '';
                    }""")
    
                    if not schedule_content:
                        print("AVVISO: Contenuto della pagina non trovato o vuoto!")
                        if attempt == max_attempts:
                            browser.close()
                            return False
                        else:
                            continue
    
                    print("Conversione HTML della programmazione principale in formato JSON...")
                    json_data = html_to_json(schedule_content)

                    print("Aggiunta della programmazione da 'Extra Schedule'...")
                    json_data = html_to_json_extra_schedule(schedule_content, json_data)

                    print("Aggiunta della programmazione da 'Extra Schedule Backup'...")
                    json_data = html_to_json_extra_backup_schedule(schedule_content, json_data)

                    print("Aggiunta della programmazione da 'Extra SD Stream Schedule'...")
                    json_data = html_to_json_extra_sd_schedule(schedule_content, json_data)
    
                    with open(json_output, "w", encoding="utf-8") as f:
                        json.dump(json_data, f, indent=4)
    
                    print(f"Dati JSON salvati in {json_output}")
    
                    modify_json_file(json_output)
                    browser.close()
                    return True
    
                except Exception as e:
                    print(f"ERRORE nel tentativo {attempt}: {str(e)}")
                    if attempt == max_attempts:
                        print("Tutti i tentativi falliti!")
                        browser.close()
                        return False
                    else:
                        print(f"Riprovando... (tentativo {attempt + 1} di {max_attempts})")
    
            browser.close()
            return False
    
    if __name__ == "__main__":
        success = extract_schedule_container()
        if not success:
            exit(1)

def epg_eventi_dlhd_generator_world(json_file_path, output_file_path="eventi_dlhd.xml"):
    # Codice del quinto script qui
    # Aggiungi il codice del tuo script "epg_eventi_dlhd_generator.py" in questa funzione.
    print("Eseguendo l'epg_eventi_dlhd_generator_world.py...")
    # Il codice che avevi nello script "epg_eventi_dlhd_generator.py" va qui, senza modifiche.
    import os
    import re
    import json
    from datetime import datetime, timedelta, timezone
    
    # Funzione di utilitÃÂ  per pulire il testo (rimuovere tag HTML span)
    def clean_text(text):
        return re.sub(r'</?span.*?>', '', str(text))
    
    # Funzione di utilitÃÂ  per pulire il Channel ID (rimuovere spazi e caratteri speciali)
    def clean_channel_id(text):
        """Rimuove caratteri speciali e spazi dal channel ID lasciando tutto attaccato"""
        # Rimuovi prima i tag HTML
        text = clean_text(text)
        # Rimuovi tutti gli spazi
        text = re.sub(r'\s+', '', text)
        # Mantieni solo caratteri alfanumerici (rimuovi tutto il resto)
        text = re.sub(r'[^a-zA-Z0-9]', '', text)
        # Assicurati che non sia vuoto
        if not text:
            text = "unknownchannel"
        return text
    
    # --- SCRIPT 5: epg_eventi_dlhd_xml_generator (genera eventi_dlhd.xml) ---
    def load_json_for_epg(json_file_path):
        """Carica e filtra i dati JSON per la generazione EPG"""
        if not os.path.exists(json_file_path):
            print(f"[!] File JSON non trovato per EPG: {json_file_path}")
            return {}
        
        try:
            with open(json_file_path, "r", encoding="utf-8") as file:
                json_data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"[!] Errore nel parsing del file JSON: {e}")
            return {}
        except Exception as e:
            print(f"[!] Errore nell'apertura del file JSON: {e}")
            return {}
            
        # Lista delle parole chiave per canali italiani
        keywords = ['italy', 'rai', 'italia', 'it', 'uk', 'tnt', 'usa', 'tennis channel', 'tennis stream', 'la']
        
        filtered_data = {}
        for date, categories in json_data.items():
            filtered_categories = {}
            for category, events in categories.items():
                filtered_events = []
                for event_info in events: # Original loop for events
                    # Filtra gli eventi_dlhd in base all'orario specificato (00:00 - 04:00)
                    event_time_str = event_info.get("time", "00:00") # Prende l'orario dell'evento, default a "00:00" se mancante
                    try:
                        event_actual_time = datetime.strptime(event_time_str, "%H:%M").time()
                        
                        # Definisci gli orari limite per il filtro
                        filter_start_time = datetime.strptime("00:00", "%H:%M").time()
                        filter_end_time = datetime.strptime("04:00", "%H:%M").time()

                        # Escludi eventi_dlhd se l'orario ÃÂ¨ compreso tra 00:00 e 04:00 inclusi
                        if filter_start_time <= event_actual_time <= filter_end_time:
                            continue # Salta questo evento e passa al successivo
                    except ValueError:
                        print(f"[!] Orario evento non valido '{event_time_str}' per l'evento '{event_info.get('event', 'Sconosciuto')}' durante il caricamento JSON. Evento saltato.")
                        continue

                    filtered_channels = []
                    # Utilizza .get("channels", []) per gestire casi in cui "channels" potrebbe mancare
                    for channel in event_info.get("channels", []): 
                        channel_name = clean_text(channel.get("channel_name", "")) # Usa .get per sicurezza
                        
                        # Filtra per canali italiani - solo parole intere
                        channel_words = channel_name.lower().split()
                        if any(word in keywords for word in channel_words):
                            filtered_channels.append(channel)
                    
                    if filtered_channels:
                        # Assicura che event_info sia un dizionario prima dello unpacking
                        if isinstance(event_info, dict):
                            filtered_events.append({**event_info, "channels": filtered_channels})
                        else:
                            # Logga un avviso se il formato dell'evento non ÃÂ¨ quello atteso
                            print(f"[!] Formato evento non valido durante il filtraggio per EPG: {event_info}")
                
                if filtered_events:
                    filtered_categories[category] = filtered_events
            
            if filtered_categories:
                filtered_data[date] = filtered_categories
        
        return filtered_data
    
    def generate_epg_xml(json_data):
        """Genera il contenuto XML EPG dai dati JSON filtrati"""
        epg_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n'
        
        italian_offset = timedelta(hours=2)
        italian_offset_str = "+0200" 
    
        current_datetime_utc = datetime.now(timezone.utc)
        current_datetime_local = current_datetime_utc + italian_offset
    
        # Tiene traccia degli ID dei canali per cui ÃÂ¨ giÃÂ  stato scritto il tag <channel>
        channel_ids_processed_for_channel_tag = set() 
    
        for date_key, categories in json_data.items():
            # Dizionario per memorizzare l'ora di fine dell'ultimo evento per ciascun canale IN QUESTA DATA SPECIFICA
            # Viene resettato per ogni nuova data.
            last_event_end_time_per_channel_on_date = {}
    
            try:
                date_str_from_key = date_key.split(' - ')[0]
                date_str_cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str_from_key)
                event_date_part = datetime.strptime(date_str_cleaned, "%A %d %b %Y").date()
            except ValueError as e:
                print(f"[!] Errore nel parsing della data EPG: '{date_str_from_key}'. Errore: {e}")
                continue
            except IndexError as e:
                print(f"[!] Formato data non valido: '{date_key}'. Errore: {e}")
                continue
    
            if event_date_part < current_datetime_local.date():
                continue
    
            for category_name, events_list in categories.items():
                # Ordina gli eventi_dlhd per orario di inizio (UTC) per garantire la corretta logica "evento precedente"
                try:
                    sorted_events_list = sorted(
                        events_list,
                        key=lambda x: datetime.strptime(x.get("time", "00:00"), "%H:%M").time()
                    )
                except Exception as e_sort:
                    print(f"[!] Attenzione: Impossibile ordinare gli eventi_dlhd per la categoria '{category_name}' nella data '{date_key}'. Si procede senza ordinamento. Errore: {e_sort}")
                    sorted_events_list = events_list
    
                for event_info in sorted_events_list:
                    time_str_utc = event_info.get("time", "00:00")
                    event_name_original = clean_text(event_info.get("event", "Evento Sconosciuto"))
                    event_name = event_name_original.replace('&', 'and')
                    event_desc = event_info.get("description", f"Trasmesso in diretta.")
    
                    # USA EVENT NAME COME CHANNEL ID - PULITO DA CARATTERI SPECIALI E SPAZI
                    channel_id = clean_channel_id(event_name)
    
                    try: # Aggiunto .replace(tzinfo=timezone.utc) per rendere il datetime "aware"
                        event_time_utc_obj = datetime.strptime(time_str_utc, "%H:%M").time()
                        event_datetime_utc = datetime.combine(event_date_part, event_time_utc_obj).replace(tzinfo=timezone.utc)
                        event_datetime_local = event_datetime_utc + italian_offset
                    except ValueError as e:
                        print(f"[!] Errore parsing orario UTC '{time_str_utc}' per EPG evento '{event_name}'. Errore: {e}") 
                        continue
                    
                    if event_datetime_local < (current_datetime_local - timedelta(hours=2)):
                        continue
    
                    # Verifica che ci siano canali disponibili
                    channels_list = event_info.get("channels", [])
                    if not channels_list:
                        print(f"[!] Nessun canale disponibile per l'evento '{event_name}'")
                        continue
    
                    for channel_data in channels_list:
                        if not isinstance(channel_data, dict):
                            print(f"[!] Formato canale non valido per l'evento '{event_name}': {channel_data}")
                            continue
    
                        channel_name_cleaned = clean_text(channel_data.get("channel_name", "Canale Sconosciuto"))
    
                        # Crea tag <channel> se non giÃÂ  processato
                        if channel_id not in channel_ids_processed_for_channel_tag:
                            epg_content += f'  <channel id="{channel_id}">\n'
                            epg_content += f'    <display-name>{event_name}</display-name>\n'
                            epg_content += f'  </channel>\n'
                            channel_ids_processed_for_channel_tag.add(channel_id)
                        
                        # --- LOGICA ANNUNCIO MODIFICATA ---
                        announcement_stop_local = event_datetime_local # L'annuncio termina quando inizia l'evento corrente
    
                        # Determina l'inizio dell'annuncio
                        if channel_id in last_event_end_time_per_channel_on_date:
                            # C'ÃÂ¨ stato un evento precedente su questo canale in questa data
                            previous_event_end_time_local = last_event_end_time_per_channel_on_date[channel_id]
                            
                            # Assicurati che l'evento precedente termini prima che inizi quello corrente
                            if previous_event_end_time_local < event_datetime_local:
                                announcement_start_local = previous_event_end_time_local
                            else:
                                # Sovrapposizione o stesso orario di inizio, problematico.
                                # Fallback a 00:00 del giorno, o potresti saltare l'annuncio.
                                print(f"[!] Attenzione: L'evento '{event_name}' inizia prima o contemporaneamente alla fine dell'evento precedente. Fallback per l'inizio dell'annuncio.")
                                announcement_start_local = datetime.combine(event_datetime_local.date(), datetime.min.time(), tzinfo=event_datetime_local.tzinfo)
                        else:
                            # Primo evento per questo canale in questa data
                            announcement_start_local = datetime.combine(event_datetime_local.date(), datetime.min.time(), tzinfo=event_datetime_local.tzinfo) # 00:00 ora italiana
    
                        # Assicura che l'inizio dell'annuncio sia prima della fine
                        if announcement_start_local < announcement_stop_local:
                            announcement_title = f'Inizia alle {event_datetime_local.strftime("%H:%M")}.' # Orario italiano
                            
                            epg_content += f'  <programme start="{announcement_start_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" stop="{announcement_stop_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" channel="{channel_id}">\n'
                            epg_content += f'    <title lang="it">{announcement_title}</title>\n'
                            epg_content += f'    <desc lang="it">{event_name}.</desc>\n' 
                            epg_content += f'    <category lang="it">Annuncio</category>\n'
                            epg_content += f'  </programme>\n'
                        elif announcement_start_local == announcement_stop_local:
                            print(f"[INFO] Annuncio di durata zero saltato per l'evento '{event_name}' sul canale '{channel_id}'.")
                        else: # announcement_start_local > announcement_stop_local
                            print(f"[!] Attenzione: L'orario di inizio calcolato per l'annuncio è successivo all'orario di fine per l'evento '{event_name}' sul canale '{channel_id}'. Annuncio saltato.")
    
                        # --- EVENTO PRINCIPALE ---
                        main_event_start_local = event_datetime_local 
                        main_event_stop_local = event_datetime_local + timedelta(hours=2) # Durata fissa 2 ore
                        
                        epg_content += f'  <programme start="{main_event_start_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" stop="{main_event_stop_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" channel="{channel_id}">\n'
                        epg_content += f'    <title lang="it">{event_desc}</title>\n'
                        epg_content += f'    <desc lang="it">{event_name}</desc>\n'
                        epg_content += f'    <category lang="it">{clean_text(category_name)}</category>\n'
                        epg_content += f'  </programme>\n'
    
                        # Aggiorna l'orario di fine dell'ultimo evento per questo canale in questa data
                        last_event_end_time_per_channel_on_date[channel_id] = main_event_stop_local
        
        epg_content += "</tv>\n"
        return epg_content
    
    def save_epg_xml(epg_content, output_file_path):
        """Salva il contenuto EPG XML su file"""
        try:
            with open(output_file_path, "w", encoding="utf-8") as file:
                file.write(epg_content)
            print(f"[✓] File EPG XML salvato con successo: {output_file_path}")
            return True
        except Exception as e:
            print(f"[!] Errore nel salvataggio del file EPG XML: {e}")
            return False
    
    def main_epg_generator(json_file_path, output_file_path="eventi_dlhd.xml"):
        """Funzione principale per generare l'EPG XML"""
        print(f"[INFO] Inizio generazione EPG XML da: {json_file_path}")
        
        # Carica e filtra i dati JSON
        json_data = load_json_for_epg(json_file_path)
        
        if not json_data:
            print("[!] Nessun dato valido trovato nel file JSON.")
            return False
        
        print(f"[INFO] Dati caricati per {len(json_data)} date")
        
        # Genera il contenuto XML EPG
        epg_content = generate_epg_xml(json_data)
        
        # Salva il file XML
        success = save_epg_xml(epg_content, output_file_path)
        
        if success:
            print(f"[✓] Generazione EPG XML completata con successo!")
            return True
        else:
            print(f"[!] Errore durante la generazione EPG XML.")
            return False
    
    # Esegui la generazione EPG con i percorsi forniti
    main_epg_generator(json_file_path, output_file_path)

# Funzione per il quinto script (epg_eventi_dlhd_generator.py)
def epg_eventi_dlhd_generator(json_file_path, output_file_path="eventi_dlhd.xml"):
    # Codice del quinto script qui
    # Aggiungi il codice del tuo script "epg_eventi_dlhd_generator.py" in questa funzione.
    print("Eseguendo l'epg_eventi_dlhd_generator.py...")
    # Il codice che avevi nello script "epg_eventi_dlhd_generator.py" va qui, senza modifiche.
    import os
    import re
    import json
    from datetime import datetime, timedelta, timezone
    
    # Funzione di utilitÃÂ  per pulire il testo (rimuovere tag HTML span)
    def clean_text(text):
        return re.sub(r'</?span.*?>', '', str(text))
    
    # Funzione di utilitÃÂ  per pulire il Channel ID (rimuovere spazi e caratteri speciali)
    def clean_channel_id(text):
        """Rimuove caratteri speciali e spazi dal channel ID lasciando tutto attaccato"""
        # Rimuovi prima i tag HTML
        text = clean_text(text)
        # Rimuovi tutti gli spazi
        text = re.sub(r'\s+', '', text)
        # Mantieni solo caratteri alfanumerici (rimuovi tutto il resto)
        text = re.sub(r'[^a-zA-Z0-9]', '', text)
        # Assicurati che non sia vuoto
        if not text:
            text = "unknownchannel"
        return text
    
    # --- SCRIPT 5: epg_eventi_dlhd_xml_generator (genera eventi_dlhd.xml) ---
    def load_json_for_epg(json_file_path):
        """Carica e filtra i dati JSON per la generazione EPG"""
        if not os.path.exists(json_file_path):
            print(f"[!] File JSON non trovato per EPG: {json_file_path}")
            return {}
        
        try:
            with open(json_file_path, "r", encoding="utf-8") as file:
                json_data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"[!] Errore nel parsing del file JSON: {e}")
            return {}
        except Exception as e:
            print(f"[!] Errore nell'apertura del file JSON: {e}")
            return {}
            
        # Lista delle parole chiave per canali italiani
        keywords = ['italy', 'rai', 'italia', 'it']
        
        filtered_data = {}
        for date, categories in json_data.items():
            filtered_categories = {}
            for category, events in categories.items():
                filtered_events = []
                for event_info in events:
                    filtered_channels = []
                    # Utilizza .get("channels", []) per gestire casi in cui "channels" potrebbe mancare
                    for channel in event_info.get("channels", []): 
                        channel_name = clean_text(channel.get("channel_name", "")) # Usa .get per sicurezza
                        
                        # Filtra per canali italiani - solo parole intere
                        channel_words = channel_name.lower().split()
                        if any(word in keywords for word in channel_words):
                            filtered_channels.append(channel)
                    
                    if filtered_channels:
                        # Assicura che event_info sia un dizionario prima dello unpacking
                        if isinstance(event_info, dict):
                            filtered_events.append({**event_info, "channels": filtered_channels})
                        else:
                            # Logga un avviso se il formato dell'evento non ÃÂ¨ quello atteso
                            print(f"[!] Formato evento non valido durante il filtraggio per EPG: {event_info}")
                
                if filtered_events:
                    filtered_categories[category] = filtered_events
            
            if filtered_categories:
                filtered_data[date] = filtered_categories
        
        return filtered_data
    
    def generate_epg_xml(json_data):
        """Genera il contenuto XML EPG dai dati JSON filtrati"""
        epg_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n'
        
        italian_offset = timedelta(hours=2)
        italian_offset_str = "+0200" 
    
        current_datetime_utc = datetime.now(timezone.utc)
        current_datetime_local = current_datetime_utc + italian_offset
    
        # Tiene traccia degli ID dei canali per cui ÃÂ¨ giÃÂ  stato scritto il tag <channel>
        channel_ids_processed_for_channel_tag = set() 
    
        for date_key, categories in json_data.items():
            # Dizionario per memorizzare l'ora di fine dell'ultimo evento per ciascun canale IN QUESTA DATA SPECIFICA
            # Viene resettato per ogni nuova data.
            last_event_end_time_per_channel_on_date = {}
    
            try:
                date_str_from_key = date_key.split(' - ')[0]
                date_str_cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str_from_key)
                event_date_part = datetime.strptime(date_str_cleaned, "%A %d %b %Y").date()
            except ValueError as e:
                print(f"[!] Errore nel parsing della data EPG: '{date_str_from_key}'. Errore: {e}")
                continue
            except IndexError as e:
                print(f"[!] Formato data non valido: '{date_key}'. Errore: {e}")
                continue
    
            if event_date_part < current_datetime_local.date():
                continue
    
            for category_name, events_list in categories.items():
                # Ordina gli eventi_dlhd per orario di inizio (UTC) per garantire la corretta logica "evento precedente"
                try:
                    sorted_events_list = sorted(
                        events_list,
                        key=lambda x: datetime.strptime(x.get("time", "00:00"), "%H:%M").time()
                    )
                except Exception as e_sort:
                    print(f"[!] Attenzione: Impossibile ordinare gli eventi_dlhd per la categoria '{category_name}' nella data '{date_key}'. Si procede senza ordinamento. Errore: {e_sort}")
                    sorted_events_list = events_list
    
                for event_info in sorted_events_list:
                    time_str_utc = event_info.get("time", "00:00")
                    event_name = clean_text(event_info.get("event", "Evento Sconosciuto"))
                    event_desc = event_info.get("description", f"Trasmesso in diretta.")
    
                    # USA EVENT NAME COME CHANNEL ID - PULITO DA CARATTERI SPECIALI E SPAZI
                    channel_id = clean_channel_id(event_name)
    
                    try: # Aggiunto .replace(tzinfo=timezone.utc) per rendere il datetime "aware"
                        event_time_utc_obj = datetime.strptime(time_str_utc, "%H:%M").time()
                        event_datetime_utc = datetime.combine(event_date_part, event_time_utc_obj).replace(tzinfo=timezone.utc)
                        event_datetime_local = event_datetime_utc + italian_offset
                    except ValueError as e:
                        print(f"[!] Errore parsing orario UTC '{time_str_utc}' per EPG evento '{event_name}'. Errore: {e}") 
                        continue
                    
                    if event_datetime_local < (current_datetime_local - timedelta(hours=2)):
                        continue
    
                    # Verifica che ci siano canali disponibili
                    channels_list = event_info.get("channels", [])
                    if not channels_list:
                        print(f"[!] Nessun canale disponibile per l'evento '{event_name}'")
                        continue
    
                    for channel_data in channels_list:
                        if not isinstance(channel_data, dict):
                            print(f"[!] Formato canale non valido per l'evento '{event_name}': {channel_data}")
                            continue
    
                        channel_name_cleaned = clean_text(channel_data.get("channel_name", "Canale Sconosciuto"))
    
                        # Crea tag <channel> se non giÃÂ  processato
                        if channel_id not in channel_ids_processed_for_channel_tag:
                            epg_content += f'  <channel id="{channel_id}">\n'
                            epg_content += f'    <display-name>{event_name}</display-name>\n'
                            epg_content += f'  </channel>\n'
                            channel_ids_processed_for_channel_tag.add(channel_id)
                        
                        # --- LOGICA ANNUNCIO MODIFICATA ---
                        announcement_stop_local = event_datetime_local # L'annuncio termina quando inizia l'evento corrente
    
                        # Determina l'inizio dell'annuncio
                        if channel_id in last_event_end_time_per_channel_on_date:
                            # C'ÃÂ¨ stato un evento precedente su questo canale in questa data
                            previous_event_end_time_local = last_event_end_time_per_channel_on_date[channel_id]
                            
                            # Assicurati che l'evento precedente termini prima che inizi quello corrente
                            if previous_event_end_time_local < event_datetime_local:
                                announcement_start_local = previous_event_end_time_local
                            else:
                                # Sovrapposizione o stesso orario di inizio, problematico.
                                # Fallback a 00:00 del giorno, o potresti saltare l'annuncio.
                                print(f"[!] Attenzione: L'evento '{event_name}' inizia prima o contemporaneamente alla fine dell'evento precedente. Fallback per l'inizio dell'annuncio.")
                                announcement_start_local = datetime.combine(event_datetime_local.date(), datetime.min.time(), tzinfo=event_datetime_local.tzinfo)
                        else:
                            # Primo evento per questo canale in questa data
                            announcement_start_local = datetime.combine(event_datetime_local.date(), datetime.min.time(), tzinfo=event_datetime_local.tzinfo) # 00:00 ora italiana
    
                        # Assicura che l'inizio dell'annuncio sia prima della fine
                        if announcement_start_local < announcement_stop_local:
                            announcement_title = f'Inizia alle {event_datetime_local.strftime("%H:%M")}.' # Orario italiano
                            
                            epg_content += f'  <programme start="{announcement_start_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" stop="{announcement_stop_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" channel="{channel_id}">\n'
                            epg_content += f'    <title lang="it">{announcement_title}</title>\n'
                            epg_content += f'    <desc lang="it">{event_name}.</desc>\n' 
                            epg_content += f'    <category lang="it">Annuncio</category>\n'
                            epg_content += f'  </programme>\n'
                        elif announcement_start_local == announcement_stop_local:
                            print(f"[INFO] Annuncio di durata zero saltato per l'evento '{event_name}' sul canale '{channel_id}'.")
                        else: # announcement_start_local > announcement_stop_local
                            print(f"[!] Attenzione: L'orario di inizio calcolato per l'annuncio è successivo all'orario di fine per l'evento '{event_name}' sul canale '{channel_id}'. Annuncio saltato.")
    
                        # --- EVENTO PRINCIPALE ---
                        main_event_start_local = event_datetime_local 
                        main_event_stop_local = event_datetime_local + timedelta(hours=2) # Durata fissa 2 ore
                        
                        epg_content += f'  <programme start="{main_event_start_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" stop="{main_event_stop_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" channel="{channel_id}">\n'
                        epg_content += f'    <title lang="it">{event_desc}</title>\n'
                        epg_content += f'    <desc lang="it">{event_name}</desc>\n'
                        epg_content += f'    <category lang="it">{clean_text(category_name)}</category>\n'
                        epg_content += f'  </programme>\n'
    
                        # Aggiorna l'orario di fine dell'ultimo evento per questo canale in questa data
                        last_event_end_time_per_channel_on_date[channel_id] = main_event_stop_local
        
        epg_content += "</tv>\n"
        return epg_content
    
    def save_epg_xml(epg_content, output_file_path):
        """Salva il contenuto EPG XML su file"""
        try:
            with open(output_file_path, "w", encoding="utf-8") as file:
                file.write(epg_content)
            print(f"[✓] File EPG XML salvato con successo: {output_file_path}")
            return True
        except Exception as e:
            print(f"[!] Errore nel salvataggio del file EPG XML: {e}")
            return False
    
    def main_epg_generator(json_file_path, output_file_path="eventi_dlhd.xml"):
        """Funzione principale per generare l'EPG XML"""
        print(f"[INFO] Inizio generazione EPG XML da: {json_file_path}")
        
        # Carica e filtra i dati JSON
        json_data = load_json_for_epg(json_file_path)
        
        if not json_data:
            print("[!] Nessun dato valido trovato nel file JSON.")
            return False
        
        print(f"[INFO] Dati caricati per {len(json_data)} date")
        
        # Genera il contenuto XML EPG
        epg_content = generate_epg_xml(json_data)
        
        # Salva il file XML
        success = save_epg_xml(epg_content, output_file_path)
        
        if success:
            print(f"[✓] Generazione EPG XML completata con successo!")
            return True
        else:
            print(f"[!] Errore durante la generazione EPG XML.")
            return False
    
    # Esegui la generazione EPG con i percorsi forniti
    main_epg_generator(json_file_path, output_file_path)

# Funzione per il sesto script (italy_channels.py)
def italy_channels():
    print("Eseguendo il italy_channels.py...")
    import requests
    import time
    import re
    import xml.etree.ElementTree as ET
    import os
    from dotenv import load_dotenv
    from bs4 import BeautifulSoup

    # Variabile d'ambiente per controllare i canali Daddylive
    CANALI_DADDY = os.getenv("CANALI_DADDY", "no").strip().lower() == "si"
    LINK_DADDY = os.getenv("LINK_DADDY", "").strip() or "https://dlhd.dad"

    def getAuthSignature():
        headers = {
            "user-agent": "okhttp/4.11.0",
            "accept": "application/json",
            "content-type": "application/json; charset=utf-8",
            "content-length": "1106",
            "accept-encoding": "gzip"
        }
        data = {
            "token": "tosFwQCJMS8qrW_AjLoHPQ41646J5dRNha6ZWHnijoYQQQoADQoXYSo7ki7O5-CsgN4CH0uRk6EEoJ0728ar9scCRQW3ZkbfrPfeCXW2VgopSW2FWDqPOoVYIuVPAOnXCZ5g",
            "reason": "app-blur",
            "locale": "de",
            "theme": "dark",
            "metadata": {
                "device": {
                    "type": "Handset",
                    "os": "Android",
                    "osVersion": "10",
                    "model": "Pixel 4",
                    "brand": "Google"
                }
            }
        }
        resp = requests.post("https://vavoo.to/mediahubmx-signature.json", json=data, headers=headers, timeout=10)
        return resp.json().get("signature")

    def vavoo_groups():
        # Puoi aggiungere altri gruppi per più canali
        return ["Italy"]

    def clean_channel_name(name):
        """Rimuove i suffissi .a, .b, .c dal nome del canale"""
        # Rimuove .a, .b, .c alla fine del nome (con o senza spazi prima)
        cleaned_name = re.sub(r'\s*\.(a|b|c|s|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|t|u|v|w|x|y|z)\s*$', '', name, flags=re.IGNORECASE)
        return cleaned_name.strip()

    def normalize_channel_name(name):
        name = re.sub(r"\s+", "", name.strip().lower())
        name = re.sub(r"\.it\b", "", name)
        name = re.sub(r"hd|fullhd", "", name)
        return name

    def fetch_logos():
        return {
            "sky uno": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-uno-it.png",
            "rai 1": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-1-it.png",
            "rai 2": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-2-it.png",
            "rai 3": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-3-it.png",
            "eurosport 1": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/spain/eurosport-1-es.png",
            "eurosport 2": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/spain/eurosport-2-es.png",
            "italia 1": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/italia1-it.png",
            "la 7": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/la7-it.png",
            "la 7 d": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/la7d-it.png",
            "rai sport+": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-sport-it.png",
            "rai sport [live during events only]": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-sport-it.png",
            "rai premium": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-premium-it.png",
            "sky sport golf": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-golf-it.png",
            "sky sport moto gp": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-motogp-it.png",
            "sky sport tennis": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-tennis-it.png",
            "sky sport f1": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-f1-it.png",
            "sky sport football": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-football-it.png",
            "sky sport football [live during events only]": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-football-it.png",
            "sky sport uno": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-uno-it.png",
            "sky sport arena": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-arena-it.png",
            "sky cinema collection": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-collection-it.png",
            "sky cinema uno": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-uno-it.png",
            "sky cinema action": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-action-it.png",
            "sky cinema action (backup)": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-action-it.png",
            "sky cinema comedy": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-comedy-it.png",
            "sky cinema uno +24": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-uno-plus24-it.png",
            "sky cinema romance": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-romance-it.png",
            "sky cinema family": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-family-it.png",
            "sky cinema due +24": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-due-plus24-it.png",
            "sky cinema drama": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-drama-it.png",
            "sky cinema suspense": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-suspense-it.png",
            "sky sport 24": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-24-it.png",
            "sky sport 24 [live during events only]": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-24-it.png",
            "sky sport calcio": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-calcio-it.png",
            "sky sport 251": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Sky_Sport_-_Logo_2020.svg/2560px-Sky_Sport_-_Logo_2020.svg.png",
            "sky sport 252": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Sky_Sport_-_Logo_2020.svg/2560px-Sky_Sport_-_Logo_2020.svg.png",
            "sky sport 253": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Sky_Sport_-_Logo_2020.svg/2560px-Sky_Sport_-_Logo_2020.svg.png",
            "sky sport 254": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Sky_Sport_-_Logo_2020.svg/2560px-Sky_Sport_-_Logo_2020.svg.png",
            "sky sport 255": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Sky_Sport_-_Logo_2020.svg/2560px-Sky_Sport_-_Logo_2020.svg.png",
            "sky sport 256": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Sky_Sport_-_Logo_2020.svg/2560px-Sky_Sport_-_Logo_2020.svg.png",
            "sky calcio 1": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/germany/sky-select-1-alt-de.png",
            "sky calcio 2": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/germany/sky-select-2-alt-de.png",
            "sky calcio 3": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/germany/sky-select-3-alt-de.png",
            "sky calcio 4": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/germany/sky-select-4-alt-de.png",
            "sky calcio 5": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/germany/sky-select-5-alt-de.png",
            "sky calcio 6": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/germany/sky-select-6-alt-de.png",
            "sky calcio 7": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/germany/sky-select-7-alt-de.png",
            "sky serie": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-serie-it.png",
            "crime+investigation": "https://upload.wikimedia.org/wikipedia/commons/4/4d/Crime_%2B_Investigation_Logo_10.2019.svg",
            "20 mediaset": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/20-it.png",
            "mediaset 20": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/20-it.png",
            "27 twenty seven": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Twentyseven_logo.svg/260px-Twentyseven_logo.svg.png",
            "27 twentyseven": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Twentyseven_logo.svg/260px-Twentyseven_logo.svg.png",
            "canale 5": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/canale5-it.png",
            "cine 34 mediaset": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/cine34-it.png",
            "cine 34": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/cine34-it.png",
            "discovery focus": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/focus-it.png",
            "focus": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/focus-it.png",
            "italia 2": "https://upload.wikimedia.org/wikipedia/it/thumb/c/c5/Logo_Italia2.svg/520px-Logo_Italia2.svg.png",
            "mediaset italia 2": "https://upload.wikimedia.org/wikipedia/it/thumb/c/c5/Logo_Italia2.svg/520px-Logo_Italia2.svg.png",
            "mediaset italia": "https://www.italiasera.it/wp-content/uploads/2019/06/Mediaset-640x366.png",
            "mediaset extra": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/mediaset-extra-it.png",
            "mediaset 1": "https://play-lh.googleusercontent.com/2-Cl0plYUCxk8bnbeavm4ZOJ_S4Xuwmql_N3_E4OJyf7XK_YUvdNOWgzn8KD-Bur8w0",
            "mediaset infinity+ 1": "https://play-lh.googleusercontent.com/2-Cl0plYUCxk8bnbeavm4ZOJ_S4Xuwmql_N3_E4OJyf7XK_YUvdNOWgzn8KD-Bur8w0",
            "mediaset infinity+ 2": "https://play-lh.googleusercontent.com/2-Cl0plYUCxk8bnbeavm4ZOJ_S4Xuwmql_N3_E4OJyf7XK_YUvdNOWgzn8KD-Bur8w0",
            "mediaset infinity+ 5": "https://play-lh.googleusercontent.com/2-Cl0plYUCxk8bnbeavm4ZOJ_S4Xuwmql_N3_E4OJyf7XK_YUvdNOWgzn8KD-Bur8w0",
            "mediaset iris": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/iris-it.png",
            "iris": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/iris-it.png",
            "rete 4": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rete4-it.png",
            "sport italia (backup)": "https://play-lh.googleusercontent.com/0IcWROAOpuEcMf2qbOBNQYhrAPUuSmw-zv0f867kUxKSwSTD_chyCDuBP2PScIyWI9k",
            "sport italia": "https://play-lh.googleusercontent.com/0IcWROAOpuEcMf2qbOBNQYhrAPUuSmw-zv0f867kUxKSwSTD_chyCDuBP2PScIyWI9k",
            "sportitalia plus": "https://www.capitaladv.eu/wp-content/uploads/2020/07/LOGO-SPORTITALIA-PLUS-HD_2-1.png",
            "sport italia solo calcio [live during events only]": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/SI_Solo_Calcio_logo_%282019%29.svg/1200px-SI_Solo_Calcio_logo_%282019%29.svg.png",
            "sportitalia solocalcio": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/SI_Solo_Calcio_logo_%282019%29.svg/1200px-SI_Solo_Calcio_logo_%282019%29.svg.png",
            "dazn 1": "https://upload.wikimedia.org/wikipedia/commons/d/d6/Dazn-logo.png",
            "dazn2": "https://upload.wikimedia.org/wikipedia/commons/d/d6/Dazn-logo.png",
            "dazn": "https://upload.wikimedia.org/wikipedia/commons/d/d6/Dazn-logo.png",
            "dazn zona": "https://upload.wikimedia.org/wikipedia/commons/d/d6/Dazn-logo.png",
            "motortrend": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Motor_Trend_logo.svg/2560px-Motor_Trend_logo.svg.png",
            "sky sport max": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-max-it.png",
            "sky sport nba": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-nba-it.png",
            "sky sport serie a": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-serie-a-it.png",
            "sky sports f1": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-f1-it.png",
            "sky sports golf": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Sky_Sport_Golf_Logo_2022.svg/2560px-Sky_Sport_Golf_Logo_2022.svg.png",
            "sky super tennis": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-tennis-it.png",
            "tennis channel": "https://images.tennis.com/image/upload/t_16-9_768/v1620828532/tenniscom-prd/assets/Fallback/Tennis_Fallback_v6_f5tjzv.jpg",
            "super tennis": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/super-tennis-it.png",
            "tv 8": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/tv8-it.png",
            "sky primafila 1": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-primafila-it.png",
            "sky primafila 2": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-primafila-it.png",
            "sky primafila 3": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-primafila-it.png",
            "sky primafila 4": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-primafila-it.png",
            "sky primafila 5": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-primafila-it.png",
            "sky primafila 6": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-primafila-it.png",
            "sky primafila 7": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-primafila-it.png",
            "sky primafila 8": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-primafila-it.png",
            "sky primafila 9": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-primafila-it.png",
            "sky primafila 10": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-primafila-it.png",
            "sky primafila 11": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-primafila-it.png",
            "sky primafila 12": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-primafila-it.png",
            "sky primafila 13": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-primafila-it.png",
            "sky primafila 14": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-primafila-it.png",
            "sky primafila 15": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-primafila-it.png",
            "sky primafila 16": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-primafila-it.png",
            "sky primafila 17": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-primafila-it.png",
            "sky primafila 18": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-primafila-it.png",
            "sky cinema due": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-due-it.png",
            "sky atlantic": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-atlantic-it.png",
            "nat geo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/national-geographic-it.png",
            "discovery nove": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/nove-it.png",
            "discovery channel": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/discovery-channel-it.png",
            "real time": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/real-time-it.png",
            "rai 5": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-5-it.png",
            "rai gulp": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-gulp-it.png",
            "rai italia": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Rai_Italia_-_Logo_2017.svg/1024px-Rai_Italia_-_Logo_2017.svg.png",
            "rai movie": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-movie-it.png",
            "rai news 24": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-news-24-it.png",
            "rai scuola": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-scuola-it.png",
            "rai storia": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-storia-it.png",
            "rai yoyo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-yoyo-it.png",
            "rai 4": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-4-it.png",
            "rai 4k": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Rai_4K_-_Logo_2017.svg/1200px-Rai_4K_-_Logo_2017.svg.png",
            "hgtv": "https://d204lf4nuskf6u.cloudfront.net/italy-images/c2cbeaabb81be73e81c7f4291cf798e3.png?k=2nWZhtOSUQdq2s2ItEDH5%2BQEPdq1khUY8YJSK0%2BNV90dhkyaUQQ82V1zGPD7O5%2BS",
            "top crime": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/top-crime-it.png",
            "cielo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/cielo-it.png",
            "dmax": "https://cdn.cookielaw.org/logos/50417659-aa29-4f7f-b59d-f6e887deed53/a32be519-de41-40f4-abed-d2934ba6751b/9a44af24-5ca6-4098-aa95-594755bd7b2d/dmax_logo.png",
            "food network": "https://upload.wikimedia.org/wikipedia/commons/f/f4/Food_Network_-_Logo_2016.png",
            "giallo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/giallo-it.png",
            "history": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/history-channel-it.png",
            "la 5": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/la5-it.png",
            "sky arte": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-arte-it.png",
            "sky documentaries": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-documentaries-it.png",
            "sky nature": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-nature-it.png",
            "warner tv": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Warner_TV_Italy.svg/1200px-Warner_TV_Italy.svg.png",
            "fox": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/fox-it.png",
            "nat geo wild": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/national-geographic-wild-it.png",
            "animal planet": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/2018_Animal_Planet_logo.svg/2560px-2018_Animal_Planet_logo.svg.png",
            "boing": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/boing-it.png",
            "k2": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/k2-it.png",
            "discovery k2": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/k2-it.png",
            "nick jr": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/nick-jr-it.png",
            "nickelodeon": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/nickelodeon-it.png",
            "premium crime": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/premium-crime-it.png",
            "rakuten action movies": "https://img.utdstc.com/icon/7f6/a4a/7f6a4a47aa35e90d889cb8e71ed9a6930fe5832219371761736e87e880f85a5f:200",
            "rakuten comedy movies": "https://img.utdstc.com/icon/7f6/a4a/7f6a4a47aa35e90d889cb8e71ed9a6930fe5832219371761736e87e880f85a5f:200",
            "rakuten drama": "https://img.utdstc.com/icon/7f6/a4a/7f6a4a47aa35e90d889cb8e71ed9a6930fe5832219371761736e87e880f85a5f:200",
            "rakuten family": "https://img.utdstc.com/icon/7f6/a4a/7f6a4a47aa35e90d889cb8e71ed9a6930fe5832219371761736e87e880f85a5f:200",
            "rakuten top free": "https://img.utdstc.com/icon/7f6/a4a/7f6a4a47aa35e90d889cb8e71ed9a6930fe5832219371761736e87e880f85a5f:200",
            "rakuten tv shows": "https://img.utdstc.com/icon/7f6/a4a/7f6a4a47aa35e90d889cb8e71ed9a6930fe5832219371761736e87e880f85a5f:200",
            "boing plus": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Boing_Plus_logo_2020.svg/1200px-Boing_Plus_logo_2020.svg.png",
            "wwe channel": "https://upload.wikimedia.org/wikipedia/en/8/8c/WWE_Network_logo.jpeg",
            "rsi la 2": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/RSI_La_2_2012.svg/1200px-RSI_La_2_2012.svg.png",
            "rsi la 1": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/RSI_La_1_2012.svg/1200px-RSI_La_1_2012.svg.png",
            "cartoon network": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/cartoon-network-it.png",
            "sky tg 24": "https://play-lh.googleusercontent.com/0RJjBW8_r64dWLAbG7kUVrkESbBr9Ukx30pDI83e5_o1obv2MTC7KSpBAIhhXvJAkXE",
            "tg com 24": "https://yt3.hgoogleusercontent.com/ytc/AIdro_kVh4SupZFtHrALXp9dRWD9aahJOUfl8rhSF8VroefSLg=s900-c-k-c0x00ffffff-no-rj",
            "tgcom 24": "https://yt3.hgoogleusercontent.com/ytc/AIdro_kVh4SupZFtHrALXp9dRWD9aahJOUfl8rhSF8VroefSLg=s900-c-k-c0x00ffffff-no-rj",
            "cartoonito": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/cartoonito-it.png",
            "super!": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Super%21_logo_2021.svg/1024px-Super%21_logo_2021.svg.png",
            "deejay tv": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/deejay-tv-it.png",
            "cartoonito (backup)": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/cartoonito-it.png",
            "frisbee": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/frisbee-it.png",
            "catfish": "https://upload.wikimedia.org/wikipedia/commons/4/46/Catfish%2C_the_TV_Show_Logo.PNG", # "tv7 news" era attaccato qui, l'ho rimosso, sembrava un errore di battitura
            "disney+ film": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Disney%2B_logo.svg/2560px-Disney%2B_logo.svg.png",
            "comedy central": "https://yt3.googleusercontent.com/FPzu1EWCI54fIh2j9JEp0NOzwoeugjL4sZTQCdoxoQY1U4QHyKx2L3wPSw27IueuZGchIxtKfv8=s900-c-k-c0x00ffffff-no-rj",
            "arte network": "https://www.arte.tv/sites/corporate/wp-content/themes/arte-entreprise/img/arte_logo.png",
            "aurora arte": "https://www.auroraarte.it/wp-content/uploads/2023/11/AURORA-ARTE-brand.png",
            "telearte": "https://www.teleartetv.it/web/wp-content/uploads/2023/04/logo_TA.jpg",
            "sky sport motogp": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-motogp-hd-it.png",
            "sky sport": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/sky-sport-it.png",
            "rai sport": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/rai-sport-it.png",
            "rtv san marino sport": "https://static.wikia.nocookie.net/internationaltelevision/images/7/79/San_Marino_RTV_Sport_-_logo.png/revision/latest?cb=20221207153729",
            "rtv sport": "https://logowik.com/content/uploads/images/san-marino-rtv-sport-20211731580347.logowik.com.webp",
            "trsport": "https://teleromagna.it/Images/logo-tr-sport.jpg",
            "aci sport tv": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/aci-sport-tv-it.png",
            "euronews": "https://play-lh.googleusercontent.com/Mi8GAQIp3x94VcvbxZNsK-CTNhHy1zmo51pmME5KkkK4WgN4aQhM1FlNgLZUMD4VAXhL",
            "tg norba 24": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/tg-norba-24-it.png",
            "tv7 news": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStj45lIWvQ0KFzv6jyIP9vOZgPnWQirEl6dw&s",
            "milan tv": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/milan-tv-it.png",
            "rtl 102.5": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/rtl-1025-it.png",
            "la c tv": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/lac-tv-it.png?raw=true",
            "italian fishing tv": "https://www.upmagazinearezzo.it/atladv/wp-content/uploads/2017/07/atlantide-adv-logo-italian-fishing-tv.jpg",
            "rtv san marino": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/rtv-san-marino-it.png",
            "antenna sud": "https://www.antennasud.com/media/2022/08/cropped-LOGO_ANTENNA_SUD_ROSSO_FORATO.png",
            "senato tv": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/senato-tv-it.png?raw=true",
            "rete oro": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkE5wuUMIVAtANMfpSL4T5bIO73owXBhpvEg&s",
            "caccia": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/caccia-it.png?raw=true",
            "111 tv": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSDr-HrHBtGsogIKps_qWVME_l5axKwINoq2Q&s",
            "lazio tv": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/lazio-style-channel-it.png?raw=true",
            "padre pio tv": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/padre-pio-tv-it.png?raw=true",
            "inter tv": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/inter-tv-it.png?raw=true",
            "kiss kiss italia": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/radio-kiss-kiss-italia-it.png?raw=true",
            "12 tv parma": "https://www.12tvparma.it/wp-content/uploads/2021/11/ogg-image.jpg",
            "canale 21 extra": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcROcfjFIqjwxnG9AbEhJ6gwKb6IprmlFnF9aQ&s",
            "videolina": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/videolina-it.png?raw=true",
            "tv 2000": "https://upload.wikimedia.org/wikipedia/it/0/0d/Logo_di_TV2000.png",
            "byoblu": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRaMdUB8WEdsRVi_WZLxoi79pqlRef4s9Zehg&s",
            "kiss kiss napoli": "https://kisskissnapoli.it/wp-content/uploads/2022/03/cropped-logo-kisskiss-napoli.png",
            "kiss kiss": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/radio-kiss-kiss-tv-it.png?raw=true",
            "caccia e pesca": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/caccia-pesca-it.png?raw=true",
            "pesca": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/pesca-it.png?raw=true",
            "canale 7": "https://upload.wikimedia.org/wikipedia/commons/2/24/Canale_7.png",
            "crime+inv": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/crime-and-investigation-it.png?raw=true",
            "cafe 24": "https://play-lh.googleusercontent.com/DW0Tvz72-8XZ7rEBVh1jBzwYE1fZhTaowuuxN75Jl8yBtnFkySH1z2T2b7OPlotmHeQ",
            "antenna 2": "https://www.omceo.bg.it/images/loghi/antenna-2.png",
            "avengers grimm channel": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQN8by3YXjCGJQaxT6b-cgZ872BjY_NLIrALA&s",
            "classica": "https://upload.wikimedia.org/wikipedia/commons/4/4e/CLA_HD_Logo-CENT-300ppi_CMYK.jpg",
            "70 80 hits": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5WEMBuK9zFW2nr_clM7noNGaUwp5fxRrmJA&s",
            "cusano italia tv": "https://play-lh.googleusercontent.com/c2HegRLQmaQFJXROyFH-phglfaZzQ-vikbZ464ZVJGfW8kX9jQuLACb2TIlydv1apsg",
            "espansione tv": "https://massimoemanuelli.com/wp-content/uploads/2017/10/etv-logo-attuale.png?w=640",
            "tva vicenza": "https://massimoemanuelli.com/wp-content/uploads/2017/10/tva-vi-2.png",
            "m2o": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Radio_m2o_-_Logo_2019.svg/1200px-Radio_m2o_-_Logo_2019.svg.png",
            "televenezia": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ0xhoeVg7nRLPp8GnPkFzLUWvJ5WolvU-iYw&s",
            "a3": "https://yt3.googleusercontent.com/3zkPKViC7G2rHWbBpYzSL6dFM9OMFBqIC6JrT-mM73EQsERHMqx4sPzWpBD8nfEqgf_uSHi124Y=s900-c-k-c0x00ffffff-no-rj",
            "alto adige tv": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQSdt3E_MmezXRKr7QOUEr0leEcErbaNGqbog&s",
            "cremona 1": "https://www.arvedi.it/fileadmin/user_upload/istituzionale/gruppo-arvedi-e-informazione-logo-Cremona1.png",
            "gold tv": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSSjSJx2Wah0-hfWbBn4_C79K5I0600lcD8zw&s",
            "france 24": "https://github.com/tv-logo/tv-logos/blob/main/countries/france/france-24-fr.png?raw=true",
            "iunior tv": "https://upload.wikimedia.org/wikipedia/commons/9/94/Iunior_tv.png",
            "canale 2": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/canale-italia-2-it.png?raw=true",
            "pesca e caccia": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/caccia-pesca-it.png?raw=true",
            "qvc": "https://github.com/tv-logo/tv-logos/blob/main/countries/germany/qvc-de.png?raw=true",
            "tele chiara": "https://upload.wikimedia.org/wikipedia/commons/b/ba/Telechiara-logo.png",
            "bergamo tv": "https://www.opq.it/wp-content/uploads/BergamoTV.png",
            "italia 3": "https://static.wikia.nocookie.net/dreamlogos/images/4/4e/Italia_3_2013.png/revision/latest?cb=20200119124403",
            "primocanale": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/primocanale-it.png?raw=true",
            "rei tv": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/rei-tv-it.png?raw=true",
            "rete veneta": "https://upload.wikimedia.org/wikipedia/it/d/df/Logo_Rete_Veneta.png",
            "telearena": "https://upload.wikimedia.org/wikipedia/commons/6/60/TeleArena_logo.png",
            "reggio tv": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Reggio_TV_logo.png/640px-Reggio_TV_logo.png",
            "tv2000": "https://upload.wikimedia.org/wikipedia/it/0/0d/Logo_di_TV2000.png",
            "retebiella tv": "https://alpitv.com/wp-content/uploads/2022/01/logo.png",
            "videostar tv": "https://www.videostartv.eu/images/videostar.png",
            "canale 8": "https://upload.wikimedia.org/wikipedia/it/thumb/6/6d/TV8_Logo_2016.svg/1200px-TV8_Logo_2016.svg.png",
            "juwelo italia": "https://upload.wikimedia.org/wikipedia/commons/f/fd/Juwelo_TV.svg",
            "rtc telecalabria": "https://play-lh.googleusercontent.com/7PzluYVAEVOCNzGYGkewkKI3PA0PkCKAc9KUZGfYzAbZnQLnlPAE5iQBMZEUi7ZKwJc",
            "tele mia": "https://upload.wikimedia.org/wikipedia/commons/a/a6/Telemia.png",
            "bloomberg tv 4k": "https://github.com/tv-logo/tv-logos/blob/main/countries/united-states/bloomberg-television-us.png?raw=true",
            "tele abruzzo": "https://www.abruzzi.tv/logo-abruzzi.png",
            "fashiontv": "https://github.com/tv-logo/tv-logos/blob/main/countries/international/fashion-tv-int.png?raw=true",
            "quarta rete": "https://quartarete.tv/wp-content/uploads/2022/06/Logo-Quartarete-ok.png",
            "fashion tv": "https://github.com/tv-logo/tv-logos/blob/main/countries/international/fashion-tv-int.png?raw=true",
            "love fm tv": "https://www.lovefm.it/themes/default/assets/img_c/logo-love-new.png",
            "telerama": "https://upload.wikimedia.org/wikipedia/commons/b/b1/T%C3%A9l%C3%A9rama_logo.png",
            "teletubbies": "https://banner2.cleanpng.com/20180606/qrg/aa9vorpin.webp",
            "primo canale": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/primocanale-it.png?raw=true",
            "lira tv": "https://liratv.es/wp-content/uploads/2021/07/LIRA-TV-1.png",
            "la tr3": "https://www.tvdream.net/img/latr3.png",
            "tele liguria sud": "https://www.teleliguriasud.it/sito/wp-content/uploads/2024/10/LOGO-RETINA.png",
            "la nuova tv": "https://play-lh.googleusercontent.com/Ck_esrelbBPGT2rsTtvuvciOBHA0f5b-VExXvBf-NP9fegvHhEuN9MIx7pgdv1WlW8o",
            "top calcio 24": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRPHW5VLQDGnNMVZszgWZRqnBSjPUTgAcUltQ&s",
            "fm italia": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRtJ5HlBu4jXOrC4iA-giQNzXa9zm42bS-yrA&s",
            "supersix lombardia": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_ebhZMV4eYibx6UpVDOt1KOlmhOPYBh0gKw&s",
            "prima tv": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Prima_TV_Logo_2022.svg/800px-Prima_TV_Logo_2022.svg.png",
            "camera dei deputati": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/camera-dei-deputati-it.png?raw=true",
            "tele venezia": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ0xhoeVg7nRLPp8GnPkFzLUWvJ5WolvU-iYw&s",
            "telemolise": "https://m.media-amazon.com/images/I/61yiY3jR+kL.png",
            "esperia tv 18": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/ESPERIATV18_verde.png/260px-ESPERIATV18_verde.png",
            "onda novara tv": "https://gag-fondazionedeagostini.s3.amazonaws.com/wp-content/uploads/2023/03/logo-Onda-Novara-TV-Ufficiale-1.png",
            "carina tv": "https://radiocarina.it/wp-content/uploads/2024/01/RadioCarina-Vers.2.png",
            "teleromagna": "https://teleromagna.it/images/teleromagna-logo.png",
            "elive tv brescia": "https://upload.wikimedia.org/wikipedia/commons/e/ec/%C3%88_live_Brescia_logo.png",
            "bellla & monella tv": "https://upload.wikimedia.org/wikipedia/commons/0/0e/Logo_Ufficiale_Radio_Bellla_%26_Monella.png",
            "videotolentino": "https://yt3.googleusercontent.com/ytc/AIdro_kAZM1WRzE6qfQx90xPJ3v1Jz1gaJwn6BbrZcewu6eTcQ=s900-c-k-c0x00ffffff-no-rj",
            "super tv brescia": "https://bresciasat.it/assets/front/img/logo3.png",
            "umbria tv": "https://upload.wikimedia.org/wikipedia/commons/0/09/Umbria_TV_wordmark%2C_ca._2020.png",
            "qvc italia": "https://github.com/tv-logo/tv-logos/blob/main/countries/germany/qvc-de.png?raw=true",
            "rttr": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/rttr-it.png?raw=true",
            "onda tv": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9Og_2yYQhg-ersjEG5xZ99bri_Di4l5dlyw&s",
            "rttr tv": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/rttr-it.png?raw=true",
            "teleboario": "https://i.ytimg.com/vi/vNB5TJBjA3U/sddefault.jpg",
            "video novara": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ1PvoHpnx0hNKtt435CUaJza2e_qsm5B87Cg&s",
            "fano tv": "https://prolocopesarourbino.it/wp-content/uploads/2019/07/FANO-TV.jpg",
            "etv marche": "https://etvmarche.it/wp-content/uploads/2021/05/Logo-Marche-BLU.png",
            "granducato": "https://www.telegranducato.it/wp-content/uploads/img_struttura_sito/logo_granducato_ridotto.png",
            "maria+vision italia": "",
            "star comedy": "https://github.com/tv-logo/tv-logos/blob/main/countries/portugal/star-comedy-pt.png?raw=true",
            "telecolor": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/telecolore-it.png?raw=true",
            "telequattro": "https://telequattro.medianordest.it/wp-content/uploads/2020/10/T4Logo.png",
            "tele tusciasabina 2000": "https://yt3.googleusercontent.com/ytc/AIdro_lp10Brud3JZex6CgE4M9c-XcKFY4MrRhcFe9PUn-N4SD4=s900-c-k-c0x00ffffff-no-rj",
            "stereo 5 tv": "https://www.stereo5.it/2022/wp-content/uploads/2023/02/LOGO-NUOVO-2023-2.png",
            "televideo agrigento": "https://lh3.googleusercontent.com/proxy/UNXKnLrwdDNoio4peXah3Pz81kI5Cv2FzJo82TPzn4seN-JZ3tovuVe45XSRBkIyMOfrrZ3bnWaMsTi80Xj40Q",
            "vco azzurra tv": "https://upload.wikimedia.org/wikipedia/commons/9/91/Logo_VCO_Azzurra_TV.png",
            "company tv": "https://www.trendcomunicazione.com/wp-content/uploads/2018/11/20180416-logo-tv-bokka-300x155.png",
            "tele pavia": "https://www.milanopavia.tv/wp-content/uploads/2020/01/logoMilanoPaviaTV.png",
            "uninettuno": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSYRpKemP5FC0RLOQVhc9kPU71aJW9Tj9DU8g&s",
            "star life": "https://github.com/tv-logo/tv-logos/blob/main/countries/argentina/star-life-ar.png?raw=true",
            "vera tv": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/vera-tv-it.png?raw=true",
            "arancia tv": "",
            "entella tv": "https://m.media-amazon.com/images/I/81omr2rZ8+L.png",
            "euro tv": "https://upload.wikimedia.org/wikipedia/it/9/93/Eurotv.png",
            "peer tv alto adige": "https://www.cxtv.com.br/img/Tvs/Logo/webp-l/6e7dee025526c334b9280153c418e10e.webp",
            "esperia tv": "https://upload.wikimedia.org/wikipedia/commons/b/b3/Logo_ESPERIAtv.png",
            "tele friuli": "https://www.telefriuli.it/wp-content/uploads/2022/11/logo_telefriuli_positivo.png",
            "rtp": "https://upload.wikimedia.org/wikipedia/commons/7/7c/RTP.png",
            "icaro tv": "https://www.gruppoicaro.it/wp-content/uploads/2020/05/icarotv.png",
            "telea tv": "https://www.tvdream.net/img/telea-tv.png",
            "telemantova": "https://www.telemantova.it/gfx/lib/ath-v1/logos/tmn/plain.svg?20241007",
            "bloomberg tv": "https://github.com/tv-logo/tv-logos/blob/main/countries/united-states/bloomberg-television-us.png?raw=true",
            "super j": "https://e7.pngegg.com/pngimages/439/74/png-clipart-superman-superhero-drawing-super-man-font-superhero-heart.png",
            "uninettuno university tv": "https://www.laureaonlinegiurisprudenza.it/wp-content/uploads/2019/09/Logo-Uninettuno.png",
            "rds social tv": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/RDS-Logo.png/260px-RDS-Logo.png",
            "rete tv italia": "https://www.retetvitalia.it/news/wp-content/uploads/2019/07/cropped-RTI-L.png",
            "fm italia tv": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRtJ5HlBu4jXOrC4iA-giQNzXa9zm42bS-yrA&s",
            "telenord": "https://upload.wikimedia.org/wikipedia/it/a/a8/Telenord.png",
            "equ tv": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/equ-tv-it.png?raw=true",
            "orler tv": "https://www.tvdream.net/img/orlertv.png",
            "rmc 101": "https://upload.wikimedia.org/wikipedia/commons/f/fc/LogoRMC101.png",
            "telebari": "https://www.aaroiemac.it/notizie/wp-content/uploads/2018/11/1524066248-telebari.png",
            "telepace trento": "https://www.tvdream.net/img/telepace-trento.png",
            "trentino tv": "https://www.trentinotv.it/images/resource/logo-trentino.png",
            "tv qui": "https://www.tvdream.net/img/tvqui-modena-cover.jpg",
            "tv 33": "https://d1yjjnpx0p53s8.cloudfront.net/styles/logo-thumbnail/s3/0013/3844/brand.gif?itok=54JkEUiu",
            "trm h24": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/trm-h24-it.png?raw=true",
            "tt teletutto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQpzqT0DLXv-md7VU-fTF5BeaEashocwHUdw&s",
            "teletricolore": "https://www.teletricolore.it/wp-content/uploads/2018/02/logo.png",
            "globus television": "https://ennapress.it/wp-content/uploads/2020/10/globus.png",
            "rtr 99 tv": "https://www.tvdream.net/img/rtr99-cover.jpg",
            "tele romagna": "https://teleromagna.it/images/teleromagna-logo.png", 
            "telecitta": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Logo_Telecitt%C3%A0.svg/800px-Logo_Telecitt%C3%A0.svg.png",
            "rds social": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/RDS-Logo.png/260px-RDS-Logo.png", 
            "super tv aristanis": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQFBXh88zZx4IvyQKyYd5Hu2yeytO42zNQ4zA&s",
            "tv yes": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/tv-yes-it.png?raw=true",
            "quadrifoglio tv": "https://i.imgur.com/GfzpwKD.png",
            "telemistretta": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQN6reG7R24hdOigLSXg2G5oKcPqKt8cBc0jQ&s",
            "tele sirio": "https://www.telesirio.it/images/logo.png",
            "tvrs": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/tvrs-it.png?raw=true",
            "tele tricolore": "https://www.teletricolore.it/wp-content/uploads/2018/02/logo.png", 
            "telepace": "https://e7.pngegg.com/pngimages/408/890/png-clipart-telepace-high-definition-television-hot-bird-%C4%8Ct1-albero-della-vita-television-text.png",
            "baby tv": "https://github.com/tv-logo/tv-logos/blob/main/countries/spain/baby-tv-es.png?raw=true",
            "mtv hits": "https://github.com/tv-logo/tv-logos/blob/main/countries/serbia/mtv-hits-rs.png?raw=true",
            "radio freccia": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/radio-freccia-it.png?raw=true",
            "bella radio tv": "https://i0.wp.com/bellaradio.it/wp-content/uploads/2020/01/Bella-2020-3.png?fit=3000%2C3000&ssl=1",
            "ol3 radio": "https://pbs.twimg.com/profile_images/570326948497195008/Wf6DPfFP_400x400.jpeg",
            "51 radio tv": "https://tvtvtv.ru/icons/51_tv.png",
            "radionorba tv": "https://github.com/tv-logo/tv-logos/blob/main/countries/italy/radio-norba-tv-it.png?raw=true",
            "euro indie music chart tv": "https://m.media-amazon.com/images/I/61Wa4RqJVJL.png",
            "tele radio sciacca": "https://pbs.twimg.com/profile_images/613988173203423232/rWCQ9j6h_400x400.png",
            "radio capital": "https://static.wikia.nocookie.net/logopedia/images/1/1e/Radio_Capital_-_Logo_2019.svg.png/revision/latest?cb=20190815181629",
            "radio 51": "https://tvtvtv.ru/icons/51_tv.png" 
        }

    CATEGORY_KEYWORDS = {
        "Rai": ["rai"],
        "Mediaset": ["twenty seven", "twentyseven", "mediaset", "italia 1", "italia 2", "canale 5", "la 5", "cine 34", "top crime", "iris", "focus", "rete 4"],
        "Sport": ["inter", "milan", "lazio", "calcio", "tennis", "sport", "sportitalia", "trsport", "sports", "super tennis", "supertennis", "dazn", "eurosport", "sky sport", "rai sport"],
        "Film - Serie TV": ["crime", "primafila", "cinema", "movie", "film", "serie", "hbo", "fox", "rakuten", "atlantic"],
        "News": ["news", "tg", "rai news", "sky tg", "tgcom", "euronews"],
        "Bambini": ["frisbee", "super!", "fresbee", "k2", "cartoon", "boing", "nick", "disney", "baby", "rai yoyo", "cartoonito"],
        "Documentari": ["documentaries", "discovery", "geo", "history", "nat geo", "nature", "arte", "documentary"],
        "Musica": ["deejay", "rds", "hits", "rtl", "mtv", "vh1", "radio", "music", "kiss", "kisskiss", "m2o", "fm"],
        "Altro": ["real time"]
    }

    def classify_channel(name):
        name_lower = name.lower()
        for category, words in CATEGORY_KEYWORDS.items():
            for word in words:
                # Gestione speciale per parole con caratteri speciali
                if any(char in word for char in ['!', '&', '+', '-']):
                    # Per parole con caratteri speciali, usa una ricerca diretta
                    if word in name_lower:
                        return category
                else:
                    # Per parole normali, usa word boundaries
                    pattern = r'\b' + re.escape(word) + r'\b'
                    if re.search(pattern, name_lower):
                        return category
        return "Altro"

    def get_channels():
        signature = getAuthSignature()
        headers = {
            "user-agent": "okhttp/4.11.0",
            "accept": "application/json",
            "content-type": "application/json; charset=utf-8",
            "accept-encoding": "gzip",
            "mediahubmx-signature": signature
        }
        all_channels = []
        for group in vavoo_groups():
            cursor = 0
            while True:
                data = {
                    "language": "de",
                    "region": "AT",
                    "catalogId": "iptv",
                    "id": "iptv",
                    "adult": False,
                    "search": "",
                    "sort": "name",
                    "filter": {"group": group},
                    "cursor": cursor,
                    "clientVersion": "3.0.2"
                }
                resp = requests.post("https://vavoo.to/mediahubmx-catalog.json", json=data, headers=headers, timeout=10)
                r = resp.json()
                items = r.get("items", [])
                all_channels.extend(items)
                cursor = r.get("nextCursor")
                if not cursor:
                    break
        return all_channels

    def create_tvg_id_map(epg_file="epg.xml"):
        """Legge un file EPG XML e mappa i nomi dei canali normalizzati ai loro tvg-id."""
        tvg_id_map = {}
        try:
            tree = ET.parse(epg_file)
            root = tree.getroot()
            for channel in root.findall('.//channel'):
                tvg_id = channel.get('id')
                display_name = channel.find('display-name').text
                if tvg_id and display_name:
                    normalized_name = normalize_channel_name(display_name)
                    tvg_id_map[normalized_name] = tvg_id
        except Exception as e:
            print(f"Errore nella lettura di {epg_file}: {e}")
        return tvg_id_map

    def save_as_m3u(channels, daddylive_channels=None, filename="italy.m3u"):
        logos = fetch_logos()
        epg_xml_path = os.path.join(output_dir, "epg.xml")
        tvg_id_map = create_tvg_id_map(epg_xml_path)
        channels_by_category = {}

        # MAPPA SEMPLIFICATA PER RENAME
        VAVOO_RENAME_MAP = {
            "DISCOVERY FOCUS": "FOCUS",
            "CINE 34 MEDIASET": "CINE 34", 
            "MEDIASET IRIS": "IRIS",
            "MEDIASET 1": "ITALIA 1",
            "ZONA DAZN": "DAZN",
            "27 TWENTY SEVEN": "27 TWENTYSEVEN"
        }

        # Processa i canali Vavoo (che sono dizionari)
        if channels and isinstance(channels[0], dict):
            for ch in channels:
                original_name = ch.get("name", "SenzaNome")
                name = clean_channel_name(original_name)
                
                # Applica il rename
                display_name = VAVOO_RENAME_MAP.get(name.upper(), name)
                
                # USA IL NOME MODIFICATO PER IL LOOKUP
                name_for_lookup = display_name  # Nome modificato per ricerca logo/tvg-id
                
                url = ch.get("url", "")
                category = classify_channel(display_name)

                if url:
                    if category not in channels_by_category:
                        channels_by_category[category] = []
                    
                    # USA IL NOME MODIFICATO PER RICERCA LOGO E TVG-ID
                    logo = logos.get(name_for_lookup.lower(), "")
                    tvg_id = tvg_id_map.get(normalize_channel_name(name_for_lookup), "")
                    
                    channels_by_category[category].append({
                        "name": display_name,      # Nome modificato per display
                        "url": url,
                        "logo": logo,             # Logo trovato con nome modificato
                        "tvg_id": tvg_id         # TVG-ID trovato con nome modificato
                    })

        # Processa i canali Daddylive se presenti
        if daddylive_channels:
            for raw_name, stream_url_with_id in daddylive_channels:
                # Pulizia e trasformazione del nome come nella logica originale
                name_after_initial_clean = clean_channel_name(raw_name)
                # Rimuovi "italy" e converti in maiuscolo
                base_daddy_name = re.sub(r'italy', '', name_after_initial_clean, flags=re.IGNORECASE).strip()
                base_daddy_name = re.sub(r'\s+', ' ', base_daddy_name).strip()
                base_daddy_name = base_daddy_name.upper()

                # Estrai l'ID del canale dall'URL per la correzione
                stream_url = stream_url_with_id
                channel_id_match = re.search(r'id=(\d+)', stream_url)
                channel_id = channel_id_match.group(1) if channel_id_match else None

                if channel_id == "877":
                    print(f"[CORREZIONE FINALE] Canale ID {channel_id} ('{base_daddy_name}') forzato a 'DAZN'")
                    base_daddy_name = "DAZN"
                    
                if channel_id == "853":
                    print(f"[CORREZIONE FINALE] Canale ID {channel_id} ('{base_daddy_name}') forzato a 'CANALE 5'")
                    base_daddy_name = "CANALE 5"

                # Usa la mappa fornita per la rinomina dei canali Sky Calcio specifici di Daddylive
                rename_map = {
                    "SKY CALCIO 1": "SKY SPORT 251",
                    "SKY CALCIO 2": "SKY SPORT 252",
                    "SKY CALCIO 3": "SKY SPORT 253",
                    "SKY CALCIO 4": "SKY SPORT 254",
                    "SKY CALCIO 5": "SKY SPORT 255",
                    "SKY CALCIO 6": "SKY SPORT 256",
                    "SKY CALCIO 7": "DAZN 1"
                }

                # Rimuovi eventuali numeri tra parentesi dal nome base prima della mappa
                base_daddy_name_clean = re.sub(r"\s*\(\d+\)", "", base_daddy_name).strip()
                if base_daddy_name_clean in rename_map:
                    base_daddy_name = rename_map[base_daddy_name_clean]

                # Skip DAZN
                if base_daddy_name == "DAZN" or base_daddy_name == "DAZN2":
                    continue

                # Aggiungi suffisso (D) per identificare i canali Daddylive
                final_name = f"{base_daddy_name} (D)"
                category = classify_channel(base_daddy_name)

                # Usa il nome base (senza suffisso) per cercare logo e tvg-id
                logo = logos.get(base_daddy_name.lower(), "")
                tvg_id = tvg_id_map.get(normalize_channel_name(base_daddy_name), "")

                if category not in channels_by_category:
                    channels_by_category[category] = []

                channels_by_category[category].append({
                    "name": final_name,
                    "url": stream_url,
                    "logo": logo,
                    "tvg_id": tvg_id
                })

        # Salva nel file M3U
        with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for category, channel_list in channels_by_category.items():
                channel_list.sort(key=lambda x: x["name"].lower())
                
                # Gestione dei canali duplicati (aggiungi suffisso numerico)
                name_count = {}
                url_by_name = {}
                # Prima passata: conta le occorrenze dei nomi e memorizza gli URL
                for ch in channel_list:
                    name = ch["name"]
                    url = ch["url"]
                    if name not in name_count:
                        name_count[name] = 1
                        url_by_name[name] = [url]
                    else:
                        name_count[name] += 1
                        url_by_name[name].append(url)

                # Seconda passata: rinomina i canali duplicati con URL diversi
                for ch in channel_list:
                    name = ch["name"]
                    url = ch["url"]
                    # Se ci sono più canali con lo stesso nome ma URL diversi
                    if name_count[name] > 1 and len(set(url_by_name[name])) > 1:
                        # Trova l'indice di questo URL nell'elenco degli URL per questo nome
                        idx = url_by_name[name].index(url) + 1
                        # Modifica il nome solo se non è già stato modificato
                        if not name.endswith(f"({idx})"):
                            ch["name"] = f"{name} ({idx})"

                f.write(f"\n# {category.upper()}\n")
                for ch in channel_list:
                    name = ch["name"]
                    url = ch["url"]
                    
                    # Usa logo e tvg_id pre-calcolati
                    logo = ch.get("logo", "")
                    tvg_id = ch.get("tvg_id", "")
                    
                    f.write(f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-logo="{logo}" group-title="{category}",{name}\n')
                    
                    # Aggiungi EXTHTTP headers per canali daddy (esclusi .php)
                    if "ava.karmakurama.com" in url and not url.endswith('.php'):
                        daddy_headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1", "Referrer": "https://ava.karmakurama.com/", "Origin": "https://ava.karmakurama.com"}
                        vlc_opt_lines = headers_to_extvlcopt(daddy_headers)
                        for line in vlc_opt_lines:
                            f.write(f'{line}\n')
                    
                    f.write(f'{url}\n')

        print(f"Playlist M3U salvata in: {os.path.join(output_dir, filename)}")
        print(f"Totale canali Vavoo: {len(channels)}")
        if daddylive_channels:
            print(f"Totale canali Daddylive: {len(daddylive_channels)}")
        print(f"Totale canali per categoria:")
        for category, channel_list in channels_by_category.items():
            print(f" {category}: {len(channel_list)} canali")

    def get_stream_from_channel_id(channel_id):
        """Risolve lo stream URL per un canale Daddylive dato il suo ID."""
        # Usa direttamente il metodo .php
        raw_php_url = f"{LINK_DADDY.rstrip('/')}/watch.php?id={channel_id}"
        print(f"URL .php per il canale Daddylive {channel_id}: {raw_php_url}")
        return raw_php_url

    def fetch_channels_from_daddy_json(json_url):
        """Estrae i canali italiani dalla pagina HTML di Daddylive (non più dal JSON)."""
        from bs4 import BeautifulSoup
        
        print(f"Recupero canali da {LINK_DADDY}/24-7-channels.php")
        channels = []
        seen_daddy_channel_ids = set()
        session = requests.Session()
    
        try:
            # Scarica la pagina HTML invece del JSON
            url = f"{LINK_DADDY}/24-7-channels.php"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15, verify=False)
            response.raise_for_status()
            
            # Parsa l'HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.find_all('a', class_='card')
            
            print(f"Trovati {len(cards)} canali nella pagina HTML di Daddylive.")
    
            for card in cards:
                # Estrae il nome del canale
                title_div = card.find('div', class_='card__title')
                if not title_div:
                    continue
                
                channel_name_raw = title_div.text.strip()
                
                # Estrae l'ID del canale
                href = card.get('href', '')
                if not ('id=' in href):
                    continue
                
                channel_id = href.split('id=')[1].split('&')[0]
    
                if not channel_name_raw or not channel_id:
                    continue
    
                # Correzione specifica per il canale ID 853
                if channel_id == "853":
                    print(f"[CORREZIONE] Trovato ID 853. Il nome '{channel_name_raw}' sarà forzato a 'Canale 5 Italy'.")
                    channel_name_raw = "Canale 5 Italy"
    
                # Filtro: deve contenere "italy" (case-insensitive)
                if "italy" in channel_name_raw.lower():
                    if channel_id in seen_daddy_channel_ids:
                        print(f"Skipping Daddylive channel '{channel_name_raw}' (ID: {channel_id}) perché l'ID è già stato processato.")
                        continue
                    seen_daddy_channel_ids.add(channel_id)
                    print(f"Trovato canale ITALIANO (Daddylive HTML): {channel_name_raw}, ID: {channel_id}. Tentativo di risoluzione stream...")
                    
                    # Usa il link .php come richiesto
                    stream_url = get_stream_from_channel_id(channel_id)
                    if stream_url:
                        url_with_id = stream_url
                        channels.append((channel_name_raw, url_with_id))
                        print(f"Aggiunto stream .php per {channel_name_raw}: {stream_url}")
                    else:
                        print(f"Impossibile risolvere lo stream per {channel_name_raw} (ID: {channel_id})")
            
            if not channels:
                print(f"Nessun canale italiano estratto/risolto dalla pagina HTML.")
    
        except requests.RequestException as e:
            print(f"Errore durante il download dalla pagina HTML: {e}")
        except Exception as e:
            print(f"Errore imprevisto durante il parsing della pagina HTML: {e}")
        
        return channels

    if __name__ == "__main__":
        # 1. Canali da sorgenti Vavoo (JSON)
        print("\n--- Fetching canali da sorgenti Vavoo (JSON) ---")
        channels = get_channels()
        print(f"Trovati {len(channels)} canali Vavoo.")
        
        # 2. Canali dalla pagina HTML di Daddylive (se abilitato)
        daddylive_channels = None
        if CANALI_DADDY:
            print("\n--- Fetching canali da Daddylive (HTML) ---")
            daddy_json_url = f"{LINK_DADDY.rstrip('/')}/daddy.json"
            daddylive_channels = fetch_channels_from_daddy_json(daddy_json_url)

            # Aggiungi manualmente il canale DAZN (ID 877) se non è già presente
            if not any(item[1] and 'id=877' in item[1] for item in daddylive_channels):
                print("[INFO] Aggiunta manuale del canale DAZN (ID: 877)...")
                # Usa il link .php come richiesto
                stream_url_877 = get_stream_from_channel_id("877")
                if stream_url_877:
                    daddylive_channels.append(("DAZN Italy (D)", stream_url_877))
                    print("[✓] Canale DAZN (ID: 877) aggiunto con successo.")

            print(f"Trovati {len(daddylive_channels)} canali Daddylive.")
        else:
            print("\n--- Canali Daddylive disabilitati (CANALI_DADDY=no) ---")
        
        # 3. Crea la playlist M3U
        print("\n--- Creazione playlist M3U ---")
        # Salva i canali Vavoo
        save_as_m3u(channels, filename="vavoo.m3u")
        
        # Salva i canali Daddylive se presenti
        if daddylive_channels:
            save_as_m3u([], daddylive_channels=daddylive_channels, filename="dlhd.m3u")
    
# Funzione per il settimo script (world_channels_generator.py)
def world_channels_generator():
    # Codice del settimo script qui
    # Aggiungi il codice del tuo script "world_channels_generator.py" in questa funzione.
    print("Eseguendo il world_channels_generator.py...")
    # Il codice che avevi nello script "world_channels_generator.py" va qui, senza modifiche.
    import requests
    import time
    import re
    
    def getAuthSignature():
        headers = {
            "user-agent": "okhttp/4.11.0",
            "accept": "application/json",
            "content-type": "application/json; charset=utf-8",
            "content-length": "1106",
            "accept-encoding": "gzip"
        }
        data = {
            "token": "tosFwQCJMS8qrW_AjLoHPQ41646J5dRNha6ZWHnijoYQQQoADQoXYSo7ki7O5-CsgN4CH0uRk6EEoJ0728ar9scCRQW3ZkbfrPfeCXW2VgopSW2FWDqPOoVYIuVPAOnXCZ5g",
            "reason": "app-blur",
            "locale": "de",
            "theme": "dark",
            "metadata": {
                "device": {
                    "type": "Handset",
                    "os": "Android",
                    "osVersion": "10",
                    "model": "Pixel 4",
                    "brand": "Google"
                }
            }
        }
        resp = requests.post("https://vavoo.to/mediahubmx-signature.json", json=data, headers=headers, timeout=10)
        return resp.json().get("signature")
    
    def vavoo_groups():
        # Puoi aggiungere altri gruppi per più canali
        return [""]
    
    def clean_channel_name(name):
        """Rimuove i suffissi .a, .b, .c dal nome del canale"""
        # Rimuove .a, .b, .c alla fine del nome (con o senza spazi prima)
        cleaned_name = re.sub(r'\s*\.(a|b|c|s|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|t|u|v|w|x|y|z)\s*$', '', name, flags=re.IGNORECASE)
        return cleaned_name.strip()
    
    def get_channels():
        signature = getAuthSignature()
        headers = {
            "user-agent": "okhttp/4.11.0",
            "accept": "application/json",
            "content-type": "application/json; charset=utf-8",
            "accept-encoding": "gzip",
            "mediahubmx-signature": signature
        }
        all_channels = []
        for group in vavoo_groups():
            cursor = 0
            while True:
                data = {
                    "language": "de",
                    "region": "AT",
                    "catalogId": "iptv",
                    "id": "iptv",
                    "adult": False,
                    "search": "",
                    "sort": "name",
                    "filter": {"group": group},
                    "cursor": cursor,
                    "clientVersion": "3.0.2"
                }
                resp = requests.post("https://vavoo.to/mediahubmx-catalog.json", json=data, headers=headers, timeout=10)
                r = resp.json()
                items = r.get("items", [])
                all_channels.extend(items)
                cursor = r.get("nextCursor")
                if not cursor:
                    break
        return all_channels
    
    def save_as_m3u(channels, filename="world.m3u"):
        # Raggruppa i canali per categoria
        channels_by_category = {}
        
        for ch in channels:
            original_name = ch.get("name", "SenzaNome")
            # Pulisce il nome rimuovendo .a, .b, .c
            name = clean_channel_name(original_name)
            url = ch.get("url", "")
            category = ch.get("group", "Generale")  # Usa il campo "group" come categoria
            
            if url:
                if category not in channels_by_category:
                    channels_by_category[category] = []
                channels_by_category[category].append((name, url))
        
        with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            
            # Scrivi i canali raggruppati per categoria
            for category, channel_list in channels_by_category.items():
                # Aggiungi un commento per la categoria
                f.write(f"\n# {category.upper()}\n")
                
                for name, url in channel_list:
                    f.write(f'#EXTINF:-1 group-title="{category}",{name}\n{url}\n')
        
        print(f"Playlist M3U salvata in: {os.path.join(output_dir, filename)}")
        print(f"Canali organizzati in {len(channels_by_category)} categorie:")
        for category, channel_list in sorted(channels_by_category.items()):
            print(f"  - {category}: {len(channel_list)} canali")
    
    if __name__ == "__main__":
        channels = get_channels()
        print(f"Trovati {len(channels)} canali. Creo la playlist M3U con i link proxy...")
        save_as_m3u(channels) 

def sportsonline():
    import requests
    import re
    from bs4 import BeautifulSoup
    import datetime
    
    # URL del file di programmazione
    PROG_URL = "https://sportsonline.sn/prog.txt"
    # Lingua che vogliamo cercare
    TARGET_LANGUAGE = "ITALIAN"
    
    def get_italian_channels(lines):
        """
        Analizza le righe del file di programmazione per trovare i canali in italiano.
        Restituisce una lista di identificativi dei canali (es. ['hd7']).
        """
        italian_channels = []
        for line in lines:
            # Cerca le righe che definiscono la lingua di un canale
            if TARGET_LANGUAGE in line.upper():
                # Estrae l'identificativo del canale (es. "HD7") e lo converte in minuscolo
                channel_id = line.split()[0].lower()
                italian_channels.append(channel_id)
                print(f"[INFO] Trovato canale italiano: {channel_id.upper()}")
        return italian_channels
    
    def main():
        """
        Funzione principale che orchestra il processo.
        """
        # --- Controllo del giorno della settimana ---
        today_weekday = datetime.date.today().weekday() # Lunedì=0, Martedì=1, ..., Domenica=6
        weekdays_english = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
        # Applichiamo sempre il filtro per il giorno corrente
        day_to_filter = weekdays_english[today_weekday]
        print(f"Oggi è {day_to_filter}, verranno cercati solo gli eventi_dlhd di oggi.")
    
        print(f"1. Scarico la programmazione da: {PROG_URL}")
        try:
            response = requests.get(PROG_URL, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"[ERRORE FATALE] Impossibile scaricare il file di programmazione: {e}")
            return
    
        lines = response.text.splitlines()
    
        print("\n2. Cerco i canali in lingua italiana...")
        italian_channels = get_italian_channels(lines)
    
        playlist_entries = []
    
        if not italian_channels:
            print("[ATTENZIONE] Nessun canale italiano trovato nella programmazione.")
            print("[INFO] Creo un canale fallback 'NESSUN EVENTO'...")
            playlist_entries.append({
                "name": "NESSUN EVENTO", 
                "url": "https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8",
                "referrer": "https://sportsonline.sn/",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
        else:
            print("\n3. Cerco gli Eventi trasmessi sui canali italiani...")
    
            # --- NUOVA LOGICA DI SCANSIONE PER GIORNO ---
            processing_today_events = (day_to_filter is None) # Se è weekend, processa tutto
    
            for line in lines:
                line_upper = line.upper().strip()
    
                # Controlliamo se la riga è un'intestazione di un giorno della settimana
                if line_upper in weekdays_english:
                    if day_to_filter and line_upper == day_to_filter:
                        # Abbiamo trovato la sezione del giorno corrente, iniziamo a processare
                        processing_today_events = True
                    else:
                        # Abbiamo trovato un altro giorno, smettiamo di processare
                        processing_today_events = False
                    continue
    
                # Processiamo la riga solo se siamo nella sezione del giorno giusto (o se è weekend)
                if not processing_today_events:
                    continue
    
                # Da qui in poi, la logica è la stessa, ma viene eseguita solo sulle righe corrette
                if '|' not in line:
                    continue
    
                parts = line.split('|')
                if len(parts) != 2:
                    continue
    
                event_info = parts[0].strip()
                page_url = parts[1].strip()
    
                is_italian_event = any(f"/{channel}.php" in page_url for channel in italian_channels)
    
                if is_italian_event:
                    print(f"\n[EVENTO] Trovato evento italiano: '{event_info}'")
                    
                    # Riformattiamo il nome dell'evento per mettere l'orario alla fine
                    event_parts = event_info.split(maxsplit=1)
                    if len(event_parts) == 2:
                        time_str_original, name_only = event_parts
                        
                        # --- Aggiungi 1 ora all'orario ---
                        try:
                            # Converte la stringa dell'orario in un oggetto datetime
                            original_time = datetime.datetime.strptime(time_str_original.strip(), '%H:%M')
                            # Aggiunge un'ora
                            new_time = original_time + datetime.timedelta(hours=1)
                            time_str = new_time.strftime('%H:%M')
                        except ValueError:
                            time_str = time_str_original.strip() # Usa l'orario originale se il formato non è valido
                        event_name = f"{name_only.strip()} {time_str}"
                    else:
                        event_name = event_info # Fallback se il formato non è quello previsto
    
                    # Aggiungiamo direttamente l'URL .php alla lista
                    playlist_entries.append({
                        "name": event_name,
                        "url": page_url,
                        "referrer": "https://sportsonline.sn/",
                        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    })
            
            # --- AGGIUNTA: Creazione canale fallback se non ci sono eventi_dlhd ---
            if not playlist_entries:
                print("\n[INFO] Nessun evento italiano con link streaming valido trovato oggi.")
                print("[INFO] Creo un canale fallback 'NESSUN EVENTO'...")
                playlist_entries.append({
                    "name": "NESSUN EVENTO", 
                    "url": "https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8",
                    "referrer": "https://sportsonline.sn/",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                })
    
        # 4. Creazione del file M3U
        output_filename = os.path.join(output_dir, "sportsonline.m3u")
        print(f"\n4. Scrivo la playlist nel file: {output_filename}")
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for entry in playlist_entries:
                f.write(f'#EXTINF:-1 group-title="Eventi Live SPORTSONLINE",{entry["name"]}\n')
                f.write(f'{entry["url"]}\n')
    
        print(f"\n[COMPLETATO] Playlist creata con successo! Apri il file '{output_filename}' con un player come VLC.")
    
    if __name__ == "__main__":
        main()

def search_m3u8_in_sites(channel_id, is_tennis=False, session=None):
    """
    Cerca i file .m3u8 nei siti specificati per i canali daddy e tennis
    """
    # Carica la variabile d'ambiente LINK_DADDY
    LINK_DADDY = os.getenv("LINK_DADDY", "").strip() or "https://dlhd.dad"
    # Restituisce direttamente l'URL .php come richiesto
    embed_url = f"{LINK_DADDY}/watch.php?id={channel_id}"
    print(f"URL .php per il canale Daddylive {channel_id}: {embed_url}")
    return embed_url

def remover_cache():
    """Rimuove i file di cache e temporanei dalla cartella scripts."""
    print("Eseguendo la pulizia dei file di cache...")
    files_to_delete = [
        os.path.join(script_dir, "daddyliveSchedule.json"),
    ]
    for filename in files_to_delete:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"File eliminato: {filename}")
            except Exception as e:
                print(f"Errore durante l'eliminazione di {filename}: {e}")
        else:
            print(f"File non trovato: {filename}")

# Funzione principale che esegue tutti gli script
def main():
    # load_daddy_cache()  # RIMOSSO: non più definita né necessaria
    try:
        canali_daddy_flag = os.getenv("CANALI_DADDY", "no").strip().lower()
        if canali_daddy_flag == "si":
            try:
                schedule_success = schedule_extractor()
            except Exception as e:
                print(f"Errore durante l'esecuzione di schedule_extractor: {e}")

        # Leggi le variabili d'ambiente
        eventi_dlhd_en = os.getenv("eventi_dlhd_EN", "no").strip().lower()
        world_flag = os.getenv("WORLD", "si").strip().lower()

        # EPG eventi_dlhd
        # Genera eventi_dlhd.xml solo se CANALI_DADDY è "si"
        if canali_daddy_flag == "si": # Questa riga è corretta
            json_input_path = os.path.join(script_dir, "daddyliveSchedule.json")
            try: # Questo blocco 'try' deve essere indentato sotto l'if
                if eventi_dlhd_en == "si":
                    epg_eventi_dlhd_generator_world(json_file_path=json_input_path, output_file_path=os.path.join(output_dir, "eventi_dlhd.xml"))
                else:
                    epg_eventi_dlhd_generator(json_file_path=json_input_path, output_file_path=os.path.join(output_dir, "eventi_dlhd.xml"))
            except Exception as e:
                print(f"Errore durante la generazione EPG eventi_dlhd: {e}")
                return # Interrompi l'esecuzione se la generazione EPG fallisce
        else: # Questo blocco 'else' deve essere l'else dell'if, non del try
            print("[INFO] Generazione eventi_dlhd.xml saltata: CANALI_DADDY non è 'si'.")

        # eventi_dlhd M3U8
        try:
            if canali_daddy_flag == "si":
                if eventi_dlhd_en == "si":
                    eventi_dlhd_m3u8_generator_world()
                else:
                    eventi_dlhd_m3u8_generator()
            else:
                print("[INFO] Generazione eventi_dlhd.m3u8 saltata: CANALI_DADDY non è 'si'.")
        except Exception as e:
            print(f"Errore durante la generazione eventi_dlhd.m3u8: {e}")
            return

        # EPG Merger
        try:
            epg_merger()
        except Exception as e:
            print(f"Errore durante l'esecuzione di epg_merger: {e}")
            return

        # Canali Italia
        try:
            italy_channels()
        except Exception as e:
            print(f"Errore durante l'esecuzione di italy_channels: {e}")
            return
            
        try:
            sportsonline()
        except Exception as e:
            print(f"Errore durante l'esecuzione di sportsonline: {e}")
            return
        
        # Canali World e Merge finale
        try:
            if world_flag == "si":
                world_channels_generator()
                merger_playlistworld()
            elif world_flag == "no":
                merger_playlist()
            else:
                print(f"Valore WORLD non valido: '{world_flag}'. Usa 'si' o 'no'.")
                return
        except Exception as e:
            print(f"Errore nella fase finale: {e}")
            return

        print("Tutti gli script sono stati eseguiti correttamente!")
    finally:
        pass  # save_daddy_cache() RIMOSSO: non più definita né necessaria
        remover_cache() # Aggiunta pulizia cache alla fine

if __name__ == "__main__":
    main()
