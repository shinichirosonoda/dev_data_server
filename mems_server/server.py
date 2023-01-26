from flask import Flask, render_template, request, jsonify, Response
from flask_httpauth import HTTPBasicAuth
import json

from io import BytesIO
import urllib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

from data_load import draw_multi_graph2, get_all_sample_name,\
                      get_information, get_information_init

import sys
import ctypes
import os

from db_control import data_create, pick_up_data, update_data, delete_data
from db_init import db_init_main

# DBの初期化
db_init_main()

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


# DB
@app.route('/data_create', methods=['POST'])
def f_data_create():
    # jsonから変換
    data = request.data.decode('utf-8')
    board_id, file_name, flag = json2data(data)
    print(board_id, file_name, flag)

    # DBにレコードを作成
    id = data_create(board_id, file_name, flag)
    print('id= ',id)

    # HTTPレスポンスを送信
    return Response(response=json.dumps({"message": "{} was recieved".format(id)}), status=200)
    

@app.route('/pick_up_data', methods=['POST'])
def f_pick_up_data():
    # jsonから変換
    data = request.data.decode('utf-8')
    board_id, _, _ = json2data(data)
    
    # DBを読み出し   
    data = pick_up_data(board_id)

    # data取り出し
    if data != []:
        board_id, file_name, flag , time= data[0][1], data[0][2], data[0][3], data[0][4]
    
        # JSONに変換
        data = data2json(board_id, file_name, flag, time)
        return Response(response=data, status=200)
    else:
        return Response(response="None", status=200)

@app.route('/update_data', methods=['POST'])
def f_update_data():
    # jsonから変換
    data = request.data.decode('utf-8')
    board_id, file_name, flag = json2data(data)

    # DBにレコードを作成
    data = update_data(board_id, file_name, flag)

    # data取り出し   
    board_id, file_name, flag , time= data[0][1], data[0][2], data[0][3], data[0][4]

    # JSONに変換
    data = data2json(board_id, file_name, flag, time)

    return Response(response=time, status=200)

@app.route('/delete_data', methods=['POST'])
def f_delete_data():
    # jsonから変換
    data = request.data.decode('utf-8')
    board_id, _, _ = json2data(data)
    
    # DBを読み出し   
    data = delete_data(board_id)

    return Response(response=data, status=200)

def json2data(data):
    data_json = json.loads(data)
    board_id, file_name, flag = data_json['board_id'], data_json['file_name'], data_json['flag']
    return board_id, file_name, flag

def data2json(board_id, file_name, flag, time):
    return json.dumps({"board_id":"{}".format(board_id),\
                       "file_name":"{}".format(file_name),\
                       "flag":"{}".format(flag),\
                       "time":"{}".format(time)})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)