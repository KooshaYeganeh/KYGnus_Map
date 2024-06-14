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
from shapely.geometry import Point, Polygon
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









app = Flask(__name__)

username = getpass.getuser()  # Get username of system



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








# Create Directory For App
appdir = os.path.join(f"/home/{username}/Apps/KYGnus_Map")
os.makedirs(appdir, exist_ok=True)
logger.info(Fore.YELLOW + "[ INFO ] App Create Directory in Home of username")


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

def number_of_maps():
    maps_path = "./templates/maps"
    if not os.path.exists(maps_path):
        print(f"The directory {maps_path} does not exist.")
        return 0
    maps = glob.glob(os.path.join(maps_path, "**/*.html"), recursive=True)
    return len(maps)

def number_of_modules():
    modules_path = os.path.abspath("../Modules")
    if not os.path.exists(modules_path):
        print(f"The directory {modules_path} does not exist.")
        return 0
    modules = glob.glob(os.path.join(modules_path, "**/*.*"), recursive=True)
    return len(modules)






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
    SECRET_KEY="KYGnus_Mapper"
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
    return render_template(
        "index.html",
        username=current_user.id,
        number_of_files=number_of_files(),
        number_of_excel_files=number_of_excel_files(),
        number_of_maps=number_of_maps(),
        number_of_modules=number_of_modules()
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
                               number_of_modules=number_of_modules(),
                               number_of_excel_file=number_of_excel_files(), username = username)



@app.route("/tools/addresses_into_coordinates" , methods=["POST"])
def addresses_into_coordinates():
    coordinates = None
    if request.method == 'POST':
        address = request.form['address']
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(address)
        if location:
            coordinates = (location.latitude, location.longitude)
    
    return Response('''
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>Geocode Address</title>
          </head>
          <body>
            <div class="container">
              <h1 class="mt-5">Geocode Address</h1>
              <form method="post">
                <div class="form-group">
                  <label for="address">Enter an address:</label>
                  <input type="text" class="form-control" id="address" name="address" placeholder="Enter address">
                </div>
                <button type="submit" class="btn btn-primary">Geocode</button>
              </form>
              {% if coordinates %}
                <h2 class="mt-5">Coordinates:</h2>
                <p>Latitude: {{ coordinates[0] }}</p>
                <p>Longitude: {{ coordinates[1] }}</p>
              {% endif %}
            </div>
          </body>
        </html>
    ''', coordinates=coordinates)



html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>GeoPandas Plot</title>
</head>
<body>
    <h1>Customize GeoPandas Plot</h1>
    <form action="/" method="post">
        <label for="country">Country (optional):</label><br>
        <input type="text" id="country" name="country" placeholder="e.g., Finland"><br><br>
        <label for="coordinates">Coordinates (optional, format: lat,lon):</label><br>
        <input type="text" id="coordinates" name="coordinates" placeholder="e.g., 37.7749,-122.4194"><br><br>
        <label for="figsize">Figure Size (width, height):</label><br>
        <input type="text" id="figsize" name="figsize" value="10, 6"><br><br>
        <label for="color">Color:</label><br>
        <input type="text" id="color" name="color" value="blue"><br><br>
        <label for="alpha">Alpha (transparency):</label><br>
        <input type="text" id="alpha" name="alpha" value="0.6"><br><br>
        <input type="submit" value="Generate Plot">
    </form>
    {% if plot_url %}
        <h2>Generated Plot:</h2>
        <img src="{{ plot_url }}" alt="GeoPandas Plot">
    {% endif %}
