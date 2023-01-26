# -*- coding: utf-8 -*-
import datetime, sqlite3

db_path = './db/mems_board.db'
#db_path = './mems_board.db'


# board_id, file_path, flag, dateを持つデータを生成する。(mems.db)
def data_create(board_id, file_name, flag):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    dt_now = datetime.datetime.now()
    date = dt_now.strftime('%Y-%m-%d %H:%M:%S')

    text = 'insert into board(board_id, file_path, flag, date) values(?,?,?,?)'
    c.execute(text, (board_id, file_name, flag, str(date)))
    data = c.lastrowid
    conn.commit()
    conn.close()

    return data


# board_idのデータを取り出す。(mems.db)
def pick_up_data(board_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    text = 'select * from board where board_id = ?'
    c.execute(text, (board_id,))
    data = c.fetchall()

    conn.commit()
    conn.close()

    return data

# boardのデータのfile_path, flag, dateを書き換える。(mems.db)
def update_data(board_id, file_name, flag):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    dt_now = datetime.datetime.now()
    date = dt_now.strftime('%Y-%m-%d %H:%M:%S')

    text = 'update board set file_path = ? where board_id = ?'
    c.execute(text,(file_name, board_id))
    text = 'update board set flag = ? where board_id = ?'
    c.execute(text,(flag, board_id))
    text = 'update board set date = ? where board_id = ?'
    c.execute(text,(str(date), board_id))

    c.execute('select * from board')
    data = c.fetchall()

    conn.commit()
    conn.close()

    return data

# 特定のboard_idのデータを削除する関数。(mems.db)
def delete_data(board_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    text = 'delete from board where board_id = ?'
    c.execute(text, (board_id,))

    c.execute('select * from board')
    data = c.fetchall()

    conn.commit()
    conn.close()

    return data


if __name__ == '__main__':
  
    print("P1:", data_create("2209-05", "./test_data1.csv","False"))
    print("P2:", data_create("2209-06", "./test_data2.csv","False"))
    print("P3:", pick_up_data("2209-05"))
    print("P4:", update_data("2209-05", "./test_data1.csv","True"))
    print("P5:", pick_up_data("2209-05"))
    #print("P6:", delete_data("2209-05"))
    #print("P7:", pick_up_data("2209-05"))