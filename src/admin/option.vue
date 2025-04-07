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
        <el-form :model="option_dialog" label-width="80px">
          <el-form-item prop="product_name" label="產品id" required>
            <!--<el-input v-model="option_dialog.product_name" style="width:300px;"placeholder="請輸入產品id"></el-input>-->
            <el-select v-model="option_dialog.product_name" placeholder="請選擇產品id">
              <el-option v-for="item in product_name_opt" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
           <el-form-item prop="option_name" label="選項id" required>
            <el-input v-model="option_dialog.option_name" style="width:300px;"placeholder="請輸入選項id"></el-input>
          </el-form-item>
          <el-form-item prop="caption" label="選項名稱" required><el-input v-model="option_dialog.caption" style="width:300px;"placeholder="請輸入名稱"></el-input></el-form-item>
          <el-form-item prop="remarks" label="備註" ><el-input v-model="option_dialog.remarks" style="width:300px;"placeholder="請輸入備註"></el-input></el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
            <el-button type="danger" @click="dialogVisible_add=false" plain>取消</el-button>
            <el-button type="primary" @click="add_check" plain>確定</el-button>
        </div>
      </el-dialog>
      <el-autocomplete style="position:relative;left:400px;" v-model="sort_value" :fetch-suggestions="querySearch" placeholder="請輸入選項名稱" @input='category_filter'></el-autocomplete>
      <el-tabs style="width: 95%" type="card" v-model="TabsValue" @tab-click="tabClick">
        <el-tab-pane v-for="(item, index) in Tabs" :key="item.name" :label="item.label" :name="item.name" ></el-tab-pane>
        <el-table :data="tableData">
          <el-table-column prop="category_id" label="選項類別" width="100"></el-table-column>
          <el-table-column prop="product_name" label="產品id" width="150"></el-table-column>
          <el-table-column prop="option_name" label="選項id" width="250"></el-table-column>
          <el-table-column prop="caption" label="選項名稱" width="200" ></el-table-column>
          <el-table-column prop="remarks" label="備註" fit></el-table-column>
          <el-table-column prop="description" label="操作" width="100">
            <template slot-scope = "{row,$index}" >
              <el-button type="primary" icon="el-icon-edit" size="small" circle @click="edit_assign(row)"></el-button>
              <el-button type="danger" icon="el-icon-delete" size="small" circle @click="delete_option(row)"></el-button>
            <template>
          </el-table-column>
        </el-table>
      </el-tabs>
      <el-dialog align="left" title="使用者表單-修改" :visible.sync="dialogVisible_edit">
        <el-form :model="option_dialog" label-width="80px">
          <el-form-item prop="category_id" label="產品類別" required>
            <span>{{option_dialog.category_id}}</span>
          </el-form-item>
          <el-form-item prop="product_name" label="產品id" required>
            <!--<el-input v-model="option_dialog.product_name" style="width:300px;"placeholder="請輸入產品id"></el-input>-->
            <el-select v-model="option_dialog.product_name" placeholder="請選擇產品id">
              <el-option v-for="item in product_name_opt" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
           <el-form-item prop="option_name" label="選項id" required>
            <el-input v-model="option_dialog.option_name" style="width:300px;"placeholder="請輸入選項id"></el-input>
          </el-form-item>
          <el-form-item prop="caption" label="選項名稱" required><el-input v-model="option_dialog.caption" style="width:300px;"placeholder="請輸入名稱"></el-input></el-form-item>
          <el-form-item prop="remarks" label="備註" ><el-input v-model="option_dialog.remarks" style="width:300px;"placeholder="請輸入備註"></el-input></el-form-item>
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
          option_dialog:{
            option_id:0,
            category_id:'',
            product_name:'',
            option_name:'',
            caption:'',
            remarks:''
          },
          dialogVisible_edit:false,
          product_name_opt:[],
        };
    },
    created(){
      this.axios.get("/admin_option",{
        headers: {'Content-Encoding': 'gzip'}
        }).then((response)=>{
            this.all_Data = JSON.parse(JSON.stringify(response.data));//所有數據傳入all_Data
            this.product_data = JSON.parse(JSON.stringify(this.all_Data['product_data']))
            this.option_data = JSON.parse(JSON.stringify(this.all_Data['option_data']))
            this.info_data = JSON.parse(JSON.stringify(this.all_Data['info_data']))
            this.tableData = JSON.parse(JSON.stringify(this.all_Data['option_data']))

            this.origin_data = JSON.parse(JSON.stringify(this.tableData))
            this.tab_data = JSON.parse(JSON.stringify(this.tableData))
            //--------------製作建議選項-----------------//
            var caption_set = new Set()
            for(let data of this.tableData)
                caption_set.add(data['caption'])
            for(let caption of caption_set)
                this.caption_opt.push({value:caption,label:caption})
            for(let pro of this.product_data)
              this.product_name_opt.push({value:pro.product_name,label:pro.product_name})
        });
    },
    methods: {
      add_check(){//確認送出表單
        if(this.option_dialog['option_name'] == ''||this.option_dialog['product_name'] == ''||this.option_dialog['caption'] == ''){
            this.$message({type: 'error',message: '請填寫完整新增表單'});
            return
          }
        for(let option of this.option_data){
          if(option.option_id != this.option_dialog.option_id && option.caption == this.option_dialog.caption){
            this.$message({type: 'error',message: '選項名稱與其他資料重複'});
            return
          }
          if(option.option_id != this.option_dialog.option_id && option.option_name == this.option_dialog.option_name){
            this.$message({type: 'error',message: '選項id與其他資料重複'});
            return
          }
        }
        this.$confirm('是否要新增{'+this.option_dialog['caption']+'}產品', '新增', {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
          type: 'warning'
          }).then(() => {
            this.axios.get("/operator_option",{
              params:{
                  data: JSON.stringify(this.option_dialog),
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
        this.dialogVisible_add = true
        this.option_dialog.option_id = 0
        this.option_dialog.category_id = ''
        this.option_dialog.product_name = ''
        this.option_dialog.option_name = ''
        this.option_dialog.caption = ''
        this.option_dialog.remarks = ''
      },
      edit_check(){//確認送出修改表單
        if(this.option_dialog['product_name'] == ''||this.option_dialog['option_name'] == ''||this.option_dialog['caption'] == ''){
            this.$message({type: 'error',message: '請填寫完整新增表單'});
            return
          }
        if(this.option_data[this.option_dialog.option_id - 1]['product_name'] == this.option_dialog.product_name&&
          this.option_data[this.option_dialog.option_id - 1]['option_name'] == this.option_dialog.option_name&&
          this.option_data[this.option_dialog.option_id - 1]['caption'] == this.option_dialog.caption&&
          this.option_data[this.option_dialog.option_id - 1]['remarks'] == this.option_dialog.remarks){
            this.$message({type: 'error',message: '未做任何修改，清修改後重新再試'});
            return
          }
        for(let option of this.option_data){
          if(option.option_id != this.option_dialog.option_id && option.caption == this.option_dialog.caption){
            this.$message({type: 'error',message: '選項名稱與其他資料重複'});
            return
          }
          if(option.option_id != this.option_dialog.option_id && option.option_name == this.option_dialog.option_name){
            this.$message({type: 'error',message: '選項id與其他資料重複'});
            return
          }
        }
        if(this.option_data[this.option_dialog.option_id - 1]['caption'] != this.option_dialog.caption){
          this.$confirm(' 是否要將 {'+this.option_data[this.option_dialog.option_id - 1]['caption']+'} 改為 {'+this.option_dialog.caption+'}', '修改', {
            confirmButtonText: '確定',
            cancelButtonText: '取消',
            type: 'warning'
            }).then(() => {
              this.axios.get("/operator_option",{
                params:{
                    data: JSON.stringify(this.option_dialog),
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
          this.axios.get("/operator_option",{
            params:{
                data: JSON.stringify(this.option_dialog),
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
        this.option_dialog.option_id = row.option_id
        this.option_dialog.category_id = row.category_id
        this.option_dialog.product_name = row.product_name
        this.option_dialog.option_name = row.option_name
        this.option_dialog.caption = row.caption
        this.option_dialog.remarks = row.remarks
      },
      delete_option(row){//確認刪除選項
        this.$confirm('是否刪除「 ' + row['caption'] +' 」?', '刪除', {
            confirmButtonText: '確定',
            cancelButtonText: '取消',
            type: 'warning'
        }).then(() => {
          for(let info of this.info_data)
            if(row['option_name'] == info['func_uid']){
              this.$message({type: 'error',message: '當前資料還有此選項資料, 不允許刪除'});          
              return
            }
          this.axios.get("/operator_option",{
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
      tabClick(tab, event) {//當點擊標籤頁時1
        this.sort_value = ''
        if(tab.label != 'all'){
          this.tableData = JSON.parse(JSON.stringify(this.origin_data));
          for(let i = 0; i <  this.tableData.length; i++){
            if(this.tableData[i]['category_id'] != tab.label){
              this.tableData.splice(i,1);
              i--;
            }
          }
          this.tab_data = JSON.parse(JSON.stringify(this.tableData));
        }
        else{//如果是all就顯示原tableData
          this.tableData = JSON.parse(JSON.stringify(this.origin_data));
          this.tab_data = JSON.parse(JSON.stringify(this.origin_data));
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
      createFilter(queryString) {//搜尋建議選項
          return (any) => {
            //return (any.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);原本
            return (String(any.value).toLowerCase().indexOf(String(queryString).toLowerCase()) != -1);
          };
        },
    },
    }
</script>