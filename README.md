# 📺 Lista IPTV + EPG con Proxy

Benvenuto nella tua **lista IPTV personalizzata** con **EPG** integrata e supporto proxy, perfetta per goderti i tuoi contenuti preferiti ovunque ti trovi!

---

## 🌟 Cosa include la lista?

- **🎥 Pluto TV Italia**  
  Il meglio della TV italiana con tutti i canali Pluto TV sempre disponibili.

- **⚽ Eventi Sportivi Live**  
  Segui in diretta **calcio**, **basket** e altri sport. Non perderti neanche un'azione!

- **📡 Sky e altro ancora**  
  Contenuti esclusivi: film, serie TV, sport e molto di più direttamente da Sky.

---

## 🔗 Link Lista + EPG

Queste liste devono essere utilizzate con un proxy.

- **Lista M3U**  
  [`https://raw.githubusercontent.com/nzo66/TV/refs/heads/main/lista.m3u`](https://raw.githubusercontent.com/nzo66/TV/refs/heads/main/lista.m3u)

- **EPG XML**  
  [`https://raw.githubusercontent.com/nzo66/TV/refs/heads/main/epg.xml`](https://raw.githubusercontent.com/nzo66/TV/refs/heads/main/epg.xml)

---

## 🔗 Link Film & MPD TEST

Queste liste devono essere utilizzate con mediaflow-proxy usando questo link per generare l' URL da usare.
[`[https://nzo666-playlist-generator.hf.space]`](https://nzo666-playlist-generator.hf.space)

- **Lista Film**  
  [`https://raw.githubusercontent.com/nzo66/TV/refs/heads/main/film.m3u`](https://raw.githubusercontent.com/nzo66/TV/refs/heads/main/film.m3u)

- **Lista MPD** (solo ip Europeo)
  [`https://raw.githubusercontent.com/nzo66/TV/refs/heads/main/mpd.m3u`](https://raw.githubusercontent.com/nzo66/TV/refs/heads/main/mpd.m3u)

---

## 📺 Come aggiungere la lista su Stremio

Per utilizzare questa lista IPTV su Stremio, dovrai usare l'addon **OMG Premium TV**:

### 🚀 Installazione OMG Premium TV

1. **Usa questo fork specifico**: [https://github.com/nzo66/OMG-Premium-TV](https://github.com/nzo66/OMG-Premium-TV)  
2. **Deploy su Docker** tramite Hugging Face o VPS seguendo la guida nel repository  
3. **Configura l'addon** inserendo:
   - **URL M3U**: Il link della lista M3U sopra indicato con il proxy 
   - **URL EPG**: Il link dell'EPG XML sopra indicato  
   - **Abilita EPG**: Metti la spunta su Abilita EPG
   - **Proxy URL**: NON METTERE NULLA!
   - **Proxy Password**: NON METTERE NULLA!
   - **Forza Proxy**: NO!
   - **Intervallo Aggiornamento Playlist**: Metti 02:00
4. **Installa su Stremio** cliccando sul pulsante "INSTALLA SU STREMIO"

### ✨ Funzionalità disponibili

Con OMG Premium TV potrai sfruttare:
- Supporto playlist **M3U/M3U8** complete  
- **EPG integrata** con informazioni sui programmi  
- **Filtri per genere** e ricerca canali  
- **Proxy per maggiore compatibilità**  
- **Resolver Python** per stream speciali  
- **Backup e ripristino** della configurazione  

---

### ✅ Crea il tuo proxy personalizzato

- **Mediaflow Proxy**:  
  [mediaflow-proxy](https://github.com/mhdzumair/mediaflow-proxy)
  
- **Mediaflow Proxy Per HuggingFace**
  
  `(usa Mediaflow Proxy solo per lista Film e MPD)`

  Usa questa repo ottimizzata: [hfmfp](https://github.com/nzo66/hfmfp)

- **TvProxy**:
  [tvproxy (repo GitHub)](https://github.com/nzo66/tvproxy)

  `usando questo proxy hai la possibilita' di installarlo su un qualsiasi dispositivo android grazie all'app Termux`

---

## ⚙️ Vuoi Personalizzare la lista

### 1. Fai il fork della repo

Avvia creando un fork della repository proxy.

### 2. Modifica il file `.env`.

---

### 🔁 Come proxare le liste con Mediaflow-Proxy e TvProxy assieme?

Usa questo: [`https://github.com/nzo66/Playlist-Generator`](https://github.com/nzo66/Playlist-Generator)

Questo ti permetterà di servire la lista M3U attraverso il tuo proxy personale in modo sicuro e performante.

---

### 🔁 Come proxare la lista con TvProxy?

Utilizza il seguente URL: `https://<server-ip>/proxy?url=<url-lista>`

questo sara il link della tua lista da mettere nelle app iptv!

Sostituisci:

- `<server-ip>` con l'indirizzo IP del tuo server TvProxy
- `<url-lista>` con l'URL effettivo della tua lista M3U (es. quello GitHub)

Questo ti permetterà di servire la lista M3U attraverso il tuo proxy personale in modo sicuro e performante.

---

## 🚀 Esecuzione automatica con GitHub Actions

Dopo le modifiche:

1. Vai sulla sezione **Actions** della tua repo  
2. Avvia manualmente lo script  
3. Assicurati che **GitHub Actions sia abilitato** nella repository  

---

## 🤝 Hai bisogno di aiuto?

Apri una **issue** o proponi un miglioramento con una **pull request**.  
Contribuire è sempre benvenuto!
