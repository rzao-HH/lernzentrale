"""Alle Tests nacheinander ausführen: python tests/run_all.py"""
import subprocess,sys,os,glob
here=os.path.dirname(os.path.abspath(__file__));os.makedirs(os.path.join(here,'out'),exist_ok=True)
bad=0
for t in sorted(glob.glob(os.path.join(here,'test_*.py'))):
    r=subprocess.run([sys.executable,t],cwd=here,capture_output=True,text=True,timeout=900)
    out=r.stdout+r.stderr;ok=r.returncode==0 and 'Traceback' not in out and not any(l.startswith('errors') and "['" in l for l in out.splitlines())
    print(('✅' if ok else '❌'),os.path.basename(t));bad+=0 if ok else 1
    if not ok:print(out[-1500:])
sys.exit(1 if bad else 0)
