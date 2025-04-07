<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .el-table .exceed-row {
    background: #ffb7b7;
  }
  .el-table .warning-row {
    background: oldlace;
  }
  .el-table .success-row {
    background: #f0f9eb;
  }
  .el-tabs /deep/ .el-tabs__item {
    padding:0 5px;
    text-align:center;
  }
  .el-tabs {
    margin: 5px;
  }
  .el-table /deep/.selection_style .cell .el-checkbox__inner{
    display:none;
    position:relative;
  }
 .el-table /deep/.selection_style .cell:before{
    content:'編輯';
    position:absolute;
    left:27px;
  }
  .fade-enter,
  .fade-leave-active{
    opacity: 0;
  }
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.5s;
  }
  #menu {
    position: fixed;
    top: 40%;
    right: 5%;
    z-index:9999;
  }
  
  .OperatorButton:hover {
    font-size:26px;
  }
  .OperatorButton {
    cursor: pointer;
    font-size:20px;
    position:relative;
    left:75px;
    bottom:20px;
    display:inline;
    transition: all 0.4s;
  }
  .memeber_button:hover {
    font-size:30px;
  }
  .memeber_button {
    font-size:25px;
    position:absolute;
    top:5px;
    right:35px;
    cursor: pointer;
    transition: all 0.4s;
  }
