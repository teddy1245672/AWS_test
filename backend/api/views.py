from django.shortcuts import render
from .models import Info,Customers,Application,Modules,Groups,Region,Products,Sn,Users,Edit,Options,Updatetime,Product_groups
# Create your views here.
from django.http import HttpResponse
import json
import copy
import sys
sys.path.append("..")#為了呼叫上級py檔案函式
import write_local_from_web
# 解决前端post请求 csrf问题
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.gzip import gzip_page
import os
from copy import copy
from datetime import datetime, timedelta, timezone
from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Border, Side, Alignment
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase #用於承載附檔
from email import encoders #用於附檔編碼
from email.mime.text import MIMEText
import variable
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>前端<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#

#-------------------login------------------------#
@csrf_exempt
def login(request):
    '''登入資料核對及回傳資料'''
    if request.method == 'GET':
        mode = request.GET['mode']
        if mode =='login':
            user = json.loads(request.GET['user'])
            if Users.objects.filter(user=user[0]):
                if user[1] == Users.objects.get(user=user[0]).password:
                    Authority = set()
                    if Users.objects.get(user=user[0]).groups != '':
                        for group_id in json.loads(Users.objects.get(user=user[0]).groups):
                            if Groups.objects.get(group_id = group_id).authority != '':
                                for authority in json.loads(Groups.objects.get(group_id = group_id).authority)['operator']:
                                    Authority.add(authority)
                    return HttpResponse('{"msg":"登入成功!","email":'+ json.dumps(Users.objects.get(user=user[0]).email) +',"region":' + json.dumps(Users.objects.get(user=user[0]).region)+
                    ',"authority":'+json.dumps(list(Authority)) +'}')
                else:
                    return HttpResponse('{"msg":"密碼錯誤!"}')
            else: 
                return HttpResponse('{"msg":"登入失敗，無此帳號!"}')


#------------------Show_all----------------------#
@csrf_exempt
@gzip_page#gzip壓縮
def show_all(request):
    '''根據當前用戶所在群組權限將資料傳入Show_all'''
    username = json.loads(request.GET['user'])
    authority = []
    group = []
    region_auth = []
    product_auth = []
    if Users.objects.get(user = username[0]).groups != '':
        group = json.loads(Users.objects.get(user = username[0]).groups)
        for gro in group:
            if Groups.objects.get(group_id = gro).authority != '':#authority只有兩種型態1.'{region:[1],product:[]}' 2.'' 完全空白
                authority.append(json.loads(Groups.objects.get(group_id = gro).authority))#找當前使用者的身分
        for auth in authority:
            for reg in auth['region']:
                if reg not in region_auth:
                    region_auth.append(reg)#區域權限
            for pro in auth['product']:
                if pro not in product_auth:
                    product_auth.append(pro)#產品權限

    module_data = []
    for mod in Modules.objects.all():
        module_data.append({'mod_uid':mod.mod_uid,'caption':mod.caption})

    customer_data = []
    for customer in Customers.objects.all():
        customer_data.append({'customer_id':customer.customer_id,'name':customer.name,'site':customer.site})

    product_dict = {}
    product_data = []
    for product in Products.objects.all():
        product_data.append({'product_id':product.product_id,'category_id':product.category_id,
        'product_name':product.product_name,'caption':product.caption,'remarks':product.remarks})
        product_dict.setdefault(product.product_name,{'product_id':product.product_id,'category_id':product.category_id,
        'caption':product.caption,'remarks':product.remarks})

    product_groups_data = []
    for product_group in Product_groups.objects.all():
        product_groups_data.append({'group_id':product_group.group_id,'caption':product_group.caption,'tag':product_group.tag,
        'product_list':product_group.product_list,'description':product_group.description,'remarks':product_group.remarks})

    option_dict = {}
    option_data = []
    for option in Options.objects.all():
        option_data.append({'id':option.option_id,'product_name':option.product_name,
        'option_name':option.option_name,'caption':option.caption,'remarks':option.remarks})
        option_dict.setdefault(option.option_name,{'id':option.option_id,'product_name':option.product_name,
        'caption':option.caption,'remarks':option.remarks})

    region_data = []
    for region in Region.objects.all():
        region_data.append({'region_id':region.region_id,'name':region.name,'description':region.description})

    sn_dict = {}
    sn_data = []
    for sn in Sn.objects.all():
        sn_data.append({'sn_id':sn.sn_id,'sn':sn.sn,'region':sn.region,'user':sn.user,
        'record':sn.record,'note1':sn.note1,'note2':sn.note2,'note3':sn.note3,'note4':sn.note1,'note5':sn.note1})
        sn_dict.setdefault(sn.sn,{'sn_id':sn.sn_id,'region':sn.region,'user':sn.user,'record':sn.record,
        'note1':sn.note1,'note2':sn.note2,'note3':sn.note3,'note4':sn.note1,'note5':sn.note1})
    
    info_data = []
    for info in Info.objects.all():
        if info.sn in sn_dict:
            if sn_dict[info.sn]['region'] == '':#若region為空表示所有人皆可查看
                if info.func_uid in product_dict:
                    if product_dict[info.func_uid]['category_id'] in product_auth:
                        info_data.append({'info_id':info.info_id,'sn':info.sn,'func_uid':info.func_uid,'version':info.version,'issued':info.issued,'expiration':info.expiration,
                        'count':info.count,'registration':info.registration,'type':info.type,'comment':info.comment,'contact':info.contact,'info':info.info})
                elif info.func_uid in option_dict:
                    if option_dict[info.func_uid]['product_name'] in product_dict:
                        if product_dict[option_dict[info.func_uid]['product_name']]['category_id'] in product_auth:
                            info_data.append({'info_id':info.info_id,'sn':info.sn,'func_uid':info.func_uid,'version':info.version,'issued':info.issued,'expiration':info.expiration,
                            'count':info.count,'registration':info.registration,'type':info.type,'comment':info.comment,'contact':info.contact,'info':info.info})
            elif int(sn_dict[info.sn]['region']) in region_auth:
                if info.func_uid in product_dict:
                    if product_dict[info.func_uid]['category_id'] in product_auth:
                        info_data.append({'info_id':info.info_id,'sn':info.sn,'func_uid':info.func_uid,'version':info.version,'issued':info.issued,'expiration':info.expiration,
                        'count':info.count,'registration':info.registration,'type':info.type,'comment':info.comment,'contact':info.contact,'info':info.info})
                elif info.func_uid in option_dict:
                    if option_dict[info.func_uid]['product_name'] in product_dict:
                        if product_dict[option_dict[info.func_uid]['product_name']]['category_id'] in product_auth:
                                info_data.append({'info_id':info.info_id,'sn':info.sn,'func_uid':info.func_uid,'version':info.version,'issued':info.issued,'expiration':info.expiration,
                                'count':info.count,'registration':info.registration,'type':info.type,'comment':info.comment,'contact':info.contact,'info':info.info}) 

    user_data = []
    for user in Users.objects.all():
        user_data.append({'user_id':user.user_id,'user':user.user,'password':user.password,'email':user.email,'groups':user.groups,'region':user.region,'record':user.record,'description':user.description,'setting':user.setting})


    group_data = []
    for group in Groups.objects.all():
        group_data.append({'group_id':group.group_id,'name':group.name,'caption':group.caption,'authority':group.authority,'description':group.description,'members':group.members})

    edit_data = []
    for edit in Edit.objects.all():
        if(edit.user == username[0]):#只傳送當前使用者的資料
            edit_data.append({'cc':edit.cc,'user':edit.user,'comment':edit.comment,'data':edit.data})
    return HttpResponse(json.dumps({
        'module_data':module_data,
        'customer_data':customer_data,
        'product_data':product_data,
        'region_data':region_data,
        'sn_data':sn_data,
        'info_data':info_data,
        'option_data':option_data,
        'user_data':user_data,
        'group_data':group_data,
        'product_groups_data':product_groups_data,
        'edit_data':edit_data,
        'update_time':Updatetime.objects.get(id = 'last_update_time').update_time,
        'git_push_time':Updatetime.objects.get(id = 'git_push_time').update_time,
        'sn_dict':sn_dict
        }))
@csrf_exempt
def save_to_handle(request):
    '''將新增 修改 刪除資料存入Edit資料庫'''
    if request.method == 'POST':
        user = json.loads(request.body)['user']
        checked_Data_from = json.loads(request.body)['checked_Data']
        checked_Data = []
        content = json.loads(request.body)['content']
        if(Edit.objects.filter(user=user[0])):
            checked_Data = json.loads(Edit.objects.get(user=user[0]).data)#之前的資料
            for i in range(0,len(checked_Data_from)):
               checked_Data.append(checked_Data_from[i])#加上 新資料一起儲存
            Edit.objects.filter(user=user[0]).update(data=json.dumps(checked_Data))
        else:
            for i in range(0,len(checked_Data_from)):
                checked_Data.append(checked_Data_from[i])
            for i in range(1,len(Groups.objects.all()) + 1):#注意
                if not Edit.objects.filter(id = i):
                    Edit.objects.create(#將修改的資料放入資料庫
                        id = i,
                        user = user[0],
                        cc = '',
                        data = json.dumps(checked_Data),
                        comment = content)
                    break
        return HttpResponse('新增 修改 刪除資料存入Edit資料庫')
