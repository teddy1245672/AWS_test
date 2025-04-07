<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
  .el-table .exceed-row {
    background: #ffb7b7;
  }
  .el-table .warning-row {
    background: oldlace;
  }
  .el-table .success-row {
    background: #f0f9eb;
  }
  .el-tabs {
    margin: 5px;
  }
</style>
<template>
  <div>
    <div>
      <div style="position:relative;bottom:5px;">資料更新時間:{{update_time}}</div>
      <el-popover ref="popover" trigger="hover" width="300" placement="bottom">
        <div>
        <div><span>成員名稱: {{user[0]}}</span></div>
        <div><span>-----------------------------------------</span></div>
        <div><span>單頁筆數: <span>
        <el-select style="width:80px;" v-model="pagesize" size="small" placeholder="請選擇">
          <el-option key= '10' label="10" value="10"></el-option>
          <el-option key= '50' label="50" value="50"></el-option>
          <el-option key= 'all' label="all" value="all"></el-option>
        </el-select></div>
        <div><span>顯示模式:<span><el-switch v-model="mode" @change="mode_switch"active-text="KeyID" active-value="KeyID"inactive-text="產品"inactive-value="product"></el-switch></div>
        <div><el-button type="text" @click="$router.push({name: 'admin', query:{}})" style="height:10px;">後台管理</el-button></div>
        <div><el-button type="text" @click="Logout" style="color:#FFA1A1;height:10px;">登出</el-button></div>
        </div>
        <el-button class="memeber_button" type="text" slot="reference" icon="el-icon-user"></el-button>
      </el-popover>
    </div>
    <div align="center">
        <div>
            <el-table
            ref="showtable"
            :data="tableData">
            <el-table-column type="selection"align="center" prop="checked" label="KeyID" width="150"></el-table-column>
            <el-table-column align="center"  prop="sn_id" label="客戶" width="150"></el-table-column>
            <el-table-column align="center"  prop="sn" label="KeyID" width="150"></el-table-column>
            <el-table-column align="center"  prop="region" label="區域" width="150"></el-table-column>
            <el-table-column align="center"  prop="user" label="負責人" width="150"> </el-table-column>
            <el-table-column align="center"  prop="record" label="紀錄" width="150"> </el-table-column>
            <el-table-column align="center"  prop="note1" label="備註1" width="150"> </el-table-column>
            <el-table-column align="center"  prop="note2" label="備註2" width="150"> </el-table-column>
            <el-table-column align="center"  prop="note3" label="備註3" width="150"> </el-table-column>
            <el-table-column align="center"  prop="note4" label="備註4" width="150"> </el-table-column>
            <el-table-column align="center"  prop="note5" label="備註5" width="150"> </el-table-column>
            </el-table>
        </div>
    </div>
  </div>
</template>
<script>

export default {
  name: 'KeyID',
  data () {
    return {
      all_Data:{},//整個資料庫的數據
      tableData: [],//要顯示的tabledata
      customer_data:[],
      region_data:[],
      origin_data:[],
      user:[],
      //篩選欄位建議選項及選中值
      mode:'KeyID',//顯示模式
      update_time:'',//push heroku的時間
      pagesize:0,
    }
  },
  created () {//創建原始資料
    this.axios.get('/KeyID',{}).then(response => {
      this.user = JSON.parse(sessionStorage.getItem('user'))//存入user帳密
      this.all_Data = JSON.parse(JSON.stringify(response.data));//所有數據傳入all_Data
      console.log(this.all_Data)
      this.customer_data = JSON.parse(JSON.stringify(this.all_Data['customer_data']))
      this.region_data = JSON.parse(JSON.stringify(this.all_Data['region_data']))
      this.tableData = JSON.parse(JSON.stringify(this.all_Data['sn_data']))
      
      
    })
  },
  methods: {
    mode_switch(){
      this.axios.post("/save_to_user_setting",{
        source:'KeyID',
        user:this.user,
        mode:this.mode,
        //pagesize:this.pagesize
      }).then(response => {
        this.$router.push({name: 'Show_All'});
      })
    },
    Logout:function(){
      sessionStorage.removeItem('token'); 
      sessionStorage.removeItem('user');
      sessionStorage.removeItem('authority');
      this.$router.push('/login');
    },
  }
}
</script>


