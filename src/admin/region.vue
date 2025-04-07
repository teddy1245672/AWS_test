<style>
.none_delete_tag .el-tag.el-tag--info .el-tag__close{
  display: none;
}
.el-select ::-webkit-scrollbar{
  display: none;
}
.el-scrollbar__wrap {
  overflow-x: hidden;
}
.el-select__tags{
    max-width:320px;
    max-height:100px;
    overflow-y: auto;
    overflow-x: hidden;
}
.custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
  }
.el-select ::-webkit-scrollbar{
    display: none;
}
</style>

<template>
  <div>
    <el-container>
    <Aside></Aside>
    <el-container>
    <el-main>
      <el-button style="position:relative;right:590px;" type="primary" icon="el-icon-plus" plain @click="add_assign">新增</el-button>
      <el-dialog align="left" title="使用者表單-新增" :visible.sync="dialogVisible_add">
        <el-form :model="region_dialog" label-width="80px">
          <el-form-item prop="name" label="地區" required>
            <el-input v-model="region_dialog.name" style="width:200px;"placeholder="請輸入地區"></el-input>
          </el-form-item>
          <el-form-item prop="description" label="描述" ><el-input v-model="region_dialog.description" style="width:300px;"placeholder="請輸入描述"></el-input></el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
            <el-button type="danger" @click="dialogVisible_add=false" plain>取消</el-button>
            <el-button type="primary" @click="add_region" plain>確定</el-button>
        </div>
      </el-dialog>
      <el-table :data="tableData">
        <el-table-column align="center" prop="region_id" label="編號" width="150"></el-table-column>
        <el-table-column align="center" prop="name" label="地區" width="200"></el-table-column>
        <el-table-column align="center" prop="description" label="描述" width="300"></el-table-column>
        <el-table-column align="center" prop="operator" label="操作" width="100">
        <template slot-scope = "{row,$index}">
          <el-button type="primary" icon="el-icon-edit" size="small" circle @click="edit_assign(row)"></el-button>
          <el-dialog align="left" title="使用者表單-修改" :visible.sync="dialogVisible_edit">
            <el-form :model="region_dialog" label-width="80px">
              <el-form-item prop="user" label="編號"><span>{{region_dialog.id}}</span></el-form-item>
              <el-form-item prop="name" label="地區" required>
                <el-input v-model="region_dialog.name" style="width:200px;"placeholder="請輸入地區"></el-input>
              </el-form-item>
              <el-form-item prop="description" label="描述" ><el-input v-model="region_dialog.description" style="width:300px;"placeholder="請輸入描述"></el-input></el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button type="danger" @click="dialogVisible_edit=false" plain>取消</el-button>
                <el-button type="primary" @click="edit_region" plain>確定</el-button>
            </div>
          </el-dialog>
          <el-button type="danger" icon="el-icon-delete" size="small" circle @click="delete_region(row)"></el-button>
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
        sn_data:[],
        customer_data:[],
        region_data:[],
        dialogVisible_edit:false,
        dialogVisible_add:false,
        region_dialog:{
          id:0,
          name:'',
          description:'',
        },
      };
    },
    created(){
      this.axios.get("/admin_region",{
        }).then((response)=>{
          this.all_Data = JSON.parse(JSON.stringify(response.data));//所有數據傳入all_Data
          this.customer_data = JSON.parse(JSON.stringify(this.all_Data['customer_data']))
          this.region_data = JSON.parse(JSON.stringify(this.all_Data['region_data']))
          this.sn_data = JSON.parse(JSON.stringify(this.all_Data['sn_data']))
          this.tableData = JSON.parse(JSON.stringify(this.all_Data['region_data']));
          //------------------------將產品換成caption----------------------------//
        });
    },
    methods: {
      delete_region(data){//刪除地區
        this.$confirm('是否刪除「 ' + data['name'] +' 」地區?', '刪除', {
        confirmButtonText: '確定',
        cancelButtonText: '取消',
        type: 'warning'
        }).then(() => {
          for(let sn of this.sn_data)
            if(sn['region'] == data['region_id'])
              return this.$message({type: 'error',message: '該地區已與Sn資料串聯，無法刪除，只可修改!'});
          this.axios.get("/operator_region",{
            params:{
                id: data['region_id'],
                operator:'delete'
            }
          }).then((response)=>{location.reload();});
          this.$message({type: 'success',message: '删除成功!'});
        }).catch(() => {
          this.$message({type: 'info',message: '已取消删除'});          
        });
      },
      edit_assign(row){//資訊帶入修改表單
        this.dialogVisible_edit = true;
        this.region_dialog.id = row['region_id']
        this.region_dialog.name = row['name']
        this.region_dialog.description = row['description']
      },
      edit_region(){//確認修改地區
        if(this.region_dialog.name == '')
          return this.$message({message: '請填入區域名稱', type: 'error'});
        for(let region of this.region_data)
          if(region.name == this.region_dialog.name){
            this.$message({message: '名稱與現有區域名稱重複', type: 'error'});
            return;
          }
        this.axios.get("/operator_region",{
          params:{
              region_dialog:JSON.stringify(this.region_dialog),
              operator:'edit'
          }
          }).then((response)=>{
            this.dialogVisible_edit = false;
            location.reload();
          });
      },
      add_assign(){//資訊帶入新增表單
        this.dialogVisible_add = true;
        this.region_dialog.id = 0
        this.region_dialog.name = ''
        this.region_dialog.description = ''
      },
      add_region(){//確認新增地區表單
        if(this.region_dialog.name == '')
          return this.$message({message: '請填入區域名稱', type: 'error'});
        for(let region of this.region_data)
          if(region.name == this.region_dialog.name){
            this.$message({message: '名稱與現有區域名稱重複', type: 'error'});
            return;
          }
        this.axios.get("/operator_region",{
          params:{
              region_dialog:JSON.stringify(this.region_dialog),
              operator:'add'
          }
          }).then((response)=>{
            this.dialogVisible_add = false;
            location.reload();
          });
      },
    },
  }
</script>