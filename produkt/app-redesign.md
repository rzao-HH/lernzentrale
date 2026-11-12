# App-Redesign: Konzept und erste Entwürfe

Stand: 12.11.2026 · in Arbeit · Favorit bisher: **Richtung B (Lernwelt)**: leicht spielerisch (Sprechblase, Krabbi hat eine Rolle), klare Linien, gut gruppiert und abgegrenzt.

**Warum:** Die App ist historisch gewachsen. Jede Lernwelt sieht anders aus, die Startseite ist voll, vieles ist Text, und es gibt keinen eigenen Stil. Bevor neue Funktionen kommen (siehe `funktionen.html`, Teil B), soll die App aufgeräumt, schnell verständlich, zugänglich und auf ein professionelles Niveau gebracht werden. Danach werden Produktseite und Videos mit den neuen Bildschirmen neu gemacht. Inhalt und Aufbau der Produktseite bleiben (`produktseite.md`).

**Entwürfe:** eigene Design-Arbeitsfläche „App-Redesign Lernzentrale“ (getrennt von der Produktseite), Link: https://claude.ai/artifact/4dGcpa3J5DwZv9Be49Upyj (privat, nur für die Besitzerin sichtbar, bis sie geteilt wird). Kopie der Quellen in `produkt/quellen/redesign/`.

## Was heute stört (Bestandsaufnahme)

- **Jede Lernwelt ist eine eigene App:** eigene Schrift (z. B. Schreibmaschine im Detektiv-Büro), eigene Kopfleiste, eigener Aufbau. Man muss jedes Fach neu lernen.
- **Startseite überladen:** Anmeldung, Personenwahl, Lernplan, „Heute lohnt sich“, vier App-Karten mit je zwei Knöpfen, Arena, Lerngruppen, Rangliste, Neuigkeiten. Es ist nicht klar, was man jetzt tun soll.
- **Kopfleiste nur aus Emojis** (🏠 ⚔️ 📄 🙂 🗓️ 🔊), ohne Beschriftung; auf schmalen Geräten rutscht sie aus dem Bild.
- **Erst Pakete ankreuzen, dann Modus wählen:** zwei getrennte Schritte, und viele Modi stehen gleichberechtigt nebeneinander (8–10 pro Fach).
- **Paketkarten voller Text:** Lernziel, Buchseite, „Fortschritt: 0 von 16 Treffern (aus den letzten 20 Aufgaben)“, „Volle Punkte – neu“.
- **Einstellungen mittendrin** (Leicht/Profi, Rekorde, Zurücksetzen) zwischen den Lerninhalten.

## Grundsätze für die neue App

Aus der Recherche (Nielsen Norman Group zu Kindern 3–12, Analysen von Duolingo und Khan Academy Kids) und aus der Bestandsaufnahme:

1. **Eine App, ein Stil.** Alle Fächer nutzen dieselben Bausteine. Ein Fach erkennt man an Farbe, Name und Bild, nicht an anderer Bedienung.
2. **Immer klar, was als Nächstes dran ist.** Die Startseite heißt „Heute“ und zeigt eine große Karte „Als Nächstes“ (aus Lernplan und „lohnt sich“), dazu den Countdown zur Arbeit. Duolingo hat aus demselben Grund auf einen einzigen Weg umgestellt.
3. **Flache Navigation.** Unten vier Reiter: Heute · Fächer · Gemeinsam · Ich. Höchstens drei Ebenen bis zur Übung (Fach → Paket → Übung).
4. **Eine Aufgabe pro Bildschirm.** In der Übung keine Leisten, nur Fortschritt, Aufgabe, große Antworten, Rückmeldung.
5. **Große Tippflächen** (mindestens 56–64 px hoch), Text mindestens 16–17 px, gute Kontraste (WCAG AA). Farbe nie als einziges Signal (immer auch Wort oder Häkchen).
6. **Symbole statt Emojis:** eine Liniensymbol-Familie mit Beschriftung.
7. **Fortschritt als Bild** (Balken, Ring, Weg) und ein Wort („neu“, „noch üben“, „sicher“) statt Zahlenkolonnen. Zahlen nur auf Nachfrage.
8. **Module nach Zweck sortiert** statt als lange Liste: Verstehen · Üben · Erleben · Testen, eins davon „empfohlen“.
9. **Nicht kindisch.** Die Zielgruppe ist etwa 9–13. Freundlich, aber erwachsen genug (Tweens empfinden Kleinkind-Optik als peinlich).
10. **Krabbi bleibt** als Begleiter: für Tipps, Lob, „Als Nächstes“. Wie präsent, hängt von der Richtung ab.