</body>
</html>
'''




@app.route("/tools/geopands")
def geopands():
    return render_template("tools.html")


@app.route("/tools/geopands" , methods=["POST"])
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

            # Load the dataset
            world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
            
            # Create the plot
            fig, ax = plt.subplots(1, 1, figsize=figsize)
            world.plot(ax=ax, color=color, alpha=alpha)

            # Highlight the specified country
            if country:
                country_data = world[world['name'].str.contains(country, case=False)]
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

    return render_template_string(html_template, plot_url=plot_url)












@app.route("/tools/geopands")
def shapely():
    return render_template("tools.html")




@app.route('/tools/geopands', methods=['POST'])
def check_point_in_polygon():
    result = None
    if request.method == 'POST':
        try:
            # Get user inputs
            point_input = request.form.get('point')
            polygon_input = request.form.get('polygon')

            # Convert input strings to appropriate types
            point_coords = tuple(map(float, point_input.split(',')))
            polygon_coords = [tuple(map(float, coord.split(','))) for coord in polygon_input.split()]

            # Create Point and Polygon objects
            point = Point(point_coords)
            polygon = Polygon(polygon_coords)

            # Check if the point is within the polygon
            result = point.within(polygon)
            result = f"The point {point} is within the polygon {polygon}: {result}"
        except Exception as e:
            result = f"An error occurred: {e}"

    return render_template("tools.html", result=result)




@app.route("/tools/harvesin")
def pyproj_get():
        return render_template("tools.html")



@app.route("/tools/harvesin" , methods = ["POST"])
def pyproj():
    try:
        lon1 = float(request.form['lon1'])
        lat1 = float(request.form['lat1'])
        lon2 = float(request.form['lon2'])
        lat2 = float(request.form['lat2'])
        
        point1 = (lat1, lon1)
        point2 = (lat2, lon2)
        
        distance = haversine(point1, point2, unit=Unit.KILOMETERS)
        
        response_data = {
            'longitude1': lon1,
            'latitude1': lat1,
            'longitude2': lon2,
            'latitude2': lat2,
            'distance_km': distance
        }
        
        return Response(json.dumps(response_data), mimetype='application/json')
    
    except ValueError as e:
        return Response(json.dumps({'error': str(e)}), mimetype='application/json')
    




def generate_heatmap(heat_data):
    # Create a map centered at a specific location
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)

    # Add heat map layer
    HeatMap(heat_data).add_to(m)

    # Save the map as a temporary HTML file
    temp_file = 'heatmap_data.html'
    m.save(temp_file)

    return temp_file




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
            return send_file(heatmap_file, as_attachment=True, attachment_filename='heatmap_data.html')

        except ValueError:
            return "Invalid input. Please enter numeric values."
    
    return render_template('heatmap.html')





@app.route("/variogram_kriging")
def variogram_kriging():
    return render_template("geostatistics.html" , username = username)




@app.route("/variogram_kriging" , methods=["POST"])
def geostatistics():
    # Get the user input from the form
    x_coords = request.form['X']
    y_coords = request.form['Y']
    values = request.form['Value']
    
    # Convert the input strings into lists of floats
    x_coords = list(map(float, x_coords.split(',')))
    y_coords = list(map(float, y_coords.split(',')))
    values = list(map(float, values.split(',')))

    # Ensure that the input lists have the same length
    if not (len(x_coords) == len(y_coords) == len(values)):
        return "Error: X, Y, and Value lists must be of the same length."

    # Create a DataFrame from the user input
    data = pd.DataFrame({
        'X': x_coords,
        'Y': y_coords,
        'Value': values
    })

    # Save the data to a CSV file as Pygeostat works with files
    data_file = 'data.csv'
    data.to_csv(data_file, index=False)

    # Load the data into a Pygeostat DataFile object
    df = gs.DataFile(flname=data_file)

    # Calculate and plot the variogram
    variogram = gs.Variogram(df, coord_cols=['X', 'Y'], var_cols='Value', log=False)

    # Fit a variogram model
    variogram_model = variogram.fit_model()

    # Perform ordinary kriging
    krig_result = gs.Krige(df, variogram_model, coord_cols=['X', 'Y'], var_cols='Value')

    # Save the kriging result to a CSV file
    krig_result_file = 'krig_result.csv'
    krig_result.to_csv(krig_result_file, index=False)

    # Send the kriging result file as a downloadable file
    return send_file(krig_result_file, as_attachment=True)



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




@app.route('/location_prediction')
def predict_loc():
    return render_template("predict_location.html" , username = username)



# Load location data from CSV
def load_location_data():
    return pd.read_csv('location_data.csv')

# Define function for linear interpolation
def interpolate_timestamp(loc, loc1, loc2, t1, t2):
    """
    Perform linear interpolation to predict timestamp at given latitude or longitude between two known locations.
    
    Parameters:
    - loc: Target latitude or longitude for prediction
    - loc1, loc2: Coordinates (latitude, longitude) of known locations
    - t1, t2: Timestamps of known locations (t1 < t < t2)
    
    Returns:
    - Predicted timestamp at given latitude or longitude
    """
    delta_loc = (loc - loc1) / (loc2 - loc1)
    interpolated_time = t1 + delta_loc * (t2 - t1)
    return interpolated_time


@app.route('/location_prediction', methods=['POST'])
def predict_locations():
    location_data = load_location_data()

    # Read latitude and longitude from form input
    input_latitude = float(request.form['latitude'])
    input_longitude = float(request.form['longitude'])

    # Find closest locations
    for i in range(len(location_data) - 1):
        loc1 = location_data[['latitude', 'longitude']].iloc[i]
        loc2 = location_data[['latitude', 'longitude']].iloc[i + 1]
        
        if loc1['latitude'] <= input_latitude <= loc2['latitude'] or loc1['longitude'] <= input_longitude <= loc2['longitude']:
            t1 = datetime.strptime(location_data['timestamp'].iloc[i], '%Y-%m-%d %H:%M:%S')
            t2 = datetime.strptime(location_data['timestamp'].iloc[i + 1], '%Y-%m-%d %H:%M:%S')
            
            # Interpolate timestamp
            interpolated_time = interpolate_timestamp(input_latitude, loc1['latitude'], loc2['latitude'], t1, t2)

            # Prepare HTML response
            html_response = f"""
            <html>
            <head><title>Predicted Location</title></head>
            <body>
                <h1>Predicted Location</h1>
                <p>Latitude: {input_latitude}</p>
                <p>Longitude: {input_longitude}</p>
                <p>Predicted Timestamp: {interpolated_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
            </body>
            </html>
            """
            
            # Create HTML response with Response object
            response = make_response(html_response)
            response.headers['Content-Type'] = 'text/html'
            return response
    
    # Return error response if prediction fails
    return make_response("<html><body><h1>Prediction Error</h1></body></html>", 400)
















@ app.route("/search", methods=["POST"])
def Search_db():
    jostoju = request.form["search"]
    logger.info(Fore.YELLOW + "[ Info ] user Start to Search ans asnad")
    cur = db.cursor()
    cur.execute(f"SELECT * FROM map WHERE Name LIKE '%{jostoju}%'")
    data1 = cur.fetchall()
    cur.close()
    # TODO : Edit template to show data
    return render_template("search_result_asnad.html", data=data1)


@ app.route("/user/db/remove", methods=["POST"])
def remove_db():
    try:
        locname = request.form["name"]
        cur = db.cursor()
        cur.execute("DELETE FROM map WHERE name = %s ", locname)
        data = db.commit()
        cur.close()
        logger.warning(
            Fore.RED + "[ Warning ] Admin Delete one Row from map database")
        return render_template("success.html")
    except:
        logger.warning(
            Fore.RED + "[ Warning ] Can't Delete one Row from map database")
        return render_template("404.html")

















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



def extract_map_info_from_csv(file_path):
    map_info = []

    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lat = float(row['latitude'])
            lon = float(row['longitude'])
            map_info.append({'latitude': lat, 'longitude': lon})

    return map_info



@ app.route("/analyzer/text", methods=["POST"])
def post_document_analyzer():
    file = request.files['textfile']
    if file.filename == '':
        return "Empty file", 400

    # Check if the file is a text file
    if file and file.filename.endswith('.txt'):
        # Save the file to a temporary location
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        # Extract map information from the file
        map_info = extract_map_info(file_path)

        # Delete the temporary file
        os.remove(file_path)

        # Create a temporary file to store the map information
        with NamedTemporaryFile(mode='w', delete=False) as temp_file:
            # Write the map information to the temporary file
            json.dump(map_info, temp_file)

        # Return the temporary file as a response
        return send_file(temp_file.name, as_attachment=True, attachment_filename='map_info.json', mimetype='application/json')
    
    else:
        return "Invalid file format, please upload a text file (.txt)", 400



@ app.route("/analyzer/csv", methods=["POST"])
def post_csv_analyzer():
    file = request.files['csvfile']

    # Check if the file is empty
    if file.filename == '':
        return "Empty file", 400

    # Check if the file is a CSV file
    if file and file.filename.endswith('.csv'):
        # Save the file to a temporary location
        file_path = os.path.join('uploads', file.filename)
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

        # Return the temporary file as a response
        return send_file(temp_file.name, as_attachment=True, attachment_filename='extracted_map_info.csv', mimetype='text/csv')
    
    else:
        return "Invalid file format, please upload a CSV file (.csv)", 400

@app.route("/home")
def home():
    return render_template('index.html', 
                           number_of_files=number_of_files(),
                           number_of_excel_files=number_of_excel_files(),
                           number_of_maps=number_of_maps(),
                           number_of_modules=number_of_modules() , username = username)




@app.route("/document")
def document():
    return render_template("Documentation.html")


if __name__ == "__main__":
    app.run (port=5005 , debug=True)
