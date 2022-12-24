#app.py
from cgitb import text
from telnetlib import XASCII
from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth

from io import BytesIO
import urllib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

from data_load import draw_multi_graph, draw_multi_graph2,\
                      get_information, get_information_init

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
    func, mode, start_point, stop_point = \
    request.json["func"], request.json["mode"], request.json["start_point"], request.json["stop_point"]

    func = func.split('_')[0]
    fig = Figure(figsize=(15,15))
    sample, _, _ = get_information(func)
    
    if mode == "latest":
        fig = draw_multi_graph2(fig, board_name=func, sample=sample,\
              start_point=-1)
    elif mode == "all":
        fig = draw_multi_graph2(fig, board_name=func, sample=sample,\
              start_point=start_point, stop_point=stop_point)
    
    canvas = FigureCanvasAgg(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    img_data = urllib.parse.quote(png_output.getvalue())
    return img_data

@app.route("/sample", methods=['post'])
def draw_sample(func='2209-05'):
    func = \
    request.json["func"], request.json["mode"], request.json["start_point"], request.json["stop_point"]
    sample, strat_point, stop_point = get_information(func)
    
    if mode == "all":
        _, strat_time, _ = get_information_init(func, sample, start_point=start_point, stop_point=stop_point)
    
    return jsonify({"sample":sample, "start_time":start_time, "stop_time":stop_time})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)