## Begriffe

- Stufen eines Pakets: **neu · noch üben · sicher**.
- Nicht verwenden: „wackelt“, „wackelig“, „noch nicht sitzt“ (wirkt abwertend bzw. unklar). Die heutige App sagt an einer Stelle „Volle Punkte – noch wackelig“ (Startseite, „Heute lohnt sich besonders“); beim Umbau ändern.

## Neuer Aufbau (in allen Entwürfen gleich)

- **Heute:** Begrüßung, Countdown zur nächsten Arbeit mit Lernplan-Fortschritt, Karte „Als Nächstes“ mit einem Knopf, „Heute im Plan“ (3 Punkte, abhakbar).
- **Fächer:** vier Kacheln (Fach, Lernwelt, Fortschritt). Darunter später „Neues Lernmaterial hinzufügen“ (Foto → Pakete, kommt bald).
- **Fach:** Name, Rang, Pakete der Reihe nach mit Status (sicher / noch üben / neu), am Ende der Abschlusstest.
- **Paket:** Lernziel, Buchseite, Fortschritt, Module in vier Gruppen (Verstehen, Üben, Erleben, Testen), eins empfohlen.
- **Übung:** Schließen, Fortschritt, Aufgabe, große Antworten, Rückmeldung mit Erklärung, „Weiter“.
- **Ergebnis:** Lob, „9 von 10“, Punkte, was das für das Paket heißt, „Noch eine Runde“ / „Weiter im Plan“.
- **Gemeinsam:** Lerngruppen als Reiter, Rangliste, Duell.
- **Ich:** Lernplan, Ränge und Abzeichen, Einstellungen (Ton, Schriftgröße, hell/dunkel), Geräte verbinden, **Für Eltern** (mit Code gesperrt).

Die Spielwelten (Küsten-Crew, Detektiv-Büro …) bleiben als Name, Bild und Rang erhalten, aber nicht mehr als eigener Bedienstil.

## Drei Stilrichtungen (zum Auswählen oder Mischen)

| | A · Klar | B · Lernwelt | C · Studio |
|---|---|---|---|
| Gefühl | ruhig, aufgeräumt, viel Weißraum | warm, verspielt, Abenteuer | modern, dunkel, für Große |
| Schrift | Lexend (für flüssiges Lesen entwickelt) | Baloo 2 + Nunito | Space Grotesk + Inter |
| Farben | hellgrauer Grund, 4 Fachfarben gedämpft | Sandgrund, kräftige Farben, schwarze Umrisse wie Aufkleber | fast schwarz, Neon-Limette als Aktion, helle Fassung dazu |
| Fach-Ansicht | Liste der Pakete | Weg mit Stationen (wie eine Karte), Krabbi läuft mit | Kacheln mit Fortschrittsringen |
| Krabbi | klein, bei Lob | groß, spricht in Sprechblasen | nur bei Lob und Tipps |
| Passt gut für | breite Zielgruppe, Eltern, Lesbarkeit | Klasse 4–6, Spielspaß | Klasse 6–8, „nicht kindisch“ |
| Risiko | wirkt evtl. zu nüchtern | wirkt ab Klasse 7 evtl. zu kindlich | dunkel ist abends gut, tagsüber Geschmackssache |

Denkbar ist auch eine Mischung, z. B. Aufbau und Lesbarkeit von A, Weg-Ansicht der Fächer aus B, Zahlen-Kacheln aus C. Eine Hell/Dunkel-Umschaltung kann jede Richtung bekommen.

## Wichtig: So wird gelernt (Lernmodell, muss die Führung tragen)

