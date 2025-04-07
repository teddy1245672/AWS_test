from django.urls import path
 
from . import views
 
urlpatterns = [
    path('show_all', views.show_all, name='show_all'),#主畫面資料索取
    #path('edit',views.edit,name='edit'),
    #path('add',views.add,name='add'),
    path('check/<str:verifyname>/',views.check,name='check'),#
    path('handle_send',views.handle_send,name='handle_send'),#送出申請頁面申請資料
    path('login',views.login,name='login'),#登入
    path('download_check',views.download_check,name='download_check'),#審查業面資料下載
    path('save_to_handle',views.save_to_handle,name='save_to_handle'),#將新增 修改 刪除資料存入Edit資料庫
    #path('delete',views.delete,name='delete'),
    path('download',views.download,name='download'),#申請頁面資料下載
    path('handle_delete',views.handle_delete,name='handle_delete'),#刪除申請頁面資料
    path('handle_edit',views.handle_edit,name='handle_edit'),#修改申請頁面資料
    path('check_verify',views.check_verify,name='check_verify'),#審核資料送出
    path('admin_user',views.admin_user,name='admin_user'),
    path('operator_group',views.operator_group,name='operator_group'),#處理新增修改刪除 群組權限
    path('operator_user',views.operator_user,name='operator_user'),#處理新增修改刪除 使用者權限
    path('edit_password',views.edit_password,name='edit_password'),#修改會員密碼
    path('auto_login', views.auto_login, name='auto_login'),#當審核人點選審核信時自動登入
    path('handle_back_ShowAll', views.handle_back_ShowAll, name='handle_back_ShowAll'),#申請頁面退回主畫面時 檢查edit是否有空資料或已上傳的檔案 若有則全部清除
    path('download_show', views.download_show, name='download_show'),#主畫面資料下載
    path('upload_on_local', views.upload_on_local, name='upload_on_local'),#將檔案上傳並在資料下載
    path('delete_upload_local', views.delete_upload_local, name='delete_upload_local'),#將以上傳之檔案清除(button)
    path('F5_handle', views.F5_handle, name='F5_handle'),#當檔案上傳後 若重新整理時 需要把以上傳的檔案全部清除
    path('save_to_product_group', views.save_to_product_group, name='save_to_product_group'),#新增產品群組
    path('get_product_groups_info_data', views.get_product_groups_info_data, name='get_product_groups_info_data'),#為了新增產品群組完直接拿到最新db資料
    path('admin_product_group', views.admin_product_group, name='admin_product_group'),#給予後台產品群組的資料
    path('operator_product_group', views.operator_product_group, name='operator_product_group'),#新增修改刪除product_group
    path('admin_region', views.admin_region, name='admin_region'),#給予後台區域資料
    path('operator_region', views.operator_region, name='operator_region'),#新增修改刪除後台region
    path('admin_product', views.admin_product, name='admin_product'),#給予後台產品的資料
    path('operator_product', views.operator_product, name='operator_product'),#新增修改刪除後台product
    path('admin_option', views.admin_option, name='admin_option'),#給予後台選項的資料
    path('operator_option', views.operator_option, name='operator_option'),#新增修改刪除後台option
    path('data_to_handle', views.data_to_handle, name='data_to_handle'),#給handle資料
    path('save_to_user_setting', views.save_to_user_setting, name='save_to_user_setting'),#儲存pagesize改動
    path('KeyID', views.KeyID, name='KeyID'),#獲得KeyID頁面所需資料
    path('dialog_check', views.dialog_check, name='dialog_check'),#check頁面當dialog確認時將資料改寫儲存至DB
]