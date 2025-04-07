<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.menuButton:hover span {
    padding-right: 25px;
}
.menuButton {
    transition: all 0.5s;
    cursor: pointer;
}

.menuButton span {
    cursor: pointer;
    position: relative;
}
.menuButton span:after {
    content: '\00bb';
    position: absolute;
    opacity: 0;
    top: 0;
    right: -20px;
}

.menuButton:hover span:after {
    opacity: 1;
    right: 0;
}
</style>
<template>
  <div>
    <div>帳號:<el-input v-model="user[0]" placeholder="請輸入帳號(使用者名稱)" style="width:200px;"></el-input></div>
    <div>密碼:<el-input v-model="user[1]" placeholder="請輸入密碼" style="width:200px;" show-password></el-input></div>
    <div><el-button class="menuButton" @click="login" type="primary" style="width:100px;" plain>登入</el-button>
  </div>
</template>

<script>
export default {
  name: 'login',
  data: function() {
        return { 
            user:['','','',''],//user[0]:user user[1]:password user[2]:email user[3]:region
            dialogVisible:false,
        }
  },
  mounted() {//監聽enter 若按enter則觸發login
    let _this = this;
    document.onkeydown = function(e) {
        if (_this.$route.name == "login") {
            let key = window.event.keyCode;
            if (key == 13) 
                _this.login();
            }
    }
  },
  methods:{
    login(){
        this.axios.get("/login",{
            params:{
                user: JSON.stringify(this.user),
                mode:'login'
            }
        }).then((response)=>{
            let res = response.data;
            if(res.msg == '登入成功!'){
                this.user[2] = res.email;
                this.$message({message: res.msg, type: 'success'});
                sessionStorage.setItem('token', 'ImLogin');//驗證器
                sessionStorage.setItem("user", JSON.stringify(this.user));//驗證器
                sessionStorage.setItem("authority",JSON.stringify(res.authority));//驗證器
                this.$router.push({name: 'Show_All'});
            }
            else if (res.msg == '密碼錯誤!')
                this.$message({message: res.msg, type: 'error'});
            else 
                this.$message({message: res.msg, type: 'error'});
        
        });
    }
  }
}
</script>

