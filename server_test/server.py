import json
from flask import Flask, request, Response

app = Flask(__name__)

# DBの初期化
from db_init import db_init_main
db_init_main()

from db_control import data_create_board, data_create_fov,\
                       pick_up_board_id, pick_up_sample_name, pick_up_id

def json2data(data):
    data_json = json.loads(data)
    board_id, file_name, flag = data_json['board_id'], data_json['file_name'], data_json['flag']
    return board_id, file_name, flag

def data2json(board_id, file_name, flag, time):
    return json.dumps({"board_id":"{}".format(board_id),\
                       "file_name":"{}".format(file_name),\
                       "flag":"{}".format(flag),\
                       "time":"{}".format(time)})


@app.route('/data_create_board', methods=['POST'])
def f_data_create_board():
    # jsonから変換
    data_json = request.data.decode('utf-8')
    data_dict = json.loads(data_json)

    print(data_json)

    # DBにレコードを作成
    id = data_create_board(data_dict)
    print('id= ',id)

    # HTTPレスポンスを送信
    return Response(response=json.dumps({"message": "{} was recieved".format(id)}), status=200)

@app.route('/data_create_fov', methods=['POST'])
def f_data_create_fov():
    # jsonから変換
    data_json = request.data.decode('utf-8')
    data_dict = json.loads(data_json)

    print(data_json)

    # DBにレコードを作成
    id = data_create_fov(data_dict)
    print('id= ',id)

    # HTTPレスポンスを送信
    return Response(response=json.dumps({"message": "{} was recieved".format(id)}), status=200)
    

@app.route('/pick_up_board_id', methods=['POST'])
def f_pick_up_board_id():
    # jsonから変換
    data_json = request.data.decode('utf-8')
    data_dict = json2data(data_json)
    board_id = data_dict["board_id"]
    
    # DBを読み出し   
    data = pick_up_board_id(board_id)
    print(data)

    return Response(response=data, status=200)

@app.route('/pick_up_sample_name', methods=['POST'])
def f_pick_up_sample_name():
    # jsonから変換
    data_json = request.data.decode('utf-8')
    data_dict = json2data(data_json)
    sample_name = data_dict["sample_name"]
    
    # DBを読み出し   
    data = pick_up_sample_name(sample_name)
    print(data)

    return Response(response=data, status=200)

@app.route('/pick_up_id', methods=['POST'])
def f_pick_up_id():
    # jsonから変換
    data_json = request.data.decode('utf-8')
    data_dict = json2data(data_json)
    id = data_dict["id"]
    
    # DBを読み出し   
    data = pick_up_id(id)
    print(data)

    return Response(response=data, status=200)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)