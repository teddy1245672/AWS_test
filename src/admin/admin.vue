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
    <Aside></Aside>
    </el-container>
  </div>
</template>
<script>
import Aside from '@/admin/aside'
  export default {
    components: {Aside},
    data() {
      return {
        all_Data:[],
        user_data:[]
      };
    },
    created(){
      this.axios.get("/admin_user",{
        }).then((response)=>{
          this.all_Data = JSON.parse(JSON.stringify(response.data));//所有數據傳入all_Data
          this.user_data = JSON.parse(JSON.stringify(this.all_Data['user_data']))
        });
    },
    methods: {
    }
  }
</script>