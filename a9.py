from flask import Flask, render_template_string
app = Flask(__name__)

# Planetary data
planetary_data = [
    {"name": "Sun ☀️", "position": 200.01, "zodiac": "Libra ♎︎", "degrees": 20.01, "nakshatra": "Vishakha", "pada": 1},
    {"name": "Moon 🌙", "position": 228.71, "zodiac": "Scorpio ♏︎", "degrees": 18.71, "nakshatra": "Jyeshta", "pada": 1},
    {"name": "Mercury ☿️", "position": 218.79, "zodiac": "Scorpio ♏︎", "degrees": 8.79, "nakshatra": "Anuradha", "pada": 2},
    {"name": "Venus ♀️", "position": 154.46, "zodiac": "Virgo ♍︎", "degrees": 4.46, "nakshatra": "Uttara Phalguni", "pada": 3},
    {"name": "Mars ♂️", "position": 95.98, "zodiac": "Cancer ♋︎", "degrees": 5.98, "nakshatra": "Pushya", "pada": 1},
    {"name": "Jupiter ♃", "position": 256.16, "zodiac": "Sagittarius ♐︎", "degrees": 16.16, "nakshatra": "Purva Ashadha", "pada": 1},
    {"name": "Saturn ♄", "position": 154.71, "zodiac": "Virgo ♍︎", "degrees": 4.71, "nakshatra": "Uttara Phalguni", "pada": 3}
]

# Basic future prediction by house
house_predictions = {
    1: "🔮 Strong personal growth and identity shift ahead. Confidence and focus will be high.",
    2: "💰 Financial gains are likely. Good time to plan savings and connect with family.",
    3: "✈️ Short travels, communications, and sibling matters come to the forefront.",
    4: "🏠 Peace at home. Ideal time to reconnect with your roots or renovate your space.",
    5: "🎨 Creative success, romance, or child-related matters will gain importance.",
    6: "⚔️ Focus on health, service, and overcoming obstacles. Avoid conflicts.",
    7: "💍 Partnerships bloom. Ideal time for romantic or business bonding.",
    8: "🕯️ Transformation, hidden truths, or joint finances may come into play.",
    9: "📚 Learning, spiritual exploration, or long-distance travel might arise.",
    10: "🧗 Big leaps in career or recognition are on the way. Stay consistent.",
    11: "👥 Social connections, gains, and long-held dreams are within reach.",
    12: "🧘 Time to reflect, rest, or travel inward. Avoid overexertion."
}

# Assume 1st house starts at 200° (Sun's current position) for simplicity
def get_house(longitude, asc_deg=200):
    diff = (longitude - asc_deg) % 360
    return int(diff // 30) + 1

@app.route('/')
def show_astrology():
    # Attach house and future prediction
    for planet in planetary_data:
        house = get_house(planet["position"])
        planet["house"] = house
        planet["future"] = house_predictions.get(house, "✨ Future holds subtle mysteries for this placement.")
    
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Astrology Today + Future 🌠</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #fdfdfd; padding: 20px; }
        h1 { text-align: center; color: #333; margin-bottom: 30px; }
        .planet {
            background: white;
            border-radius: 12px;
            padding: 15px;
            margin: 15px auto;
            max-width: 700px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        .planet h2 { margin: 0; color: #444; }
        .info, .house, .benefit-bar, .future { font-size: 15px; color: #444; margin-top: 10px; }
        .benefit-bar {
            background: #e8f5e9;
            color: #2e7d32;
            padding: 10px;
            border-left: 5px solid #43a047;
            font-weight: 500;
        }
        .future {
            background: #fff3e0;
            color: #ef6c00;
            padding: 10px;
            border-left: 5px solid #ff9800;
        }
    </style>
</head>
<body>
    <h1>🌟 Today's Planetary Benefits + Future Prediction</h1>

    {% for planet in data %}
    <div class="planet">
        <h2>{{ planet.name }}</h2>
        <div class="info">
            <strong>Position:</strong> {{ planet.position }}°<br>
            <strong>Zodiac Sign:</strong> {{ planet.zodiac }}<br>
            <strong>Degrees:</strong> {{ planet.degrees }}°<br>
            <strong>Nakshatra:</strong> {{ planet.nakshatra }} (Pada {{ planet.pada }})<br>
            <strong>House:</strong> {{ planet.house }}
        </div>
        <div class="benefit-bar">{{ benefits[planet.name] }}</div>
        <div class="future"><strong>🔮 Prediction:</strong> {{ planet.future }}</div>
    </div>
    {% endfor %}
</body>
</html>
''', data=planetary_data, benefits={
    "Sun ☀️": "🧘 Confidence | 🌐 Public Influence | ⚖️ Justice | 🔎 Clarity in Leadership",
    "Moon 🌙": "🌊 Emotional Strength | 🔐 Secrets Revealed | 🧠 Intuition | ✨ Spiritual Awakening",
    "Mercury ☿️": "🗣️ Persuasion | 🔍 Strategic Thinking | 📖 Deep Learning | 🧠 Mental Focus",
    "Venus ♀️": "🎨 Aesthetic Purity | ❤️ Practical Love | 🧺 Order & Cleanliness | 🪄 Creative Refinement",
    "Mars ♂️": "💪 Emotional Courage | 🏡 Family Protection | 🔧 Repair Energy | 🚫 Avoid Aggression",
    "Jupiter ♃": "📚 Wisdom | 🧭 Righteous Path | 🛤️ Expansion | ✨ Good Fortune",
    "Saturn ♄": "🛠️ Disciplined Effort | 🗓️ Routine Building | 📈 Career Growth | ⏳ Patience Rewarded"
})

if __name__ == '__main__':
    app.run(debug=True)
