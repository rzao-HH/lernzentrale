# Robins Lernzentrale

Lern-Web-App für die 6. Klasse: 📐 Winkel-Akademie · 🪄 Wasser-Zauberschule · 🐚 Küsten-Crew · 🕵️ Detektiv-Büro – mit Lernplan, Rangliste, Arena und Lerngruppen.

- **Adresse:** https://rzao-hh.github.io/lernzentrale/ (GitHub Pages, Branch `main`, Ordner `/`)
- **Offline:** `sw.js` speichert alle Dateien; nach einem Besuch mit Internet läuft alles auch ohne Netz.

## Aufbau
| Pfad | Inhalt |
|---|---|
| `index.html` | Startseite (nur Gerüst) |
| `css/start.css` | Aussehen der Startseite |
| `js/sync.js` | Abgleich pro Benutzername über Supabase (`lz_pull` / `lz_push`) |
| `js/konto.js` | Anmelden mit Benutzername |
| `js/start.js` | Startseite: Personen, Lernplan-Übersicht, Rangliste |
| `js/router.js` | Öffnet die Apps (iframes aus `apps/`) |
| `js/groups.js` | Lerngruppen: anlegen, teilen, beitreten |
| `js/arena.js` | Arena: Tauziehen, Power-ups, Geister-Duell, Glücksrad (online-Anzeige und Live-Züge über die Datenbank der Lerngruppe, Abfrage alle 1–3 s) |
| `js/news.js` | „Was ist neu?“ |
| `apps/*.html` | Die vier Apps |
| `js/app-core.js`, `js/nutzer-init.js`, `js/nutzer.js`, `js/lernplan.js`, `js/home-btn.js`, `js/arena-btn.js`, `css/nutzer.css`, `css/lernplan.css` | Gemeinsame Bausteine aller Apps |
| `sw.js` | Service Worker (Offline) |
| `tests/` | Automatische Browser-Tests (`python tests/run_all.py`) |
| `archiv/` | Stände vor Version 5.0.0 |
| `lernzettel/` | Fotos der Arbeitsblätter je Fach als HTML-Dateien, Übersicht in `lernzettel/README.md` (nicht Teil der App, nicht im Offline-Speicher) |

> **Lernzettel:** Die aktuellen Lernzettel-Dateien liegen in `lernzettel/`, mit Übersicht in `lernzettel/README.md`. Änderungen immer dort ablegen, nicht als separate Datei in einem Chat.

## Speicher
Auf dem Gerät liegt alles im localStorage derselben Adresse. Schlüssel u. a. `nutzer-alle`, `lz-ergebnisse`, `lernplan-*@<person>` (Lernplan pro Person), `lzp-*`, App-Stände (`winkelakademie-v1`, `wasserzauberschule-v1`, `unit6-progress`, `detektivbuero-v1`), `lz-groups@…`, `lz-arena-…`.

## Konten
Jede Person meldet sich mit einem Benutzernamen an (überall eindeutig, Groß-/Kleinschreibung egal, noch ohne Passwort). In `nutzer-alle` steht er als `acc`.
Auf dem Server liegen ihre Daten unter `lernzentrale:<benutzername>` mit geräteunabhängigen Schlüsseln: `profile`, `app:W|Z|E|D`, `lzp:…`, `plan:…`, `arena`, `groups`, `story`, `erg`, `g:<geister-duell>`.
Beim ersten Anmelden auf einem Gerät gewinnt der Server, bei App-Ständen der höhere Punktestand; danach gilt der neuere Stand.
Später: E-Mail + Passwort (Supabase Auth) wird einmal einem Benutzernamen zugeordnet – die Schlüssel bleiben gleich.
Lerngruppen-Codes stehen nie im Code.

## Versionen
`Umbau.Funktion.Korrektur` – erste Stelle nur bei großen, für Benutzer spürbaren Umbauten; zweite bei neuen Funktionen oder Umbauten im Hintergrund; dritte bei kleinen Korrekturen. Bei jedem Update: Versionsnummer in `index.html`, `js/news.js` und `sw.js` (`VER`) sowie `?v=` in den Verweisen anheben.
