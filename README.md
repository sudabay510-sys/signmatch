# SignMatch

Make your business name, address, and phone match everywhere customers look.

## Run locally
```bash
cd /workspace/quiz-plans
.venv/bin/python signmatch/app.py
# → http://127.0.0.1:5102
```

Admin: set `SIGNMATCH_ADMIN_PASSWORD` then visit `/admin`.

## Tests
```bash
cd /workspace/quiz-plans/signmatch
../.venv/bin/pytest -q
```

**Not production-ready:** no Stripe, ephemeral/local SQLite, deterministic plans (AI hook can be added later), founding-list only.

## Production-style run
```bash
pip install -r requirements.txt
PORT=10000 gunicorn -b 0.0.0.0:$PORT app:app
```

Set `SECRET_KEY` and `ADMIN_PASSWORD` in the environment. Set `DATABASE_URL` to the shared Neon pooled connection string and `DATABASE_SCHEMA` to this app's slug so leads and quiz answers survive restarts. When `DATABASE_URL` is unset, the app falls back to a local SQLite file. There is no payment processor; the paywall is a founding-list signup only.
