import json
from db_control import data_create_single

json_open = open('mes_conf.json', 'r')
json_dict = json.load(json_open)

conf = "condition1"

# fast axis scan
fast_start_word = json_dict[conf]["fast_start_word"]
fast_target_phase = json_dict[conf]["fast_target_phase"]
fast_start_volt, fast_stop_volt = json_dict[conf]["fast_volt"][0],  json_dict[conf]["fast_volt"][1]

# slow axis scan
slow_start_word = json_dict[conf]["slow_start_word"]
slow_target_phase = json_dict[conf]["slow_target_phase"]
slow_start_volt, slow_stop_volt = json_dict[conf]["slow_volt"][0],  json_dict[conf]["slow_volt"][1]

# Q measurement condition
fast_word_width = json_dict[conf]["fast_word_width"]
fast_word_step = json_dict[conf]["fast_word_step"]
fast_asym = json_dict[conf]["fast_asym"]
slow_word_width = json_dict[conf]["slow_word_width"]
slow_word_step = json_dict[conf]["slow_word_step"]
slow_asym = json_dict[conf]["slow_asym"]

# sample name
sample_name = "TT2222222"

# search scan file name
csv_file_name = "test.csv"

# Q scan file name
csv_file_name2 = "test_Q.csv"

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
               "scan_file_name":    csv_file_name,
               "Q_scan_file_name":  csv_file_name2,
               "board_id":          board_id,
               "equip_id":          equip_id,
               "camera_id":         camera_id,
               "fast_start_word":   fast_start_word,
               "fast_target_phase": fast_target_phase,
               "fast_start_volt":   fast_start_volt, 
               "fast_stop_volt":    fast_stop_volt,
               "slow_start_word":   slow_start_word,
               "slow_target_phase": slow_target_phase,
               "slow_start_volt":   slow_start_volt, 
               "slow_stop_volt":    slow_stop_volt,
               "fast_word_width":   fast_word_width,
               "fast_word_step":    fast_word_step,
               "fast_asym":         fast_asym,
               "slow_word_width":   slow_word_width,
               "slow_word_step":    slow_word_step,              
               "slow_asym":         slow_asym
               }

#print(output_dict)
data = output_dict

print(data_create_single(data))