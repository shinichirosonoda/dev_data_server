#app.py
#from cgitb import text
#from telnetlib import XASCII
from flask import Flask, render_template, request, jsonify
from flask_httpauth import HTTPBasicAuth

from io import BytesIO
import urllib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

from data_load import draw_multi_graph2, get_all_sample_name,\
                      get_information, get_information_init

import sys
import ctypes
import os

# Set title
title = "MEMS server"
if os.name == 'nt':
    ctypes.windll.kernel32.SetConsoleTitleW(title) # Windows
else:
    sys.stdout.write("\x1b]2;" + title +"\x07") # Linux

# Flask server
app = Flask(__name__)

auth = HTTPBasicAuth()
users = {"senken1": "2022mems"}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route("/")
@auth.login_required
def index():
    return render_template("index.html")

@app.route("/plot", methods=['post'])
def plot_graph(func='2209-05_latest'):
    func, mode, start_point, stop_point ,sample_name = \
    request.json["func"], request.json["mode"], request.json["start_point"], request.json["stop_point"],\
    request.json["sample_name"]

    func = func.split('_')[0]
    fig = Figure(figsize=(20,20))
    
    if sample_name == "":
        sample_name, _, _ , _= get_information(func, sample_name, flag=False)
    else:
        sample_name, _, _ , _= get_information(func, sample_name, flag=True)
    
    if mode == "latest":
        fig = draw_multi_graph2(fig, board_name=func, sample=sample_name,\
              start_point=1, stop_point=1)
    elif mode == "all": 
        fig = draw_multi_graph2(fig, board_name=func, sample=sample_name,\
              start_point=int(start_point), stop_point=int(stop_point))
    
    canvas = FigureCanvasAgg(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    img_data = urllib.parse.quote(png_output.getvalue())
    return img_data

@app.route("/sample", methods=['post'])
def draw_sample(func='2209-05'):
    func , mode, start_point, stop_point, sample_name = \
    request.json["func"], request.json["mode"], request.json["start_point"], request.json["stop_point"],\
    request.json["sample_name"]

    if sample_name == "":
        sample_name, start_time, stop_time, max_num = get_information(func, sample_name, flag=False)
    else:
        sample_name, start_time, stop_time, max_num = get_information(func, sample_name, flag=True)
    
    if mode == "all":
        start_point, stop_point = int(start_point), int(stop_point)
    else:
        start_point, stop_point = 1, 1

    sample_name , start_time, stop_time = get_information_init(func, sample_name, start_point=int(start_point), stop_point=int(stop_point))
    
    return jsonify({"sample":"sample: " + sample_name, "start_time":"start_time: " + start_time,\
                    "stop_time":"stop_time: " + stop_time, "max_num": max_num})

@app.route("/list", methods=['post'])
def list():
    func = request.json["func"]
    sample_list = get_all_sample_name(func)
    return jsonify({'sample_list': sample_list})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)