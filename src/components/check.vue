<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
#note{
    display:inline;
}
.input_no_border textarea.el-textarea__inner{
  border: 0px solid #dcdfe6;
  resize:none;
}
.el-textarea ::-webkit-scrollbar{
    display: none;
}
.el-notification {
  white-space:pre !important; 
  width:450px;
}
</style>
<template>
  <div>
      <el-link type="success" style="position:relative;left:280px;bottom:50px;" icon="el-icon-s-custom">{{user[0]}}</el-link>
      <div style="position:relative;top:50px"align = "center">
        <el-table
        :data="app_Data"
        style="width: 95%">
        <el-table-column align="left" prop="check" width="55">
        <template slot-scope = "{row,$index}">
          <el-checkbox v-model="check[$index]" @change="click_checkbox(check[$index],$index)" :disabled="disabled_checkbox(row)"></el-checkbox>
        </template>
        </el-table-column>
        <el-table-column type="" header-align="center" prop="validator"  :render-header="label_for_validator" width="300">
        <template align="left" slot-scope = "{row,$index}">
          審核群組:
          <template v-for="(item, index) in row.validator['verify_group']">
          <span style="color: #67C23A" v-if="row.validator['verify_check']['verify_group'][index] == true">{{item}}</span><!--條件通過-->
          <span style="color: #FF7575" v-if="row.validator['verify_check']['verify_group'][index] == false">{{item}}</span><!--條件未過-->
          <span v-if="(index+1) != row.validator['verify_group'].length">,</span>
          </template>
          <br>審核人:
          <template v-for="(item, index) in row.validator['verify_user']">
          <span style="color: #67C23A" v-if="row.validator['verify_check']['verify_user'][index] == true">{{item}}</span><!--條件通過-->
          <span style="color: #FF7575" v-if="row.validator['verify_check']['verify_user'][index] == false">{{item}}</span><!--條件未過-->
          <span v-if="(index+1) != row.validator['verify_user'].length">,</span>
          </template>
          <br>審核人數:
          <span style="color: #67C23A" v-if="row.validator['verify_check']['verify_num'] >= row.validator['verify_num']">{{row.validator['verify_num']}}</span><!--條件通過-->
          <span style="color: #FF7575" v-if="row.validator['verify_check']['verify_num'] < row.validator['verify_num']">{{row.validator['verify_num']}}</span><!--條件未過-->
        </template>
        </el-table-column>
        <el-table-column type=""align="center" prop="id" label="申請編號" width="100"></el-table-column>
        <el-table-column type=""align="center" prop="fake_id" label="順序編號" width="100"></el-table-column>
        <el-table-column type=""align="center" prop="verify_status" label="審核狀態" width="120">
        <template slot-scope = "{row,$index}" >
        <span v-show="row.verify_status==1" style="color: #67C23A">已審核</span>
        <span v-show="row.verify_status==0" style="color: #FF7575">尚未審核</span>
        </template>
        </el-table-column>
        <el-table-column type=""align="center" prop="applicant" label="申請人" width="100"></el-table-column>
        <el-table-column type=""align="center" prop="date" label="申請日期" width="180"></el-table-column>
        <el-table-column type=""align="center" prop="" label="編輯" width="150">
          <template slot-scope = "{row,$index}" ><!--此時row是app_data-->
            <el-button type="text" @click="open_dialog(row,$index)">查看資料</el-button>
            <el-dialog width='1500px'title="申請內容" :visible.sync="dialogTableVisible[$index]">
              <span style="position:relative;left:50px;bottom:100px;"> 申請人 :</span>
                <el-input class="input_no_border" type="textarea" :autosize="{ minRows: 1, maxRows: 1}"name="sender" v-model="content['user']" readonly style="position:relative;bottom:103px;left:52px;width:150px;"></el-input>
              <span style="position:relative;bottom:75px;right:168px;"> 申請內文 :</span>
                <el-input class="input_no_border" type="textarea" :autosize="{ minRows: 4, maxRows: 4}" name="sender" v-model="content['text']" readonly style="position:relative;bottom:15px;right:165px;width:250px;"></el-input>
              <span style="position:relative;bottom:75px;right:155px;"> 審核者回覆 :</span>
                <el-input type="textarea" :autosize="{ minRows: 4, maxRows: 4}" name="sender" v-model="content['reply']" style="position:relative;bottom:15px;right:140px;width:400px;"></el-input>
              <span style="position:relative;right:110px;bottom:100px;" > 附件下載 :</span>
                <el-button style="position:relative;right:90px;bottom:100px;" type="text" @click="download_check(row,$index)">license-application.xlsx</el-button>
              <span style="position:relative;bottom:75px;right:295px;"> 副本 :</span>
                <template  v-for="(item, index) in cc">
                    <el-autocomplete v-model="cc[index]" :style="cc_location(index,'input')" :fetch-suggestions="querySearch_cc" placeholder="請輸入副本" ></el-autocomplete>
                    <el-button v-show="index != 0" type="text" icon="el-icon-error" :style="cc_location(index,'button')" @click="remove_cc(index)"></el-button>
                    <br>
                    <br>
                </template>
                <el-button type="text" icon="el-icon-circle-plus" style="font-size:15px;position:absolute;top:80px;right:160px;" @click="add_cc()"></el-button>
              <el-table :data="tableData" >
                 <el-table-column align="center" width="120px" prop="customer" label="審核">
                  <template slot-scope = "{row,$index}" ><!--此時row是app_data['data']-->
                    <el-radio-group  :fill="radio[$index] == '√'? '#67C23A':'#F56C6C'" v-model="radio[$index]" @change="verify_change(row,$index)" size="mini">
                      <el-radio-button label="√"></el-radio-button>
                      <el-radio-button label="×" ></el-radio-button>
                    </el-radio-group>
                  </template>
                </el-table-column>
                <el-table-column type=""align="center" prop="" label="編輯" width="130">
                  <template slot-scope = "{row,$index}" >
                  <el-row>
                    <el-button type="primary" size="mini"@click.native="handleCheck($index, row)"  v-if="showEdit[$index]"icon="el-icon-check" circle></el-button>
                    <el-button type="danger"  style="position:relative;right:5px;" size="mini"@click.native="handelRestore($index, row)"  v-if="showEdit[$index]"icon="el-icon-close" circle></el-button>
                    <el-button type="primary" size="mini"@click.native="handleEdit($index, row)"  v-if="!showEdit[$index]"icon="el-icon-edit" circle></el-button>
                    <!--<el-button type="danger"  style="position:relative;right:5px;" size="mini"@click="deleterow(row)" v-if="!showEdit[$index]" icon="el-icon-delete" circle></el-button>-->
                    <el-popover ref="popover" width="950px" trigger="hover" placement="top">
                      <el-table :cell-class-name="cell_color" :data="compare_Data" >
                      <el-table-column width="100px" prop="customer" label="客戶"></el-table-column>
                      <el-table-column width="130px" prop="issued" label="更新日期"></el-table-column>
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
                <el-table-column width="100px" prop="operator" label="操作"></el-table-column>
                <el-table-column align="center" width="140px" prop="customer" label="客戶">
                  <template slot-scope = "{row,$index}" >
                    <el-autocomplete  v-if="showEdit[$index]" style="width: 110px"  size='small' name="customer" v-model="row.customer"
                        :fetch-suggestions="querySearch_customer"></el-autocomplete>
                    <!--<el-input v-if="showEdit[$index]" type="text" name="customer" v-model="row.customer" style="width: 110px"></el-input>-->
                    <span v-if="!showEdit[$index]">{{row.customer}}</span>
                  </template>
                </el-table-column>
                <el-table-column align="center" width="165px" prop="issued" label="更新日期">
                  <template slot-scope = "{row,$index}" >
                    <el-date-picker v-if="showEdit[$index]" value-format="yyyy-MM-dd" type="date" name="issued" v-model="row.issued" style="width: 135px;"></el-date-picker>
                    <span v-if="!showEdit[$index]">{{row.issued}}</span>
                  </template>
                </el-table-column>
                <el-table-column align="center" width="120px" prop="sn" label="KeyID">
                <template slot-scope = "{row,$index}" >
                    <el-input v-if="showEdit[$index]" type="text" name="sn" v-model="row.sn" style="width: 90px"></el-input>
                    <span v-if="!showEdit[$index]">{{row.sn}}</span>
                </template>
                </el-table-column>
                <el-table-column align="center" width="210px" prop="func_uid" label="產品名稱">
                <template slot-scope = "{row,$index}" >
                    <el-autocomplete  v-if="showEdit[$index]" style="width: 180px"  size='small' name="func_uid" v-model="row.func_uid"
                        :fetch-suggestions="querySearch_func_uid"></el-autocomplete>
                    <!--<el-input v-if="showEdit[$index]" type="text" name="func_uid" v-model="row.func_uid" style="width: 130px"></el-input>-->
                    <span v-if="!showEdit[$index]">{{row.func_uid}}</span>
                </template>
                </el-table-column>
                <el-table-column align="center" width="100px" prop="version" label="版本">
                <template slot-scope = "{row,$index}" >
                    <el-input v-if="showEdit[$index]" type="text" name="version" v-model="row.version" style="width: 70px"></el-input>
                    <span v-if="!showEdit[$index]">{{row.version}}</span>
                </template>
                </el-table-column>
                <el-table-column align="center" width="110px" prop="type" label="類型">
                <template slot-scope = "{row,$index}" >
                    <el-autocomplete  v-if="showEdit[$index]" style="width:80px"  size='small' name="type" v-model="row.type"
                        :fetch-suggestions="querySearch_type"></el-autocomplete>
                    <!--<el-input v-if="showEdit[$index]" type="text" name="type" v-model="row.type" style="width: 60px"></el-input>-->
                    <span v-if="!showEdit[$index]">{{row.type}}</span>
                </template>
                </el-table-column>
                <el-table-column align="center" width="80px" prop="count" label="數量">
                <template slot-scope = "{row,$index}" >
                    <el-input v-if="showEdit[$index]" type="text" name="count" v-model="row.count" style="width: 50px"></el-input>
                    <span v-if="!showEdit[$index]">{{row.count}}</span>
                </template>
                </el-table-column>
                <el-table-column align="center" width="165px" prop="expiration" label="到期日期">
                <template slot-scope = "{row,$index}" >
                  <el-date-picker v-if="showEdit[$index]" value-format="yyyy-MM-dd" type="date" name="expiration" v-model="row.expiration" style="width: 135px;"></el-date-picker>
                  <span v-if="!showEdit[$index]">{{row.expiration}}</span>
                </template>
                </el-table-column>
                <el-table-column align="center" width="110px" prop="region" label="地區">
                <template slot-scope = "{row,$index}" >
                  <el-autocomplete  v-if="showEdit[$index]" style="width:80px"  size='small' name="region" v-model="row.region"
                    :fetch-suggestions="querySearch_region"></el-autocomplete>
                  <!--<el-input v-if="showEdit[$index]" type="text" name="region" v-model="row.region" style="width: 60px"></el-input>-->
                  <span v-if="!showEdit[$index]">{{row.region}}</span>
                </template>
                </el-table-column>
                <el-table-column align="center" width="140px" prop="comment" label="備註">
                <template slot-scope = "{row,$index}" >
                  <el-input v-if="showEdit[$index]" type="text" name="comment" v-model="row.comment" style="width: 110px"></el-input>
                  <span v-if="!showEdit[$index]">{{row.comment}}</span>
                </template>
                </el-table-column>
                <el-table-column align="center" width="100px" prop="contact" label="聯絡人">
                <template slot-scope = "{row,$index}" >
                  <el-input v-if="showEdit[$index]" type="text" name="contact" v-model="row.contact" style="width: 70px"></el-input>
                  <span v-if="!showEdit[$index]">{{row.contact}}</span>
                </template>
                </el-table-column>
              </el-table>
              <div>
                <el-button round = "true" style="position:relative;top:5px;width:150px;height:50px;" @click="dialog_cancel(row,$index)" size = "medium" >取消</el-button>
                <el-button round = "true" style="position:relative;top:5px;width:150px;height:50px;" @click="dialog_check(row,$index)" size = "medium" >確認</el-button>
              </div>
            </el-dialog>
          </template>
        </el-table-column>
        </el-table>
      </div>
      <div style="position:relative;top:50px">
        <el-button round = "true" style="position:relative;top:5px;width:150px;height:50px;" @click="submit()">送出</el-button>
      </div>
  </div>
