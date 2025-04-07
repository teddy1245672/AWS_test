<style>
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
  }
  .el-header {
    background-color: #B3C0D1;
    color: #333;
    line-height: 60px;
  }
  
  .el-aside {
    color: #333;
  }
</style>

<template>
  <div>
    <el-container>
    <el-aside width="210px" height="700px">
      <el-menu :default-active="$route.path"  :router="true" class="el-menu-vertical-demo" @select="route" >
        <el-menu-item align="left" index="admin"><i class="el-icon-menu"></i><span slot="title">首頁</span></el-menu-item>
        <el-menu-item index="password" align="left"><i class="el-icon-key"></i><span slot="title">更改密碼</span></el-menu-item>
        <el-submenu index="2" v-show="user_deter" align="left">
          <template slot="title"><i class="el-icon-user"></i><span slot="title">使用者</span></template>
          <el-menu-item-group>
            <el-menu-item align="left" index="user">使用者</el-menu-item>
            <el-menu-item align="left" index="group">群組</el-menu-item>
          </el-menu-item-group>
        </el-submenu>
        <el-submenu index="3" v-show="product_deter" align="left">
          <template slot="title"><i class="el-icon-box"></i><span slot="title">產品</span></template>
          <el-menu-item index="product" align="left">產品</el-menu-item>
          <el-menu-item index="option" align="left">選項</el-menu-item>
          <el-menu-item index="product_group" align="left">產品群組</el-menu-item>
        </el-submenu>
        <el-menu-item index="region" v-show="region_deter" align="left"><i class="el-icon-map-location"></i><span slot="title">業務地區</span></el-menu-item>
        <el-menu-item index="Show_All" align="left"><i class="el-icon-back"></i><span slot="title">退回主畫面</span></el-menu-item>
        <el-menu-item index="login" align="left"><i style="color:#F56C6C" class="el-icon-switch-button"></i><span style="color:#F56C6C" slot="title">登出</span></el-menu-item>
      </el-menu>
    </el-aside>
      <el-link type="success" style="position:absolute;right:80px;top:32px;" icon="el-icon-s-custom">{{user[0]}}</el-link>
    </el-container>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        user:[],
        user_id:'',
        user_deter:false,
        product_deter:false,
        region_deter:false,
      };
    },
    created(){
      this.user = JSON.parse(sessionStorage.getItem('user'))//存入user帳密
      this.axios.get("/admin_user",{
        }).then((response)=>{
          this.all_Data = JSON.parse(JSON.stringify(response.data));//所有數據傳入all_Data
          this.user_data = JSON.parse(JSON.stringify(this.all_Data['user_data']))
          for(let user_compare of this.user_data)
             if(user_compare.user == this.user[0])
               this.user_id = user_compare.user_id;

          var operator_authority = new Set();
          for(let group of this.all_Data['group_data']){//若管理員群組有現在使用者 就給予修改權限
            if(group.members.indexOf(String(this.user_id)) != -1){
              if(group.authority != '')
                if(JSON.parse(group.authority)['operator'] != undefined && JSON.parse(group.authority)['operator'] != [])
                  for(let operator of JSON.parse(group.authority)['operator'])
                    operator_authority.add(operator)
            }
          }
          var authority = []
          if(operator_authority.has('使用者權限')){
            this.user_deter = true
            authority.push('使用者權限')
          }
          if(operator_authority.has('產品權限')){
            this.product_deter = true
            authority.push('產品權限')
          }
          if(operator_authority.has('區域權限')){
            this.region_deter = true
             authority.push('區域權限')
          }
          if(operator_authority.has('下載權限'))
            authority.push('下載權限')
          sessionStorage.setItem("authority",JSON.stringify(authority));//驗證器
        });
    },
    methods: {
      route(key, keyPath) {//當點選登出時key為null觸發Logout
        if(key == 'login'){
          sessionStorage.clear();
        }
      },
    }
  }
</script>