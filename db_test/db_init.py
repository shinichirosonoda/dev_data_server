import os, sqlite3

config_data =[]

# define DB
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
