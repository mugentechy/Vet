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




@users.route('/find_veterinarians', methods=['GET'])
def find_veterinarians():
    lat = request.args.get('lat')
    lng = request.args.get('lng')

    if not lat or not lng:
        return jsonify({'error': 'Latitude and longitude are required'}), 400

    veterinarians = get_veterinarians_near(lat, lng)

    return jsonify({'veterinarians': veterinarians})

def get_veterinarians_near(lat, lng):
    # Example function to fetch veterinarians near given lat, lng using Overpass API
    overpass_url = f"https://overpass-api.de/api/interpreter?data=[out:json];node(around:5000,{lat},{lng})[amenity=veterinary];out;"
    try:
        response = requests.get(overpass_url)
        data = response.json()

        veterinarians = []
        for element in data.get('elements', []):
            name = element.get('tags', {}).get('name', 'Unknown')
            location = f"{element['lat']}, {element['lon']}"
            veterinarians.append({'name': name, 'location': location})

        return veterinarians
    except requests.exceptions.RequestException as e:
        print(f"Error fetching veterinarians data: {e}")
        return []



# Assuming your route is within a Blueprint named 'users'
@users.route('/search_veterinarians', methods=['GET'])
def search_veterinarians():
    # Retrieve location input from the query parameters
    location = request.args.get('location')
    print(location)
    
    if not location:
        # Handle case where location is not provided
        return render_template('index.html', message='Please provide a location')
    
    # Step 1: Geocoding using Nominatim API
    geo_data = geocode_location(location)
    
    if geo_data is None:
        # Handle case where geocoding fails
        return render_template('index.html', message='Location not found')
    
    # Extract latitude and longitude from geocoding response
    lat = geo_data['lat']
    lon = geo_data['lon']
    
    # Step 2: Query veterinarians using Overpass API
    veterinarians = query_veterinarians(lat, lon)
    
    # Render a template with the search results
    return render_template('location.html', veterinarians=veterinarians, location=location)

def geocode_location(location):
    # Geocoding API endpoint
    geocode_url = f'https://nominatim.openstreetmap.org/search.php?q={location}&format=json'
    
    try:
        response = requests.get(geocode_url)
        data = response.json()
        
        if data:
            # Return the first result (assuming it's the most relevant)
            return {
                'lat': data[0]['lat'],
                'lon': data[0]['lon']
            }
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching geocoding data: {e}")
        return None

def query_veterinarians(lat, lon):
    # Overpass API endpoint for querying veterinarians (amenities=vet)
    overpass_url = f'https://overpass-api.de/api/interpreter?data=[out:json];node(around:10000,{lat},{lon})[amenity=vet];out;'
    
    try:
        response = requests.get(overpass_url)
        data = response.json()
        
        if 'elements' in data:
            veterinarians = []
            for element in data['elements']:
                name = element.get('tags', {}).get('name', 'Unknown')
                location = f"{element['lat']}, {element['lon']}"
                veterinarians.append({'name': name, 'location': location})
            
            return veterinarians
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching veterinarians data: {e}")
        return []