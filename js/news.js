/* ===================== 🆕 Was ist neu? ===================== */
(function(){
const NEWS=[
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