</style>
<template>
  <div>
    <transition name="fade"><!--loading動畫-->
      <loading v-if="isLoading"></loading>
    </transition>
    <div id = "menu">
      <div><el-button class="OperatorButton" circle type="primary" icon="el-icon-plus"  @click="GoAdd" ></el-button></div>
      <div><el-button class="OperatorButton" circle type="primary" icon="el-icon-edit"  @click="GoEdit" ></el-button></div>
      <div><el-button class="OperatorButton" circle type="primary" icon="el-icon-timer"  @click="Go_Edit_time" ></el-button></div>
      <div><el-button class="OperatorButton" v-show="deter_download" circle type="primary" icon="el-icon-download"  @click="GoDownload" ></el-button></div>
      <div><el-button class="OperatorButton" circle type="danger" icon="el-icon-delete"  @click="GoDelete" ></el-button></div>
    </div>
    <div>
      <div style="position:relative;bottom:40px;">資料更新時間:{{update_time}}</div>
      <div style="position:relative;bottom:40px;">heroku上傳時間:{{git_push_time}}</div>
      <div style="position:relative;bottom:40px;"><span style="background-color: #ffb7b7">紅色</span>代表過期、<span style="background-color: #FFFF30">黃色</span>代表一個月內過期</div>
      <el-badge  style="position:relative;bottom:85px;left:610px;" :value="num_handle" class="item" type="danger">
        <el-button @click="GoHandle" size="medium">進入申請頁面</el-button>
      </el-badge>
      <el-popover ref="popover" trigger="hover" width="300"placement="bottom">
        <div>
        <div><span>成員名稱: {{user[0]}}</span></div>
        <div><span>-----------------------------------------</span></div>
        <div><span>單頁筆數: <span>
        <el-select style="width:80px;" v-model="pagesize" size="small" @change="pagesize_change" placeholder="請選擇">
          <el-option key= '10' label="10" value='10'></el-option>
          <el-option key= '20' label="20" value='20'></el-option>
          <el-option key= '50' label="50" value='50'></el-option>
          <el-option key= '100' label="100" value='100'></el-option>
          <el-option key= '200' label="200" value='200'></el-option>
          <el-option key= '500' label="500" value='500'></el-option>
          <el-option key= 'all' label="all" value='all'></el-option>
        </el-select></div>
        <div><span>顯示模式:<span><el-switch v-model="mode" @change="mode_switch" active-text="KeyID" active-value="KeyID" inactive-text="產品"inactive-value="product"></el-switch></div>
        <div><el-button type="text" @click="$router.push({name: 'admin', query:{}})" style="height:10px;">後台管理</el-button></div>
        <div><el-button type="text" @click="Logout" style="color:#FFA1A1;height:10px;">登出</el-button></div>
        </div>
        <el-button class="memeber_button" type="text" slot="reference" icon="el-icon-user"></el-button>
      </el-popover>
    </div>
    <div style="position:relative;bottom:60px;" align="center">
      <el-tabs tab-position="left" style="width: 100%" v-model="TabsValue" @tab-click="tabClick">
        <el-tab-pane v-for="(item, index) in Tabs" :key="item.name" :label="item.label" :name="item.name" ></el-tab-pane>
          <div align = "center">
            <el-checkbox v-model="all_checked" @change='all_check' style='position:relative;right:70px;top:5px;'></el-checkbox>
            <el-autocomplete clearable style='position:relative;right:20px;width:130px' size='small' v-model='customer_value' 
                        :fetch-suggestions="querySearch_customer" @input = 'category_filter'></el-autocomplete><!--客戶OK-->
            <el-autocomplete clearable style='position:relative;width:100px;' size='small' v-model='KeyID_value' 
                        :fetch-suggestions="querySearch_KeyID" @input = 'category_filter'></el-autocomplete><!--KeyIDOK-->
            <el-autocomplete clearable style='position:relative;left:40px;width:340px' size='small' v-model='func_uid_value' 
                        :fetch-suggestions="querySearch_funcuid" @input = 'category_filter'></el-autocomplete><!--產品名稱OK-->
            <el-autocomplete clearable style='position:relative;left:75px;width:75px' size='small' v-model='count_value' 
                        :fetch-suggestions="querySearch_count" @input = 'category_filter'></el-autocomplete><!--count-->
            <el-autocomplete clearable style='position:relative;left:80px;width:75px' size='small' v-model='type_value' 
                        :fetch-suggestions="querySearch_type" @input = 'category_filter'></el-autocomplete><!--類型-->
            <el-autocomplete clearable style='position:relative;left:85px;width:75px' size='small' v-model='region_value' 
                        :fetch-suggestions="querySearch_region" @input = 'category_filter'></el-autocomplete><!--地區OK-->
            <el-autocomplete clearable style='position:relative;left:95px;width:170px' size='small' v-model='contact_value' 
                        :fetch-suggestions="querySearch_contact" @input = 'category_filter'></el-autocomplete><!--聯絡人OK-->
            <el-popover ref="popover" title="到期日" placement="left-end" width="350" trigger="click">
              <el-date-picker @change="category_filter" value-format="yyyy-MM-dd" size="mini" v-model="expiration_value" type="daterange" range-separator="-" start-placeholder="開始日期" end-placeholder="結束日期"> </el-date-picker>
              <el-button slot="reference" plain style='position:relative;left:100px;width:115px;' size='mini'>到期日</el-button>
            </el-popover>
            <el-popover ref="popover" title='結束日期' placement="left-end" width="350" trigger="click">
              <el-date-picker @change="category_filter" value-format="yyyy-MM-dd" size="mini" v-model="issued_value" type="daterange" range-separator="-" start-placeholder="開始日期" end-placeholder="結束日期"></el-date-picker>
              <el-button slot="reference" plain style='position:relative;left:105px;width:115px;' size='mini'>更新日期</el-button>
            </el-popover>
            <!--<el-autocomplete clearable style='position:relative;left:100px;width:115px' size='small' v-model='expiration_value' 
                        :fetch-suggestions="querySearch_expiration" @input = 'category_filter'></el-autocomplete>--><!--到期日OK-->
            <!--<el-autocomplete clearable style='position:relative;left:105px;width:115px' size='small' v-model='issued_value' 
                        :fetch-suggestions="querySearch_issued" @input = 'category_filter'></el-autocomplete>--><!--更新日期OK-->
              <el-table
                ref="showtable"
                @row-click='rowclick'
                :row-class-name="tableRowColor"
                :row-style="{height:0+'px'}"
                :cell-style="{padding:6.5+'px'}"
                @sort-change='sortChange'
                @selection-change="handleSelectionChange"
                :header-cell-class-name="selection_column_style"
                :data="tableData.slice((currentPage-1)*pagesize,currentPage*pagesize)">
                <el-table-column type="selection" align="center" prop="" label="編輯" width="80"></el-table-column>
                <el-table-column align="center" sortable='custom' prop="customer" label="客戶" width="170"></el-table-column>
                <el-table-column align="center" sortable='custom' prop="sn" label="KeyID" width="105"> </el-table-column>
                <el-table-column align="center" sortable='custom' prop="func_uid" label="產品名稱" width="420"> </el-table-column>
                <!--<el-table-column align="center" sortable='custom' prop="user" label="負責人" width="150"> </el-table-column>-->
                <el-table-column align="center" sortable='custom' prop="count" label="數量" width="75"> </el-table-column>
                <el-table-column align="center" sortable='custom' prop="type" label="類型" width="75"> </el-table-column>
                <el-table-column align="center" sortable='custom' prop="region" label="地區" width="75"> </el-table-column>
                <el-table-column align="center" sortable='custom' prop="contact_display" label="聯絡人" width="200" show-overflow-tooltip></el-table-column>
                <el-table-column align="center" sortable='custom' prop="expiration" label="到期日" width="110"> </el-table-column>
                <el-table-column align="center" sortable='custom' prop="issued" label="更新日期" width="110"> </el-table-column>
                <!--<el-table-column align="center" prop="info" label="申請紀錄" width="150"> </el-table-column>-->
              </el-table>
            </div>
            <div class="pagination"><!--對頁面做分頁 當當前頁改變時改變tableData 補充:sync是雙向綁定-->
              <el-pagination 
                background
                @current-change="handleCurrentChange" 
                :current-page.sync="currentPage" 
                :page-size.sync="pagesize" 
                layout="prev, pager, next" 
                :total="tableData.length" >
              </el-pagination>
            </div>
          </div>
      </el-tabs>
    <div>
  </div>
