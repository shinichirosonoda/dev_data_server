from flask import Flask, render_template, request, jsonify, Response
from flask_httpauth import HTTPBasicAuth

from io import BytesIO
import urllib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

"""
from data_load import draw_multi_graph2, get_all_sample_name,\
                      get_information, get_information_init
"""
from data_load import draw_multi_graph2, get_all_sample_name_db,\
                      get_information, get_information_init
                      
import sys
import ctypes
import os

import json
import argparse

# data logging setting
parser = argparse.ArgumentParser(description='mems_server')
parser.add_argument('-db_init', help='db_init', action='store_true')

args = parser.parse_args()

# DBの初期化
if args.db_init:
    from db_init import db_init_main
    db_init_main()

from db_control import data_create_board, data_create_fov,\
                       pick_up_board_id, pick_up_sample_name, pick_up_id

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
    #sample_list = get_all_sample_name(func)
    sample_list = get_all_sample_name_db(func)
    return jsonify({'sample_list': sample_list})

@app.route("/board_list", methods=['post'])
def board_list():
    board_list = ["2112-01", "2203-04",\
                  "2209-05", "2209-06", "2209-07", "2209-08", "2209-09", "2209-11"]   
    return jsonify({"board_list": board_list})

# DB
@app.route('/data_create_board', methods=['POST'])
def f_data_create_board():
    # jsonから変換
    data_json = request.data.decode('utf-8')
    data_dict = json.loads(data_json)

    # DBにレコードを作成
    id = data_create_board(data_dict)

    # HTTPレスポンスを送信
    return Response(response=json.dumps({"id": id}), status=200)

@app.route('/data_create_fov', methods=['POST'])
def f_data_create_fov():
    # jsonから変換
    data_json = request.data.decode('utf-8')
    data_dict = json.loads(data_json)

    # DBにレコードを作成
    id = data_create_fov(data_dict)

    # HTTPレスポンスを送信
    return Response(response=json.dumps({"id": id}), status=200)
    

@app.route('/pick_up_board_id', methods=['POST'])
def f_pick_up_board_id():
    # jsonから変換
    data_json = request.data.decode('utf-8')
    data_dict = json.loads(data_json)
    board_id = data_dict["board_id"]
    path = data_dict["path"]
    
    # DBを読み出し   
    data = pick_up_board_id(board_id, path)

    return Response(response=json.dumps(data), status=200)

@app.route('/pick_up_sample_name', methods=['POST'])
def f_pick_up_sample_name():
    # jsonから変換
    data_json = request.data.decode('utf-8')
    data_dict = json.loads(data_json)
    sample_name = data_dict["sample_name"]
    path = data_dict["path"]
    
    # DBを読み出し   
    data = pick_up_sample_name(sample_name, path)

    return Response(response=json.dumps(data), status=200)

@app.route('/pick_up_id', methods=['POST'])
def f_pick_up_id():
    # jsonから変換
    data_json = request.data.decode('utf-8')
    data_dict = json.loads(data_json)
    id = data_dict["id"]
    path = data_dict["path"]
    
    # DBを読み出し   
    data = pick_up_id(id, path)

    return Response(response=json.dumps(data), status=200)




if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)