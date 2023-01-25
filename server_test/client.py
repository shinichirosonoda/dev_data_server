import json
import requests

board_id = "2209-05"
file_name = "2209-05.csv"
flag ="False"


# JSONに格納
json_data = json.dumps({'board_id': board_id, "file_name": file_name, "flag": flag}).encode('utf-8')

# HTTPリクエストを送信
response = requests.post("http://localhost:8080/data_create", data=json_data)
response = requests.post("http://localhost:8080/pick_up_data", data=json_data)
print(response.text)

flag ="True"
# JSONに格納
json_data = json.dumps({'board_id': board_id, "file_name": file_name, "flag": flag}).encode('utf-8')
response = requests.post("http://localhost:8080/update_data", data=json_data)
response = requests.post("http://localhost:8080/pick_up_data", data=json_data)
print(response.text)

response = requests.post("http://localhost:8080//delete_data", data=json_data)
response = requests.post("http://localhost:8080/pick_up_data", data=json_data)
print(response.text)
