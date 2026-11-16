# Entwurf G: Usability, Lenkung und Punkte

Stand: 16.11.2026 · Konzept und Klick-Dummy · Arbeitsfläche „App-Redesign Lernzentrale“, Reihe „G · Usability, Lenkung und Punkte“ (https://claude.ai/artifact/4dGcpa3J5DwZv9Be49Upyj), Quellen in `produkt/quellen/redesign-g/`.

**Kurz:** Ein Paket wird nicht durch Punkte „sicher“, sondern durch **drei Haken: Kennen · Können · Behalten**. Jeder Haken ist ein Lernprinzip (wiedererkennen, selbst abrufen, später gemischt behalten). Punkte richten sich danach, **wie viel man selbst denkt**: Antippen bringt 4, Selbst machen 10 Punkte je richtiger Antwort, Raten bringt nichts. Das Kind wählt frei, aber aus **drei guten Vorschlägen** von Krabbi, ein großer „Los“-Knopf startet den besten. „Selbst zusammenstellen“ bleibt offen, nichts ist gesperrt. Eltern stellen ein, wie viel Freiheit es gibt (frei · ausgewogen · geführt).

---

## 1. Ausgangslage: Warum die freie Wahl zum Bequemen geführt hat

Aus dem Code der heutigen App (`js/lernstand.js`, `apps/winkel.html`):

1. **Alle Aufgabenarten zählen gleich.** In der Winkel-Akademie bringt jede richtige Antwort 10 Punkte, egal ob man eine Winkelart antippt (eine von vier) oder einen Winkel selbst misst (Zeile 1415). Antippen ist viel weniger Arbeit, also lohnt es sich mehr.
2. **Raten wird belohnt.** Bei vier Antworten trifft man durch Zufall jede vierte. Es gibt keine Bremse für schnelles Tippen.
3. **„Sicher“ geht ohne Selbstmachen.** Die Stufe steigt bei 80 % richtig in jedem Modul, also auch im Quiz. Ein Paket kann so als sicher gelten, ohne dass das Kind es je selbst gemessen, geschrieben oder gezeichnet hat. Wiedererkennen ist aber deutlich leichter als Abrufen (siehe Abschnitt 4).
4. **Der Tagesdeckel gilt je Paket.** Wer zum nächsten Paket wechselt, bekommt wieder volle Punkte.
5. **Die Wahl ist ungelenkt.** 8–10 Module stehen gleichberechtigt nebeneinander. Was etwas bringt und was nicht, sieht man erst hinterher, wenn überhaupt.

Die heutige Punkte-Logik (volle Punkte für Neues und Noch-Üben, wenig für Sicheres, +20 % für lange nicht Geübtes, Tagesdeckel) ist richtig gedacht und bleibt erhalten. Es fehlt, **was** man tut (Aufgabenart) und **wie** man es tut (in Ruhe oder geraten).

## 2. Was an den Entwürfen A–F trägt und was nicht

| Entwurf | Trägt | Trägt nicht |
|---|---|---|
| **A · Klar** | Flache Navigation mit vier Reitern, höchstens drei Ebenen bis zur Übung, gute Lesbarkeit. | Zu nüchtern für 9–11-Jährige; Paket → feste Module. |
| **B · Lernwelt** | Der Stil: Umrisse wie Aufkleber, Tasten mit Kante, Krabbi spricht in Sprechblasen und hat eine Rolle, klar gruppiert. Fach-Konzept 2 („Krabbi schlägt vor“ mit „Warum das?“) und 5 (Lernrucksack: Mischung sichtbar). | Paket wählen, dann dessen Module: Mischen nicht sichtbar. |
| **C · Studio** | Zahlen-Kacheln für Größere. | Dunkel und kühl, passt nicht zur Mehrheit der Zielgruppe. |
| **D / D2 · Weg** | Immer klar, was dran ist (ein Startpunkt, Ring und START). Fertige Stationen in Gold. Misch-Stationen mehrfarbig. Keine Leben, keine Strafen. | Ein langer, fest vorgegebener Weg passt schlecht zu verteilter Wiederholung (Lernen ist ein Kreislauf, keine Linie) und wird bei 20+ Paketen endlos. Popups zeigten zu wenig. Freies Üben war ein Anhängsel. |
| **E · Flugkarte** | Bühne und Papier (Thema hinten, Lesbares auf hellen Karten), Herkunft jeder Aufgabe („Paket 3 · neu dabei“), Mischung als Balken, „antippen, dann prüfen“, Tempo-Bremse, Tagesdosis, „Noch nicht ganz“ ohne Rot. | Spuren tragen nicht bei vielen Paketen. Neue Wörter („nachleuchten“) muss man lernen. |
| **F · Regal und Treppe** | Regal mit Gruppen zum Aufklappen (skaliert auf 24 Pakete), Krabbis Vorschlag ist beim Öffnen vorgewählt, „Punkte schalten nichts frei“, Ergebnis je Paket. | Zwei Ebenen auf einmal (Paketstand und Lernform-Stufen) sind schwer zu durchschauen. Viele Schlösser wirken wie Verbote und widersprechen der freien Wahl. |

**G übernimmt:** Stil B mit der Optik von E (Bühne + Papier), Krabbi mit Rolle; aus D2 „ein klarer nächster Schritt“; aus E Herkunft, Mischbalken, Tempo-Bremse, keine Strafen; aus F das gruppierte Regal und den vorgewählten Vorschlag.
**G ist neu:** die drei Haken statt abstrakter Stufen und Schlösser; Punkte nach Anspruch; drei Vorschläge statt eines festen Wegs; Ergebnis mit verständlicher Punkterechnung; Lenkungsregler für Eltern; Neugier-Bremse gegen das Paket-Hüpfen.

## 3. Das Lernmodell in einem Bild: drei Haken je Paket

| Haken | Bedeutung für das Kind | Wie man ihn bekommt | Lernprinzip |
|---|---|---|---|
| **Kennen** (Auge) | „Ich erkenne es, wenn ich es sehe.“ | Eine Runde mit mindestens 80 % richtig, in Ruhe beantwortet, egal welche Aufgabenart. Meist nach „Wissen lesen“ und Antippen. | Erster Kontakt, Erfolgserlebnis, Wiedererkennen |
| **Können** (Stift) | „Ich kann es selbst.“ | Eine Runde mit **Selbst-machen-Aufgaben** aus diesem Paket (messen, zeichnen, schreiben, rechnen, Lücke tippen) mit mindestens 80 %, mindestens 4 Aufgaben aus dem Paket. | Abrufen statt Wiedererkennen, Erzeugungseffekt |
| **Behalten** (Kreispfeil) | „Ich kann es auch später, wenn es durcheinanderkommt.“ | **An einem späteren Tag** als „Können“, **gemischt** mit mindestens einem anderen Paket (oder im Test), mindestens 80 % in den Selbst-machen-Aufgaben dieses Pakets. | Verteilte Wiederholung, Vermischen |

- **Begriffe:** kein Haken = **neu**, ein oder zwei Haken = **noch üben**, drei Haken = **sicher**.
- **Am Paket:** ein Ring aus drei Teilen um die Paketmarke (Thema Weltraum: ein Planet). Leer und gestrichelt = neu. Jeder Haken füllt ein Drittel. Darunter steht immer das Wort, Farbe ist nie das einzige Signal.
- **Wieder dran:** Ein sicheres Paket wird nach 2, 4, 8, 16 Tagen wieder fällig (Uhr-Marke „wieder dran“). Klappt das Auffrischen (mindestens 80 %), wird der Abstand länger und der Ring bekommt einen kleinen Stern. Klappt es gar nicht (unter 50 %), wird der Behalten-Haken gestrichelt und das Paket heißt wieder „noch üben“, bis eine gute Misch-Runde gelingt. Kennen und Können bleiben.
- **Passt zur heutigen Technik:** Stufe 0 = neu, 1 = Kennen, 2 = Können, 3 = Behalten (sicher), 4–5 = aufgefrischt. Intervalle 1/2/4/8/16 Tage bleiben. Neu ist nur: `applyRound` bekommt die Aufgabenart und ob gemischt wurde, und Stufe 2 und 3 verlangen die passende Art.
- **Wenige oder viele Pakete:** Gibt es in einem Fach nur ein Paket, zählt für „Behalten“ eine Runde mit gemischten Aufgabenarten an einem späteren Tag.
- **Wissen und Lernkarten bleiben immer offen** (Grundsatz aus `funktionen.html`). Sie bringen keine Punkte pro Karte, aber der kurze Check danach zählt.

## 4. Lernforschung und was daraus in der Bedienung wird

| Befund | Bedienung in G |
|---|---|
| **Abrufüben** (Testing-Effekt, z. B. Roediger & Karpicke 2006): Etwas aus dem Kopf holen festigt mehr als wieder lesen. **Erzeugungseffekt** (Slamecka & Graf 1978): Selbst Erzeugtes bleibt besser als Ausgewähltes. | Selbst-machen-Aufgaben bringen 10 statt 4 Punkte und sind Pflicht für „Können“. Lernkarten durchblättern bringt nichts, der Check danach schon. |
| **Verteilte Wiederholung** (z. B. Cepeda u. a. 2006): Abstände zwischen Lerntagen verbessern das Behalten. | „Behalten“ geht erst an einem späteren Tag. „Wieder dran“-Marke, volle Punkte, +20 % bei lange nicht Geübtem. Sicheres bringt wenig, bis es wieder dran ist. |
| **Vermischen** (z. B. Rohrer & Taylor 2007, Mathe): Gemischte Aufgaben lehren, die richtige Methode zu erkennen. Lernende halten Blocken trotzdem für besser (Kornell & Bjork 2008). | Misch-Bonus ×1,2. Krabbi schlägt Mischungen vor und erklärt sie („wie in der Arbeit“). Jede Aufgabe zeigt, aus welchem Paket sie kommt, der Fortschrittsbalken zeigt die Paketfarben. |
| **Erwünschte Schwierigkeiten** (Bjork 1994): Was sich schwerer anfühlt, bleibt oft besser. Kinder wählen trotzdem das Leichte. | Das Schwierigere wird nicht verordnet, sondern lohnt sich sichtbar. „Noch nicht ganz“ ist orange und freundlich, nie rot, mit Tipp und zweitem Versuch. |
| **Mastery-Lernen** (Bloom): Weiter erst, wenn das Ziel weitgehend erreicht ist (etwa 80 %), aber mit neuen Wegen statt Wiederholung des Gleichen. | 80 % je Haken. Neugier-Bremse: Höchstens zwei Pakete gleichzeitig nur mit „Kennen“. Bei Misserfolg schlägt Krabbi eine andere Lernform vor, nichts wird gesperrt. |
| **Selbstbestimmungstheorie** (Deci & Ryan): Autonomie, Kompetenz, Zugehörigkeit. Wahl motiviert am meisten bei wenigen sinnvollen Möglichkeiten (Patall u. a. 2008). Erwartete, kontrollierende Belohnungen können die eigene Lust verdrängen (Deci, Koestner & Ryan 1999), Rückmeldung über Können stärkt sie. | **Autonomie:** drei Vorschläge zur Wahl plus freies Zusammenstellen, Aufhören ist ausdrücklich erlaubt. **Kompetenz:** Haken zeigen echtes Können, das Ergebnis sagt in Worten, was neu gelungen ist („Du kannst Überstumpf jetzt selbst messen“). Punkte sind Rückmeldung, kein Lohn für Gehorsam. **Zugehörigkeit:** Krabbi als Begleiter, Lerngruppe mit gemeinsamem Wochenziel aus Haken (nicht aus Punkten). |

## 5. Der Weg des Kindes durch die App

```
App öffnen → Heute → [Los] → Übung → Ergebnis → Weiter (Vorschlag) | Andere Wahl | Für heute aufhören
                 ↘ Fach → 3 Vorschläge → Vorschau → Übung …
                          ↘ Pakete (Regal) → Paket-Blatt → Wissen lesen | Starten
                          ↘ Selbst zusammenstellen → Was? → Wie? → Starten
```

| Bildschirm | Frage des Kindes | Was es sofort sehen muss (ohne Erklärung) | Eine Hauptaktion |
|---|---|---|---|
| **Heute** | „Was soll ich jetzt machen?“ | Gruß mit Name, Rang-Symbol und Punkten. **Tagesziel** als drei Sterne („heute 3 Runden, etwa 15 Minuten“). **Ein großer Knopf** mit dem besten Vorschlag in Worten („Überstumpf selbst messen“). Countdown zur Arbeit, falls eingetragen. Je Fach eine Zeile, was dort dran ist. | **Los** (startet direkt die Übung) |
| **Fach** | „Was kann ich hier machen, und wie weit bin ich?“ | Rang und Punkte des Fachs. **Krabbi: „Such dir eins aus“** mit drei Karten (Was, Wie, Haken-Ziel, Punkte). Darunter das **Regal** mit allen Paketen in Gruppen, jedes mit Haken-Ring und Wort. Unten „Selbst zusammenstellen“. | Eine der drei Karten antippen |
| **Vorschau** (Blatt) | „Was erwartet mich?“ | Was (Paketmarken, Mischung als Balken), Wie (Lernform), wie viele Aufgaben, **warum jetzt**, welcher Haken möglich ist, Punkte je Antwort. | **Starten** |
| **Paket-Blatt** | „Was muss ich hier noch können?“ | Lernziel („Ich kann …“), Quelle im Heft, die drei Haken mit Status und „So bekommst du ihn“. Wissen lesen ist immer da. Lernformen nach Haken gruppiert. | Den nächsten fehlenden Haken üben |
| **Selbst zusammenstellen** | „Ich will selbst bestimmen.“ | Erst **Was?** (Paketmarken antippen, höchstens 6), dann **Wie?**: alle Lernformen offen, jede mit dem Haken, den sie bringen kann, und **Punkten je Antwort für genau diese Auswahl**. Passt eine Lernform nicht, steht der Grund dabei („nur mit Paket 5–8“). | **Starten** |
| **Übung** | „Was soll ich tun, wie weit bin ich?“ | Oben: Schließen, Lernform und Herkunft („Paket 3 · Überstumpf · noch üben“). Fortschritt als **10 Punkte in Paketfarben** (Mischen wird sichtbar). Eine Aufgabe, große Antwortflächen, Zahlentasten zum Selbstmachen. | Antworten → **Prüfen** |
| **Rückmeldung** | „Hatte ich recht, und warum?“ | Richtig: grün, Häkchen, ein Satz Erklärung, „+10 · selbst gemessen“. Noch nicht ganz: orange, Tipp, zweiter Versuch (halbe Punkte). Zu schnell: „Richtig, aber sehr schnell getippt. Lies erst die Frage, dann gibt es Punkte.“ | **Weiter** |
| **Ergebnis** | „Was hat es gebracht?“ | „9 von 10“, **je Paket** ein Satz und der Haken-Ring (neu gewonnener Haken leuchtet). **Punkterechnung in Zeilen**, die man versteht. Tagesziel „2 von 3 Runden“. | **Weiter: nächster Vorschlag**, daneben „Andere Wahl“ und „Für heute aufhören“ |
| **Tagesziel geschafft** | „Darf ich aufhören?“ | „Geschafft für heute.“ Was heute neu gelungen ist. Aufhören ist der Hauptknopf, „Noch eine Runde“ steht daneben. Keine Serie, die reißt, keine Drohung. | **Für heute fertig** |

**Gestaltungsregeln für alle Bildschirme:** eine Hauptaktion je Bildschirm (gelber Knopf mit Kante), höchstens drei Wahlkarten auf einmal, Herkunft und Zweck immer in Worten, Tippflächen mindestens 56 px, Farbe nie allein, keine Leben, keine Strafen, keine Werbesprüche. In der Übung keine Reiterleiste.

## 6. Frei, aber gelenkt: fünf Ebenen

1. **Voreinstellung:** Der große „Los“-Knopf startet Krabbis besten Vorschlag. Wer nichts entscheiden will, lernt trotzdem richtig. Der Vorschlag folgt festen Regeln (Abschnitt 8).
2. **Kleine Auswahl:** Drei Vorschläge, alle sinnvoll, bewusst verschieden: meist **weiterkommen** (nächster Haken), **Neues oder Wiederholung** und **etwas Spielerisches**. Drei Karten bleiben drei Karten, ob ein Fach 3 oder 30 Pakete hat.
3. **Volle Freiheit:** „Selbst zusammenstellen“ öffnet alles. Nichts ist gesperrt, aber **jede Lernform sagt vorher ehrlich, welchen Haken sie bringen kann und wie viele Punkte**. Das Bequeme bleibt erlaubt, es lohnt sich nur nicht.
4. **Sanfte Bremsen statt Sperren:** Ratebremse, halbe Punkte fürs Antippen bei Gekonntem, Tagesdeckel, Neugier-Bremse. Nie Abzug, nie Sperre, Lernen ist immer möglich.
5. **Regler für Eltern** (Ich › Für Eltern, mit Code):
   - **Frei:** wie Ausgewogen, aber ohne Neugier-Bremse.
   - **Ausgewogen** (Standard): alles wie beschrieben.
   - **Geführt:** nur Krabbis drei Vorschläge, Wissen und Lernkarten. „Selbst zusammenstellen“ ist aus. Das kommt einem festen Weg nahe, ohne einen zu zeichnen.
   - Dazu: Tagesziel 2, 3 oder 4 Runden. Eltern sehen die Haken, nicht nur Punkte.

So muss die Frage „fester Pfad oder freie Wahl“ nicht für alle Kinder gleich entschieden werden. Für Robin passt anfangs „Geführt“ oder „Ausgewogen“.

## 7. Punktesystem

**Leitsatz für Kinder:** „Punkte gibt es fürs Selberdenken. Raten bringt nichts.“

### 7.1 Grundpunkte je richtiger Antwort (erster Versuch, in Ruhe)

| Aufgabenart | Beispiele | Punkte |
|---|---|---|
| **Antippen** | Quiz, Wahr oder falsch, Winkelart antippen, Gradzahl einordnen, Blitz-Duell mit Auswahl | **4** |
| **Ordnen** | Sortieren, Zuordnen, Puzzle, Sätze bauen, Lücke mit Auswahl | **6** |
| **Selbst machen** | Messen, Zeichnen, Konstruieren, Schätzen (nah dran), Schreiben, Lücke tippen, Rechnen, Schreibtest | **10** |
| **Lesen** | Wissen, Lernzettel, Lernkarten umdrehen | **0**; der Kurz-Check danach zählt nach seiner Aufgabenart |
| **Test mit Note** | Abschlusstest | wie heute: Note 1 = 100, 2 = 80, 3 = 60, 4 = 40, 5 = 20, 6 = 10, mal Paketfaktor |

Ein Spiel zählt nach den Aufgaben darin. **Empfehlung für neue Spiele:** auch Selbst-machen-Aufgaben einbauen (tippen statt antippen), dann zählen sie voll.

### 7.2 Faktoren (werden multipliziert, zusammen höchstens ×1,5; jede richtige Antwort in Ruhe bringt mindestens 1 Punkt)

| Regel | Faktor | Kurzer Grund (so steht er in der App) |
|---|---|---|
| Paket ist neu, noch üben oder wieder dran | ×1 | „volle Punkte“ |
| Lange nicht geübt (mehr als doppelter Abstand) | ×1,2 | „+20 %, lange nicht geübt“ |
| Paket ist sicher und noch nicht wieder dran | ×0,15 | „wenig Punkte, kannst du schon, wieder voll in 3 Tagen“ |
| Antippen bei einem Paket mit Können-Haken | ×0,5 | „Antippen ist für dich jetzt leicht“ |
| Gemischt (mindestens 2 Pakete in der Runde) | ×1,2 | „+20 %, gemischt wie in der Arbeit“ |
| 3. und weitere Runde desselben Pakets am selben Tag | ×0,15 | „heute schon viel geübt, morgen wieder voll“ |
| Neugier-Bremse: schon 2 andere Pakete nur mit „Kennen“ | ×0,5 für das dritte neue Paket | „Mach erst eins davon selbst“ |

### 7.3 Keine oder halbe Punkte

| Fall | Punkte | Wirkung auf die Haken |
|---|---|---|
| Zu schnell geantwortet (Antippen und Ordnen: schneller als die Lesezeit, etwa 1 s + 1 s je 12 Wörter, mindestens 1,5 s; in Zeitrunden 0,8 s) | **0**, Antwort wird trotzdem gezeigt und erklärt | zählt nicht mit. Ab 3 zu schnellen Antworten in einer Runde bringt die Runde keinen Haken. |
| 3 zu schnelle **falsche** Antworten hintereinander | 0 | Krabbi hält kurz an: „Lass uns langsamer machen. Ich lese dir die nächste Frage vor.“ Keine Strafe. |
| Zweiter Versuch nach Tipp, Selbst machen | **halbe** Punkte | zählt als halb richtig |
| Zweiter Versuch, Antippen | **0** | zählt als falsch |
| Fehler am Rundenende richtig wiederholt („Fehler ausbügeln“) | volle Punkte | zählt |

### 7.4 Einmalige Boni

| Bonus | Punkte | Wann |
|---|---|---|
| Kennen-Haken | +20 | einmal je Paket |
| Können-Haken | +30 | einmal je Paket |
| Behalten-Haken, Paket ist sicher | +50 | einmal je Paket (nach einem Rückfall erneut, dann +20) |
| Aufgefrischt (sicheres Paket wieder dran, mindestens 80 %) | +20 | bei jeder Fälligkeit |
| Tagesziel geschafft | +15 | einmal am Tag |

**Nie Abzug:** Gesammelte Punkte bleiben immer. Keine Leben, keine Serie, die reißt.

### 7.5 Beispiele (Winkel-Akademie, Runde mit 10 Aufgaben)

| Situation | Rechnung | Punkte G | heute |
|---|---|---|---|
| Robin klickt wild durchs Quiz zu einem **neuen** Paket: 6 Antworten zu schnell (davon 2 zufällig richtig), 4 in Ruhe, 3 richtig | 3 × 4 | **12**, kein Haken | etwa 50 |
| Quiz zu **sicherem** Paket, nicht wieder dran, 10 richtig | je Antwort 4 × 0,15 × 0,5 = 0,3 → Mindestpunkt 1, also 10 × 1 | **10** | 15 |
| Kennenlern-Runde Paket 4 (neu), erst Wissen lesen, dann 5 Antipp-Fragen, 4 richtig | 4 × 4 + Kennen-Haken 20 | **36** | 40 |
| **Selbst messen**, Paket 3 (noch üben) gemischt mit 1 und 2, 9 von 10 richtig | 9 × 10 × 1,2 + Können-Haken 30 | **138** | 90 |
| Paket 1 ist **lange nicht geübt**, Misch-Runde Zeichnen mit Paket 2, 8 richtig | 8 × 10 × 1,2 × 1,2 = 115 (unter dem Deckel ×1,5) + Aufgefrischt 20 | **135** | 96 |
| **Farmen:** dieselbe Paket-Runde zum 3. Mal am Tag, 10 richtig, Selbst machen | 10 × 10 × 0,15 | **15** | 15 |
| **Paket-Hüpfen:** drittes neues Paket nur angetippt, 10 richtig | 10 × 4 × 0,5 | **20** (Krabbi rät: erst eins selbst machen) | 100 |
| Zweimal „Noch nicht ganz“ beim Messen, im zweiten Versuch richtig | 2 × 5 | **10** statt 20 | – |

**Einordnung:** Ein guter Lerntag mit drei Runden ergibt etwa 150–300 Punkte, also ungefähr so viel wie heute bei ernsthaftem Üben. Bequemes Üben bringt aber nur noch ein Zehntel. Die Rang-Schwellen (100, 250, 500, 850, 1300 …) können bleiben.

### 7.6 Technik (für den Umbau)

- `LS.pts(base, ids)` bekommt zusätzlich `art` (`tippen` | `ordnen` | `selbst` | `test`), `ms` (Antwortzeit) und `versuch`. Grundwert aus `art`, Faktoren wie oben, `LS_CONF` um `GRUND`, `FAKTOR_GEMISCHT`, `FAKTOR_UNTER_STAND`, `LESEZEIT`, `MAX_FAKTOR` ergänzen.
- `LS.answer(id, ok)` bekommt `art`, `schnell`. Die Runde merkt sich Anteil Selbst-machen und Zahl der Pakete.
- `applyRound`: Stufe 0→1 bei 80 % (jede Art), 1→2 nur mit `selbst` und mindestens 4 Aufgaben aus dem Paket, 2→3 nur an einem späteren Tag, gemischt, `selbst` oder Test. Runden mit 3 oder mehr zu schnellen Antworten ändern die Stufe nicht.
- Vorhandene Stufen übernehmen: Stufe 2+ aus Quiz-Runden ist „unbestätigt“. Einmalig auf höchstens 2 setzen, wenn es nie eine Selbst-Runde gab (kein Punktabzug).

## 8. Krabbis Vorschläge: nach welchen Regeln

Die drei Karten werden je Fach aus diesen Regeln gefüllt (die erste ist der „Los“-Vorschlag):

1. **Weiterkommen:** das Paket mit dem nächsten fehlenden Haken, dessen Lernform zuletzt nicht dran war (Perspektivwechsel). Fehlt „Können“, eine Selbst-machen-Lernform, gemischt mit 1–2 sicheren Paketen (etwa 5 : 3 : 2 Aufgaben). Fehlt „Behalten“ und ist ein Tag vergangen, eine Misch-Runde.
2. **Neu oder wieder dran:** Ist ein Paket wieder dran oder lange nicht geübt, dieses. Sonst das nächste neue Paket in der Reihenfolge des Hefts, aber nur, wenn höchstens ein Paket auf „nur Kennen“ steht. Neue Pakete immer **zuerst allein**: Wissen lesen und Kennenlern-Runde.
3. **Spielerisch:** ein Spiel, eine Zeitrunde oder ein Experiment mit den Paketen, die schon „Kennen“ haben, ehrlich mit Punktzahl.

Weitere Regeln: Nie dieselbe Lernform zweimal hintereinander vorschlagen. Steht eine Arbeit an (Lernplan), wird Karte 1 drei Tage vorher zur Misch-Runde über alle Pakete und am Vortag zum Probetest. Klappt eine Runde nicht (unter 50 %), schlägt Krabbi dasselbe Paket in einer **anderen** Lernform vor, nicht dasselbe noch einmal.

## 9. Erklärung für Kinder (so steht es in der App unter „So bekommst du Punkte“)

> **Punkte gibt es fürs Selberdenken.**
> 1. **Je mehr du selbst machst, desto mehr Punkte.** Antippen: 4. Ordnen: 6. Selbst messen, schreiben oder zeichnen: 10.
> 2. **Neues und Wieder-dran bringt volle Punkte.** Was du sicher kannst, bringt wenig, bis es wieder dran ist. Gemischt üben bringt 20 % mehr.
> 3. **Raten bringt nichts.** Wenn du schneller tippst, als man lesen kann, gibt es keine Punkte. Lies die Frage, dann antworte.
>
> **Sicher wird ein Paket mit drei Haken:**
> **Kennen**, du erkennst es. **Können**, du kannst es selbst. **Behalten**, du kannst es auch an einem anderen Tag, wenn es gemischt kommt.
> Für jeden neuen Haken gibt es Extrapunkte. Punkte werden dir nie weggenommen.

## 10. Im Klick-Dummy (Arbeitsfläche, Reihe G)

- **G-App** (klickbar): Heute mit Tagesziel und Los → Übung „Selbst messen“ (Zahlentasten, Prüfen, Rückmeldung, zweiter Versuch mit Tipp) → Ergebnis mit Punkterechnung und neuem Können-Haken → Weiter/Andere Wahl/Aufhören. Fach-Seite mit drei Vorschlägen, Regal mit Haken-Ringen, Paket-Blatt, Vorschau, Selbst zusammenstellen (Punkte je Antwort ändern sich mit der Auswahl). Kennenlern-Runde für ein neues Paket (Wissen-Karte, dann Antippen mit Ratebremse). Blitz-Runde (Spiel, ehrliche niedrige Punkte). „So bekommst du Punkte“, Ich mit Eltern-Regler, Gemeinsam mit Wochenziel aus Haken.
- **G-Punkte** (klickbar): Punkte-Rechner für Kinder: Aufgabenart, Paketstand, gemischt, schnell oder in Ruhe wählen, das Ergebnis erklärt sich in Worten.
- **G-Ablauf:** Weg des Kindes, die drei Haken, die fünf Ebenen der Lenkung auf einer Seite (für Eltern und Planung).

**Tipp zum Ausprobieren:** In der Kennenlern-Runde sehr schnell auf eine Antwort und „Prüfen“ tippen, dann greift die Ratebremse.

## 11. Annahmen

- Schwellen 80 % je Haken, mindestens 4 Aufgaben aus dem Paket, Lesezeit 1,5 s (im Dummy fest), Tagesziel 3 Runden zu je etwa 5 Minuten, Kennenlern-Runde mit 5 Fragen, normale Runde mit 10.
- Punktwerte 4 / 6 / 10 und Boni 20 / 30 / 50 sind ein erster Vorschlag, damit gründliches Arbeiten etwa zehnmal so viel bringt wie Raten. Feinjustieren nach einigen Wochen Nutzung.
- Beispiel-Lernstand im Dummy: Paket 1 und 2 sicher (1 wieder dran), 3 und 5 noch üben, 4, 6, 7, 8 neu. Kind „Robin“, Rang Komet.
- Nur Mathe (Weltraum) ist ausgearbeitet; die Themenhaut folgt dem Baukasten in `app-redesign.md`.

## 12. Offene Fragen

1. **Schwellen:** Reichen 80 % und 4 Aufgaben für „Können“, oder sollen es zwei gute Runden sein (wie in F)?
2. **Lesezeit:** feste Grenze oder je Kind lernend (ein Kind, das schnell liest, soll nicht ausgebremst werden)? Vorschlag: ab der 20. Antwort die eigene mittlere Antwortzeit als Maß nehmen.
3. **Spiele:** Sollen bestehende Spiele (Duelle, Rennen) Selbst-machen-Aufgaben bekommen, damit sie mehr zählen? Oder bekommen Spiele eigene Spiel-Rekorde statt Lernpunkten?
4. **Behalten bei einem Paket:** Reicht eine Runde mit gemischten Aufgabenarten an einem späteren Tag, wenn ein Fach nur ein Paket hat?
5. **Rückfall:** Ist das Zurückstufen auf „noch üben“ bei unter 50 % zu streng? Alternative: nur die Uhr-Marke „bald wieder üben“.
6. **Bestehende Stände:** Die heutige Stufe 2+ aus reinen Quiz-Runden wird auf „Können fehlt“ gesetzt. Ist das für Robin in Ordnung (ohne Punktabzug)?
7. **Regler:** Soll der Standard „Ausgewogen“ oder für neue Kinder erst „Geführt“ sein, mit Freischaltung durch die Eltern?
8. **Lerngruppe:** gemeinsames Wochenziel aus Haken (z. B. „30 Haken zusammen“) statt Punkte-Rangliste, oder beides?
9. **Fächer ohne „Selbst machen“:** Welche Aufgaben gelten in Deutsch und NWT als Selbst machen (Satz bauen = Ordnen oder Selbst)? Liste je Modul anlegen.
