"""Vorschau bauen: kopiert die App (index.html, sw.js, Icon, apps/, js/, css/) aus einem Git-Stand nach vorschau/.
Erreichbar unter https://rzao-hh.github.io/lernzentrale/vorschau/ – die echte App (Hauptordner) bleibt unverändert.

Aufruf (im Repository):  python3 tools/vorschau.py [git-stand]     z. B.  python3 tools/vorschau.py entwicklung
Ohne Angabe wird der aktuelle Arbeitsstand genommen.

Anpassungen in der Kopie:
- Links auf ../lernzettel/, ../nachtest/, ../videos/ zeigen auf die Ordner der echten App (eine Ebene höher).
- Service Worker mit eigenem Cache-Präfix „lzv-“, damit Vorschau und echte App sich den Offline-Speicher nicht gegenseitig löschen.
- Rotes Schild „🧪 Vorschau“ unten rechts auf der Startseite und in jeder App.
Achtung: Die Vorschau liegt auf derselben Adresse und nutzt den Gerätespeicher mit. Zum Testen eine Person „Test“ ohne Benutzernamen anlegen."""
import os,sys,shutil,subprocess,tempfile
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,'vorschau')
PARTS=['index.html','sw.js','icon-180.png','apps','js','css']
BADGE='<div id="lzPreview" style="position:fixed;right:8px;bottom:calc(6px + env(safe-area-inset-bottom,0px));z-index:99999;background:#c0392b;color:#fff;font:800 12px/1 system-ui,sans-serif;padding:6px 10px;border-radius:999px;box-shadow:0 2px 8px rgba(0,0,0,.25);pointer-events:none">🧪 Vorschau</div>'
def src_dir(ref):
    if not ref: return ROOT,None
    tmp=tempfile.mkdtemp()
    a=subprocess.run(['git','-C',ROOT,'archive',ref]+PARTS,capture_output=True,check=True).stdout
    subprocess.run(['tar','-x','-C',tmp],input=a,check=True)
    return tmp,tmp
def main():
    ref=sys.argv[1] if len(sys.argv)>1 else None
    src,tmp=src_dir(ref)
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    for p in PARTS:
        s=os.path.join(src,p);d=os.path.join(OUT,p)
        (shutil.copytree if os.path.isdir(s) else shutil.copy2)(s,d)
    for dp,_,fs in os.walk(OUT):
        for f in fs:
            if not f.endswith(('.html','.js','.css')): continue
            fp=os.path.join(dp,f);t=open(fp,encoding='utf-8').read()
            for folder in ('lernzettel','nachtest','videos'): t=t.replace('../'+folder+'/','../../'+folder+'/')
            if f=='sw.js':
                assert 'CACHE="lz-"+VER' in t and 'k.startsWith("lz-")' in t,'sw.js hat sich geändert – vorschau.py anpassen'
                t=t.replace('CACHE="lz-"+VER','CACHE="lzv-"+VER').replace('k.startsWith("lz-")','k.startsWith("lzv-")')
            if f.endswith('.html') and '</body>' in t: t=t.replace('</body>',BADGE+'</body>',1)
            open(fp,'w',encoding='utf-8').write(t)
    open(os.path.join(OUT,'LIESMICH.md'),'w',encoding='utf-8').write('# Vorschau\n\nAutomatisch erzeugt mit `python3 tools/vorschau.py '+(ref or '')+'` – nicht von Hand ändern.\nÄnderungen immer im Hauptordner bzw. im Zweig `entwicklung` machen.\n')
    if tmp: shutil.rmtree(tmp)
    print('Vorschau gebaut aus',ref or 'Arbeitsstand','→',OUT)
main()
