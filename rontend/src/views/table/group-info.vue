<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.name"
        :placeholder="$t('table.groupname')"
        style="width: 200px"
        class="filter-item"
        @keyup.enter.native="handleFilter"
      />
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <el-input
        v-model="listQuery.scope"
        :placeholder="$t('table.grouprange')"
        style="width: 200px"
        class="filter-item"
        @keyup.enter.native="handleFilter"
      />
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <el-input
        v-model="listQuery._id"
        :placeholder="$t('table.groupid')"
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
        新建分组
      </el-button>
      <el-button type="danger" class="filter-item" @click="grouDelects">批量删除</el-button>
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
      <el-table-column :label="$t('table.grouprange')" min-width="200px" align="center">
        <template slot-scope="{row}">
          <div class="scrollable">
          <div v-for="item in row.scope_array" :key="item">
            <span class="el-tag el-tag--success el-tag--medium el-tag--light">{{ item }}</span>
            <i class="el-icon-close" @click="deleteItem(row._id, item)" />
          </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.type')" width="70px" align="center">
        <template slot-scope="{row}">
          <span v-if="row.scope_type === 'domain'">域名</span>
          <span v-else>IP</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.groupid')" width="220px" align="center">
        <template slot-scope="{row}">
          <span>{{ row._id }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.actions')" align="center" width="500" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">
            {{ $t('table.addgroup') }}
          </el-button>
          <el-button type="info" size="mini" @click="grouptaskCreate(row)">
            {{ $t('table.addlook') }}
          </el-button>
          <el-button size="mini" type="success" @click="groupsiteCreate(row)">
            {{ $t('table.addsitelook') }}
          </el-button>
          <el-button size="mini" type="danger" @click="grouDelect1(row._id)">
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
        <el-form-item :label="$t('table.type')" required>
          <el-select v-model="temp.scope_type" class="filter-item" :disabled="dialogStatus === 'update'">
            <el-option v-for="item in levelptOptions" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item :label="$t('table.groupname')" required>
          <el-input v-model="temp.name" :disabled="dialogStatus === 'update'" />
        </el-form-item>
        <el-form-item :label="$t('table.grouprange')" required>
          <el-input
            v-model="temp.scope"
            :autosize="{ minRows: 2, maxRows: 4}"
            type="textarea"
            placeholder="Please input"
          />
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

    <el-dialog :title="listentask[dialogStatus]" :visible.sync="dialogVisible">
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temps"
        label-position="left"
        label-width="70px"
        style="width: 400px; margin-left:50px;"
      >
        <el-form-item v-if="dialogStatus !== 'site'" :label="$t('table.grouprange')" required>
          <el-select v-model="orgData" size="small" multiple collapse-tags style="width: 500px" filterable>
            <div class="select_up">
              <el-button type="text" @click="selectAll">
                <i class="jw jw-quanxuan " />
                全选</el-button>
              <el-button type="text" @click="removeTag">
                <i class="jw jw-qingkong " />
                清空</el-button>
              <el-button type="text" @click="selectReverse">
                <i class="jw jw-fanxuan " />
                反选</el-button>
            </div>
            <div class="select_list" style="width: 500px">
              <el-option v-for="item in taskOption" :key="item" :label="item" :value="item" />
            </div>
          </el-select>
        </el-form-item>
        <el-form-item :label="$t('table.run_time')" required>
          <el-input-number v-model="temp.interval" :min="1" :max="1000" style="width: 500px" />
        </el-form-item>
        <el-form-item v-if="dialogStatus !== 'site'" :label="$t('table.rule')">
          <el-select v-model="temp.policy_id" class="filter-item" style="width: 500px">
            <el-option v-for="item in policyid" :key="item._id" :label="item.name" :value="item._id" style="width: 500px" />
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogStatus==='create'?listTask():siteTask()">确 定</el-button>
      </span>
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
  fetchPv, groupList, addGroup, grouDelect, addGrouprange, grouDelectscope, policyGroup, listtaskGroup, sitetaskGroup
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
        scope: '',
        interval: 24,
        domain: '',
        name: '',
        policy_id: '',
        scope_id: ''
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
      this.orgData = []
    },
    selectAll(val) {
      val = []
      this.taskOption.map(item => {
        val.push(item)
      })
      this.orgData = val
    },
    selectReverse(val) {
      val = []
      this.taskOption.map(item => {
        const index = this.orgData.indexOf(item)
        // eslint-disable-next-line no-empty
        if (index !== -1) {
        } else {
          val.push(item)
        }
      })
      this.orgData = val
    },
    getList() {
      this.listLoading = true
      groupList(this.listQuery).then(response => {
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
          scope: this.temp.scope,
          scope_type: this.temp.scope_type
        }
        addGroup(data).then(response => {
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
      this.temp.scope_type = row.scope_type
      this.temp._id = row._id
      this.temp.scope = ''
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
    // 批量删除执行操作
    grouDelects(id) {
      // 删除前的提示
      this.$confirm('确认删除记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        const data = {
          scope_id: this.sels.map((item) => item._id)
        }
        grouDelect(data).then(response => {
          if (response.code === 200) {
            this.$notify({
              title: '成功',
              message: '删除成功',
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
    grouDelect1(id) {
      // 删除前的提示
      this.$confirm('确认删除记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        const data = {
          scope_id: [id]
        }
        grouDelect(data).then(response => {
          if (response.code === 200) {
            this.$notify({
              title: '成功',
              message: '删除成功',
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
    deleteItem(scope_id, scope) {
      this.listLoading = false
      // 删除前的提示
      this.$confirm('确认删除记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        grouDelectscope(scope_id, scope).then(response => {
          if (response.code === 200) {
            this.$notify({
              title: '成功',
              message: '删除成功',
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
          scope_id: this.temp._id,
          scope: this.temp.scope
        }
        addGrouprange(tempData).then(response => {
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
