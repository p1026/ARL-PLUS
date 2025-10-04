<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.name"
        placeholder="SRC名称"
        style="width: 200px"
        class="filter-item"
        @keyup.enter.native="handleFilter"
      />
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        {{ $t('table.search') }}
      </el-button>
      <br> <br>
      <el-button
        class="filter-item"
        style="margin-left: 10px;"
        type="success"
        @click="handleCreate"
      >
        新增SRC
      </el-button>
    </div>

    <el-table
      :key="tableKey"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @selection-change="handleSelectionChange"
      @sort-change="sortChange"
    >
      <el-table-column type="selection" width="40" /> <!-- 添加复选框列 -->
      <el-table-column type="index" :index="indexMethod" align="center" width="60" label="序号" />
      <el-table-column :label="$t('table.groupname')" min-width="70px" align="center">
        <template slot-scope="{row}">
          <span >
            {{ row.name }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="地址" min-width="200px" align="center">
        <template slot-scope="{row}">
          <a class="link-type" :href="row.url" target="_blank"> {{ row.url }} </a>
        </template>
      </el-table-column>
      <el-table-column label="活跃度" width="200px" align="center">
        <template slot-scope="{row}">
          <span> {{row.level}} </span>
        </template>
      </el-table-column>
      <el-table-column label="范围" width="200px" align="center">
        <template slot-scope="{row}">
          <div v-for="item in row.range" :key="item">
            <span class="el-tag el-tag--success el-tag--medium el-tag--light">{{ item }}</span>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="礼品" width="200px" align="center">
        <template slot-scope="{row}">
          <div v-for="item in row.gift" :key="item">
            <span class="el-tag el-tag--success el-tag--medium el-tag--light" >{{ item }}</span><br>
          </div>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.actions')" align="center" width="300" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button size="mini" type="success" @click="handleUpdate(row)">
            编辑
          </el-button>
          <el-button size="mini" type="danger" @click="batchDelect1(row)">
            {{ $t('table.delete') }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.size" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temp"
        label-position="left"
        label-width="70px"
        style="width: 400px; margin-left:50px;"
      >
        <el-form-item label="名称" required>
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="地址" required>
          <el-input v-model="temp.url" />
        </el-form-item>
        <el-form-item label="活跃度" required>
          <el-select v-model="temp.level" class="filter-item">
            <el-option v-for="item in levelData" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="范围" required>
          <el-select v-model="temp.range" size="small" multiple collapse-tags style="width:330px" filterable>
            <div class="select_up">
              <el-button type="text" @click="selectAll">
                <i class="jw jw-quanxuan " />
                全选</el-button>
              <el-button type="text" @click="removeTag">
                <i class="jw jw-qingkong " />
                清空</el-button>
            </div>
            <div class="select_list" style="width: 330px">
              <el-option v-for="item in rangeData" :key="item" :label="item" :value="item" />
            </div>
          </el-select>
        </el-form-item>
        <el-form-item label="奖励" required>
          <el-select v-model="temp.gift" size="small" multiple collapse-tags style="width:330px" filterable>
            <div class="select_up">
              <el-button type="text" @click="selectAll1">
                <i class="jw jw-quanxuan " />
                全选</el-button>
              <el-button type="text" @click="removeTag1">
                <i class="jw jw-qingkong " />
                清空</el-button>
            </div>
            <div class="select_list" style="width: 330px">
              <el-option v-for="item in giftData" :key="item" :label="item" :value="item" />
            </div>
          </el-select>
        </el-form-item>
        <br><br>
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          {{ $t('table.cancel') }}
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          {{ $t('table.confirm') }}
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<style>
.form-container {
  display: grid;
  grid-template-columns: 1fr;
}

.el-select-dropdown__list {
  height: 100%;
  overflow: hidden;

}
.scrollable {
  width: 100%;
  height: 100px;
  overflow: hidden;
  display: flex;
  flex-wrap: wrap; /* 允许项目换行 */
}

.scrollable:hover {
  overflow-y: auto;
}

.select_up {
  padding: 0 12px;
  font-size: 14px;
  position: absolute;
  z-index: 99999;
  background-color: white;
  top: 0px;
  width: 100%;
  border-radius: 5px 5px 0 0;

  ::v-deep .el-button {
    color: #bcbcbc;
    font-size: 14px;

    i {
      font-size: 14px;
    }
  }

  ::v-deep .el-button:hover {
    color: #409EFF;
  }

  .el-button+.el-button {
    margin-left: 6px;
  }
}

.select_list {
  margin-top: 25px;
}

</style>

<script>
import {
  fetchPv,
  policyGroup,
  listtaskGroup,
  sitetaskGroup,
  srcList, addSrc, updateSrc, batchdeletesrc
} from '@/api/article'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination'

const calendarTypeOptions = [
  { key: 'CN', display_name: 'China' },
  { key: 'US', display_name: 'USA' },
  { key: 'JP', display_name: 'Japan' },
  { key: 'EU', display_name: 'Eurozone' }
]

// arr to obj, such as { CN : "China", US : "USA" }
const calendarTypeKeyValue = calendarTypeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'ComplexTable',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        done: 'success',
        error: 'danger'
      }
      return statusMap[status]
    },
    typeFilter(type) {
      return calendarTypeKeyValue[type]
    }
  },

  data() {
    return {
      rangeData: ['常规漏洞', '威胁情报', '隐私合规(安卓)', '隐私合规(IOS)'],
      giftData: ['京东卡', '周边', '现金'],
      levelData: ['活跃', '一般', '沉寂'],
      policyid: [],
      dialogVisible: false,
      orgData: [],
      tableKey: 0,
      list: null,
      sels: '', // 当前选框选中的值
      total: 0,
      listLoading: true,
      listQuery: {
        _id: '',
        page: 1,
        size: 10
      },
      sortOptions: [{ label: '升序', key: 'target' }, { label: '降序', key: '-target' }],
      statusOptions: ['test', 'big'],
      srcptOptions: ['test', 'top100', 'top1000', 'all'],
      levelptOptions: ['domain', 'ip'],
      taskOptions: [],
      taskOption: [],
      showReviewer: false,
      temp: {
        range: [],
        gift: [],
        url: '',
        name: '',
        level: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      listentask: {
        create: 'Task',
        site: 'Site'
      },
      listensite: {
        create: 'Create'
      },
      dialogPvVisible: false,
      pvData: [],
      downloadLoading: false
    }
  },
  created() {
    this.listQuery._id = this.$route.query._id
    this.listQuery.scope_id = this.$route.query.scope_id
    this.getList()
  },
  methods: {
    removeTag() {
      this.temp.range = []
    },
    selectAll() {
      this.temp.range = this.rangeData
    },
    removeTag1() {
      this.temp.gift = []
    },
    selectAll1() {
      this.temp.gift = this.giftData
    },
    getList() {
      this.listLoading = true
      srcList(this.listQuery).then(response => {
        this.list = response.items
        this.total = response.total
        this.taskOptions = response.items.map(item => item.scope_array)

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1 * 1000)
      })
    },
    indexMethod(index) {
      return index + 1
    },
    handleFilter() {
      this.getList()
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    resetTemp() {
      this.temp = {
        scope_type: '',
        name: '',
        scope: ''
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    grouptaskCreate(row) {
      this.dialogStatus = 'create'
      const idx = this.newindexMethod(row._id)
      this.temp.scope_id = row._id
      this.temp.name = ''
      this.orgData = []
      this.temp.policy_id = ''
      this.temp.interval = 24
      this.taskOption = this.taskOptions[idx]
      this.dialogVisible = true
      policyGroup(1000).then(response => {
        this.policyid = response.items
      })
    },
    groupsiteCreate(row) {
      this.dialogStatus = 'site'
      this.temp.scope_id = row._id
      this.temp.interval = 24
      this.dialogVisible = true
    },
    createData() {
      this.dialogVisible = false
      this.$refs['dataForm'].validate((valid) => {
        const data = {
          name: this.temp.name,
          url: this.temp.url,
          level: this.temp.level,
          range: this.temp.range,
          gift: this.temp.gift
        }
        addSrc(data).then(response => {
          if (response.code === 200) {
            this.dialogFormVisible = false
            this.$notify({
              title: '成功',
              message: '创建成功',
              type: 'success',
              duration: 2000
            })
            this.getList()
          }
        }).catch(error => {
          // 处理请求异常
          this.$notify({
            title: '失败',
            message: error.message,
            type: 'error',
            duration: 2000
          })
        })
      })
    },
    handleUpdate(row) {
      // eslint-disable-next-line no-sequences
      this.temp.name = row.name
      this.temp._id = row._id
      this.temp.url = row.url
      this.temp.level = row.level
      this.temp.range = row.range
      this.temp.gift = row.gift
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    listTask() {
      this.dialogVisible = false
      const data = {
        name: this.temp.name ? this.temp.name : '',
        interval: this.temp.interval * 3600,
        domain: this.orgData.join(','),
        policy_id: this.temp.policy_id,
        scope_id: this.temp.scope_id
      }
      listtaskGroup(data).then(response => {
        if (response.code === 200) {
          this.$notify({
            title: '成功',
            message: '创建成功',
            type: 'success',
            duration: 2000
          })
        }
      }).catch(error => {
        // 处理请求异常
        this.$notify({
          title: '失败',
          message: error.message,
          type: 'error',
          duration: 2000
        })
      })
    },
    siteTask() {
      this.dialogVisible = false
      const data = {
        interval: this.temp.interval * 3600,
        scope_id: this.temp.scope_id
      }
      sitetaskGroup(data).then(response => {
        if (response.code === 200) {
          this.$notify({
            title: '成功',
            message: response.message,
            type: 'success',
            duration: 2000
          })
        }
      }).catch(error => {
        // 处理请求异常
        this.$notify({
          title: '失败',
          message: error.message,
          type: 'error',
          duration: 2000
        })
      })
    },
    newindexMethod(id) {
      // 假设 this.tableData 是你的表格数据
      return this.list.findIndex(row => row._id === id)
    },
    handleSelectionChange(sels) {
      this.sels = sels
    },

    batchDelect1(row) {
      console.log(row._id)
      // 删除前的提示
      this.$confirm('确认删除记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        const data = {
          _id: row._id
        }
        batchdeletesrc(data)
        this.$notify({
          title: '成功',
          message: '删除成功',
          type: 'success',
          duration: 2000
        })
        this.getList()
      })
    },
    handleFetchPv(pv) {
      fetchPv(pv).then(response => {
        this.pvData = response.data.pvData
        this.dialogPvVisible = true
      })
    },
    updateData() {
      this.dialogVisible = false
      this.$refs['dataForm'].validate((valid) => {
        const tempData = {
          _id: this.temp._id,
          name: this.temp.name,
          url: this.temp.url,
          level: this.temp.level,
          range: this.temp.range,
          gift: this.temp.gift
        }
        updateSrc(tempData).then(response => {
          if (response.code === 200) {
            this.dialogFormVisible = false
            this.$notify({
              title: '成功',
              message: '更新成功',
              type: 'success',
              duration: 2000
            })
            this.getList()
          }
        }).catch(error => {
          // 处理请求异常
          this.$notify({
            title: '失败',
            message: error.message,
            type: 'error',
            duration: 2000
          })
        })
      })
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['任务', '目标', '状态', '开始时间', '结束时间']
        const filterVal = ['name', 'target', 'status', 'start_time', 'end_time']
        const data = this.formatJson(filterVal)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: '任务表'
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal) {
      return this.list.map(v => filterVal.map(j => {
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    },
    getSortClass: function(key) {
      const order = this.listQuery.order
      return order === `+${key}` ? 'ascending' : 'descending'
    }
  }
}
</script>
<style scoped>
.scrollable {
  width: 100%;
  height: 80px;
  overflow: hidden;
}

.scrollable:hover {
  overflow-y: auto;
}

</style>
