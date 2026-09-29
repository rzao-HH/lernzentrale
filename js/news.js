/* ===================== 🆕 Was ist neu? ===================== */
(function(){
const NEWS=[
 ["7.7.0","29.09.2026",["📐 Winkel-Akademie, Aufgaben-Mission – neu nach Abgleich mit den Lernzetteln:","🧭 Punkte einzeichnen, Wege mit Kurs und Kästchen gehen (Schatzsuche), links oder rechts herum in dieselbe Richtung","🧮 Winkel an geschnittenen Parallelen (AH S. 16 Nr. 5) und Winkel im Dreieck messen (AH S. 18)","📏 Parallele im Abstand zeichnen und Rechtecke ergänzen (Übungsheft Geodreieck)"]],
 ["7.6.1","29.09.2026",["📐 Winkel-Akademie: Bei „Wie viele rechte Winkel hat jedes Rechteck?“ ist jetzt ein Rechteck zu sehen; nach der Antwort sind die vier rechten Winkel markiert"]],
 ["7.6.0","29.09.2026",["📄 Winkel-Akademie: Der 📄-Knopf oben öffnet jetzt auch die Mathe-Lernzettel – 45 Blätter zu Kompass, Winkelarten, Messen, Zeichnen, Berechnen und Geodreieck, mit Lösungen"]],
 ["7.5.0","28.09.2026",["🧭 Winkel-Akademie, „Wissen“: Kompass und Kurs ausführlich – Kompassrose mit Gradzahlen, Drehungen als Bruchteil mit Bildern, Kurs Schritt für Schritt im Koordinatensystem","🙈 Aufgaben-Mission verrät die Lösung nicht mehr: keine Gradzahl bei „Wie viel Grad sind ¾ Drehung?“, kein eingefärbter Bruchteil bei „Welcher Bruchteil sind 270°?“, keine Beschriftung S, a, b, α bei den Fragen zu den Teilen des Winkels"]],
 ["7.4.0","28.09.2026",["📄 Neuer Knopf oben in der Wasser-Zauberschule, der Küsten-Crew und im Detektiv-Büro: öffnet die Lernzettel (Fotos der Arbeitsblätter) in einem neuen Tab – in Englisch mit Auswahl zwischen Unit 5/6 und Simple Past. Braucht Internet.","📱 Wasser-Zauberschule und Detektiv-Büro: Die Kopfleiste passt jetzt auch auf schmale Handys (🔊 ragte über den Rand, der Rangname wurde abgeschnitten)"]],
 ["7.3.2","28.09.2026",["🗓️ Lernplan: Pakete mit unterschiedlichem Tipp stehen jetzt in eigenen Zeilen mit eigenem Knopf – z. B. in der Winkel-Akademie „Messen und Winkelart erkennen“ für Paket 4, „Aufgaben-Mission“ für Pakete 5 und 6"]],
 ["7.3.1","28.09.2026",["📄 Lernzettel-Angabe jetzt auch bei allen Mathe-Paketen, den Englisch-Vokabeln (Seiten der Vokabelliste) und den unregelmäßigen Verben"]],
 ["7.3.0","28.09.2026",["🧱 Detektiv-Büro, Satz-Baumeister: Bei „und“, „oder“ und „weder … noch“ ist die Reihenfolge der beiden Teile egal – geprüft wird nur, wohin das Verb wandert","📄 Pakete zeigen, auf welchen Lernzettel sie sich beziehen (Deutsch, NWT, Englisch-Grammatik)","💡 Detektiv-Büro: Lernkarten haben unter der Antwort klein gedruckt eine Zusatz-Erklärung mit Beispiel vom Lernzettel"]],
 ["7.2.0","28.09.2026",["🗓️ Lernplan in allen Fächern: Der Knopf heißt jetzt „📦 Pakete auswählen“ und wählt nur die Pakete aus – die Seite springt nicht mehr weg","🟧 Die Übung oder Prüfung, die laut Lernplan dran ist, hat unten einen dicken Rahmen","✅ Der angetippte Knopf zeigt „✓ Ausgewählt“, bis du die Pakete von Hand änderst"]],
 ["7.1.10","28.09.2026",["⚔️ Arena: Live-Duell erkennt jetzt zuverlässig, wenn jemand online ist – vorher hielt die App das andere Gerät fälschlich für „sich selbst“, wenn auf beiden Geräten die erste angelegte Person dieselbe interne Nummer hatte"]],
 ["7.1.9","27.09.2026",["🏆 Rangliste zeigt automatisch die Lerngruppe statt „Dieses Gerät“, wenn man einer beigetreten ist"]],
 ["7.1.8","27.09.2026",["🏆 Rangliste: Die Lerngruppen-Reiter fehlten manchmal direkt nach dem Laden – behoben"]],
 ["7.1.7","27.09.2026",["⚔️ Arena: Online-Erkennung fragt den Server jetzt genauso ab wie Abgleich und Lerngruppen","🩺 Im Herausfordern-Fenster steht, ob die Verbindung zum Arena-Server klappt; Fehler erscheinen auf der Arena-Karte"]],
 ["7.1.6","27.09.2026",["🔧 Apps erscheinen beim Öffnen sofort (vorher blieb die Seite manchmal leer bis zum Neuladen)","🔬 Wasser-Zauberschule: Experimentier-Werkstatt und Forscherlabor sind jetzt ein Forscherlabor mit sechs Stationen","🦉 Wasser-Zauberschule: Der erste Test unter „Prüfen“ heißt wieder Zauberprüfung"]],
 ["7.1.5","27.09.2026",["📄 Detektiv-Büro: Jede Lernkarte nennt auf der Rückseite ihren Lernzettel (Nr. 29–41 oder Heft Zeitformen); was nicht auf den Zetteln steht, ist als Zusatz markiert"]],
 ["7.1.4","27.09.2026",["🕵️ Detektiv-Büro: Lernkarten zeigen vorne eine klare Frage, Antworten im Wortlaut der Lernzettel","🔎 Verb-Jäger: angetippte Wörter sind deutlich markiert, nach dem Prüfen ✓ und durchgestrichen","📝 Begriffe wie auf den Lernzetteln: „gebeugte (finite) Verbform“, „Nebensatz-Konjunktionen“, kein „Relativsatz“ mehr"]],
 ["7.1.3","27.09.2026",["🐚 Küsten-Crew: „Laut Lernplan heute“ steht jetzt wie in den anderen Apps über „Pakete wählen“, mit „Diese Pakete wählen“"]],
 ["7.1.2","27.09.2026",["⚔️ Arena: funktioniert jetzt auch, wenn die Uhr eines Geräts falsch geht","👻 Geister-Duell gegen alle aus den eigenen Lerngruppen – auch gegen die, die gerade online sind"]],
 ["7.1.1","27.09.2026",["⚔️ Arena: Wer online ist, wird jetzt zuverlässig angezeigt; Live-Duelle laufen über dieselbe Datenbank wie der Abgleich"]],
 ["7.1.0","27.09.2026",["👥 Alle Lerngruppen sind für alle sichtbar: unter „Weitere Lerngruppen“ mit einem Tipp beitreten – kein Code mehr nötig"]],
 ["7.0.1","27.09.2026",["🔧 Anmelden mit Benutzername funktioniert jetzt (vorher „Keine Verbindung zum Server“)","✏️ Keine Mindestlänge mehr für Benutzernamen"]],
 ["7.0.0","27.09.2026",["👤 Anmelden mit Benutzernamen: Namen eingeben – auf jedem Gerät sind Punkte, Noten und Lernplan sofort da","📅 Der Lernplan gilt jetzt pro Person","🧹 Der Geräte-Code fällt weg; Lerngruppen und Arena laufen über den Benutzernamen"]],
 ["6.7.0","27.09.2026",["🧭 Einheitliche Bedienung: überall „Punkte“ und „Abschlusstest“, Zurück-Pfeil ← in allen Apps","🐚 Küsten-Crew: Ton an/aus mit Klängen bei richtig und falsch, Dunkelmodus, Noten-Sprüche im Küsten-Stil"]],
 ["6.6.0","27.09.2026",["📴 Offline-Modus: Nach einem Besuch mit Internet öffnet sich die Lernzentrale auch ohne Internet","🧹 Im Hintergrund aufgeräumt: aufgeteilt in Startseite, vier Apps und gemeinsame Bausteine – für Robin bleibt alles gleich","🖼️ Eigenes Symbol für den Home-Bildschirm"]],
 ["6.5.1","27.09.2026",["🔢 Versionsnummern sind jetzt dreistellig: große Umbauten · neue Funktionen · kleine Korrekturen"]],
 ["6.5","27.09.2026",["🆕 Diese Seite: Was ist neu? – ganz unten auf der Startseite über „🆕 Was ist neu?“","👥 Gleicher Name in einer Lerngruppe: Beim Beitreten kann man einen eigenen Namen für die Gruppe wählen","👥 Warnung, wenn man schon in einer Lerngruppe mit demselben Namen ist"]],
 ["6.4","27.09.2026",["👥 Lerngruppen: beliebig viele anlegen, per Link oder Code teilen, beitreten und austreten","🏆 Rangliste mit Reitern: dieses Gerät und jede Lerngruppe","⚔️ Arena über alle Lerngruppen, auch zwischen verschiedenen Familien","📱 „Geräte verbinden“ heißt jetzt so (vorher „Lerngruppe“) und gleicht den ganzen Lernstand der eigenen Geräte ab"]],
 ["6.3","27.09.2026",["⚔️ Arena: 🪢 Tauziehen live gegen andere","⚡ Power-ups: Einfrieren, Doppelzug, Schild","👻 Geister-Duell gegen Aufzeichnungen, wenn der andere offline ist","🎰 Fach-Glücksrad mit Fragen aus allen vier Apps","💰 Arena-Punkte mit Einsatz, eigene Spalte in der Rangliste","⚔️-Knopf oben in jeder App"]],
 ["6.2","27.09.2026",["🕵️ Detektiv-Büro: ⚡ Blitz-Ermittlung – 60 Sekunden, mit Rekord pro Akten-Auswahl"]],
 ["6.1","27.09.2026",["🐚 Küsten-Crew: ☕ Café in Brighton (bestellen, mit Pfund bezahlen, Wechselgeld)","🔎 Verhör im Hafen (Fragen im Simple Past, Täter finden)","🗺️ Küsten-Schatzkarte","🔊 Hör-Kapitän (britische Aussprache)","📝 Schreibtest mit Musterlösung und Note"]],
 ["6.0","27.09.2026",["🐚 Küsten-Crew im Aufbau der anderen Apps: Pakete wählen, Mission starten","⚓ Punkte und Ränge vom Schiffsjungen bis zum Admiral","🏆 Englisch zählt jetzt in der Rangliste"]],
 ["5.9","26.09.2026",["🏆 Rangliste auf der Startseite: Winkel, NWT, Deutsch und Gesamt"]],
 ["5.8","26.09.2026",["🔧 Personen bekommen eindeutige Kennungen, damit auf mehreren Geräten nichts vermischt wird"]],
 ["5.1–5.7","26.09.2026",["🌐 Umzug auf die eigene Adresse rzao-hh.github.io/lernzentrale – Updates löschen keine Punkte mehr","☁️ Abgleich zwischen Geräten über eine eigene Datenbank","🎨 Verbinden-Karte oben statt versteckt im Fußbereich, klarere Beschriftungen"]],
 ["5.0","26.09.2026",["🪄 Wasser-Zauberschule: Noten aus Prüfung und Schreibtest direkt auf den Paket-Karten"]],
 ["4.9","26.09.2026",["📐 Winkel-Akademie: Pakete 5–8 (Kompass, Winkel benennen, berechnen, Senkrechte & Parallelen) und Schul-Checkliste"]],
 ["4.8","26.09.2026",["🧹 Eltern-Bereich und KI-Korrektur entfernt, Schreibtests mit Selbstkontrolle"]],
 ["4.5–4.7","25.09.2026",["🧪 Werkstatt und Forscherlabor mit Start/Prüfen und ausgeblendeter Anzeige während der Aufgabe","🔎 Speicher-Info unten auf der Startseite"]],
 ["4.4","25.09.2026",["🚫 Keine Anmelde-Aufforderung mehr beim Öffnen"]]
];
const cur=NEWS[0][0];
const OV=document.createElement("div");OV.id="newsOv";document.body.appendChild(OV);
function open(){OV.innerHTML=`<div class="ar-box"><div class="ar-top"><b>🆕 Was ist neu?</b><button type="button" class="ar-x" data-nx>✕</button></div>
  ${NEWS.map(([v,d,L])=>`<div class="nw-v"><div class="nw-h"><b>Version ${v}</b><small>${d}</small></div><ul>${L.map(x=>`<li>${x}</li>`).join("")}</ul></div>`).join("")}</div>`;
  OV.classList.add("on");try{localStorage.setItem("lz-news-seen",cur);}catch(e){}mark();}
function mark(){const v=document.querySelector("footer .ver");if(!v)return;let seen="";try{seen=localStorage.getItem("lz-news-seen")||"";}catch(e){}
  let b=document.getElementById("nwBtn");if(!b){b=document.createElement("button");b.type="button";b.id="nwBtn";b.className="nw-link";b.setAttribute("data-news","1");v.after(b);}
  b.innerHTML=`🆕 Was ist neu?${seen!==cur?' <span class="nw-dot">neu</span>':""}`;}
OV.addEventListener("click",e=>{if(e.target.closest("[data-nx]")||e.target===OV)OV.classList.remove("on");});
document.addEventListener("click",e=>{if(e.target.closest&&e.target.closest("[data-news]"))open();});
window.lzNewsOpen=open;mark();
})();
