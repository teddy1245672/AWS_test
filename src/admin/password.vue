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
    <el-container>
      <el-main>
        <div style="position:relative;right:500px">
            <div>帳號:<el-input v-model="user[0]" style="width:200px" disabled></el-input></div>
            <div>密碼:<el-input v-model="user[1]" style="width:200px" :disabled="!edit_lock"></el-input></div>
            <div><el-button type="primary" plain @click="edit_lock = true" v-show="edit_lock == false">更改密碼</el-button></div>
            <div style="position:relative;left:20px;">
              <el-button type="primary" plain @click="edit_lock = false" v-show="edit_lock == true">取消</el-button>
              <el-button type="primary" plain @click="check" v-show="edit_lock == true">確認</el-button>
            </div>
        </div>
      </el-main>
    </el-container>
  </el-container>
  </div>
</template>
<script>
import Aside from '@/admin/aside'
  export default {
    components: {Aside},
    data() {
      return {
        user:[],
        edit_lock:false,
      };
    },
    created(){
          this.user = JSON.parse(sessionStorage.getItem('user'))//存入user帳密
    },
    methods: {
        check(){
            if(this.user[1] == ''){
                this.$message({message: '密碼不得為空', type: 'error'});
                return;
            }
            this.axios.get("/edit_password",{
                params:{
                    user: JSON.stringify(this.user),
                }
                }).then((response)=>{
                    sessionStorage.setItem("user", JSON.stringify(this.user));//驗證器
                    this.edit_lock = false;
                    this.$message({message: '密碼修改成功', type: 'success'});
                })
        }
    }
  }
</script>