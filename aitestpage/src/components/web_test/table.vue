<template>
  <div class="table-container">
    <!-- Page Header -->
    <div class="page-header">
      <h2 class="page-title">App 执行结果</h2>
      <div class="page-actions">
        <el-button type="success" @click="click_button_one">查询数据</el-button>
      </div>
    </div>

    <!-- Table Card -->
    <div class="table-card">
      <!-- 普通表格 -->
      <div class="table-section">
        <h3 class="section-title">普通表格</h3>
        <el-table :data="tableData" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80"></el-table-column>
          <el-table-column prop="name" label="姓名" width="120"></el-table-column>
          <el-table-column prop="age" label="年龄" width="80"></el-table-column>
          <el-table-column prop="sex" label="性别" width="80"></el-table-column>
        </el-table>
      </div>

      <!-- 边框表格 -->
      <div class="table-section">
        <h3 class="section-title">边框表格</h3>
        <el-table :data="tableData2" border>
          <el-table-column prop="id" label="ID"></el-table-column>
          <el-table-column prop="name" label="姓名"></el-table-column>
          <el-table-column prop="age" label="年龄"></el-table-column>
          <el-table-column prop="sex" label="性别"></el-table-column>
        </el-table>
      </div>

      <!-- 斑马纹表格 -->
      <div class="table-section">
        <h3 class="section-title">斑马纹表格</h3>
        <el-table :data="tableData2" border stripe>
          <el-table-column prop="id" label="ID"></el-table-column>
          <el-table-column prop="name" label="姓名"></el-table-column>
          <el-table-column prop="age" label="年龄"></el-table-column>
          <el-table-column prop="sex" label="性别"></el-table-column>
        </el-table>
      </div>

      <!-- 固定表头表格 -->
      <div class="table-section">
        <h3 class="section-title">固定表头表格</h3>
        <el-table :data="tableData1" stripe height="200">
          <el-table-column prop="date" label="日期" width="150"></el-table-column>
          <el-table-column prop="name" label="姓名" width="120"></el-table-column>
          <el-table-column prop="province" label="省份" width="120"></el-table-column>
          <el-table-column prop="city" label="市区" width="120"></el-table-column>
          <el-table-column prop="address" label="地址" width="300"></el-table-column>
        </el-table>
      </div>

      <!-- 固定列表格 -->
      <div class="table-section">
        <h3 class="section-title">固定列表格</h3>
        <el-table :data="tableData2" stripe @current-change="clickButton">
          <el-table-column prop="id" label="ID" fixed width="80"></el-table-column>
          <el-table-column prop="name" label="姓名" width="300"></el-table-column>
          <el-table-column prop="age" label="年龄" width="260"></el-table-column>
          <el-table-column prop="sex" label="性别" width="150" fixed="right"></el-table-column>
        </el-table>
      </div>

      <!-- 多级表格 -->
      <div class="table-section">
        <h3 class="section-title">多级表格</h3>
        <el-table :data="tableData1" style="width: 100%">
          <el-table-column prop="date" label="日期" width="150"></el-table-column>
          <el-table-column label="配送信息">
            <el-table-column prop="name" label="姓名" width="120"></el-table-column>
            <el-table-column label="地址">
              <el-table-column prop="province" label="省份" width="120"></el-table-column>
              <el-table-column prop="city" label="市区" width="120"></el-table-column>
              <el-table-column prop="address" label="地址" width="300"></el-table-column>
              <el-table-column prop="zip" label="邮编" width="120"></el-table-column>
            </el-table-column>
          </el-table-column>
        </el-table>
      </div>

      <!-- 单选表格 -->
      <div class="table-section">
        <h3 class="section-title">单选表格</h3>
        <el-table :data="tableData2" @current-change="clickButton">
          <el-table-column prop="id" label="ID" width="80"></el-table-column>
          <el-table-column prop="name" label="姓名" width="120"></el-table-column>
          <el-table-column prop="age" label="年龄" width="80"></el-table-column>
          <el-table-column prop="sex" label="性别" width="80"></el-table-column>
        </el-table>
      </div>

      <!-- 多选表格 -->
      <div class="table-section">
        <h3 class="section-title">多选表格</h3>
        <el-table :data="tableData2" @selection-change="handleSelectionChange">
          <el-table-column type="selection" width="55"></el-table-column>
          <el-table-column prop="id" label="ID" width="80"></el-table-column>
          <el-table-column prop="name" label="姓名" width="120"></el-table-column>
          <el-table-column prop="age" label="年龄" width="80"></el-table-column>
          <el-table-column prop="sex" label="性别" width="80"></el-table-column>
        </el-table>
      </div>

      <!-- 筛选表格 -->
      <div class="table-section">
        <h3 class="section-title">筛选表格</h3>
        <div class="filter-actions">
          <el-button size="small" @click="removeDate">清除日期过滤器</el-button>
          <el-button size="small" @click="removeTag">清除标签过滤器</el-button>
          <el-button size="small" @click="removeAll">清除所有过滤器</el-button>
        </div>
        <el-table :data="tableData3" ref="filterTable">
          <el-table-column sortable column-key="date" prop="date" label="日期" width="150"
            :filter-method="filterHandler"
            :filters="[{text: '2016-05-01', value: '2016-05-01'}, {text: '2016-05-02', value: '2016-05-02'}]">
          </el-table-column>
          <el-table-column prop="name" label="姓名" width="120"></el-table-column>
          <el-table-column prop="address" label="地址" width="300"></el-table-column>
          <el-table-column prop="tag" label="标签" width="150"
            :filter-method="filterTag"
            :filters="[{ text: '家', value: '家' }, { text: '公司', value: '公司' }]">
            <template slot-scope="scope">
              <el-tag :type="scope.row.tag === '家' ? '' : 'success'" disable-transitions>{{ scope.row.tag }}</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 搜索输入框表格 -->
      <div class="table-section">
        <h3 class="section-title">搜索输入框表格</h3>
        <el-table :data="tableData2.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))">
          <el-table-column prop="id" label="ID" width="80"></el-table-column>
          <el-table-column prop="name" label="姓名" width="120"></el-table-column>
          <el-table-column prop="age" label="年龄" width="80"></el-table-column>
          <el-table-column prop="sex" label="性别" width="80"></el-table-column>
          <el-table-column align="right" width="200">
            <template slot="header">
              <el-input v-model="search" size="mini" placeholder="输入关键字搜索"/>
            </template>
            <template slot-scope="scope">
              <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
              <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 尾行合计表格 -->
      <div class="table-section">
        <h3 class="section-title">尾行合计表格</h3>
        <el-table :data="tableData2" border show-summary>
          <el-table-column prop="id" label="ID" width="80"></el-table-column>
          <el-table-column prop="name" label="姓名" width="120"></el-table-column>
          <el-table-column prop="age" label="年龄" width="80"></el-table-column>
          <el-table-column prop="sex" label="性别" width="80"></el-table-column>
        </el-table>
      </div>

      <!-- 索引表格 -->
      <div class="table-section">
        <h3 class="section-title">索引表格</h3>
        <el-table :data="tableData2" border show-summary>
          <el-table-column type="index" label="#" width="60"></el-table-column>
          <el-table-column prop="id" label="ID" width="80"></el-table-column>
          <el-table-column prop="name" label="姓名" width="120"></el-table-column>
          <el-table-column prop="age" label="年龄" width="80"></el-table-column>
          <el-table-column prop="sex" label="性别" width="80"></el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      tableData1: [
        {date: '2016-05-03', name: '王小虎', province: '上海', city: '普陀区', address: '上海市普陀区金沙江路 1518 弄', zip: 102983},
        {date: '2022-05-03', name: '疯狂过', province: '深圳', city: '深圳', address: '广东省深圳市', zip: 325456},
        {date: '2009-05-03', name: '我都是', province: '长沙', city: '长沙', address: '湖南省长沙市', zip: 567213},
        {date: '2019-05-03', name: '夹克衫', province: '北京', city: '北京', address: '北京鸟巢', zip: 244512},
        {date: '2023-05-03', name: '黄小仙', province: '惠州', city: '大亚湾', address: '大牙哇==', zip: 222343},
        {date: '2004-05-03', name: '陈嘉嘉', province: '天津', city: '海边', address: '天津市海边', zip: 109283}
      ],
      tableData2: [
        {'id': 1, 'name': 'casam1', 'age': 23, 'sex': '男'},
        {'id': 2, 'name': 'casam2', 'age': 23, 'sex': '男'},
        {'id': 3, 'name': 'casam3', 'age': 23, 'sex': '男'},
        {'id': 4, 'name': 'casam4', 'age': 23, 'sex': '男'},
        {'id': 5, 'name': 'casam5', 'age': 23, 'sex': '男'}
      ],
      tableData3: [
        {date: '2016-05-01', name: '王小虎', address: '上海市普陀区金沙江路 1518 弄', tag: '家'},
        {date: '2016-05-02', name: '疯狂过', address: '广东省深圳市', tag: '公司'},
        {date: '2009-05-03', name: '我都是', address: '湖南省长沙市', tag: '公司'}
      ],
      tableData: [],
      search: ''
    }
  },
  methods: {
    click_button_one () {
      this.tableData = [
        {'id': 1, 'name': 'casam1', 'age': 23, 'sex': '男'},
        {'id': 2, 'name': 'casam2', 'age': 23, 'sex': '男'},
        {'id': 3, 'name': 'casam3', 'age': 23, 'sex': '男'},
        {'id': 4, 'name': 'casam4', 'age': 23, 'sex': '男'},
        {'id': 5, 'name': 'casam5', 'age': 23, 'sex': '男'}
      ]
      this.$message({
        message: '查询成功',
        type: 'success'
      })
    },
    clickButton (params) {
      this.$message({
        message: '选中的为' + params.id,
        type: 'success'
      })
    },
    handleSelectionChange (val) {
      // 多选处理
    },
    filterTag (value, row) {
      return row.tag === value
    },
    filterHandler (value, row, column) {
      const property = column['property']
      return row[property] === value
    },
    removeDate () {
      this.$refs.filterTable.clearFilter('date')
    },
    removeTag () {
      this.$refs.filterTable.clearFilter('tag')
    },
    removeAll () {
      this.$refs.filterTable.clearFilter()
    },
    handleEdit (index, row) {
      // 编辑处理
    },
    handleDelete (index, row) {
      // 删除处理
    }
  }
}
</script>

