from flask import request, jsonify, Blueprint, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import requests


users = Blueprint('users', __name__)




@users.route('/addusers')
def addusers():
    return render_template('register.html')

@users.route('/login')
def login():
    return render_template('login.html')


@users.route('/')
def index():
    return render_template('index.html')



@users.route('/nearby')
def nearby():
    return render_template('nearby.html')


def get_nearby_veterinarians(lat, lon):
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    node(around:5000, {lat}, {lon})["amenity"="veterinary"];
    out;
    """
    response = requests.get(overpass_url, params={'data': query})
    data = response.json()
    return data['elements'] if 'elements' in data else []

@users.route('/location', methods=['GET', 'POST'])
def location():
    places = []
    lat = None
    lon = None

    if request.method == 'POST':
        address = request.form.get('address')
        # You can use a geocoding API here to convert 'address' to lat/lng if needed

        # For demonstration, fetch user's geolocation
        lat = request.form.get('latitude')
        lon = request.form.get('longitude')

        # Fetch veterinarians near the location
        if lat and lon:
            places = get_nearby_veterinarians(lat, lon)

    return render_template('location.html', places=places, lat=lat, lon=lon)


@users.route('/logout', methods=['POST'])
def logout():
    # Handle logout logic here (clear session, etc.)
    return redirect(url_for('index'))



@users.route('/search_veterinarians', methods=['POST'])
def search_veterinarians():
    # Hardcoded list of veterinarians in Kenya
    veterinarians = [
        {'name': 'Vet Aid Machakos', 'location': {'lat': -1.5083533597174845,  'lng': 37.27112329964676}, 'address': 'Machakos, Kenya'},
        {'name': 'Nairobi Veterinary Centre (Machakos Branch)', 'location': {'lat': -1.5166095231242784, 'lng':  37.27131898756945}, 'address': 'Machakos, Kenya'},
        {'name': 'Briggits Veterinary Clinic and Services Machakos (Ambulatory)', 'location': {'lat': -1.5028475056821828,  'lng': 37.275181977647776}, 'address': 'Machakos, Kenya'},
        
         {'name': 'Lukenya Agro~Vet Supplies Ltd', 'location': {'lat': -1.5248744153640412, 'lng': 37.278212485500624 }, 'address': 'Machakos, Kenya'},
        {'name': 'Machakos Vet Supplies', 'location': {'lat': -1.450822215515419,  'lng':  37.2574066968316 }, 'address': 'Machakos, Kenya'},
  


    ]
    
    location = request.form.get('address')
    print(f"Location: {location}")
    
    if not location:
        return render_template('index.html', message='Please provide a location')
    
    # Render a template with the search results
    return render_template('location.html', veterinarians=veterinarians, location=location)
