from flask import Flask, request, render_template_string
import urllib.request
import json

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agro Future | Smart Agriculture</title>

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f4f8f2;
    color: #26352a;
}

header {
    background: #176b3a;
    color: white;
    padding: 24px 8%;
}

header h1 {
    margin: 0;
    font-size: 32px;
}

header p {
    margin-bottom: 0;
}

nav {
    background: white;
    padding: 16px 8%;
    box-shadow: 0 2px 8px #0001;
}

nav a {
    color: #176b3a;
    text-decoration: none;
    margin-right: 22px;
    font-weight: bold;
}

.hero {
    padding: 45px 8%;
    background: linear-gradient(120deg, #e2f2df, #f8fff5);
}

.hero h2 {
    color: #176b3a;
    font-size: 34px;
}

.hero p {
    font-size: 17px;
    line-height: 1.7;
}

.container {
    max-width: 1100px;
    margin: 30px auto;
    padding: 0 18px;
}

.cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 18px;
}

.card {
    background: white;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 3px 12px #0000000c;
}

.card h3 {
    color: #176b3a;
}

form {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 18px;
}

label {
    display: block;
    font-weight: bold;
    margin-bottom: 8px;
}

input, select {
    width: 100%;
    padding: 12px;
    border: 1px solid #cbd8ca;
    border-radius: 7px;
    font-size: 15px;
}

button {
    background: #208447;
    color: white;
    border: none;
    padding: 14px 22px;
    border-radius: 7px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
}

button:hover {
    background: #145d30;
}

.result {
    margin-top: 24px;
    padding: 22px;
    background: #e4f5e5;
    border-left: 5px solid #208447;
    border-radius: 8px;
    line-height: 1.8;
}

.note {
    color: #657267;
    font-size: 14px;
    line-height: 1.6;
}

footer {
    margin-top: 45px;
    padding: 25px;
    text-align: center;
    color: white;
    background: #176b3a;
}

@media (max-width: 600px) {
    header h1 {
        font-size: 26px;
    }

    .hero h2 {
        font-size: 27px;
    }

    nav a {
        display: inline-block;
        margin: 5px 10px 5px 0;
    }
}
</style>
</head>

<body>

<header>
    <h1>🌱 Agro Future</h1>
    <p>AI-Powered Smart Agriculture & Crop Planning</p>
</header>

<nav>
    <a href="#home">Home</a>
    <a href="#recommend">Crop Recommendation</a>
    <a href="#weather">Weather</a>
    <a href="#fertilizer">Fertilizer Guide</a>
</nav>

<section class="hero" id="home">
    <h2>Grow Smarter. Farm Better.</h2>
    <p>
        Welcome to Agro Future! Explore suitable crops for your land
        using soil information, pH, temperature, humidity and rainfall.
        Get basic soil guidance, weather information and fertilizer tips
        in one place.
    </p>
    <a href="#recommend">
        <button>Find Suitable Crops 🌾</button>
    </a>
</section>

<div class="container">
    <h2>Our Smart Agriculture Services</h2>

    <div class="cards">
        <div class="card">
            <h3>🌾 Crop Recommendation</h3>
            <p>Explore crops based on the soil and environmental values you enter.</p>
        </div>

        <div class="card">
            <h3>🧪 Soil pH Analysis</h3>
            <p>Understand whether your soil is acidic, neutral or alkaline.</p>
        </div>

        <div class="card" id="weather">
            <h3>🌦️ Weather Information</h3>
            <p>Look up current weather for a supported location using a weather service.</p>
        </div>

        <div class="card" id="fertilizer">
            <h3>🌿 Fertilizer Guidance</h3>
            <p>Learn why soil testing is important before choosing fertilizers.</p>
        </div>
    </div>
</div>