<style scoped>
.table-container {
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
  padding: 32px;
}

.table-section {
  margin-bottom: 40px;
}

.table-section:last-child {
  margin-bottom: 0;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 16px 0;
}

.filter-actions {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

/* Element UI Table 深色主题 */
/deep/ .el-table {
  background-color: transparent;
  color: var(--text-primary);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
}

/deep/ .el-table th,
/deep/ .el-table tr {
  background-color: var(--bg-elevated);
  color: var(--text-primary);
}

/deep/ .el-table td {
  border-bottom: 1px solid var(--border-subtle);
  color: var(--text-secondary);
}

/deep/ .el-table--border::after,
/deep/ .el-table--group::after,
/deep/ .el-table::before {
  background-color: var(--border-subtle);
}

/deep/ .el-table__empty-block {
  background-color: var(--bg-elevated);
  color: var(--text-muted);
}

/deep/ .el-table__body tr:hover > td {
  background-color: rgba(59, 130, 246, 0.08) !important;
}

/deep/ .el-table--striped .el-table__body tr.el-table__row--striped td {
  background-color: var(--bg-base);
}

/deep/ .el-table .cell {
  color: inherit;
}

/* Input 深色主题 */
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

/* Tag 深色主题 */
/deep/ .el-tag {
  background-color: var(--bg-elevated);
  border-color: var(--border-subtle);
  color: var(--text-secondary);
}

/deep/ .el-tag--primary {
  background-color: rgba(59, 130, 246, 0.15);
  border-color: var(--color-primary-500);
  color: var(--color-primary-500);
}

/deep/ .el-tag--success {
  background-color: rgba(34, 197, 94, 0.15);
  border-color: #22C55E;
  color: #22C55E;
}

/* Button 深色主题 */
/deep/ .el-button--default {
  background-color: var(--bg-elevated);
  border-color: var(--border-subtle);
  color: var(--color-primary-500) !important;
}

/deep/ .el-button--default span,
/deep/ .el-button--default i {
  color: var(--color-primary-500) !important;
}

/deep/ .el-button--default:hover {
  background-color: var(--color-primary-500);
  border-color: var(--color-primary-500);
}

/deep/ .el-button--default:hover span,
/deep/ .el-button--default:hover i {
  color: #FFFFFF !important;
}
</style>
