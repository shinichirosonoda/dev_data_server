import os
import json
import cv2
import base64
import numpy as np
from datetime import datetime
from flask import Flask, request, Response
import time
import glob
import shutil

app = Flask(__name__)

# DBの初期化
from sqlite.db_init import db_init_main
db_init_main()

from sqlite.db_control import data_create, pick_up_data, pick_up_status_data, update_data2

# 古い画像の保存とフォルダのリセット
image_dir = "./images"
old_dir = "./images_old"


if os.path.isdir(old_dir):
  shutil.rmtree(old_dir)

if not os.path.isdir(image_dir):
  os.mkdir(image_dir)
else:
  shutil.move(image_dir, old_dir)
  os.mkdir(image_dir)

# データの変換処理
def json2img(data):
    data_json = json.loads(data)
    image = data_json['image']
    image_dec = base64.b64decode(image)
    data_np = np.frombuffer(image_dec, dtype='uint8')
    decimg = cv2.imdecode(data_np, 1)
    return decimg

def json2printer_id(data):
    data_json = json.loads(data)
    printer_id = data_json['printer_id']
    return printer_id

@app.route('/print', methods=['POST'])
def print_image():
    
    # データの変換処理
    data = request.data.decode('utf-8')
    decimg = json2img(data)
    printer_id = json2printer_id(data)

    # DBにレコードを作成
    id = data_create(printer_id, "", "Stanby", "")
    #print('id= ',id)

    # 画像ファイルを保存
    filename =  "./images/image_{}.png".format(id)
    cv2.imwrite(filename, decimg)
    
    # DBに登録
    update_data2(id, filename, "False")
    #print('id= ',id)
    
    # HTTPレスポンスを送信
    return Response(response=json.dumps({"message": "{} was recieved".format(filename)}), status=200)
    

@app.route('/remain_num', methods=['POST'])
def remain_num():
    # データの変換処理
    data = request.data.decode('utf-8')
    printer_id = json2printer_id(data)
    
    # DBを読み出し   
    data = pick_up_status_data(printer_id)

    # data取り出し   
    printer_id = data[0][1]
    value = data[0][2]

    return Response(response=json.dumps({"printer_id": printer_id,
                                         "value": value}), status=200)

@app.route('/status', methods=['POST'])
def printer_status():
    # データの変換処理
    data = request.data.decode('utf-8')
    printer_id = json2printer_id(data)
    
    # DBを読み出し   
    data = pick_up_status_data(printer_id)

    # data取り出し   
    printer_id = data[0][1]
    status = (data[0][3] == "True")

    return Response(response=json.dumps({"printer_id": printer_id,
                                         "status": status}), status=200)

@app.route('/SN', methods=['POST'])
def printer_SN():
    # データの変換処理
    data = request.data.decode('utf-8')
    printer_id = json2printer_id(data)
    
    # DBを読み出し   
    data = pick_up_status_data(printer_id)

    # data取り出し   
    printer_id = data[0][1]
    SN = data[0][4]

    return Response(response=json.dumps({"printer_id": printer_id,
                                         "SN": SN}), status=200)


if __name__ == '__main__':
    # ipアドレスを取得、表示
    import socket
    host = socket.gethostname()
    print(host)
    ip = socket.gethostbyname(host)
    print(ip)

    app.run(host=str(ip), port=8080, debug=False)
