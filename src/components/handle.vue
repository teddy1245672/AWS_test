<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
#note{
    display:inline;
}
.avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }
  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 50px;
    height: 50px;
    line-height: 50px;
    text-align: center;
  }
  .avatar {
    width: 50x;
    height: 50px;
    display: block;
  }
  .fade-enter,
  .fade-leave-active{
    opacity: 0;
  }
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.5s;
  }
</style>
<template>
  <div>
    <transition name="fade"><!--loading動畫-->
      <loading v-if="isLoading"></loading>
    </transition>
    <div>
      <div align = "left" style="position:relative;left:150px;"><span>* 申請人 :</span>
        <!--<el-input type="textarea" :autosize="{ minRows: 1, maxRows: 3}"name="sender" v-model="user[0]" required style="left:15px;width: 200px;"></el-input></div>-->
        <span style="position:relative;left:18px;">{{user[0]}}</span></div>
      <div align="left" style="position:relative;left:150px;top:20px;"><span>* 副本 :</span>
        <!--<el-input type="textarea" :autosize="{ minRows: 1, maxRows: 3}" name="sender" v-model="cc" required style="left:30px;width: 400px;"></el-input></div>-->
        <template  v-for="(item, index) in cc">
          <el-autocomplete v-model="cc[index]" style="position:relative;left:30px;":fetch-suggestions="querySearch_cc" placeholder="請輸入副本" ></el-autocomplete>
          <el-button type="text" icon="el-icon-error" style="color:#F56C6C;position:relative;bottom:18px;left:21px;"@click="remove_cc(index)"></el-button>
        </template>
        <el-button type="text" style="position:relative;left:10px;"icon="el-icon-circle-plus"  @click="add_cc()"></el-button>
      </div>
      <div align="left" style="position:relative;left:150px;top:40px;"><span>* 內文 :</span>
        <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 3}" name="sender" v-model="text" required style="left:30px;width: 400px;"></el-input></div>
      <div align="left" style="position:relative;left:150px;top:60px;"><span>* 附件 :</span>
        <el-button  type="text" @click="download">license-application.xlsx</el-button></div>
      <div style="position:absolute;right:350px;top:60px">
        <span>檔案上傳區</span> 
          <el-upload
          class="avatar-uploader"
          action="111"
          :http-request = "customUpload"
          :on-remove="handleRemove"
          :on-exceed="handleExceed"
          :on-change="handleChange"
          :before-upload="handleUpload"
          accept=".png,.jpg,.docx,.xlsx,.xls,.pdf"
          multiple
          :limit="5"
          :file-list="fileList">
          <i class="el-icon-plus avatar-uploader-icon"></i>
          <div slot="tip" class="el-upload__tip">檔案類型限定:jpg,png,docx,xlsx,pdf</div>
          </el-upload>
      </div>
      <div style="position:relative;top:50px;">
        <el-button round = "true"style="width:150px;height:50px;display:inline;" @click="cancel" size = "medium" >返回主畫面</el-button>
        <el-button round = "true"style="width:150px;height:50px;display:inline;" @click="submit" size = "medium" >送出申請</el-button>
      </div>
    </div>
    <div>
      <div style ="position:relative;top:80px" align = "center">
        <el-table
        :data="tableData"
        style="width: 95%">
        <el-table-column type=""align="center" prop="" label="編輯" width="130">
          <template slot-scope = "{row,$index}" >
          <el-row>
            <el-button type="primary" size="mini"@click.native="handleCheck($index, row)"  v-if="showEdit[$index]"icon="el-icon-check" circle></el-button>
            <el-button type="danger"  style="position:relative;right:5px;" size="mini"@click.native="handelRestore($index, row)"  v-if="showEdit[$index]"icon="el-icon-close" circle></el-button>
            <el-button type="primary" size="mini"@click.native="handleEdit($index, row)"  v-if="!showEdit[$index] && row.operator != '刪除'"icon="el-icon-edit" circle></el-button>
            <el-button type="danger"  style="position:relative;right:5px;" size="mini"@click="deleterow(row)" v-if="!showEdit[$index]" icon="el-icon-delete" circle></el-button>
            <el-popover ref="popover" width="950px" trigger="hover" placement="top">
              <el-table :cell-class-name="cell_color" :data="compare_Data" >
                <el-table-column width="100px" prop="customer" label="客戶"></el-table-column>
                <el-table-column width="70px" prop="sn" label="KeyID"></el-table-column>
                <el-table-column width="140px" prop="func_uid" label="產品名稱"></el-table-column>
                <el-table-column width="70px" prop="version" label="版本"></el-table-column>
                <el-table-column width="70px" prop="type" label="類型"></el-table-column>
                <el-table-column width="70px" prop="count" label="數量"></el-table-column>
                <el-table-column width="130px" prop="expiration" label="到期日期"></el-table-column>
                <el-table-column width="70px" prop="region" label="地區"></el-table-column>
                <el-table-column width="140px" prop="comment" label="備註"></el-table-column>
                <el-table-column width="150px" prop="contact" label="聯絡人"></el-table-column>
              </el-table>
            <el-button type="info " size="mini" slot="reference" @mouseenter.native="compare_row(row,$index)" v-show="row.operator=='修改'" icon="el-icon-view" circle></el-button>
            </el-popover>
          </el-row>
          </template>
        </el-table-column>
        <el-table-column align="center" prop="operator" label="操作" width="80">
        </el-table-column>
        <el-table-column align="center" prop="customer" label="客戶" width="140">
          <template slot-scope = "{row,$index}" >
              <!--<el-input v-if="showEdit[$index]" type="text" name="customer" readonly v-model="row.customer" style="width: 110px"></el-input>
              <span v-if="!showEdit[$index]">{{row.customer}}</span>-->
              <span>{{row.customer}}</span>
          </template>
        </el-table-column>
        <!--<el-table-column align="center" prop="issued" label="更新日期" width="170"> 
          <template slot-scope = "{row,$index}" >
            <el-date-picker v-if="showEdit[$index]" value-format="yyyy-MM-dd" type="date" name="issued" v-model="row.issued" style="width: 140px;"></el-date-picker>
            <span v-if="!showEdit[$index]">{{row.issued}}</span>
          </template>
        </el-table-column>-->
        <el-table-column align="center" prop="sn" label="KeyID" width="120"> 
          <template slot-scope = "{row,$index}" >
            <!--<el-input v-if="showEdit[$index]" type="text" name="sn" readonly v-model="row.sn" style="width: 90px"></el-input>
            <span v-if="!showEdit[$index]">{{row.sn}}</span>-->
            <span>{{row.sn}}</span>
          </template>
        </el-table-column>
        <el-table-column align="center" prop="func_uid" label="產品名稱" width="160"> 
          <template slot-scope = "{row,$index}" >
              <!--<el-input v-if="showEdit[$index]" type="text" name="func_uid" readonly v-model="row.func_uid" style="width: 130px"></el-input>
              <span v-if="!showEdit[$index]">{{row.func_uid}}</span>-->
              <span>{{row.func_uid}}</span>
          </template>
        </el-table-column>
        <el-table-column align="center" prop="version" label="版本" width="100"> 
          <template slot-scope = "{row,$index}" >
              <el-input v-if="showEdit[$index]" type="text" name="version" v-model="row.version" style="width: 70px"></el-input>
              <span v-if="!showEdit[$index]">{{row.version}}</span>
          </template>
        </el-table-column>
        <el-table-column align="center" prop="type" label="類型" width="90"> 
          <template slot-scope = "{row,$index}" >
              <el-input v-if="showEdit[$index]" type="text" name="type" v-model="row.type" style="width: 60px"></el-input>
              <span v-if="!showEdit[$index]">{{row.type}}</span>
          </template>
          </el-table-column>
        <el-table-column align="center" prop="count" label="數量" width="80"> 
          <template slot-scope = "{row,$index}" >
              <el-input v-if="showEdit[$index]" type="text" name="count" v-model="row.count" style="width: 50px"></el-input>
              <span v-if="!showEdit[$index]">{{row.count}}</span>
          </template>
          </el-table-column>
        <el-table-column align="center" prop="expiration" label="到期日期" width="170"> 
          <template slot-scope = "{row,$index}" >
              <el-date-picker v-if="showEdit[$index]" value-format="yyyy-MM-dd" type="date" name="expiration" v-model="row.expiration" style="width: 140px;"></el-date-picker>
              <span v-if="!showEdit[$index]">{{row.expiration}}</span>
          </template>
          </el-table-column>
        <el-table-column align="center" prop="region" label="地區" width="90"> 
          <template slot-scope = "{row,$index}" >
              <el-input v-if="showEdit[$index]" type="text" name="region" v-model="row.region" style="width: 60px"></el-input>
              <span v-if="!showEdit[$index]">{{row.region}}</span>
          </template>
          </el-table-column>
        <el-table-column align="center" prop="comment" label="備註" width="140"> 
          <template slot-scope = "{row,$index}" >
              <el-input v-if="showEdit[$index]" type="text" name="comment" v-model="row.comment" style="width: 110px"></el-input>
              <span v-if="!showEdit[$index]">{{row.comment}}</span>
          </template>
        </el-table-column>
        <el-table-column align="center" prop="contact" label="聯絡人" width="110"> 
          <template slot-scope = "{row,$index}" >
              <el-input v-if="showEdit[$index]" type="text" name="contact" v-model="row.contact" style="width: 80px"></el-input>
              <span v-if="!showEdit[$index]">{{row.contact}}</span>
          </template>
        </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script>
