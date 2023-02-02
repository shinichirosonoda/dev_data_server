import json
from flask import Flask, request, Response

app = Flask(__name__)

# DBの初期化
from db_init import db_init_main
db_init_main()

from db_control import data_create_board, data_create_fov,\
                       pick_up_board_id, pick_up_sample_name, pick_up_id

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)