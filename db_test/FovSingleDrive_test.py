import datetime
import json
from db_control import data_create_single

if __name__ == '__main__':
    # condition load
    json_open = open('mes_conf.json', 'r')
    json_dict = json.load(json_open)

    conf = "1"
    mes_conf = json_dict[conf]

    # sample name
    sample_name = "TT2222222"

    # save file setting
    dir_name = "log"
    datetime_initial = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    csv_file_name = "{}/{}_voltage_scan_{}.csv".format(dir_name, datetime_initial, sample_name)
    #df = DataLogging.data_save_init(cols=["as_slow", "angle", "word", "volt", "phase", "vpp", "temp", "humidity", "time"])

    csv_file_name2 = "{}/{}_Q_scan_{}.csv".format(dir_name, datetime_initial, sample_name)
    #df2 = DataLogging.data_save_init(cols=["as_slow", "angle", "word", "volt", "phase", "vpp", "temp", "humidity", "time"])

    json_file_name = "{}/{}_condition_{}.json".format(dir_name, datetime_initial, sample_name)

    # board_id
    board_id = '2112-01'
    print("board_id:", board_id)
    #fov = FovSingeScan(board_id, df, df2)

    # equip_id
    #print("equip_id:", fov.fov.equip["equip_id"])

    # camera_id
    #print("camera_id:", fov.fov.equip["camera_id"])
        
    # fast axis scan
    start_word0 = 27877
    target_phase0 = 3700
    start_volt0, stop_volt0 =6.5, 11.5

    start_word = mes_conf["fast"]["start_word"]
    target_phase =  mes_conf["fast"]["target_phase"]
    start_volt, stop_volt =mes_conf["fast"]["volt"][0],  mes_conf["fast"]["volt"][1]

    assert start_word0 == start_word, "start_word false"
    assert target_phase0 == target_phase, "target_phase false"
    assert start_volt0 == start_volt, "start_volt false"
    assert stop_volt0 ==  stop_volt, " stop_volt false"

    #volt, angle, word = \
    #fov.total_scan(start_word, start_volt, stop_volt, target_phase, as_slow=False, draw_option=False)
    #print(volt, angle, word)
    
    #fov.q_scan(word, volt, word_width = 15, word_step = 1.0, asym = 0.5, as_slow=False)
    word_width = mes_conf["fast"]["word_width"]
    word_step = mes_conf["fast"]["word_step"]
    asym = mes_conf["fast"]["asym"]

    print(word_width, word_step, asym)

    # slow axis scan
    start_word0 = 13892
    target_phase0 = 7500
    start_volt0, stop_volt0 =9.0, 14.5

    start_word = mes_conf["slow"]["start_word"]
    target_phase =  mes_conf["slow"]["target_phase"]
    start_volt, stop_volt =mes_conf["slow"]["volt"][0],  mes_conf["slow"]["volt"][1]

    assert start_word0 == start_word, "start_word false"
    assert target_phase0 == target_phase, "target_phase false"
    assert start_volt0 == start_volt, "start_volt false"
    assert stop_volt0 ==  stop_volt, " stop_volt false"
    
    #volt, angle, word = \
    #fov.total_scan(start_word, start_volt, stop_volt, target_phase, as_slow=True, draw_option=False)
    #print(volt, angle, word)

    #fov.q_scan(word, volt, word_width = 7, word_step = 0.5, asym = 0.0, as_slow=True)

    word_width = mes_conf["slow"]["word_width"]
    word_step = mes_conf["slow"]["word_step"]
    asym = mes_conf["slow"]["asym"]

    print(word_width, word_step, asym)

    # save file
    #DataLogging.data_save_to_file(fov.df, file_name= csv_file_name) 
    #DataLogging.data_save_to_file(fov.df2, file_name= csv_file_name2) 
    with open(json_file_name, 'w') as f:
        json.dump(mes_conf, f, ensure_ascii=False)


    # get Q_factor
    #fov.df2["as_slow"] = (fov.df2["as_slow"] == "True") # str -> bool type convert
    #Q_fast, x_peak_fast, x_th_min_fast, x_th_max_fast = fov.get_Q_factor(fov.df2, as_slow=False)
    #Q_slow, x_peak_slow, x_th_min_slow, x_th_max_slow = fov.get_Q_factor(fov.df2, as_slow=True)

    #print("fast Q, peak, min ,max:", Q_fast, x_peak_fast, x_th_min_fast, x_th_max_fast)
    #print("slow Q, peak, min ,max:", Q_slow, x_peak_slow, x_th_min_slow, x_th_max_slow)

    # get sensor data
    #temp, humidity =  fov.P.sensor.temperature, fov.P.sensor.humidity
    #print("temp, humidity:", temp, humidity)
