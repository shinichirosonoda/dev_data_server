import datetime, sqlite3

# ? array create
def q_create(num):
    str_text = ''
    for i in range(num - 1):
        str_text += '?,'
    str_text += '?'
    return str_text


# general create
def data_create(data, db_path):
    keys_list = list(data.keys())
    values_list = list(data.values())

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    dt_now = datetime.datetime.now()
    date = dt_now.strftime('%Y-%m-%d %H:%M:%S')
    keys_list.append("date")
    values_list.append(date)

    text = 'insert into board{} values({})'.format(tuple(keys_list), q_create(len(keys_list)))
    c.execute(text, tuple(values_list))

    return_data = c.lastrowid
    conn.commit()
    conn.close()

    return return_data


# mems_board.dbの発番を行う。
def data_create_board(data, db_path = './db/mems_board.db'):
    return data_create(data, db_path)

# mems_fov.dbの発番を行う。
def data_create_fov(data, db_path = './db/mems_fov.db'):
   return data_create(data, db_path)

# mems_scan.dbの発番を行う。
def data_create_single(data, db_path = './db/mems_single.db'):
   return data_create(data, db_path)   

# board_idのデータを取り出す。
def pick_up_board_id(board_id, path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    text = 'select * from board where board_id = ?'
    c.execute(text, (board_id,))
    data = c.fetchall()

    conn.commit()
    conn.close()

    return data

# board_id, mes_modeのデータを取り出す。
def pick_up_board_id_mes_mode(board_id, mes_mode, path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    text = 'select * from board where board_id = ? and mes_mode = ?'
    c.execute(text, (board_id, mes_mode))
    data = c.fetchall()

    conn.commit()
    conn.close()

    return data
# board_id, mes_modeのデータを取り出す。
def pick_up_sample_board_id_mes_mode(sample_name, board_id, mes_mode, path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    text = 'select * from board where sample_name = ? and board_id = ? and mes_mode = ?'
    c.execute(text, (sample_name, board_id, mes_mode))
    data = c.fetchall()

    conn.commit()
    conn.close()

    return data

# board_id, mes_modeのデータを取り出す。
def pick_up_sample_board_id(sample_name, board_id, path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    text = 'select * from board where sample_name = ? and board_id = ?'
    c.execute(text, (sample_name, board_id))
    data = c.fetchall()

    conn.commit()
    conn.close()

    return data

# sample_nameのデータを取り出す。
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
    db_path1 = './db/mems_board.db'
    db_path2 = './db/mems_fov.db'

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

    list1 = [x[2] for x in pick_up(db_path1)]
    list2 = sorted(set(list1), key=list1.index)
    list2.sort()
    print(list2)

    
    data = {"sample_name": "TT2222222",
            "board_id": "2209-05",
            "file_name": "test.csv",
            "mes_mode": "start"}

    experiment_id = data_create_board(data)
    print(experiment_id)
    
    data = {"experiment_id": experiment_id,
            "sample_name": "TT2222222",
                 "board_id": "2209-05",
                 "fov_id":  "lte1",
                 "camera_id": "AA12345678",
                 "file_name": "fov.csv"}
    
    print(data_create_fov(data))
