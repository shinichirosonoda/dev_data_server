# -*- coding: utf-8 -*-
import datetime, sqlite3

"""
db_path1 = './db/mems_board.db'
db_path2 = './db/mems_fov.db'
"""

db_path1 = '/home/sonoda/git2/dev_data_server/mems_server/db/mems_board.db'
db_path2 = '/home/sonoda/git2/dev_data_server/mems_server/db/mems_fov.db'


# mems_board.dbの発番を行う。
def data_create_board(data):
    sample_name = data["sample_name"]
    board_id = data["board_id"]
    file_name = data["file_name"]
    mes_mode = data["mes_mode"]

    conn = sqlite3.connect(db_path1)
    c = conn.cursor()
    dt_now = datetime.datetime.now()
    date = dt_now.strftime('%Y-%m-%d %H:%M:%S')

    text = 'insert into board(sample_name,\
                              board_id,\
                              file_name,\
                              mes_mode,\
                              date) values(?,?,?,?,?)'
    
    c.execute(text, (sample_name,\
                     board_id,\
                     file_name,\
                     mes_mode,\
                     date))
    
    data = c.lastrowid
    conn.commit()
    conn.close()

    return data

# mems_fov.dbの発番を行う。
def data_create_fov(data):
    experiment_id = data["experiment_id"]
    sample_name = data["sample_name"]
    board_id = data["board_id"]
    fov_id = data["fov_id"]
    camera_id = data["camera_id"]
    file_name = data["file_name"]

    conn = sqlite3.connect(db_path2)
    c = conn.cursor()
    dt_now = datetime.datetime.now()
    date = dt_now.strftime('%Y-%m-%d %H:%M:%S')

    text = 'insert into board(experiment_id,\
                              sample_name,\
                              board_id,\
                              fov_id,\
                              camera_id,\
                              file_name,\
                              date) values(?,?,?,?,?,?,?)'
    
    c.execute(text, (experiment_id,\
                     sample_name,\
                     board_id,\
                     fov_id,\
                     camera_id,\
                     file_name,\
                     date))
    
    data = c.lastrowid
    conn.commit()
    conn.close()

    return data

# board_idのデータを取り出す。(mems_board.db, mems_fov.db)
def pick_up_board_id(board_id, path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    text = 'select * from board where board_id = ?'
    c.execute(text, (board_id,))
    data = c.fetchall()

    conn.commit()
    conn.close()

    return data

# sample_nameのデータを取り出す。(mems_board.db, mems_fov.db)
def pick_up_sample_name(sample_name, path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    text = 'select * from board where sample_name = ?'
    c.execute(text, (sample_name,))
    data = c.fetchall()

    conn.commit()
    conn.close()

    return data

# idのデータを取り出す。(mems_board.db, mems_fov.db)
def pick_up_id(id, path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    text = 'select * from board where id = ?'
    c.execute(text, (id,))
    data = c.fetchall()

    conn.commit()
    conn.close()

    return data

if __name__ == '__main__':
    """
    data = {"sample_name": "1w01",\
            "board_id": "2209-05",\
            "file_name": "2023-02-02_13-27-00_1w01.csv",\
            "mes_mode": "start"}
    id = data_create_board(data)
    """
    id = 1
    print(id)
    output_data = pick_up_id(id, db_path1)
    print(output_data)
    #sample_name = output_data[0][1]
    #board_id = output_data[0][2]
    #print(sample_name)
    #print(board_id)

    """
    data = {"experiment_id": id,
            "sample_name": sample_name,
            "board_id": board_id,
            "fov_id":  "LTE-01",
            "camera_id": "AA01234",
            "file_name": "2023-02-02_13-27-00_1w01_fov.csv"}
    id = data_create_fov(data)
    """

    id = 1
    print(id)
    output_data = pick_up_id(id, db_path2)
    print(output_data)

    print(pick_up_sample_name("TT2222222", db_path1))
    print(pick_up_sample_name("TT2222222", db_path2))