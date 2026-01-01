from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'


# Inject 'user' and robust date formatting filter into all templates
@app.template_filter('datefmt')
def datefmt(value, fmt='%a, %d %b %Y'):
    from datetime import datetime
    if isinstance(value, datetime):
        return value.strftime(fmt)
    return ''

@app.context_processor
def inject_user():
    user = session.get('user')
    return dict(user=user)

# API configuration
AUTH_API = os.getenv('AUTH_API', 'http://auth-service:8001')
FLIGHT_API = os.getenv('FLIGHT_API', 'http://flight-service:8002')
BOOKING_API = os.getenv('BOOKING_API', 'http://booking-service:8002')

# Helper functions
def get_token():
    """Get JWT token from session"""
    return session.get('token')

def get_auth_header():
    """Get authorization header with token"""
    token = get_token()
    if token:
        return {'Authorization': f'Bearer {token}'}
    return {}

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Flight search page"""
    origin_raw = request.values.get('origin') or request.values.get('Origin')
    destination_raw = request.values.get('destination') or request.values.get('Destination')
    depart_date = request.values.get('depart_date') or request.values.get('DepartDate')
    return_date = request.values.get('return_date') or request.values.get('ReturnDate')
    debug_api_text = None
    flights = None
    # Helper to convert code to city name (simple mapping, expand as needed)
    def code_to_city(code):
        mapping = {
            'del': 'Delhi',
            'bom': 'Mumbai',
            'blr': 'Bangalore',
            'ccu': 'Kolkata',
            'maa': 'Chennai',
            # Add more as needed
        }
        return mapping.get(code.lower(), code.upper() if code else '')
    class Place:
        def __init__(self, code):
            self.code = code.upper() if code else ''
            self.city = code_to_city(code) if code else ''
    origin = Place(origin_raw) if origin_raw else None
    destination = Place(destination_raw) if destination_raw else None
    # Parse depart_date and return_date as datetime objects if present
    from datetime import datetime
    def parse_date(date_str):
        if date_str:
            try:
                return datetime.strptime(date_str, '%Y-%m-%d')
            except Exception:
                return None
        return None
    depart_date_obj = parse_date(depart_date)
    return_date_obj = parse_date(return_date)
    # If any search params are present, call the API
    if origin or destination or depart_date:
        try:
            params = {}
            if origin:
                params['origin__code__icontains'] = origin
            if destination:
                params['destination__code__icontains'] = destination
            response = requests.get(
                f'{FLIGHT_API}/api/flights/flights/',
                params=params,
                headers=get_auth_header(),
                timeout=5
            )
            debug_api_text = response.text
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    flights = data
                elif isinstance(data, dict):
                    flights = data.get('flights', data.get('results', []))
                else:
                    flights = []
            else:
                flights = []
        except Exception as e:
            debug_api_text = str(e)
            flights = []
    return render_template('search.html', flights=flights, origin=origin, destination=destination, depart_date=depart_date_obj, return_date=return_date_obj, debug_api_text=debug_api_text)

@app.route('/book/<int:flight_id>', methods=['GET', 'POST'])
def book(flight_id):
    """Flight booking page"""
    if not get_token():
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        passenger_name = request.form.get('passenger_name')
        seat_class = request.form.get('class', 'economy')
        
        try:
            response = requests.post(
                f'{BOOKING_API}/api/bookings/create/',
                json={
                    'flight_id': flight_id,
                    'passenger_name': passenger_name,
                    'class': seat_class
                },
                headers=get_auth_header(),
                timeout=5
            )
            
            if response.status_code == 201:
                return redirect(url_for('bookings'))
            else:
                error = response.json().get('error', 'Booking failed')
                return render_template('book.html', flight_id=flight_id, error=error)
        except Exception as e:
            return render_template('book.html', flight_id=flight_id, error=str(e))
    
    return render_template('book.html', flight_id=flight_id)

@app.route('/bookings')
def bookings():
    """User bookings page"""
    if not get_token():
        return redirect(url_for('login'))
    
    try:
        response = requests.get(
            f'{BOOKING_API}/api/bookings/bookings/',
            headers=get_auth_header(),
            timeout=5
        )
        
        if response.status_code == 200:
            bookings_data = response.json().get('results', [])
            return render_template('bookings.html', bookings=bookings_data)
        else:
            return render_template('bookings.html', error='Failed to fetch bookings')
    except Exception as e:
        return render_template('bookings.html', error=str(e))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            response = requests.post(
                f'{AUTH_API}/api/auth/login/',
                json={'username': username, 'password': password},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                session['token'] = data.get('token')
                session['username'] = username
                return redirect(url_for('index'))
            else:
                error = response.json().get('error', 'Login failed')
                return render_template('login.html', error=error)
        except Exception as e:
            return render_template('login.html', error=f'Error: {str(e)}')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email', '')
        
        try:
            response = requests.post(
                f'{AUTH_API}/api/auth/register/',
                json={
                    'username': username,
                    'password': password,
                    'email': email
                },
                timeout=5
            )
            
            if response.status_code == 201:
                # Auto-login after registration
                return redirect(url_for('login'))
            else:
                error = response.json().get('error', 'Registration failed')
                return render_template('register.html', error=error)
        except Exception as e:
            return render_template('register.html', error=f'Error: {str(e)}')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/user')
def api_user():
    """Get current user info"""
    try:
        response = requests.get(
            f'{AUTH_API}/api/auth/me/',
            headers=get_auth_header(),
            timeout=5
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/flights/search')
def api_flights_search():
    """API endpoint for flight search"""
    try:
        origin = request.args.get('origin')
        destination = request.args.get('destination')
        
        params = {'limit': 50}
        if origin:
            params['origin__code__icontains'] = origin
        if destination:
            params['destination__code__icontains'] = destination
        
        response = requests.get(
            f'{FLIGHT_API}/api/flights/flights/',
            params=params,
            headers=get_auth_header(),
            timeout=5
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