<div class="container" id="recommend">
    <div class="card">
        <h2>🌾 Crop Recommendation System</h2>
        <p>Enter the available information about your farmland.</p>

        <form method="POST" action="/recommend">

            <div>
                <label>Soil pH (0–14)</label>
                <input type="number" name="ph" min="0" max="14"
                       step="0.1" value="6.5" required>
            </div>

            <div>
                <label>Temperature (°C)</label>
                <input type="number" name="temperature"
                       min="-10" max="60" step="0.1"
                       value="27" required>
            </div>

            <div>
                <label>Humidity (%)</label>
                <input type="number" name="humidity"
                       min="0" max="100" step="0.1"
                       value="70" required>
            </div>

            <div>
                <label>Annual Rainfall (mm)</label>
                <input type="number" name="rainfall"
                       min="0" max="10000" step="1"
                       value="1200" required>
            </div>

            <div>
                <label>Soil Type</label>
                <select name="soil">
                    <option>Loamy</option>
                    <option>Clay</option>
                    <option>Sandy</option>
                    <option>Silty</option>
                    <option>Laterite</option>
                    <option>Black Soil</option>
                </select>
            </div>

            <div>
                <label>Water Availability</label>
                <select name="water">
                    <option>High</option>
                    <option>Medium</option>
                    <option>Low</option>
                </select>
            </div>

            <div>
                <label>Location (for weather)</label>
                <input type="text" name="location"
                       placeholder="e.g. Kochi">
            </div>

            <div style="align-self:end">
                <button type="submit">Analyze My Farm</button>
            </div>

        </form>

        {% if result %}
        <div class="result">
            <h3>🌱 Your Farm Analysis</h3>
            <p><b>Soil pH:</b> {{ result.ph }}</p>
            <p><b>Soil condition:</b> {{ result.ph_text }}</p>
            <p><b>Entered soil type:</b> {{ result.soil }}</p>
            <p><b>Temperature:</b> {{ result.temperature }} °C</p>
            <p><b>Humidity:</b> {{ result.humidity }}%</p>
            <p><b>Rainfall:</b> {{ result.rainfall }} mm</p>
            <p><b>Water availability:</b> {{ result.water }}</p>

            <h3>Suggested Crops to Investigate</h3>
            <p>{{ result.crops }}</p>

            <h3>Soil and Fertilizer Guidance</h3>
            <p>{{ result.fertilizer }}</p>

            <p class="note">
                These are preliminary educational suggestions based on
                simple rules, not a trained AI prediction. Confirm crop
                suitability with local agricultural experts and a soil test.
            </p>
        </div>
        {% endif %}
    </div>
</div>

<div class="container">
    <div class="card">
        <h2>🌦️ Current Weather Lookup</h2>
        <p>
            Weather data is fetched from Open-Meteo when an internet
            connection is available.
        </p>

        <form method="POST" action="/weather">
            <div>
                <label>City or Town</label>
                <input name="location" placeholder="e.g. Kochi" required>
            </div>

            <div style="align-self:end">
                <button type="submit">Check Weather</button>
            </div>
        </form>

        {% if weather %}
        <div class="result">
            <h3>Weather for {{ weather.location }}</h3>
            <p><b>Temperature:</b> {{ weather.temperature }} °C</p>
            <p><b>Relative humidity:</b> {{ weather.humidity }}%</p>
            <p><b>Wind speed:</b> {{ weather.wind }} km/h</p>
            <p><b>Condition:</b> {{ weather.condition }}</p>
        </div>
        {% endif %}

        {% if weather_error %}
        <p class="result">{{ weather_error }}</p>
        {% endif %}
    </div>
</div>

<footer>
    <h3>Agro Future 🌱</h3>
    <p>Smart Agriculture for a Sustainable Future</p>
    <p>Educational AI Project | CBSE Class XII</p>
</footer>

