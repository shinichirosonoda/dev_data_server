import pandas as pd
from single_search_load import get_all_single_search_files_db, single_scan_dataframe,\
                               original_scan_data_dataframe

from fov_data_load import get_all_fov_data_files

from db_control import pick_up_board_id,\
                       pick_up_board_id_mes_mode, pick_up_sample_board_id_mes_mode

db_path1 = './db/mems_board.db'
db_path2 = './db/mems_fov.db'

items_1 = ["2x", "2y",\
           "delay_fast", "delay_slow", "vpp_sum2", "vpp_sum1", "Ch1_word", "Ch2_word", "Ch1_Amp", "Ch2_Amp",\
           "fast_vpp_freq", "slow_vpp_freq", "fast_phase_freq", "slow_phase_freq",\
           "fast_vpp_list", "slow_vpp_list", "fast_phase_list", "slow_phase_list"]

items_2 = ["temperature", "temperature",\
           "temperature", "temperature", "temperature", "temperature", "temperature", "temperature", "temperature", "temperature",\
           "temperature", "temperature", "temperature", "temperature", "", "", "", ""]

color =["b", "r", "b", "r", "b", "r", "b", "r", "b", "r", "b", "r", "b", "r", "", "", "", ""]

axis_1 = ["Angle(deg)", "Angle(deg)",\
          "Phase (clocks)", "Phase (clocks)", "Vpp (14bit x 100)", "Vpp (14bit x 100)",\
          "Frequency (word)", "Frequency (word)", "Voltage (volt)", "Voltage (volt)",\
          "Frequency (word)", "Frequency (word)", "Frequency (word)", "Frequency (word)",\
          "Vpp (14bit)", "Vpp (14bit)", "Phase (clocks)", "Phase (clocks)"]

axis_2 = ["Temperature (deg)", "Temperature (deg)",\
          "Temperature (deg)", "Temperature (deg)", "Temperature (deg)", "Temperature (deg)",\
          "Temperature (deg)", "Temperature (deg)", "Temperature (deg)", "Temperature (deg)",\
          "Temperature (deg)", "Temperature (deg)", "Temperature (deg)", "Temperature (deg)",\
          "", "", "", ""]

titles = ["Fast FOV angle", "Slow FOV angle",\
          "Phase_fast", "Phase_slow", "Vpp_fast", "Vpp_slow",\
          "Frequency_fast", "Frequency_slow", "Voltage_fast", "Voltage_slow",\
          "Peak search using Vpp fast", "Peak search using Vpp slow", "Peak search using phase fast", "Peak search using phase slow",
          "Fast Vpp at Single axis Scan", "Slow Vpp at Single axis Scan",\
          "Fast phase at Single axis Scan", "Slow phase at Single axis Scan"]

x_axis_label = ["Time", "Time",\
                "Time", "Time", "Time", "Time",\
                "Time", "Time", "Time", "Time",\
                "Time", "Time", "Time", "Time",\
                "fast_freq_list", "slow_freq_list",\
                "fast_freq_list", "slow_freq_list"]

x_axis_label_title = ["Time", "Time",\
                      "Time", "Time", "Time", "Time",\
                      "Time", "Time", "Time", "Time",\
                      "Time", "Time", "Time", "Time",\
                      "Frequency (word)", "Frequency (word)",\
                      "Frequency (word)", "Frequency (word)"]


def get_all_sample_name_db(board_name):
    list1 = [x[1] for x in pick_up_board_id(board_name, db_path1)]
    list2 = sorted(set(list1), key=list1.index)
    list2.reverse()
    return list2


def get_latest_file_db(board_name):
    try:
        list1 = [x[3] for x in pick_up_board_id_mes_mode(board_name, "start", db_path1)]
        return list1[-1]
    except:
        return

def get_all_files_db(board_name, sample, start_num = 1, stop_num = 1000000):
    files = [x[3] for x in pick_up_sample_board_id_mes_mode(sample, board_name, "start", db_path1)]
    end_point =  len(files) - start_num + 1
    strat_point = len(files) - stop_num

    if strat_point < 0:
        strat_point = 0
    if strat_point > end_point:
        strat_point = end_point

    files = [file  for file in files[strat_point:end_point] ]

    return files

def get_dataframe(file_name):
    if file_name is not None:
        df = pd.read_csv(file_name, index_col=0)
        return df

def get_information(board_name, sample_name, flag=True):
    file_name = get_latest_file_db(board_name)
   
    if file_name is None:
        return "","","",""

    df = pd.read_csv(file_name, index_col=0)
    
    if flag == False:
        sample_name = (lambda file: file.split('_')[-1][:-4])(file_name)

    max_num = len(get_all_files_db(board_name, sample_name))
    start_time = df["Time"][0]
    stop_time = df["Time"][len(df["Time"])-1]
    return sample_name, start_time, stop_time, max_num

def get_information_init(board_name, sample, start_point=1, stop_point=10000):
    file_name =  get_all_files_db(board_name, sample)
    if file_name == []:
        return "","",""
        
    start = len(file_name) - stop_point
    stop = len(file_name) - start_point
    
    if start <  0:
       start = 0
    if stop >  len(file_name) - 1:
       stop = len(file_name) - 1

    try:
        file_name_start = get_all_files_db(board_name, sample)[start]
        file_name_stop = get_all_files_db(board_name, sample)[stop]
        df_start = pd.read_csv(file_name_start, index_col=0)
        df_stop = pd.read_csv(file_name_stop, index_col=0)
        sample_name = (lambda file: file.split('_')[-1][:-4])(file_name_start)
        start_time = df_start["Time"][0]
        stop_time = df_stop["Time"][len(df_stop["Time"])-1]
        return sample_name, start_time, stop_time
    except:
        return "", "", ""


