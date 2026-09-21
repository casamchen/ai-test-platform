<template>
  <div class="config-container">
    <!-- Page Header -->
    <div class="page-header">
      <h2 class="page-title">项目配置</h2>
      <div class="page-actions">
        <el-button type="primary" @click="add_dialogVisible = true">新增配置</el-button>
      </div>
    </div>

    <!-- Table Card -->
    <div class="table-card">
      <el-table :data="configDatalist" style="width: 100%" border>
        <el-table-column prop="id" label="ID" min-width="80">
          <template slot-scope="scope"> {{ scope.row.id }} </template>
        </el-table-column>
        <el-table-column prop="key" label="Key" min-width="120">
          <template slot-scope="scope"> {{ scope.row.key }} </template>
        </el-table-column>
        <el-table-column prop="value" label="Value" min-width="150">
          <template slot-scope="scope"> {{ scope.row.value }} </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" min-width="160">
          <template slot-scope="scope"> {{ scope.row.create_time }} </template>
        </el-table-column>
        <el-table-column prop="remarks" label="备注" min-width="150">
          <template slot-scope="scope"> {{ scope.row.remarks }} </template>
        </el-table-column>
        <el-table-column label="操作" min-width="180" fixed="right">
          <template slot-scope="scope">
            <el-button type="danger" size="small" @click="deletedata(scope.row)">删除</el-button>
            <el-button type="warning" size="small" @click="getData(scope.row)">修改</el-button>
            <el-dialog title="编辑配置" :visible.sync="update_dialogVisible" append-to-body>
              <el-form :model="updateData" :rules="rules" ref="updateData">
                <el-form-item label="ID">
                  <el-input v-model="updateData.id" :disabled="true"></el-input>
                </el-form-item>
                <el-form-item label="Key" prop="key">
                  <el-input v-model="updateData.key"></el-input>
                </el-form-item>
                <el-form-item label="Value" prop="value">
                  <el-input v-model="updateData.value"></el-input>
                </el-form-item>
                <el-form-item label="备注" prop="remarks">
                  <el-input v-model="updateData.remarks"></el-input>
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
    </div>

    <!-- Add Dialog -->
    <el-dialog title="新增配置" :visible.sync="add_dialogVisible">
      <el-form :model="addData" :rules="rules" ref="addData">
        <el-form-item label="Key" prop="key">
          <el-input v-model="addData.key"></el-input>
        </el-form-item>
        <el-form-item label="Value" prop="value">
          <el-input v-model="addData.value"></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="remarks">
          <el-input v-model="addData.remarks"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="cancelButton">取消</el-button>
        <el-button type="primary" @click="addconfigdata()">确定</el-button>
      </div>
    </el-dialog>
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
          {required: true, message: '请输入配置名称', trigger: 'blur'},
          {min: 3, max: 20, message: '长度在3-20个字符', trigger: 'blur'}
        ],
        value: [
          {required: true, message: '请输入配置值', trigger: 'blur'},
          {min: 3, max: 20, message: '长度在3-20个字符', trigger: 'blur'}
        ],
        remarks: [
          {required: true, message: '请输入备注', trigger: 'blur'},
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
              type: 'error'
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
              type: 'error'
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

<style scoped>
.config-container {
  padding: 24px;
  background-color: var(--bg-base);
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 20px 24px;
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
}

.page-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
}

.page-actions {
  display: flex;
  gap: 12px;
}

.table-card {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: 24px;
}

/* Element UI 深色主题覆盖 */
.table-card /deep/ .el-table {
  background-color: transparent;
  color: var(--text-primary);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
}

.table-card /deep/ .el-table th,
.table-card /deep/ .el-table tr {
  background-color: var(--bg-elevated);
  color: var(--text-primary);
}

.table-card /deep/ .el-table td {
  border-bottom: 1px solid var(--border-subtle);
  color: var(--text-secondary);
}

.table-card /deep/ .el-table--border::after,
.table-card /deep/ .el-table--group::after,
.table-card /deep/ .el-table::before {
  background-color: var(--border-subtle);
}

.table-card /deep/ .el-table__empty-block {
  background-color: var(--bg-elevated);
  color: var(--text-muted);
}

/* Dialog 深色主题 */
/deep/ .el-dialog {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
}

/deep/ .el-dialog__header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-subtle);
}

/deep/ .el-dialog__title {
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 600;
}

/deep/ .el-dialog__body {
  padding: 20px;
  color: var(--text-secondary);
}

/deep/ .el-dialog__footer {
  padding: 12px 20px;
  border-top: 1px solid var(--border-subtle);
}

/* Form 深色主题 */
/deep/ .el-form-item__label {
  color: var(--text-secondary);
}

/deep/ .el-input__inner {
  background-color: var(--bg-elevated);
  border-color: var(--border-subtle);
  color: var(--text-primary);
}

/deep/ .el-input__inner:focus {
  border-color: var(--color-primary-500);
}

/deep/ .el-input__inner::placeholder {
  color: var(--text-muted);
}

/deep/ .el-input.is-disabled .el-input__inner {
  background-color: var(--bg-base);
  color: var(--text-muted);
}
</style>
