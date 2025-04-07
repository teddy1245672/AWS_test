# -*- coding: utf-8 -*- 
#將database資料寫入csv檔案中
import sys
import subprocess
import csv
import sqlite3
import codecs
import os

if len(sys.argv) == 1:
    print("insufficient parameters")
    sys.exit(1)

if sys.argv[1] == '-w' or sys.argv[1] == '-l':
    database = sqlite3.connect("db.sqlite3")
    cursor = database.cursor()
    tables = ['Application','Customers','Groups', 'Info','Modules','Products','Region', 'Sn', 'Users','Edit','Product_groups']

    if not os.path.isdir("./csv"):
        os.mkdir("./csv")

    for table in tables:
        csv_file = codecs.open(('./csv/%s.csv') % table, 'w', encoding='utf-8')
        writer = csv.writer(csv_file)

        for row in cursor.execute("SELECT * FROM %s" % table):
            writer.writerow(row)

        csv_file.close()
    
    """if sys.argv[1] == '-w':  # 更新 heroku 的 database
        subprocess.run("git add .", shell=True)
        subprocess.run("git commit -m 'auto'", shell=True)
        subprocess.run("git push heroku master", shell=True)

        subprocess.run("heroku run python import_csv_to_DB.py", shell=True)
        subprocess.run("heroku run python create_usergroups.py", shell=True)

    else:  # sys.argv[1] == '-l':  # 更新 localhost 的 database
        print('python3 import_csv_to_DB.py')
        subprocess.run("python3 import_csv_to_DB.py", shell=True)
        print('python3 create_usergroups.py')
        subprocess.run("python3 create_usergroups.py", shell=True)"""

else:
    print("invalid parameter")
    sys.exit(1)
