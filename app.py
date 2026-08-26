import os
import requests
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


# ---------- Weather (no API key needed - Open-Meteo) ----------
@app.route("/api/weather")
def weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "location not provided"}), 400

    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&current=temperature_2m,weather_code,wind_speed_10m"
        )
        r = requests.get(url, timeout=6)
        data = r.json()
        current = data.get("current", {})

        weather_codes = {
            0: "clear sky", 1: "mostly clear", 2: "partly cloudy", 3: "overcast",
            45: "foggy", 48: "foggy", 51: "light drizzle", 61: "light rain",
            63: "rain", 65: "heavy rain", 71: "light snow", 73: "snow",
            75: "heavy snow", 80: "rain showers", 95: "thunderstorm",
        }
        condition = weather_codes.get(current.get("weather_code"), "unclear conditions")

        return jsonify({
            "temperature": current.get("temperature_2m"),
            "condition": condition,
            "wind": current.get("wind_speed_10m"),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- Joke (no API key needed) ----------
@app.route("/api/joke")
def joke():
    try:
        r = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=6)
        data = r.json()
        return jsonify({
            "text": f"{data.get('setup', '')} ... {data.get('punchline', '')}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- Quote (no API key needed) ----------
@app.route("/api/quote")
def quote():
    try:
        r = requests.get("https://api.quotable.io/random", timeout=6)
        data = r.json()
        return jsonify({
            "text": f"{data.get('content', '')} — {data.get('author', '')}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


# ---------- Chatbot (real AI answers via Groq - free tier) ----------
@app.route("/api/chat", methods=["POST"])
def chat():
    if not GROQ_API_KEY:
        return jsonify({"error": "GROQ_API_KEY not set on the server"}), 500

    user_message = (request.json or {}).get("message", "").strip()
    if not user_message:
        return jsonify({"error": "no message provided"}), 400

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are Jarvis, a helpful voice assistant. "
                        "Keep replies short and conversational since they will be spoken aloud - "
                        "usually 1-3 sentences."
                    ),
                },
                {"role": "user", "content": user_message},
            ],
        }
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=15,
        )
        data = r.json()
        reply = data["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
