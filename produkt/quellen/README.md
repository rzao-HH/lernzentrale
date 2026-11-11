# Quellen der Produktseite und des Erklärvideos

Sicherung von allem, was sonst nur in einer Claude-Session oder auf dem Design-Canvas liegt (Stand: 11.11.2026, Video Version 1).

- `canvas/` – Kopie der Canvas-Dateien (Claude Design, Format `.dc.html`): ganze Seite (`Seite.dc.html`), Stil B (`Main.dc.html`), gewählter Einstieg 7, `canvas.json`. Bilder verweisen auf `/_blob/…` im Canvas. Impressum und Datenschutz liegen nur auf dem Canvas (Namen und Anschrift nicht im Repository).
- `bewegtbilder/` – alle animierten Szenen als WebP (600×800), so wie sie auf der Seite laufen. `duell.webp` und `creator.webp` sind nachgebaut, die übrigen echte Aufnahmen der App (außer `klasse.webp`, nachgebaut).
- `video/` – Erklärvideo: `video.html` (alle Szenen, `render(t)`), nachgebaute Animationen (`klasse.html`, `duell.html`, `creator.html`, `rang.html` = alte Rangliste, nicht mehr benutzt), `render.py` (Bilder rendern, 25 fps, 1920×1080) und `rec_*.py` (Animation → WebP). Die Einzelbilder (`fr/`) werden aus den WebPs erzeugt und sind nicht gesichert. Pfade in den Skripten zeigen auf das Arbeitsverzeichnis der Session und müssen angepasst werden.
- `aufnahme/` – Skripte, mit denen die echten App-Szenen per Playwright aufgenommen wurden (Fingerpunkt, Tippen, Ziehen).

Das fertige Video liegt in `produkt/lernzentrale-erklaervideo.mp4`.