import Loading from '@/assets/loading'
export default {
  components:{ Loading },
  name: 'handle',
  data: function() {
        return { 
            user:[],
            tableData:[],
            origin_edit:[],
            all_Data:[],
            nofilter_info_Data:[],
            info_data:[],
            compare_Data:[],//修改的對照表(原本的)
            compare_edit_Data:[],//修改的對照表(修改過的)row
            showEdit:[],//false:不可編輯 true:可編輯
            cc:[],
            text:'',
            fileList:[],//顯示以上傳列表
            fileList_check:[],
            isLoading:true,
            cc_opt:[],
            unuser_map: new Map()
        }
  },
  created(){
    this.axios.get('/get_product_groups_info_data',{
      headers: {'Content-Encoding': 'gzip'}
      }).then(response => {
      this.user = JSON.parse(sessionStorage.getItem('user'))//存入user帳密
      this.info_data = JSON.parse(JSON.stringify(response.data))['info_data']
      this.all_Data = JSON.parse(this.$route.query.all_Data);
      
      var product_map = new Map()
      var option_map = new Map()
      var module_map = new Map()
      var sn_dict = JSON.parse(JSON.stringify(response.data))['sn_dict']
      for(let product of this.all_Data['product_data'])
        product_map.set(product['product_name'],{'category_id':product['category_id'],'caption':product['caption']})
      for(let option of this.all_Data['option_data'])
        option_map.set(option['option_name'],{'category_id':product_map.get(option['product_name'])['category_id'],'product_name':option['product_name'],'caption':option['caption']})
      
      this.all_Data['module_data'].forEach(item => module_map.set(item['mod_uid'],item['caption']))

      var cc_set = new Set();
      for(let user of this.all_Data['sn_data'])
        for(let user_email of user['user'].split(','))
            cc_set.add(user_email)
      cc_set.forEach(item => this.cc_opt.push({value:item,label:item}))

      var order_form = JSON.parse(JSON.stringify(this.info_data))
      var i = 0
      for (let info of this.info_data){
          if (sn_dict[info['sn']] != undefined){
              if(this.all_Data['customer_data'][sn_dict[info['sn']]['sn_id'] - 1]['site'] !='')
                order_form[i] = Object.assign(order_form[i],{'customer':this.all_Data['customer_data'][sn_dict[info['sn']]['sn_id'] - 1]['name'] + '|' + 
                this.all_Data['customer_data'][sn_dict[info['sn']]['sn_id'] - 1]['site'],'user':sn_dict[info['sn']]['user']
                ,'info':[sn_dict[info['sn']]['note1'],sn_dict[info['sn']]['note2'],sn_dict[info['sn']]['note3'],sn_dict[info['sn']]['note4'],sn_dict[info['sn']]['note5']]})
              else
                order_form[i] = Object.assign(order_form[i],{'customer':this.all_Data['customer_data'][sn_dict[info['sn']]['sn_id'] - 1]['name'] ,'user':sn_dict[info['sn']]['user']
                ,'info':[sn_dict[info['sn']]['note1'],sn_dict[info['sn']]['note2'],sn_dict[info['sn']]['note3'],sn_dict[info['sn']]['note4'],sn_dict[info['sn']]['note5']]})
              if(sn_dict[info['sn']]['region'] != '')
                order_form[i] = Object.assign(order_form[i],{'region':this.all_Data['region_data'][parseInt(sn_dict[info['sn']]['region'],10) - 1]['name']})
              else
                order_form[i] = Object.assign(order_form[i],{'region':''})
              }
          
          if(option_map.get(info['func_uid']) != undefined){
            order_form[i] = Object.assign(order_form[i],{'caption':option_map.get(info['func_uid'])['category_id']})
            order_form[i]['func_uid'] = (option_map.get(info['func_uid'])['caption']+'('+option_map.get(info['func_uid'])['product_name']+')');//edit介面需要
          }
          else if (product_map.get(info['func_uid']) != undefined){//db有錯
            order_form[i] = Object.assign(order_form[i],{'caption':product_map.get(info['func_uid'])['category_id']})
            order_form[i]['func_uid'] = product_map.get(info['func_uid'])['caption'];//edit介面需要
          }
          if(module_map.get(info['type']) != undefined)
            order_form[i]['type'] = module_map.get(info['type']);//edit介面需要
          
          i++
      }
      this.nofilter_info_Data = JSON.parse(JSON.stringify(order_form))
      var user_map = new Map()
      this.all_Data['user_data'].forEach(item => user_map.set(item['email'],item['user']))
      this.all_Data['user_data'].forEach(item => this.unuser_map.set(item['user'],item['email']))
      
      for(let edit of this.all_Data['edit_data'])
        if(edit['user'] == this.user[0])//只給使用者他申請的資料
          this.tableData = JSON.parse(edit['data'])
      
      for (let table of this.tableData){//如在 (users) 有資料, 就去掉信箱網域(@後面)
          if(user_map.get(table['contact']) != undefined)
            table['contact'] = user_map.get(table['contact']);
        }
      for (let info of this.tableData){//當聯絡人超過兩人時的tableData email簡化
        if(info['contact'].split(',').length > 1){
          info['contact'] = info['contact'].split(',')
          for(let i = 0; i < info['contact'].length; i++)
            if(user_map.get(info['contact'][i]) != undefined)
              info['contact'][i] = user_map.get(info['contact'][i])
          info['contact'] = info['contact'].join(',')
        }
      }
      var contact_set = new Set();
      for(let table of this.tableData)//使用set過濾多餘的contact 
        if(table['contact'].indexOf(',') != -1)
          for(let contact of table['contact'].split(','))
            contact_set.add(contact)
        else
          contact_set.add(table['contact'])
      
      for(let contact of contact_set)//將contact帶入副本
        if(this.unuser_map.has(contact))
            this.cc.push(this.unuser_map.get(contact))
        else
          this.cc.push(contact)

      for (let info of this.nofilter_info_Data){//如在 (users) 有資料, 就去掉信箱網域(@後面)
        for(let user of this.all_Data['user_data'])
          if (user_map.get(info['contact']) != undefined)
            info['contact'] = user_map.get(info['contact']); 
        }
      for (let info of this.nofilter_info_Data){//當聯絡人超過兩人時的nofilter email簡化
        if(info['contact'].split(',').length > 1){
          info['contact'] = info['contact'].split(',')
          for(let i = 0; i < info['contact'].length; i++)
            if(user_map.get(info['contact'][i]) != undefined)
              info['contact'][i] = user_map.get(info['contact'][i])
          info['contact'] = info['contact'].join(',')
        }
      }
      this.axios.get("/handle_edit",{//為了讓table與資料庫edit同步 因為簡化聯絡人email的資料未與資料庫同步
          params:{
              Newrow: JSON.stringify(this.tableData),
              user:JSON.stringify(this.user)
          }
          }).then((response)=>{let res = response.data;});
        this.origin_edit = JSON.parse(JSON.stringify(this.tableData))
      for(let i = 0; i < this.origin_edit.length; i++)
        this.showEdit.push(false);

      this.isLoading = false
      })
  },
  mounted() {//避免上傳檔案 並刷新頁面後 殘留檔案在heroku上
    let _this = this
    window.onbeforeunload = function (e) {
    if (_this.$route.name == "handle") {
      var upload_file_name = [];
      for(let file of _this.fileList)
        upload_file_name.push(file.name)//將上傳的檔案的名字傳入upload_file_name
      _this.axios.get("/F5_handle",{
      params:{
        upload_file_name:JSON.stringify(upload_file_name)
      }})
    } else {
      window.onbeforeunload = null
    }
  };
  },
  methods:{
    add_cc(){//上方聯絡人修改框增加
      this.cc.push('');
    },
    remove_cc(index){//上方聯絡人修改框減少
      this.cc.splice(index,1);
    },
    handleUpload(file){//阻止檔案容量>20MB時 依然顯示清單問題
      var size = 0  
      for(let file_before of this.fileList_check)
        size += file_before.size;   
      const size_check = size / 1024 / 1024 < 20
      if(!size_check){
        this.$message.error('上傳總容量不得高於20MB!');
        return size_check
      }
    },
    handleChange(file,fileList){//上傳檔案時 在本地端下載上傳檔案 (阻止跑去後台載檔案)
      this.fileList_check = fileList
      var size = 0  
      for(let file_before of fileList)
        size += file_before.size;   
      const size_check = size / 1024 / 1024 < 20
      if(size_check){
        this.fileList = fileList
        let fd = new FormData()
        fd.append('file', file.raw)
        fd.append('name',file.name)
        fd.append('type', file.raw.type)
        let config = {
          headers:{"Content-Type":"application/octet-stream;charset=utf-8"}
        };
        const instance = this.axios.create({
          withCredentials:true
        });
        this.axios.post('/upload_on_local',fd)//,config)
      }
    },
    customUpload(file){//此function拿來覆蓋action 使upalod不自動上傳
    },
    handleExceed(files, fileList) {
        this.$message.warning('限制上傳5個文件以下');
    },
    handleRemove(file, fileList) {//remove檔案時 移除本地端下載的檔案
      this.fileList = fileList
      this.axios.get("/delete_upload_local",{
        params:{
          name: file.name
        }})
      },
    tranfer_xlsx(data) {//web下載 xlsx
      if (!data) {
        return
      }
      let url = window.URL.createObjectURL(new Blob([data]))
      let link = document.createElement('a')
      link.style.display = 'none'
      link.href = url
      link.setAttribute('download', 'license-application.xlsx')
  
      document.body.appendChild(link)
      link.click()
    },
    download(){
      this.axios.get("/download",{//跑去後端下載資料庫內的資料(web下載)
        params:{
          user:JSON.stringify(this.user)
        },
        responseType: 'blob'
        }).then((response)=>{
          this.tranfer_xlsx(response.data)
          
        })
    },
    submit:function(){

      this.$confirm('是否送出申請?', '提示', {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          for(let i = 0;i < this.cc.length; i++)
            if(this.cc[i] == ''){
              this.cc.splice(i,1);
              i--;
            }

          if(this.cc.length != 0){//防止內文email格式出錯
            for(let index in this.cc)
              if(this.cc[index].indexOf('@') == -1){
                this.$message({message:'副本請填入正確email格式', type:'error'});
                return;
              }
          }

          var upload_file_name = [];
          for(let file of this.fileList)
            upload_file_name.push(file.name)//將上傳的檔案的名字傳入upload_file_name

          this.axios.post("/handle_send",{
              origin_data:this.nofilter_info_Data,
              edit_data: this.tableData,
              content: {'user':this.user[0],'cc':this.cc.join(','),'text':this.text,'reply':''},//申請人 副本 內文 審核人回覆(check頁面才會用到)
              upload_file_name:upload_file_name
            }).then((response)=>{
                if(response.data=='郵件傳送成功!'){
                  this.$message({ showClose: true, message: '郵件傳送成功!', type: 'success' });
                  this.$router.push({name: 'Show_All'});
                }
                else
                  this.$message({ showClose: true, message: '郵件傳送失敗!', type: 'error' });
            });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消送出申請'
          });    
        })      
    },
    handleEdit(index, row) {//開始修改
      this.$set(this.showEdit,index,true)
    },
    handleCheck(index,row){//確認修改資料
      this.axios.get("/handle_edit",{//跑去後端修改資料庫內的資料
        params:{
            Newrow: JSON.stringify(this.tableData),
            user:JSON.stringify(this.user)
        }
        }).then((response)=>{
            let res = response.data;
        });
      this.origin_edit[index] = JSON.parse(JSON.stringify(this.tableData[index]));
      this.$set(this.showEdit,index,false)
    },
    handelRestore(index, row) {//回復被修改資料(上一步)
      this.tableData[index] = JSON.parse(JSON.stringify(this.origin_edit[index]));
      this.$set(this.showEdit,index,false)
    },
    cancel:function(){
      var upload_file_name = [];
      for(let file of this.fileList)
        upload_file_name.push(file.name)//將上傳的檔案的名字傳入upload_file_name

      this.axios.get("/handle_back_ShowAll",{//跑去後端修改資料庫內的資料
        params:{
            user:JSON.stringify(this.user),
            upload_file_name:JSON.stringify(upload_file_name)
        }
        })
      this.$router.push({name: 'Show_All'});
    },
    deleterow:function(row){
      for(var i = 0; i < this.origin_edit.length; i++)//把all_Data的資料更新
        if(JSON.stringify(this.origin_edit[i]) == JSON.stringify(row)){
          this.origin_edit.splice(i,1);
          this.showEdit.splice(i,1);
        }

      this.tableData = JSON.parse(JSON.stringify(this.origin_edit));//更新tableData
      
      this.cc = []
      var contact_set = new Set();
      for(let table of this.tableData){//使用set過濾多餘的contact 
        if(table['contact'].indexOf(',') != -1)
          for(let contact of table['contact'].split(','))
            contact_set.add(contact)
        else
          contact_set.add(table['contact'])
      }
      
      for(let contact of contact_set){//將contact帶入副本
        if(this.unuser_map.has(contact))
            this.cc.push(this.unuser_map.get(contact))
        else
          this.cc.push(contact)
      }
      this.axios.get("/handle_delete",{//跑去後端刪除資料庫內的資料
        params:{
            Row: JSON.stringify(this.tableData),
            user:JSON.stringify(this.user)
        }
        }).then((response)=>{
            let res = response.data;
        });
    },
    cell_color({row, column, rowIndex, columnIndex}){//若原來資料與修改後資料不依 則顯示紅色
      if(column.label == '客戶')
        if(row.customer != this.compare_edit_Data[0].customer)
          return 'warning-row';
      /*if(column.label == '更新日期')
        if(row.issued != this.compare_edit_Data[0].issued)
          return 'warning-row';*/
      if(column.label == 'KeyID')
        if(row.sn != this.compare_edit_Data[0].sn)
          return 'warning-row';
      if(column.label == '產品名稱')
        if(row.func_uid != this.compare_edit_Data[0].func_uid)
          return 'warning-row';
      if(column.label == '版本')
        if(row.version != this.compare_edit_Data[0].version)
          return 'warning-row';
      if(column.label == '類型')
        if(row.type != this.compare_edit_Data[0].type)
          return 'warning-row';
      if(column.label == '數量')
        if(row.count != this.compare_edit_Data[0].count)
          return 'warning-row';
      if(column.label == '到期日期')
        if(row.expiration != this.compare_edit_Data[0].expiration)
          return 'warning-row';
      if(column.label == '地區')
        if(row.region != this.compare_edit_Data[0].region)
          return 'warning-row';
      if(column.label == '備註')
        if(row.comment != this.compare_edit_Data[0].comment)
          return 'warning-row';
      if(column.label == '聯絡人')
        if(row.contact != this.compare_edit_Data[0].contact)
          return 'warning-row';
    },
    compare_row:function(row,index){
      //--------------製造修改的對照表--------------//
      this.compare_Data.length = 0;
      this.compare_edit_Data.length = 0;
      for(let origin_info of this.nofilter_info_Data)
        if(JSON.stringify(origin_info['info_id']) == JSON.stringify(row['info_id'])){
          this.compare_Data.push(origin_info);
          this.compare_edit_Data.push(row);
          }
    },
    querySearch_cc(queryString, cb){
        var results = queryString ? this.cc_opt.filter(this.createFilter(queryString)) : this.cc_opt;
        if(results.length == 0){
            results.push({value:queryString + '@eastek.com.cn',label:queryString + '@eastek.com.cn'});
            results.push({value:queryString + '@eastek.com.tw',label:queryString + '@eastek.com.tw'});
        }
        cb(results);// 調用 callback 返回建議列表的數據
    },
    createFilter(queryString) {//搜尋建議選項
        return (any) => {
          //return (any.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);原本
          return (String(any.value).toLowerCase().indexOf(String(queryString).toLowerCase()) != -1);
        };
      },
  }
}
</script>

