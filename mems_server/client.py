import json
import requests

db_path1 = './db/mems_board.db'
db_path2 = './db/mems_fov.db'
db_path3 = './db/mems_single.db'

# JSONに格納
dict_data = {"sample_name": "1w01",\
             "board_id": "2209-05",\
             "file_name": "2023-02-02_13-27-00_1w01.csv",\
             "mes_mode": "start"}
json_data = json.dumps(dict_data).encode('utf-8')

# HTTPリクエストを送信
response = requests.post("http://localhost:8080/data_create_board", data=json_data)
id = response.json()["id"]
print(id)

dict_data = {"id": id, "path": db_path1}
json_data = json.dumps(dict_data).encode('utf-8')

response = requests.post("http://localhost:8080/pick_up_id", data=json_data)
data = response.json()
print(data)

sample_name = data[0][1]
board_id = data[0][2]

# JSONに格納
dict_data = {"experiment_id": id,
        "sample_name": sample_name,
        "board_id": board_id,
        "fov_id":  "LTE-01",
        "camera_id": "AA01234",
        "file_name": "2023-02-02_13-27-00_1w01_fov.csv"}

json_data = json.dumps(dict_data).encode('utf-8')
response = requests.post("http://localhost:8080/data_create_fov", data=json_data)
id = response.json()["id"]
print(id)

dict_data = {"id": id, "path": db_path2}
json_data = json.dumps(dict_data).encode('utf-8')

response = requests.post("http://localhost:8080/pick_up_id", data=json_data)
data = response.json()
print(data)


# JSONに格納
dict_data = {"sample_name":       "1w01",
             "fast_word":         28000,
             "slow_word":         14000,
             "fast_volt":         7.5,
             "slow_volt":         10.0,
             "Q_fast":            2000.0,
             "Q_slow":            4000.0,
             "temperature":       25.0,
             "humidity":          45.0,          
             "board_id":          "2209-05",
             "equip_id":          "LTE-01",
             "camera_id":         "AA01234",
             "scan_file_name":    "scan_file.csv",
             "Q_scan_file_name":  "Q_scan.csv",
             "config_file_name":  "config.json"
            }

json_data = json.dumps(dict_data).encode('utf-8')
response = requests.post("http://localhost:8080/data_create_single", data=json_data)
id = response.json()["id"]
print(id)

dict_data = {"id": id, "path": db_path3}
json_data = json.dumps(dict_data).encode('utf-8')

response = requests.post("http://localhost:8080/pick_up_id", data=json_data)
data = response.json()
print(data)
