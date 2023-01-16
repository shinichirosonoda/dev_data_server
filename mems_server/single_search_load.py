import glob
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime as dt


def select_sample_path(name, sample, file_type="csv"):
    return "../long_data/{}/*_{}.{}".format(name, sample, file_type)


def get_all_single_search_files(board_name, sample):
    try:
        path = select_sample_path(board_name, sample, file_type="txt")
        files = sorted(glob.glob(path))
        return files
    except:
        return

def median1d(arr, k=5):
    w = len(arr)
    idx = np.fromfunction(lambda i, j: i + j, (k, w), dtype=np.int32) - k // 2
    idx[idx < 0] = 0
    idx[idx > w - 1] = w - 1
    return np.median(arr[idx], axis=0)

def data_to_dict(data):
    slow_freq_list = np.array([int(_i) for _i in data.split("slow_freq_list[bit]")[1].\
                      split("slow_phase_list[clk]")[0].split("[")[1].split("]")[0].split(",")])
    slow_phase_list = np.array([float(_i) for _i in data.split("slow_phase_list[clk]")[1].\
                       split("slow_vpp_list[bit]")[0].split("[")[1].split("]")[0].split(",")])
    slow_vpp_list = np.array([float(_i) for _i in data.split("slow_vpp_list[bit]")[1].\
                     split("temperature[deg]")[0].split("[")[1].split("]")[0].split(",")])
    
    fast_freq_list = np.array([int(_i) for _i in data.split("slow_freq_list[bit]")[2].\
                      split("slow_phase_list[clk]")[0].split("[")[1].split("]")[0].split(",")])
    fast_phase_list = np.array([float(_i) for _i in data.split("slow_phase_list[clk]")[2].\
                       split("slow_vpp_list[bit]")[0].split("[")[1].split("]")[0].split(",")])
    fast_vpp_list = np.array([float(_i) for _i in data.split("slow_vpp_list[bit]")[2].\
                     split("temperature[deg]")[0].split("[")[1].split("]")[0].split(",")])

    sample_name = data.split("Sample_name")[1].split("res[bit]")[0].split(":")[1][2:-4]
    temperature = float(data.split("temperature[deg]")[1].split("humid[%]")[0].split(":")[1][1:-3])
    humidity = float(data.split("humid[%]")[1].split("}")[0][3:])
    
    return {"sample_name": sample_name,\
             "slow_freq_list": slow_freq_list, "slow_phase_list": slow_phase_list, "slow_vpp_list": slow_vpp_list,\
             "fast_freq_list": fast_freq_list, "fast_phase_list": fast_phase_list, "fast_vpp_list": fast_vpp_list,\
             "temperature":  temperature, "humidity": humidity}

def peak_serch(x_data, y_data):
    x = x_data[np.where(y_data==np.max(y_data))[0]][0]
    y = y_data[np.where(y_data==np.max(y_data))[0]][0]
    return x, y

def get_res_pos(data, th):
    return np.where((data > th*0.9) & (data < th*1.1))[0][0]


def get_peak(file_name, plot_draw=True):
    f = open(file_name, 'r')
    data_org = f.read()
    f.close()

    time_str = file_name.split("_")[-2].split("\\")[-1]
    tdatetime = dt.strptime(time_str, '%Y-%m-%d-%H-%M-%S')

    ex_data = data_to_dict(data_org)

    graph_list = [["slow_freq_list", "slow_vpp_list"], ["fast_freq_list", "fast_vpp_list"],\
              ["slow_freq_list", "slow_phase_list"], ["fast_freq_list", "fast_phase_list"]]

    graph_list3 = [["slow_freq_list", "slow_phase_list", 7500], ["fast_freq_list", "fast_phase_list", 3500]]
    

    data = {"slow_vpp": peak_serch(ex_data[graph_list[0][0]],  median1d(ex_data[graph_list[0][1]])) ,
            "fast_vpp": peak_serch(ex_data[graph_list[1][0]],  median1d(ex_data[graph_list[1][1]])) ,
            "slow_phase": (ex_data[graph_list3[0][0]][get_res_pos(ex_data[graph_list3[0][1]], graph_list3[0][2])],\
                           ex_data[graph_list3[0][1]][get_res_pos(ex_data[graph_list3[0][1]], graph_list3[0][2])]) ,
            "fast_phase": (ex_data[graph_list3[1][0]][get_res_pos(ex_data[graph_list3[1][1]], graph_list3[1][2])],\
                           ex_data[graph_list3[1][1]][get_res_pos(ex_data[graph_list3[1][1]], graph_list3[1][2])]) ,
            "temperature":  ex_data["temperature"], "humidity": ex_data["humidity"], "Time": tdatetime}


    if plot_draw is True:
        fig = plt.figure(figsize=(15,15))
        [rows, cols] = [2,2]
        axs = [ fig.add_subplot(rows, cols, i) for i in range(1,5) ]

        axs[0].plot(ex_data[graph_list[0][0]], median1d(ex_data[graph_list[0][1]]))
        axs[0].scatter(data["slow_vpp"][0], data["slow_vpp"][1])
        axs[1].plot(ex_data[graph_list[1][0]], median1d(ex_data[graph_list[1][1]]))
        axs[1].scatter(data["fast_vpp"][0], data["fast_vpp"][1])

        axs[2].plot(ex_data[graph_list3[0][0]], ex_data[graph_list3[0][1]])
        axs[2].scatter(data["slow_phase"][0], data["slow_phase"][1])
        axs[3].plot(ex_data[graph_list3[1][0]], ex_data[graph_list3[1][1]])
        axs[3].scatter(data["fast_phase"][0], data["fast_phase"][1])

        plt.show()
    return data


def single_scan_dataframe(files):
    cols =["Time", "humidity", "temperature", "slow_vpp_freq", "slow_vpp_val",
           "fast_vpp_freq", "fast_vpp_val", "slow_phase_freq", "slow_phase_val",
           "fast_phase_freq", "fast_phase_val"]
    df = pd.DataFrame(columns=cols, dtype=object)

    for file in files:
        data = get_peak(file, plot_draw=False)
        data_df = [data["Time"], data["humidity"], data["temperature"],\
                   data["slow_vpp"][0], data["slow_vpp"][1], data["fast_vpp"][0], data["fast_vpp"][1],\
                   data["slow_phase"][0], data["slow_phase"][1], data["fast_phase"][0], data["fast_phase"][1]]
        df.loc[len(df)] = np.array(data_df)
        
    return df

def original_scan_data_dataframe(files):
    cols = ["slow_freq_list", "slow_phase_list", "slow_vpp_list",\
            "fast_freq_list", "fast_phase_list", "fast_vpp_list"]

    df_array = []
       
    for file in files:
        f = open(file, 'r')
        data_org = f.read()
        f.close()
        data = data_to_dict(data_org)
        data_df = [data["slow_freq_list"], data["slow_phase_list"], data["slow_vpp_list"],\
                   data["fast_freq_list"], data["fast_phase_list"], data["fast_vpp_list"]]
        df = pd.DataFrame(np.array(data_df).T, columns=cols) 
        
        df_array.append(df)

    return df_array

    

if __name__ == '__main__':
    folder = "../long_data/2209-08"
    files = glob.glob(folder + "/*.txt")
    dfs = original_scan_data_dataframe(files)
    print(dfs[0]["slow_freq_list"])
    print(get_peak(files[0]))
    print(single_scan_dataframe(files))
    