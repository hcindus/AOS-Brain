#!/usr/bin/env python3
"""
Build an interactive North America service-areas map for psdepot.com.
Generates /var/www/psdepot.com/service-areas-map.html
Uses self-hosted Leaflet (assets/leaflet/) to respect the site CSP.
"""
import json, os

OUT = "/var/www/psdepot.com/service-areas-map.html"

# ---- Countries (anchor markers) ----
COUNTRIES = [
    ("United States", 39.8, -98.6, "us"),
    ("Canada", 56.1, -106.3, "ca"),
    ("México", 23.6, -102.5, "mx"),
]

# ---- US States (name, lat, lng) ----
US_STATES = [
    ("Alabama", 32.8, -86.8), ("Alaska", 64.0, -152.0), ("Arizona", 34.3, -111.7),
    ("Arkansas", 34.9, -92.4), ("California", 37.2, -119.5), ("Colorado", 39.0, -105.5),
    ("Connecticut", 41.6, -72.7), ("Delaware", 39.0, -75.5), ("Florida", 28.6, -82.4),
    ("Georgia", 32.6, -83.4), ("Hawaii", 20.5, -157.5), ("Idaho", 44.4, -114.4),
    ("Illinois", 40.0, -89.0), ("Indiana", 39.9, -86.2), ("Iowa", 42.0, -93.5),
    ("Kansas", 38.5, -98.3), ("Kentucky", 37.5, -85.3), ("Louisiana", 31.1, -92.0),
    ("Maine", 45.4, -69.0), ("Maryland", 39.0, -76.8), ("Massachusetts", 42.3, -71.8),
    ("Michigan", 44.3, -85.4), ("Minnesota", 46.3, -94.3), ("Mississippi", 32.7, -89.7),
    ("Missouri", 38.5, -92.5), ("Montana", 47.0, -110.0), ("Nebraska", 41.5, -99.8),
    ("Nevada", 39.3, -116.6), ("New Hampshire", 43.7, -71.6), ("New Jersey", 40.2, -74.7),
    ("New Mexico", 34.4, -106.1), ("New York", 43.0, -75.5), ("North Carolina", 35.5, -79.4),
    ("North Dakota", 47.5, -100.5), ("Ohio", 40.3, -82.7), ("Oklahoma", 35.5, -97.5),
    ("Oregon", 43.9, -120.6), ("Pennsylvania", 40.9, -77.8), ("Rhode Island", 41.6, -71.5),
    ("South Carolina", 33.9, -80.9), ("South Dakota", 44.4, -100.2), ("Tennessee", 35.8, -86.0),
    ("Texas", 31.5, -99.5), ("Utah", 39.3, -111.7), ("Vermont", 44.0, -72.7),
    ("Virginia", 37.5, -78.5), ("Washington", 47.4, -121.5), ("West Virginia", 38.6, -80.7),
    ("Wisconsin", 44.6, -89.8), ("Wyoming", 42.9, -107.5), ("Washington DC", 38.9, -77.0),
]

