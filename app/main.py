from crypt import methods
from curses import COLOR_CYAN
import os
import readline
import sys
import datetime
import logging
import datetime
import time
import glob
import re
import getpass
from flask import Flask, Response, redirect, session, abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user , current_user
from types import MethodDescriptorType
from flask import Flask, render_template, request, url_for , render_template_string , flash , jsonify, make_response
from flask_limiter import Limiter
from flask import send_file
from flask_limiter.util import get_remote_address
import folium
from folium import FeatureGroup, LayerControl, Map, Marker
from folium.plugins import HeatMap
import pandas as pd
import numpy as np
import pymysql
import csv
from colorama import init, Fore, Back, Style
import pathlib
import pipes
import config
import pdfkit
from pathlib import Path
from geopy.geocoders import Nominatim
import geopandas as gpd
import matplotlib.pyplot as plt  
import geopandas as gpd
from werkzeug.utils import secure_filename
import os
from pyproj import Proj, transform
from haversine import haversine, Unit
from tempfile import NamedTemporaryFile
import json
from folium.plugins import HeatMap
from obspy import read
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import datetime, timedelta
import io
import base64
import tempfile
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError
from shapely.geometry import Point, Polygon
import requests
import datetime
from sklearn.linear_model import LinearRegression
from flask_talisman import Talisman





plt.switch_backend('Agg')


app = Flask(__name__)
talisman = Talisman(app)


username = getpass.getuser()  # Get username of system


mytime = datetime.datetime.now()
hour = mytime.hour
minute = mytime.minute
localtime = f"{hour}:{minute}"


appdir = os.path.join(f"/home/{username}/Apps/KYGnus_Map")
os.makedirs(appdir, exist_ok=True)



logdir = os.path.join(f"/home/{username}/Apps/KYGnus_Map/LOG")
os.makedirs(logdir, exist_ok=True)