Ein Paket hat **keine eigene Lernstrecke**. Module gelten für die **gewählte Auswahl an Paketen**, nicht für ein einzelnes Paket:
- Ein **neues Paket lernt man zuerst allein**.
- Danach **nimmt man es zu den Paketen dazu, die schon sitzen**, und übt alles **gemischt** (so bleibt Altes frisch, und die Aufgaben kommen wie in der Arbeit durcheinander).
- Manche Module gehen nur mit bestimmten Paketen (Winkel-Akademie: Messen, Winkelart, Schätzen, Zeichnen, Zeitrunde nur mit Paketen 1–4; Aufgaben-Mission nur mit 5–8; Test mit jeder Auswahl). Die Oberfläche muss zeigen, **warum** ein Modul gerade nicht geht.

Heute geschieht das mit „Pakete ankreuzen, dann Modus wählen“. Das ist richtig gedacht, aber nicht erklärt.

## Grundablauf neu: erst „Was?“, dann „Wie?“ (Klick-Dummy 2, Stil B)

Rückmeldung zu den ersten Dummies (A, B, C) und zum festen Weg in D: Wer erst ein Paket wählt und dann dessen Module bekommt, sieht nicht, dass dieselben Module für mehrere Pakete gelten, kann nicht mehrere Pakete zusammen lernen und hat in D sogar einen festen Weg statt freier Wahl. Deshalb gilt ab jetzt dieser Grundablauf auf der Fach-Seite:

1. **Was übst du?** Pakete antippen: eins allein oder mehrere zusammen. Schnellwahl: „Neu: nur Paket 3“, „Alles, was ich kann“, „Neues + Bekanntes“.
2. Ein Band zeigt die Auswahl in Worten: „Du übst: Paket 1 + 2 + 3 gemischt“.
3. **Wie übst du?** Alle Module frei wählbar. Jedes Modul zeigt, **aus welchen der gewählten Pakete** es Aufgaben nimmt („aus Paket 1 und 2“). Passt ein Modul zu keinem gewählten Paket, ist es ausgegraut mit Grund („nur mit Paket 5–8“).
4. In der Übung steht oben „Winkelart erkennen · Paket 1 + 2 + 3 gemischt“, und an jeder Aufgabe, **aus welchem Paket sie kommt**.
5. Das Ergebnis zeigt **pro Paket**, wie es lief. So sieht man, welches Paket man noch üben sollte.

Krabbi erklärt je nach Auswahl in einem Satz, was das bedeutet (allein = kennenlernen, gemischt = wie in der Arbeit, Altes bleibt frisch). Vorschläge (Konzept 2), Plan (4) und Weg (D) können darauf aufbauen, indem sie eine Auswahl plus ein Modul vorschlagen, statt den Weg festzulegen.

## Startseite je Fach: fünf Konzepte (Stil B, auf der Arbeitsfläche, alle klickbar)

1. **Weg mit Schritten** (Pakete als Akkordeon, jedes mit Verstehen → Üben → Erleben → Prüfen). **Verworfen** in dieser Form: Es tut so, als hätte jedes Paket eine eigene Strecke, Module kämen mehrfach vor, und Mischen ginge nicht.
2. **Krabbi schlägt vor:** oben ein einziger Vorschlag mit „Warum das?“, darunter vier zugeklappte Schubladen (Neues lernen, Noch üben, Spielen und ausprobieren, Testen).
3. **Was willst du heute?** Vier große Türen nach Absicht, darunter erscheint nur das Passende.
4. **Plan bis zur Arbeit:** Wenn eine Arbeit eingetragen ist, ist der Lernplan die Startseite (Tag für Tag, heute aufgeklappt, Probearbeit, Arbeit).
5. **Lernrucksack:** zeigt das Lernmodell direkt. Oben steht, was gerade „im Rucksack“ ist (ein Paket allein oder mehrere gemischt), mit „Allein lernen“ für das neue Paket und „Alles, was ich kann“. Darunter die Module, die für diese Mischung gelten; nicht passende sind ausgegraut mit Grund („braucht Paket 1–4“).

Die Konzepte lassen sich kombinieren, z. B. Vorschlag oben (2) + Rucksack darunter (5), oder Plan (4), wenn eine Arbeit ansteht, sonst Weg (D).

## Navigation: von heute nach neu