</template>

<script>
export default {
  name: 'check',
  data: function() {
        return { 
            origin_tableData:[],//修改前的tableData
            tableData:[],
            all_Data:[],
            app_Data:[],//all_Data['appliection_data']
            dialogTableVisible:[],//dialog開關
            showEdit:[],//false:不可編輯 true:可編輯
            nofilter_info_Data:[],
            compare_Data:[],
            compare_edit_Data:[],
            radio:[],
            content:{},
            user:[],
            customer_opt:[],
            region_opt:[],
            func_uid_opt:[],
            type_opt:[{label: '正式',value: '正式'},
                    {label: '測試',value: '測試'},
                    {label: '出貨',value: '出貨'},
                    {label: '永久',value: '永久'}],
            cc:[''],
            cc_opt:[],
            check:[]
        }
  },
  created(){
    this.axios.get('/check/' + this.$route.params.verifyname,{
      headers: {'Content-Encoding': 'gzip'}
      }).then(response => {
      this.user = JSON.parse(sessionStorage.getItem('user'))
      this.all_data = JSON.parse(JSON.stringify(response.data));//所有數據傳入all_Data

      this.app_Data = JSON.parse(JSON.stringify(response.data['application_data']));
      for(let app of this.app_Data)
        this.check.push(false)
      var module_map = new Map()
      for (let func_uid of this.all_data['module_data']){
        this.func_uid_opt.push({value:func_uid['caption'],label:func_uid['caption']});
        module_map.set(func_uid['mod_uid'],func_uid['caption'])
      }
      
      for (let region of this.all_data['region_data'])
        this.region_opt.push({value:region['name'],label:region['name']});

      var cc_set = new Set();
      for(let user of this.all_data['sn_data'])
        for(let user_email of user['user'].split(','))
            cc_set.add(user_email)
      for(let user of cc_set)
        this.cc_opt.push({value:user,label:user})

      for (let customer of this.all_data['customer_data'])
        this.customer_opt.push({value:customer['name']+'|'+customer['site'],label:customer['name']+'|'+customer['site']})
      var i = 1
      for(let app of this.app_Data){
        app = Object.assign(app,{'fake_id':i,'verify_status':1,'check':false})//0:尚未審核 1:已審核
        i++
      }
      for(let app of this.app_Data){
        let test = 0
        app['data'] = JSON.parse(app['data'])
        app['validator'] = JSON.parse(app['validator'])
        for(let data of app['data']){
          if(data.verify == undefined && data.reason == undefined){
            data = Object.assign(data,{'verify':'','reason':null})
            test = 1
          }
          if(data.verify == '')
            test = 1
        }
        if(test == 1)
          app['verify_status'] = 0
        app['data'] = JSON.stringify(app['data'])
      }
      for(var i = 0; i < this.app_Data.length; i++){
        this.dialogTableVisible.push(false);
      }
      var order_form = JSON.parse(JSON.stringify(this.all_data['info_data']));//複製一個完全獨立的info 深複製
      var i = 0
      var sn_dict = response.data['sn_dict']
      var product_map = new Map()
      var option_map = new Map()
      for(let product of response.data['product_data'])
        product_map.set(product['product_name'],{'category_id':product['category_id'],'caption':product['caption']})
      for(let option of response.data['option_data'])
        option_map.set(option['option_name'],{'category_id':product_map.get(option['product_name'])['category_id'],'product_name':option['product_name'],'caption':option['caption']})

      for (let info of this.all_data['info_data']){
        if(sn_dict[info['sn']] != undefined){
            if(response.data['customer_data'][sn_dict[info['sn']]['sn_id'] - 1]['site'] !='')
              order_form[i] = Object.assign(order_form[i],{'customer':this.all_data['customer_data'][sn_dict[info['sn']]['sn_id'] - 1]['name'] + '|' + 
              this.all_data['customer_data'][sn_dict[info['sn']]['sn_id'] - 1]['site'],'user':sn_dict[info['sn']]['user']
              ,'info':[sn_dict[info['sn']]['sn_id']['note1'],sn_dict[info['sn']]['sn_id']['note2'],sn_dict[info['sn']]['sn_id']['note3'],sn_dict[info['sn']]['sn_id']['note4'],sn_dict[info['sn']]['sn_id']['note5']]})
            else
              order_form[i] = Object.assign(order_form[i],{'customer':this.all_data['customer_data'][sn_dict[info['sn']]['sn_id'] - 1]['name'],'user':sn_dict[info['sn']]['user']
              ,'info':[sn_dict[info['sn']]['sn_id']['note1'],sn_dict[info['sn']]['sn_id']['note2'],sn_dict[info['sn']]['sn_id']['note3'],sn_dict[info['sn']]['sn_id']['note4'],sn_dict[info['sn']]['sn_id']['note5']]})
            if(sn_dict[info['sn']]['region'] != '')
                order_form[i] = Object.assign(order_form[i],{'region':response.data['region_data'][parseInt(sn_dict[info['sn']]['region'],10) - 1]['name']})
            else
              order_form[i] = Object.assign(order_form[i],{'region':''})
          }
          if(option_map.get(info['func_uid']) != undefined){//將option換成caption(product_name) 
            order_form[i] = Object.assign(order_form[i],{'caption':option_map.get(info['func_uid'])['category_id']})
            order_form[i]['func_uid'] = (option_map.get(info['func_uid'])['caption']+'('+option_map.get(info['func_uid'])['product_name']+')');
          }
          else if(product_map.get(info['func_uid']) != undefined){//將product_name換成caption
            order_form[i] = Object.assign(order_form[i],{'caption':product_map.get(info['func_uid'])['category_id']})
            order_form[i]['func_uid'] = product_map.get(info['func_uid'])['caption'];//edit介面需要
          }
          if(module_map.get(info['type']) != undefined)
            order_form[i]['type'] = module_map.get(info['type']);//edit介面需要
        i++
      }
      this.nofilter_info_Data = JSON.parse(JSON.stringify(order_form));//複製一個完全獨立的info(未過濾) 深複製
      for (let info of this.nofilter_info_Data){//如在 (users) 有資料, 就去掉信箱網域(@後面)
          for(let user of this.all_data['user_data'])
          if (info['contact'] == user['email']){
              info['contact'] = user['user'];
          }
      }
      for (let info of this.nofilter_info_Data){//當聯絡人超過兩人時的nofilter email簡化
      if(info['contact'].split(',').length > 1){
        info['contact'] = info['contact'].split(',')
        for(let i = 0; i < info['contact'].length; i++){
          for(let user of this.all_data['user_data'])
            if(info['contact'][i] == user['email']){
              info['contact'][i] = user['user']
            }
        }
        info['contact'] = info['contact'].join()
      }
    }
    })
  },
  methods:{
    click_checkbox(check,index){
      this.$set(this.app_Data[index],'check',check)
    },
    cc_location(index,mode){
      if(mode == 'input'){
        var top = (80 + index * 45)
        return ("width:200px;position:absolute;right:200px;top:" + String(top)+"px")
      }
      else if(mode == 'button'){
        var top = (63 + index * 45)
        return ("color:#F56C6C;font-size:15px;position:absolute;right:192px;top:"+String(top)+'px')
      }
    },
    add_cc(){//上方聯絡人修改框增加
        this.cc.push('');
    },
    remove_cc(index){//上方聯絡人修改框減少
      this.cc.splice(index,1);
    },
    tranfer_xlsx(data) {//web下載 xlsx
      if (!data) {
        return
      }
      let url = window.URL.createObjectURL(new Blob([data]))
      let link = document.createElement('a')
      link.style.display = 'none'
      link.href = url
      link.setAttribute('download', 'verify-application.xlsx')
  
      document.body.appendChild(link)
      link.click()
    },
    download_check(row,index){
      this.axios({
          method: 'post', // 请求方式
          url: '/download_check',
          data: {
            data:row
          }, // 请求参数
          responseType: 'blob' // 服务器返回的数据类型
        }).then((response)=>{
          this.tranfer_xlsx(response.data)
        })
    },
    submit(){
      var pass_app_Data = []//只儲存已通過的資料
      for(let app of this.app_Data)
        if(app['check'] == true)
          pass_app_Data.push(app)
      
      if(pass_app_Data.length == 0){
        this.$message({message: '尚未審核任何資料', type: 'error'});
        return;
      }
      this.$confirm('是否確定送出審核?', '提示', {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.axios.post("/check_verify",{
                verify_Data:pass_app_Data,
                user:this.user
            }).then((response)=>{
                this.$message({
                  type: 'success',
                  message: '審核成功!'
                });
                //location.reload();
                this.$router.push({name: 'Show_All'});
            });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消送出審核'
          });          
        });
    },
    verify_change(row,index){//二級參數無法直接渲染視圖 顧透過change來給row.verify值
      this.$set(this.tableData[index],'verify',this.radio[index]);
      if(this.radio[index] == '×'){
        var comment = prompt("請輸入審核原因：\n");
        row.reason = comment;
      }
    },
    dialog_check:function(row,index){//把dialog修改的資料儲存在row['data']
      for(var i = 0; i < this.showEdit.length; i++)
        if(this.showEdit[i] == true){
          this.$message({message: '請先將確認修改資料√', type: 'error'});
          return;
        }
        this.app_Data[index]['verify_status'] = 1
        this.app_Data[index]['check'] = true
        this.$set(this.check,index,true)
        for(let data of this.tableData)
          if(data.verify == ''){
            this.app_Data[index]['verify_status'] = 0
            this.app_Data[index]['check'] = false
            this.$set(this.check,index,false)
          }
      row['data'] = JSON.stringify(this.tableData);
      this.content['cc'] = this.cc.join();
      row['content'] = JSON.stringify(this.content);
      console.log(this.app_Data[index])
      this.$set(this.dialogTableVisible,index,false);
          this.axios.post("/dialog_check",{
                check_data:this.app_Data[index],
                user:this.user
            }).then((response)=>{
                location.reload();
            });
    },
    open_dialog:function(row,index){
      console.log(JSON.parse(row['data']))
      this.tableData = JSON.parse(row['data']);//tableData就是當前你點查看資料時的row的data(已轉成array)
      this.content = JSON.parse(row['content'])
      this.cc = this.content['cc'].split(',')
      this.origin_tableData = JSON.parse(JSON.stringify(this.tableData));
      this.dialogTableVisible[index]=true;
      this.showEdit.length = 0;//重置開關
      this.radio.length = 0;
      for(let i = 0; i < this.tableData.length; i++){//showEdit&radio的數量=tableData[data]數量 
        this.showEdit.push(false);//showEdit:編輯修改的開關
        this.radio.push('');//勾選勾叉的開關
      }
      
      var i = 0;
      for(let data of this.tableData){//verify用來儲存審核是否通過
          this.radio[i] = data.verify;
        i++
      }
    },
    dialog_cancel:function(row,index){//關閉dialog
      this.$set(this.dialogTableVisible,index,false)
      this.cc=[''];
    },
    handleEdit(index, row) {//修改tableData資料
      this.$set(this.showEdit,index,true)
    },
    /*deleterow(row){//刪除tableData單列資料
      for(var i = 0; i < this.tableData.length; i++)
        if(JSON.stringify(row) == JSON.stringify(this.tableData[i])){
          this.tableData.splice(i,1);
          this.origin_tableData.splice(i,1);
        }
    },*/
    handleCheck(index,row){
      var test = 0;
      for(let info of this.nofilter_info_Data)//比對是否有衝突
        if(this.tableData[index]['sn'] != this.origin_tableData[index]['sn'] || 
            this.tableData[index]['type'] != this.origin_tableData[index]['type'] || 
            this.tableData[index]['func_uid'] != this.origin_tableData[index]['func_uid'])
          if(this.tableData[index]['sn'] == info['sn'] && this.tableData[index]['type'] == info['type'] && this.tableData[index]['func_uid'] == info['func_uid']){
            var msg = '修改資料'+ '\nKeyID:' + this.tableData[index]['sn'] +'\n類型:' + this.tableData[index]['type'] +'\n產品名稱:' + this.tableData[index]['func_uid'] + '\n已有重複資料';
            //this.$message({message: msg, type: 'error'});
            this.$notify.error({
              title: '修改通知',
              message: msg,
              duration: 0
            });
            this.tableData[index] = JSON.parse(JSON.stringify(this.origin_tableData[index]));
            this.$set(this.showEdit,index,false)
            test = 1;
          }
      if(test == 0){
      this.origin_tableData[index] = this.tableData[index];
      this.$set(this.showEdit,index,false)
      }
    },
    handelRestore(index, row){
      this.tableData[index] = JSON.parse(JSON.stringify(this.origin_tableData[index]));
      this.$set(this.showEdit,index,false)
    },
    compare_row(row,index){//此時row是app_data['data']
      //--------------製造修改的對照表--------------//
      for(let origin_info of this.nofilter_info_Data)
        if(JSON.stringify(origin_info['info_id']) == JSON.stringify(row['info_id'])){
          console.log(origin_info)
          this.$set(this.compare_Data,0,origin_info)
          this.$set(this.compare_edit_Data,0,row)
          }
    },
    cell_color({row, column, rowIndex, columnIndex}){//若原來資料與修改後資料不依 則顯示紅色
      if(column.label == '客戶')
        if(row.customer != this.compare_edit_Data[0].customer)
          return 'warning-row';
      if(column.label == '更新日期')
        if(row.issued != this.compare_edit_Data[0].issued)
          return 'warning-row';
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
    querySearch_customer(queryString, cb) {
      var results = queryString ? this.customer_opt.filter(this.createFilter(queryString)) : this.customer_opt;
      cb(results);// 調用 callback 返回建議列表的數據
    },
    querySearch_func_uid(queryString, cb) {
        var results = queryString ? this.func_uid_opt.filter(this.createFilter(queryString)) : this.func_uid_opt;
        cb(results);// 調用 callback 返回建議列表的數據
    },
    querySearch_type(queryString, cb) {
      var results = queryString ? this.type_opt.filter(this.createFilter(queryString)) : this.type_opt;
      cb(results);// 調用 callback 返回建議列表的數據
    },
    querySearch_region(queryString, cb) {
      var results = queryString ? this.region_opt.filter(this.createFilter(queryString)) : this.region_opt;
      cb(results);// 調用 callback 返回建議列表的數據
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
        return (any.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
      };
    },
    label_for_validator(h, {column}){//validator的Label
      return(<span>審核條件<br></br>(<span style="color:black;background-color: #ffb7b7">紅色</span>為缺少條件，
      <span style="color:black;background-color:#67C23A">綠色</span>為已滿足條件)</span>)
    },
    disabled_checkbox(row){
      if(row.verify_status==0)
        return true
      if(row.validator['verify_check']['verify_group'].indexOf(false) != -1)
        return true
      if(row.validator['verify_check']['verify_user'].indexOf(false) != -1)
        return true
      if(row.validator['verify_check']['verify_num'] < row.validator['verify_num'])
        return true

      return false
    }
  }
}
</script>

