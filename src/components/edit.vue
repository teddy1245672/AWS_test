<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
#note{
    display:inline;
}
.noedit-input /deep/ .el-input__inner{
  background-color:#FF9797; 
}
.input_require input.el-input__inner {
    border:#FF7575 1px solid;
}
</style>
<template>
    <div>
        <div style="position:relative;bottom:20px;font-size:28px;">資料修改</div>
        <div :data="sub_row">
            <div align="left" id = 'left100px'>
                客戶(必填):<el-input :class="deter_require == 'customer'?'input_require':''" style="position:relative;left:32px;width:110px;"  size='small' v-model="input.name" disabled placeholder="請輸入客戶"></el-input>
                <span style="position:relative;left:50px;">廠區(選填):</span>
                <el-input style="position:relative;left:50px;width:100px" size='small' v-model="input.factory" disabled placeholder="請輸入廠區"></el-input>
                <span style="position:relative;left:500px;font-size:16px;bottom:5px;">● 測試 - 借用給客戶(3個月)</span>
                <span style="position:relative;left:328px;top:21px;">○ 申請新的 key 須填寫領用單，行政查詢用</span>
                <span style="position:relative;left:25px;top:42px;">○ 此狀態須由申請人自行申請延期</span>
            </div>
            <div align="left" id = 'left100px'>
                KeyID(必填):<el-input  :class="deter_require == 'sn'?'input_require':''" v-model="sub_row.sn" style="position:relative;left:20px;width:110px;" size='small' placeholder="請輸入KeyID" disabled></el-input>
                <span style="position:relative;left:40px;">類型(必填):</span>
                <el-select :class="deter_require == 'type'?'input_require':''" size="small" v-model="sub_row.type" style="position:relative;left:40px;width:100px" @change="type_change" placeholder="類型">
                    <el-option
                        v-for="item in type_opt" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                </el-select>
                <!--<el-autocomplete style="position:relative;left:40px;width:100px"  size='small' v-model="sub_row.type" 
                        :fetch-suggestions="querySearch_type" placeholder="請輸入類型"></el-autocomplete>-->
            </div>
            <div align="left" id = 'left100px'>業務地區(必填):
            <!--<el-autocomplete :class="deter_require == 'region'?'input_require':''" style="width:110px"  size='small' v-model="sub_row.region":fetch-suggestions="querySearch_region" placeholder="請輸入業務地區"></el-autocomplete>-->
            <el-select :class="deter_require == 'region'?'input_require':''" style="position:relative;right:5px;width:110px"  size='small' v-model="sub_row.region" placeholder="業務地區">
                <el-option
                    v-for="item in region_opt" :key="item.value" :label="item.label" :value="item.value">
                </el-option>
            </el-select>
            </div>
            <div align="left" id = 'left100px'>
            產品類別(必填):<el-input  :class="deter_require == 'caption'?'input_require':''" style="width: 150px"  size='small' v-model="sub_row.caption" 
                        placeholder="請輸入產品類別" disabled></el-input>
                        <!--<el-autocomplete ref="pro_caption" style="width: 150px"  size='small' v-model="sub_row.caption" 
                        :fetch-suggestions="querySearch_caption" placeholder="請輸入產品類別" readonly></el-autocomplete>-->
            <span style="position:relative;left:10px;">
            產品名稱(必填):</span><el-input  :class="deter_require == 'func_uid'?'input_require':''" style="width:250px;position:relative;left:10px"  size='small' v-model="sub_row.func_uid" 
                       placeholder="請輸入產品名稱" disabled></el-input>
                        <!--<el-autocomplete ref="pro_name" style="width:180px;position:relative;left:10px"  size='small' v-model="sub_row.func_uid" 
                        :fetch-suggestions="querySearch_func_uid(sub_row)"placeholder="請輸入產品名稱" readonly></el-autocomplete>-->
                <span style="position:relative;left:241px;bottom:23px;">● 出貨 - 尚未完全付完款項(6個月)</span>
                <span style="position:relative;left:22px;top:2px;">○ 須提供訂單編號(詢問業務)供行政查詢</span>
                <span style="position:relative;right:259px;top:26px;bottom:1px;">○ 此狀態須由申請人自行申請延期</span>
            </div>
            <div align="left" id = 'left100px'>數量(必填):<el-input :class="deter_require == 'count'?'input_require':''" v-model="sub_row.count" style="width:100px;position:relative;left:32px;" size = "small" placeholder="請輸入數量"></el-input></div>
            <div align="left" id = 'left100px'>
            到期日(必填):<el-date-picker :class="deter_require == 'expiration'?'input_require':''" type="date" value-format="yyyy-MM-dd" name="expiration" v-model="sub_row.expiration" style="width:200px;position:relative;left:16px;" placeholder="請輸入到期日"></el-date-picker>
            <span style="position:relative;left:32px;">允許版本(選填):</span>
            <el-input v-model="sub_row.version" style="width:200px;position:relative;left:32px;" size = "small" placeholder="請輸入允許版本"></el-input>
                <span style="position:relative;bottom:5px;left:262px;">● 正式 - 付完全部款項(隔年1月31日)</span>
                <span style="position:relative;left:23px;top:20px">○ 須提供訂單編號供行政查詢，財務查詢付款狀況</span>
                <!--<span style="position:relative;right:328px;top:43px;">○ 此狀態會由系統自動延期一年並寄給各申請人</span>-->
            </div>
            <div align="left" id = 'left100px'>
            負責人(必填):
                <!--<el-input :class="deter_require == 'user'?'input_require':''" v-model="sub_row.user" style="width:200px;position:relative;left:16px;" size = "small" placeholder="請輸入負責人"readonly></el-input>-->
                <template  v-for="(item, index) in sub_row.user_display">
                    <el-autocomplete :class="deter_require == 'user'?'input_require':''" v-model="sub_row.user_display[index]" style="width:200px;position:relative;left:12px;" :fetch-suggestions="querySearch_user" placeholder="請輸入負責人" ></el-autocomplete>
                    <el-button v-show="!lock[row_index] || lock.length != 0 && index != 0" type="text" icon="el-icon-error" style="color:#F56C6C;font-size:15px;position:relative;bottom:15px;left:3px;" @click="remove_user(index)"></el-button>
                </template>
                <el-button v-show="!lock[row_index] || lock.length != 0" type="text" icon="el-icon-circle-plus" style="font-size:15px;" @click="add_user()"></el-button>
            </div>
            <div align="left" id = 'left100px' >
            聯絡人(必填):
                <template  v-for="(item, index) in sub_row.contact_display">
                    <el-autocomplete :class="deter_require == 'contact'?'input_require':''" v-model="sub_row.contact_display[index]" style="width:200px;position:relative;left:12px;" :fetch-suggestions="querySearch_contact" placeholder="請輸入聯絡人" ></el-autocomplete>
                    <el-button v-show="!lock[row_index] || lock.length != 0 && index != 0" type="text" icon="el-icon-error" style="color:#F56C6C;font-size:15px;position:relative;bottom:15px;left:3px;" @click="remove_contact(index)"></el-button>
                </template>
                <el-button v-show="!lock[row_index] || lock.length != 0" type="text" icon="el-icon-circle-plus" style="font-size:15px;" @click="add_contact()"></el-button>
            </div>
            <div align="left" id = 'left100px'>備註(選填):<el-input v-model="sub_row.comment" style="width:200px;position:relative;left:32px;" size = "small" placeholder="請輸入備註"></el-input>
                <span style="position:relative;bottom:40px;left:589px;">● 永久</span>
                <span style="position:relative;left:562px;bottom:13px;">○ 台灣區需提供客戶切結書</span>
                <span style="position:relative;left:372px;bottom:74px;">○ 此狀態會由系統自動延期一年並寄給各申請人</span>
            </div>
        </div>
        <div align = "center" style="position:relative;top:20px;">
            <el-button style="position:relative;left:550px;width:150px;display:inline;" @click="cancel" size = "medium" v-show="lock[row_index] || lock.length == 0">取消</el-button>
            <el-button style="position:relative;left:550px;width:150px;display:inline;" @click="submit" size = "medium" v-show="lock[row_index] || lock.length == 0">送出</el-button>
            <el-button style="position:relative;right:280px;bottom:45px;" circle type="primary" icon="el-icon-check" @click="store_row()" medium v-show="!lock[row_index] && lock.length != 0"></el-button>
            <el-button style="position:relative;right:280px;bottom:45px;" circle type="danger" icon="el-icon-close" @click="cancel_row()" medium v-show="!lock[row_index] && lock.length != 0"></el-button>
            <el-table
            :row-class-name="tableRowColor"
            @selection-change="handleSelectionChange"
            ref="edittable"
            :data="tableData"
            style="width: 100%">
            <el-table-column type="selection"align="center" prop="" label="編輯"  width="50"></el-table-column>
            <el-table-column align="center" prop="" label="操作"  width="100">
                <template slot-scope = "{$index,row}" >
                    <el-button circle type="primary" icon="el-icon-refresh-right" @click="restore($index,row)" size = "mini" v-show="lock[$index]"></el-button>
                    <el-button circle type="primary" icon="el-icon-edit" @click="edit_row($index,row)" size = "mini" v-show="lock[$index]"></el-button>
                    <!--<el-button circle type="primary" icon="el-icon-check" @click="store_row($index,row)" size = "mini" v-show="!lock[$index]"></el-button>
                    <el-button circle type="danger" icon="el-icon-close" @click="cancel_row($index,row)" size = "mini" v-show="!lock[$index]"></el-button>-->
                </template>
            </el-table-column>
            <el-table-column align="center" prop="customer" label="客戶" width="140">
                <template slot-scope = "{row}" >
                    <el-input type="text" name="customer" v-model="row.customer" readonly style="width: 110px"></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="sn" label="KeyID" width="120"> 
                <template slot-scope = "{row}" >
                    <el-input type="text" name="sn" v-model="row.sn" readonly style="width: 100px"></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="func_uid" label="產品名稱" width="190"> 
                <template slot-scope = "{row}" >
                    <el-input type="text" name="func_uid" v-model="row.func_uid" style="width: 160px" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="version" label="版本" width="100"> 
                <template slot-scope = "{row}" >
                    <el-input type="text" name="version" v-model="row.version" style="width: 80px" readonly ></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="count" label="數量" width="80"> 
                <template slot-scope = "{row}" >
                    <el-input type="text" name="count" v-model="row.count" style="width: 50px" readonly ></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="expiration" label="到期日" width="170"> 
                <template slot-scope = "{row}" >
                    <el-date-picker type="date" value-format="yyyy-MM-dd" name="expiration" v-model="row.expiration" style="width: 140px;" readonly ></el-date-picker>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="type" label="類型" width="100"> 
                <template slot-scope = "{row}" >
                    <el-input type="text" name="type" v-model="row.type" style="width: 80px" readonly ></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="user" label="負責人" width="80"> 
                <template slot-scope = "{row}" >
                    <el-input type="text" name="user" v-model="row.user" style="width: 60px" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="region" label="地區" width="100"> 
                <template slot-scope = "{row}" >
                    <el-input type="text" name="region" v-model="row.region" style="width: 70px" readonly ></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="comment" label="備註" width="160"> 
                <template slot-scope = "{row}" >
                    <el-input type="text" name="comment" v-model="row.comment" style="width: 130px" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="contact" label="聯絡人" width="100"> 
                <template slot-scope = "{row}" >
                    <el-input type="text" name="contact" v-model="row.contact" style="width: 80px" readonly></el-input>
                </template>
            </el-table-column>
            </el-table>
        </div>
    </div>
