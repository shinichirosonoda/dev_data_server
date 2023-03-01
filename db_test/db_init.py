# -*- coding: utf-8 -*-
import os, sqlite3

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


def db_init_main(db_path_list, old_path_list, sql_method_list):
    for db_path, old_path, sql_method in zip(db_path_list, old_path_list, sql_method_list) :
        db_init(db_path, old_path, sql_method)

if __name__ == '__main__':
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

    db_path_list = [db_path_1, db_path_2]
    old_path_list = [old_path_1, old_path_2]
    sql_method_list = [sql_method_1, sql_method_2]
    db_init_main(db_path_list, old_path_list, sql_method_list)
