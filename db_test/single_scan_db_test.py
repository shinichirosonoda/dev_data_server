import json
from db_control import data_create_single

json_open = open('mes_conf.json', 'r')
json_dict = json.load(json_open)

conf = "1"
mes_conf = json_dict[conf]

# fast axis scan
fast_start_word = mes_conf["fast"]["start_word"]
fast_delta_word = mes_conf["fast"]["delta_word"]
fast_scan_word =  mes_conf["fast"]["scan_word"]
fast_target_phase = mes_conf["fast"]["target_phase"]
fast_start_volt, fast_stop_volt = mes_conf["fast"]["volt"][0],  mes_conf["fast"]["volt"][1]

# slow axis scan
slow_start_word = mes_conf["slow"]["start_word"]
slow_delta_word =  mes_conf["slow"]["delta_word"]
slow_scan_word = mes_conf["slow"]["scan_word"]
slow_target_phase = mes_conf["slow"]["target_phase"]
slow_start_volt, slow_stop_volt =  mes_conf["slow"]["volt"][0],  mes_conf["slow"]["volt"][1]

# Q measurement condition
fast_word_width = mes_conf["fast"]["word_width"]
fast_word_step = mes_conf["fast"]["word_step"]
fast_asym = mes_conf["fast"]["asym"]
slow_word_width = mes_conf["slow"]["word_width"]
slow_word_step = mes_conf["slow"]["word_step"]
slow_asym = mes_conf["slow"]["asym"]

# sample name
sample_name = "TT2222222"

# search scan file name
csv_file_name = "test.csv"

# Q scan file name
csv_file_name2 = "test_Q.csv"

# config file name
json_file_name = "test_config.json"


# board_id
board_id = '2112-01'

# equip_id
equip_id = "lte1"

# camera_id
camera_id = "AA12345678"

# resonance condition
fast_word = 280000
fast_volt = 7.5
slow_word =14000
slow_volt = 10.0
        
# fast Q, peak, min ,max
Q_fast, x_peak_fast, x_th_min_fast, x_th_max_fast =\
(1000, 28000, 27900, 28100)

#slow Q, peak, min ,max:
Q_slow, x_peak_slow, x_th_min_slow, x_th_max_slow =\
(2000, 14000, 13900, 14100)

# get sensor data
temp, humidity = 22.5, 45.0

# output
output_dict = {"sample_name":       sample_name,
               "fast_word":         fast_word,
               "slow_word":         slow_word,
               "fast_volt":         fast_volt,
               "slow_volt":         slow_volt,
               "Q_fast":            Q_fast,
               "Q_slow":            Q_slow,
               "temperature":       temp,
               "humidity":          humidity,          
               "board_id":          board_id,
               "equip_id":          equip_id,
               "camera_id":         camera_id,
               "scan_file_name":    csv_file_name,
               "Q_scan_file_name":  csv_file_name2,
               "config_file_name":  json_file_name
               }

#print(output_dict)
data = output_dict

print(data_create_single(data))