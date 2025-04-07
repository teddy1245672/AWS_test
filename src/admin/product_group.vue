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
      <el-dialog
        title="產品群組-新增"
        :visible.sync="dialogVisible_add"
        width="60%"
        :append-to-body="true"
        :show-close="false">
        <el-scrollbar style="height: 350px">
        <el-tree
            style="position:relative;left:440px;width:400px;height:350px;"
            :data="productgroup_tree"
            :props="defaultProps"
            accordion
            node-key="id"
            ref="product_group_tree"
            @check="choose_product_group"
            show-checkbox>
        <span class="custom-tree-node" slot-scope="{ node, data }">
            <span>{{ node.label }}</span>
            <span>
            <el-button
                v-show="data['add'] != true && deter_exist_group==false" size="mini"
                type="text"
                size="mini"
                @click="() => append(node, data)">
                加入此標籤
            </el-button>
            <el-button
                v-show="data['add'] == true"
                size="mini"
                type="text"
                size="mini"
                @click="() => remove(node, data)">
                重選標籤
            </el-button>
            <el-tag v-show="data['add'] == true" style="font-size:14px;height:22px;" type="success">G</el-tag>
            </span>
        </span>
        </el-tree>
        </el-scrollbar>
        <div style="position:absolute;top:80px">
        <div style="position:relative;">群組名稱:<el-input v-model="product_dialog.caption" style="width:150px"placeholder="請輸入群組名稱"></el-input></div>
        <div style="position:relative;">群組分類:<el-select class="none_delete_tag" ref="dialog_pro_tag" v-model="product_dialog.tag" filterable remote multiple style="width:300px;" @focus="make_blur('0')" placeholder="請輸入產品群組"></el-select></div>
        <div style="position:relative;">產品清單:<el-select class="none_delete_tag" ref="dialog_pro_group" v-model="product_dialog.product_list" filterable remote multiple style="width:300px;" @focus="make_blur('1')" placeholder="請輸入產品群組"></el-select></div>
        <div style="position:relative;">描述:<el-input v-model="product_dialog.description" style="width:200px" placeholder="請輸入描述"></el-input></div>
        <div style="position:relative;">備註:<el-input v-model="product_dialog.remarks" style="width:200px" placeholder="請輸入備註"></el-input></div>
        <span>
            <el-button style="position:relative;left:30px;"type="danger" @click="cancel_product_group('add')" plain>取消</el-button>
            <el-button style="position:relative;left:40px;"type="primary" @click="store_product_group('add')" plain>確定</el-button>
        </span>
        <div>
      </el-dialog>
      <el-table :data="tableData">
        <el-table-column align="center" prop="caption" label="群組名稱" width="150"></el-table-column>
        <el-table-column align="center" prop="tag" label="群組分類" width="300">
          <template slot-scope = "{row,$index}" >
            <span v-for="(item, index) in JSON.parse(row.tag)">
              {{item}}
              <span v-if="index != JSON.parse(row.tag).length-1">→</span>
            </span>
          </template>
        </el-table-column>
        <el-table-column align="center" prop="product_list" label="產品清單" width="150">
          <template slot-scope = "{row,$index}" >
            <el-popover ref="popover" placement="bottom-start" title="產品清單" trigger="hover" placement="top">
                <span v-for="item in JSON.parse(row.product_list)">{{item}}<br></span>
                <el-button style="font-size:20px;"type="text" slot="reference" icon="el-icon-box"></el-button>
            </el-popover>
          </template>
        </el-table-column>
        <el-table-column align="center" prop="description" label="描述" width="200"></el-table-column>
        <el-table-column align="center" prop="remarks" label="備註" width="200"></el-table-column>
        <el-table-column align="center" prop="operator" label="操作" width="150">
          <template slot-scope = "{row,$index}" >
          <el-button type="primary" icon="el-icon-edit" size="small" circle @click="edit_assign(row.caption)"></el-button>
          <el-dialog
                title="產品群組-修改"
                :visible.sync="dialogVisible_edit"
                width="60%"
                :append-to-body="true"
                :show-close="false">
                <el-scrollbar style="height: 350px">
                <el-tree
                    style="position:relative;left:440px;width:400px;height:350px;"
                    :data="productgroup_tree"
                    :props="defaultProps"
                    accordion
                    node-key="id"
                    ref="product_group_tree"
                    @check="choose_product_group"
                    show-checkbox>
                <span class="custom-tree-node" slot-scope="{ node, data }">
                    <span>{{ node.label }}</span>
                    <span>
                    <el-button
                        v-show="data['add'] != true && deter_exist_group==false" size="mini"
                        type="text"
                        size="mini"
                        @click="() => append(node, data)">
                        加入此標籤
                    </el-button>
                    <el-button
                        v-show="data['add'] == true"
                        size="mini"
                        type="text"
                        size="mini"
                        @click="() => remove(node, data)">
                        重選標籤
                    </el-button>
                    <el-tag v-show="data['add'] == true" style="font-size:14px;height:22px;" type="success">G</el-tag>
                    </span>
                </span>
                </el-tree>
                </el-scrollbar>
                <div style="position:absolute;top:80px">
                <div style="position:relative;">群組名稱:<el-input v-model="product_dialog.caption" style="width:150px"placeholder="請輸入群組名稱"></el-input></div>
                <div style="position:relative;">群組分類:<el-select class="none_delete_tag" ref="dialog_pro_tag" v-model="product_dialog.tag" filterable remote multiple style="width:300px;" @focus="make_blur('0')" placeholder="請輸入產品群組"></el-select></div>
                <div style="position:relative;">產品清單:<el-select class="none_delete_tag" ref="dialog_pro_group" v-model="product_dialog.product_list" filterable remote multiple style="width:300px;" @focus="make_blur('1')" placeholder="請輸入產品群組"></el-select></div>
                <div style="position:relative;">描述:<el-input v-model="product_dialog.description" style="width:200px" placeholder="請輸入描述"></el-input></div>
                <div style="position:relative;">備註:<el-input v-model="product_dialog.remarks" style="width:200px" placeholder="請輸入備註"></el-input></div>
                <span>
                    <el-button style="position:relative;left:30px;"type="danger" @click="cancel_product_group('edit')" plain>取消</el-button>
                    <el-button style="position:relative;left:40px;"type="primary" @click="store_product_group('edit')" plain>確定</el-button>
                </span>
                <div>
            </el-dialog>
          <el-button type="danger" icon="el-icon-delete" size="small" circle @click="delete_product_group(row.caption)"></el-button>
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
        option_data:[],
        product_data:[],
        product_group_data:[],
        user_data:[],
        dialogVisible_edit:false,
        dialogVisible_add:false,
        product_dialog:{
          id:0,
          caption:'',
          tag:[],
          product_list:[],
          description:'',
          remarks:'',
          product_list_detail:[]
        },
        productgroup_tree:[],
        productgroup_tree_origin:[],
        tree_node_count:0,
        child_node_map:new Map(),
        caption_map:new Map(),
        deter_exist_group:false
      };
    },
    created(){
      this.axios.get("/admin_product_group",{
        }).then((response)=>{
          this.all_Data = JSON.parse(JSON.stringify(response.data));//所有數據傳入all_Data
          this.user_data = JSON.parse(JSON.stringify(this.all_Data['user_data']))
          this.product_data = JSON.parse(JSON.stringify(this.all_Data['product_data']))
          this.option_data = JSON.parse(JSON.stringify(this.all_Data['option_data']))
          this.product_group_data = JSON.parse(JSON.stringify(this.all_Data['product_group_data']))
          //------------------------將產品換成caption----------------------------//
          for(let opt of this.option_data)
            this.caption_map.set(opt.option_name,{'caption':opt.caption,'product_name':opt.product_name})
          for(let pro of this.product_data)
            this.caption_map.set(pro.product_name,{'caption':pro.caption})
          var temp_pro_list = []
          for(let i = 0;i < this.product_group_data.length; i++){
            temp_pro_list = []
            for(let pro of JSON.parse(this.product_group_data[i]['product_list'])){
              if(this.caption_map.get(pro)['product_name'] != undefined)
                temp_pro_list.push(this.caption_map.get(pro)['caption']+'('+this.caption_map.get(pro)['product_name']+')')
              else
                temp_pro_list.push(this.caption_map.get(pro)['caption'])
            }
            this.product_group_data[i]['product_list'] = JSON.stringify(temp_pro_list)
          }
          this.tableData = JSON.parse(JSON.stringify(this.product_group_data))
          console.log(this.all_Data)
          //-----------------------將產品tree建構出來-----------------------------------------//
          var captionSet = new Set();
          for(let caption of this.all_Data['product_data'])
              captionSet.add(caption['category_id'])
          for(let caption of captionSet){
              this.productgroup_tree.push({'id':this.tree_node_count,'label':caption,'children':[]})
              this.tree_node_count++;
          }
          for(let product of this.all_Data['product_data'])
              for(let i = 0;i < this.productgroup_tree.length; i++)
                  if(this.productgroup_tree[i]['label'] == product['category_id']){
                    this.productgroup_tree[i]['children'].push({'id':this.tree_node_count,'label':product['caption'],'children':[],'category':product['category_id']})
                    this.tree_node_count++;
                  }

          for(let i = 0; i < this.productgroup_tree.length; i++)
              for(let j = 0; j < this.productgroup_tree[i]['children'].length; j++)
                  for(let product of this.all_Data['product_data'])
                      if(this.productgroup_tree[i]['children'][j]['label'] == product['caption'])
                          for(let option of this.all_Data['option_data'])
                              if(product['product_name'] == option['product_name']){
                                  this.productgroup_tree[i]['children'][j]['children'].push({'id':this.tree_node_count,'label':option['caption'],'product_name':option['product_name'],'children':[],'category':option['product_name']})
                                  this.tree_node_count++;
                              }
          this.productgroup_tree_origin = JSON.parse(JSON.stringify(this.productgroup_tree))
          //------------------------children對應id的Map--------------------------------//
          for(let node of this.productgroup_tree){
            if(node['children'].length == 0){
                this.child_node_map.set(node.label,node.id)
                continue
            }
            for(let node_c of node['children']){
                if(node_c['children'].length == 0){
                  this.child_node_map.set(node_c.label,node_c.id)
                  continue
                }
              for(let node_c_c of node_c['children']){
                if(node_c_c['children'].length == 0){
                  if(node_c_c['product_name'] != undefined)
                    this.child_node_map.set(node_c_c.label+'('+node_c_c['product_name']+')',node_c_c.id)
                  else
                    this.child_node_map.set(node_c_c.label,node_c_c.id)
                  continue
                }
              }
            }
          }
        });
    },
    methods: {
      choose_product_group(data,checked){//選擇product_group_tree時 同步帶入產品群組新增表單 
        var temp_product_list = []
        var temp_product_list_detail = []
        for(let product of this.$refs.product_group_tree.getCheckedNodes())
            if(product['children'].length == 0){
              if(product['product_name']!=undefined){
                temp_product_list.push(product['label']+'('+product['product_name']+')')
                temp_product_list_detail.push({'label':product['label'],'category':product['category']})
              }
              else{
                temp_product_list.push(product['label'])
                temp_product_list_detail.push({'label':product['label'],'category':product['category']})
              }

            }
        this.product_dialog.product_list = temp_product_list
        this.product_dialog.product_list_detail = temp_product_list_detail
        console.log(this.product_dialog.product_list_detail)
      },
      add_assign(){//開啟新增表單並初始化product_dialog
        this.productgroup_tree = JSON.parse(JSON.stringify(this.productgroup_tree_origin))//初始化產品群組tree
        this.dialogVisible_add = true;
        this.product_dialog.id = 0
        this.product_dialog.caption = ''
        this.product_dialog.tag = []
        this.product_dialog.product_list = []
        this.product_dialog.description = ''
        this.product_dialog.remarks = ''
        this.deter_exist_group = false;
      },
      edit_assign(group_name){//開啟edit_product_group_dialog 並帶入資訊
          this.productgroup_tree = JSON.parse(JSON.stringify(this.productgroup_tree_origin))//初始化產品群組tree
          for(let pro_gro of this.product_group_data){
            if(pro_gro['caption'] == group_name){
              this.product_dialog.id = pro_gro['group_id']
              this.product_dialog.caption = pro_gro['caption']
              this.product_dialog.tag = JSON.parse(pro_gro['tag'])
              this.product_dialog.product_list = JSON.parse(pro_gro['product_list'])
              this.product_dialog.description = pro_gro['description']
              this.product_dialog.remarks = pro_gro['remarks']
            }
          }
          this.dialogVisible_edit = true;
          //-----------原本的product_list進帶入tree中--------//
          console.log(this.child_node_map)
          var temp = []
          for(let pro of this.product_dialog.product_list)
            temp.push(this.child_node_map.get(pro))
          this.$nextTick(() => {
            this.$refs.product_group_tree.setCheckedKeys(temp)
          });
          //-----------------初始化product_dialog.product_list_detail 因store時需要用到---------------//
          this.$nextTick(() => {
            var temp_product_list_detail = []
            for(let product of this.$refs.product_group_tree.getCheckedNodes())
                if(product['children'].length == 0)
                    temp_product_list_detail.push({'label':product['label'],'category':product['category']})
                
            this.product_dialog.product_list_detail = temp_product_list_detail
          });

          for(let pro_group of this.product_group_data){
            if(pro_group['caption'] == group_name){//根據tag找到所對應的tree節點
              let temp = this.productgroup_tree;
              for(let tag of JSON.parse(pro_group.tag))
                  temp = temp[this.search_tree_index(temp,tag)]['children']

              temp.unshift({'id':this.tree_node_count++,'label':pro_group['caption'],'children':[],disabled: true,'add':true})
              this.deter_exist_group = true;
            }
          }
      },
      store_product_group(mode){
        var optionSet = new Set()
        for(let opt of this.all_Data['option_data'])
          optionSet.add(opt['product_name'])

        if (this.product_dialog.caption == '' || this.product_dialog.product_list.length == 0){
            this.$message.error('請將「產品群組」新增單，填寫完整');
            return
        }
        var temp = []
        for(let product of this.product_dialog.product_list_detail){//將caption換成product
            let test = 0
            let label_copy = product['label'].split('').reverse().join('').split('(') 
            if(optionSet.has(label_copy[0].replace(')','')))
                product['label'] = product['label'].replace('('+label_copy[0].replace(')','')+')','')
            for(let opt of this.all_Data['option_data'])
                if(product['label'] == opt['caption'] && product['category'] == opt['product_name']){
                    temp.push(opt['option_name'])
                    test = 1
                    break
                }
            if(test == 0)
                for(let pro of this.all_Data['product_data'])
                    if(product['label'] == pro['caption']){
                        temp.push(pro['product_name'])
                        break
                    }
        }

        for(let product_group of this.product_group_data){//防止產品群組名稱or產品 重複
            if(product_group['caption'] == this.product_dialog.caption){
              if(product_group['group_id'] != this.product_dialog.id){
                this.$message.error('產品名稱重複，請更改');
                return
              }
            }
            if(product_group.product_list == JSON.stringify(temp)){
              if(product_group['group_id'] != this.product_dialog.id){
                this.$message.error('群組內產品與其他群組完全重複');
                return
              }
            }
        }
        if(this.deter_exist_group == false){
            this.$message.error('請選擇群組群組分類');
            return
        }

        this.product_dialog.product_list = JSON.parse(JSON.stringify(temp));
        console.log(this.product_dialog)
        if(mode == 'add'){
          this.axios.get("/operator_product_group",{
            params:{
              product_dialog:JSON.stringify(this.product_dialog),
              operator:'add'
            }
          }).then((response)=>{
            location.reload();
          });
        }
        else if(mode == 'edit'){
          this.axios.get("/operator_product_group",{
            params:{
              product_dialog:JSON.stringify(this.product_dialog),
              operator:'edit'
            }
          }).then((response)=>{
            location.reload();
          });
        }
      },
      cancel_product_group(mode){//初始化產品群組Dialog
        this.product_dialog.caption = ''
        this.product_dialog.tag = []
        this.product_dialog.product_list = []
        this.product_dialog.description = ''
        this.product_dialog.remarks = ''
        this.product_dialog.product_list_detail = []//
        this.$nextTick(() => {this.$refs.product_group_tree.setCheckedKeys([])});//清空tree選擇
        if(mode == 'edit')
          this.dialogVisible_edit = false;
        else if(mode == 'add')
          this.dialogVisible_add = false;
      },
      append(node,data) {//新增群組節點
        if(this.product_dialog.caption == ''){
            this.$message.error('請填寫「群組名稱」，再選擇插入位置');
            return 
        }
        this.deter_exist_group = true;
        const newChild = {'label': this.product_dialog.caption, 'children': [], disabled:true,'add':true};
        if (!data.children) {
          this.$set(data, 'children', []);
        }
        data.children.unshift(newChild);
        var temp = node
        while(temp.label != undefined){
            this.product_dialog['tag'].unshift(temp.label)
            temp = temp.parent;
        }
      },
      remove(node, data) {//刪除新增產品群組
        this.deter_exist_group = false;
        this.tree_node_count--;
        this.product_dialog['tag'] = [];
        const parent = node.parent;
        const children = parent.data.children || parent.data;
        const index = children.findIndex(d => d.id === data.id);
        children.splice(index, 1);
      },
      make_blur(mode){//使el-select失焦
        if(mode == '0')
            this.$nextTick(()=>{this.$refs.dialog_pro_tag.blur();})
        if(mode == '1')
            this.$nextTick(()=>{this.$refs.dialog_pro_group.blur();})
        if(mode == '2')
            this.$nextTick(()=>{this.$refs.sub_row_pro.blur();})
        },

      delete_product_group(group_name){//刪除某一產品群組
        this.$confirm('是否刪除「 ' +group_name +' 」群組?', '刪除', {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
          type: 'warning'
          }).then(() => {
            this.axios.get("/operator_product_group",{
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
      search_tree_index(array,SearchWord){//找自訂群組所對應tree的index
        for(let i = 0; i < array.length; i++)
            if(array[i]['label'] == SearchWord)
                return i
        return -1
      },
    },
    }
</script>