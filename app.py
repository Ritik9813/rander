from flask import Flask, render_template, request
from datetime import datetime
import pytz
from skyfield.api import load, Topos

app = Flask(__name__)


# Load planetary data
planets = load('de421.bsp')
ts = load.timescale()

zodiac_signs = [
    "Aries ♈︎", "Taurus ♉︎", "Gemini ♊︎", "Cancer ♋︎", "Leo ♌︎", "Virgo ♍︎",
    "Libra ♎︎", "Scorpio ♏︎", "Sagittarius ♐︎", "Capricorn ♑︎", "Aquarius ♒︎", "Pisces ♓︎"
]

nakshatras = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
    "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra",
    "Swati", "Vishakha", "Anuradha", "Jyeshta", "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

planet_keys = {
    'Sun ☀️': 'sun',
    'Moon 🌙': 'moon',
    'Mercury ☿️': 'mercury',
    'Venus ♀️': 'venus',
    'Mars ♂️': 'mars',
    'Jupiter ♃': 'jupiter barycenter',
    'Saturn ♄': 'saturn barycenter'
}

house_benefits = {
    1: "Self, body, personality: A good day to focus on your personal health and well-being.",
    2: "Family, wealth, speech: You may receive material gains and family harmony.",
    3: "Siblings, courage: A good day to communicate or be bold.",
    4: "Home, mother: Good for family bonding and peace.",
    5: "Children, creativity: Favorable for romantic and artistic efforts.",
    6: "Enemies, health: Time to overcome obstacles and heal.",
    7: "Marriage, partner: Great for partnerships and deep connections.",
    8: "Transformation, secrets: Inner changes and uncovering truths.",
    9: "Luck, higher learning: Excellent for wisdom, travel, and spirituality.",
    10: "Career, status: Recognition and career growth await.",
    11: "Friends, gains: Network expansion and wishes fulfilled.",
    12: "Spirituality, losses: Time to reflect, retreat, and grow within."
}

house_predictions = {
    1: "🔮 Strong personal growth and identity shift ahead.",
    2: "💰 Financial gains and stronger family bonding likely.",
    3: "✈️ Travels and new communication ventures ahead.",
    4: "🏠 Peace at home; good time to invest emotionally.",
    5: "🎨 Romance, creativity, and children come to focus.",
    6: "⚔️ Face health and enemies wisely; time to heal.",
    7: "💍 New partnerships or strengthening old ones possible.",
    8: "🕯️ Big changes, transformation, or shared assets influence.",
    9: "📚 Higher knowledge, travel or blessings may arrive.",
    10: "🧗 Career boost or public image elevation ahead.",
    11: "👥 Friends, networks and dreams will align positively.",
    12: "🧘 Reflection, solitude, or spiritual growth will benefit."
}


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        try:
            birth_date = request.form['birth_date']
            birth_time = request.form['birth_time']
            latitude = float(request.form['latitude'])
            longitude = float(request.form['longitude'])
            timezone = request.form['timezone']

            dt_local = pytz.timezone(timezone).localize(datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M"))
            dt_utc = dt_local.astimezone(pytz.utc)

            t = ts.from_datetime(dt_utc)
            observer = planets['earth'] + Topos(latitude_degrees=latitude, longitude_degrees=longitude)

            ascendant_deg = get_ascendant(observer, t)
            houses = calculate_houses(ascendant_deg)

            planetary_positions = []

            for name, key in planet_keys.items():
                planet = planets[key]
                astrometric = observer.at(t).observe(planet).apparent()
                ecliptic = astrometric.ecliptic_latlon()
                longitude_deg = ecliptic[1].degrees % 360

                rashi_index = int(longitude_deg // 30)
                rashi = zodiac_signs[rashi_index]
                degree_in_sign = longitude_deg % 30

                nak_index = int(longitude_deg // (360 / 27))
                nakshatra = nakshatras[nak_index]
                pada = int((longitude_deg % (360 / 27)) // 3.3333) + 1

                house = get_house(longitude_deg, ascendant_deg)
                future = house_predictions.get(house, "✨ Unfolding potential in subtle areas.")

                planetary_positions.append({
                    'name': name,
                    'position': round(longitude_deg, 2),
                    'rashi': rashi,
                    'degree_in_sign': round(degree_in_sign, 2),
                    'nakshatra': nakshatra,
                    'pada': pada,
                    'house': house,
                    'future': future,
                    'benefit': house_benefits[house]
                })

            return render_template("result.html", planetary_positions=planetary_positions)

        except Exception as e:
            error = str(e)

    return render_template("index.html", error=error)


def get_ascendant(observer, t):
    sun = planets['sun']
    astrometric = observer.at(t).observe(sun).apparent()
    ecliptic = astrometric.ecliptic_latlon()
    return ecliptic[1].degrees


def calculate_houses(ascendant_deg):
    return [(ascendant_deg + i * 30) % 360 for i in range(12)]


def get_house(longitude, asc_deg):
    diff = (longitude - asc_deg) % 360
    return int(diff // 30) + 1


if __name__ == "__main__":
    app.run(debug=True)
