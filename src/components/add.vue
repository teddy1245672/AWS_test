<style>
#note{
    display:inline;
},
.message-waring{
    width:1300px;
    overflow-y: auto;
    overflow-x: hidden;
    max-width:1300px;
    max-height:600px;
}
.none_delete_tag .el-tag.el-tag--info .el-tag__close{
  display: none;
}
#left100px{
    position:relative;
    left:100px;
}
.el-scrollbar__wrap {
    overflow-x: hidden;
}
 .input_require input.el-input__inner {
    border:#FF7575 1px solid;
}
.fade-enter,
.fade-leave-active{
    opacity: 0;
}
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}
.el-drawer__body {
    overflow: auto;
}
.el-input__inner{
    max-height:120px;
}
.el-select__tags{
    max-width:320px;
    max-height:100px;
    overflow-y: auto;
    overflow-x: hidden;
}

.el-select ::-webkit-scrollbar{
    display: none;
}

.custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
    }
</style>
<template>
    <div>
        <transition name="fade"><!--loading動畫-->
            <loading v-if="isLoading"></loading>
        </transition>
        <div style="position:relative;bottom:20px;font-size:28px;">資料新增</div>
        <div>
            <!--product tree 產品選擇-->
            <el-drawer
            title="產品選擇"
            :visible.sync="drawer"
            :with-header="false"
            size="20%">
            <el-button icon="el-icon-plus" @click="dialogVisible=true" type="warning" plain size="mini" v-show="this.lock[this.row_index]">產品群組</el-button>
            <el-button @click="cancel_drawer" type="danger" size="mini" plain>取消</el-button>
            <el-button @click="check_drawer" type="primary" size="mini" plain>確認</el-button>
            <el-tree
                :data="tree_data"
                :props="defaultProps"
                accordion
                node-key="id"
                ref="tree"
                @check="handleCheckChange"
                :render-content="tag_for_tree"
                show-checkbox>
            </el-tree>
            <br>
            <el-dialog
                title="產品群組(新增)"
                :visible.sync="dialogVisible"
                width="60%"
                :append-to-body="true">
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
                        v-show="deter_product_group(node)==false && append_tree_lock==false && data['add'] != true"size="mini"
                        type="text"
                        size="mini"
                        @click="() => append(node,data)">
                        加入此標籤
                    </el-button>
                    <el-button
                        v-show="data['add'] == true"size="mini"
                        type="text"
                        size="mini"
                        @click="() => remove(node, data)">
                        重選標籤
                    </el-button>
                    <el-tag v-show="deter_product_group(node)=='group'" style="font-size:14px;height:22px;" type="success">G</el-tag>
                    </span>
                </span>
                </el-tree>
                </el-scrollbar>
                <div style="position:absolute;top:80px;">
                <div style="position:relative;">名稱:<el-input v-model="product_dialog.caption" style="width:150px"placeholder="請輸入群組名稱"></el-input></div>
                <div style="position:relative;">產品:<el-select ref="dialog_pro" class="none_delete_tag" v-model="product_dialog.product_list" filterable remote multiple style="width:300px;" @focus="make_blur('1')" placeholder="請輸入產品群組"></el-select></div><!--@remove-tag="interact_tree"-->
                <div style="position:relative;">描述:<el-input v-model="product_dialog.description" style="width:200px" placeholder="請輸入描述"></el-input></div>
                <div style="position:relative;">備註:<el-input v-model="product_dialog.remarks" style="width:200px" placeholder="請輸入備註"></el-input></div>
                <span>
                    <el-button style="position:relative;left:30px;"type="danger" @click="cancel_product_group" plain>取消</el-button>
                    <el-button style="position:relative;left:40px;"type="primary" @click="store_product_group" plain>確定</el-button>
                </span>
                </div>
            </el-dialog>
            
            <!--<span style="position:relative;bottom:5px;" v-show="this.lock[this.row_index]">(新增後會重新整理)</span>-->
            </el-drawer>
        </div>
        <div :data="sub_row">
            <div align="left" id = 'left100px'>
                客戶(必填):<el-autocomplete :class="deter_require == 'customer'?'input_require':''" style="position:relative;left:32px;width:110px;"  size='small' v-model="input.name" 
                        :fetch-suggestions="querySearch_name" placeholder="請輸入客戶"></el-autocomplete>
                <span style="position:relative;left:50px;">廠區(選填):</span>
                <el-autocomplete style="position:relative;left:50px;width:100px" size='small' v-model="input.factory" 
                    :fetch-suggestions="querySearch_site" placeholder="請輸入廠區"></el-autocomplete>
                    <span style="position:relative;left:458px;font-size:16px;bottom:5px;">● 測試 - 借用給客戶(3個月)</span>
                    <span style="position:relative;left:286px;top:21px;">○ 申請新的 key 須填寫領用單，行政查詢用</span>
                    <span style="position:relative;right:17px;top:42px;">○ 此狀態須由申請人自行申請延期</span>
            </div>
            <div align="left" id = 'left100px'>
                KeyID(必填):<el-autocomplete :class="deter_require == 'sn'?'input_require':''" style="position:relative;left:20px;width:110px;"  size='small' v-model="sub_row.sn" 
                        :fetch-suggestions="querySearch_sn" placeholder="請輸入KeyID"></el-autocomplete>
                <span style="position:relative;left:40px;">類型(必填):</span>
                <el-select :class="deter_require == 'type'?'input_require':''" size="small"v-model="sub_row.type" @change="type_change" style="position:relative;left:40px;width:100px" placeholder="類型">
                    <el-option
                        v-for="item in type_opt" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                </el-select>
            </div>
            <div align="left" id = 'left100px'>業務地區(必填):
            <!--<el-autocomplete :class="deter_require == 'region'?'input_require':''" style="width:110px"  size='small' v-model="sub_row.region":fetch-suggestions="querySearch_region" placeholder="請輸入地區"></el-autocomplete>-->
            <el-select :class="deter_require == 'region'?'input_require':''" style="position:relative;right:5px;width:110px"  size='small' v-model="sub_row.region" placeholder="業務地區">
                <el-option
                    v-for="item in region_opt" :key="item.value" :label="item.label" :value="item.value">
                </el-option>
            </el-select>
            </div>
            <div align="left" id = 'left100px'>
            產品名稱(必填):</span><el-select :class="deter_require == 'func_uid'?'input_require':''" ref="sub_row_pro"v-model="sub_row.func_uid" filterable remote multiple style="width:350px;" placeholder="請點選右邊「產品選擇」" @focus="make_blur('2')"></el-select>
                <el-button @click="choose_func_uid()" style="position:relative;left:20px;" type="primary" size="mini" plain>產品選擇</el-button>
                <span style="position:relative;left:284px;bottom:23px;">● 出貨 - 尚未完全付完款項(6個月)</span>
                <span style="position:relative;left:63px;top:2px;">○ 須提供訂單編號(詢問業務)供行政查詢</span>
                <span style="position:relative;right:217px;top:26px;bottom:1px;">○ 此狀態須由申請人自行申請延期</span>
            </div>
            <div align="left" id = 'left100px'>數量(必填):<el-input :class="deter_require == 'count'?'input_require':''" v-model="sub_row.count" style="width:100px;position:relative;left:32px;" size = "small" placeholder="請輸入數量"></el-input></div>
            <div align="left" id = 'left100px'>
            到期日(必填):<el-date-picker :class="deter_require == 'expiration'?'input_require':''" type="date" value-format="yyyy-MM-dd" name="expiration" v-model="sub_row.expiration" style="width:200px;position:relative;left:16px;" placeholder="請輸入到期日"></el-date-picker>
            <span style="position:relative;left:32px;">允許版本(選填):</span>
            <el-input v-model="sub_row.version" style="width:200px;position:relative;left:32px;" size = "small" placeholder="請輸入允許版本"></el-input>
                <span style="position:relative;bottom:5px;left:220px;">● 正式 - 付完全部款項(隔年1月31日)</span>
                <span style="position:relative;right:20px;top:20px">○ 須提供訂單編號供行政查詢，財務查詢付款狀況</span>
            </div>
            <div align="left" id = 'left100px'>
            負責人(必填):
            <!--<el-input :class="deter_require == 'user'?'input_require':''" v-model="sub_row.user" style="width:200px;position:relative;left:16px;" size = "small" placeholder="請輸入負責人"></el-input>-->
                <template  v-for="(item, index) in sub_row.user_display">
                    <el-autocomplete :class="deter_require == 'user'?'input_require':''" v-model="sub_row.user_display[index]" style="width:200px;position:relative;left:12px;" :fetch-suggestions="querySearch_user" placeholder="請輸入負責人" ></el-autocomplete>
                    <el-button v-show="index != 0" type="text" icon="el-icon-error" style="color:#F56C6C;font-size:15px;position:relative;bottom:15px;left:3px;" @click="remove_user(index)"></el-button>
                </template>
                <el-button  type="text" icon="el-icon-circle-plus" style="font-size:15px;" @click="add_user()"></el-button>
            </div>
            <div align="left" id = 'left100px'>
            聯絡人(必填):
                <template  v-for="(item, index) in sub_row.contact_display">
                    <el-autocomplete :class="deter_require == 'contact'?'input_require':''" v-model="sub_row.contact_display[index]" style="width:200px;position:relative;left:12px;" :fetch-suggestions="querySearch_contact" placeholder="請輸入聯絡人"></el-autocomplete>
                    <el-button v-show="index != 0" type="text" icon="el-icon-error" style="color:#F56C6C;font-size:15px;position:relative;bottom:15px;left:3px;" @click="remove_contact(index)"></el-button>
                </template>
                <el-button  type="text" icon="el-icon-circle-plus" style="font-size:15px;" @click="add_contact()"></el-button>
            </div>
            <div align="left" id = 'left100px'>備註(選填):<el-input v-model="sub_row.comment" style="width:200px;position:relative;left:32px;" size = "small" placeholder="請輸入備註"></el-input>
                <span style="position:relative;bottom:40px;left:545px;">● 永久</span>
                <span style="position:relative;left:518px;bottom:13px;">○ 台灣區需提供客戶切結書</span>
                <span style="position:relative;left:329px;bottom:74px;">○ 此狀態會由系統自動延期一年並寄給各申請人</span>
            </div>
        </div>
        <div style ="position:relative;top:20px;" align = "center">
            <el-button circle type="primary" icon="el-icon-plus" style="position:relative;right:120px;bottom:45px;display:inline;" medium @click="add" v-show="lock[row_index] || lock.length == 0"></el-button>
            <el-button style="position:relative;left:550px;width:150px;display:inline;" @click="cancel" size = "medium" v-show="lock[row_index] || lock.length == 0">取消</el-button>
            <el-button style="position:relative;left:550px;width:150px;display:inline;" @click="submit" size = "medium" v-show="lock[row_index] || lock.length == 0">送出</el-button>
            <el-button style="position:relative;right:280px;bottom:45px;" circle type="primary" icon="el-icon-check" @click="store_row()" medium v-show="!lock[row_index] && lock.length != 0"></el-button>
            <el-button style="position:relative;right:280px;bottom:45px;" circle type="danger" icon="el-icon-close" @click="cancel_row()" medium v-show="!lock[row_index] && lock.length != 0"></el-button>
            <el-table
            ref="addtable"
            :data="tableData"
            style="width: 100%">
            <el-table-column align="center" prop="" label="編輯"  width="65">
                <template slot-scope = "{$index,row}" >
                    <el-button round type="danger" icon="el-icon-delete" @click="canceldata($index,row)" size = "mini" ></el-button>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="" label="操作"  width="100">
                <template slot-scope = "{$index,row}" >
                    <el-button circle type="primary"icon="el-icon-edit" @click="edit_row($index,row)" size = "mini" v-show="lock[$index]"></el-button>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="customer" label="客戶"  width="140">
                <template slot-scope = "{$index,row}" >
                    <el-input type="text" name="customer" v-model="row.customer" readonly style="width: 110px"></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="sn" label="KeyID"  width="120"> 
                <template slot-scope = "{row}" >
                    <el-input type="text" name="sn" v-model="row.sn" readonly style="width: 100px"></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="func_uid" label="產品名稱"  width="190"> 
                <template slot-scope = "{row}" >
                    <el-input type="text" name="func_uid" v-model="row.func_uid" readonly style="width: 160px"></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="version" label="版本" width="100"> 
                <template slot-scope = "{row}" >
                    <el-input type="text" name="version" v-model="row.version" readonly style="width: 80px"></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="count" label="數量" width="80"> 
                <template slot-scope = "{row}" >
                    <el-input type="text" name="count" v-model="row.count" readonly style="width: 50px"></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="expiration" label="到期日" width="170"> 
                <template slot-scope = "{row}" >
                    <el-input type="text" name="expiration" value-format="yyyy-MM-dd" v-model="row.expiration" readonly style="width: 140px" ></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="type" label="類型" width="100"> 
                <template slot-scope = "{row}" >
                    <el-input type="text" name="type" v-model="row.type" readonly style="width: 80px"></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="user" label="負責人" width="90"> 
                <template slot-scope = "{row}" >
                    <el-input type="text" name="user" v-model="row.user" readonly style="width: 60px"></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="region" label="地區" width="90"> 
                <template slot-scope = "{row}" >
                    <el-input type="text" name="region" v-model="row.region" readonly style="width: 60px" ></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="comment" label="備註" width="160"> 
                <template slot-scope = "{row}" >
                    <el-input type="text" name="comment" v-model="row.comment" readonly style="width: 130px"></el-input>
                </template>
            </el-table-column>
            <el-table-column align="center" prop="contact" label="聯絡人" width="100"> 
                <template slot-scope = "{row}" >
                    <el-input type="text" name="contact" v-model="row.contact" readonly style="width: 80px"></el-input>
                </template>
            </el-table-column>
            </el-table>
        </div>
    </div>
