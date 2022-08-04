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
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from types import MethodDescriptorType
from flask import Flask, render_template, request, url_for
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


app = Flask(__name__)



""" Define Basic Configs of Logging.This Bsic Configs have Time and 
Message and FileMode"""
logging.basicConfig(filename="KYGnus_Map.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger() # Create Logger of Logging System

logger.setLevel(logging.DEBUG) # Set Level For Logger


## connect to MariaDB

try:
    logger.info(Fore.YELLOW + "[ INFO ] connecting to database")
    db = pymysql.connect(host=config.DB_HOST,
						user=config.DB_USER,
						passwd=config.DB_PASSWORD,
						db=config.DB,
						port=config.DB_PORT,
						charset='utf8',
						use_unicode=True)
except:
    logger.warning(Fore.YELLOW + "[ Warning ] Could not connect to database")
    print("ERROR on connecting to mariaDB")



username=getpass.getuser() # Get username of system
logger.info(Fore.YELLOW + f"[ INFO ] Get username of system: This Username is {username}")


# Create Directory For App
appdir = os.path.join(f"/home/{username}/KYGnus_Map")
os.makedirs(appdir,exist_ok=True)
logger.info(Fore.YELLOW + "[ INFO ] App Create Directory in Home of username")



# Create Directory For Filed in App Directory
""" make Directory For Files in user Direcory If Exist pass it"""
Filespath = os.path.join(f"/home/{username}/KYGnus_Map/Files") 
os.makedirs(Filespath,exist_ok=True) 
logger.info(Fore.YELLOW + f"[ INFO ] Making Directory for Files in /home/{username}/KYGnus_Map")




""" make Directory For  Excel Files in user Direcory If Exist pass it"""
excel_files_path = os.path.join(f"/home/{username}/KYGnus_Map/Files/Excel") 
os.makedirs(excel_files_path,exist_ok=True) 
logger.info(Fore.YELLOW + f"[ INFO ] Making Directory for Excel Files in /home/{username}/KYGnus_Map/Files")


""" make Directory For CIrcular Markger Excel Files in user Direcory If Exist pass it"""
excel_marker_files_path = os.path.join(f"/home/{username}/KYGnus_Map/Files/Excel/marker") 
os.makedirs(excel_marker_files_path,exist_ok=True) 
logger.info(Fore.YELLOW + f"[ INFO ] Making Directory for Excel Files in /home/{username}/KYGnus_Map/Files")

""" make Directory For circular marker Excel Files in user Direcory If Exist pass it"""
excel_cmarker_files_path = os.path.join(f"/home/{username}/KYGnus_Map/Files/Excel/circular") 
os.makedirs(excel_cmarker_files_path,exist_ok=True) 
logger.info(Fore.YELLOW + f"[ INFO ] Making Directory for Excel Files in /home/{username}/KYGnus_Map/Files")




""" make Directory For doc Files in user Direcory If Exist pass it"""
doc_files_path = os.path.join(f"/home/{username}/KYGnus_Map/Files/Documents") 
os.makedirs(doc_files_path,exist_ok=True) 
logger.info(Fore.YELLOW + f"[ INFO ] Making Directory for doc Files in /home/{username}/KYGnus_Map/Files")




""" make Directory For Files in user Direcory If Exist pass it"""
backup_path = os.path.join(f"/home/{username}/KYGnus_Map/Files/Backup") 
os.makedirs(backup_path,exist_ok=True) 
logger.info(Fore.YELLOW + f"[ INFO ] Making Directory for doc Files in /home/{username}/KYGnus_Map/Files/Backup")



""" make Directory For DB Backup Files in user Direcory If Exist pass it"""
db_backup_path = os.path.join(f"/home/{username}/KYGnus_Map/Files/Backup/DB") 
os.makedirs(db_backup_path,exist_ok=True) 
logger.info(Fore.YELLOW + f"[ INFO ] Making Directory for doc Files in /home/{username}/KYGnus_Map/Files/Backup/DB")



""" make Directory For system Backup Files in user Direcory If Exist pass it"""
sysfile_backup_path = os.path.join(f"/home/{username}/KYGnus_Map/Files/Backup/System") 
os.makedirs(sysfile_backup_path,exist_ok=True) 
logger.info(Fore.YELLOW + f"[ INFO ] Making Directory for doc Files in /home/{username}/KYGnus_Map/Files/Backup/")



""" make Directory For app Backup in user Direcory If Exist pass it"""
app_backup_path = os.path.join(f"/home/{username}/KYGnus_Map/Files/Backup/App") 
os.makedirs(app_backup_path,exist_ok=True) 
logger.info(Fore.YELLOW + f"[ INFO ] Making Directory for doc Files in /home/{username}/KYGnus_Map/Files/Backup/app")



# Flask limiter
""" Limit the number of requests to the server """
limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["1000 per day", "500 per hour"]
)