# ---- US Cities (name, lat, lng) ----
US_CITIES = [
    ("Albuquerque", 35.1, -106.6), ("Anaheim", 33.8, -117.9), ("Arlington", 32.7, -97.1),
    ("Atlanta", 33.7, -84.4), ("Austin", 30.3, -97.7), ("Bakersfield", 35.4, -119.0),
    ("Baltimore", 39.3, -76.6), ("Bay Area", 37.8, -122.3), ("Boston", 42.4, -71.1),
    ("Charlotte", 35.2, -80.8), ("Chicago", 41.9, -87.6), ("Colorado Springs", 38.8, -104.8),
    ("Columbus", 40.0, -83.0), ("Dallas", 32.8, -96.8), ("Denver", 39.7, -105.0),
    ("Detroit", 42.3, -83.0), ("El Paso", 31.8, -106.5), ("Fort Worth", 32.8, -97.3),
    ("Fresno", 36.7, -119.8), ("Houston", 29.8, -95.4), ("Indianapolis", 39.8, -86.2),
    ("Jacksonville", 30.3, -81.7), ("Kansas City", 39.1, -94.6), ("Las Vegas", 36.2, -115.1),
    ("Long Beach", 33.8, -118.2), ("Los Angeles", 34.05, -118.24), ("Louisville", 38.3, -85.8),
    ("Mesa", 33.4, -111.8), ("Miami", 25.8, -80.2), ("Milwaukee", 43.0, -87.9),
    ("Minneapolis", 45.0, -93.3), ("Nashville", 36.2, -86.8), ("New Orleans", 30.0, -90.1),
    ("New York City", 40.7, -74.0), ("Oakland", 37.8, -122.3), ("Oklahoma City", 35.5, -97.5),
    ("Omaha", 41.3, -95.9), ("Philadelphia", 40.0, -75.2), ("Phoenix", 33.4, -112.1),
    ("Portland", 45.5, -122.7), ("Raleigh", 35.8, -78.6), ("Sacramento", 38.6, -121.5),
    ("San Antonio", 29.4, -98.5), ("San Diego", 32.7, -117.2), ("San Francisco", 37.8, -122.4),
    ("San Jose", 37.3, -121.9), ("Seattle", 47.6, -122.3), ("Tucson", 32.2, -110.9),
    ("Tulsa", 36.2, -95.9), ("Virginia Beach", 36.9, -76.0), ("Wichita", 37.7, -97.3),
]

# ---- Canada provinces/territories ----
CA_PROVINCES = [
    ("Alberta", 54.5, -115.0), ("British Columbia", 53.7, -124.5), ("Manitoba", 54.5, -97.5),
    ("New Brunswick", 46.5, -66.5), ("Newfoundland & Labrador", 53.1, -60.0),
    ("Northwest Territories", 64.5, -118.0), ("Nova Scotia", 45.0, -63.0),
    ("Nunavut", 68.0, -90.0), ("Ontario", 50.0, -85.0), ("Prince Edward Island", 46.3, -63.1),
    ("Quebec", 52.0, -72.0), ("Saskatchewan", 54.0, -106.0), ("Yukon", 63.0, -136.0),
]

# ---- Mexico states ----
MX_STATES = [
    ("Aguascalientes", 22.0, -102.4), ("Baja California", 30.0, -115.0),
    ("Baja California Sur", 25.5, -111.5), ("Campeche", 18.8, -90.5), ("Chiapas", 16.5, -92.5),
    ("Chihuahua", 28.6, -106.0), ("Ciudad de México", 19.4, -99.1), ("Coahuila", 27.0, -102.0),
    ("Colima", 19.1, -103.9), ("Durango", 24.8, -104.8), ("Guanajuato", 20.9, -101.0),
    ("Guerrero", 17.6, -99.8), ("Hidalgo", 20.4, -98.7), ("Jalisco", 20.7, -103.3),
    ("Michoacán", 19.2, -101.9), ("Morelos", 18.7, -99.1), ("Nayarit", 22.0, -104.8),
    ("Nuevo León", 25.6, -99.7), ("Oaxaca", 17.0, -96.7), ("Puebla", 19.0, -97.8),
    ("Querétaro", 20.6, -100.0), ("Quintana Roo", 19.8, -88.0), ("Sinaloa", 25.0, -107.5),
    ("Sonora", 29.3, -110.7), ("Tabasco", 17.8, -92.6), ("Tamaulipas", 24.0, -98.7),
    ("Tlaxcala", 19.4, -98.2), ("Veracruz", 19.2, -96.1), ("Yucatán", 20.7, -89.1),
    ("Zacatecas", 23.0, -102.7),
]

def slug(name):
    s = name.lower()
    for a, b in [("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ñ", "n"), ("ü", "u")]:
        s = s.replace(a, b)
    s = s.replace(" & ", "-").replace(" ", "-")
    return s

