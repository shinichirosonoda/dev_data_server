import json
import requests

# ipアドレスを取得、表示
import socket
host = socket.gethostname()
print(host)
ip = socket.gethostbyname(host)
print(ip)


board_id = "2209-05"
file_name = "2209-05.csv"
flag ="False"


# JSONに格納
json_data = json.dumps({'board_id': board_id, "file_name": file_name, "flag": flag}).encode('utf-8')

# HTTPリクエストを送信
response = requests.post("http://localhost:8080/data_create", data=json_data)
#response = requests.get("http://localhost:8080/")
    
    
#print('{0} printer_id:{1}'.format(response.status_code, json.loads(response.text)["printer_id"]))
#print('{0} value:{1}'.format(response.status_code, json.loads(response.text)["value"]))
print(response)