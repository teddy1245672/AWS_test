<style>

</style>

<template>
  <div>
    <el-container>
    <Aside></Aside>
    <el-container>
    <el-main>
      <el-button style="position:relative;right:480px;" type="primary" icon="el-icon-plus" plain @click="add_assign">新增</el-button>
      <el-dialog align="left" title="使用者表單-新增" :visible.sync="dialogVisible_add">
        <el-form :model="product_dialog" label-width="80px">
          <el-form-item prop="category_id" label="產品類別" required>
            <!--<el-input v-model="product_dialog.category_id" style="width:200px;"placeholder="請輸入產品類別"></el-input>-->
            <el-autocomplete v-model="product_dialog.category_id" :fetch-suggestions="querySearch_category_id" placeholder="請輸入產品類別" ></el-autocomplete>
          </el-form-item>
          <el-form-item prop="product_name" label="id" required>
          <el-input v-model="product_dialog.product_name" style="width:300px;"placeholder="請輸入id"></el-input>
          </el-form-item>
          <el-form-item prop="caption" label="產品名稱" required><el-input v-model="product_dialog.caption" style="width:300px;"placeholder="請輸入名稱"></el-input></el-form-item>
          <el-form-item prop="remarks" label="備註" ><el-input v-model="product_dialog.remarks" style="width:300px;"placeholder="請輸入備註"></el-input></el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
            <el-button type="danger" @click="dialogVisible_add=false" plain>取消</el-button>
            <el-button type="primary" @click="add_check" plain>確定</el-button>
        </div>
      </el-dialog>
      <el-autocomplete style="position:relative;left:400px;" v-model="sort_value" :fetch-suggestions="querySearch" placeholder="請輸入名稱" @input='category_filter'></el-autocomplete>
      <el-tabs style="width: 95%" type="card" v-model="TabsValue" @tab-click="tabClick">
        <el-tab-pane v-for="(item, index) in Tabs" :key="item.name" :label="item.label" :name="item.name" ></el-tab-pane>
        <el-table :data="tableData">
          <el-table-column prop="category_id" label="產品類別" width="100"></el-table-column>
          <el-table-column prop="product_name" label="id" width="250"></el-table-column>
          <el-table-column prop="caption" label="產品名稱" fit ></el-table-column>
          <el-table-column prop="remarks" label="備註" width="150"></el-table-column>
          <el-table-column prop="description" label="操作" width="100">
            <template slot-scope = "{row,$index}" >
              <el-button type="primary" icon="el-icon-edit" size="small" circle @click="edit_assign(row)"></el-button>
              <el-button type="danger" icon="el-icon-delete" size="small" circle @click="delete_product(row)"></el-button>
            <template>
          </el-table-column>
        </el-table>
      </el-tabs>
      <el-dialog align="left" title="使用者表單-修改" :visible.sync="dialogVisible_edit">
        <el-form :model="product_dialog" label-width="80px">
          <el-form-item prop="category_id" label="產品類別" required>
            <!--<el-input v-model="product_dialog.category_id" style="width:200px;"placeholder="請輸入產品類別"></el-input>-->
            <el-autocomplete v-model="product_dialog.category_id" :fetch-suggestions="querySearch_category_id" placeholder="請輸入產品類別" ></el-autocomplete>
          </el-form-item>
          <el-form-item prop="product_name" label="id" required>
          <el-input v-model="product_dialog.product_name" style="width:300px;"placeholder="請輸入id"></el-input>
          </el-form-item>
          <el-form-item prop="caption" label="產品名稱" required><el-input v-model="product_dialog.caption" style="width:300px;"placeholder="請輸入名稱"></el-input></el-form-item>
          <el-form-item prop="remarks" label="備註" ><el-input v-model="product_dialog.remarks" style="width:300px;"placeholder="請輸入備註"></el-input></el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
            <el-button type="danger" @click="dialogVisible_edit=false" plain>取消</el-button>
            <el-button type="primary" @click="edit_check()" plain>確定</el-button>
        </div>
      </el-dialog>
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
        product_data:[],
        option_data:[],
        origin_data:[],
        tab_data:[],
        info_data:[],
        TabsValue: '1',//default <all>
        Tabs: [{label: 'all',name: '1'},
          {label: 'ezCAM',name: '2'},
          {label: 'ezCAT',name: '3'},
          {label: 'ezTool',name: '4'},
          {label: 'Quote',name: '5'},
          {label: 'ezPlan',name: '6'},
          {label: 'ezDI',name: '7'},
          {label: 'Other',name: '8'},
          ],
          sort_value:'',
          caption_opt:[],
          dialogVisible_add:false,
          product_dialog:{
            product_id:0,
            category_id:'',
            product_name:'',
            caption:'',
            remarks:''
          },
          dialogVisible_edit:false,
          category_id_opt:[],
        };
    },
    created(){
      this.axios.get("/admin_product",{
        headers: {'Content-Encoding': 'gzip'}
        }).then((response)=>{
          this.all_Data = JSON.parse(JSON.stringify(response.data));//所有數據傳入all_Data
          this.product_data = JSON.parse(JSON.stringify(this.all_Data['product_data']))
          this.option_data = JSON.parse(JSON.stringify(this.all_Data['option_data']))
          this.info_data = JSON.parse(JSON.stringify(this.all_Data['info_data']))
          this.tableData = JSON.parse(JSON.stringify(this.all_Data['product_data']))
          
          this.origin_data = JSON.parse(JSON.stringify(this.tableData))
          this.tab_data = JSON.parse(JSON.stringify(this.tableData))
          //--------------製作建議選項-----------------//
          for(let data of this.tableData)
            this.caption_opt.push({value:data['caption'],label:data['caption']})

          var category_id_set = new Set()
          for(let data of this.tableData)
            category_id_set.add(data['category_id'])
          for(let data of category_id_set)
            this.category_id_opt.push({value:data,label:data})
        });
    },
    methods: {
      add_check(){//確認新增表單
        if(this.product_dialog['category_id'] == ''||this.product_dialog['product_name'] == ''||this.product_dialog['caption'] == ''){
            this.$message({type: 'error',message: '請填寫完整新增表單'});
            return
          }
        for(let product of this.product_data){
          if(product.product_id != this.product_dialog.product_id && product.caption == this.product_dialog.caption){
            this.$message({type: 'error',message: '產品名稱與其他資料重複'});
            return
          }
          if(product.product_id != this.product_dialog.product_id && product.product_name == this.product_dialog.product_name){
            this.$message({type: 'error',message: 'id與其他資料重複'});
            return
          }
        }
        this.$confirm('是否要新增{'+this.product_dialog['caption']+'}產品', '新增', {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
          type: 'warning'
          }).then(() => {
            this.axios.get("/operator_product",{
              params:{
                  data: JSON.stringify(this.product_dialog),
                  operator:'add'
              }
            }).then((response)=>{
                location.reload();
                this.$message({type: 'success',message: '新增成功!'});
            });
          }).catch(() => {
            this.$message({
                type: 'info',
                message: '已取消新增'
            });          
          });
      },
      add_assign(){//資訊帶入新增表單
        this.dialogVisible_add = true;
        this.product_dialog.product_id = 0
        this.product_dialog.category_id = ''
        this.product_dialog.product_name = ''
        this.product_dialog.caption = ''
        this.product_dialog.remarks = ''
      },
      edit_check(){//確認修改表單
        if(this.product_dialog['category_id'] == ''||this.product_dialog['product_name'] == ''||this.product_dialog['caption'] == ''){
            this.$message({type: 'error',message: '請填寫完整新增表單'});
            return
          }
        if(this.product_data[this.product_dialog.product_id - 1]['category_id'] == this.product_dialog.category_id&&
          this.product_data[this.product_dialog.product_id - 1]['product_name'] == this.product_dialog.product_name&&
          this.product_data[this.product_dialog.product_id - 1]['caption'] == this.product_dialog.caption&&
          this.product_data[this.product_dialog.product_id - 1]['remarks'] == this.product_dialog.remarks){
            this.$message({type: 'error',message: '未做任何修改，請修改後重新再試'});
            return
          }
        for(let product of this.product_data){
          if(product.product_id != this.product_dialog.product_id && product.caption == this.product_dialog.caption){
            this.$message({type: 'error',message: '產品名稱與其他資料重複'});
            return
          }
          if(product.product_id != this.product_dialog.product_id && product.product_name == this.product_dialog.product_name){
            this.$message({type: 'error',message: 'id與其他資料重複'});
            return
          }
        }
        if(this.product_data[this.product_dialog.product_id - 1]['caption'] != this.product_dialog.caption){
          this.$confirm(' 是否要將 {'+this.product_data[this.product_dialog.product_id - 1]['caption']+'} 改為 {'+this.product_dialog.caption+'}', '修改', {
            confirmButtonText: '確定',
            cancelButtonText: '取消',
            type: 'warning'
            }).then(() => {
              this.axios.get("/operator_product",{
                params:{
                    data: JSON.stringify(this.product_dialog),
                    operator:'edit'
                }
              }).then((response)=>{
                  location.reload();
                  this.$message({type: 'success',message: '修改成功!'});
              });
            }).catch(() => {
              this.$message({
                  type: 'info',
                  message: '已取消修改'
              });          
            });
        }
        else{
          this.axios.get("/operator_product",{
            params:{
                data: JSON.stringify(this.product_dialog),
                operator:'edit'
            }
          }).then((response)=>{
              location.reload();
              this.$message({type: 'success',message: '修改成功!'});
          });
        }
      },
      edit_assign(row){//資訊帶入修改表單
        this.dialogVisible_edit = true
        this.product_dialog.product_id = row.product_id
        this.product_dialog.category_id = row.category_id
        this.product_dialog.product_name = row.product_name
        this.product_dialog.caption = row.caption
        this.product_dialog.remarks = row.remarks
      },

      delete_product(row){//刪除產品
        this.$confirm('是否刪除「 ' + row['caption'] +' 」?', '刪除', {
        confirmButtonText: '確定',
        cancelButtonText: '取消',
        type: 'warning'
        }).then(() => {
          for(let info of this.info_data)
            if(row['product_name'] == info['func_uid']){
              this.$message({type: 'error',message: '當前資料還有此產品資料, 不允許刪除'});          
              return
            }
          for(let option of this.option_data)
            if(row['product_name'] == option['product_name']){
              this.$message({type: 'error',message: '此產品下尚有option功能, 不允許刪除'});          
              return
            }
          this.axios.get("/operator_product",{
            params:{
                data: JSON.stringify(row),
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
      tabClick(tab, event) {//tab分類
        this.sort_value = ''
        if(tab.label == 'all'){
          this.tableData = JSON.parse(JSON.stringify(this.origin_data));
          this.tab_data = JSON.parse(JSON.stringify(this.origin_data));
        }
        else if(tab.label == 'Other'){
          this.tableData = JSON.parse(JSON.stringify(this.origin_data));
          var category_id_set = new Set()
          for(let data of this.Tabs)
            if(data['label'] != 'Other')
              category_id_set.add(data['label'])
          for(let i = 0; i < this.tableData.length; i++)
            if(category_id_set.has(this.tableData[i]['category_id'])){
              this.tableData.splice(i,1);
              i--;
            }
          this.tab_data = JSON.parse(JSON.stringify(this.origin_data));
        }
        else{//如果是all就顯示原tableData
          this.tableData = JSON.parse(JSON.stringify(this.origin_data));
          for(let i = 0; i <  this.tableData.length; i++){
            if(this.tableData[i]['category_id'] != tab.label){
              this.tableData.splice(i,1);
              i--;
            }
          }
          this.tab_data = JSON.parse(JSON.stringify(this.tableData));
        }
      },
      category_filter: function(){//對product分頁底下的tableData做過濾
        this.tableData = JSON.parse(JSON.stringify(this.tab_data));
        if(this.sort_value != ''){
          for(let i = 0; i < this.tableData.length; i++){
            if(this.tableData[i]['caption'].indexOf(this.sort_value) == -1){
              this.tableData.splice(i,1);
              i--;
            }
          }
        }
      },
      querySearch(queryString, cb) {
        var results = queryString ? this.caption_opt.filter(this.createFilter(queryString)) : this.caption_opt;
        cb(results); // 調用 callback 返回建議列表的數據
      },
      querySearch_category_id(queryString, cb) {
        var results = queryString ? this.category_id_opt.filter(this.createFilter(queryString)) : this.category_id_opt;
        cb(results); // 調用 callback 返回建議列表的數據
      },
      createFilter(queryString) {//搜尋建議選項
          return (any) => {
            //return (any.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);原本
            return (String(any.value).toLowerCase().indexOf(String(queryString).toLowerCase()) != -1);
          };
        },
    },
    }
</script>