</template>
<script>
function merge(left, right,name){//合併排序法
  const result = [];
  let leftIndex = 0;
  let rightIndex = 0;
  while(leftIndex < left.length && 
        rightIndex < right.length){
     if(left[leftIndex][name] > right[rightIndex][name]){
       result.push(left[leftIndex]);
       leftIndex++;
     } else{
       result.push(right[rightIndex]);
       rightIndex++
    }
  }  
  
  return result.concat(left.slice(leftIndex)).concat(right.slice(rightIndex));

  }
function ascending_order(initial_Data,name){//升序排序
  if (initial_Data.length === 1) {
    return initial_Data
  }
  
  // 將陣列切成左右
  const length = initial_Data.length;
  const middle = Math.floor(length / 2)
  const left = initial_Data.slice(0, middle) 
  const right = initial_Data.slice(middle)

  return merge(
    ascending_order(left,name),
    ascending_order(right,name),
    name
  )
  }

import Loading from '@/assets/loading'
export default {
  components:{ Loading },
  name: 'Show_All',
  data () {
    return {
      all_Data:{},//整個資料庫的數據
      tableData: [],//要顯示的tabledata
      origin_Data:[],//原始的tableData
      filter_Data:[],//分頁後的tableData
      sort_Data:[],//做完搜尋的Data 之後拿sort來做排序 同時也是最完整最終的Data
      checked_Data:[],//勾選row的資料
      
      currentPage: 1, //默認當前頁為1
      pagesize: 10, //每頁顯示數量
      user:[],
      TabsValue: '1',//default <all>
      Tabs: [{label: 'All',name: '1'},
        {label: '即將過期',name:'2'},
        {label: 'ezCAM',name: '3'},
        {label: 'ezCAT',name: '4'},
        {label: 'ezTool',name: '5'},
        {label: 'Quote',name: '6'},
        {label: 'ezPlan',name: '7'},
        {label: 'ezDI',name: '8'},
        {label: 'Other',name: '9'}
        ],
      //篩選欄位建議選項及選中值
      customer_opt:[],
      customer_value:'',
      issued_opt:[],
      issued_value:null,
      KeyID_opt:[],
      KeyID_value:'',
      funcuid_opt:[],
      func_uid_value:'',
      contact_opt:[],
      contact_value:'',
      expiration_opt:[],
      expiration_value:null,
      count_opt:[],
      count_value:'',
      region_opt:[],
      region_value:'',
      type_opt:[],
      type_value:'',
      num_handle:0,
      all_checked:false,
      mode:'產品',//顯示模式
      update_time:'',//push heroku的時間
      git_push_time:'',//git push 時間
      deter_download:false,//判斷是否有download excel權限
      isLoading:true
    }
  },
  created () {//創建原始資料
    this.axios.get('/show_all',{
      headers: {'Content-Encoding': 'gzip'},
    params:{
            user:JSON.stringify(JSON.parse(sessionStorage.getItem('user')))//為了讓後端 傳出來的edit table資料只限於當前使用者的
        }
    }).then(response => {
      //-----------------------------建議選項處理------------------------------//
      if(JSON.parse(sessionStorage.getItem('authority')).includes('下載權限'))
        this.deter_download = true

      this.user = JSON.parse(sessionStorage.getItem('user'))//存入user帳密
      this.all_Data = JSON.parse(JSON.stringify(response.data));//所有數據傳入all_Data
      
      this.update_time = this.all_Data['update_time']
      this.git_push_time = this.all_Data['git_push_time']
      
      for(let edit of this.all_Data['edit_data']){
        if(edit['user'] == this.user[0])
          this.num_handle = JSON.parse(edit.data).length//handle的資料筆數
      }
      for (let customer of response.data['customer_data']){
        if(customer['site'] != '')
          this.customer_opt.push({value:(customer['name'] + '|' + customer['site']),label:(customer['name'] + '|' + customer['site'])});
        else
          this.customer_opt.push({value:customer['name'],label:customer['name']});
      }
      var temp_info_func_uid = [];
      var countSet = new Set();//用set過濾 因有重複
      var contactSet = new Set();//用set過濾 因有重複
      var issuedSet = new Set();//用set過濾 因有重複
      var expirationSet = new Set();//用set過濾 因有重複
      var typeSet = new Set();//用set過濾 因有重複
      var module_map = new Map()
      response.data['module_data'].forEach(item => module_map.set(item['mod_uid'],item['caption']))
      for (let info of response.data['info_data']){
        var copy = info['contact'].replace('@eastek.com.tw','')
        copy = copy.replace('@eastek.com.cn','')
        contactSet.add(copy)
        countSet.add(info['count'])
        temp_info_func_uid.push(info['func_uid'])
        issuedSet.add(info['issued'])
        expirationSet.add(info['expiration'])
        if(module_map.get(info['type'])!=undefined)
          typeSet.add(module_map.get(info['type']))
      }
      contactSet.forEach(item => this.contact_opt.push({value:item,label:item}))
      response.data['sn_data'].forEach(item => this.KeyID_opt.push({value:item['sn'],label:item['sn']}))
      countSet.forEach(item => this.count_opt.push({value:item,label:item}))
      response.data['region_data'].forEach(item => this.region_opt.push({value:item['name'],label:item['name']}))
      
      var func_uid_set = new Set()
      for (let funcuid of response.data['product_data'])
        if(temp_info_func_uid.includes(funcuid['product_name']))//把測試新增修改刪除(建議)去掉
          func_uid_set.add(funcuid['caption']);
      for(let option of response.data['option_data'])
        if(temp_info_func_uid.includes(option['option_name']))
          func_uid_set.add(option['caption']);
      
      func_uid_set.forEach(item => this.funcuid_opt.push({value:item,label:item}))
      issuedSet.forEach(item => this.issued_opt.push({value:item,label:item}))
      expirationSet.forEach(item => this.expiration_opt.push({value:item,label:item}))
      typeSet.forEach(item => this.type_opt.push({value:item,label:item}))
      //---------------------------處理tableData關聯資料統整-------------------------//
      var order_form = JSON.parse(JSON.stringify(response.data.info_data));//複製一個完全獨立的info 深複製
      var sn_dict = response.data['sn_dict']
      var i = 0
      var product_map = new Map()
      var option_map = new Map()
      for(let product of response.data['product_data'])
        product_map.set(product['product_name'],{'category_id':product['category_id'],'caption':product['caption']})
      for(let option of response.data['option_data'])
        option_map.set(option['option_name'],{'category_id':product_map.get(option['product_name'])['category_id'],'product_name':option['product_name'],'caption':option['caption']})

      for (let info of response.data['info_data']){
        if (sn_dict[info['sn']] != undefined){
          if(response.data['customer_data'][sn_dict[info['sn']]['sn_id'] - 1]['site'] != '')//若客戶site=''
            order_form[i] = Object.assign(order_form[i],{'customer':response.data['customer_data'][sn_dict[info['sn']]['sn_id'] - 1]['name'] + '|' + 
            response.data['customer_data'][sn_dict[info['sn']]['sn_id'] - 1]['site'],'user':sn_dict[info['sn']]['user']
            ,'info':[sn_dict[info['sn']]['note1'],sn_dict[info['sn']]['note2'],sn_dict[info['sn']]['note3'],sn_dict[info['sn']]['note4'],sn_dict[info['sn']]['note5']]})
          else//若客戶site!='' 則客戶name|site
            order_form[i] = Object.assign(order_form[i],{'customer':response.data['customer_data'][sn_dict[info['sn']]['sn_id'] - 1]['name'] ,'user':sn_dict[info['sn']]['user']
            ,'info':[sn_dict[info['sn']]['note1'],sn_dict[info['sn']]['note2'],sn_dict[info['sn']]['note3'],sn_dict[info['sn']]['note4'],sn_dict[info['sn']]['note5']]})
          if(sn_dict[info['sn']]['region'] != '')
            order_form[i] = Object.assign(order_form[i],{'region':response.data['region_data'][parseInt(sn_dict[info['sn']]['region'],10) - 1]['name']})
          else
            order_form[i] = Object.assign(order_form[i],{'region':''})
          }
        
        if(option_map.get(info['func_uid']) != undefined){//將option換成caption(product_name) 
          order_form[i] = Object.assign(order_form[i],{'caption':option_map.get(info['func_uid'])['category_id']})
          order_form[i]['func_uid'] = (option_map.get(info['func_uid'])['caption']+'('+option_map.get(info['func_uid'])['product_name']+')');
        }
        else{//將product_name換成caption
          order_form[i] = Object.assign(order_form[i],{'caption':product_map.get(info['func_uid'])['category_id']})
          order_form[i]['func_uid'] = product_map.get(info['func_uid'])['caption'];//edit介面需要
        }
        if(module_map.get(info['type']) != undefined)
          order_form[i]['type'] = module_map.get(info['type']);//edit介面需要
        
        i++
      }
    //--------------------------根據日期將資料上色分類----------------------//
    if(order_form.length != 0)
      order_form = ascending_order(order_form,'expiration')//綠黃紅

    var tempDate = new Date;
    tempDate.setHours(tempDate.getHours());
    var today = tempDate.toISOString().slice(0, 10)
    tempDate.setMonth(tempDate.getMonth()+1);
    var oneMonthLater = tempDate.toISOString().slice(0, 10)

    var yellow_order_form = order_form.filter(item => (item['expiration'] < oneMonthLater && item['expiration'] > today))
    order_form = order_form.filter(item=>(item['expiration'] >= oneMonthLater || item['expiration'] <= today))//調整初始數據順序 綠黃紅->黃綠紅
    for(let order of yellow_order_form)
      order_form.unshift(order)
    //-----------------------聯絡人細節省略處理------------------------//
    for(let order of order_form){//若info聯絡人在user中有對應到email 則去除尾段email address
        order = Object.assign(order,{'contact_display':order['contact'].split(',')})
        order = Object.assign(order,{'user_display':order['user'].split(',')})//新增編輯頁面需要負責人欄位
        for(let i = 0; i < order['contact_display'].length; i++){
          for(let user of this.all_Data['user_data'])
            if(order['contact_display'][i] == user['email'])
              order['contact_display'][i] = Object.assign(user['user'])
          if(order['contact_display'][i].indexOf('@eastek.com.tw') != -1 || order['contact_display'][i].indexOf('@eastek.com.cn') != -1){
            order['contact_display'][i] = order['contact_display'][i].replace('@eastek.com.tw','')
            order['contact_display'][i] = order['contact_display'][i].replace('@eastek.com.cn','')
          }
        }
        order['contact_display'] = order['contact_display'].join(',');
    }
    this.origin_Data = order_form
    this.tableData = order_form
    this.filter_Data = order_form;
    this.sort_Data = order_form;
    //this.pagesize = 10;//預設資料筆數
    this.isLoading = false;

    var user_setting = JSON.parse(this.all_Data['user_data'].filter(item => (item['user'] == this.user[0]))[0]['setting'])//處理使用者設定
    if(user_setting['pagesize'] != 'all')
      this.pagesize = user_setting['pagesize']
    else
      this.pagesize = this.tableData.length

    if(user_setting['mode'] != 'product')
      this.$router.push({name: 'KeyID'});
    })
  },
  watch:{
    },
  methods: {
    pagesize_change(){//變更單頁筆數時 去DB更改User[setting]
      if(this.pagesize == 'all'){
        this.pagesize = this.tableData.length
        this.axios.post("/save_to_user_setting",{
          source:'product',
          user:this.user,
          mode:this.mode,
          pagesize:'all'
        })
      }
      else{
        this.axios.post("/save_to_user_setting",{
          source:'product',
          user:this.user,
          mode:this.mode,
          pagesize:parseInt(this.pagesize)
        })
      }

      },
    mode_switch(){//模式切換時觸發 更改DB User[setting]
      this.axios.post("/save_to_user_setting",{
        source:'product',
        user:this.user,
        mode:this.mode,
        pagesize:this.pagesize
      }).then(response => {
        this.$router.push({name: 'KeyID'});
      })
      },
    all_check(){//自製的全選框被觸發時
      if(this.all_checked == true)
        this.$refs.showtable.toggleAllSelection()
      else 
        this.$refs.showtable.clearSelection()
      },
    selection_column_style:function(row){//將header 全選框隱藏 因為排版問題只能自己做一個自製全選框 
      if(row.columnIndex == 0)
        return 'selection_style'
      },
    Logout:function(){
      sessionStorage.clear();
      this.$router.push('/login');
      },
    GoHandle:function(){//編輯頁面
      delete this.all_Data['info_data']//edit頁面用不到 節省傳輸時間
      this.$router.push({name: 'handle', query:{user:JSON.stringify(this.user),all_Data:JSON.stringify(this.all_Data)}});
      },
    GoAdd:function(){//新增頁面
      delete this.all_Data['info_data']//edit頁面用不到 節省傳輸時間
      this.$router.push({name: 'add', query:{user:JSON.stringify(this.user),checked_Data: JSON.stringify(this.checked_Data),all_Data:JSON.stringify(this.all_Data)}});
      },
    GoEdit:function(){//修改頁面
      if(this.checked_Data[0] == undefined){
        alert('請選取須修改的選項');
        return;
      }//也可以用this.$router.push(name:'',params:{})傳參數 但要設置路由
      delete this.all_Data['info_data']//edit頁面用不到 節省傳輸時間
      this.$router.push({name: 'edit', query:{user:JSON.stringify(this.user),checked_Data: JSON.stringify(this.checked_Data),all_Data: JSON.stringify(this.all_Data)}});
      },
    Go_Edit_time:function(){//延展到期日
      if(this.checked_Data[0] == undefined){
        alert('請選取欲修改時間的資料');
        return;
      }
      this.$prompt("請輸入到期日",'到期日修改',{
        confirmButtonText: '確定',
        cancelButtonText: '取消',
        inputType:'date',
        inputPattern:/\d.\d.\d/,
        inputErrorMessage:'輸入日期不合法!'
      }).then(({ value }) => {
        for(let check of this.checked_Data){//
          check = Object.assign(check,{'operator':'修改'})
          check = Object.assign(check,{'expiration':value})
        }
        for (let check of this.checked_Data)//如在 (users) 有資料, 就去掉信箱網域(@後面)
          for(let user of this.all_Data['user_data'])
            if (check['contact'] == user['email'])
                check['contact'] = user['user'];

        this.axios.post("/save_to_handle",{
          checked_Data:this.checked_Data,
          content:'延展到期日',
          user:this.user
        }).then((response)=>{
            let res = response.data;
            location.reload();
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消修改'
        });          
      });
      },
    GoDownload:function(){//下載勾選資料
      var data_download = [];
      var i = 0;
      for(let check of this.checked_Data){
        data_download.push(check);
        data_download[i] = Object.assign(data_download[i],{'operator':'下載'});//增加index讓 row中有index
        i++;
      }
      this.axios({
        method: 'post', // 请求方式
        url: '/download_show',
        data: {
          user:this.user,
          data:data_download
        }, // 请求参数
        responseType: 'blob' // 服务器返回的数据类型
      }).then((response)=>{
        this.tranfer_xlsx(response.data)
      })
      },
    GoDelete: function(){//刪除頁面
      if(this.checked_Data[0] == undefined){
        alert('請選取須刪除的資料');
        return;
      }
      var comment = prompt("請輸入刪除原因：\n" +
                            "1.客戶測試結束\n" +
                            "2.key 損壞\n" +
                            "3.其他, __________\n\n", "");
      console.log(comment)
      if(comment == null)//當使用者按cancel時
        return;
      else if(comment == ''){
        alert('請填寫原因');
        return;
      }
      for(let check of this.checked_Data)
        check = Object.assign(check,{'operator':'刪除'})
      
      for (let check of this.checked_Data)//如在 (users) 有資料, 就去掉信箱網域(@後面)
        for(let user of this.all_Data['user_data'])
          if (check['contact'] == user['email'])
            check['contact'] = user['user'];
          
        
      this.axios.post("/save_to_handle",{
            checked_Data:this.checked_Data,
            content:comment,
            user:this.user
        }).then((response)=>{
            let res = response.data;
            location.reload();
        });
      },
    rowclick(row, event, column){//點選列時也可以觸發勾選框
      this.$refs.showtable.toggleRowSelection(row);
      },
    handleSelectionChange (val) {//當select 有變化時執行 且val是所選row的所有資訊(type:array)
      this.checked_Data = JSON.parse(JSON.stringify(val));
      },
    sortChange: function(column){//3
      var initial_Data = JSON.parse(JSON.stringify(this.sort_Data));
      var order_Data = []
      switch (column.prop) {
        case 'customer':
          order_Data = ascending_order(initial_Data,'customer');
          if(column.order == 'ascending')
            this.tableData = order_Data;
          else if(column.order == 'descending')
            this.tableData = order_Data.reverse();
          else
            this.tableData = this.sort_Data;
          break;
        case 'contact':
          order_Data = ascending_order(initial_Data,'contact');
          if(column.order == 'ascending')
            this.tableData = order_Data;
          else if(column.order == 'descending')
            this.tableData = order_Data.reverse();
          else
            this.tableData = this.sort_Data;
          break;
        case 'version':
          order_Data = ascending_order(initial_Data,'version');
          if(column.order == 'ascending')
            this.tableData = order_Data;
          else if(column.order == 'descending')
            this.tableData = order_Data.reverse();
          else
            this.tableData = this.sort_Data;
          break;
        case 'func_uid':
          order_Data = ascending_order(initial_Data,'func_uid');
          if(column.order == 'ascending')
            this.tableData = order_Data;
          else if(column.order == 'descending')
            this.tableData = order_Data.reverse();
          else
            this.tableData = this.sort_Data;
          break;
        case 'count':
          order_Data = ascending_order(initial_Data,'count');
          if(column.order == 'ascending')
            this.tableData = order_Data;
          else if(column.order == 'descending')
            this.tableData = order_Data.reverse();
          else
            this.tableData = this.sort_Data;
          break;
        case 'issued':
          order_Data = ascending_order(initial_Data,'issued');
          if(column.order == 'ascending')
            this.tableData = order_Data;
          else if(column.order == 'descending')
            this.tableData = order_Data.reverse();
          else
            this.tableData = this.sort_Data;
          break;
        case 'sn':
          order_Data = ascending_order(initial_Data,'sn');
          if(column.order == 'ascending')
            this.tableData = order_Data;
          else if(column.order == 'descending')
            this.tableData = order_Data.reverse();
          else
            this.tableData = this.sort_Data;
          break;
        /*case 'caption':
          order_Data = ascending_order(initial_Data,'caption');
          if(column.order == 'ascending')
            this.tableData = order_Data;
          else if(column.order == 'descending')
            this.tableData = order_Data.reverse();
          else
            this.tableData = this.sort_Data;
          break;*/
        case 'expiration':
          order_Data = ascending_order(initial_Data,'expiration');
          if(column.order == 'ascending')
            this.tableData = order_Data;
          else if(column.order == 'descending')
            this.tableData = order_Data.reverse();
          else
            this.tableData = this.sort_Data;
          break;
        /*case 'user':
          order_Data = ascending_order(initial_Data,'user');
          if(column.order == 'ascending')
            this.tableData = order_Data;
          else if(column.order == 'descending')
            this.tableData = order_Data.reverse();
          else
            this.tableData = this.sort_Data;
          break;*/
        case 'region':
          order_Data = ascending_order(initial_Data,'region');
          if(column.order == 'ascending')
            this.tableData = order_Data;
          else if(column.order == 'descending')
            this.tableData = order_Data.reverse();
          else
            this.tableData = this.sort_Data;
          break;
      }
      },
    category_filter: function(){//對product分頁底下的tableData做過濾2
      var customer_value = this.customer_value
      var copy_data = this.filter_Data.filter(x => 
      (x['customer'].indexOf(this.customer_value) != -1 &&
      x['contact_display'].indexOf(this.contact_value) != -1 &&
      x['type'].indexOf(this.type_value) != -1 &&
      x['func_uid'].indexOf(this.func_uid_value) != -1 &&
      String(x['count']).indexOf(String(this.count_value)) != -1 &&
      String(x['sn']).indexOf(String(this.KeyID_value)) != -1 &&
      String(x['region']).indexOf(String(this.region_value)) != -1))
      if(this.expiration_value == null && this.issued_value == null){
      }
      else if(this.expiration_value == null){
        copy_data = copy_data.filter(x => (this.issued_value[0] <= x['issued'] && x['issued'] <= this.issued_value[1]))
      }
      else if(this.issued_value == null){
        copy_data = copy_data.filter(x => (this.expiration_value[0] <= x['expiration'] && x['expiration'] <= this.expiration_value[1]))
      }
      else{
        copy_data = copy_data.filter(x => (this.issued_value[0] <= x['issued'] && x['issued'] <= this.issued_value[1]
                                          && this.expiration_value[0] <= x['expiration'] && x['expiration'] <= this.expiration_value[1]))
      }
      this.sort_Data = JSON.parse(JSON.stringify(copy_data))
      this.tableData = this.sort_Data;
      },
    tabClick(tab, event) {//當點擊標籤頁時1
      this.currentPage = 1;
      this.all_checked = false;//自製全選框連動
      this.KeyID_value = '';
      this.customer_value = '';
      if(tab.label == 'All'){//如果是all就顯示原tableData
        this.tableData = this.origin_Data;
        this.filter_Data = this.origin_Data;
        this.sort_Data = this.origin_Data;
      }
      else if(tab.label == '即將過期'){
        var tempDate = new Date;
        
        tempDate.setHours(tempDate.getHours());
        var today = tempDate.toISOString().slice(0, 10)

        tempDate.setMonth(tempDate.getMonth()+1);
        var oneMonthLater = tempDate.toISOString().slice(0, 10)
        this.filter_Data = this.origin_Data.filter(item=> item['expiration'] < oneMonthLater)//濾掉綠色
        this.filter_Data = this.filter_Data.filter(item=> item['expiration'] > today)//濾掉紅色
        this.tableData = this.filter_Data;
        this.sort_Data = this.filter_Data;
      }
      else{
        var copy_data = []
        this.filter_Data = this.origin_Data.filter(item=> item['caption'] == tab.label)
        this.tableData = this.filter_Data;
        this.sort_Data = this.filter_Data;
      }
      },
    tableRowColor({row, rowIndex}) {//比較當前與過期時間來顯示顏色
        var Index = rowIndex + (this.currentPage - 1) * this.pagesize;//分頁問題 當換到當前分頁時顏色才會顯現正確
        row.index = rowIndex;//把每一行的index放入row 為了給rowclick用
        var tempDate = new Date;
        
        tempDate.setHours(tempDate.getHours());
        var today = tempDate.toISOString().slice(0, 10)
        
        tempDate.setMonth(tempDate.getMonth()+1);
        var oneMonthLater = tempDate.toISOString().slice(0, 10)
        
        var order_expiration = this.tableData[Index]['expiration'];
        
        if (order_expiration < today){
            return 'exceed-row';
        }
        else if (order_expiration < oneMonthLater) {
            return 'warning-row';
        }
        return 'success-row';
      },
    handleCurrentChange: function(currentPage) {//點擊第幾頁
        this.currentPage = currentPage;
        this.all_checked = false;//自製全選框初始化
      },

    //---------------hearder搜索欄處理函式-------------//
    querySearch_customer(queryString, cb) {
        var results = queryString ? this.customer_opt.filter(this.createFilter(queryString)) : this.customer_opt;
        cb(results); // 調用 callback 返回建議列表的數據
      },
    querySearch_KeyID(queryString, cb) {
        var results = queryString ? this.KeyID_opt.filter(this.createFilter(queryString)) : this.KeyID_opt;
        cb(results);// 調用 callback 返回建議列表的數據
      },
    querySearch_region(queryString, cb) {
        var results = queryString ? this.region_opt.filter(this.createFilter(queryString)) : this.region_opt;
        cb(results);// 調用 callback 返回建議列表的數據
      },
    querySearch_count(queryString, cb) {
        var results = queryString ? this.count_opt.filter(this.createFilter(queryString)) : this.count_opt;
        cb(results); // 調用 callback 返回建議列表的數據
      },
    querySearch_type(queryString, cb) {
        var results = queryString ? this.type_opt.filter(this.createFilter(queryString)) : this.type_opt;
        cb(results); // 調用 callback 返回建議列表的數據
      },
    querySearch_funcuid(queryString, cb) {
        var results = queryString ? this.funcuid_opt.filter(this.createFilter(queryString)) : this.funcuid_opt;
        cb(results); // 調用 callback 返回建議列表的數據
      },
    querySearch_issued(queryString, cb) {
        var results = queryString ? this.issued_opt.filter(this.createFilter(queryString)) : this.issued_opt;
        cb(results); // 調用 callback 返回建議列表的數據
      },
    querySearch_contact(queryString, cb) {
        var results = queryString ? this.contact_opt.filter(this.createFilter(queryString)) : this.contact_opt;
        cb(results); // 調用 callback 返回建議列表的數據
      },
    querySearch_expiration(queryString, cb) {
        var results = queryString ? this.expiration_opt.filter(this.createFilter(queryString)) : this.expiration_opt;
        cb(results); // 調用 callback 返回建議列表的數據
      },
    createFilter(queryString) {//搜尋建議選項
        return (any) => {
          //return (any.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);原本
          return (String(any.value).toLowerCase().indexOf(String(queryString).toLowerCase()) != -1);
        };
      },
    tranfer_xlsx(data) {//web下載 xlsx
      if(!data)
        return
      let url = window.URL.createObjectURL(new Blob([data]))
      let link = document.createElement('a')
      link.style.display = 'none'
      link.href = url
      link.setAttribute('download', 'license-application.xlsx')
  
      document.body.appendChild(link)
      link.click()
      },
  }
}
</script>


