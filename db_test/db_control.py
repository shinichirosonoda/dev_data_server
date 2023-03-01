import datetime, sqlite3

def q_create(num):
    str_text = ''
    for i in range(num):
        str_text += '?,'
    str_text += '?'
    return str_text


# general create
def data_create(data, col_tuple, db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    dt_now = datetime.datetime.now()
    date = dt_now.strftime('%Y-%m-%d %H:%M:%S')

    text = 'insert into board{} values({})'.format(col_tuple, q_create(len(col_tuple) -1))
    
    c.execute(text, col_tuple)
    data = c.lastrowid
    conn.commit()
    conn.close()

    return data


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

# board_id, mes_modeのデータを取り出す。(mems_board.db, mems_fov.db)
def pick_up_board_id_mes_mode(board_id, mes_mode, path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    text = 'select * from board where board_id = ? and mes_mode = ?'
    c.execute(text, (board_id, mes_mode))
    data = c.fetchall()

    conn.commit()
    conn.close()

    return data
# board_id, mes_modeのデータを取り出す。(mems_board.db, mems_fov.db)
def pick_up_sample_board_id_mes_mode(sample_name, board_id, mes_mode, path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    text = 'select * from board where sample_name = ? and board_id = ? and mes_mode = ?'
    c.execute(text, (sample_name, board_id, mes_mode))
    data = c.fetchall()

    conn.commit()
    conn.close()

    return data

# board_id, mes_modeのデータを取り出す。(mems_board.db, mems_fov.db)
def pick_up_sample_board_id(sample_name, board_id, path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    text = 'select * from board where sample_name = ? and board_id = ?'
    c.execute(text, (sample_name, board_id))
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

# データを取り出す。(mems_board.db, mems_fov.db)
def pick_up(path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    text = 'select * from board'
    c.execute(text,)
    data = c.fetchall()

    conn.commit()
    conn.close()

    return data

if __name__ == '__main__':
    """
    id = 1
    print(id)
    output_data = pick_up_id(id, db_path1)
    print(output_data)

    id = 1
    print(id)
    output_data = pick_up_id(id, db_path2)
    print(output_data)

    print(pick_up_sample_name("TT2222222", db_path1))
    print(pick_up_sample_name("TT2222222", db_path2))
    """

    """
    list1 = [x[2] for x in pick_up(db_path1)]
    list2 = sorted(set(list1), key=list1.index)
    list2.sort()
    print(list2)
    """

    print(q_create(4))
    col_tuple_board = ("sample_name", "board_id", "file_name", "mes_mode", "date")
    db_path_board = './db/mems_board.db'
    db_path_fov = './db/mems_fov.db'
    data = ("3p01", "2209-05", "test.csv", "start", "2023/03/01")
    print(data_create(data, col_tuple_board, db_path_board))
