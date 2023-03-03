import os, sqlite3

config_data =[]

# define DB
# mems_board DB
sql_method_1 = """
               CREATE TABLE board(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               sample_name TEXT,
               board_id TEXT,
               file_name TEXT,
               mes_mode TEXT,
               date TEXT
               )
               """


db_path_1 = './db/mems_board.db'
old_path_1 = './db/mems_borad_old.db'

config_data.append((sql_method_1, db_path_1, old_path_1))

# mems_fov DB
sql_method_2 = """
               CREATE TABLE board(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               experiment_id INTEGER,
               sample_name TEXT,
               board_id TEXT,
               fov_id TEXT,
               camera_id TEXT,
               file_name TEXT,
               date TEXT
               )
               """

db_path_2 = './db/mems_fov.db'
old_path_2 = './db/mems_fov_old.db'

config_data.append((sql_method_2, db_path_2, old_path_2))

# mems_single DB
sql_method_3 = """
               CREATE TABLE board(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               sample_name TEXT,
               fast_word REAL,
               slow_word REAL,
               fast_volt REAL,
               slow_volt REAL,
               Q_fast REAL,
               Q_slow REAL,
               temperature REAL,
               humidity REAL,
               scan_file_name TEXT,
               Q_scan_file_name TEXT,
               board_id TEXT,
               equip_id TEXT,
               camera_id TEXT,
               fast_start_word REAL,
               fast_target_phase REAL,
               fast_start_volt REAL, 
               fast_stop_volt REAL,
               slow_start_word REAL,
               slow_target_phase REAL,
               slow_start_volt REAL, 
               slow_stop_volt REAL,
               fast_word_width REAL,
               fast_word_step REAL,
               fast_asym REAL,
               slow_word_width REAL,
               slow_word_step REAL,              
               slow_asym REAL,
               date TEXT
               )
               """
               
db_path_3 = './db/mems_single.db'
old_path_3 = './db/mems_single_old.db'

config_data.append((sql_method_3, db_path_3, old_path_3))

# DB setting
sql_method_list = [data[0] for data in config_data]
db_path_list = [data[1] for data in config_data]
old_path_list = [data[2] for data in config_data]

# DB initiarize
def db_init(db_path, old_path, sql_method):

    # save old db and reset db
    db_is_new = not os.path.exists(db_path)
    old_is_new = not os.path.exists(old_path)

    if not old_is_new:
        os.remove(old_path)

    if not db_is_new:
        os.rename(db_path, old_path)

    conn = sqlite3.connect(db_path)

    # テーブル作成
    conn.execute(sql_method)

    conn.commit()
    conn.close()


def db_init_main():
    for db_path, old_path, sql_method in zip(db_path_list, old_path_list, sql_method_list) :
        db_init(db_path, old_path, sql_method)

if __name__ == '__main__':
    db_init_main()
