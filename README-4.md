# Jarvis - Next Level

Voice + text assistant with a Flask backend.

## New in this version
- Python (Flask) backend
- "what's the weather" → real weather via Open-Meteo (no API key needed)
- "tell me a joke" → random joke
- "tell me a quote" → random quote
- Always-on listening (tap mic once, keeps listening/responding)
- Text input box as an alternative to voice

## Run locally
```
pip install -r requirements.txt
python app.py
```
Then open http://localhost:5000

## Deploy on Render
1. Push this folder to a GitHub repo
2. On Render: New → Web Service → connect the repo
3. Build Command:
   ```
   pip install -r requirements.txt
   ```
4. Start Command:
   ```
   gunicorn app:app
   ```
5. Deploy. Render auto-detects the `PORT` env var, gunicorn/Flask use it automatically.
