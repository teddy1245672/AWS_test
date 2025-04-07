import Vue from 'vue'
import App from '@/App.vue'
import router from '@/router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import axios from 'axios'
import VueAxios from 'vue-axios'
import qs from  'qs'  

//配全局属性配置，在任意组件内可以使用this.$qs獲取qs对象 (axios.post需要)
Vue.prototype.$qs = qs

Vue.config.productionTip = false
Vue.use(VueAxios, axios)
axios.defaults.baseURL = '/api'//跨域問題
Vue.use(ElementUI);

router.beforeEach((to, from, next)=>{
  if(to.matched[0].path == '/check/:verifyname'){//審核者的自動登入
    sessionStorage.setItem('token', 'ImLogin');
    axios.get("/auto_login",{
        params:{user: to.params.verifyname,}
        }).then((response)=>{
          var user = response.data;
          sessionStorage.setItem('user', JSON.stringify(user));
        });
  }
  const isLogin = sessionStorage.getItem('token') == 'ImLogin' ;
  if( isLogin ){
    if(to.path == '/option' || to.path == '/product' || to.path == '/product_group' || to.path == '/user' || to.path == '/group' || to.path == '/region'){
      const Authority = JSON.parse(sessionStorage.getItem('authority'));
      if( to.path == '/region') 
        if(Authority.includes('區域權限'))
          next();
        else{
          alert('無此權限')
          next('/admin');
        }
      else if( to.path == '/product' || to.path == '/product_group' || to.path == '/option')
        if(Authority.includes('產品權限'))
          next();
        else{
          alert('無此權限')
          next('/admin');
        }
      else if( to.path == '/user' || to.path == '/group')
        if(Authority.includes('使用者權限'))
          next();
        else{
          alert('無此權限')
          next('/admin');
        }
    }
    else
      next();
  } else {
    if( to.path !== '/login')
      next('/login');
    else
      next();
  }
});

const vue = new Vue({
  router,
  render: h => h(App)
})

vue.$mount('#app')
