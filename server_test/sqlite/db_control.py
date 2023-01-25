# -*- coding: utf-8 -*-
import datetime, os, sqlite3

db_path = './sqlite/print_instax.db'
#db_path = './print_instax.db'

db2_path = './sqlite/instax_status.db'
#db2_path = './instax_status.db'


# printer_id, file_path, flag, valueを持つデータを生成する。(print_instax.db)
def data_create(printer_id, file_path, flag, value):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    date = datetime.datetime.now()
    text = 'insert into printer(printer_id,file_path,flag,value,date) values(?,?,?,?,?)'
    c.execute(text,(str(printer_id), file_path, flag, value, str(date)))
    data = c.lastrowid
    conn.commit()
    conn.close()

    return data


# printer_id, flagのデータを取り出す。(print_instax.db)

def pick_up_data2(printer_id, flag):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    text = 'select * from printer where printer_id = ? and flag = ?'
    c.execute(text,(str(printer_id), flag))
    data = c.fetchall()
    #print(data)

    conn.commit()
    conn.close()

    return data

def pick_up_data(id, flag):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    text = 'select * from printer where id = ? and  flag = ?'
    c.execute(text,(str(id), flag))
    data = c.fetchall()
    #print(data)

    conn.commit()
    conn.close()

    return data


# idのデータのflag, valueを書き換える。(print_instax.db)
def update_data(id, flag, value):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    text = 'update printer set flag = ? where id = ?'
    c.execute(text,(flag, str(id)))
    text = 'update printer set value = ? where id = ?'
    c.execute(text,(value, str(id)))

    c.execute('select * from printer')
    data = c.fetchall()
    #print(data)

    conn.commit()
    conn.close()

# idのデータのfile_path, flagを書き換える。(print_instax.db)
def update_data2(id, file_path, flag):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    text = 'update printer set file_path = ? where id = ?'
    c.execute(text,(file_path, str(id)))
    text = 'update printer set flag = ? where id = ?'
    c.execute(text,(flag, str(id)))

    c.execute('select * from printer')
    data = c.fetchall()
    #print(data)

    conn.commit()
    conn.close()

# 特定のidのデータを削除する関数。(print_instax.db)

def delete_data(id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    text = 'delete from printer where id = ?'
    c.execute(text, str(id))

    c.execute('select * from printer')
    data = c.fetchall()
    #print(data)

    conn.commit()
    conn.close()


# printer_id, value, status, SNを持つデータを生成する。(instax_status.db)
def instax_status_create(printer_id, value, status, SN):
    conn = sqlite3.connect(db2_path)
    c = conn.cursor()
    date = datetime.datetime.now()
    text = 'insert into status(printer_id, value, status, SN, date) values(?,?,?,?,?)'
    c.execute(text,(str(printer_id), value, status, SN, str(date)))

    c.execute('select * from status')
    data = c.fetchall()
    #print(data)

    conn.commit()
    conn.close()

# print_idのvalueを書き換える。(instax_status.db)
def update_status_data(printer_id, value):
    conn = sqlite3.connect(db2_path)
    c = conn.cursor()
    text = 'update status set value = ? where printer_id = ?'
    c.execute(text,(value, str(printer_id)))

    c.execute('select * from status')
    data = c.fetchall()
    #print(data)

    conn.commit()
    conn.close()

# print_idのstatusを書き換える。(instax_status.db)
def update_status_data_status(printer_id, status):
    conn = sqlite3.connect(db2_path)
    c = conn.cursor()
    text = 'update status set status = ? where printer_id = ?'
    c.execute(text,(status, str(printer_id)))

    c.execute('select * from status')
    data = c.fetchall()
    #print(data)

    conn.commit()
    conn.close()

# print_idのSNを書き換える。(instax_status.db)
def update_status_data_SN(printer_id, SN):
    conn = sqlite3.connect(db2_path)
    c = conn.cursor()
    text = 'update status set SN = ? where printer_id = ?'
    c.execute(text,(SN, str(printer_id)))

    c.execute('select * from status')
    data = c.fetchall()
    #print(data)

    conn.commit()
    conn.close()

# printerの数に対応したデータを生成する関数。(instax_status.db)
def instax_status_for_printers(printer_num=5):
    conn = sqlite3.connect(db2_path)
    c = conn.cursor()
    c.execute('select * from status')
    data = c.fetchall()
    
    if len(data) == 0:
        num = printer_num
        for i in range(1,num+1):
            instax_status_create(i, "", "", "")

    elif data[-1][0] < printer_num:
        num =  printer_num - data[-1][0]
        for i in range(data[-1][0]+1,data[-1][0]+num+1):
            instax_status_create(i, "", "", "")

   
    conn.commit()
    conn.close()


# printerの数に対応したデータを生成する。(instax_status.db)
instax_status_for_printers()

def pick_up_status_data(printer_id):
    conn = sqlite3.connect(db2_path)
    c = conn.cursor()
    text = 'select * from status where printer_id = ?'
    c.execute(text, str(printer_id))
    data = c.fetchall()
    #print(data)

    conn.commit()
    conn.close()

    return data


if __name__ == '__main__':
  
    data_create(1, "./image/image_1","False","")
    data_create(2, "./image/image_2","False","")
    pick_up_data(1, "False")
    update_data(1, "True", "5")
    update_status_data(1, "10")
    pick_up_status_data(1)
    delete_data(3)
    pick_up_data(3, "False")

    instax_status_create(1, "10", "True", "1")
    update_status_data(1, "7")
    update_status_data_status(1, "False")
    update_status_data_SN(1, "4")
    
    instax_status_for_printers(printer_num=5)
    pick_up_status_data(2)