</body>
</html>
"""


def ph_description(ph):
    if ph < 5.5:
        return "Strongly acidic soil"
    elif ph < 6.5:
        return "Moderately acidic soil"
    elif ph <= 7.5:
        return "Near-neutral soil"
    elif ph <= 8.5:
        return "Alkaline soil"
    return "Strongly alkaline soil"


def recommend_crops(ph, temperature, humidity, rainfall, soil, water):
    crops = []

    if rainfall >= 1000 and temperature >= 20:
        crops.extend(["Rice", "Banana"])

    if 20 <= temperature <= 35 and rainfall >= 500:
        crops.extend(["Maize", "Groundnut"])

    if 18 <= temperature <= 32 and 5.5 <= ph <= 7.5:
        crops.extend(["Vegetables", "Pulses"])

    if soil in ["Laterite", "Loamy"] and rainfall >= 1500:
        crops.extend(["Rubber", "Pineapple"])

    if soil == "Sandy" and rainfall < 1000:
        crops.extend(["Millets", "Groundnut"])

    if water == "Low":
        crops.extend(["Millets", "Pulses"])

    if humidity >= 75 and temperature >= 24:
        crops.append("Banana")

    if ph < 5.0:
        crops = [crop for crop in crops if crop not in ["Pulses"]]

    if ph > 8.5:
        crops = [crop for crop in crops if crop not in ["Vegetables"]]

    crops = list(dict.fromkeys(crops))

    if not crops:
        crops = ["Millets", "Pulses", "Locally suitable vegetables (verify first)"]

    return ", ".join(crops)


def fertilizer_guidance(ph, soil):
    advice = []

    if ph < 5.5:
        advice.append(
            "Soil is acidic. Test lime requirement before applying agricultural lime."
        )
    elif ph > 7.5:
        advice.append(
            "Soil is alkaline. Test soil nutrients before selecting any amendment."
        )
    else:
        advice.append(
            "The pH is near the range suitable for many crops. Check soil nutrients."
        )

    if soil == "Sandy":
        advice.append(
            "Sandy soils may need split fertilizer applications and organic matter."
        )
    elif soil == "Clay":
        advice.append(
            "Avoid overwatering clay soil. Base fertilizer application on soil testing."
        )
    elif soil == "Laterite":
        advice.append(
            "Laterite soils may need nutrient management based on a laboratory soil test."
        )

    advice.append(
        "Use a soil-test-based NPK recommendation. Do not apply fertilizer blindly."
    )

    return " ".join(advice)


def get_json(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "AgroFutureSchoolProject/1.0"}
    )

    with urllib.request.urlopen(req, timeout=12) as response:
        return json.loads(response.read().decode("utf-8"))


@app.route("/")
def home():
    return render_template_string(HTML, result=None, weather=None,
                                  weather_error=None)


@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        ph = float(request.form["ph"])
        temperature = float(request.form["temperature"])
        humidity = float(request.form["humidity"])
        rainfall = float(request.form["rainfall"])

        if not 0 <= ph <= 14:
            raise ValueError("Soil pH must be between 0 and 14.")

        if not -10 <= temperature <= 60:
            raise ValueError("Enter a valid temperature.")

        if not 0 <= humidity <= 100:
            raise ValueError("Humidity must be between 0 and 100.")

        if not 0 <= rainfall <= 10000:
            raise ValueError("Enter a valid rainfall value.")

        soil = request.form["soil"]
        water = request.form["water"]

        result = {
            "ph": ph,
            "ph_text": ph_description(ph),
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall,
            "soil": soil,
            "water": water,
            "crops": recommend_crops(
                ph, temperature, humidity, rainfall, soil, water
            ),
            "fertilizer": fertilizer_guidance(ph, soil)
        }

        return render_template_string(
            HTML, result=result, weather=None, weather_error=None
        )

    except (ValueError, KeyError):
        return "Invalid input. Please check the values and try again.", 400


@app.route("/weather", methods=["POST"])
def weather():
    location = request.form.get("location", "").strip()

    if not location:
        return render_template_string(
            HTML, result=None, weather=None,
            weather_error="Please enter a city or town."
        )

    try:
        geo_url = (
            "https://geocoding-api.open-meteo.com/v1/search?"
            "name=" + urllib.parse.quote(location) +
            "&count=1&language=en&format=json"
        )

        geo = get_json(geo_url)
        places = geo.get("results", [])

        if not places:
            raise ValueError("Location not found. Check the spelling.")

        place = places[0]
        latitude = place["latitude"]
        longitude = place["longitude"]

        weather_url = (
            "https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}"
            "&current=temperature_2m,relative_humidity_2m,"
            "wind_speed_10m,weather_code"
        )

        data = get_json(weather_url)
        current = data["current"]

        code = current.get("weather_code", 0)

        if code == 0:
            condition = "Clear sky"
        elif code in [1, 2, 3]:
            condition = "Mainly clear, partly cloudy or overcast"
        elif code in [45, 48]:
            condition = "Fog"
        elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
            condition = "Rain or drizzle"
        elif code in [71, 73, 75, 85, 86]:
            condition = "Snow"
        elif code in [95, 96, 99]:
            condition = "Thunderstorm"
        else:
            condition = "Variable weather"

        weather_data = {
            "location": place["name"],
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "wind": current["wind_speed_10m"],
            "condition": condition
        }

        return render_template_string(
            HTML, result=None, weather=weather_data,
            weather_error=None
        )

    except Exception as error:
        return render_template_string(
            HTML, result=None, weather=None,
            weather_error=(
                "Weather lookup failed: " + str(error) +
                ". Check your internet connection and try again."
            )
        )


if __name__ == "__main__":
    import urllib.parse
    app.run(debug=True)