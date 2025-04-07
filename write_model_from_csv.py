import os
import django
# -------------------------------------------------------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.dev")
django.setup()
# -------------------------------------------------------------------------

from backend.api.models import Info,Customers,Application,Modules,Groups,Region,Products,Sn,Users,Edit,Options,Product_groups
from backend.api.models import Updatetime
from backend.api.views import generate_last_update_time
from datetime import datetime

from copy import copy

import csv


for module in [Info,Customers,Application,Modules,Groups,Region,Products,Sn,Users,Edit,Updatetime,Options,Product_groups]:
    module.objects.all().delete()

i = 0
# 將資料由csv檔寫入model
with open('./csv/Application.csv', newline='', encoding='utf-8') as csvfile:
    my_csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in my_csv_reader:
        Application.objects.create(
            application_id = row[0],
            date = row[1],
            applicant = row[2],
            status = row[3],
            data = row[4],
            validator = row[5],
            verify_time = row[6],
            content = row[7])
        i+=1
    
with open('./csv/Customers.csv', newline='', encoding='utf-8') as csvfile:
    my_csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in my_csv_reader:
        Customers.objects.create(
            customer_id = row[0],
            name = row[1],
            site = row[2])

with open('./csv/Groups.csv', newline='', encoding='utf-8') as csvfile:
    my_csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in my_csv_reader:
        Groups.objects.create(
            group_id = row[0],
            name = row[1],
            caption = row[2],
            authority = row[3],
            description = row[4],
            members = row[5])

i = 0
with open('./csv/Info.csv', newline='', encoding='utf-8') as csvfile:
    my_csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in my_csv_reader:
        Info.objects.create(
            info_id = row[0],
            sn = row[1],
            func_uid = row[2],
            version = row[3],
            issued = row[4],
            expiration = row[5],
            count = row[6],
            registration = row[7],
            type = row[8],
            comment = row[9],
            contact = row[10],
            info = row[11])
        i+=1

i = 0
with open('./csv/Modules.csv', newline='', encoding='utf-8') as csvfile:
    my_csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in my_csv_reader:
        Modules.objects.create(
            mod_uid = row[0],
            caption = row[1])
        i+=1

with open('./csv/Products.csv', newline='', encoding='utf-8') as csvfile:
    my_csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in my_csv_reader:
        Products.objects.create(
            product_id = row[0],
            category_id = row[1],
            product_name = row[2],
            caption = row[3],
            remarks = row[4])

with open('./csv/Region.csv', newline='', encoding='utf-8') as csvfile:
    my_csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in my_csv_reader:
        Region.objects.create(
            region_id = row[0],
            name = row[1],
            description = row[2])

with open('./csv/Options.csv', newline='', encoding='utf-8') as csvfile:
    my_csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in my_csv_reader:
        Options.objects.create(
            option_id = row[0],
            product_name = row[1],
            option_name = row[2],
            caption = row[3],
            remarks = row[4])

with open('./csv/Product_groups.csv', newline='', encoding='utf-8') as csvfile:
    my_csv_reader = csv.reader(csvfile, delimiter=',',quotechar='"')
    for row in my_csv_reader:
        Product_groups.objects.create(
            group_id = row[0],
            caption = row[1],
            tag = row[2],
            product_list = row[3],#之後再來改改 下面註解是參考
            description = row[4],
            remarks = row[5])
"""with open('./csv/Product_groups.csv', newline='', encoding='utf-8') as csvfile:
    my_csv_reader = csv.reader(csvfile, delimiter=',',quotechar='|')
    for row in my_csv_reader:
        Product_groups.objects.create(
            group_id = row[0],
            caption = row[1],
            product_list = row[2],
            description = row[3],
            remarks = row[4])"""

i = 0
with open('./csv/Sn.csv', newline='', encoding='utf-8') as csvfile:
    my_csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in my_csv_reader:
        Sn.objects.create(
            sn_id = row[0],
            sn = row[1],
            region = row[2],
            user = row[3],
            record = row[4],
            note1 = row[5],
            note2 = row[6],
            note3 = row[7],
            note4 = row[8],
            note5 = row[9])
        i+=1
i = 0
with open('./csv/Edit.csv', newline='', encoding='utf-8') as csvfile:
    my_csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in my_csv_reader:
        Edit.objects.create(
            id = row[0],
            user = row[1],
            cc = row[2],
            data = row[3],
            comment = row[4])
        i+=1

with open('./csv/Users.csv', newline='', encoding='utf-8') as csvfile:
    my_csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in my_csv_reader:
        Users.objects.create(
            user_id = row[0],
            user = row[1],
            password = row[2],
            email = row[3],
            groups = row[4],
            region = row[5],
            record = row[6],
            description = row[7],
            setting = row[8])

Updatetime.objects.create(#生成上傳heroku時間
    id = 'last_update_time',
    update_time = generate_last_update_time())
Updatetime.objects.create(#生成上傳heroku時間
    id = 'git_push_time',
    update_time = generate_last_update_time())