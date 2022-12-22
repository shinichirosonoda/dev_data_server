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

def ax_set(fig, num):
    ax =fig.add_subplot(4, 2, num+1)
    ax.tick_params(axis='x', labelsize=4)
    ax.tick_params(axis='y', labelsize=4)
    return ax

@app.route("/plot/<func>")
def plot_graph(func='2209-05_latest'):
    mode = func.split('_')[1]
    start_point = int(func.split('_')[2])
    stop_point =  int(func.split('_')[3])

    func = func.split('_')[0]
    fig = Figure(figsize=(15,15))
    sample, _, _ = get_information(func)
    
    if mode == "latest":
        fig = draw_multi_graph(fig, board_name=func)
    elif mode == "all":
        fig = draw_multi_graph2(fig, board_name=func, sample=sample,\
              start_point=start_point, stop_point=stop_point)
    
    canvas = FigureCanvasAgg(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    img_data = urllib.parse.quote(png_output.getvalue())
    return img_data

@app.route("/sample/<func>")
def draw_sample(func='2209-05'):
    func = func.split('_')[0]
    sample, _, _ = get_information(func)
    return "sample: " + sample

@app.route("/start_time/<func>")
def draw_start_time(func='2209-05'):
    mode = func.split('_')[1]
    start_point = int(func.split('_')[2])
    stop_point =  int(func.split('_')[3])

    func = func.split('_')[0]
    sample,strat_time, _ = get_information(func)
    
    if mode == "all":
        _, strat_time, _ = get_information_init(func, sample, start_point=start_point, stop_point=stop_point)
    
    return "start: " + strat_time

@app.route("/stop_time/<func>")
def draw_stop_time(func='2209-05'):
    mode = func.split('_')[1]
    start_point = int(func.split('_')[2])
    stop_point =  int(func.split('_')[3])

    func = func.split('_')[0]
    sample, _, stop_time = get_information(func)
    
    if mode == "all":
        _, _, stop_time = get_information_init(func, sample, start_point=start_point, stop_point=stop_point)

    return "stop: " + stop_time

@app.route("/")
@auth.login_required
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)