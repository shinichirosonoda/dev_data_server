# -*- coding: utf-8 -*-
import os, sqlite3

def init_config():
    config_data =[]
    # define board DB
    keys = ["sample_name", "board_id", "file_name", "mes_mode", "date"]
    sql_method = sql_text(keys)
    db_path = './db/mems_board.db'
    old_path = './db/mems_borad_old.db'
    config_data.append((sql_method, db_path, old_path))

    # define fov DB 
    keys = ["sample_name", "board_id TEXT", "fov_id", "camera_id", "file_name", "date TEXT"]
    sql_method = sql_text(keys)
    db_path = './db/mems_fov.db'
    old_path = './db/mems_fov_old.db'
    config_data.append((sql_method, db_path, old_path))

    # DB setting
    sql_method_list = [data[0] for data in config_data]
    db_path_list = [data[1] for data in config_data]
    old_path_list = [data[2] for data in config_data]
    
    return db_path_list, old_path_list, sql_method_list

# sql_text
def sql_text(keys):
    str_text = ""
    for text in keys[:-1]:
        str_text += text + " TEXT,"
    str_text += keys[-1] + " TEXT"
    sql_method = """
                 CREATE TABLE board(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 {}
                 date TEXT
                 )
                 """.format(str_text)
    return sql_method

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
    db_path_list, old_path_list, sql_method_list = init_config()
    for db_path, old_path, sql_method in zip(db_path_list, old_path_list, sql_method_list) :
        db_init(db_path, old_path, sql_method)

if __name__ == '__main__':
    db_init_main()
