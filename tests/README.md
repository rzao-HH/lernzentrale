# Tests der Lernzentrale

Automatische Browser-Tests (Playwright/Chromium). Supabase und die Live-Verbindung der Arena werden simuliert.

```
pip install playwright && python -m playwright install chromium
python tests/run_all.py
```

Einzelne Tests: `python tests/test_sync.py` usw. Screenshots landen in `tests/out/`.
