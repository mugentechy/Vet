from flask import request, jsonify, Blueprint, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import googlemaps
users = Blueprint('users', __name__)




gmaps = googlemaps.Client(key='AIzaSyA1MIEXY2hOk955M59Oqkb2oAaYmHm2Un0&callback=initMap')
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
        {'name': 'Jakaranda Veterinary Clinic & Surgery', 'location': {'lat': -1.2673401741777748, 'lng': 36.80009452723776}, 'address': 'Nairobi, Kenya'},
        {'name': 'Noble Veterinary Surgeons', 'location': {'lat': -1.256432359420563, 'lng': 36.78594549110323}, 'address': 'Nairobi, Kenya'},
        {'name': 'Westlands Paws Veterinary Clinic', 'location': {'lat': -1.2629667797925608, 'lng': 36.805681537817996}, 'address': 'Nairobi, Kenya'},
        
         {'name': 'Sarit Vet Clinic', 'location': {'lat': -1.2605640990461553,  'lng': 36.80216229547738}, 'address': 'Nairobi, Kenya'},
        {'name': 'Sarat Shah Veterinary Clinic', 'location': {'lat': -1.2604782635136045, 'lng':  36.800703117370254}, 'address': 'Nairobi, Kenya'},
        {'name': 'Veterinary Dr. Sura', 'location': {'lat': -1.2629612678396978, 'lng':  36.78538885528098}, 'address': 'Nairobi, Kenya'},
     

        {'name': 'St Austins Rd Veterinary Clinic', 'location': {'lat': -1.281894467479835,   'lng': 36.76673925492056}, 'address': 'Nairobi, Kenya'},
        {'name': 'Davis and Ghalay Veterinary Clinic', 'location': {'lat': -1.2667722639331507,  'lng':  36.80497331911033}, 'address': 'Nairobi, Kenya'},
    


    ]
    
    location = request.form.get('address')
    print(f"Location: {location}")
    
    if not location:
        return render_template('index.html', message='Please provide a location')
    
    # Render a template with the search results
    return render_template('location.html', veterinarians=veterinarians, location=location)
