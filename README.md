
# NeuroDx – Flask app (ready for Render/Heroku/Railway)

## Project structure
```
neurodx/
├─ app.py
├─ requirements.txt
├─ Procfile
└─ templates/
   ├─ index.html
   └─ result.html
```

## Local run
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
# open http://localhost:8080
```

## Deploy (Render example)
1. Push this folder to a GitHub repo.
2. On Render, create **Web Service** → connect the repo.
3. Runtime: Python 3.11+
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app`
6. Render will set `$PORT` automatically – app.py reads it.

> Note: Netlify does **not** run Python/Flask servers. If you want to keep Netlify for the frontend, host this Flask backend on Render/Railway and point your frontend to it (or add a proxy).
