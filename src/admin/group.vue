<style>

</style>

<template>
  <div>
    <el-container>
    <Aside></Aside>
    <el-container>
    <el-main>
        <div align="left"><!--新增-->
            <el-button type="primary" icon="el-icon-plus" plain @click="form.id=0,form.name='',form.caption='',form.authority='',form.description='',form.members='',form.members_arr=[],form.region_authority=[],form.product_authority=[],add_lock = true">新增</el-button>
            <el-dialog title="群組表單-新增" :visible.sync="add_lock">
                <el-form :model="form" label-width="120px">
                    <el-form-item prop="name" label="群組名稱" required><el-input v-model="form.name" style="width:200px;"placeholder="請輸入群組名稱"></el-input></el-form-item>
                    <el-form-item prop="caption" label="群組類別" required><el-input v-model="form.caption" style="width:200px;"placeholder="請輸入群組類別"></el-input></el-form-item>
                    <el-form-item prop="region_authority" label="區域權限" >
                        <el-select v-model="form.region_authority" width="200px" multiple placeholder="請輸入區域權限">
                            <el-option v-for="item in region_opt" :key="item.value" :label="item.label" :value="item.value"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item prop="product_authority" label="產品權限" >
                        <el-select v-model="form.product_authority" width="200px" multiple placeholder="請輸入產品權限">
                            <el-option v-for="item in product_opt" :key="item.value" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item prop="operator_authority" label="功能權限" >
                        <el-select v-model="form.operator_authority" width="200px" multiple placeholder="請輸入功能權限">
                            <el-option v-for="item in operator_opt" :key="item.value" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item prop="description" label="描述" ><el-input v-model="form.description" width="200px"placeholder="請輸入描述"></el-input></el-form-item>
                    <el-form-item prop="members" label="成員" >
                        <el-select v-model="form.members_arr" width="400px" multiple placeholder="請輸入成員">
                            <el-option v-for="item in user_opt" :key="item.value" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button type="danger" @click="add_lock=false" plain>取消</el-button>
                    <el-button type="primary" @click="add_group" plain>確定</el-button>
                </div>
            </el-dialog>
        </div>
        <el-table :data="tableData" ><!--table-->
            <el-table-column align="center" prop="name" label="id" width="200"></el-table-column>
            <el-table-column align="center" prop="caption" label="群組名稱" width="100"></el-table-column>
            <el-table-column align="center" prop="authority" label="權限" width="200">
                <template slot-scope = "{row,$index}" >
                <el-popover ref="popover" placement="bottom-start" title="權限" trigger="hover" placement="top">
                    <span style="font-size:15px;color:black;">區域權限:</span>
                    <span>{{region_authority}}<br></span>
                    <span style="font-size:15px;color:black;">產品權限:</span>
                    <span>{{product_authority}}<br></span>
                    <span style="font-size:15px;color:black;">功能權限:</span>
                    <span>{{operator_authority}}<br></span>
                    <el-button type="info" slot="reference" icon="el-icon-s-check"@mouseenter.native="authority_all(row,$index)" v-show="row.authority != ''" circle></el-button>
                </el-popover>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="members" label="成員" width="200">
                <template slot-scope = "{row,$index}" >
                <el-popover ref="popover1" placement="top-start" title="成員"trigger="hover" placement="top">
                    <span>{{row.members}}</span>
                    <el-button type="info" icon = "el-icon-s-custom" slot="reference" v-show="row.members != ''" circle></el-button>
                </el-popover>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="description" label="描述" width="200"></el-table-column>
            <el-table-column align="center" prop="description" label="操作" width="120">
                <template slot-scope = "{row,$index}" >
                <el-button type="primary" icon="el-icon-edit" size="small" circle @click="edit_assign(row.name)"></el-button>
                    <el-dialog align="left" title="群組表單-修改" :visible.sync="edit_lock">
                        <el-form :model="form" label-width="120px">
                            <el-form-item prop="name" label="群組名稱(必填)" required><el-input v-model="form.name" style="width:200px;"placeholder="請輸入群組名稱"></el-input></el-form-item>
                            <el-form-item prop="caption" label="群組類別(必填)" required><el-input v-model="form.caption" style="width:200px;"placeholder="請輸入群組類別"></el-input></el-form-item>
                            <el-form-item prop="region_authority" label="區域權限" >
                                <el-select v-model="form.region_authority" width="200px" multiple placeholder="請輸入區域權限">
                                    <el-option v-for="item in region_opt" :key="item.value" :label="item.label" :value="item.value"> </el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item prop="product_authority" label="產品權限" >
                                <el-select v-model="form.product_authority" width="200px" multiple placeholder="請輸入產品權限">
                                    <el-option v-for="item in product_opt" :key="item.value" :label="item.label" :value="item.value"> </el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item prop="operator_authority" label="功能權限" >
                                <el-select v-model="form.operator_authority" width="200px" multiple placeholder="請輸入功能權限">
                                    <el-option v-for="item in operator_opt" :key="item.value" :label="item.label" :value="item.value"> </el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item prop="description" label="描述" ><el-input v-model="form.description" width="200px"placeholder="請輸入描述"></el-input></el-form-item>
                            <el-form-item prop="members" label="成員(可複選)" >
                                <el-select v-model="form.members_arr" width="400px" multiple placeholder="請輸入">
                                    <el-option v-for="item in user_opt" :key="item.value" :label="item.label" :value="item.value"> </el-option>
                                </el-select>
                            </el-form-item>
                        </el-form>
                        <div slot="footer" class="dialog-footer">
                            <el-button type="danger" @click="edit_lock=false" plain>取消</el-button>
                            <el-button type="primary" @click="edit_group" plain>確定</el-button>
                        </div>
                    </el-dialog>
                  <el-button type="danger" icon="el-icon-delete" circle size="small" @click="delete_group(row.name)"></el-button>
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
          region_authority:'',
          product_authority:'',
          operator_authority:'',
          add_lock:false,
          edit_lock:false,
          form:{
              id:0,//edit才用的到
              name:'',
              caption:'',
              authority:'',
              region_authority:[],
              product_authority:[],
              operator_authority:[],
              description:'',
              members:'',
              members_arr:[]
          },
          user_opt:[],
          region_opt:[],
          product_opt:[],
          operator_opt:[{'value':'下載權限','label':'下載權限'},{'value':'使用者權限','label':'使用者權限'},
          {'value':'產品權限','label':'產品權限'},{'value':'區域權限','label':'區域權限'}],
      };
    },
    created(){
      this.axios.get("/admin_user",{
        }).then((response)=>{
            this.all_Data = JSON.parse(JSON.stringify(response.data));//所有數據傳入all_Data
            this.user_data = JSON.parse(JSON.stringify(this.all_Data['user_data']))
            this.group_data = JSON.parse(JSON.stringify(this.all_Data['group_data']))
            this.region_data = JSON.parse(JSON.stringify(this.all_Data['region_data']))
            this.product_data = JSON.parse(JSON.stringify(this.all_Data['product_data']))
            this.tableData = JSON.parse(JSON.stringify(this.group_data))

            var user = JSON.parse(sessionStorage.getItem('user'))//存入user帳密
            var user_id = 0;
            for(let user_compare of this.user_data)
             if(user_compare.user == user[0])
                user_id = user_compare.user_id;
            var operator_authority = new Set();
            console.log(this.all_Data['group_data'])
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
            //---------------以上為判斷是否有權限進入group頁面-------------------//
            for (let user of this.user_data)
                this.user_opt.push({'value':user.user,'label':user.user})
            for (let region of this.region_data)
                this.region_opt.push({'value':region.name,'label':region.name})

            var product_set = new Set();
            for (let product of this.product_data)//過濾多餘的category_id
                product_set.add(product.category_id)
            for(let product of product_set)
                this.product_opt.push({'value':product,'label':product})

            for(let data of this.tableData){
                data['members'] = data['members'].replace('[', '').replace(']','').split(',');
                for(var i = 0;i < data['members'].length; i++)
                    if(data['members'][i] != '')
                        for(let user of this.user_data)
                            if(parseInt(data['members'][i]) == user['user_id'])
                                data['members'][i] = user['user']
                data['members'] =  JSON.stringify(data['members'])
                data['members'] = data['members'].replace('["', '').replace('"]','').replace(/","/g,',')
            }
        });
    },
    methods: {
        authority_all(row,index){//處理所顯示的權限
            this.region_authority = '';
            this.product_authority = '';
            this.operator_authority = '';
            for(let region_row of JSON.parse(row.authority)['region'])
                for(let region of this.region_data)
                    if(region_row == region['region_id']){//數字代號換成中文
                        this.region_authority += (region['name'] +',');
                    }

            for(let product_row of JSON.parse(row.authority)['product'])
                this.product_authority += (product_row + ',');

            for(let operator_row of JSON.parse(row.authority)['operator'])
                this.operator_authority += (operator_row + ',');

            this.region_authority = this.region_authority.slice(0,this.region_authority.length -1)
            this.product_authority = this.product_authority.slice(0,this.product_authority.length -1)
            this.operator_authority = this.operator_authority.slice(0,this.operator_authority.length -1)
        },
        add_group(){//確定新增群組
            if(this.form.name == '' || this.form.caption == ''){
                this.$message({message: '請填入群組名稱及群組類別', type: 'error'});
                return;
            }
            for(let group of this.tableData){
                if(this.form.name == group['name']){
                   this.$message({message: '群組名稱 '+this.form.name+' 重複', type: 'error'});
                   return;
                }
                if(this.form.name == group['name']){
                   this.$message({message: '群組類別 '+this.form.caption+' 重複', type: 'error'});
                   return;
                }
            }
            if(this.form.region_authority.length != 0 || this.form.product_authority.length != 0 || this.form.operator_authority.length){
                this.form.authority = '{"region":'+JSON.stringify(this.form.region_authority) + ',' +'"product":' + JSON.stringify(this.form.product_authority) + ','+'"operator":'+ JSON.stringify(this.form.operator_authority) +'}'
                this.form.authority = JSON.parse(this.form.authority)
                for (var i = 0; i < this.form.authority['region'].length; i++)//將authority[region]中文換成數字代號
                    for(let region of this.region_data)
                        if(this.form.authority['region'][i] == region['name']){
                            this.form.authority['region'][i] = region['region_id'];
                        }
                this.form.authority = JSON.stringify(this.form.authority)
            }
            else 
                this.form.authority = ''

            this.form.members = JSON.stringify(this.form.members_arr).replace('["','').replace('"]','').replace(/","/g,',')
            if(this.form.members != '[]'){
                this.form.members = this.form.members.split(',');
                for(var i = 0; i < this.form.members.length; i++){//將成員名稱轉成數字代號
                    for(let user of this.user_data)
                        if(this.form.members[i] == user['user'])
                            this.form.members[i] = user['user_id']
                }
                this.form.members = JSON.stringify(this.form.members);
            }
            else
                this.form.members = '';
            this.axios.get("/operator_group",{
                params:{
                    form: JSON.stringify(this.form),
                    operator:'add'
                }
                }).then((response)=>{
                    this.add_lock = false;
                    this.form.name = '';
                    this.form.caption = '';
                    this.form.authority = '';
                    this.form.region_authority = [];
                    this.form.product_authority = [];
                    this.form.operator_authority = [];
                    this.form.description = '';
                    this.form.members = '';
                    this.form.members_arr = '';
                    location.reload();
                });
        },
        edit_assign(group_name){//資訊帶入修改表單
            for(let group of this.tableData)
                if(group_name == group['name']){
                    console.log(group)
                    this.form.id = group['group_id']
                    this.form.name = group['name']
                    this.form.caption = group['caption']
                    this.form.authority = group['authority']
                    if(group['authority'] != ''){
                        this.form.region_authority = JSON.parse(group['authority'])['region']          
                        for (var i = 0; i < this.form.region_authority.length; i++)//將authority[region]數字代號換成中文
                            for(let region of this.region_data)
                                if(this.form.region_authority[i] == region['region_id']){
                                    this.form.region_authority[i] = region['name'];
                                }
                        this.form.product_authority = JSON.parse(group['authority'])['product']
                        this.form.operator_authority = JSON.parse(group['authority'])['operator']
                    }
                    else{
                        this.form.region_authority = []
                        this.form.product_authority = []
                        this.form.operator_authority = []
                    }
                    this.form.description = group['description']
                    this.form.members = group['members']//admin,claire
                    if(group['members'] != '')
                        this.form.members_arr = JSON.parse(('["' + group['members'] + '"]').replace(/,/g,'","'))
                    else
                        this.form.members_arr = [];
                }
                this.edit_lock = true;
        },
        edit_group(){//確認表單修改
            if(this.form.name == '' || this.form.caption == ''){
                this.$message({message: '請填入群組名稱及群組類別', type: 'error'});
                return;
            }
            if(this.form.region_authority.length != 0 || this.form.product_authority.length != 0){
                this.form.authority = '{"region":'+JSON.stringify(this.form.region_authority) + ',' +'"product":' + JSON.stringify(this.form.product_authority) + ','+'"operator":'+ JSON.stringify(this.form.operator_authority) +'}'
                this.form.authority = JSON.parse(this.form.authority)
                for (var i = 0; i < this.form.authority['region'].length; i++)//將authority[region]中文換成數字代號
                    for(let region of this.region_data)
                        if(this.form.authority['region'][i] == region['name']){
                            this.form.authority['region'][i] = region['region_id'];
                        }
                this.form.authority = JSON.stringify(this.form.authority)
            }
            else 
                this.form.authority = ''
            this.form.members = JSON.stringify(this.form.members_arr).replace('["','').replace('"]','').replace(/","/g,',')
            
            if(this.form.members != '[]'){
                this.form.members = this.form.members.split(',');
                for(var i = 0; i < this.form.members.length; i++){//將成員名稱轉成數字代號
                    for(let user of this.user_data)
                        if(this.form.members[i] == user['user'])
                            this.form.members[i] = user['user_id']
                }
                this.form.members = JSON.stringify(this.form.members);
            }
            else
                this.form.members = '';
            this.axios.get("/operator_group",{
                params:{
                    form: JSON.stringify(this.form),
                    operator:'edit'
                }
                }).then((response)=>{
                    this.add_lock = false;
                    this.form.id = 0;
                    this.form.name = '';
                    this.form.caption = '';
                    this.form.authority = '';
                    this.form.prodcut_authority = [];
                    this.form.region_authority = [];
                    this.form.operator_authority = [];
                    this.form.description = '';
                    this.form.members = '';
                    this.form.members_arr = [];
                    location.reload();
                });
        },
        delete_group(group_name){//刪除群組
            this.$confirm('是否刪除「 ' +group_name+' 」群組?', '刪除', {
            confirmButtonText: '確定',
            cancelButtonText: '取消',
            type: 'warning'
            }).then(() => {
                this.axios.get("/operator_group",{
                params:{
                    group_name: JSON.stringify(group_name),
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