Oben im Fach nur noch: zurück, Fachname, Rang. Unten vier Reiter (Heute, Welten, Gemeinsam, Ich). Haus → Reiter Heute; Schwerter/Arena → Gemeinsam und beim Testen; Lernzettel → beim Verstehen bzw. am Abschnitt; Person wechseln, Ton, Leicht/Profi, Rekorde, Zurücksetzen, Neuigkeiten → Ich; Lernplan → Heute und Fach-Start (Konzept 4); Checkliste und Elternübersicht → Ich › Für Eltern; Pakete ankreuzen → Rucksack bzw. automatisch auf dem Weg.

## Entwurf D: ein Weg mit Misch-Stationen (Prinzipien großer Sprach-Apps)

Angelehnt an den Aufbau großer Sprach-Apps (Duolingo), **ohne deren Gestaltung zu kopieren**: Die Startseite ist der Weg. Abschnitte mit farbigem Band und Lernzettel; runde Stationen mit „Tastenkante“; Infos erst beim Antippen; eine Aufgabe pro Bildschirm; „Prüfen“, dann Rückmeldung als Streifen von unten; Ergebnis mit drei Kacheln.
**Passt zum Lernmodell:** Auf dem Weg wechseln sich neue Pakete (allein) und **Misch-Stationen** (alle bisherigen Pakete zusammen) ab, am Ende ein Abschnittstest. Beispiel Winkel: Paket 1 → Paket 2 → Mischen 1+2 → Paket 3 → Mischen 1–3 → Paket 4 → Mischen 1–4 → Abschnittstest; dann Abschnitt 2 (Pakete 5–8).
**Bewusst anders als dort:** keine Leben, kein Sperren nach Fehlern, Serie ohne Druck, Krabbi statt Eule, eigene Farben; jede Station lässt sich trotzdem antippen („Trotzdem ausprobieren“), freies Üben bleibt möglich.
**Abgeglichen mit echten Bildschirmen:** Die offiziellen App-Store-Bilder von Duolingo und Khan Academy Kids (apps.apple.com, in der Umgebung „lernzentrale“ freigegeben) zeigen die Übungsbildschirme: weißer Grund, dünner runder Fortschrittsbalken mit „… in Folge“ darüber, oben eine Anweisung, große Bild- oder Wortkacheln (gewählt = hellblau), eine Figur stellt die Frage mit Sprechblase, unten ein hellgrüner Streifen „Sehr gut!“ mit breitem „Weiter“. Entwurf D folgt dem; ergänzt wurden „3 richtig in Folge“ über dem Balken und Krabbi, der die Frage in einer Sprechblase stellt. Den Lernweg selbst zeigen die Store-Bilder nicht.
**Stilvorbilder der Konkurrenzanalyse:** Die Session „Konkurrenzanalyse Lern-Apps“ hat 130 Aufnahmen der Webseiten von StudySmarter, Duolingo, Prodigy, Knowunity, Khanmigo und Photomath gemacht (Artefakt „Stilvorbilder“, https://claude.ai/artifact/XoV1Vka1YbEpkVBV5C7xoP#galerie). Das sind Werbeseiten, keine App-Bildschirme; brauchbar für Farben, Schrift und Tasten, nicht für Aufbau. Echte App-Bildschirme: App-Store-/Play-Einträge oder eigene Screenshots vom Handy.

## Themen: Grunddesign + Themenhaut (Themen-Baukasten auf der Arbeitsfläche)

Jede Welt folgt einem Thema, und das soll man auch sehen, ohne dass Bedienung und Aufbau sich ändern. Deshalb gibt es **ein Grunddesign** (Aufbau, Schrift, Knöpfe mit Umriss, Krabbi, Tab-Leiste) und darüber **eine Themenhaut** aus festen Bausteinen:

| Baustein | Weltraum (Mathe) | Zauberschule (NWT) | Küste (Englisch) | Detektiv-Büro (Deutsch) | Eigenes, z. B. Dinos (KI) |
|---|---|---|---|---|---|
| Hintergrund | heller Sternenhimmel | Türkis mit Blasen | Sand mit Wellenlinien | Papier mit Linien | Hügel und Farn |
| Farben | Blau + Sternengelb | Türkis + Zauberlila | Koralle + Himmelblau | Braun + Gelb | Grün + Gelb |
| Form der Pakete | Sterne | Tropfen | Rettungsringe | Lupen | Dino-Eier |
| Krabbi trägt | Antennen mit Sternen | Zaubermütze | Kapitänsmütze | Detektivhut | Dino-Kapuze |
| Fliegt ab und zu vorbei | Sternschnuppe | Seifenblasen | Möwe | Fußspuren | Flugsaurier |
| Ränge (mit Symbol) | Sternenstaub … Galaxis-Legende | Funke … Elementar-Meisterschaft | Schiffsjunge … Admiral | Praktikant … Meisterdetektiv | Dino-Ei … Dino-Legende |
| Wörter | Mission, Landung | Zauber, Kessel | an Bord, Hafen | Akte, Fall | Ei, Nest, Expedition |

Effekte bleiben im Hintergrund (langsam, blass, abschaltbar, bei „weniger Bewegung“ aus). Weil ein Thema nur diese Liste ist, kann später die KI ein **eigenes Thema** eines Kindes füllen, ohne die App zu ändern.

**Punkte und Ränge** gehören sichtbar dazu: oben im Fach Rang-Symbol, Rangname, Punkte und Balken „noch 220 bis Planet“; an jedem Modul eine Münze „volle Punkte“ (neu oder noch üben), „+20 % Bonus“ (lange nicht geübt) oder „wenige Punkte“ (sicher, noch nicht wieder fällig), mit kurzem Grund.

## Funktions-Check (auf der Arbeitsfläche)

Alle heutigen Funktionen haben einen Platz im neuen Aufbau. In den Klick-Dummies **noch nicht gezeigt**: Lernkarten-Suche, Schwierigkeitsstufen im Modul, Fotos der Arbeitsblätter, Schreibtest und Probearbeit drucken, Selbsteinschätzung und Checkliste, Lernverlauf und Fehlerarten, Person wechseln, Neuigkeiten und Offline-Hinweis. **Nur angedeutet**: Wissen/Lernzettel, Experimente und Szenen, Wiederholung nach Tagen, „Heute lohnt sich“, Arena mit Geister-Duell, Power-ups und Glücksrad, Elternübersicht, Geräte verbinden.

## Nächste Schritte

1. Fach-Startseite entscheiden (Konzepte 2–5 und Entwurf D vergleichen, Robin anklicken lassen), dann Stil festlegen (Favorit B, ggf. mit der Weg-Logik aus D).
2. Daraus ein kleines Designsystem: Farben, Schrift, Abstände, Bausteine (Knöpfe, Karten, Antworten, Reiter, Statuschips, Fortschritt), Symbolsatz, Krabbi-Posen.
3. Weitere Bildschirme entwerfen: Lernplan, Elternbereich, Wissen lesen, Geodreieck/Experimente im neuen Rahmen, Duell, Anmeldung und erster Start, Handy-Querformat und Telefonformat.
4. Umbau der App Schritt für Schritt: erst gemeinsamer Rahmen (Reiter, Heute, Fächer, Paket), dann die Übungen je Fach.
5. Danach Produktseite und Videos mit den neuen Bildschirmen neu aufnehmen.

## Quellen der Recherche

- Nielsen Norman Group: Physical Development and UX for children (https://www.nngroup.com/articles/children-ux-physical-development/), Kids' cognition (https://www.nngroup.com/articles/kids-cognition/)
- Duolingo, neuer Lernweg auf der Startseite: UX-Analysen (https://uxplanet.org/analyzing-duolingo-from-product-design-perspective-after-400-days-of-non-stop-practice-c4d4809bdb37, https://medium.com/usabilitygeek/ux-case-study-duolingo-ade986ec7450)
- Khan Academy Kids, Lernweg mit Figuren: https://screenwiseapp.com/guides/khan-academy-kids-learning-game
- Gestaltung für 9–12-Jährige (Praxisartikel): https://gapsystudio.com/blog/ux-design-for-kids, https://uxdesign.cc/children-first-802bd12fe28c
- Dribbble ließ sich aus der Sitzung nicht automatisch ansehen (die Seite blockiert automatische Browser). Beispielbilder von dort am besten selbst sammeln und als Bilder in den Chat legen.
