<style>

</style>

<template>
  <div>
    <el-container>
    <Aside></Aside>
    <el-container>
    <el-main>
      <div align="left">
          <el-button type="primary" icon="el-icon-plus" @click="form.id=0,form.user='',form.password='',form.email='',form.groups=[],form.region='',form.record='',form.description='',add_lock = true"plain >新增</el-button>
          <el-dialog title="使用者表單-新增" :visible.sync="add_lock">
                <el-form :model="form" label-width="80px">
                    <el-form-item prop="user" label="使用者" required><el-input v-model="form.user" style="width:200px;"placeholder="請輸入使用者名稱"></el-input></el-form-item>
                    <el-form-item prop="password" label="密碼" required><el-input v-model="form.password" style="width:200px;"placeholder="請輸入密碼"></el-input></el-form-item>
                    <el-form-item prop="email" label="信箱" required><el-input v-model="form.email" style="width:300px;"placeholder="請輸入信箱"></el-input></el-form-item>
                    <el-form-item prop="groups" label="群組" >
                      <el-select v-model="form.groups" width="400px" multiple placeholder="請輸入群組">
                            <el-option v-for="item in groups_opt" :key="item.value" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item prop="region" label="區域" >
                        <el-select v-model="form.region" width="400px" placeholder="請輸入區域">
                            <el-option v-for="item in region_opt" :key="item.value" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                    <!--<el-form-item prop="record" label="紀錄" ><el-input v-model="form.record" style="width:600px;"placeholder="請輸入紀錄"></el-input></el-form-item>-->
                    <el-form-item prop="description" label="描述" ><el-input v-model="form.description" style="width:600px;"placeholder="請輸入描述"></el-input></el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button type="danger" @click="add_lock=false" plain>取消</el-button>
                    <el-button type="primary" @click="add_user" plain>確定</el-button>
                </div>
            </el-dialog>
      </div>
      <el-table :data="tableData">
        <el-table-column prop="user" label="使用者" width="100"></el-table-column>
        <el-table-column prop="password" label="密碼" width="100"></el-table-column>
        <el-table-column prop="email" label="信箱" width="200"></el-table-column>
        <el-table-column prop="groups" label="群組" fit ></el-table-column>
        <el-table-column prop="region" label="地區" width="150"></el-table-column>
        <!--<el-table-column prop="record" label="紀錄" width="100"></el-table-column>-->
        <el-table-column prop="description" label="描述" width="100"></el-table-column>
        <el-table-column prop="description" label="操作" width="100">
          <template slot-scope = "{row,$index}" >
          <el-button type="primary" icon="el-icon-edit" size="small" circle @click="edit_assign(row.user)"></el-button>
          <el-dialog title="使用者表單-修改" :visible.sync="edit_lock">
            <el-form :model="form" label-width="80px">
              <el-form-item prop="user" label="使用者" required><el-input v-model="form.user" style="width:200px;"placeholder="請輸入使用者名稱"></el-input></el-form-item>
              <el-form-item prop="password" label="密碼" required><el-input v-model="form.password" style="width:200px;"placeholder="請輸入密碼"></el-input></el-form-item>
              <el-form-item prop="email" label="信箱" required><el-input v-model="form.email" style="width:300px;"placeholder="請輸入信箱"></el-input></el-form-item>
              <el-form-item prop="groups" label="群組" >
                <el-select v-model="form.groups" width="400px" multiple placeholder="請輸入群組">
                  <el-option v-for="item in groups_opt" :key="item.value" :label="item.label" :value="item.value"> </el-option>
                </el-select>
              </el-form-item>
              <el-form-item prop="region" label="區域" >
                <el-select v-model="form.region" width="400px" placeholder="請輸入區域">
                    <el-option v-for="item in region_opt" :key="item.value" :label="item.label" :value="item.value"> </el-option>
                </el-select>
              </el-form-item>
              <!--<el-form-item prop="record" label="紀錄" ><el-input v-model="form.record" style="width:600px;"placeholder="請輸入紀錄"></el-input></el-form-item>-->
              <el-form-item prop="description" label="描述" ><el-input v-model="form.description" style="width:600px;"placeholder="請輸入描述"></el-input></el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button type="danger" @click="edit_lock=false" plain>取消</el-button>
                <el-button type="primary" @click="edit_user" plain>確定</el-button>
            </div>
          </el-dialog>
          <el-button type="danger" icon="el-icon-delete" size="small" circle @click="delete_user(row.user)"></el-button>
          </template>
        </el-table-column>
      </el-table>
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
          tableData:[],
          all_Data:[],
          user_data:[],
          group_data:[],
          groups_opt:[],
          region_opt:[],
          form:{
              id:0,//edit才用的到
              user:'',
              password:'',
              email:'',
              groups:[],
              region:'',
              //record:'',
              description:'',
          },
          add_lock:false,
          edit_lock:false,
      };
    },
    created(){
      this.axios.get("/admin_user",{
        }).then((response)=>{
            this.all_Data = JSON.parse(JSON.stringify(response.data));//所有數據傳入all_Data
            this.user_data = JSON.parse(JSON.stringify(this.all_Data['user_data']))
            this.group_data = JSON.parse(JSON.stringify(this.all_Data['group_data']))
            this.region_data = JSON.parse(JSON.stringify(this.all_Data['region_data']))
            this.tableData = JSON.parse(JSON.stringify(this.user_data))

            var user = JSON.parse(sessionStorage.getItem('user'))//存入user帳密
            var user_id = 0;
            for(let user_compare of this.user_data)
             if(user_compare.user == user[0])
                user_id = user_compare.user_id;
            var operator_authority = new Set();
            for(let group of this.all_Data['group_data']){//若管理員群組有現在使用者 就給予修改權限
                if(group.members.indexOf(String(user_id)) != -1){
                  if(group.authority != '')
                    if(JSON.parse(group.authority)['operator'] != undefined && JSON.parse(group.authority)['operator'] != [])
                        for(let operator of JSON.parse(group.authority)['operator'])
                          operator_authority.add(operator)
                  }
            }
            if(!operator_authority.has('使用者權限'))
                this.$router.push({name: 'admin'});
            //-------------------以上為確認是否有進入user頁面的權限----------------//
            for (let region of this.region_data)
                this.region_opt.push({'value':region.name,'label':region.name})
            for (let group of this.group_data)
                this.groups_opt.push({'value':group.caption,'label':group.caption})

            for(let data of this.tableData){
              data['region'] = data['region'].replace('[', '').replace(']','').split(',');//處理region
              for(var i = 0;i < data['region'].length; i++)
                  if(data['region'][i] != '')
                    for(let reg of this.region_data)
                      if(reg['region_id'] == parseInt(data['region'][i]))
                        data['region'][i] = reg['name']
              data['region'] =  JSON.stringify(data['region'])
              data['region'] = data['region'].replace('["', '').replace('"]','').replace(/","/g,',')

              data['groups'] = data['groups'].replace('[', '').replace(']','').split(',');//處理group
              for(var i = 0;i < data['groups'].length; i++)
                  if(data['groups'][i] != '')
                    for(let group of this.group_data)
                      if(group['group_id'] == parseInt(data['groups'][i]))
                        data['groups'][i] = group['caption']
              data['groups'] =  JSON.stringify(data['groups'])
              data['groups'] = data['groups'].replace('["', '').replace('"]','').replace(/","/g,',')
            }
        });
    },
    methods: {
      edit_assign(user_name){//資訊帶入修改表單
        for(let user of this.tableData)
          if(user_name == user['user']){
              this.form.id = user['user_id'];
              this.form.user = user['user'];
              this.form.password = user['password'];
              this.form.email = user['email'];
              this.form.groups = user['groups'];
              this.form.region = user['region'];
              this.form.record = user['record'];
              this.form.description = user['description'];

              if(this.form.groups != '')
                  this.form.groups = JSON.parse(('["' + user['groups'] + '"]').replace(/,/g,'","'))
          }
          this.edit_lock = true;
      },
      add_user(){//送出新增表單
        if(this.form.user == '' || this.form.password == ''|| this.form.email == ''){
                this.$message({message: '請填入群組名稱及群組類別及信箱', type: 'error'});
                return;
            }
        if(this.form.email.split('@')[1] == undefined){
            this.$message({message:'請填入正確email格式', type:'error'});
            return;
        }
        for(let user of this.tableData){
                if(this.form.user == user['user']){
                   this.$message({message: '使用者 '+this.form.user+' 重複', type: 'error'});
                   return;
                }
            }
        this.form.groups = JSON.stringify(this.form.groups).replace('["','').replace('"]','').replace(/","/g,',')
        if(this.form.groups != '[]'){
            this.form.groups = this.form.groups.split(',');
            for(var i = 0; i < this.form.groups.length; i++){//將群組名稱轉成數字代號
                for(let group of this.group_data)
                    if(this.form.groups[i] == group['caption'])
                        this.form.groups[i] = group['group_id']
            }
            this.form.groups = JSON.stringify(this.form.groups);
        }
        else
          this.form.groups = '';
        if(this.form.region != ''){//將區域名稱轉成數字代號
          for(let region of this.region_data)
              if(this.form.region == region['name'])
                  this.form.region = region['region_id']
            this.form.region = '[' + JSON.stringify(this.form.region) + ']';
        }
        else
          this.form.region = '';

        this.axios.get("/operator_user",{
            params:{
                form: JSON.stringify(this.form),
                operator:'add'
            }
            }).then((response)=>{
                this.add_lock = false;
                this.form.id = 0;
                this.form.user = '';
                this.form.password = '';
                this.form.email = '';
                this.form.groups = [];
                this.form.region = '';
                this.form.record = '';
                this.form.description = '';
                location.reload();
            });
      },
      edit_user(){//送出修改表單
        if(this.form.user == '' || this.form.password == '' || this.form.email == ''){
          this.$message({message: '請填入使用者名稱及密碼及信箱', type: 'error'});
          return;
        }
        if(this.form.email.split('@')[1] == undefined){
            this.$message({message:'請填入正確email格式', type:'error'});
            return;
        }
        this.form.groups = JSON.stringify(this.form.groups).replace('["','').replace('"]','').replace(/","/g,',')
          if(this.form.groups != '[]'){
              this.form.groups = this.form.groups.split(',');
              for(var i = 0; i < this.form.groups.length; i++){//將群組名稱轉成數字代號
                  for(let group of this.group_data)
                      if(this.form.groups[i] == group['caption'])
                          this.form.groups[i] = group['group_id']
              }
              this.form.groups = JSON.stringify(this.form.groups);
          }
          else
            this.form.groups = '';
          if(this.form.region != ''){//將區域名稱轉成數字代號
            for(let region of this.region_data)
                if(this.form.region == region['name'])
                    this.form.region = region['region_id']
              this.form.region = '[' + JSON.stringify(this.form.region) + ']';
          }
          else
            this.form.region = '';

          this.axios.get("/operator_user",{
                params:{
                    form: JSON.stringify(this.form),
                    operator:'edit'
                }
                }).then((response)=>{
                    this.add_lock = false;
                    this.form.id = 0;
                    this.form.user = '';
                    this.form.password = '';
                    this.form.email = '';
                    this.form.groups = [];
                    this.form.region = '';
                    this.form.record = '';
                    this.form.description = '';
                    location.reload();
                });
      },
      delete_user(user_name){//刪除使用者
            this.$confirm('是否刪除「 ' + user_name +' 」群組?', '刪除', {
            confirmButtonText: '確定',
            cancelButtonText: '取消',
            type: 'warning'
            }).then(() => {
                this.axios.get("/operator_user",{
                params:{
                    user_name: JSON.stringify(user_name),
                    operator:'delete'
                }
                }).then((response)=>{
                    location.reload();
                });
                this.$message({
                    type: 'success',
                    message: '删除成功!'
                });
            }).catch(() => {
            this.$message({
                type: 'info',
                message: '已取消删除'
            });          
            });
        },
    },
    }
</script>