def marker_js(name, lat, lng, url, kind):
    # kind: 'country', 'state', 'city'
    color = {"us": "#2563eb", "ca": "#dc2626", "mx": "#16a34a"}[kind] if kind in ("us","ca","mx") else None
    if kind == "country":
        return f'L.marker([{lat},{lng}], {{icon: countryIcon}}).bindPopup(`<b>{name}</b><br><a href="{url}">View services &rarr;</a>`).addTo(countriesLayer);'
    if kind == "state":
        return f'L.circleMarker([{lat},{lng}], {{radius:7, color:"#1e40af", weight:2, fillColor:"#2563eb", fillOpacity:0.85}}).bindPopup(`<b>{name}</b><br><a href="{url}">View &rarr;</a>`).addTo(statesLayer);'
    return f'L.circleMarker([{lat},{lng}], {{radius:5, color:"#7c3aed", weight:1.5, fillColor:"#8b5cf6", fillOpacity:0.9}}).bindPopup(`<b>{name}</b><br><a href="{url}">View &rarr;</a>`).addTo(citiesLayer);'

# Build URL helpers
def state_url(name, country):
    if country == "us":
        if name == "Washington DC": return "/washington-dc.html"
        return "/" + slug(name) + ".html"
    if country == "ca":
        mapping = {"Newfoundland & Labrador": "newfoundland-labrador", "Prince Edward Island": "prince-edward-island",
                   "British Columbia": "british-columbia", "Northwest Territories": "northwest-territories",
                   "New Brunswick": "new-brunswick", "Nova Scotia": "nova-scotia"}
        return "/" + mapping.get(name, slug(name)) + ".html"
    if country == "mx":
        mapping = {"Ciudad de México": "ciudad-de-mexico", "Nuevo León": "nuevo-leon",
                   "Baja California": "baja-california", "Baja California Sur": "baja-california-sur",
                   "Quintana Roo": "quintana-roo"}
        return "/" + mapping.get(name, slug(name)) + ".html"
    return "#"

def city_url(name):
    mapping = {
        "Bay Area": "bay-area-pos-supplies", "New York City": "new-york-city",
        "Kansas City": "kansas-city", "Los Angeles": "los-angeles", "San Francisco": "san-francisco",
        "San Jose": "san-jose", "El Paso": "el-paso", "Fort Worth": "fort-worth",
        "Las Vegas": "las-vegas", "New Orleans": "new-orleans", "San Antonio": "san-antonio",
        "San Diego": "san-diego", "Colorado Springs": "colorado-springs", "Oklahoma City": "oklahoma-city",
        "Long Beach": "long-beach-pos-supplies", "Virginia Beach": "virginia-beach",
    }
    return "/" + mapping.get(name, slug(name)) + ".html"

parts = []
# country markers (unused — built inline in HTML below)

# states
for name, lat, lng in US_STATES:
    parts.append(marker_js(name, lat, lng, state_url(name, "us"), "state"))
for name, lat, lng in CA_PROVINCES:
    parts.append(marker_js(name, lat, lng, state_url(name, "ca"), "state"))
for name, lat, lng in MX_STATES:
    parts.append(marker_js(name, lat, lng, state_url(name, "mx"), "state"))

# cities
for name, lat, lng in US_CITIES:
    parts.append(marker_js(name, lat, lng, city_url(name), "city"))

markers_js = "\n    ".join(parts)