app.config.update(
    SECRET_KEY="KYGnus_Mapper"
)

# Flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "%d" % (self.id)


user = User(0)


@app.route("/")
@login_required
def loogin():
    return render_template("index.html")



@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
@limiter.limit("5 per minutes") # This Limits Requests to Prevent BruteForce Attack
def loggin():
    username = request.form["username"]
    password = request.form["password"]
    if username == config.USERNAME and password == config.PASSWORD:
        logger.warning(Fore.RED + "user Try ro login")
        time.sleep(5)
        number_of_files = len(glob.glob(f"/home/{username}/Documents/**/*.*" , recursive=True))
        number_of_excel_files = len(glob.glob(f"/home/{username}/Documents/**/*.csv" , recursive=True))
        number_of_documents = len(glob.glob(f"/home/{username}/Documents/**/*.txt" , recursive=True))
        return render_template("index.html" , Number_of_Files=number_of_files , number_of_excel_file=number_of_excel_files , number_of_Documents=number_of_documents)
    else:
        logger.warning(Fore.RED + "[ Warning ] Login Faild.system redirect User to /login")
        return redirect("/login")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    logger.info(Fore.YELLOW  +"[ INFO ] user logout")
    return Response('<p>Logged out</p>')


@app.errorhandler(401)
def page_not_found(e):
    logger.warning(Fore.RED + "[ Warning ] 401 Error")
    return Response('<center><h1>Login Failed</h1><center>')


@login_manager.user_loader
def load_user(userid):
    return User(userid)



allowed_formats = {"csv"} # allowed file types


