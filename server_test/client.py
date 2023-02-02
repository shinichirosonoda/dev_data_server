import json
import requests

# JSONに格納
dict_data = {"sample_name": "1w01",\
             "board_id": "2209-05",\
             "file_name": "2023-02-02_13-27-00_1w01.csv",\
             "mes_mode": "start"}
json_data = json.dumps(dict_data).encode('utf-8')

# HTTPリクエストを送信
response = requests.post("http://localhost:8080/data_create", data=json_data)
print(response.text)