</template>

<script>
export default {
  name: 'edit',
  data: function() {
        return { 
            all_Data:{},//整個資料庫所有數據
            tableData:[],
            func_uid_Data:[],//整體資料(未修改前==origin_Data)
            origin_Data:[],//原始整體資料(不被修改)
            checked_Data:[],//被勾選的資料
            user_opt:[],
            region_opt:[],
            caption_opt:[],
            func_uid_opt:[],
            contact_opt:[],
            type_opt:[{label: '正式',value: '正式'},
                    {label: '測試',value: '測試'},
                    {label: '出貨',value: '出貨'},
                    {label: '永久',value: '永久'}],
            
            word:"頁面內文:                                   \n"+
                 "測試: 產品借用測試 (須由人員主動申請展延)     \n"+
                 "出貨: 款項讓未付完 (須由人員主動申請展延)     \n"+
                 "正式: 款項付完 (每年自動展延寄給 KeyID 負責人)\n"+
                 "永久: 部分產品需提供客戶切結書                ",
            input:{//左上方input框使用的(為了將客戶拆解)
                name:'',
                factory:''
            },
            sub_row:{
                caption: "",
                comment: "",
                contact: "",
                count: null,
                customer: "",
                expiration: "",
                func_uid: "",
                index: null,
                info: [],
                info_id: null,
                issued: "",
                operator: "",
                region: "",
                registration: "",
                sn: null,
                type: "",
                user: "",
                version: "",
                contact_display:[''],
                user_display:['']},
            lock:[],
            row_index:0,
            deter_require:'',
        }
  },
  created(){
      this.user = JSON.parse(this.$route.query.user);//把user傳進來
      this.all_Data = JSON.parse(this.$route.query.all_Data);
      for (let caption of this.all_Data['product_data']){
        this.caption_opt.push({value:caption['caption'],label:caption['caption']});
      }
      for (let region of this.all_Data['region_data']){
        this.region_opt.push({value:region['name'],label:region['name']});
      }
      for (let contact of this.all_Data['user_data']){
        this.contact_opt.push({value:contact['email'],label:contact['email']});
      }
      var user_set = new Set();
      for(let user of this.all_Data['sn_data'])
        for(let user_email of user['user'].split(','))
            user_set.add(user_email)
      for(let user of user_set)
        this.user_opt.push({value:user,label:user})

      var i = 0;
      for(let check of JSON.parse(this.$route.query.checked_Data)){
        check = Object.assign(check,{'operator':'修改','index':i});//增加index讓 row中有index
        this.func_uid_Data.push(check);
        i++;
      }
      for (let info of this.func_uid_Data){//如在 (users) 有資料, 就去掉信箱網域(@後面)
        info['contact_display'] = info['contact'].split(',');
      }
      for(let color of this.func_uid_Data){//新增color為判斷是否為更改資料
          color = Object.assign(color,{'color':0})
      }

      this.origin_Data = JSON.parse(JSON.stringify(this.func_uid_Data));
      this.tableData = JSON.parse(JSON.stringify(this.func_uid_Data));
      for(let i of this.tableData)
        this.lock.push(true);
  },
  watch:{
        tableData: function(){//當tableData資料變動時觸發自動勾選
            this.$nextTick(function(){ 
                for(var i = 0; i < this.tableData.length;i++){
                    if(this.tableData[i]['color'] == 1)//checked_Data 與 submit連動問題
                        this.$refs.edittable.toggleRowSelection(this.tableData[i],true);
                }
            }) 
        },
    },
  methods:{
      type_change(){//根據type自動調整期限
        let tempDate = new Date;
        if(this.sub_row.type == '正式'){//*當 B ==正式, 日期設定在隔年的 1/30
            tempDate.setMonth(tempDate.getMonth()+12);
            this.sub_row.expiration = tempDate.toISOString().slice(0, 4) + '-01-30'
        }
        if(this.sub_row.type == '測試'){//* 當 B ==測試, 日期往後設定 3 個月
            tempDate.setMonth(tempDate.getMonth()+3);
            this.sub_row.expiration = tempDate.toISOString().slice(0, 10)
        }
        if(this.sub_row.type == '出貨'){//* 當 B ==出貨, 日期往後設定 6 個月
            tempDate.setMonth(tempDate.getMonth()+6);
            this.sub_row.expiration = tempDate.toISOString().slice(0, 10)
        }
        if(this.sub_row.type == '永久')//* 當 B ==永久, 日期設定 9999年12月31日
            this.sub_row.expiration = '9999-12-31'
        },
      add_user(){//上方聯絡人修改框增加
          this.sub_row.user_display.push('');
        },
      remove_user(index){//上方聯絡人修改框減少
        this.sub_row.user_display.splice(index,1);
        },
      add_contact(){//上方聯絡人修改框增加
          this.sub_row.contact_display.push('');
        },
      remove_contact(index){//上方聯絡人修改框減少
        this.sub_row.contact_display.splice(index,1);
        },
      edit_row(index, row){//編輯row 將tabledata row帶入sub_row
        for(let i = 0; i < this.lock.length;i++)//防止使用者連續觸發兩列以上的編輯
            if(this.lock[i] == false && i != index)
                this.cancel_row();

        if(row.customer.indexOf('|') != -1){
            this.input.name = row.customer.split('|')[0]
            this.input.factory = row.customer.split('|')[1]
        }
        else{
            this.input.name = row.customer
            this.input.factory = ''
        }
        this.row_index = index;
        this.sub_row = JSON.parse(JSON.stringify(row));
        this.$set(this.lock,index,false)
        },
      cancel_row(){//取消編輯 初始化sub_row
        this.sub_row = {caption: "",comment: "",contact: "",count: null,customer: "",
            expiration: "",func_uid: "",index: null,info: [],info_id: null,issued: "",
            operator: "",region: "",registration: "",sn: null,type: "",user: "",version: "",contact_display:[''],user_display:['']}
        this.input.name = ''
        this.input.factory = ''
        this.$set(this.lock,this.row_index,true)
        },
      store_row(){
        for(let i = 0; i < this.sub_row['contact_display'].length; i++)//若聯絡人修改框中有框無值 則刪除此框
            if(this.sub_row['contact_display'][i] == ''){
                this.sub_row['contact_display'].splice(i,1);
                i--;
            }
        for(let i = 0; i < this.sub_row['user_display'].length; i++)//若聯絡人修改框中有框無值 則刪除此框
            if(this.sub_row['user_display'][i] == ''){
                this.sub_row['user_display'].splice(i,1);
                i--;
            }    
        if(this.test_edit_add()){
            if(this.tableData[this.row_index]['expiration'] != this.sub_row['expiration'] && this.tableData.length > 1){//更改到期日
                this.$confirm('修改全部資料時間', '選擇', {
                confirmButtonText: '同意',
                cancelButtonText: '不同意',
                type: 'warning'
                }).then(() => {//修改全部資料列時間
                    for(let table of this.tableData)
                        table = Object.assign(table,{'expiration':this.sub_row['expiration']})
                    this.tableData[this.row_index] = Object.assign({},this.sub_row);
                    this.tableData[this.row_index]['contact'] = this.sub_row['contact_display'].join();
                    this.tableData[this.row_index]['user'] = this.sub_row['user_display'].join();
                    this.sub_row = {caption: "",comment: "",contact: "",count: null,customer: "",
                        expiration: "",func_uid: "",index: null,info: [],info_id: null,issued: "",
                        operator: "",region: "",registration: "",sn: null,type: "",user: "",version: "",contact_display:[''],user_display:['']}
                    this.input.name = ''
                    this.input.factory = ''
                    this.datachange()
                    this.$set(this.lock,this.row_index,true)
                }).catch(() => {//不修改全部資料列時間
                    this.tableData[this.row_index] = Object.assign({},this.sub_row);
                    this.tableData[this.row_index]['contact'] = this.sub_row['contact_display'].join();
                    this.tableData[this.row_index]['user'] = this.sub_row['user_display'].join();
                    this.sub_row = {caption: "",comment: "",contact: "",count: null,customer: "",
                        expiration: "",func_uid: "",index: null,info: [],info_id: null,issued: "",
                        operator: "",region: "",registration: "",sn: null,type: "",user: "",version: "",contact_display:[''],user_display:['']}
                    this.input.name = ''
                    this.input.factory = ''
                    this.datachange()
                    this.$set(this.lock,this.row_index,true)
                });
            }else{//無更改到期日
                this.tableData[this.row_index] = Object.assign({},this.sub_row);
                this.tableData[this.row_index]['contact'] = this.sub_row['contact_display'].join();
                this.tableData[this.row_index]['user'] = this.sub_row['user_display'].join();
                this.sub_row = {caption: "",comment: "",contact: "",count: null,customer: "",
                    expiration: "",func_uid: "",index: null,info: [],info_id: null,issued: "",
                    operator: "",region: "",registration: "",sn: null,type: "",user: "",version: "",contact_display:[''],user_display:['']}
                this.input.name = ''
                this.input.factory = ''
                this.datachange()
                this.$set(this.lock,this.row_index,true)
            }
        }
        },
      test_edit_add(){//修改資料的防呆
        if(this.input.name == null || this.input.name == ""){
                this.$message({message: '客戶不可為空',type: 'warning'});
                this.deter_require = 'customer';
                return false;
            }
        if(this.sub_row['contact_display'].length == 0){
            this.$message({message: '聯絡人不可為空',type: 'warning'});
            this.deter_require = 'contact';
            return false;
        }
        if(this.sub_row['user_display'].length == 0){
            this.$message({message: '負責人不可為空',type: 'warning'});
            this.deter_require = 'user';
            return false;
        }
        if(this.sub_row['sn'] == null || this.sub_row['sn'] == ""){
            this.$message({message: 'KeyID不可為空',type: 'warning'});
            this.deter_require = 'sn';
            return false;
        }
        if(this.sub_row['caption'] == null || this.sub_row['caption'] == ""){
            this.$message({message: '產品類別不可為空',type: 'warning'});
            this.deter_require = 'caption';
            return false;
        }
        if(this.sub_row['func_uid'] == null || this.sub_row['func_uid'] == ""){
            this.$message({message: '產品名稱不可為空',type: 'warning'});
            this.deter_require = 'func_uid';
            return false;
        }
        if(this.sub_row['count'] == null || this.sub_row['count'] == ""){
            this.$message({message: '數量不可為空',type: 'warning'});
            this.deter_require = 'count';
            return false;
        }
        if(this.sub_row['expiration'] == null || this.sub_row['expiration'] == ""){
            this.$message({message: '到期日期不可為空',type: 'warning'});
            this.deter_require = 'expiration';
            return false;
        }
        if(this.sub_row['type'] == null || this.sub_row['type'] == ""){
            this.$message({message: '類型不可為空',type: 'warning'});
            this.deter_require = 'type';
            return false;
        }
        if(this.sub_row['region'] == null || this.sub_row['region'] == ""){
            this.$message({message: '地區不可為空',type: 'warning'});
            this.deter_require = 'region';
            return false;
        }
        let test = 0;//驗證新增客戶 sn是否也有修改
        for(let customer of this.all_Data['customer_data']){//若新增客戶則可以修改負責人
            if(this.input.name == customer['name'] && this.input.factory == customer['site'])
                test = 1;
        }
        if(test == 0){
            for(let sn of this.all_Data['sn_data']){//若新增客戶則可以修改負責人
                if(this.sub_row['sn'] == sn['sn'] ){
                    this.$message({message: '新增客戶時，也要新增一筆新keyID',type: 'warning'});
                    this.deter_require = 'sn';
                    return false;
                }
            }
        }
        return true;
        },
      //當select 有變化時執行 且val是所選row的所有資訊(type:array)//
      handleSelectionChange (val) {
        this.checked_Data = JSON.parse(JSON.stringify(val));
        },
      submit:function(){//送出到編輯介面
        //--------------------------判斷有無空資料，若有要求更改後重送--------------------------//
        this.axios.post("/save_to_handle",{
            checked_Data: this.checked_Data,
            content:'none',
            user:this.user
        }).then((response)=>{
            let res = response.data;
            this.$router.push({name: 'Show_All'});
        });
        },
      cancel:function(){
          this.$router.push({name: 'Show_All'});
        },
      restore:function(index,row){//回復成原本的資料列
        this.$set(this.tableData,index,this.origin_Data[index]);
        },
      datachange:function(){//跟原資料比較 若不一致 則color=1
        var copy_table = JSON.parse(JSON.stringify(this.tableData))
        for(let copy of copy_table)//因color之前修改成1所以在這邊要先用一個替代的talbe將color改成0再去比較
            copy = Object.assign(copy,{'color':0})
        for(var i = 0; i < this.origin_Data.length; i++){
            if(JSON.stringify(this.origin_Data[i]) != JSON.stringify(copy_table[i]))
                this.tableData[i]['color'] = 1;
            else
                this.tableData[i]['color'] = 0;
          }
        this.tableData = Object.assign([], this.tableData);//為了更新觸發watch
        },
      //------------------------列變色判斷------------------------------//
      tableRowColor({row, rowIndex}) {//被修改的資料->紅色
        if(this.tableData[rowIndex]['color'] == 1)
            return 'exceed-row';
        },
      //-------------------以下是el-input建議所需的function-------------------//
      querySearch_contact(queryString, cb){
        var results = queryString ? this.contact_opt.filter(this.createFilter(queryString)) : this.contact_opt;
        if(results.length == 0){
            results.push({value:queryString + '@eastek.com.cn',label:queryString + '@eastek.com.cn'});
            results.push({value:queryString + '@eastek.com.tw',label:queryString + '@eastek.com.tw'});
        }
        cb(results);// 調用 callback 返回建議列表的數據
        },
      querySearch_user(queryString, cb){
        var results = queryString ? this.user_opt.filter(this.createFilter(queryString)) : this.user_opt;
        if(results.length == 0){
            results.push({value:queryString + '@eastek.com.cn',label:queryString + '@eastek.com.cn'});
            results.push({value:queryString + '@eastek.com.tw',label:queryString + '@eastek.com.tw'});
        }
        cb(results);// 調用 callback 返回建議列表的數據
        },
      /*querySearch_func_uid(row,queryString,cb) {
          return (queryString, cb) => {
              this.func_uid_opt.length=0;//清空array
              if(row.caption != ''){
                for (let caption of this.all_Data['product_data']){//根據Caption去返回func_uid建議
                    if(caption['caption'] == row.caption)
                        for(let mod of this.all_Data['module_data'])
                            if(caption['product_id'] == mod['category'])
                                this.func_uid_opt.push({value:mod['caption'],label:mod['caption'],category:mod['category']})
                }
              }
              else
                for(let mod of this.all_Data['module_data'])
                    if(mod['category'] != 0)
                        this.func_uid_opt.push({value:mod['caption'],label:mod['caption'],category:mod['category']})
                
              var results = queryString ? this.func_uid_opt.filter(this.createFilter(queryString)) : this.func_uid_opt;
            cb(results)
        }
      },
      querySearch_caption(queryString, cb) {
        var results = queryString ? this.caption_opt.filter(this.createFilter(queryString)) : this.caption_opt;
        cb(results);// 調用 callback 返回建議列表的數據
      },
      querySearch_type(queryString, cb) {
        var results = queryString ? this.type_opt.filter(this.createFilter(queryString)) : this.type_opt;
        cb(results);// 調用 callback 返回建議列表的數據
      },
      querySearch_region(queryString, cb) {
        var results = queryString ? this.region_opt.filter(this.createFilter(queryString)) : this.region_opt;
        cb(results);// 調用 callback 返回建議列表的數據
        },*/
      createFilter(queryString) {//搜尋建議選項
        return (any) => {
          return (any.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
        };
        },
  }

}
</script>