# Secure File name
def check_files(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in allowed_formats





@app.route("/createmap")
def createmap():
    logger.info(Fore.CYAN + "[ Info ] Loading Create Map Page")
    return render_template("createmap.html")

""" This Route Create Route For main Map Without Any Marks
This Will be Get Lat and Long and Create Map in That Locations"""

@app.route("/createmap/createmainmap")
def create_main_map():
    logger.info(Fore.CYAN + "[ Info ] Loading Create Map Page")
    return render_template("main_map_creator.html")




## TODO : create Template For main Map 
""" This Route create main Map and save map in templates Directory
This is Basic map with No Marker"""
@app.route("/createmap/createmainmap" , methods=["POST"])
def main_map():
    lat = request.form["lat"]
    lan = request.form["lan"]
    logger.info("lat: " + lat + " lan: " + lan)
    try:
        map = folium.Map(location=[lat,lan], zoom_start = 14)
        logger.info(Fore.CYAN + "User Load Main map")
        map.save("./templates/maps/mainmap.html")
        logger.info(Fore.CYAN + "[ Info ] User Save Map")
        return render_template("maps/mainmap.html")
    except:
        return Response("<html><body style='background-color:white;'><center ><h1 style='color:red;'> Can't Process Excel File !!!</h1><h2> Please Check File Type and Format Or Sure This File Design is True</center></html></body>")




# marker

""" This Route Create Map and insert Marker in File.
This is Basic map with Marker and Save File in templates Directory in templates/maps"""

@app.route("/createmap/map/marker" , methods=["POST"])
def marker():
    """ This route get excel File and insert marker on map"""
    csv_file = request.files["csv_file"]
    if check_files(csv_file.filename):
        print(check_files(csv_file.filename))
        logger.info(Fore.YELLOW + "[ Info ] check File Format for Security Reasons")
        try:
            locations = pd.read_csv(csv_file)
            main_locations = locations[["Latitude", "Longitude", "Name"]]
            map = folium.Map(location=[main_locations.Latitude.mean(), main_locations.Longitude.mean()], zoom_start=14, control_scale=True)
            for index, location_info in main_locations.iterrows():
                if folium.Marker([location_info["Latitude"], location_info["Longitude"]], popup=location_info["Name"]).add_to(map) :
                    map.save(f"./templates/maps/{csv_file.filename}.html")
                    print("map Saved succesfully")
            goal_path = os.path.join(excel_marker_files_path, csv_file.filename)
            csv_file.save(goal_path)  # the file save in Goal path
            return redirect("/createmap")
        except:
             return Response("<html><body style='background-color:white;'><center ><h1 style='color:red;'> Can't Process Excel File !!!</h1><h2> Please Check File Type and Format Or Sure This File Design is True</center></html></body>")



# circular marker

""" This Route Make marker in Circular Mode and Save Map in template/maps Directory"""


@app.route("/createmap/map/circular-maker" ,  methods=["POST"])
def cmarker():
    """ at this route and Function  make curcular maker to map.first Get excwl File and
    make sure this File is Safe and after that save it in excelpath"""
    csv_file = request.files["csv_file"]
    if check_files(csv_file.filename):
        print(check_files(csv_file.filename))
        logger.info(Fore.YELLOW + "[ Info ] check File Format for Security Reasons")
        try:
            locations = pd.read_csv(csv_file)
            main_locations = locations[["Latitude", "Longitude", "Name"]]
            map = folium.Map(location=[main_locations.Latitude.mean(), main_locations.Longitude.mean()], zoom_start=14, control_scale=True)
            for index, location_info in main_locations.iterrows():
                if folium.CircleMarker([location_info["Latitude"], location_info["Longitude"]], popup=location_info["Name"]).add_to(map):
                    map.save(f"./templates/maps/{csv_file.filename}_circular.html")
                    print("map Saved succesfully")
            goal_path = os.path.join(excel_marker_files_path, csv_file.filename)
            csv_file.save(goal_path)  # the file save in Goal path
            return redirect("/createmap")
        except:
            return Response("<html><body style='background-color:white;'><center ><h1 style='color:red;'> Can't Process Excel File !!!</h1><h2> Please Check File Type and Format Or Sure This File Design is True</center></html></body>")








# Related
""" this Route Show Related Sites Like this Map , This is Have Sites 
and Their Link Can Download Data or Use Informations of This Sites"""
@app.route("/related")
def related():
    logger.info(Fore.YELLOW + "[ Info ] Get related template")
    return render_template("related.html")




# Download Files

# wget https://github.com/jadijadi/machine_learning_with_python_jadi/archive/refs/heads/main.zip




# Extensions
""" at This route You Can Download Extensions Like WordPress
"""
@app.route("/extensions")
def extensions_get():
    logger.info(Fore.YELLOW + "[ Info ] Get extensions template")
    return render_template("extensions.html")

@app.route("/extensions/fs" , methods=["POST"])
def extensions_fs():
    opt = os.popen("cd /opt").read()
    mainzip = os.popen("wget https://github.com/KooshaYeganeh/FS/archive/refs/heads/main.zip").read()
    unzip = os.popen("unzip main.zip").read()
    fs = os.popen("cd FS-main").read()
    usr_bin = os.popen("sudo cp sort /usr/bin").read()
    cd = os.popen("cd").read()
    print(opt,mainzip,unzip,fs,usr_bin,cd)
    logger.info(Fore.YELLOW + "[ Info ] FS App installed")
    return render_template("success.html")  



@app.route("/extensions/clamav" , methods=["POST"])
def clamav_install():
    update = os.popen("sudo apt update -y").read()
    install = os.popen("sudo apt-get install clamav clamav-daemon -y").read()
    updatedb = os.popen("sudo freshclam").read()
    print(update,install,updatedb)
    logger.info(Fore.YELLOW + "[ Info ] clamAV Installed")
    return render_template("success.html")




@app.route("/extensions/maldet" , methods=["POST"])
def maldet():
    update = os.popen("sudo apt update -y").read()
    chdir = os.popen("cd /tmp").read()
    getfile = os.popen("wget http://www.rfxn.com/downloads/maldetect-current.tar.gz").read()
    unzip = os.popen("tar xfz maldetect-current.tar.gz").read()
    chmaldet = os.popen("cd maldetect-1.6.4").read()
    install = os.popen("./install").read()
    print(update,chdir,getfile,unzip,chmaldet,install)
    logger.info(Fore.YELLOW + "[ Info ] maldet Installed")
    return render_template("success.html")


	
@app.route("/extensions/rkhunter" , methods=["POST"])
def rkhunter():
    update = os.popen("sudo apt update -y").read()
    install = os.popen("sudo apt install rkhunter -y").read()
    print(update,install)
    logger.info(Fore.YELLOW + "[ Info ] RootKit Hunter Installed")
    return render_template("success.html")




@app.route("/extensions/lynis"  , methods=["POST"])
def lynis():
    update = os.popen("sudo apt update -y").read()
    install = os.popen.read("sudo apt install lynis").read()
    print(update,install)
    logger.info(Fore.YELLOW + "[ Info ] Lynis Installed")
    return render_template("success.html")


    
# Admin

@app.route("/user")
def admin():
    logger.info(Fore.YELLOW + "[ Info ] Admin Dashboard Loaded")
    return render_template("login_admin.html")

## Login Admin
@app.route("/user" , methods=["POST"])
@limiter.limit("3 per minutes")
def admin_login():
    admin_username = request.form["admin_username"]
    admin_password = request.form["admin_password"]
    if admin_username == config.ADMIN_USERNAME and admin_password == config.ADMIN_PASSWORD:
        logger.info(Fore.YELLOW + "[ Info ] App sleep for Prevent Bruteforce Attack")
        time.sleep(5)
        csv_files = os.popen(f"find /home/{username}/KYGnus_Map/ -type f -iname '*.csv' | wc -l").read()
        map_files = os.popen("find ./templates/maps -type f | wc -l").read()
        doc_file1 = os.popen(f"find /home/{username}/KYGnus_Map -type f -iname '*.docx' | wc -l").read()
        doc_file2 = os.popen(f"find /home/{username}/KYGnus_Map -type f -iname '*.txt' | wc -l").read()
        alldoc = int(doc_file1) + int(doc_file2)
        roll = 5
        logger.info(Fore.YELLOW + "[ Info ] connecting To MariaDB")
        con = pymysql.connect(host=config.DB_HOST,
                          database=config.DB,
                          user=config.DB_USER,
                          port=config.DB_PORT,
                          password=config.DB_PASSWORD)
        logger.info(Fore.YELLOW + "[ Info ] connected To MariaDB")
        cur = con.cursor()
        cur.execute("SELECT * FROM map")
        cur.fetchall()
        rc = cur.rowcount
        cur.close()
        return render_template("form_dash.html", database_record=rc , number_of_maps = map_files , number_of_excel_file = csv_files , number_of_documents = alldoc)
    else:
        logger.warning(Fore.RED + "[ Warning ] Username or Password is False,redirected to /admin")
        return redirect("/user")


## CSV to MYSQL
"""at This Route read csv File and try to save it in MYSQL"""
@app.route("/user/csvtomtsql" , methods=["POST"])
def csvtomtsql():
    # read csv file and save it in mysql
    #csvfile = request.files["csv_file"]
    logger.info(Fore.YELLOW + "[ Info ] connection to mariaDB to Insert csv File")
    db = pymysql.connect(host=config.DB_HOST,
						user=config.DB_USER,
						passwd=config.DB_PASSWORD,
						db=config.DB,
						port=config.DB_PORT,
						charset='utf8',
						use_unicode=True)
    try:
        cursor = db.cursor()
        csv_data = csv.reader(open("../dublin.csv"))
        print(csv_data)
        next(csv_data)
        for row in csv_data:
            # create table map (radif VARCHAR(100) , nam VARCHAR(1000) , tozih VARCHAR(1500) , tool varchar(1000) , arz varchar(1000));
            # cur.execute("INSERT INTO shohada (namekamel,tarikhetavallod,mahalletavllod,tarikheshahadat,mahalleshahadat,kholase,tozihat)" "VALUES('%s' , '%s' , '%s' , '%s' , '%s' ,'%s' ,'%s')" % (''.join(namekamel), ''.join(tarikhetavallod), ''.join(mahalletavllod), ''.join(tarikheshahadat), ''.join(mahalleshahadat), ''.join(kholase), ''.join(tozihat)))
            cursor.execute("INSERT INTO map(radif,nam,tozih,tool,arz)" "VALUES(%s, %s,%s, %s , %s)",row)
            db.commit()
            cursor.close()
            logger.info(Fore.YELLOW + "[ INFO ] File Read And Save in CSV File succuessfuly")
            return render_template("success.html")
    except:
        logger.warning(Fore.RED + "[ Warning ] Can't Insert data to mariaDb")
        return Response("<center><h2 > ERROR  </h2></br><p>Please Check File or MariaDB Columns ...</p></br><h1>Cant't Insert data to MariaDB !!!</h1></center>")  
            




@app.route("/user/db/search", methods=["POST"])
def Search_db():
    jostoju = request.form["search"]
    logger.info(Fore.YELLOW + "[ Info ] user Start to Search ans asnad")
    cur = db.cursor()
    cur.execute("SELECT * FROM map WHERE name = %s", jostoju)
    data1 = cur.fetchall()
    cur.close()
	## TODO : Edit template to show data
    return render_template("search_result_asnad.html", data=data1)


@app.route("/user/db/remove", methods=["POST"])
def remove_db():
    try:
        locname = request.form["name"]
        cur = db.cursor()
        cur.execute("DELETE FROM map WHERE name = %s ", locname)
        data = db.commit()
        cur.close()
        logger.warning(Fore.RED + "[ Warning ] Admin Delete one Row from map database")
        return render_template("success.html")
    except:
        logger.warning(Fore.RED + "[ Warning ] Can't Delete one Row from map database")
        return render_template("404.html")



@app.route("/user/db/backup", methods=["POST"])
def db_backup():
#     DB_HOST = config.DB_HOST
#     DB_USER = config.DB_USER
#     DB_USER_PASSWORD = config.DB_PASSWORD
#     PORT = config.DB_PORT
#     # DB_NAME = '/backup/dbnameslist.txt'
#     DB_NAME = config.DB
#     BACKUP_PATH = db_backup_path
#     logger.warning(Fore.RED + "[ Warning ] Get backup of Database")
#     # Getting current DateTime to create the separate backup folder like "20180817-123433".
#     DATETIME = time.strftime('%Y%m%d-%H%M%S')
#     TODAYBACKUPPATH = BACKUP_PATH + '/' + DATETIME

#     # Checking if backup folder already exists or not. If not exists will create it.
#     try:
#         os.stat(TODAYBACKUPPATH)
#     except:
#         os.mkdir(TODAYBACKUPPATH)

#     # Code for checking if you want to take single database backup or assinged multiple backups in DB_NAME.
#     print("checking for databases names file.")
#     if os.path.exists(DB_NAME):
#         file1 = open(DB_NAME)
#         multi = 1
#         print("Databases file found...")
#         logger.info(Fore.YELLOW + "[ Info ] Databases file found...")
#         print("Starting backup of all dbs listed in file " + DB_NAME)
#     else:
#         print("Databases file not found...")
#         print("Starting backup of database " + DB_NAME)
#         multi = 0

#     # Starting actual database backup process.
#     if multi:
#         in_file = open(DB_NAME, "r")
#         flength = len(in_file.readlines())
#         in_file.close()
#         p = 1
#         dbfile = open(DB_NAME, "r")

#         while p <= flength:
#             db = dbfile.readline()   # reading database name from file
#             db = db[:-1]         # deletes extra line
#             dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + \
#                 " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
#             os.system(dumpcmd)
#             gzipcmd = "gzip " + \
#                 pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
#             os.system(gzipcmd)
#             p = p + 1
#         dbfile.close()
#     else:
#         db = DB_NAME
#         dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + \
#             " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
#         os.system(dumpcmd)
#         gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
#         os.system(gzipcmd)

#     print("")
    #print("Backup script completed")
    backup = os.popen(f"mysqldump -u {config.DB_USER} -p {config.DB_PASSWORD} mapper > {db_backup_path}/mapper.sql").read()
    return Response(f"<center><h1> Mariadb Backup</h1><h2>Your backups have been created. </h2><h1> File Saved in {db_backup_path}</h1></center>")








@app.route("/user/db/export2excel", methods=["POST"])
def export_excel():
    try:
        user = config.DB_USER  # your username
        passwd = config.DB_PASSWORD  # your password
        host = config.DB_HOST  # your host
        port = config.DB_PORT  # mysql port
        db = config.DB  # database where your table is stored
        table = 'map'  # table you want to save
        logger.critical( Fore.RED + "[ Warning ] admin Try to Dump Excel of Mapper Table in Excel")
        con = pymysql.connect(user=user, passwd=passwd,
                          host=host, db=db, port=port)
        cursor = con.cursor()
        query = "SELECT * FROM %s;" % table
        cursor.execute(query)
        with open(f'{db_backup_path}/map.csv', 'w') as f:
            writer = csv.writer(f)
            for row in cursor.fetchall():
                writer.writerow(row)
                return render_template("success.html")
    except:
        return render_template("404.html")


@app.route("/user/read_excel/circular" , methods=["POST"])
def read_excel_cicular():
    excel_file = request.files["excel_file"]
    if clear():
        try:
            df  = pd.read_csv(excel_file)
            for index,(Number,Name,Address,Latitude,Longitude) in df.iterrows():
                db = pymysql.connect(host=config.DB_HOST,
                    user=config.DB_USER,
					passwd=config.DB_PASSWORD,
					db=config.DB,
					port=config.DB_PORT,
					charset='utf8',
					use_unicode=True)
                cur = db.cursor()
                query = "INSERT INTO map VALUES( %s , %s , %s , %s , %s )"
                cur.execute(query , 
					(Number,Name,Address,Latitude,Longitude))
                db.commit()
                db.close()
            return Response(f"""<body style='background-color:white;'>
						<center>
						<h2 style='color:red;'>Done</h2>
						<h1>Excel File Saved Successfuly in Database</h1>
						<a href='/'><button>Home</button></a>
						</center>
						</body>""")

        except:
            return Response(f"""<body style='background-color:white;'>
						<center>
						<h2 style='color:red;'>ERROR</h2>
                            <h1 style='color:red;'>Error File Saving in Database</h1>
						<a href='/'><button>Home</button></a>
						</center>
						</body>""")


    
     
#logs
@app.route("/user/logs")
def logs():
    with open("KYGnus_Map.log" , "r") as log_file:
        log_read = log_file.readlines()
        #logger.info(Fore.YELLOW + "[ Info ] Loading Log File")
        return render_template("log.html" , log_line=log_read) 





# Document

""" Create Minimal Documents For app in Html Style """
@app.route("/documentation")
def document():
    logger.info(Fore.YELLOW + "[ Info ] user Start to View Documentation")
    return render_template("Documentation.html")




## TODO : create log template

        



@app.route("/analyzer")
def analyzer():
    logger.info(Fore.YELLOW + "[ Info ]  Analyzer template Loaded")
    return render_template("analyzer.html")

# Document Analyzer

## TODO : check Document File Type and Format and Extensions and Interior of File for Unwanted Data


@app.route("/analyzer/files" , methods=["POST"])
def post_document_analyzer():
   # logger.info(Fore.YELLOW + "[ Info ]  User start to Analyze Document")
    path = request.form["docfile"]
    files = glob.glob(f"{path}/**/*.txt" , recursive=True)
    for file in files:
        with open(file,"r") as readfile:
            result = readfile.read()
            if re.search("encrypt",result) or re.search("decrypt",result) or re.search("crypt",result) or re.search("hacked" , result):
                #logger.critical(Fore.RED + "Malicious File Detected [ERROR]")
                with open(f"/home/{username}/KYGnus_Map/Analyze_results.txt" , "w") as af:
                    af.write("Malicious File Detected [ERROR]")
                    af.close()
            else:
                with open(f"/home/{username}/KYGnus_Map/Analyze_results.txt" , "w") as af:
                    af.write("File check [ OK ]")
                    af.close()
                #logger.info(Fore.CYAN + "File check [ OK ]")
    return Response(f"<body style='background-color:white;'><center><h2 style='color:red;''> File Checked </h2><h1> Results saved in app Directory </h1><h3> app Directory is {appdir}</h3></center></body>")

        


# maps
@app.route("/maps")
def maps():
    logger.info("system File Manager is Loaded in maps Directory")
    maps = os.popen(f"xdg-open /home/{username}/work/Test/Mapper/mapper/templates/maps").read()
    return maps







if __name__ == "__main__" :
    app.run(port=8080 , debug=True)
