import pandas as pd
import matplotlib.pyplot as plt
import glob

items = ["delay_fast", "delay_slow", "vpp_sum2", "vpp_sum1", "Ch1_word", "Ch2_word", "Ch1_Amp", "Ch2_Amp"]
color =["b", "r", "b", "r", "b", "r", "b", "r"]
axis = ["Phase (clocks)", "Phase (clocks)", "Vpp (14bit x 100)", "Vpp (14bit x 100)",\
             "Frequency (word)", "Frequency (word)", "Voltage (volt)", "Voltage (volt)"]
titles = ["Phase_fast", "Phase_slow", "Vpp_fast", "Vpp_slow",\
             "Frequency_fast", "Frequency_slow", "Voltage_fast", "Voltage_slow"]


def get_all_sample_name(board_name):
    try:
        path = select_path(board_name)
        files = sorted(glob.glob(path))
        sample_list = [str(file_name)[-13:-4] for file_name in files]
        sample_list = sorted(set(sample_list), key=sample_list.index)
        return sample_list
    except:
        return

def get_latest_file(board_name):
    try:
        path = select_path(board_name)
        files = sorted(glob.glob(path))
        return files[-1]
    except:
        return

def get_all_files(board_name, sample, start_num = 1, stop_num = 1000000):
    try:
        path = select_sample_path(board_name, sample)
        #print(path)
        files = sorted(glob.glob(path))
        
        end_point =  len(files) - start_num + 1
        strat_point = len(files) - stop_num

        if strat_point < 0:
           strat_point = 0
        if strat_point > end_point:
           strat_point = end_point

        files = [file  for file in files[strat_point:end_point] ]

        return files
    except:
        return

def select_path(name):
    return "../long_data/{}/*.csv".format(name)

def select_sample_path(name, sample):
    return "../long_data/{}/*_{}.csv".format(name, sample)

def get_dataframe(file_name):
    if file_name is not None:
        df = pd.read_csv(file_name, index_col=0)
        return df

def get_information(board_name):
    file_name = get_latest_file(board_name)
   
    if file_name is None:
        return "","","",""
    df = pd.read_csv(file_name, index_col=0)
    sample_name = str(file_name)[-13:-4]
    max_num = len(get_all_files(board_name, sample_name))
    start_time = df["Time"][0]
    stop_time = df["Time"][len(df["Time"])-1]
    return sample_name, start_time, stop_time, max_num

def get_information_init(board_name, sample, start_point=1, stop_point=10000):

    file_name =  get_all_files(board_name, sample)
    if file_name == []:
        return "","",""
        
    start = len(file_name) - stop_point
    stop = len(file_name) - start_point
    
    if start <  0:
       start = 0
    if stop >  len(file_name) - 1:
       stop = len(file_name) - 1

    try:   
        file_name_start = get_all_files(board_name, sample)[start]
        file_name_stop = get_all_files(board_name, sample)[stop]
        df_start = pd.read_csv(file_name_start, index_col=0)
        df_stop = pd.read_csv(file_name_stop, index_col=0)
        sample_name = str(file_name_start)[-13:-4]
        start_time = df_start["Time"][0]
        stop_time = df_stop["Time"][len(df_stop["Time"])-1]
        return sample_name, start_time, stop_time
    except:
        return "", "", ""


def draw_graph2(df_array, i, ax1, fig):
    if df_array == []:
        return
    ax2 = ax1.twinx()

    ax1.set_xlabel("Time", size=10)
    ax1.set_ylabel(axis[i], size=10)
    ax2.set_ylabel("Temperature (deg)", size=10)

    for df in df_array:
        time = pd.to_datetime(df["Time"])
        ax1.plot(time, df[items[i]], color=color[i])
        ax2.plot(time, df["temperature"], color="g")

    time_start = pd.to_datetime(df_array[0]["Time"])
    time_stop = pd.to_datetime(df_array[len(df_array)-1]["Time"])
    xmin = time_start[0]
    xmax = time_stop[len(time_stop)-1]

    ax1.tick_params(axis='x', labelsize=8)
    ax1.tick_params(axis='y', labelsize=8)
    ax2.tick_params(axis='y', labelsize=8)

    ax1.set_title(titles[i], size=10)
    fig.subplots_adjust(wspace=0.3, hspace=0.3)
    ax1.set_xlim(xmin,xmax)
    ax1.set_xticks([xmin, xmax]) 
    ax1.set_xticklabels([xmin, xmax])


def draw_multi_graph2(fig, board_name="2209-05", sample="AT1910305", start_point=1, stop_point=10000):
    files = get_all_files(board_name, sample, start_num=start_point, stop_num=stop_point)
    df_array = []
    for file_name in files:
        df_array.append(get_dataframe(file_name))

    for i in range(8):
        ax = fig.add_subplot(4, 2, i+1)
        draw_graph2(df_array, i, ax, fig)

    return fig


if __name__ == '__main__':

    print(get_information("2209-05"))
    file_name = get_latest_file("2209-05")
    print(file_name)
    fig = plt.figure(figsize=(15,15))
    fig = draw_multi_graph2(fig)
    plt.show()

    fig = plt.figure(figsize=(15,15))
    fig = draw_multi_graph(fig)
    plt.show()

    

    