</template>
<script>
import Loading from '@/assets/loading'
export default {
  components:{ Loading },
  name: 'add',
  data: function() {
        return {
            product_groups_data:[],
            user:[],
            all_Data:{},//整個資料庫所有數據
            info_data:[],
            tableData:[],
            productgroup_tree:[],
            customer_site_opt:[],
            user_opt:[],
            customer_name_opt:[],
            region_opt:[],
            //caption_opt:[],
            func_uid_opt:[],
            sn_opt:[],
            contact_opt:[],
            type_opt:[{label: '正式',value: '正式'},
                    {label: '測試',value: '測試'},
                    {label: '出貨',value: '出貨'},
                    {label: '永久',value: '永久'}],
            info_id:0,
            input:{//左上方input框使用的(為了將客戶拆解)
                name:'',
                factory:''
            },
            product_dialog:{
                caption:'',
                product_list:[],
                description:'',
                remarks:'',
                product_list_detail:[]
            },
            sub_row:{
                caption: "",
                comment: "",
                contact: "",
                count: null,
                customer: "",
                expiration: "",
                func_uid: [],
                index: null,
                info: [],
                info_id: null,
                issued: "",
                operator: "",
                region: "",
                registration: "",
                sn: null,
                type: "",
                user: "",
                version: "",
                contact_display:[''],
                user_display:['']},
            lock:[],
            row_index:0,
            drawer: false,
            tree_data:[],
            origin_tree_data:[],
            dialogVisible:false,
            deter_require:'',
            append_tree_lock:false,//新增產品群組的lock
            register_append_node:[],//暫存新增產品群組data
            tree_node_count: 0,//key_id
            caption_to_product:[],//群組下對應所有產品
            tree_map:new Map(),
            optionSet:new Set(),
            isLoading:true
        }
  },
  created(){
      this.axios.get('/get_product_groups_info_data',{
        headers: {'Content-Encoding': 'gzip'}
      }).then(response => {
      this.product_groups_data = JSON.parse(JSON.stringify(response.data))['product_groups'];//最新product_group資料
    
      this.info_data = JSON.parse(JSON.stringify(response.data))['info_data']
      this.user = JSON.parse(this.$route.query.user);//把user傳進來
      this.all_Data = JSON.parse(this.$route.query.all_Data);
      //-----------------------處理nofilter_data(跟Show_all nofilter_data不一樣，add頁面的nofilter_data是整個info_data不關乎權限)
      var product_map = new Map()
      var option_map = new Map()
      var module_map = new Map()
      var sn_dict = JSON.parse(JSON.stringify(response.data))['sn_dict']
      for(let product of this.all_Data['product_data'])
        product_map.set(product['product_name'],{'category_id':product['category_id'],'caption':product['caption']})
      for(let option of this.all_Data['option_data'])
        option_map.set(option['option_name'],{'category_id':product_map.get(option['product_name'])['category_id'],'product_name':option['product_name'],'caption':option['caption']})
      for(let mod of this.all_Data['module_data']){
          module_map.set(mod['mod_uid'],mod['caption'])
        }
      var order_form = JSON.parse(JSON.stringify(this.info_data))
      var i = 0
      for (let info of this.info_data){
          if (sn_dict[info['sn']] != undefined){
              if(this.all_Data['customer_data'][sn_dict[info['sn']]['sn_id'] - 1]['site'] !='')
                order_form[i] = Object.assign(order_form[i],{'customer':this.all_Data['customer_data'][sn_dict[info['sn']]['sn_id'] - 1]['name'] + '|' + 
                this.all_Data['customer_data'][sn_dict[info['sn']]['sn_id'] - 1]['site'],'user':sn_dict[info['sn']]['user']
                ,'info':[sn_dict[info['sn']]['note1'],sn_dict[info['sn']]['note2'],sn_dict[info['sn']]['note3'],sn_dict[info['sn']]['note4'],sn_dict[info['sn']]['note5']]})
              else
                order_form[i] = Object.assign(order_form[i],{'customer':this.all_Data['customer_data'][sn_dict[info['sn']]['sn_id'] - 1]['name'] ,'user':sn_dict[info['sn']]['user']
                ,'info':[sn_dict[info['sn']]['note1'],sn_dict[info['sn']]['note2'],sn_dict[info['sn']]['note3'],sn_dict[info['sn']]['note4'],sn_dict[info['sn']]['note5']]})
              if(sn_dict[info['sn']]['region'] != '')
                order_form[i] = Object.assign(order_form[i],{'region':this.all_Data['region_data'][parseInt(sn_dict[info['sn']]['region'],10) - 1]['name']})
              else
                order_form[i] = Object.assign(order_form[i],{'region':''})
              }
          
          if(option_map.get(info['func_uid']) != undefined){
            order_form[i] = Object.assign(order_form[i],{'caption':option_map.get(info['func_uid'])['category_id']})
            order_form[i]['func_uid'] = (option_map.get(info['func_uid'])['caption']+'('+option_map.get(info['func_uid'])['product_name']+')');//edit介面需要
          }
          else if (product_map.get(info['func_uid']) != undefined){//db有錯
            order_form[i] = Object.assign(order_form[i],{'caption':product_map.get(info['func_uid'])['category_id']})
            order_form[i]['func_uid'] = product_map.get(info['func_uid'])['caption'];//edit介面需要
          }
          if(module_map.get(info['type']) != undefined)
            order_form[i]['type'] = module_map.get(info['type']);//edit介面需要
          
          i++
      }
      this.info_data = JSON.parse(JSON.stringify(order_form))
      
      this.info_id = this.info_data.length;
      for(let sn of this.all_Data['sn_data'])
        this.sn_opt.push({value:sn['sn'],label:sn['sn']});
        
      var user_set = new Set();
      for(let user of this.all_Data['sn_data'])
        for(let user_email of user['user'].split(','))
            user_set.add(user_email)
      for(let user of user_set)
        this.user_opt.push({value:user,label:user})

      for (let region of this.all_Data['region_data'])
        this.region_opt.push({value:region['name'],label:region['name']});
        
      for (let contact of this.all_Data['user_data']){
        this.contact_opt.push({value:contact['email'],label:contact['email']});
      }
      for (let customer of this.all_Data['customer_data']){
        let test_name = 0;
        let test_site = 0;
        for(let customer_name of this.customer_name_opt)
            if(customer_name['value'] == customer['name'])
                test_name = 1
        for(let customer_site of this.customer_site_opt)
            if(customer_site['value'] == customer['site'])
                test_site = 1
        if(test_name == 0)
            this.customer_name_opt.push({value:customer['name'],label:customer['name']})
        if(test_site == 0)
            this.customer_site_opt.push({value:customer['site'],label:customer['site']})
      }


      var checkData = JSON.parse(this.$route.query.checked_Data);
      if(checkData.length != 0){
        for (let add of checkData){//如在 (users) 有資料, 就去掉信箱網域(@後面)
            add['contact_display'] = add['contact'].split(',');
        }
        for (let data of checkData){
            data['info_id'] = this.info_id;
            data = Object.assign(data,{'operator':'新增'});
            this.info_id++;
        }
        this.tableData = JSON.parse(JSON.stringify(checkData));
      }
      for(let i of this.tableData)
        this.lock.push(true);
    //-----------------------處理樹狀數據(未加入自訂群組)---------------------//
    var captionSet = new Set();
    for(let caption of this.all_Data['product_data'])
        captionSet.add(caption['category_id'])
    for(let caption of captionSet){
        this.tree_data.push({'id':this.tree_node_count,'label':caption,'children':[]})
        this.tree_node_count++;
    }
    for(let product of this.all_Data['product_data'])
        for(let i = 0;i < this.tree_data.length; i++)
            if(this.tree_data[i]['label'] == product['category_id']){
                this.tree_data[i]['children'].push({'id':this.tree_node_count,'label':product['caption'],'children':[],'category':product['category_id']})
                this.tree_node_count++;
            }

    for(let i = 0; i < this.tree_data.length; i++)
        for(let j = 0; j < this.tree_data[i]['children'].length; j++)
            for(let product of this.all_Data['product_data'])
                if(this.tree_data[i]['children'][j]['label'] == product['caption'])
                    for(let option of this.all_Data['option_data'])
                        if(product['product_name'] == option['product_name']){
                            this.tree_data[i]['children'][j]['children'].push({'id':this.tree_node_count,'label':option['caption'],'product_name':option['product_name'],'children':[],'category':option['product_name']})
                            this.tree_node_count++;
                        }
    this.origin_tree_data = JSON.parse(JSON.stringify(this.tree_data))
    //-------------------------caption對應product-------------------//
    for(let caption of captionSet){
        this.caption_to_product.push({'caption':caption,'product':[]})
        for(let pro of this.all_Data['product_data']){
            if(pro['category_id'] == this.caption_to_product[this.caption_to_product.length - 1]['caption'])
                this.caption_to_product[this.caption_to_product.length - 1]['product'].push(pro['product_name'])
        }
    }

    for(let opt of this.all_Data['option_data'])
        this.optionSet.add(opt['product_name'])
    for(let opt of this.optionSet){
        this.caption_to_product.push({'caption':opt,'product':[]})
        for(let option of this.all_Data['option_data']){
            if(option['product_name'] == this.caption_to_product[this.caption_to_product.length - 1]['caption'])
                this.caption_to_product[this.caption_to_product.length - 1]['product'].push(option['option_name'])
        }
        for(let i = 0; i < this.caption_to_product.length - 1; i++)
            if(this.caption_to_product[i]['product'].indexOf(this.caption_to_product[this.caption_to_product.length - 1]['caption']) != -1){
                this.caption_to_product[i]['product'].splice(this.caption_to_product[i]['product'].indexOf(this.caption_to_product[this.caption_to_product.length - 1]['caption']),1)
                for(let option of this.caption_to_product[this.caption_to_product.length - 1]['product'])
                    this.caption_to_product[i]['product'].push(option)
            }
    }
    for(let i = 0;i < this.caption_to_product.length; i++)
        for(let pro of this.all_Data['product_data']){
            if(this.caption_to_product[i]['caption'] == pro['product_name'])
                this.caption_to_product[i]['caption'] = pro['caption']
        }

    //--------------------------caption所對應的tree-----------------------------//

    for(let tree of JSON.parse(JSON.stringify(this.tree_data)))
        if(tree.children.length != 0){
            this.tree_map.set(tree.label,tree)
            for(let c_tree of tree.children)
                if(c_tree.children.length != 0)
                    this.tree_map.set(c_tree.label,c_tree)
        }
    //---------------------將自訂群組插入樹狀圖中(根據tag)----------------------//
    for(let pro_group of this.product_groups_data){//根據tag找到所對應的tree節點
        let temp = this.tree_data;
        for(let tag of JSON.parse(pro_group.tag))
            temp = temp[this.search_tree_index(temp,tag)]['children']

        temp.unshift({'id':this.tree_node_count++,'label':pro_group['caption'],'children':[]})
        let under_group = this.deter_group(this.caption_to_product,JSON.parse(pro_group['product_list']))

        let copy_pro_group = JSON.parse(pro_group['product_list']);
        for(let gro of under_group){
            let tree = this.tree_node_adjust(this.tree_map.get(gro),this.tree_node_count)
            temp[0]['children'].push(tree[0])
            this.tree_node_count = tree[1]
            for(let table of this.caption_to_product)
                if(table['caption'] == gro){
                    for(let pro of table['product']){
                        let index = copy_pro_group.indexOf(pro);
                        if(index != -1)
                            copy_pro_group.splice(index,1)
                    }
                }
        }

        for(let remainder_pro of copy_pro_group){//將預設群組內的產品去掉後 剩下的func_uid再額外插入自訂群組
            for(let opt of this.all_Data['option_data'])
                if(opt['option_name'] == remainder_pro)
                    temp[0]['children'].push({'id':this.tree_node_count,'label':opt['caption'],'product_name':opt['product_name'],'children':[]})
            for(let pro of this.all_Data['product_data'])
                if(pro['product_name'] == remainder_pro)
                    temp[0]['children'].push({'id':this.tree_node_count,'label':pro['caption'],'children':[]})
            this.tree_node_count++
        }
    }
    this.productgroup_tree = JSON.parse(JSON.stringify(this.tree_data))
    this.isLoading = false
    })},
    watch:{
        input:{
            handler(newName, oldName) {//監測input是否改變 若改變則改變tableData customer
                if(this.input.factory != '')
                    this.sub_row.customer = this.input.name + '|' + this.input.factory
                else
                    this.sub_row.customer = this.input.name;
            },
            deep: true,
        },
        sub_row:{
            handler(newName, oldName) {//根據監測sn 帶入sn of user
                for(let sn of this.all_Data['sn_data'])//當你新增客戶 改了user 又把新增的庫戶改回來 此時需要把user還原
                    if(this.sub_row['sn'] == sn['sn'])
                        this.sub_row['user'] = sn['user'];
            },
            deep: true,
        },
    },
    methods:{
      type_change(){//根據type自動調整期限
        let tempDate = new Date;
        switch (this.sub_row.type){
            case '正式'://*當 B ==正式, 日期設定在隔年的 1/30
                tempDate.setMonth(tempDate.getMonth()+12);
                this.sub_row.expiration = tempDate.toISOString().slice(0, 4) + '-01-30'
                break;
            case '測試'://* 當 B ==測試, 日期往後設定 3 個月
                tempDate.setMonth(tempDate.getMonth()+3);
                this.sub_row.expiration = tempDate.toISOString().slice(0, 10)  
                break;
            case '出貨'://* 當 B ==出貨, 日期往後設定 6 個月
                tempDate.setMonth(tempDate.getMonth()+6);
                this.sub_row.expiration = tempDate.toISOString().slice(0, 10)  
                break;
            case '永久'://* 當 B ==永久, 日期設定 9999年12月31日
                this.sub_row.expiration = '9999-12-31'  
            break;
        }
        },
      deter_group(caption_to_product,compare_product){//用caption_to_product判斷自訂群組底下有那些預設群組
        var group_record = []
        var copy = JSON.parse(JSON.stringify(compare_product))
        for(let table of caption_to_product){
            let test = 0
            for(let pro of table['product']){
                if(copy.indexOf(pro) === -1){//若自訂群組沒有預設群組中一個產品 則直接break
                    test = 1
                    //copy = JSON.parse(JSON.stringify(compare_product))
                    break
                }
            }
            if(test == 0){//若群組有該預設群組下所有產品 則將預設群組中所有產品從群組下移除
                group_record.push(table['caption'])
                for(let pro of table['product'])
                    copy.splice(copy.indexOf(pro),1)
            }
        }

        return group_record
      },
      store_product_group(){//儲存新增產品群組
        if (this.product_dialog.caption == '' || this.product_dialog.product_list.length == 0){
            this.$message.error('請將「產品群組」新增單，填寫完整');
            return
        }
        var temp = []
        for(let product of this.product_dialog.product_list_detail){//將caption換成product
            let test = 0
            let label_copy = product['label'].split('').reverse().join('').split('(') 
            if(this.optionSet.has(label_copy[0].replace(')','')))
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

        for(let product_group of this.product_groups_data){//防止產品群組名稱or產品 重複
            if(product_group['caption'] == this.product_dialog.caption){
                this.$message.error('產品名稱重複，請更改');
                return
            }
            if(product_group.product_list == JSON.stringify(temp)){
                this.$message.error('群組內產品與其他群組完全重複');
                return
            }
        }
        if(this.append_tree_lock != true){
            this.$message.error('請選擇群組所在位置');
            return
        }
        this.product_dialog.product_list = JSON.parse(JSON.stringify(temp));
        var temp_local = []
        var temp = this.register_append_node[0]
        while(temp.label != undefined){
            temp_local.unshift(temp.label)
            temp = temp.parent;
        }

        this.axios.post("/save_to_product_group",{
            caption:this.product_dialog.caption,
            product_list:JSON.stringify(this.product_dialog.product_list),
            tag:JSON.stringify(temp_local),
            description:this.product_dialog.description,
            remarks:this.product_dialog.remarks
        }).then((response)=>{
            this.axios.get('/get_product_groups_info_data',{
            }).then(response => {
            this.product_groups_data = JSON.parse(JSON.stringify(response.data))['product_groups'];//最新product_group資料
            this.dialogVisible = false
            //------------------------把新增的product_groups重新insert tree一次---------------------//
            this.tree_data = JSON.parse(JSON.stringify(this.origin_tree_data))
            for(let pro_group of this.product_groups_data){//根據tag找到所對應的tree節點
                let temp = this.tree_data;
                for(let tag of JSON.parse(pro_group.tag))
                    temp = temp[this.search_tree_index(temp,tag)]['children']

                temp.unshift({'id':this.tree_node_count++,'label':pro_group['caption'],'children':[]})
                let under_group = this.deter_group(this.caption_to_product,JSON.parse(pro_group['product_list']))

                let copy_pro_group = JSON.parse(pro_group['product_list']);
                for(let gro of under_group){
                    let tree = this.tree_node_adjust(this.tree_map.get(gro),this.tree_node_count)
                    temp[0]['children'].push(tree[0])
                    this.tree_node_count = tree[1]
                    for(let table of this.caption_to_product)
                        if(table['caption'] == gro){
                            for(let pro of table['product']){
                                let index = copy_pro_group.indexOf(pro);
                                if(index != -1)
                                    copy_pro_group.splice(index,1)
                            }
                        }
                }

                for(let remainder_pro of copy_pro_group){//將預設群組內的產品去掉後 剩下的func_uid再額外插入自訂群組
                    for(let opt of this.all_Data['option_data'])
                        if(opt['option_name'] == remainder_pro)
                            temp[0]['children'].push({'id':this.tree_node_count,'product_name':opt['product_name'],'label':opt['caption'],'children':[]})
                    for(let pro of this.all_Data['product_data'])
                        if(pro['product_name'] == remainder_pro)
                            temp[0]['children'].push({'id':this.tree_node_count,'label':pro['caption'],'children':[]})
                    this.tree_node_count++
                }
            }
            this.productgroup_tree = JSON.parse(JSON.stringify(this.tree_data))
            this.product_dialog.caption = ''
            this.product_dialog.product_list = []
            this.product_dialog.description = ''
            this.product_dialog.remarks = ''
            this.product_dialog.product_list_detail = []
            })
        });
      },
      /*interact_tree(data){//el-select 刪除tag連動
        let temp_list = []

        for(let temp of this.$refs.product_group_tree.getCheckedNodes()){
            if(temp['children'].length == 0 && temp['label'] != data)
                temp_list.push(temp)
        }
       this.$nextTick(() => {
        this.$refs.product_group_tree.setCheckedNodes([])
        this.$refs.product_group_tree.setCheckedNodes(temp_list)
        });
      },*/
      choose_func_uid(){//產品選擇
        this.drawer = true;
        this.product_group = []//將產品群組選擇初始化
      },
      cancel_drawer(){//取消tree選擇
        this.$nextTick(() => {this.$refs.tree.setCheckedKeys([])});//清空tree選擇
        this.drawer = false;
      },
      check_drawer(){//確認產品選擇

        this.sub_row.func_uid=[]
        if(this.lock[this.row_index] == false){
            for(let node of this.$refs.tree.getCheckedNodes())
                if(node['children'].length == 0 || node['children'] == undefined){
                    if(node['product_name'] != undefined)
                        this.sub_row.func_uid = [(node['label']+'('+node['product_name']+')')]
                    else
                        this.sub_row.func_uid = [node['label']]
                }
        }
        else{
            var product_Set = new Set();//用set過濾 因有重複
            for(let node of this.$refs.tree.getCheckedNodes()){
                if(node['children'].length == 0 || node['children'] == undefined){
                    if(node['product_name'] != undefined)
                        product_Set.add(node['label']+'('+node['product_name']+')')
                    else
                        product_Set.add(node['label'])
                }
            }
            for(let product of product_Set)
                this.sub_row.func_uid.push(product)
        }
        this.$nextTick(() => {this.$refs.tree.setCheckedKeys([])});//清空tree選擇
        this.drawer = false;
      },
      tree_node_adjust(tree,tree_node_count){//調整整個子樹的tree_node_count 
        let copy_tree = JSON.parse(JSON.stringify(tree))
        copy_tree.id = tree_node_count++;
        for(let c_tree of copy_tree.children){
            c_tree.id = tree_node_count++;
            for(let cc_tree of c_tree.children)
                cc_tree.id = tree_node_count++;
        }
        return [copy_tree,tree_node_count]//[0]tree [1]node_count
      },
      cancel_product_group(){//初始化產品群組Dialog
        this.product_dialog.caption = ''
        this.product_dialog.product_list = []
        this.product_dialog.description=''
        this.product_dialog.remarks=''
        this.$nextTick(() => {this.$refs.product_group_tree.setCheckedKeys([])});//清空tree選擇
        this.dialogVisible = false;
      },
      remove(node, data) {//刪除新增節點
        this.append_tree_lock = false;
        const parent = node.parent;
        const children = parent.data.children || parent.data;
        const index = children.findIndex(d => d.id === data.id);
        children.splice(index, 1);
        this.productgroup_tree = JSON.parse(JSON.stringify(this.tree_data))//初始化產品群組tree
        this.register_append_node = [];
      },
      append(node,data) {//新增群組節點
        if(this.product_dialog.caption == ''){
            this.$message.error('請填寫「群組名稱」，再選擇插入位置');
            return 
        }
        this.append_tree_lock = true;
        const newChild = {'label': this.product_dialog.caption, 'children': [], disabled:true,'add':true};
        if (!data.children) {
          this.$set(data, 'children', []);
        }
        data.children.push(newChild);
        this.register_append_node = [node];
      },
      tag_for_tree(h, { node, data, store }) {//產品群組在tree中 右邊有[群組]tag字樣
        for(let pro_group of this.product_groups_data){
            if(node.label == pro_group['caption'])
                return ( <div> <span>{node.label}</span> <el-tag style="position:absolute;right:1px;font-size:14px;height:25px;"type="success">G</el-tag></div>)
            if(node.parent.label == pro_group['caption'])
                if(node.data.children.length == 0 && node.data.product_name != undefined)
                    return ( <div> <span>{node.label}</span> <el-tag style="position:absolute;right:1px;font-size:14px;height:25px;"type="info">{node.data.product_name}</el-tag></div>)
        }
        return( <div> <span>{node.label}</span></div>) 
      },
      deter_product_group(node){//若是自訂群組則貼家G標籤 若是自訂群組下的product則不用
        for(let pro_group of this.product_groups_data)
          if(node.label == pro_group['caption'])
            return 'group'
        for(let pro_group of this.product_groups_data)
          if(node.parent.label == pro_group['caption'])
            return 'under_group'
        return false
      },
      choose_product_group(data,checked){//選擇product_group_tree時 同步帶入產品群組新增表單 

        var temp_product_list = []
        var temp_product_list_detail = []
        for(let product of this.$refs.product_group_tree.getCheckedNodes())
            if(product['children'].length == 0){
                if(product['product_name']!= undefined){
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
      },
      handleCheckChange(data, checked){//使修改模式時無法點擊全選
        if(this.lock[this.row_index] == false){
            if(data['children'].length > 0){
                this.$nextTick(() => {this.$refs.tree.setCheckedNodes([])});
                this.$message({message: '修改模式無法全選',type: 'warning'});
                return
            }
            this.$nextTick(() => {this.$refs.tree.setCheckedNodes([data])});
        }
      },
      search_tree_index(array,SearchWord){//找自訂群組所對應tree的index
        for(let i = 0; i < array.length; i++)
            if(array[i]['label'] == SearchWord)
                return i
        return -1
      },

      add_user(){//上方聯絡人修改框增加
          this.sub_row.user_display.push('');
      },
      remove_user(index){//上方聯絡人修改框減少
        this.sub_row.user_display.splice(index,1);
      },
      add_contact(){//上方聯絡人修改框增加
          this.sub_row.contact_display.push('');
      },
      remove_contact(index){//上方聯絡人修改框減少
        this.sub_row.contact_display.splice(index,1);
      },
      edit_row(index, row){
        for(let i = 0; i < this.lock.length;i++)//防止使用者連續觸發兩列以上的編輯
            if(this.lock[i] == false && i != index)
                this.cancel_row();
            
        if(row.customer.indexOf('|') != -1){
            this.input.name = row.customer.split('|')[0]
            this.input.factory = row.customer.split('|')[1]
        }
        else{
            this.input.name = row.customer
            this.input.factory = ''
        }
        this.row_index = index;
        this.sub_row = JSON.parse(JSON.stringify(row));
        this.sub_row.func_uid = [row['func_uid']]
        this.$set(this.lock,index,false)
      },
      cancel_row(){
        this.sub_row = {caption: "",comment: "",contact: "",count: null,customer: "",
            expiration: "",func_uid: [],index: null,info: [],info_id: null,issued: "",
            operator: "",region: "",registration: "",sn: null,type: "",user: "",version: "",contact_display:[''],user_display:['']}
        this.input.name = ''
        this.input.factory = ''
        this.$set(this.lock,this.row_index,true)
      },
      store_row(){
        for(let i = 0; i < this.sub_row['contact_display'].length; i++)//若聯絡人修改框中有框無值 則刪除此框
            if(this.sub_row['contact_display'][i] == ''){
                this.sub_row['contact_display'].splice(i,1);
                i--;
            }
        for(let i = 0; i < this.sub_row['user_display'].length; i++)//若負責人修改框中有框無值 則刪除此框
            if(this.sub_row['user_display'][i] == ''){
                this.sub_row['user_display'].splice(i,1);
                i--;
            }  
        if(this.test_edit_add()){
            this.tableData[this.row_index] = Object.assign({},this.sub_row);
            this.tableData[this.row_index]['func_uid'] = this.sub_row['func_uid'][0];
            this.tableData[this.row_index]['contact'] = this.sub_row['contact_display'].join();
            this.tableData[this.row_index]['user'] = this.sub_row['user_display'].join();

            this.sub_row = {caption: "",comment: "",contact: "",count: null,customer: "",
                expiration: "",func_uid: [],index: null,info: [],info_id: null,issued: "",
                operator: "",region: "",registration: "",sn: null,type: "",user: "",version: "",contact_display:[''],user_display:['']}
            this.input.name = ''
            this.input.factory = ''
            this.$set(this.lock,this.row_index,true)
        }
      },
      test_edit_add(){//修改資料和新增資料的防呆
        if(this.input.name == null || this.input.name == ""){
            this.$message({message: '客戶不可為空',type: 'warning'});
            this.deter_require = 'customer';
            return false;
        }
        /*if(this.sub_row['user'] == null || this.sub_row['user'] == ""){
            this.$message({message: '負責人不可為空',type: 'warning'});
            this.deter_require = 'user';
            return false;
        }*/
        if(this.sub_row['user_display'].length == 0){
            this.$message({message: '負責人不可為空',type: 'warning'});
            this.deter_require = 'user';
            return false;
        }
        if(this.sub_row['contact_display'].length == 0){
            this.$message({message: '聯絡人不可為空',type: 'warning'});
            this.deter_require = 'contact';
            return false;
        }
        if(this.sub_row['sn'] == null || this.sub_row['sn'] == ""){
            this.$message({message: 'KeyID不可為空',type: 'warning'});
            this.deter_require = 'sn';
            return false;
        }
        /*if(this.sub_row['caption'] == null || this.sub_row['caption'] == ""){
            this.$message({message: '產品類別不可為空',type: 'warning'});
            return false;
        }*/
        if(this.sub_row['func_uid'] == null || this.sub_row['func_uid'] == ""){
            this.$message({message: '產品名稱不可為空',type: 'warning'});
            this.deter_require = 'func_uid';
            return false;
        }
        if(this.sub_row['count'] == null || this.sub_row['count'] == ""){
            this.$message({message: '數量不可為空',type: 'warning'});
            this.deter_require = 'count';
            return false;
        }
        if(this.sub_row['expiration'] == null || this.sub_row['expiration'] == ""){
            this.$message({message: '到期日期不可為空',type: 'warning'});
            this.deter_require = 'expiration';
            return false;
        }
        if(this.sub_row['type'] == null || this.sub_row['type'] == ""){
            this.$message({message: '類型不可為空',type: 'warning'});
            this.deter_require = 'type';
            return false;
        }
        if(this.sub_row['region'] == null || this.sub_row['region'] == ""){
            this.$message({message: '地區不可為空',type: 'warning'});
            this.deter_require = 'region';
            return false;
        }
        var customer_map = new Map()
        let test = 0;//驗證新增客戶 sn是否也有修改
        for(let customer of this.all_Data['customer_data']){//若新增客戶則可以修改負責人
            if(customer['site'] != '')
                customer_map.set(customer['customer_id'],customer['name']+'|'+customer['site'])
            else
                customer_map.set(customer['customer_id'],customer['name'])
            
            if(this.input.name == customer['name'] && this.input.factory == customer['site'])
                test = 1;
        }
        if(test == 0){
            for(let sn of this.all_Data['sn_data']){//若新增客戶則可以修改負責人
                if(this.sub_row['sn'] == sn['sn'] ){
                    //this.deter_require = 'sn';
                    //this.$message({message: '新增客戶時，也要新增一筆新keyID',type: 'warning'});
                    var html_text = "<body><table border='1'><tr>"
                    +  '<th align="center" width="120">客戶</th>'
                    +  '<th align="center" width="100">更新日期</th>'
                    +  '<th align="center" width="90">KeyID</th>'
                    +  '<th align="center" width="350">產品名稱</th>'
                    +  '<th align="center" width="100">版本</th>'
                    +  '<th align="center" width="60">類型</th>'
                    +  '<th align="center" width="60">數量</th>'
                    +  '<th align="center" width="100">到期日</th>'
                    +  '<th align="center" width="60">地區</th>'
                    +  '<th align="center" width="130">備註</th>'
                    +  '<th align="center" width="170">聯絡人</th></tr>'

                    for(let d of this.info_data){
                        if(d['sn'] == sn['sn']){
                            html_text+='<tr align="center">'
                            html_text+=(
                            '<td width="120">'+ String(d['customer'])+'</td>'+
                            '<td width="100">'+ String(d['issued'])+'</td>'+
                            '<td width="90">'+ String(d['sn'])+'</td>'+
                            '<td width="350">'+ String(d['func_uid'])+'</td>'+
                            '<td width="100">'+ String(d['version'])+'</td>'+
                            '<td width="60">'+ String(d['type'])+'</td>'+
                            '<td width="60">'+ String(d['count'])+'</td>'+
                            '<td width="100">'+ String(d['expiration'])+'</td>'+
                            '<td width="60">'+ String(d['region'])+'</td>'+ 
                            '<td width="130">'+ String(d['comment'])+'</td>'+
                            '<td width="170">'+ String(d['contact'])+'</td>'+
                                '</tr>')
                        }
                    }
                    html_text += "</table></body>"
                    //this.deter_require = 'sn';
                    //this.$message({message: '新增客戶時，也要新增一筆新keyID',type: 'warning'});
                    this.$confirm('此<span style="background-color: #ffb7b7">〈ID:'+String(sn['sn'])+'〉</span>已在<span style="background-color: #ffb7b7"><strong>〈客戶:'+customer_map.get(sn['sn_id'])+'〉</strong></span>下，是否要刪除以下此ID連結資料後新增'+html_text, '警告', {
                            confirmButtonText: '確定',
                            customClass: 'message-waring',
                            cancelButtonText: '取消',
                            dangerouslyUseHTMLString:true
                        }).then(() => {
                            console.log("確定");//將要刪除的KeyID存起來 等送出後將sn底下資料送出刪除申請*/
                            return true})//這裡的return有問題 問題原因:異步問題
                        .catch(() => {
                            console.log('取消');
                            return false})//這裡的return有問題 問題原因:異步問題
     
                }
            }
        }
        return true;
      },
      submit:function(){
        var fight_data = [];//將與主畫面重複的原始資訊放入
        //---------------跟主畫面資料比對有無重複----------------//
        for(let check of this.tableData)//看新增資料是否跟主畫面的資料有重複 比較類型、KeyID、產品名稱
            for(let show_all_info of this.info_data)
                if(JSON.stringify(check['sn']) == JSON.stringify(show_all_info['sn']) & 
                JSON.stringify(check['func_uid']) == JSON.stringify(show_all_info['func_uid']) & JSON.stringify(check['type']) == JSON.stringify(show_all_info['type'])){
                    alert("新增資料庫與原資料庫發生衝突，自動新增以下幾筆資料的刪除申請\n" + /*"客戶名稱: "+ check['customer']+ */"\nKeyID: " + check['sn']+ "\n產品名稱: " + check['func_uid']+"\n類型 : " + check['type'] + "\n此筆資料重複");
                    fight_data.push(show_all_info);
                }
        if(fight_data.length != 0){//若有新增內重複的資料就自動加一筆刪除(原本的)
            for (let fight of fight_data){//如在 (users) 有資料, 就去掉信箱網域(@後面)
                for(let user of this.all_Data['user_data'])
                if (fight['contact'] == user['email']){
                    fight['contact'] = user['user'];
                }
                fight = Object.assign(fight,{'operator':'刪除'})
            }
            this.axios.post("/save_to_handle",{
                            checked_Data:fight_data,
                            content:'資料庫衝突',
                            user:this.user
                        }).then((response)=>{
                        this.axios.post("/save_to_handle",{//刪除後新增 必須擺在刪除then後 不然會衝突
                                checked_Data: this.tableData,
                                content:'none',
                                user:this.user
                            }).then((response)=>{
                                let res = response.data;
                                this.$router.push({name: 'Show_All'});
                            });
                        });
            }
            else{
                this.axios.post("/save_to_handle",{
                        checked_Data: this.tableData,
                        content:'none',
                        user:this.user
                    }).then((response)=>{
                        let res = response.data;
                        this.$router.push({name: 'Show_All'});
                    });
            }
      },
      add:function(){//新增一行空數據
        if(this.sub_row['contact_display'].length > 1)
            for(let i = 0; i < this.sub_row['contact_display'].length; i++)//若聯絡人修改框中有框無值 則刪除此框
                if(this.sub_row['contact_display'][i] == ''){
                    this.sub_row['contact_display'].splice(i,1);
                    i--;
                }
        if(this.test_edit_add()){
            var tempDate = new Date;
            var today = tempDate.toISOString().slice(0, 10)
            for(let func_uid of this.sub_row.func_uid){
                this.tableData.push({'info_id':this.info_id,'caption':this.sub_row.caption,'comment':this.sub_row.comment,'contact':this.sub_row.contact_display.join(),
                'count':this.sub_row.count,'customer':this.sub_row.customer,'expiration':this.sub_row.expiration,
                'func_uid':func_uid,'info':this.sub_row.info,'issued':today,'region':this.sub_row.region,
                'registration':this.sub_row.registration,'sn':this.sub_row.sn,'type':this.sub_row.type,
                'user':this.sub_row.user,'version':this.sub_row.version,'operator':'新增','index':this.tableData.length,'contact_display':this.sub_row.contact_display})
                this.info_id++;
                this.lock.push(true);
            }
        }
      },
      canceldata:function(index,row){//刪除該行數據
         this.tableData.splice(index,1);
         this.lock.splice(index,1);
      },
      cancel:function(){//退回主畫面
          this.$router.push({name: 'Show_All'});
      },
      //------------------------------建議選項-----------------------------//
      querySearch_sn(queryString, cb) {
        var results = queryString ? this.sn_opt.filter(this.createFilter(queryString)) : this.sn_opt;
        cb(results);// 調用 callback 返回建議列表的數據
      },
      querySearch_name(queryString, cb) {
        var results = queryString ? this.customer_name_opt.filter(this.createFilter(queryString)) : this.customer_name_opt;
        cb(results);// 調用 callback 返回建議列表的數據
      },
      querySearch_site(queryString, cb) {
        var results = queryString ? this.customer_site_opt.filter(this.createFilter(queryString)) : this.customer_site_opt;
        cb(results);// 調用 callback 返回建議列表的數據
      },
      querySearch_user(queryString, cb){
        var results = queryString ? this.user_opt.filter(this.createFilter(queryString)) : this.user_opt;
        if(results.length == 0){
            results.push({value:queryString + '@eastek.com.cn',label:queryString + '@eastek.com.cn'});
            results.push({value:queryString + '@eastek.com.tw',label:queryString + '@eastek.com.tw'});
        }
        cb(results);// 調用 callback 返回建議列表的數據
      },
      /*querySearch_region(queryString, cb) {
        var results = queryString ? this.region_opt.filter(this.createFilter(queryString)) : this.region_opt;
        cb(results);// 調用 callback 返回建議列表的數據
      },*/
      querySearch_contact(queryString, cb){
        var results = queryString ? this.contact_opt.filter(this.createFilter(queryString)) : this.contact_opt;
        if(results.length == 0){
            results.push({value:queryString + '@eastek.com.cn',label:queryString + '@eastek.com.cn'});
            results.push({value:queryString + '@eastek.com.tw',label:queryString + '@eastek.com.tw'});
        }
        cb(results);// 調用 callback 返回建議列表的數據
      },
      createFilter(queryString) {//搜尋建議選項
        return (any) => {
          return (String(any.value).toLowerCase().indexOf(String(queryString).toLowerCase()) != -1);
        };
      },
      make_blur(mode){//使el-select失焦
        if(mode == '1')
            this.$nextTick(()=>{this.$refs.dialog_pro.blur();})
        if(mode == '2')
            this.$nextTick(()=>{this.$refs.sub_row_pro.blur();})
        },
    }
}
</script>