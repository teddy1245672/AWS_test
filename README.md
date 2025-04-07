#   **host環境建立(一)**
1.安裝 [Python 3.6.3rc1](https://www.python.org/downloads/release/python-363rc1/)

2.安裝 [node.js 12.16.1](https://nodejs.org/download/release/v12.16.1/)

3.安裝 Vue.js 2.5.17  ```npm install vue```

#   **host環境建置(二)**
1.將 bitbucket vue-test-simple內所有文件複製到D槽，在 `D:\`下執行以下指令:
    `git clone bitbucket_URL`
    
2.首先進入 `D:\vue-test-simple` 終端中利用package.json建立環境，在`D:\vue-test-simple`下執行指令:
    ```npm install```
    
3.建立好環境後，為了建立index.html檔案，在 `D:\vue-test-simple` 下執行指令:
	```npm run build```
	
4.操作以下指令:
	```將backend/api/views.py內所有程式碼設為註解```
    ```將backend/urls.py中 將此行設為註解->path('api/', include('backend.api.urls'))```
    
5.建立資料庫、且資料庫創制table，在`D:\vue-test-simple`下執行指令:
	```
	python db_create.py
	```
	
6.將上述「第4步驟」所註解掉的程式碼還原並儲存

7.將csv資料導入db中，在`D:\vue-test-simple`下執行指令:
	```python write_model_from_csv.py -w```

8.建立其他所需模組，Ex:python django,xlws.....
    ```pip install -r requirements.txt```
    
9.確認網頁跑的狀態，看是否有成功建置，在`D:\vue-test-simple`下執行指令:
	```python manage.py runserver```
	
# **架站流程(heroku)**
1.參考以下教學，[Heroku 部署網站](https://djangogirlstaipei.herokuapp.com/tutorials/deploy-to-heroku/?os=windows)，其中設定檔的部分皆以建置完畢
  * 請先根據教學安裝好heroku工具
  * 帳號 : eastek.intern@gmail.com/密碼 : Eastek.2019

2.先登入 heroku 網站 創建 app <`license_app`>

3.在`D:\`下執行以下指令(帳號 : eastek.intern@gmail.com/密碼 : Eastek.2019)
	```heroku login```
	
4.使用cmd登入heroku後，回到heroku網站點選Settings，找到Heroku git URL，在`D:\`下執行:
	```git clone Heroku_git_URL```
(Heroku_git_URL 為https://git.heroku.com/xxxxxxxxx.git)

5.將建置好的 vue-test-simple 內所有檔案複製到剛剛clone下來的 license_app 中

6.其中複製進來的檔案資料夾內，需確認 .gitignore 是否與下方一致:
**(上傳bitbucket 不需要上傳db.sqlite3 若是heroku則需要)**

    .DS_Store
    node_modules/

    /venv
    __pycache__/
    
    # local env files
    .env.local
    .env.*.local
    
    # Log files
    npm-debug.log*
    yarn-debug.log*
    yarn-error.log*
    
    # Editor directories and files
    .idea
    .vscode
    *.suo
    *.ntvs*
    *.njsproj
    *.sln
    *.sw*

7.為了將剛剛複製的檔案上傳到heroku，請在 `D:\license_app` 下執行
	```git init```
	```git add ```
	```git commit -m "XXX"```
	```heroku config:set DJANGO_SETTINGS_MODULE=backend.settings.prod```
	```git push```
	
8.heroku 會自動建置heroku資料庫，我們只需將CSV資料導入heroku db，請在 `D:\license_app` 下執行
	```heroku run python manage.py migrate```
	```heroku run python write_model_from_csv.py -w ```

9.打開上傳的heroku網站，請在 `D:\license_app` 下執行
    ```heroku open```
# ***如何改變本地端的 database table:***
1.先將原本在```D:\vue-test-simple```下的```db.sqlite3 刪除```，並創建新的 ```db.sqlite```至```D:\vue-test-simple```下

2.執行以下操作
    ```將backend/api/migrations/0001_initial.py 刪除```
	```將backend/api/views.py內所有程式碼設為註解 ```
	```將backend/urls.py中 將此行設為註解->path('api/', include('backend.api.urls'))```
	
3.將model格式刻入db中，在從heroku clone下來的檔案下執行以下指令:
	```python manage.py makemigrations```
	```python manage.py migrate```

4.再將「第2步驟」所註解掉的程式碼還原

5.將csv資料導入db，`D:\license_app` 同資料夾下執行以下指令:
	```python write_model_from_csv.py -w```
# ***改變local DB Table後，須確定...***
**因改變 DB Table，不論新增、修改、刪除都需檢查Table欄位是否與write_model_from_csv.py程式穩合，當前DB 是無資料只有Table架構的狀態，確定Table與Write_model_from_csv.py穩合後，執行```python write_model_from_csv.py```，將原本的csv資料洗入剛更新的 DB上，若有報錯，請根據bug資料作處理**

**通常錯誤原因:**

 1. Table:無法獲得Table，可能Table被刪掉或是改變Database Table就沒更新好

 2. 欄位:欄位不符，欄位被刪除，且```write_model_from_csv.py```尚未修改，導致py黨獲取不到資料，故報錯
 
 3. 數值:Csv中數值與```models.py```預設的欄位數值不符，需檢查```backend/api/models.py```

  
# ***如何根據DB改變 CSV***

**[本地端]** 在```D:\vue-test-simple```下運行```python write_csv_from_db.py -w```

**[Heroku]** ```heroku login```後運行```heroku run python write_csv_from_db.py -w```
# **更新 heroku 上的 database(請先更新本地端db):**
1.在 `D:\license_app` 下開啟cmd，並執行以下指令:
	```heroku login```
	
2.登入後執行以下指令:
	```git add .```
	```git commit -m "commit message"```
	```git push ```
	
3.在 heroku 網站上 ```reset heroku db ```

  * 以**eastek.intern**登入heroku官方網站->開啟**vue-test-simple**的App網站
  * 點擊**heroku Postgres**->跳轉分頁
  * 點擊**settings**->點選**Reset Database**->輸入**app名稱**
	
4.在終端機輸入以下指令
	```heroku run python3 manage.py makemigrations```
	```heroku run python3 manage.py migrate```
	
5.再將剛剛 push 至 heroku 的 csv 導入 heroku db 
	```heroku run python write_model_from_csv.py -w```	
# **Notice**
**以下參數可在varible.py修改**

    Sender_email_account   #寄件者帳號
    Sender_email_password  #寄件者密碼
    handle_applicant_title #申請確認信給申請人的主旨
    check_applicant_title  #審核確認信給申請人的主旨
    handle_verify_title    #申請審核通知信給審核人的主旨
    check_verify_title     #審核確認信給審核人的主旨
    
    verify_group = ['審核-產品','審核-財務'] #審核群組
    verify_user = ['teddy']                  #審核人
    verify_num = 1                           #審核人數
    verify_check = {'verify_group':[False,False], 'verify_user':[False], 'verify_num':0}