# Custom icons via L.divIcon for countries (colored)
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Service Areas Map — Performance Supply Depot LLC</title>
<meta name="description" content="Interactive map of Performance Supply Depot's service areas across the United States, Canada, and México — states, provinces, and cities we serve.">
<link rel="canonical" href="https://psdepot.com/service-areas-map.html">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/leaflet/leaflet.css">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ height:100%; }}
  body {{ font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif; background:#0A1A2F; color:#fff; }}
  header {{ background:#0A1A2F; padding:14px 24px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; box-shadow:0 2px 6px rgba(0,0,0,0.3); position:relative; z-index:1000; }}
  header .logo {{ font-size:22px; font-weight:800; color:#fff; text-decoration:none; }}
  header .logo span {{ color:#63b3ed; }}
  header nav a {{ color:#bee3f8; text-decoration:none; font-weight:600; font-size:14px; margin-left:20px; }}
  header nav a:hover {{ color:#fff; }}
  #map {{ position:absolute; top:60px; bottom:0; left:0; right:0; background:#0A1A2F; }}
  .legend {{ position:absolute; bottom:20px; left:20px; background:rgba(10,26,47,0.92); color:#fff; padding:12px 16px; border-radius:10px; font-size:13px; z-index:1000; box-shadow:0 4px 12px rgba(0,0,0,0.4); }}
  .legend .row {{ display:flex; align-items:center; margin:5px 0; }}
  .legend .dot {{ width:12px; height:12px; border-radius:50%; margin-right:8px; display:inline-block; }}
  .leaflet-popup-content-wrapper {{ background:#0A1A2F; color:#fff; border-radius:10px; }}
  .leaflet-popup-content a {{ color:#63b3ed; font-weight:600; }}
  .leaflet-popup-tip {{ background:#0A1A2F; }}
  @media (max-width:600px) {{ header nav a {{ margin-left:10px; font-size:12px; }} #map {{ top:104px; }} }}
</style>
</head>
<body>
<header>
  <a href="/" class="logo">Performance<span>Supply</span>Depot</a>
  <nav>
    <a href="/">Home</a>
    <a href="/locations.html">Service Areas</a>
    <a href="/contact.html">Contact</a>
  </nav>
</header>
<div id="map"></div>
<div class="legend">
  <div class="row"><span class="dot" style="background:#2563eb;"></span> U.S. States</div>
  <div class="row"><span class="dot" style="background:#8b5cf6;"></span> U.S. Cities</div>
  <div class="row"><span class="dot" style="background:#dc2626;"></span> Canada</div>
  <div class="row"><span class="dot" style="background:#16a34a;"></span> México</div>
</div>
<script src="/assets/leaflet/leaflet.js"></script>
<script>
var map = L.map('map').setView([45, -100], 4);
L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
  maxZoom: 18,
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}}).addTo(map);

var countriesLayer = L.layerGroup().addTo(map);
var statesLayer = L.layerGroup().addTo(map);
var citiesLayer = L.layerGroup().addTo(map);

function countryIcon(color) {{
  return L.divIcon({{ html:'<div style="width:18px;height:18px;border-radius:50%;background:'+color+';border:3px solid #fff;box-shadow:0 0 8px rgba(0,0,0,0.5);"></div>', className:'', iconSize:[18,18], iconAnchor:[9,9] }});
}}
var usIcon = countryIcon('#2563eb');
var caIcon = countryIcon('#dc2626');
var mxIcon = countryIcon('#16a34a');

// Countries
L.marker([39.8, -98.6], {{icon: usIcon}}).bindPopup('<b>United States</b><br>50 states + 50 cities').addTo(countriesLayer);
L.marker([56.1, -106.3], {{icon: caIcon}}).bindPopup('<b>Canada</b><br>13 provinces &amp; territories').addTo(countriesLayer);
L.marker([23.6, -102.5], {{icon: mxIcon}}).bindPopup('<b>México</b><br>30 states').addTo(countriesLayer);

{markers_js}

var overlay = {{
  "Countries": countriesLayer,
  "States &amp; Provinces": statesLayer,
  "Cities": citiesLayer
}};
L.control.layers(null, overlay, {{ collapsed:false }}).addTo(map);
</script>
</body>
</html>
"""

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    f.write(html)

# count
total = len(US_STATES) + len(US_CITIES) + len(CA_PROVINCES) + len(MX_STATES) + len(COUNTRIES)
print(f"Wrote {OUT}")
print(f"Markers: {len(COUNTRIES)} countries, {len(US_STATES)} US states, {len(US_CITIES)} US cities, {len(CA_PROVINCES)} CA, {len(MX_STATES)} MX = {total} total")
