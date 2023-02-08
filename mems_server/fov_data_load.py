from db_control import pick_up_sample_board_id

db_path1 = './db/mems_board.db'
db_path2 = './db/mems_fov.db'

def get_all_fov_data_files(board_name, sample):
    files = [x[6] for x in pick_up_sample_board_id(sample, board_name, db_path2)]
    return files

def fov_dataframe(files):
    for file in files:
        df = pd.read_csv(file, index_col=0)
        df_array.append(df)
    return df_array

if __name__ == '__main__':
    board_name = "2112-001"
    sample ='TT2222222'

    print(get_all_fov_data_files(board_name, sample))