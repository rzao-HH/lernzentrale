# Robins Lernzentrale

Lern-Web-App für die 6. Klasse: 📐 Winkel-Akademie · 🪄 Wasser-Zauberschule · 🐚 Küsten-Crew · 🕵️ Detektiv-Büro – mit Lernplan, Rangliste, Arena und Lerngruppen.

- **Adresse:** https://rzao-hh.github.io/lernzentrale/ (GitHub Pages, Branch `main`, Ordner `/`)
- **Offline:** `sw.js` speichert alle Dateien; nach einem Besuch mit Internet läuft alles auch ohne Netz.

## Aufbau
| Pfad | Inhalt |
|---|---|
| `index.html` | Startseite (nur Gerüst) |
| `css/start.css` | Aussehen der Startseite |
| `js/sync.js` | Geräte-Abgleich über Supabase (`lz_pull` / `lz_push`) |
| `js/start.js` | Startseite: Personen, Lernplan-Übersicht, Rangliste |
| `js/router.js` | Öffnet die Apps (iframes aus `apps/`) |
| `js/groups.js` | Lerngruppen: anlegen, teilen, beitreten |
| `js/arena.js` | Arena: Tauziehen, Power-ups, Geister-Duell, Glücksrad |
| `js/news.js` | „Was ist neu?“ |
| `apps/*.html` | Die vier Apps |
| `js/app-core.js`, `js/nutzer-init.js`, `js/nutzer.js`, `js/lernplan.js`, `js/home-btn.js`, `js/arena-btn.js`, `css/nutzer.css`, `css/lernplan.css` | Gemeinsame Bausteine aller Apps |
| `sw.js` | Service Worker (Offline) |
| `tests/` | Automatische Browser-Tests (`python tests/run_all.py`) |
| `archiv/` | Stände vor Version 5.0.0 |

## Speicher
Alles liegt im Browser (localStorage) derselben Adresse. Schlüssel u. a. `nutzer-alle`, `lz-ergebnisse`, `lernplan-*`, `lzp-*`, App-Stände (`winkelakademie-v1`, `wasserzauberschule-v1`, `unit6-progress`, `detektivbuero-v1`), `lz-groups@…`, `lz-arena-…`.
Geräte-Code (`lz-fam`) und Lerngruppen-Codes stehen nie im Code.

## Versionen
`Umbau.Funktion.Korrektur` – erste Stelle nur bei großen, für Benutzer spürbaren Umbauten; zweite bei neuen Funktionen oder Umbauten im Hintergrund; dritte bei kleinen Korrekturen. Bei jedem Update: Versionsnummer in `index.html`, `js/news.js` und `sw.js` (`VER`) sowie `?v=` in den Verweisen anheben.