def draw_graph2(df_array, i, ax1, fig, df_array_sub = None):
    if df_array == []:
        return

    ax2 = ax1.twinx()

    ax1.set_xlabel("Time", size=10)
    ax1.set_ylabel(axis_1[i], size=10)
    ax2.set_ylabel(axis_2[i], size=10)

    time_start = pd.to_datetime(df_array[0]["Time"])
    time_stop = pd.to_datetime(df_array[len(df_array)-1]["Time"])
    xmin = time_start[0]
    xmax = time_stop[len(time_stop)-1]

    ax1.tick_params(axis='x', labelsize=8)
    ax1.tick_params(axis='y', labelsize=8)
    ax2.tick_params(axis='y', labelsize=8)

    ax1.set_title(titles[i], size=10)
    fig.subplots_adjust(wspace=0.3, hspace=0.5)
    ax1.set_xlim(xmin,xmax)
    ax1.set_xticks([xmin, xmax]) 
    ax1.set_xticklabels([xmin, xmax])

    if df_array_sub is not None:
        df_array = df_array_sub
    
    if df_array == []:
        return

    for df in df_array:
        time = pd.to_datetime(df["Time"])
        ax1.plot(time, df[items_1[i]], color=color[i])
        ax2.plot(time, df[items_2[i]], color="g")

    

def draw_graph3(df_array, i, ax1, fig):
    if df_array == []:
        return

    ax1.set_xlabel(x_axis_label_title[i], size=10)
    ax1.set_ylabel(axis_1[i], size=10)

    ax1.tick_params(axis='x', labelsize=8)
    ax1.tick_params(axis='y', labelsize=8)
    
    ax1.set_title(titles[i], size=10)
    fig.subplots_adjust(wspace=0.3, hspace=0.5)

    for df in df_array:
        ax1.plot(df[x_axis_label[i]], df[items_1[i]])

def draw_graph4(df_array, i, ax1, fig, df_array_sub = None):
    if df_array == []:
        return

    ax2 = ax1.twinx()

    ax1.set_xlabel("Time", size=10)
    ax1.set_ylabel(axis_1[i], size=10)
    ax2.set_ylabel(axis_2[i], size=10)

    time_start = pd.to_datetime(df_array[0]["Time"])
    time_stop = pd.to_datetime(df_array[len(df_array)-1]["Time"])
    xmin = time_start[0]
    xmax = time_stop[len(time_stop)-1]

    ax1.tick_params(axis='x', labelsize=8)
    ax1.tick_params(axis='y', labelsize=8)
    ax2.tick_params(axis='y', labelsize=8)

    ax1.set_title(titles[i], size=10)
    fig.subplots_adjust(wspace=0.3, hspace=0.5)
    ax1.set_xlim(xmin,xmax)
    ax1.set_xticks([xmin, xmax]) 
    ax1.set_xticklabels([xmin, xmax])

    for df in df_array:
        time = pd.to_datetime(df["Time"])
        ax2.plot(time, df[items_2[i]], color="g")

    if df_array_sub is not None:
        df_array = df_array_sub
    
    if df_array == []:
        return

    for df in df_array:
        time = pd.to_datetime(df["Time"])
        ax1.plot(time, df[items_1[i]], color=color[i])

def draw_multi_graph2(fig, board_name="2209-05", sample="AT1910305", start_point=1, stop_point=10000):
    files = get_all_files_db(board_name, sample, start_num=start_point, stop_num=stop_point)
    df_array = []
    for file_name in files:
        df_array.append(get_dataframe(file_name))

    files4 = get_all_fov_data_files(board_name, sample)
    df_array4 = []
    for file_name in files4:
        df_array4.append(get_dataframe(file_name))

    for i in range(2):
        ax = fig.add_subplot(9, 2, i+1)
        draw_graph4(df_array, i, ax, fig, df_array_sub=df_array4)

    for i in range(2, 10):
        ax = fig.add_subplot(9, 2, i+1)
        draw_graph2(df_array, i, ax, fig)
    files2 = get_all_single_search_files_db(board_name, sample)
    df_array2 = [single_scan_dataframe(files2)]

    for i in range(10, 14):
        ax = fig.add_subplot(9, 2, i+1)
        draw_graph2(df_array, i, ax, fig, df_array_sub=df_array2)
    
    files3 = get_all_single_search_files_db(board_name, sample)
    df_array3 = original_scan_data_dataframe(files3)
    
    for i in range(14, 18):
        ax = fig.add_subplot(9, 2, i+1)
        draw_graph3(df_array3, i, ax, fig)
    
    return fig

if __name__ == '__main__':
    board_name = "2209-05"
    print(get_all_sample_name(board_name), get_all_sample_name_db(board_name))
    assert get_all_sample_name(board_name) == get_all_sample_name_db(board_name)
    print(get_latest_file(board_name), get_latest_file_db(board_name))
    #assert get_latest_file(board_name) == get_latest_file_db(board_name)
    sample ='AT1910305'
    print(get_all_files(board_name, sample, start_num = 10, stop_num = 11))
    print(get_all_files_db(board_name, sample, start_num = 10, stop_num = 11))