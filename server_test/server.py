import json
from flask import Flask, request, Response

app = Flask(__name__)

# DBの初期化
from db_init import db_init_main
db_init_main()

from db_control import data_create, pick_up_data, update_data, delete_data

def json2data(data):
    data_json = json.loads(data)
    board_id, file_name, flag = data_json['board_id'], data_json['file_name'], data_json['flag']
    return board_id, file_name, flag

def data2json(board_id, file_name, flag):
    return json.dumps({"board_id:{}, file_name:{}, flag:{}".format(board_id, file_name, flag)})


@app.route('/data_create', methods=['POST'])
def data_create():
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
def pick_up_data():
    # jsonから変換
    data = request.data.decode('utf-8')
    board_id, _, _ = json2data(data)
    
    # DBを読み出し   
    data = pick_up_data(board_id)

    # data取り出し   
    board_id, file_name, flag = data[0][0], data[0][1], data[0][2]

    # JSONに変換

    return Response(response=data2json(board_id, file_name, flag), status=200)

@app.route('/update_data', methods=['POST'])
def update_data():
    # jsonから変換
    data = request.data.decode('utf-8')
    board_id, file_name, flag = json2data(data)

    # DBにレコードを作成
    data = update_data(board_id, file_name, flag)

    # data取り出し   
    board_id, file_name, flag = data[0][0], data[0][1], data[0][2]

    return Response(response=data2json(board_id, file_name, flag), status=200)

@app.route('/delete_data', methods=['POST'])
def delete_data():
    # jsonから変換
    data = request.data.decode('utf-8')
    board_id, _, _ = json2data(data)
    
    # DBを読み出し   
    data = delete_data(board_id)

    return Response(response=data, status=200)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)