@csrf_exempt
def download_show(request):
    '''Show_all所勾選的資料下載'''
    if request.method == 'POST':#download
        user = json.loads(request.body)['user']
        data = json.loads(request.body)['data']
        workbook = write_license_applicationXLSX(user[0], user[0],data)
        response = HttpResponse(content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=license-application.xlsx'
        workbook.save(response)
        workbook.close()
        return response
@csrf_exempt
def save_to_user_setting(request):
    '''將使用者設定存入DB'''
    if request.method == 'POST':
        user = json.loads(request.body)['user']
        source = json.loads(request.body)['source']
        if source == 'KeyID':
            mode = json.loads(request.body)['mode']
            setting = json.loads(Users.objects.get(user=user[0]).setting)
            setting['mode'] = mode
            Users.objects.filter(user=user[0]).update(setting=json.dumps(setting))
        elif source == 'product':
            pagesize = json.loads(request.body)['pagesize']
            mode = json.loads(request.body)['mode']
            setting = json.loads(Users.objects.get(user=user[0]).setting)
            setting['pagesize'] = pagesize
            setting['mode'] = mode
            Users.objects.filter(user=user[0]).update(setting=json.dumps(setting))
        return HttpResponse('改動pagesize成功') 

#-------------------KeyID------------------------#
@csrf_exempt
def KeyID(request):
    '''資料傳入KeyI頁面'''
    region_data = []
    for region in Region.objects.all():
        region_data.append({'region_id':region.region_id,'name':region.name,'description':region.description})

    customer_data = []
    for customer in Customers.objects.all():
        customer_data.append({'customer_id':customer.customer_id,'name':customer.name,'site':customer.site})

    sn_data = []
    for sn in Sn.objects.all():
        sn_data.append({'sn_id':sn.sn_id,'sn':sn.sn,'region':sn.region,'user':sn.user,
        'record':sn.record,'note1':sn.note1,'note2':sn.note2,'note3':sn.note3,'note4':sn.note1,'note5':sn.note1})
        
    return HttpResponse(json.dumps({
        'customer_data':customer_data,
        'sn_data':sn_data,
        'region_data':region_data
        }))
#--------------------add-------------------------#
@csrf_exempt
@gzip_page
def get_product_groups_info_data(request):
    '''為了讓ADD頁面新增完產品群組就可以拿到資料'''
    product_groups = []
    for p in Product_groups.objects.all():
        product_groups.append({
            'id':p.group_id,
            'caption':p.caption,
            'tag':p.tag,
            'product_list':p.product_list,
            'description':p.description,
            'remarks':p.remarks})
    info_data = []
    for info in Info.objects.all():
        info_data.append({'info_id':info.info_id,'sn':info.sn,'func_uid':info.func_uid,'version':info.version,'issued':info.issued,'expiration':info.expiration,
        'count':info.count,'registration':info.registration,'type':info.type,'comment':info.comment,'contact':info.contact,'info':info.info})
    sn_dict = {}
    for sn in Sn.objects.all():
        sn_dict.setdefault(sn.sn,{'sn_id':sn.sn_id,'region':sn.region,'user':sn.user,'record':sn.record,
        'note1':sn.note1,'note2':sn.note2,'note3':sn.note3,'note4':sn.note1,'note5':sn.note1})
    return HttpResponse(json.dumps({
        'product_groups':product_groups,
        'info_data':info_data,
        'sn_dict':sn_dict
        }))
@csrf_exempt
def save_to_product_group(request):
    '''新增產品群組'''
    if request.method == 'POST':
        caption = json.loads(request.body)['caption']
        tag = json.loads(request.body)['tag']
        product_list = json.loads(request.body)['product_list']
        description = json.loads(request.body)['description']
        remarks = json.loads(request.body)['remarks']
        for i in range(1,len(Product_groups.objects.all())+2):#將新增資料填充再有空的info_id位置
            if not Product_groups.objects.filter(group_id = i):
                Product_groups.objects.create(#將修改的資料放入資料庫
                group_id = i,
                caption = caption,
                tag = tag,
                product_list = product_list,
                description = description,
                remarks = remarks)
                break
        return HttpResponse('新增產品群組')


#---------------------handle----------------------#           
@csrf_exempt
def data_to_handle(request):
    '''資料傳入handle'''
    info_data = []
    for info in Info.objects.all():
        info_data.append({'info_id':info.info_id,'sn':info.sn,'func_uid':info.func_uid,'version':info.version,'issued':info.issued,'expiration':info.expiration,
        'count':info.count,'registration':info.registration,'type':info.type,'comment':info.comment,'contact':info.contact,'info':info.info})
    sn_dict = {}
    for sn in Sn.objects.all():
        sn_dict.setdefault(sn.sn,{'sn_id':sn.sn_id,'region':sn.region,'user':sn.user,'record':sn.record,
        'note1':sn.note1,'note2':sn.note2,'note3':sn.note3,'note4':sn.note1,'note5':sn.note1})
    return HttpResponse(json.dumps({
        'info_data':info_data,
        'sn_dict':sn_dict
        }))
@csrf_exempt
def handle_edit(request):
    '''修改資料庫edit資料'''
    if request.method == 'GET':
        user = json.loads(request.GET['user'])#
        newrow = json.loads(request.GET['Newrow'])#更改後的資料
        Edit.objects.filter(user = user[0]).update(data=json.dumps(newrow))
    return HttpResponse('成功修改申請頁面資料')
@csrf_exempt
def F5_handle(request):
    '''申請頁面返回時確認有無data是空的資料'''
    if request.method == 'GET':
        attachments = json.loads(request.GET['upload_file_name'])
        for file in attachments:#回到主畫面時要刪除以上傳的檔案
            os.remove(file)
    return HttpResponse('F5後，將上傳的本地檔案刪除')
@csrf_exempt
def upload_on_local(request):
    '''將上傳的檔案下載到本地端'''
    if request.method == 'POST':
        imgdata = request.FILES.get('file').read()
        file=open(request.POST['name'],'wb')  
        file.write(imgdata)  
        file.close()
    return HttpResponse("上傳檔案下載成功!")
@csrf_exempt
def delete_upload_local(request):
    '''將刪除的檔案從本地端本地端刪除'''
    if request.method == 'GET':
        remove_name = request.GET['name']
        if os.path.isfile(remove_name):
            os.remove(remove_name)
    return HttpResponse("上傳檔案下載成功!")
@csrf_exempt
def download(request):
    '''申請頁面底下的申請資料下載'''
    if request.method == 'GET':#download
        user = json.loads(request.GET['user'])
        workbook = write_license_applicationXLSX(user[0], user[0],json.loads(Edit.objects.get(user=user[0]).data))
        response = HttpResponse(content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=license-application.xlsx'
        workbook.save(response)
        workbook.close()
        return response
@csrf_exempt
def handle_back_ShowAll(request):
    '''申請頁面返回時確認有無data是空的資料'''
    if request.method == 'GET':
        user = json.loads(request.GET['user'])
        attachments = json.loads(request.GET['upload_file_name'])
        for file in attachments:#回到主畫面時要刪除以上傳的檔案
            os.remove(file)
        if Edit.objects.filter(user=user[0]):
            if Edit.objects.get(user = user[0]).data == '[]':
                Edit.objects.get(user = user[0]).delete()
    return HttpResponse('申請頁面返回主畫面')
@csrf_exempt
def handle_delete(request):
    '''刪除資料庫edit資料'''
    if request.method == 'GET':
        user = json.loads(request.GET['user'])#
        row = json.loads(request.GET['Row'])
        Edit.objects.filter(user = user[0]).update(data=json.dumps(row))
    return HttpResponse('刪除資料庫edit資料')
#-------------------寄信處理(handle)----------------#
def create_message_handle(msgPlain, cc, username,attachments,mode,origin_data,xlsx,type):
    '''附帶xlsx檔案進申請通知信件中'''
    workbook = write_license_applicationXLSX(username, username,json.loads(Edit.objects.get(user=username).data))
    output = BytesIO()
    workbook.save(output)
    workbook.close()
    #建立郵件主題
    msg = MIMEMultipart()
    if type == 'applicant':
        msg['Subject'] = variable.handle_applicant_title + ' ' + str(len(Application.objects.all())+1)#申請確認信給申請人的主旨
    elif type == 'verify':
        msg['Subject'] = variable.handle_verify_title + ' '+ str(len(Application.objects.all())+1)#申請審核通知信給審核人的主旨
    msg['To'] = variable.Sender_email_account#寄給誰
    msg["cc"] = cc#副本

    #msg.attach(MIMEText(msgPlain, 'plain'))#將信件內文傳入email中
    if mode == 'html':
        msg.attach(MIMEText(msgPlain+ tr_html_table(json.loads(Edit.objects.get(user=username).data),origin_data) + \
                    "<br>已經收到您的申請,請等待審核結果,謝謝." + \
                    "<br>We have received your application,Please wait for the audit results.Thank you."+ \
                    "<br>此信件為系統回覆,請勿回覆此信件 如有疑問請聯絡 Claire(claire@eastek.com.tw) ,謝謝", 'html'))#將信件內文傳入email中
    else:
        msg.attach(MIMEText(msgPlain, 'plain'))#將信件內文傳入email中
    for file in attachments:#負責上傳檔案的夾帶
        with open(file, 'rb') as fp:
            add_file = MIMEBase('application', "octet-stream")
            add_file.set_payload(fp.read())
        encoders.encode_base64(add_file)
        add_file.add_header('Content-Disposition', 'attachment', filename=file)
        msg.attach(add_file)
    
    if xlsx == True:
        part = MIMEApplication(output.getvalue())#負責xlsx的夾帶
        part.add_header('Content-Disposition', 'attachment', filename="license-application.xlsx")
        msg.attach(part)

    return msg.as_bytes()
def tr_html_table(data,origin_data):
    '''夾帶html table給信件'''
    html_text='''
    <body>
    <div>
    <div><span style="background-color:#98FB98">綠色</span>->有修改的部分，可以與上一欄原資料比較</div>
    <div><span style="background-color:#fcff72">黃色</span>->新客戶</div>
    <div><span style="background-color:#ff0000">紅色</span>->唯一值(sn碼+產品+類型)與新增(下一欄)有衝突，請確認此次申請有無刪除衝突資料</div>
    </div>
    <br>'''
    html_text += '''
    <table border='1'>
    <tr>
        <th width="100">操作</th>
        <th width="130">客戶</th>
        <th width="100">KeyID</th>
        <th width="210">產品名稱</th>
        <th width="100">版本</th>
        <th width="70">類型</th>
        <th width="70">數量</th>
        <th width="90">到期日</th>
        <th width="100">地區</th>
        <th width="150">備註</th>
        <th width="150">聯絡人</th>
    </tr>'''
    for d in data:
        if d['operator'] == '刪除':
            test = 0
            for d_test in data:#查看是否衝突資料
                if d_test['operator'] == '新增':
                    if d_test['sn'] == d['sn'] and d_test['type'] == d['type'] and d_test['func_uid'] == d['func_uid']:
                        html_text+=('<tr align="center">'+
                        '<td width="100">'+ str(d['operator'])+'</td>'+
                        '<td width="130">'+ str(d['customer'])+'</td>'+
                        '<td style="width:100px;background-color:#ff0000">'+ str(d['sn'])+'</td>'+
                        '<td style="width:210px;background-color:#ff0000">'+ str(d['func_uid'])+'</td>'+
                        '<td width="100">'+ str(d['version'])+'</td>'+
                        '<td style="width:70px;background-color:#ff0000">'+ str(d['type'])+'</td>'+
                        '<td width="70">'+ str(d['count'])+'</td>'+
                        '<td width="90">'+ str(d['expiration'])+'</td>'+
                        '<td width="100">'+ str(d['region'])+'</td>'+ 
                        '<td width="150">'+ str(d['comment'])+'</td>'+
                        '<td width="150">'+ str(d['contact'])+'</td>'+
                        '</tr>')
                        test = 1
            if test == 0:
                html_text+=('<tr align="center">'+
                    '<td width="100">'+ str(d['operator'])+'</td>'+
                    '<td width="130">'+ str(d['customer'])+'</td>'+
                    '<td width="100">'+ str(d['sn'])+'</td>'+
                    '<td width="210">'+ str(d['func_uid'])+'</td>'+
                    '<td width="100">'+ str(d['version'])+'</td>'+
                    '<td width="70">'+ str(d['type'])+'</td>'+
                    '<td width="70">'+ str(d['count'])+'</td>'+
                    '<td width="90">'+ str(d['expiration'])+'</td>'+
                    '<td width="100">'+ str(d['region'])+'</td>'+ 
                    '<td width="150">'+ str(d['comment'])+'</td>'+
                    '<td width="150">'+ str(d['contact'])+'</td>'+
                '</tr>')
        elif d['operator'] == '新增':
            customer = d['customer'].split('|')
            if len(customer) == 1:
                customer.append('')
            if not (Customers.objects.filter(name = customer[0]).filter(site = customer[1])):#若客戶是新增的則顯示黃色
                html_text+=('<tr align="center">'+
                '<td width="100">'+ str(d['operator'])+'</td>'+
                '<td style="width:130px;background-color:#fcff72">'+ str(d['customer'])+'</td>'+
                '<td width="100">'+ str(d['sn'])+'</td>'+
                '<td width="210">'+ str(d['func_uid'])+'</td>'+
                '<td width="100">'+ str(d['version'])+'</td>'+
                '<td width="70">'+ str(d['type'])+'</td>'+
                '<td width="70">'+ str(d['count'])+'</td>'+
                '<td width="90">'+ str(d['expiration'])+'</td>'+
                '<td width="100">'+ str(d['region'])+'</td>'+ 
                '<td width="150">'+ str(d['comment'])+'</td>'+
                '<td width="150">'+ str(d['contact'])+'</td>'+
                '</tr>')
            else:
                html_text+=('<tr align="center">'+
                '<td width="100">'+ str(d['operator'])+'</td>'+
                '<td width="130">'+ str(d['customer'])+'</td>'+
                '<td width="100">'+ str(d['sn'])+'</td>'+
                '<td width="210">'+ str(d['func_uid'])+'</td>'+
                '<td width="100">'+ str(d['version'])+'</td>'+
                '<td width="70">'+ str(d['type'])+'</td>'+
                '<td width="70">'+ str(d['count'])+'</td>'+
                '<td width="90">'+ str(d['expiration'])+'</td>'+
                '<td width="100">'+ str(d['region'])+'</td>'+ 
                '<td width="150">'+ str(d['comment'])+'</td>'+
                '<td width="150">'+ str(d['contact'])+'</td>'+
                '</tr>')
        elif d['operator'] == '修改':
            for origin_info in origin_data:
                if d['info_id'] == origin_info['info_id']:
                    html_text+=('<tr align="center">'+
                    '<td width="100">'+ '原資料'+'</td>'+#原資料
                    '<td width="130">'+ str(origin_info['customer'])+'</td>'+
                    '<td width="100">'+ str(origin_info['sn'])+'</td>'+
                    '<td width="210">'+ str(origin_info['func_uid'])+'</td>'+
                    '<td width="100">'+ str(origin_info['version'])+'</td>'+
                    '<td width="70">'+ str(origin_info['type'])+'</td>'+
                    '<td width="70">'+ str(origin_info['count'])+'</td>'+
                    '<td width="90">'+ str(origin_info['expiration'])+'</td>'+
                    '<td width="100">'+ str(origin_info['region'])+'</td>'+ 
                    '<td width="150">'+ str(origin_info['comment'])+'</td>'+
                    '<td width="150">'+ str(origin_info['contact'])+'</td>'+
                    '</tr>')
                    html_text+=('<tr align="center">'+
                    '<td width="100">'+ str(d['operator'])+'</td>'+
                    '<td width="130">'+ str(d['customer'])+'</td>'+
                    '<td width="100">'+ str(d['sn'])+'</td>')
                    if d['func_uid'] != origin_info['func_uid']:
                        html_text+=('<td style="width:210px;background-color:#98FB98">'+ str(d['func_uid'])+'</td>')
                    else:
                        html_text+=('<td width="210">'+ str(d['func_uid'])+'</td>')
                    if d['version'] != origin_info['version']:
                        html_text+=('<td style="width:100px;background-color:#98FB98">'+ str(d['version'])+'</td>')
                    else:
                        html_text+=('<td width="100"'+ str(d['version'])+'</td>')
                    if d['type'] != origin_info['type']:
                        html_text+=('<td style="width:70px;background-color:#98FB98">'+ str(d['type'])+'</td>')
                    else:
                        html_text+=('<td width="70">'+ str(d['type'])+'</td>')
                    if d['count'] != origin_info['count']:
                        html_text+=('<td style="width:70px;background-color:#98FB98">'+ str(d['count'])+'</td>')
                    else:
                        html_text+=('<td width="70">'+ str(d['count'])+'</td>')
                    if d['expiration'] != origin_info['expiration']:
                        html_text+=('<td style="width:90px;background-color:#98FB98">'+ str(d['expiration'])+'</td>')
                    else:
                        html_text+=('<td width="90">'+ str(d['expiration'])+'</td>')
                    if d['region'] != origin_info['region']:
                        html_text+=('<td style="width:100px;background-color:#98FB98">'+ str(d['region'])+'</td>')
                    else:
                        html_text+=('<td width="100">'+ str(d['region'])+'</td>')
                    if d['comment'] != origin_info['comment']:
                        html_text+=('<td style="width:150px;background-color:#98FB98">'+ str(d['comment'])+'</td>')
                    else:
                        html_text+=('<td width="150">'+ str(d['comment'])+'</td>')
                    if d['contact'] != origin_info['contact']:
                        html_text+=('<td style="width:150px;background-color:#98FB98">'+ str(d['contact'])+'</td></tr>')
                    else:
                        html_text+=('<td width="150">'+ str(d['contact'])+'</td></tr>')
    html_text += "</table></body>"
    return html_text
@csrf_exempt
def handle_send(request):
    '''審核後傳送審核結果通知信 及 確認信'''
    if request.method == 'POST':#send
        content = json.loads(request.body)['content']
        date = datetime.today()
        edit_data = json.loads(request.body)['edit_data']
        Application.objects.create(#把edit資料轉到application
            application_id = len(Application.objects.all())+1,
            date = date.strftime('%Y-%m-%d %H:%M:%S'),
            applicant = content['user'],
            status = 'wait_for_verification',
            data = json.dumps(edit_data),
            validator = json.dumps({'verify_group':variable.verify_group,'verify_user':variable.verify_user,'verify_num':variable.verify_num
                                    ,'verify_check':variable.verify_check}),
            verify_time = '',
            content = json.dumps(content)
        )
        #^^^^^^^^^^^^^^^^^^^^^^^^^^先儲存在application table^^^^^^^^^^^^^^^^^^^^^^^^^^^#
        attachments = json.loads(request.body)['upload_file_name']
        origin_data = json.loads(request.body)['origin_data']#用來寄信夾帶html table時對比修改資料
        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(variable.Sender_email_account,variable.Sender_email_password)
        verify_members = []
        for mem in json.loads(Groups.objects.get(name = 'product-verification').members):#把審核者群組的成員信箱push到verify_members
            verify_members.append(Users.objects.get(user_id = mem).email)
        for email in verify_members:
            msgPlain =  "審核人地址: " + json.dumps(verify_members).replace('[','').replace(']','') + \
                        "\nText: " + content['text'] + \
                        "\n審核網址: " + 'https://vue-test-simple.herokuapp.com/#/check/'+ Users.objects.get(email = email).user
            message = create_message_handle(msgPlain, json.dumps(verify_members).replace('[','').replace(']',''), content['user'],attachments,'plain',origin_data,True,'verify')#msgPlan內文
            
            from_addr=variable.Sender_email_account
            to_addr = email#
            status = mailServer.sendmail(from_addr, to_addr, message)#送給審核人
            if(status != {}):
                return HttpResponse("郵件傳送失敗!")#沒傳遞成功則不刪
        #-------------------^審核通知信^------------------#
        msgPlain =  "<span>申請人: " + content['user']+ \
                    "</span><br><span>申請說明</span>"
                    #"<br>Text:" + content['text']
        message = create_message_handle(msgPlain, content['cc'], content['user'],attachments,'html',origin_data,False,'applicant')#msgPlan內文
        from_addr=variable.Sender_email_account
        to_addr = Users.objects.get(user = content['user']).email
        mailServer.sendmail(from_addr, to_addr, message)#送給申請人
        if content['cc'] != '':
            other_mail = content['cc'].split(',')
            for to_addr in other_mail:
                mailServer.sendmail(from_addr, to_addr, message)#送副本內的聯絡人
        mailServer.close()
        #最後將attachments從本地端刪除↓
        for file in attachments:
            os.remove(file)
        #--------------------^申請確認信^----------------#
        
        Edit.objects.filter(user=content['user']).delete()#傳遞成功就刪申請資料
        return HttpResponse("郵件傳送成功!")


#----------------------check-----------------------#
@csrf_exempt
def dialog_check(request):
    '''check頁面dialog確認後，操作DB'''
    if request.method == 'POST':
        check_data = json.loads(request.body)['check_data']
        user = json.loads(request.body)['user']
        Application.objects.filter(application_id = check_data['id']).update(content=check_data['content'],data=check_data['data'])
        groups_name = []
        for group_id in json.loads(Users.objects.get(user = user[0]).groups):#審核者自身群組
           groups_name.append(Groups.objects.get(group_id = group_id).caption)

        validator = check_data['validator']
        print(validator)
        for index,verify_gpname in enumerate(validator['verify_group']):#審核verify_group
            if verify_gpname in groups_name:
                validator['verify_check']['verify_group'][index] = True
                
        for index,vfy_email in enumerate(validator['verify_user']):#審核verify_email
            if vfy_email == user[0]:
                validator['verify_check']['verify_user'][index] = True
        validator['verify_check']['verify_num']+=1
        Application.objects.filter(application_id = check_data['id']).update(validator=json.dumps(validator))
        print(validator)
        return HttpResponse('哈哈')
@csrf_exempt
def check_verify(request):
    '''審核送出'''
    if request.method == 'POST':
        verify_Data = json.loads(request.body)['verify_Data']
        verifier = json.loads(request.body)['user']
        i = 0
        for verify in verify_Data:
            if verify['data'] != '[]':
                Application.objects.filter(application_id = verify['id']).update(content=verify['content'],data=verify['data'])
                Application.objects.filter(application_id = verify['id']).update(verify_time=json.dumps(datetime.today().strftime('%Y-%m-%d %H:%M:%S')))
            else:
                Application.objects.filter(application_id = verify['id']).delete()
        User_record = []
        for verify in verify_Data:
            app = Application.objects.get(application_id = verify['id'])#將application所有申請人等於user的資料全部放入user(record)
            if app.status == 'wait_for_verification':
                User_record = Users.objects.get(user = app.applicant).record
                if User_record == '':
                    User_record = []
                else:
                    User_record = json.loads(User_record)
                User_record.append({'id': app.application_id,'date':app.date,'applicant':app.applicant,'status':app.status,'data':app.data,
                'validator':app.validator,'verify_time':app.verify_time,'content':app.content})
                Users.objects.filter(user = app.applicant).update(record = json.dumps(User_record))
                Sn_record = []
                for app_data in json.loads(app.data):#將application data 將資料根據sn儲存在sn(record)中(只放verify = √)
                    if app_data['verify'] == '√':
                        operator_DB(app_data)
                        Sn_record = Sn.objects.get(sn = app_data['sn']).record
                        if Sn_record == '':
                            Sn_record = []
                        else:
                            Sn_record = json.loads(Sn_record)
                        Sn_record.append(app_data)
                        Sn.objects.filter(sn = app_data['sn']).update(record = json.dumps(Sn_record))
                write_local_from_web.web_to_local()#更新local_DB
        check_send(verifier,verify_Data)
        for verify in verify_Data:
            test = 0
            for data in json.loads(verify['data']):
                if data['verify'] != '√':
                    Application.objects.filter(application_id = verify['id']).update(status='nopass')
                    test = 1
            if test == 0:
                Application.objects.filter(application_id = verify['id']).update(status='pass')
        
        return HttpResponse('審核成功')
@csrf_exempt
def download_check(request):
    '''審查頁面dialog內的審核資料下載'''
    if request.method == 'POST':
        data = json.loads(request.body)['data']
        data['data'] = json.loads(data['data'])
        data['content'] = json.loads(data['content'])
        workbook = write_license_applicationXLSX(data['content']['user'], data['content']['user'],data['data'])
        response = HttpResponse(content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=verify-application.xlsx'
        workbook.save(response)
        workbook.close()
        return response
@csrf_exempt
@gzip_page
def check(request,verifyname):
    '''審核頁面資料傳入'''
    module_data = []
    for mod in Modules.objects.all():
        module_data.append({'mod_uid':mod.mod_uid,'caption':mod.caption})

    customer_data = []
    for customer in Customers.objects.all():
        customer_data.append({'customer_id':customer.customer_id,'name':customer.name,'site':customer.site})

    product_data = []
    for product in Products.objects.all():
        product_data.append({'product_id':product.product_id,'category_id':product.category_id,
        'product_name':product.product_name,'caption':product.caption,'remarks':product.remarks})

    region_data = []
    for region in Region.objects.all():
        region_data.append({'region_id':region.region_id,'name':region.name,'description':region.description})

    sn_dict = {}
    sn_data = []
    for sn in Sn.objects.all():
        sn_data.append({'sn_id':sn.sn_id,'sn':sn.sn,'region':sn.region,'user':sn.user,
        'record':sn.record,'note1':sn.note1,'note2':sn.note2,'note3':sn.note3,'note4':sn.note1,'note5':sn.note1})
        sn_dict.setdefault(sn.sn,{'sn_id':sn.sn_id,'region':sn.region,'user':sn.user,'record':sn.record,
        'note1':sn.note1,'note2':sn.note2,'note3':sn.note3,'note4':sn.note1,'note5':sn.note1})
    info_data = []
    for info in Info.objects.all():
        info_data.append({'info_id':info.info_id,'sn':info.sn,'func_uid':info.func_uid,'version':info.version,'issued':info.issued,'expiration':info.expiration,
            'count':info.count,'registration':info.registration,'type':info.type,'comment':info.comment,'contact':info.contact,'info':info.info})

    user_data = []
    for user in Users.objects.all():
        user_data.append({'user_id':user.user_id,'user':user.user,'password':user.password,'email':user.email,'groups':user.groups,'region':user.region,'record':user.record,'description':user.description})

    group_data = []
    for group in Groups.objects.all():
        group_data.append({'group_id':group.group_id,'name':group.name,'caption':group.caption,'authority':group.authority,'description':group.description,'members':group.members})

    edit_data = []
    for edit in Edit.objects.all():
        if(edit.user == verifyname):#只傳送當前使用者的資料
            edit_data.append({'cc':edit.cc,'user':edit.user,'comment':edit.comment,'data':edit.data})

    application_data = []
    for application in Application.objects.all():
        if application.status == 'wait_for_verification':
            application_data.append({'id':application.application_id,'date':application.date,'applicant':application.applicant,'status':application.status,
            'data':application.data,'validator':application.validator,'verify_time':application.verify_time,'content':application.content})
    option_dict = {}
    option_data = []
    for option in Options.objects.all():
        option_data.append({'id':option.option_id,'product_name':option.product_name,
        'option_name':option.option_name,'caption':option.caption,'remarks':option.remarks})
        option_dict.setdefault(option.option_name,{'id':option.option_id,'product_name':option.product_name,
        'caption':option.caption,'remarks':option.remarks})
    return HttpResponse(json.dumps({
        'module_data':module_data,
        'customer_data':customer_data,
        'product_data':product_data,
        'region_data':region_data,
        'sn_data':sn_data,
        'info_data':info_data,
        'option_data':option_data,
        'user_data':user_data,
        'group_data':group_data,
        'edit_data':edit_data,
        'application_data':application_data,
        'sn_dict':sn_dict,
        'option_dict':option_dict,
        'user':str(verifyname)
        }))
def check_send(verifier,verify_Data):
    '''發送審核結果通知信'''
    for app in verify_Data:
        if app['status'] == 'wait_for_verification':
            mailServer = smtplib.SMTP('smtp.gmail.com', 587)
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login(variable.Sender_email_account,variable.Sender_email_password)
            from_addr=variable.Sender_email_account
            content = json.loads(app['content'])
            verify_members = []
            for mem in json.loads(Groups.objects.get(name = 'product-verification').members):
                verify_members.append(Users.objects.get(user_id = mem).email)
            for email in verify_members:
                            #"Cc: " + json.dumps(verify_members).replace('[','').replace(']','') + \
                            #"<br>審核人: 「" + verifier[0] + '」' + \
                msgPlain =  "Text:" 
                message = create_message_check(msgPlain,verifier,app,content,json.dumps(verify_members).replace('[','').replace(']',''),'html','verify')#msgPlan內文
                from_addr=variable.Sender_email_account
                to_addr = email#
                status = mailServer.sendmail(from_addr, to_addr, message)#送給審核人
                if(status != {}):
                    return HttpResponse("郵件傳送失敗!")#沒傳遞成功則不刪
            #--------------------^審核結果通知信(to 審核者)^------------------------------#
                        #"Cc: " + content['cc'] + \
                        #"<br>審核人: 「" + verifier[0] + "」" + \
            msgPlain =  "Text:" + \
                        "<br>審核者回覆: 「" + content['reply'] + "」"
            message = create_message_check(msgPlain,verifier,app,content,content['cc'],'html','applicant')#msgPlan內文
            
            to_addr = Users.objects.get(user = content['user']).email
            status = mailServer.sendmail(from_addr, to_addr, message)#送給申請人
            if content['cc'] != '':
                other_mail = content['cc'].split(',')
                for to_addr in other_mail:
                    mailServer.sendmail(from_addr, to_addr, message)#送副本內的聯絡人
            mailServer.close()
            #--------------------^審核結果通知信(to 申請人)^------------------------------#
#-----------------寄信處理(check)-------------------#
def create_message_check(msgPlain,verifier,verify_Data,content,cc,mode,type):
    '''建立郵件主題'''
    msg = MIMEMultipart()
    if type == 'applicant':
        msg['Subject'] = variable.check_applicant_title + ' '+ str(verify_Data['id'])#審核確認信給申請人的主旨
    elif type == 'verify':
        msg['Subject'] = variable.check_verify_title + ' ' + str(verify_Data['id'])#審核確認信給審核人的主旨
    msg['To'] = variable.Sender_email_account#寄給誰
    msg["cc"] = cc#副本

    #msg.attach(MIMEText(msgPlain, 'plain'))#將信件內文傳入email中
    if mode == 'html':
        msg.attach(MIMEText(msgPlain+ tr_html_table_check(verify_Data,content) + \
                    "<br>審核者: 「" + verifier[0] + "」" + \
                    "<br>申請已審核完畢,謝謝." + \
                    "<br>We have check your application,Thank you."+ \
                    "<br>此信件為系統回覆,請勿回覆此信件 如有疑問請聯絡 Claire(claire@eastek.com.tw) ,謝謝", 'html'))#將信件內文傳入email中
    else:
        msg.attach(MIMEText(msgPlain, 'plain'))#將信件內文傳入email中

    return msg.as_bytes()
def tr_html_table_check(data,content):
    '''夾帶html table給信件'''
    html_text='''
    <body>
    <div>
    <div><span style="background-color:#98FB98">綠色</span>->通過</div>
    <div><span style="background-color:#ff0000">紅色</span>->不通過</div>
    </div>
    <br>'''
    if content['text'] == '':
        html_text +="<div><span>申請內文: "+'無'+"</span><div>"
    else:
        html_text +="<div><span>申請內文: "+content['text']+"</span><div>"
    html_text += '''
    <table border='1'>
    <tr>
        <th width="70">結果</th>
        <th width="150">原因</th>
        <th width="70">操作</th>
        <th width="130">客戶</th>
        <th width="90">更新日期</th>
        <th width="100">KeyID</th>
        <th width="210">產品名稱</th>
        <th width="100">版本</th>
        <th width="70">類型</th>
        <th width="70">數量</th>
        <th width="90">到期日</th>
        <th width="70">地區</th>
        <th width="150">備註</th>
        <th width="150">聯絡人</th>
    </tr>'''
    for d in json.loads(data['data']):
        html_text+='<tr align="center">'
        if d['verify'] == '√':
            html_text+=('<td style="font-size:16px;width:70px;background-color:#98FB98">'+ str(d['verify'])+'</td>')
        else:
            html_text+=('<td style="font-size:20px;width:70px;background-color:#ff0000">'+ str(d['verify'])+'</td>')
        html_text+=(
        '<td width="150">'+ str(d['reason'])+'</td>'+
        '<td width="70">'+ str(d['operator'])+'</td>'+
        '<td width="130">'+ str(d['customer'])+'</td>'+
        '<td width="90">'+ str(d['issued'])+'</td>'+
        '<td width="100">'+ str(d['sn'])+'</td>'+
        '<td width="210">'+ str(d['func_uid'])+'</td>'+
        '<td width="100">'+ str(d['version'])+'</td>'+
        '<td width="70">'+ str(d['type'])+'</td>'+
        '<td width="70">'+ str(d['count'])+'</td>'+
        '<td width="90">'+ str(d['expiration'])+'</td>'+
        '<td width="70">'+ str(d['region'])+'</td>'+ 
        '<td width="150">'+ str(d['comment'])+'</td>'+
        '<td width="150">'+ str(d['contact'])+'</td>'+
            '</tr>')
    html_text += "</table></body>"
    return html_text


#------------------製成excel檔(公共)----------------#
def write_license_applicationXLSX(username, applicant,data):
    '''將Edit中的資料寫進excel'''
    workbook = Workbook()
    order_forms = []
    last_update_time = Updatetime.objects.get(id="last_update_time").update_time

    for check in data:
        order_forms.append(check)

    SCALING_RATIO = 5.0885

    # 表格大小
    worksheet = workbook.active
    worksheet.sheet_format.defaultColWidth = 1.71 * SCALING_RATIO
    worksheet.sheet_format.defaultRowHeight = 12.7

    worksheet.column_dimensions['A'].width = 1.71 * SCALING_RATIO
    worksheet.column_dimensions['B'].width = 1.89 * SCALING_RATIO
    worksheet.column_dimensions['C'].width = 1.94 * SCALING_RATIO
    worksheet.column_dimensions['D'].width = 2.44 * SCALING_RATIO
    worksheet.column_dimensions['E'].width = 2.19 * SCALING_RATIO
    worksheet.column_dimensions['F'].width = 4.36 * SCALING_RATIO
    worksheet.column_dimensions['G'].width = 5.01 * SCALING_RATIO
    worksheet.column_dimensions['H'].width = 1.71 * SCALING_RATIO
    worksheet.column_dimensions['I'].width = 2.72 * SCALING_RATIO
    worksheet.column_dimensions['J'].width = 1.96 * SCALING_RATIO
    worksheet.column_dimensions['K'].width = 2.36 * SCALING_RATIO
    worksheet.column_dimensions['L'].width = 2.36 * SCALING_RATIO
    worksheet.column_dimensions['M'].width = 5.39 * SCALING_RATIO
    worksheet.column_dimensions['N'].width = 2.83 * SCALING_RATIO
    worksheet.column_dimensions['O'].width = 5.39 * SCALING_RATIO
    worksheet.column_dimensions['P'].width = 2.72 * SCALING_RATIO

    for i in range(1, len(order_forms)+2):
        worksheet.row_dimensions[i].height = 16.37

    # 表格對齊
    for cell in worksheet['A1':'P1'][0]:
        cell.alignment = Alignment(horizontal='center', vertical='center')

    worksheet.freeze_panes = "A1"

    # 表格資料
    worksheet['A1'] = '更新'
    worksheet['B1'] = '申請人'
    worksheet['C1'] = '申請類別'
    worksheet['D1'] = '客戶'
    worksheet['E1'] = '申請日期'
    worksheet['F1'] = '產品編號/ID號碼(sn)'
    worksheet['G1'] = '產品名稱'
    worksheet['H1'] = '類型'
    worksheet['I1'] = '數量(USER)'
    worksheet['J1'] = '使用期限'
    worksheet['K1'] = '地區'
    worksheet['L1'] = '備註'
    worksheet['M1'] = '聯絡人'
    worksheet['N1'] = '最後更新時間'
    worksheet['O1'] = last_update_time
    worksheet['P1'] = '版本'

    row_index_iterater = iter(range(len(order_forms)))

    for order_form in order_forms:
        str_row_index = str(next(row_index_iterater) + 2)
        worksheet['A' + str_row_index] = "o"
        worksheet['B' + str_row_index] = applicant
        worksheet['C' + str_row_index] = order_form['operator']
        worksheet['D' + str_row_index] = order_form['customer']
        worksheet['E' + str_row_index] = order_form['issued']
        worksheet['F' + str_row_index] = order_form['sn']
        worksheet['G' + str_row_index] = order_form['func_uid']
        worksheet['H' + str_row_index] = order_form['type']
        worksheet['I' + str_row_index] = order_form['count']
        worksheet['J' + str_row_index] = order_form['expiration']
        worksheet['K' + str_row_index] = order_form['region']
        worksheet['L' + str_row_index] = order_form['comment']
        worksheet['M' + str_row_index] = order_form['contact']
        worksheet['P' + str_row_index] = order_form['version']

    return workbook


#--------------審核確認送出後修改資料庫--------------#
def operator_DB(data):
    '''審核送出後修改DB'''
    print(data)
    deter_option = data['func_uid'][::-1].split('(')[0].replace(')','')[::-1]
    if Options.objects.filter(product_name = deter_option):
        data['func_uid'] = data['func_uid'].replace('('+deter_option+')','')
        func_uid = Options.objects.get(product_name = deter_option,caption=data['func_uid']).option_name
    else:
        func_uid = Modules.objects.get(caption = data['func_uid']).mod_uid#將caption轉mod_uid ezCAM->ezcam_starting
    type = Modules.objects.get(caption = data['type']).mod_uid#將caption轉mod_uid ex:正式->OFFICAL
    if data['operator'] == '刪除':
        Info.objects.filter(info_id = data['info_id']).delete()
    elif data['operator'] == '修改':
        if ',' in data['contact']:
            data['contact'] = data['contact'].split(',')
            for i in range(0,len(data['contact'])):
                for user in Users.objects.all():
                    if data['contact'][i] == user.user:
                        data['contact'][i] = user.email
            data['contact'] = ','.join(data['contact'])
        if '@' not in data['contact']:#將被轉成user名子的信箱再轉換回email address
            for user in Users.objects.all():
                if data['contact'] == user.user:
                    data['contact'] = user.email
        Sn.objects.filter(sn = data['sn']).update(
            sn = data['sn'],
            region = Region.objects.get(name = data['region']).region_id,
            user = data['user'],
            record = '',
            note1 = '',
            note2 = '',
            note3 = '',
            note4 = '',
            note5 = ''
            )
        #-----------------若有修改type的情況--------------------#
        if type != Info.objects.get(info_id = data['info_id']).type:
            same_info_id = None#紀錄與修改資料相同 sn func_uid type相同之資料之info_id
            for info in Info.objects.all():
                if type == info.type and func_uid == info.func_uid and data['sn'] == info.sn:
                    same_info_id = info.info_id
            if same_info_id != None:#情況一type A -> B (B已存在)        #* 做法: 
                Info.objects.filter(info_id = data['info_id']).delete()#    1. 將 A 資料刪除
                Info.objects.filter(info_id = same_info_id).update(    #    2. 將 B 資料修改(個數為 A+B 總和)
                    count = data['count'] + Info.objects.get(info_id = same_info_id).count,
                    expiration = data['expiration'],
                )
            else:#情況2 type A -> B (B不存在)                          #* 做法: 
                Info.objects.filter(info_id = data['info_id']).delete()#    1. 將 A 資料刪除
                for i in range(0,len(Info.objects.all())+1):#將新增資料填充再有空的info_id位置
                    if not Info.objects.filter(info_id = i):
                        Info.objects.create(                           #2. 新增 B 資料
                            info_id = i,
                            sn = data['sn'],
                            func_uid = func_uid,
                            version = data['version'],
                            issued = data['issued'],
                            expiration = data['expiration'],
                            count = data['count'],
                            registration = data['registration'],
                            type = type,
                            comment = data['comment'],
                            contact = data['contact'],
                            info = data['info'],
                        )
                        break
        else:#沒改type的情況
            Info.objects.filter(info_id = data['info_id']).update(
                sn = data['sn'],
                func_uid = func_uid,
                version = data['version'],
                issued = data['issued'],
                expiration = data['expiration'],
                count = data['count'],
                registration = data['registration'],
                type = type,
                comment = data['comment'],
                contact = data['contact'],
                info = data['info'],
            )
    elif data['operator'] == '新增':
        if not Sn.objects.filter(sn = data['sn']):#若新增介面 新增全新客戶則增加Customer及sn以對應新資料
            customer = data['customer'].split('|')
            if len(customer) == 1:
                customer.append('')
            if not (Customers.objects.filter(name = customer[0]).filter(site = customer[1])):
                for i in range(1,len(Customers.objects.all())+2):
                    if not Customers.objects.filter(customer_id = i):
                        Customers.objects.create(customer_id = i,name = customer[0],site = customer[1])
                        break
            Sn.objects.create(
                sn_id = Customers.objects.get(name = customer[0],site = customer[1]).customer_id,
                sn = data['sn'],
                region = Region.objects.get(name = data['region']).region_id,
                user = data['user'],
                record = '',
                note1 = '',
                note2 = '',
                note3 = '',
                note4 = '',
                note5 = ''
                )
        if ',' in data['contact']:
            data['contact'] = data['contact'].split(',')
            for i in range(0,len(data['contact'])):
                for user in Users.objects.all():
                    if data['contact'][i] == user.user:
                        data['contact'][i] = user.email
            data['contact'] = ','.join(data['contact'])
        if '@' not in data['contact']:#將被轉成user名子的信箱再轉換回email address
            for user in Users.objects.all():
                if data['contact'] == user.user:
                    data['contact'] = user.email

        for i in range(1,len(Info.objects.all())+2):
                if not Info.objects.filter(info_id = i):
                    Info.objects.create(
                        info_id = i,
                        sn = data['sn'],
                        func_uid = func_uid,
                        version = data['version'],
                        issued = data['issued'],
                        expiration = data['expiration'],
                        count = data['count'],
                        registration = data['registration'],
                        type = type,
                        comment = data['comment'],
                        contact = data['contact'],
                        info = data['info'],
                    )
                    break
    Updatetime.objects.filter(id = 'last_update_time').update(update_time = generate_last_update_time())#改DB同時更新heroku上傳時間
def generate_last_update_time():
    '''生成heroku上傳時間'''
    i = datetime.now()
    i = i.astimezone(timezone(timedelta(hours=8)))#台灣時區GMT+8
    print(("%d/%02d/%02d %02d:%02d:%02d") % (i.year, i.month, i.day, i.hour, i.minute, i.second))
    return (("%d/%02d/%02d %02d:%02d:%02d") % (i.year, i.month, i.day, i.hour, i.minute, i.second))


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>後台<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#
#--------------------product----------------------#
@csrf_exempt
@gzip_page
def admin_product(request):
    '''資料傳入product'''
    product_data = []
    for product in Products.objects.all():
        product_data.append({'product_id':product.product_id,'category_id':product.category_id,
        'product_name':product.product_name,'caption':product.caption,'remarks':product.remarks})
    option_data = []
    for option in Options.objects.all():
        option_data.append({'option_id':option.option_id,'product_name':option.product_name,'option_name':option.option_name,'caption':option.caption,
        'remarks':option.remarks})
    info_data = []
    for info in Info.objects.all():
        info_data.append({'info_id':info.info_id,'sn':info.sn,'func_uid':info.func_uid,'version':info.version,'issued':info.issued,'expiration':info.expiration,
                        'count':info.count,'registration':info.registration,'type':info.type,'comment':info.comment,'contact':info.contact,'info':info.info})
    if request.method == 'GET':
       return HttpResponse(json.dumps({
        'option_data':option_data,
        'product_data':product_data,
        'info_data':info_data
        }))
    return HttpResponse('資料傳入後台product_group頁面')
@csrf_exempt
def operator_product(request):
    '''操作product table'''
    if request.method == 'GET':
        operator = request.GET['operator']
        if operator == 'delete':
            product = json.loads(request.GET['data'])
            Products.objects.filter(product_id = product['product_id']).delete()
            return HttpResponse('成功刪除產品')
        elif operator == 'add':
            product = json.loads(request.GET['data'])
            for i in range(1,len(Products.objects.all())+2):
                if not Products.objects.filter(product_id = i):
                    Products.objects.create(
                        product_id = i,
                        category_id = product['category_id'],
                        product_name = product['product_name'],
                        caption = product['caption'],
                        remarks = product['remarks']
                    )
                    break
            return HttpResponse('成功新增產品')
        elif operator == 'edit':
            product = json.loads(request.GET['data'])
            origin_product_name = Products.objects.get(product_id = product['product_id']).product_name
            if origin_product_name == product['product_name']:
                Products.objects.filter(product_id = product['product_id']).update(
                    category_id = product['category_id'],
                    caption = product['caption'],
                    remarks = product['remarks']
                )
            else:
                Products.objects.filter(product_id = product['product_id']).update(
                    category_id = product['category_id'],
                    product_name = product['product_name'],
                    caption = product['caption'],
                    remarks = product['remarks']
                )
                Info.objects.filter(func_uid = origin_product_name).update(func_uid = product['product_name'])
                Options.objects.filter(product_name = origin_product_name).update(product_name = product['product_name'])
            return HttpResponse('成功修改產品')


#---------------------option----------------------#
@csrf_exempt
@gzip_page
def admin_option(request):
    '''資料傳入option'''
    product_data = []
    for product in Products.objects.all():
        product_data.append({'product_id':product.product_id,'category_id':product.category_id,
        'product_name':product.product_name,'caption':product.caption,'remarks':product.remarks})
    option_data = []
    for option in Options.objects.all():#新增category_id
        option_data.append({'category_id':Products.objects.get(product_name = option.product_name).category_id,'option_id':option.option_id,'product_name':option.product_name,'option_name':option.option_name,'caption':option.caption,
        'remarks':option.remarks})
    info_data = []
    for info in Info.objects.all():
        info_data.append({'info_id':info.info_id,'sn':info.sn,'func_uid':info.func_uid,'version':info.version,'issued':info.issued,'expiration':info.expiration,
                        'count':info.count,'registration':info.registration,'type':info.type,'comment':info.comment,'contact':info.contact,'info':info.info})
    if request.method == 'GET':
       return HttpResponse(json.dumps({
        'option_data':option_data,
        'product_data':product_data,
        'info_data':info_data
        }))
    return HttpResponse('資料傳入後台product_group頁面')
@csrf_exempt
def operator_option(request):
    '''操作option table'''
    if request.method == 'GET':
        operator = request.GET['operator']
        if operator == 'delete':
            option = json.loads(request.GET['data'])
            Options.objects.filter(option_id = option['option_id']).delete()
            return HttpResponse('成功刪除選項')
        elif operator == 'add':
            option = json.loads(request.GET['data'])
            if not Options.objects.filter(product_name = option['product_name']):
                for i in range(1,len(Options.objects.all())+2):
                    if not Options.objects.filter(option_id = i):
                        Options.objects.create(
                            option_id = i,
                            product_name = option['product_name'],
                            option_name = option['product_name'],
                            caption = Products.objects.get(product_name = option['product_name']).caption,
                            remarks = Products.objects.get(product_name = option['product_name']).remarks,
                        )
                        break
            for i in range(1,len(Options.objects.all())+2):
                if not Options.objects.filter(option_id = i):
                    Options.objects.create(
                        option_id = i,
                        product_name = option['product_name'],
                        option_name = option['option_name'],
                        caption = option['caption'],
                        remarks = option['remarks']
                    )
            return HttpResponse('成功新增選項')
        elif operator == 'edit':
            option = json.loads(request.GET['data'])
            origin_option_name = Options.objects.get(option_id = option['option_id']).option_name
            origin_product_name = Options.objects.get(option_id = option['option_id']).product_name
            if option['product_name'] != origin_product_name:
                if not Options.objects.filter(product_name = option['product_name']):
                    for i in range(1,len(Options.objects.all())+2):
                        if not Options.objects.filter(option_id = i):
                            Options.objects.create(
                                option_id = i,
                                product_name = option['product_name'],
                                option_name = option['product_name'],
                                caption = Products.objects.get(product_name = option['product_name']).caption,
                                remarks = Products.objects.get(product_name = option['product_name']).remarks,
                            )
                            break
            if origin_option_name == option['option_name']:
                Options.objects.filter(option_id = option['option_id']).update(
                    product_name = option['product_name'],
                    caption = option['caption'],
                    remarks = option['remarks']
                )
            else:
                Options.objects.filter(option_id = option['option_id']).update(
                    product_name = option['product_name'],
                    option_name = option['option_name'],
                    caption = option['caption'],
                    remarks = option['remarks']
                )
                Info.objects.filter(func_uid = origin_option_name).update(func_uid = option['option_name'])
            return HttpResponse('成功修改選項')

#----------------------user-----------------------#
@csrf_exempt
def admin_user(request):
    '''將資料傳入後台user頁面'''
    user_data = []
    for user in Users.objects.all():
        user_data.append({'user_id':user.user_id,'user':user.user,'password':user.password,'email':user.email,'groups':user.groups,'region':user.region,'record':user.record,'description':user.description})
    group_data = []
    for group in Groups.objects.all():
        group_data.append({'group_id':group.group_id,'name':group.name,'caption':group.caption,'authority':group.authority,'description':group.description,'members':group.members})
    region_data = []
    for region in Region.objects.all():
        region_data.append({'region_id':region.region_id,'name':region.name,'description':region.description})
    product_data = []
    for product in Products.objects.all():
        product_data.append({'product_id':product.product_id,'category_id':product.category_id,
        'product_name':product.product_name,'caption':product.caption,'remarks':product.remarks})
        
    if request.method == 'GET':
       return HttpResponse(json.dumps({
        'user_data':user_data,
        'group_data':group_data,
        'region_data':region_data,
        'product_data':product_data,
        }))
    return HttpResponse('資料傳入後台user頁面')
@csrf_exempt
def operator_user(request):
    '''修改資料庫group資料'''
    if request.method == 'GET':
        operator = request.GET['operator']
        if operator == 'delete':
            user_name = json.loads(request.GET['user_name'])
            user_id = Users.objects.get(user = user_name).user_id
            if Users.objects.get(user = user_name).groups != '':#若該刪除資料群組不為空 則將group中的member一一刪除
                groups = json.loads(Users.objects.get(user = user_name).groups)
                for gro in groups:
                    copy = json.loads(Groups.objects.get(group_id = gro).members)
                    copy.remove(user_id)
                    Groups.objects.filter(group_id = gro).update(members = json.dumps(copy))
            Users.objects.filter(user = user_name).delete()
            return HttpResponse('成功刪除使用者')
        elif operator == 'add':
            form = json.loads(request.GET['form'])
            for i in range(1,len(Users.objects.all())+2):
                if not Users.objects.filter(user_id = i):
                    Users.objects.create(
                        user_id = i,
                        user = form['user'],
                        password = form['password'],
                        email = form['email'],
                        groups = form['groups'],
                        region = form['region'],
                        #record = form['record'],
                        record = '',
                        description = form['description'],
                        setting = '{"pagesize":10,"mode":"product"}'
                    )
                    break
            user_id = Users.objects.get(user = form['user']).user_id
            if form['groups'] != '':#若該新增群組不為空 則將groups內members一一添加
                groups = json.loads(form['groups'])
                for gro in groups:
                    if Groups.objects.get(group_id = gro).members == '':
                        copy = []
                    else:
                        copy = json.loads(Groups.objects.get(group_id = gro).members)
                    copy.append(user_id)
                    Groups.objects.filter(group_id = gro).update(members = json.dumps(copy))
            return HttpResponse('成功新增使用者')
        elif operator == 'edit':
            form = json.loads(request.GET['form'])
            Users.objects.filter(user_id = form['id']).update(
                user = form['user'],
                password = form['password'],
                email = form['email'],
                groups = form['groups'],
                region = form['region'],
                #record = form['record'],
                description = form['description'],
            )
            user_id = form['id']
            if form['groups'] != '':#若該修改後資料群組不為空 
                for group in Groups.objects.all():#先將所有 有該筆members資料的groups全部清空
                    copy = group.members
                    if copy != '':
                        copy = json.loads(copy)
                        if user_id in copy:
                            copy.remove(user_id)
                            Groups.objects.filter(group_id = group.group_id).update(members = json.dumps(copy))

                groups = json.loads(form['groups'])
                for gro in groups:#再將該user內所有groups添加到groups的members內
                    if Groups.objects.get(group_id = gro).members == '':
                        copy = []
                    else:
                        copy = json.loads(Groups.objects.get(group_id = gro).members)
                    if user_id not in copy:
                        copy.append(user_id)
                    Groups.objects.filter(group_id = gro).update(members = json.dumps(copy))
            if form['groups'] == '':#若user群組資料為空則將所有groups中在member內的成員清空
                for group in Groups.objects.all():
                    copy = group.members
                    if copy != '':
                        copy = json.loads(copy)
                        if user_id in copy:
                            copy.remove(user_id)
                            Groups.objects.filter(group_id = group.group_id).update(members = json.dumps(copy))
            return HttpResponse('成功修改使用者')


#----------------------region----------------------#
@csrf_exempt
def admin_region(request):
    '''資料傳入region'''
    sn_data = []
    for sn in Sn.objects.all():
        sn_data.append({'sn_id':sn.sn_id,'sn':sn.sn,'region':sn.region,'user':sn.user,
        'record':sn.record,'note1':sn.note1,'note2':sn.note2,'note3':sn.note3,'note4':sn.note1,'note5':sn.note1}) 

    customer_data = []
    for customer in Customers.objects.all():
        customer_data.append({'customer_id':customer.customer_id,'name':customer.name,'site':customer.site})

    region_data = []
    for region in Region.objects.all():
        region_data.append({'region_id':region.region_id,'name':region.name,'description':region.description})
        
    if request.method == 'GET':
       return HttpResponse(json.dumps({
        'sn_data':sn_data,
        'customer_data':customer_data,
        'region_data':region_data,
        }))
    return HttpResponse('資料傳入後台region頁面')
@csrf_exempt
def operator_region(request):
    '''修改資料庫region資料(後台)'''
    if request.method == 'GET':
        operator = request.GET['operator']
        if operator == 'delete':
            id = json.loads(request.GET['id'])
            Region.objects.filter(region_id = id).delete()
            return HttpResponse('成功刪除業務地區')
        elif operator == 'add':
            region_dialog = json.loads(request.GET['region_dialog'])
            for i in range(1,len(Region.objects.all())+2):
                if not Region.objects.filter(region_id = i):
                    Region.objects.create(
                        region_id = i,
                        name = region_dialog['name'],
                        description = region_dialog['description']
                    )   
                    break
            return HttpResponse('成功新增區域')
        elif operator == 'edit':
            region_dialog = json.loads(request.GET['region_dialog'])
            Region.objects.filter(region_id = region_dialog['id']).update(
                region_id = region_dialog['id'],
                name = region_dialog['name'],
                description = region_dialog['description'],
            )
            return HttpResponse('成功修改區域')


#-------------------product_group------------------#
@csrf_exempt
def admin_product_group(request):
    '''將資料傳入admin_profuct_group'''
    user_data = []
    for user in Users.objects.all():
        user_data.append({'user_id':user.user_id,'user':user.user,'password':user.password,'email':user.email,'groups':user.groups,'region':user.region,'record':user.record,'description':user.description})
    product_group_data = []
    for pro_gro in Product_groups.objects.all():
        product_group_data.append({'group_id':pro_gro.group_id,'caption':pro_gro.caption,'tag':pro_gro.tag,'product_list':pro_gro.product_list,
        'description':pro_gro.description,'remarks':pro_gro.remarks})
    product_data = []
    for product in Products.objects.all():
        product_data.append({'product_id':product.product_id,'category_id':product.category_id,
        'product_name':product.product_name,'caption':product.caption,'remarks':product.remarks})
    option_data = []
    for option in Options.objects.all():
        option_data.append({'option_id':option.option_id,'product_name':option.product_name,'option_name':option.option_name,'caption':option.caption,
        'remarks':option.remarks})

    if request.method == 'GET':
       return HttpResponse(json.dumps({
        'user_data':user_data,
        'option_data':option_data,
        'product_data':product_data,
        'product_group_data':product_group_data
        }))
    return HttpResponse('資料傳入後台product_group頁面')
@csrf_exempt
def operator_product_group(request):
    '''修改資料庫group資料'''
    if request.method == 'GET':
        operator = request.GET['operator']
        if operator == 'delete':
            group_name = json.loads(request.GET['group_name'])
            Product_groups.objects.filter(caption = group_name).delete()
            return HttpResponse('成功刪除產品群組')
        elif operator == 'add':
            product_dialog = json.loads(request.GET['product_dialog'])
            for i in range(1,len(Product_groups.objects.all())+2):
                if not Product_groups.objects.filter(group_id = i):
                    Product_groups.objects.create(
                        group_id = i,
                        caption = product_dialog['caption'],
                        tag = json.dumps(product_dialog['tag']),
                        product_list = json.dumps(product_dialog['product_list']),
                        description = product_dialog['description'],
                        remarks = product_dialog['remarks']
                    )   
                    break
            return HttpResponse('成功新增群組')
        elif operator == 'edit':
            product_dialog = json.loads(request.GET['product_dialog'])
            Product_groups.objects.filter(group_id = product_dialog['id']).update(
                group_id = product_dialog['id'],
                caption = product_dialog['caption'],
                tag = json.dumps(product_dialog['tag']),
                product_list = json.dumps(product_dialog['product_list']),
                description = product_dialog['description'],
                remarks = product_dialog['remarks']
            )
            return HttpResponse('成功修改產品群組')


#---------------------password----------------------#
@csrf_exempt
def edit_password(request):
    '''修改資料庫user password資料'''
    if request.method == 'GET':
        user = json.loads(request.GET['user'])
        Users.objects.filter(user = user[0]).update(password = user[1])
        return HttpResponse('成功更改密碼')


#----------------------group------------------------#
@csrf_exempt
def operator_group(request):
    '''修改資料庫group資料'''
    if request.method == 'GET':
        operator = request.GET['operator']
        if operator == 'delete':
            group_name = json.loads(request.GET['group_name'])
            Group_id = Groups.objects.get(name = group_name).group_id
            if Groups.objects.get(name = group_name).members != '':#若該刪除資料成員不為空 則將user中的groups一一刪除
                member = json.loads(Groups.objects.get(name = group_name).members)
                for mem in member:
                    copy = json.loads(Users.objects.get(user_id = mem).groups)
                    copy.remove(Group_id)
                    Users.objects.filter(user_id = mem).update(groups = json.dumps(copy))
            Groups.objects.filter(name = group_name).delete()
            return HttpResponse('成功刪除群組')
        elif operator == 'add':
            form = json.loads(request.GET['form'])
            for i in range(1,len(Groups.objects.all())+2):
                if not Groups.objects.filter(group_id = i):
                    Groups.objects.create(
                        group_id = i,
                        name = form['name'],
                        caption = form['caption'],
                        authority = form['authority'],
                        description = form['description'],
                        members = form['members'],
                    )
                    break
            Group_id = Groups.objects.get(name = form['name']).group_id
            if form['members'] != '':#若該新增成員不為空 則將user內group一一添加
                member = json.loads(form['members'])
                for mem in member:
                    if Users.objects.get(user_id = mem).groups == '':
                        copy = []
                    else:
                        copy = json.loads(Users.objects.get(user_id = mem).groups)
                    copy.append(Group_id)
                    Users.objects.filter(user_id = mem).update(groups = json.dumps(copy))
            return HttpResponse('成功新增群組')
        elif operator == 'edit':
            form = json.loads(request.GET['form'])
            Groups.objects.filter(group_id = form['id']).update(
                name = form['name'],
                caption = form['caption'],
                authority = form['authority'],
                description = form['description'],
                members = form['members'],
            )
            Group_id = form['id']
            if form['members'] != '':#若該修改後資料成員不為空 
                for user in Users.objects.all():#先將所有 有該筆群組資料的user全部清空
                    copy = user.groups
                    if copy != '':
                        copy = json.loads(copy)
                        if Group_id in copy:
                            copy.remove(Group_id)
                            Users.objects.filter(user_id = user.user_id).update(groups = json.dumps(copy))

                member = json.loads(form['members'])
                for mem in member:#再將該群組內所有成員添加到user的群組內
                    if Users.objects.get(user_id = mem).groups == '':
                        copy = []
                    else:
                        copy = json.loads(Users.objects.get(user_id = mem).groups)
                    if Group_id not in copy:
                        copy.append(Group_id)
                    Users.objects.filter(user_id = mem).update(groups = json.dumps(copy))
            else:#若群組成員資料為空則將所有user中在群組內的成員清空
                for user in Users.objects.all():
                    copy = user.groups
                    if copy != '':
                        copy = json.loads(copy)
                        if Group_id in copy:
                            copy.remove(Group_id)
                            Users.objects.filter(user_id = user.user_id).update(groups = json.dumps(copy))
            return HttpResponse('成功修改群組')


#----------------------main.js------------------------#                
@csrf_exempt
def auto_login(request):
    '''為了讓審核者自動登入(傳入user名稱 回傳username password email)'''
    if request.method == 'GET':
        username = request.GET['user']
        user = [Users.objects.get(user = username).user,Users.objects.get(user = username).password,Users.objects.get(user = username).email,'']
        return HttpResponse(json.dumps(user))

