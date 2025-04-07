#--------------------------將web上的資料庫備份到local_db--------------------------#
import sqlite3
import os
import django
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.dev")
django.setup()

def web_to_local():
    #----------------local DB----------------#
    local_database = sqlite3.connect("local_db.sqlite3")
    local_cursor = local_database.cursor()
    local_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    local_Tables = local_cursor.fetchall()
    #module.objects.all().delete()
    #-----------------Web DB-----------------#
    web_table = []
    web_database = sqlite3.connect("db.sqlite3")
    web_cursor = web_database.cursor()
    web_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    web_Tables = web_cursor.fetchall()


    for table in web_Tables:
        web_table.append(table[0])
    for table in local_Tables:#根據loacl有的table去web_table抓資料
        if table[0] in web_table:
            local_cursor.execute('DELETE FROM '+ table[0]+';',)#將local_DB資料刪除
            local_cursor.execute("SELECT * FROM {}".format(table[0]))#獲取local_DB table內各行名稱
            table_detail = str(tuple([tuple[0] for tuple in local_cursor.description]))#為了符合sql語法 Ex:sqlite_sequence(name,seq)
            table_type = str(tuple([(':'+tuple[0]) for tuple in local_cursor.description])).replace("'",'')#為了符合sql語法 Ex:sqlite_sequence(:name,:seq)
            web_cursor.execute("SELECT * FROM "+table[0])#獲取web_local資料
            myresult = web_cursor.fetchall()
            for web_table_data in myresult:
                local_cursor.execute("INSERT INTO "+table[0]+table_detail+"VALUES"+table_type, web_table_data)
    local_database.commit()#提交更新

    """local_cursor.execute("SELECT * FROM {}".format('sqlite_sequence'))
    table_detail = str(tuple([tuple[0] for tuple in local_cursor.description]))#為了符合sql語法 Ex:sqlite_sequence(name,seq)
    table_type = str(tuple([(':'+tuple[0]) for tuple in local_cursor.description])).replace("'",'')#為了符合sql語法 Ex:sqlite_sequence(:name,:seq)
    local_cursor.execute('DELETE FROM sqlite_sequence;',)
    #local_cursor.execute("INSERT INTO sqlite_sequence(name, seq)VALUES(:name, :seq)", ("django_migrations","18"))
    local_cursor.execute("INSERT INTO sqlite_sequence"+table_detail+"VALUES"+table_type, ("django_migrations","18"))
    local_database.commit()"""

if sys.argv[1] == '-w' or sys.argv[1] == '-l':
    web_to_local()