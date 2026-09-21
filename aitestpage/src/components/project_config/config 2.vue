<template>
    <div>
      <el-row display="margin-top:10px">
        <el-button type="primary" @click="add_dialogVisible = true" style="float:left; margin: 2px;">新增</el-button>
        <el-dialog title="configData" :visible.sync="add_dialogVisible">
          <el-form :model="addData" :rules="rules" ref="addData">
            <el-form-item label="key" prop="key">
              <el-input v-model="addData.key"></el-input>
            </el-form-item>
            <el-form-item label="value" prop="value">
              <el-input v-model="addData.value"></el-input>
            </el-form-item>
            <el-form-item label="remarks" prop="remarks">
              <el-input v-model="addData.remarks"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="cancelButton">取消</el-button>
            <el-button type="primary" @click="addconfigdata()">确定</el-button>
          </div>
        </el-dialog>
        <el-table :data="configDatalist" style="width: 100%" border>
          <el-table-column prop="id" label="id" min-width="100">
            <template slot-scope="scope"> {{ scope.row.id }} </template>
          </el-table-column>
          <el-table-column prop="key" label="key" min-width="100">
            <template slot-scope="scope"> {{ scope.row.key }} </template>
          </el-table-column>
          <el-table-column prop="value" label="value" min-width="100">
            <template slot-scope="scope"> {{ scope.row.value }} </template>
          </el-table-column>
          <el-table-column prop="create_time" label="create_time" min-width="100">
            <template slot-scope="scope"> {{ scope.row.create_time }} </template>
          </el-table-column>
          <el-table-column prop="remarks" label="remarks" min-width="100">
            <template slot-scope="scope"> {{ scope.row.remarks }} </template>
          </el-table-column>
          <el-table-column label="操作" min-width="100">
            <template  slot-scope="scope">
              <el-button type="danger" @click="deletedata(scope.row)" small>删除</el-button>
              <el-button type="warning" @click="getData(scope.row)" small>修改</el-button>
              <el-dialog title="configData" :visible.sync="update_dialogVisible">
                <el-form :model="updateData" :rules="rules" ref="updateData">
                    <el-form-item label="id">
                        <el-input v-model="updateData.id" :placeholder="scope.row.id" :disabled="true"></el-input>
                    </el-form-item>
                    <el-form-item label="key" prop="key">
                        <el-input v-model="updateData.key" :placeholder="scope.row.key"></el-input>
                    </el-form-item>
                    <el-form-item label="value" prop="value">
                        <el-input v-model="updateData.value" :placeholder="scope.row.value"></el-input>
                    </el-form-item>
                    <el-form-item label="remarks" prop="remarks">
                        <el-input v-model="updateData.remarks" :placeholder="scope.row.remarks"></el-input>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="cancelButton">取消</el-button>
                    <el-button type="primary" @click="updatedata()">确定</el-button>
                </div>
              </el-dialog>
            </template>
          </el-table-column>
        </el-table>
      </el-row>
    </div>
</template>

<script>
export default {
  data () {
    return {
      addData: {
        key: '',
        value: '',
        remarks: ''
      },
      updateData: {
        id: '',
        key: '',
        value: '',
        remarks: ''
      },
      add_dialogVisible: false,
      update_dialogVisible: false,
      configDatalist: [],
      rules: {
        key: [
          {required: true, message: '配置名称', trigger: 'blur'},
          {min: 3, max: 20, message: '长度在3-20个字符', trigger: 'blur'}
        ],
        value: [
          {required: true, message: '配置描述', trigger: 'blur'},
          {min: 3, max: 20, message: '长度在3-20个字符', trigger: 'blur'}
        ],
        remarks: [
          {required: true, message: '备注', trigger: 'blur'},
          {min: 3, max: 20, message: '长度在3-20个字符', trigger: 'blur'}
        ]
      }
    }
  },
  created () {
    this.showconfigdata()
  },
  methods: {
    showconfigdata () {
      this.axios.get('/api/checkconfig')
        .then((res) => {
          this.configDatalist = Object.values(res.data.data)
        })
        .catch(error => {
          console.error('Error fetching data:', error)
        })
    },
    addconfigdata () {
      var params = {
        key: this.addData.key,
        value: this.addData.value,
        remarks: this.addData.remarks
      }
      this.axios.post('/api/addconfigdata', params)
        .then((res) => {
          console.log(params)
          this.showconfigdata()
          this.addData = {
            key: '',
            value: '',
            remarks: ''
          }
          this.add_dialogVisible = false
          this.$message({
            message: '添加成功',
            type: 'success'
          })
        })
    },
    deletedata (row) {
      var params = {
        id: row.id
      }
      this.$confirm('确定要删除吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.axios.post('/api/deleteconfigdata', params)
          .then((res) => {
            this.showconfigdata()
            this.$message({
              message: '删除成功',
              type: 'success'
            })
          })
          .catch(error => {
            console.error('Error fetching data:', error)
            this.$message({
              message: '删除失败',
              type: 'danger'
            })
          })
      })
    },
    getData (row) {
      this.update_dialogVisible = true
      this.updateData = {
        id: row.id,
        key: row.key,
        value: row.value,
        remarks: row.remarks
      }
    },
    updatedata () {
      var params = {
        id: this.updateData.id,
        key: this.updateData.key,
        value: this.updateData.value,
        remarks: this.updateData.remarks
      }
      this.$confirm('确定要修改吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.axios.post('/api/updataconfigdata', params)
          .then((res) => {
            this.showconfigdata()
            this.$message({
              message: '修改成功',
              type: 'success'
            })
          })
          .catch(error => {
            console.error('Error fetching data:', error)
            this.$message({
              message: '修改失败',
              type: 'danger'
            })
          })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消修改'
        })
      })
      this.update_dialogVisible = false
    },
    cancelButton () {
      this.addData = {
        id: '',
        key: '',
        value: '',
        remarks: ''
      }
      this.updateData = {
        id: '',
        key: '',
        value: '',
        remarks: ''
      }
      this.add_dialogVisible = false
      this.update_dialogVisible = false
    }
  }
}
</script>

<style>
.el-dialog__header {
    padding-left: 1px; /* 设置对话框头部标题左边距 */
    padding-top: 10px; /* 设置对话框头部标题上边距 */
    padding-bottom: 1px; /* 设置对话框头部标题底部边距 */
    padding-right: 1px; /* 设置对话框头部标题右边距 */
}
.el-table {
    line-height: 30px; /* 设置表格行高 */
}
</style>