""" Define Basic Configs of Logging.This Bsic Configs have Time and
Message and FileMode"""
logging.basicConfig(filename=f"{logdir}/KYGnus_Map.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()  # Create Logger of Logging System

logger.setLevel(logging.DEBUG)  # Set Level For Logger


logger.info(Fore.GREEN + """

██╗  ██╗██╗   ██╗ ██████╗ ███╗   ██╗██╗   ██╗███████╗        ███╗   ███╗ █████╗ ██████╗
██║ ██╔╝╚██╗ ██╔╝██╔════╝ ████╗  ██║██║   ██║██╔════╝        ████╗ ████║██╔══██╗██╔══██╗
█████╔╝  ╚████╔╝ ██║  ███╗██╔██╗ ██║██║   ██║███████╗        ██╔████╔██║███████║██████╔╝
██╔═██╗   ╚██╔╝  ██║   ██║██║╚██╗██║██║   ██║╚════██║        ██║╚██╔╝██║██╔══██║██╔═══╝  
██║  ██╗   ██║   ╚██████╔╝██║ ╚████║╚██████╔╝███████║███████╗██║ ╚═╝ ██║██║  ██║██║          
╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝      



            """)








# Create Directory For Filed in App Directory
""" make Directory For Files in user Direcory If Exist pass it"""
Filespath = os.path.join(f"/home/{username}/Apps/KYGnus_Map/Files")
os.makedirs(Filespath, exist_ok=True)
logger.info(Fore.YELLOW +
            f"[ INFO ] Making Directory for Files in /home/{username}/Apps/KYGnus_Map")


""" make Directory For  Excel Files in user Direcory If Exist pass it"""
excel_files_path = os.path.join(f"/home/{username}/Apps/KYGnus_Map/Files/Excel")
os.makedirs(excel_files_path, exist_ok=True)
logger.info(Fore.YELLOW +
            f"[ INFO ] Making Directory for Excel Files in /home/{username}/Apps/KYGnus_Map/Files")


""" make Directory For CIrcular Markger Excel Files in user Direcory If Exist pass it"""
excel_marker_files_path = os.path.join(
    f"/home/{username}/Apps/KYGnus_Map/Files/Excel/marker")
os.makedirs(excel_marker_files_path, exist_ok=True)
logger.info(Fore.YELLOW +
            f"[ INFO ] Making xDirectory for Excel Files in /home/{username}/Apps/KYGnus_Map/Files")

""" make Directory For circular marker Excel Files in user Direcory If Exist pass it"""
excel_cmarker_files_path = os.path.join(
    f"/home/{username}/Apps/KYGnus_Map/Files/Excel/circular")
os.makedirs(excel_cmarker_files_path, exist_ok=True)
logger.info(Fore.YELLOW +
            f"[ INFO ] Making Directory for Excel Files in /home/{username}/Apps/KYGnus_Map/Files")


""" make Directory For doc Files in user Direcory If Exist pass it"""
upload_path = os.path.join(f"/home/{username}/Apps/KYGnus_Map/Files/Uploads")
os.makedirs(upload_path, exist_ok=True)
logger.info(Fore.YELLOW +
            f"[ INFO ] Making Directory for Uploaded Files in /home/{username}/Apps/KYGnus_Map/Files")



















# check Number of Files

def number_of_files():
    files = glob.glob(f"{Filespath}/**/*.*", recursive=True)
    return len(files)

def number_of_excel_files():
    files = glob.glob(f"{excel_files_path}/**/*.csv", recursive=True)
    return len(files)







allowed_formats = {"csv" , "txt"}  # allowed file types


# Secure File name
def check_files(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in allowed_formats




# Flask limiter
""" Limit the number of requests to the server """
limiter = Limiter(
    app,
    # key_func=get_remote_address,
    default_limits=["50 per day", "10 per hour"]
)

app.config.update(
    SECRET_KEY=config.SECRET_KEY
)

# Flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Configure rate limiting


# Set up logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "%d" % (self.id)

@login_manager.user_loader
def load_user(userid):
    return User(userid)


@app.route("/")
@login_required
def index():
    locations = [
        {"name": "New York", "lat": 40.7128, "lon": -74.0060},
        {"name": "London", "lat": 51.5074, "lon": -0.1278},
        {"name": "Paris", "lat": 48.8566, "lon": 2.3522},
        {"name": "Tokyo", "lat": 35.6895, "lon": 139.6917},
        {"name": "Sydney", "lat": -33.8688, "lon": 151.2093},
        {"name": "Dubai", "lat": 25.2048, "lon": 55.2708},
        {"name": "Rome", "lat": 41.9028, "lon": 12.4964},
        {"name": "Hong Kong", "lat": 22.3193, "lon": 114.1694},
        {"name": "Berlin", "lat": 52.5200, "lon": 13.4050},
        {"name": "Istanbul", "lat": 41.0082, "lon": 28.9784},
    ]
    # Create a Folium map centered on the first location
    center_lat, center_lon = locations[0]["lat"], locations[0]["lon"]
    map = folium.Map(location=[center_lat, center_lon], zoom_start=2)

    # Add markers for each location
    for loc in locations:
        name = loc["name"]
        lat, lon = loc["lat"], loc["lon"]
        folium.Marker([lat, lon], popup=name).add_to(map)

    # Save the map as an HTML string
    map_html = map._repr_html_()
    return render_template(
        "index.html",
        username=current_user.id,
        number_of_files=number_of_files(),
        number_of_excel_files=number_of_excel_files() , 
        map_html=map_html ,
        localtime = localtime

    )

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def loggin():
    username = request.form["username"]
    password = request.form["password"]
    if username == config.USERNAME and password == config.PASSWORD:
        logger.warning(Fore.RED + "User tried to login")
        user = User(username)
        login_user(user)
        return redirect('/')
    else:
        logger.warning(Fore.RED + "[Warning] Login failed. System redirecting user to /login")
        return redirect("/login")



@app.route("/logout")
@login_required
def logout():
    logout_user()
    logger.info(Fore.YELLOW + "[INFO] User logged out")
    return Response('<p>Logged out</p>')



@app.errorhandler(401)
def unauthorized(e):
    logger.warning(Fore.RED + "[Warning] 401 Error")
    return Response('<center><h1>Login Failed</h1></center>')



@ app.route("/createmap")
def createmap():
    logger.info(Fore.CYAN + "[ Info ] Loading Create Map Page")
    return render_template("createmap.html" , username = username)


""" This Route Create Route For main Map Without Any Marks
This Will be Get Lat and Long and Create Map in That Locations"""


@ app.route("/createmap/createmainmap")
def create_main_map():
    logger.info(Fore.CYAN + "[ Info ] Loading Create Map Page")
    return render_template("main_map_creator.html" , username = username)


# TODO : create Template For main Map
""" This Route create main Map and save map in templates Directory
This is Basic map with No Marker"""


@ app.route("/createmap/createmainmap", methods=["POST"])
def main_map():
    lat = request.form["lat"]
    lan = request.form["lan"]
    logger.info("lat: " + lat + " lan: " + lan)
    try:
        map = folium.Map(location=[lat, lan], zoom_start=14)
        logger.info(Fore.CYAN + "User Load Main map")
        map.save("./templates/maps/mainmap.html")
        logger.info(Fore.CYAN + "[ Info ] User Save Map")
        return render_template("maps/mainmap.html")
    except:
        return Response("<html><body style='background-color:white;'><center ><h1 style='color:red;'> Can't Process Excel File !!!</h1><h2> Please Check File Type and Format Or Sure This File Design is True</center></html></body>")


# marker
""" This Route Create Map and insert Marker in File.
This is Basic map with Marker and Save File in templates Directory in templates/maps"""


@ app.route("/createmap/map/marker", methods=["POST"])
def marker():
    """ This route get excel File and insert marker on map"""
    csv_file = request.files["csv_file"]
    zoom = request.form["zoom_start"]
    if check_files(csv_file.filename):
        print(check_files(csv_file.filename))
        logger.info(
            Fore.YELLOW + "[ Info ] check File Format for Security Reasons")
        try:
            locations = pd.read_csv(csv_file)
            main_locations = locations[["Latitude", "Longitude", "Name"]]
            map = folium.Map(location=[main_locations.Latitude.mean(
            ), main_locations.Longitude.mean()], zoom_start=zoom, control_scale=True)
            for index, location_info in main_locations.iterrows():
                if folium.Marker([location_info["Latitude"], location_info["Longitude"]], popup=location_info["Name"]).add_to(map):
                    map.save(f"./templates/maps/{csv_file.filename}.html")
                    print("map Saved succesfully")
            goal_path = os.path.join(
                excel_marker_files_path, csv_file.filename)
            csv_file.save(goal_path)  # the file save in Goal path
            return redirect("/createmap")
        except:
            return Response("<html><body style='background-color:white;'><center ><h1 style='color:red;'> Can't Process Excel File !!!</h1><h2> Please Check File Type and Format Or Sure This File Design is True</center></html></body>")


# circular marker
""" This Route Make marker in Circular Mode and Save Map in template/maps Directory"""


@ app.route("/createmap/map/circular-maker",  methods=["POST"])
def cmarker():
    """ at this route and Function  make curcular maker to map.first Get excwl File and
    make sure this File is Safe and after that save it in excelpath"""
    csv_file = request.files["csv_file"]
    zoom = request.form["zoom_start"]
    if check_files(csv_file.filename):
        print(check_files(csv_file.filename))
        logger.info(
            Fore.YELLOW + "[ Info ] check File Format for Security Reasons")
        try:
            locations = pd.read_csv(csv_file)
            main_locations = locations[["Latitude", "Longitude", "Name"]]
            map = folium.Map(location=[main_locations.Latitude.mean(
            ), main_locations.Longitude.mean()], zoom_start=zoom, control_scale=True)
            for index, location_info in main_locations.iterrows():
                if folium.CircleMarker([location_info["Latitude"], location_info["Longitude"]], popup=location_info["Name"]).add_to(map):
                    map.save(
                        f"./templates/maps/{csv_file.filename}_circular.html")
                    print("map Saved succesfully")
            goal_path = os.path.join(
                excel_marker_files_path, csv_file.filename)
            csv_file.save(goal_path)  # the file save in Goal path
            return redirect("/createmap")
        except:
            return Response("<html><body style='background-color:white;'><center ><h1 style='color:red;'> Can't Process Excel File !!!</h1><h2> Please Check File Type and Format Or Sure This File Design is True</center></html></body>")



@app.route("/tools")
def addresses_into_coordinates_get():
    return render_template("tools.html", Number_of_Files=number_of_files(),
                               number_of_excel_file=number_of_excel_files(), username = username)



@app.route("/tools/addresses_into_coordinates", methods=["GET", "POST"])
def addresses_into_coordinates():
    coordinates = None
    error_message = None
    
    if request.method == 'POST':
        address = request.form['address']
        geolocator = Nominatim(user_agent="your_unique_app_name")
        
        try:
            location = geolocator.geocode(address)
            if location:
                coordinates = (location.latitude, location.longitude)
            else:
                error_message = "Could not geocode the provided address."
        except GeocoderServiceError as e:
            error_message = str(e)
    
    return render_template("tools.html", coordinates=coordinates, error_message=error_message)





@app.route("/tools/geopands")
def geopands():
    return render_template("tools.html")


@app.route("/tools/geopands", methods=["GET", "POST"])
def plot_world():
    plot_url = None
    if request.method == 'POST':
        try:
            # Get user inputs
            country = request.form.get('country')
            coordinates = request.form.get('coordinates')
            figsize = tuple(map(float, request.form.get('figsize', '10,6').split(',')))
            color = request.form.get('color', 'blue')
            alpha = float(request.form.get('alpha', '0.6'))

            # Load the dataset from local file
            data_path = os.path.join('data', 'ne_110m_admin_0_countries.shp')
            world = gpd.read_file(data_path)
            
            # Create the plot
            fig, ax = plt.subplots(1, 1, figsize=figsize)
            world.plot(ax=ax, color=color, alpha=alpha)

            # Highlight the specified country
            if country:
                country_data = world[world['NAME'].str.contains(country, case=False)]
                if not country_data.empty:
                    country_data.plot(ax=ax, color='red')

            # Highlight the specified coordinates
            if coordinates:
                lat, lon = map(float, coordinates.split(','))
                ax.plot(lon, lat, 'ro', markersize=10)  # Plot as a red dot

            # Save the plot to a file
            plot_path = 'static/world_plot.png'
            if not os.path.exists('static'):
                os.makedirs('static')
            plt.savefig(plot_path)
            plt.close(fig)
            
            plot_url = plot_path
        except Exception as e:
            return f"An error occurred: {e}", 500






@app.route('/tools/shapely', methods=['GET', 'POST'])
def shapely_tools():
    if request.method == 'POST':
        point_data = request.form.get('point')
        polygon_data = request.form.get('polygon')

        try:
            # Parse the point data
            point_coords = tuple(map(float, point_data.split(',')))
            point = Point(point_coords)

            # Parse the polygon data
            polygon_coords = [tuple(map(float, coord.split(','))) for coord in polygon_data.split()]
            polygon = Polygon(polygon_coords)

            # Check if the point is within the polygon
            result = polygon.contains(point)

            return render_template('tools.html', point=point.wkt, polygon=polygon.wkt, result=result)
        except Exception as e:
            return f"An error occurred: {e}", 400

    return render_template('index.html')




## Harvesin

@app.route("/tools/harvesin")
def pyproj_get():
        return render_template("tools.html")



@app.route('/tools/haversine', methods=['GET', 'POST'])
def pyproj():
    if request.method == 'POST':
        try:
            lon1 = float(request.form['lon1'])
            lat1 = float(request.form['lat1'])
            lon2 = float(request.form['lon2'])
            lat2 = float(request.form['lat2'])

            point1 = (lat1, lon1)
            point2 = (lat2, lon2)

            distance = haversine(point1, point2, unit=Unit.KILOMETERS)

            return render_template('tools.html', 
                                   lon1=lon1, lat1=lat1, 
                                   lon2=lon2, lat2=lat2, 
                                   distance=distance)

        except ValueError as e:
            return render_template('tools.html', error=str(e))

    return render_template('404.html')
    




## Heat Map Creation

""" This Route Create HeatMap from Given Locations"""



@app.route("/heatmap")
def heatmap_get():
    return render_template("heatmap.html")




@app.route('/heatmap', methods=['POST'])
def heatmap_post():
    if request.method == 'POST':
        heat_data = []
        try:
            num_points = int(request.form['num_points'])
            for i in range(num_points):
                latitude = float(request.form[f'latitude_{i+1}'])
                longitude = float(request.form[f'longitude_{i+1}'])
                intensity = float(request.form[f'intensity_{i+1}'])
                heat_data.append([latitude, longitude, intensity])
            
            # Generate the heatmap
            heatmap_file = generate_heatmap(heat_data)

            # Return the heatmap file as a response
            return send_file(heatmap_file, as_attachment=True, download_name=f'{Filespath}/heatmap_data.html')

        except ValueError:
            return "Invalid input. Please enter numeric values."
    
    return render_template('heatmap.html')


def generate_heatmap(data):
    # Initialize the map centered around a central point
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Add heatmap layer
    HeatMap(data).add_to(m)

    # Save the map to a temporary file
    tmp_dir = tempfile.mkdtemp()
    heatmap_file = os.path.join(tmp_dir, "heatmap.html")
    m.save(heatmap_file)

    return heatmap_file












#



@app.route('/process_seismic')
def seismic():
    return render_template("geostatistics.html" , username = username)






@app.route('/process_seismic', methods=['POST'])
def process_seismic():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    
    try:
        file_path = os.path.join(upload_path, uploaded_file.filename)
        uploaded_file.save(file_path)

        # Read the seismic data file using ObsPy
        st = read(file_path)
        
        # Select the first trace in the stream
        tr = st[0]
        
        # Filter the data (e.g., bandpass filter between 0.1 and 10 Hz)
        tr.filter("bandpass", freqmin=0.1, freqmax=10.0)
        
        # Plot the filtered data
        plot_path = os.path.join(upload_path, 'filtered_seismic_data.png')
        tr.plot(outfile=plot_path)

        return send_file(plot_path, as_attachment=True)
    except Exception as e:
        flash(f'Error processing file: {str(e)}')
        return redirect(url_for('index'))










## Location Prediction

@app.route('/location_prediction')
def predict_loc():
    return render_template("predict_location.html" , username = username)



def read_csv(filename):
    positions = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            positions.append({
                "timestamp": row['timestamp'],
                "latitude": float(row['latitude']),
                "longitude": float(row['longitude'])
            })
    return positions

# Function to predict next position using Linear Regression
def predict_next_position(historical_positions):
    if len(historical_positions) < 2:
        return np.mean([pos["latitude"] for pos in historical_positions]), np.mean([pos["longitude"] for pos in historical_positions])
    
    timestamps = np.array(range(len(historical_positions))).reshape(-1, 1)
    latitudes = np.array([pos["latitude"] for pos in historical_positions])
    longitudes = np.array([pos["longitude"] for pos in historical_positions])

    lat_model = LinearRegression().fit(timestamps, latitudes)
    lon_model = LinearRegression().fit(timestamps, longitudes)

    next_timestamp = np.array([[len(historical_positions)]])

    next_latitude = lat_model.predict(next_timestamp)[0]
    next_longitude = lon_model.predict(next_timestamp)[0]

    return next_latitude, next_longitude

# Construct the absolute path to the CSV file
base_dir = os.path.abspath(os.path.dirname(__file__))
csv_file = os.path.join(base_dir, '..', 'Databases', 'positions-p.csv')

# Initialize with data from CSV file
historical_positions = read_csv(csv_file)


@app.route('/location_prediction', methods=['POST'])
def predict_locations():
    if request.method == 'POST':
        timestamp = request.form['timestamp']
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        
        new_position = {
            "timestamp": timestamp,
            "latitude": latitude,
            "longitude": longitude
        }
        historical_positions.append(new_position)
        predicted_latitude, predicted_longitude = predict_next_position(historical_positions)
        return render_template('predict_location.html', predicted_latitude=predicted_latitude, predicted_longitude=predicted_longitude)
    else:
        predicted_latitude = request.args.get('predicted_latitude')
        predicted_longitude = request.args.get('predicted_longitude')
        return render_template('predict_location.html', predicted_latitude=predicted_latitude, predicted_longitude=predicted_longitude)

















# TODO : create log template


@ app.route("/analyzer")
def analyzer():
    logger.info(Fore.YELLOW + "[ Info ]  Analyzer template Loaded")
    return render_template("analyzer.html" , username = username)

# Document Analyzer

# TODO : check Document File Type and Format and Extensions and Interior of File for Unwanted Data


def extract_map_info(file_path):
    map_info = []

    with open(file_path, 'r') as file:
        for line in file:
            # Assuming latitude and longitude are in the format "Lat: xx.xx, Lon: xx.xx"
            match = re.search(r'Lat: ([\d.-]+), Lon: ([\d.-]+)', line)
            if match:
                lat = float(match.group(1))
                lon = float(match.group(2))
                map_info.append({'latitude': lat, 'longitude': lon})
    
    return map_info



def extract_map_info(file_path):
    # Dummy function to simulate extracting map information from the text file
    # Replace this with actual logic
    with open(file_path, 'r') as f:
        content = f.read()
    # Example map_info extracted from file
    map_info = {
        "lines": content.split('\n')
    }
    return map_info

@app.route("/analyzer/text", methods=["POST"])
def post_document_analyzer():
    file = request.files['textfile']
    if file.filename == '':
        return "Empty file", 400

    # Check if the file is a text file
    if file and file.filename.endswith('.txt'):
        # Save the file to a temporary location
        file_path = os.path.join(Filespath, file.filename)
        file.save(file_path)

        # Extract map information from the file
        map_info = extract_map_info(file_path)

        # Delete the temporary file after extracting information
        os.remove(file_path)

        # Create a temporary file to store the map information
        with NamedTemporaryFile(mode='w', delete=False) as temp_file:
            # Write the map information to the temporary file
            json.dump(map_info, temp_file)
            temp_file_name = temp_file.name

        # Return the temporary file as a response
        return send_file(temp_file_name, as_attachment=True, mimetype='application/json')

    else:
        return "Invalid file format, please upload a text file (.txt)", 400


def extract_map_info_from_csv(file_path):
    # Dummy function to simulate extracting map information from the CSV file
    # Replace this with actual logic
    data = pd.read_csv(file_path)
    # Example: assuming the CSV has 'latitude' and 'longitude' columns
    map_info = data[['latitude', 'longitude']].to_dict(orient='records')
    return map_info

@app.route("/analyzer/csv", methods=["POST"])
def post_csv_analyzer():
    file = request.files['csvfile']

    # Check if the file is empty
    if file.filename == '':
        return "Empty file", 400

    # Check if the file is a CSV file
    if file and file.filename.endswith('.csv'):
        # Save the file to a temporary location
        file_path = os.path.join(Filespath, file.filename)
        file.save(file_path)

        # Extract map information from the CSV file
        map_info = extract_map_info_from_csv(file_path)

        # Delete the temporary file
        os.remove(file_path)

        # Create a temporary file to store the map information in CSV format
        with NamedTemporaryFile(mode='w', delete=False, newline='') as temp_file:
            # Create a CSV writer object
            csv_writer = csv.DictWriter(temp_file, fieldnames=['latitude', 'longitude'])
            csv_writer.writeheader()
            # Write the map information to the temporary file
            csv_writer.writerows(map_info)
            temp_file_name = temp_file.name

        # Return the temporary file as a response
        return send_file(temp_file_name, as_attachment=True, attachment_filename='extracted_map_info.csv', mimetype='text/csv')

    else:
        return "Invalid file format, please upload a CSV file (.csv)", 400


@app.route("/home")
def home():
    locations = [
        {"name": "New York", "lat": 40.7128, "lon": -74.0060},
        {"name": "London", "lat": 51.5074, "lon": -0.1278},
        {"name": "Paris", "lat": 48.8566, "lon": 2.3522},
        {"name": "Tokyo", "lat": 35.6895, "lon": 139.6917},
        {"name": "Sydney", "lat": -33.8688, "lon": 151.2093},
        {"name": "Dubai", "lat": 25.2048, "lon": 55.2708},
        {"name": "Rome", "lat": 41.9028, "lon": 12.4964},
        {"name": "Hong Kong", "lat": 22.3193, "lon": 114.1694},
        {"name": "Berlin", "lat": 52.5200, "lon": 13.4050},
        {"name": "Istanbul", "lat": 41.0082, "lon": 28.9784},
    ]
    # Create a Folium map centered on the first location
    center_lat, center_lon = locations[0]["lat"], locations[0]["lon"]
    map = folium.Map(location=[center_lat, center_lon], zoom_start=2)

    # Add markers for each location
    for loc in locations:
        name = loc["name"]
        lat, lon = loc["lat"], loc["lon"]
        folium.Marker([lat, lon], popup=name).add_to(map)

    # Save the map as an HTML string
    map_html = map._repr_html_()
    return render_template(
        "index.html",
        username=current_user.id,
        number_of_files=number_of_files(),
        number_of_excel_files=number_of_excel_files() , 
        map_html=map_html , 
        localtime = localtime

    )




@app.route("/document")
def document():
    return render_template("Documentation.html")


if __name__ == "__main__":
    app.run (port=5005 , debug=True)
