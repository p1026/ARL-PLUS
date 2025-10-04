<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.name"
        placeholder="名称"
        style="width: 200px"
        class="filter-item"
        @keyup.enter.native="handleFilter"
      />
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <el-input
        v-model="listQuery.target"
        placeholder="目标"
        style="width: 200px"
        class="filter-item"
        @keyup.enter.native="handleFilter"
      />
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <el-input
        v-model="listQuery.schedule_type"
        placeholder="计划类型"
        style="width: 200px"
        class="filter-item"
        @keyup.enter.native="handleFilter"
      />
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        {{ $t('table.search') }}
      </el-button>
      <br><br>
      <el-button type="success" class="filter-item" @click="schedulecreate">新建计划</el-button>
      <el-button type="danger" class="filter-item" @click="schedulebatchDelect">批量删除</el-button>
      <el-button type="warning" class="filter-item" @click="schedulebatchstop">批量停止</el-button>
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
      <el-table-column label="任务名" min-width="89px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="目标" width="200px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.target }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.type')" width="150px" align="center">
        <template slot-scope="{row}">
          <span>
            {{ row.task_tag === 'task' ? '资产任务' : (row.task_tag === 'risk_cruising' ? '风险任务' : '') }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="150px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.status }}</span>
        </template>
      </el-table-column>
      <el-table-column label="策略" width="200px" align="center">
        <template slot-scope="{row}">
          <span class="link-type" @click="tocron(row)">{{ row.policy_name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="时间配置" width="150px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.start_date }}</span>
        </template>
      </el-table-column>
      <el-table-column label="上次运行" width="170px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.last_run_date }}</span>
        </template>
      </el-table-column>
      <el-table-column label="下次运行" width="170px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.next_run_date }}</span>
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('table.actions')"
        align="center"
        width="250"
        class-name="small-padding fixed-width"
      >
        <template slot-scope="{row}">
          <el-button size="mini" type="danger" @click="schedulebatchDelect1(row)">
            {{ $t('table.delete') }}
          </el-button>
          <el-button size="mini" type="warning" :disabled="row.status === 'stop'" @click="schedulebatchstop1(row)">
            {{ $t('table.draft') }}
          </el-button>
          <el-button size="mini" type="success" :disabled="row.status === 'scheduled'" @click="schedulerecover(row)">
            恢复
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.size"
      @pagination="getList"
    />
    <el-dialog title="新建计划任务" :visible.sync="dialogVisible">
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
        <el-form-item :label="$t('table.target')" required>
          <el-input
            v-model="temp.target"
            :autosize="{ minRows: 2, maxRows: 4}"
            type="textarea"
          />
        </el-form-item>
        <el-form-item label="类型" required>
          <el-select v-model="temp.schedule_type" class="filter-item">
            <el-option v-for="item in scheduleOptions" :key="item.key" :label="item.label" :value="item.key" />
          </el-select>
        </el-form-item>
        <el-form-item label="策略" required>
          <el-select v-model="temp.policy_id" class="filter-item">
            <el-option v-for="item in ruleOption" :key="item._id" :label="item.name" :value="item._id" />
          </el-select>
        </el-form-item>
        <div v-if="temp.schedule_type === 'future_scan'">
          <el-form-item label="时间" required>
            <el-date-picker
              v-model="temp.start_date"
              type="datetime"
              placeholder="选择日期时间"
              align="right"
              :picker-options="pickerOptions"
            />
          </el-form-item>
        </div>
        <div v-if="temp.schedule_type === 'recurrent_scan'">
          <el-form-item label="cron" required>
            <el-input v-model="temp.cron" />
          </el-form-item>
        </div>
        <el-form-item label="类别" required>
          <el-select v-model="temp.task_tag" class="filter-item">
            <el-option v-for="item in tasktagOption" :key="item.key" :label="item.label" :value="item.key" />
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addplantask">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import {
  fetchPv,
  updateArticle,
  startArticle,
  stopArticle,
  pocSync, policyPlan, schedulecreate, scheduleList, scheduleDelect, scheduleRecover, scheduleStop
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
      tasktagOption: [{ label: '资产发现任务', key: 'task' }, { label: '风险巡航任务', key: 'risk_cruising' }],
      ruleOption: [],
      pickerOptions: {
        shortcuts: [{
          text: '今天',
          onClick(picker) {
            picker.$emit('pick', new Date())
          }
        }, {
          text: '昨天',
          onClick(picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24)
            picker.$emit('pick', date)
          }
        }, {
          text: '一周前',
          onClick(picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24 * 7)
            picker.$emit('pick', date)
          }
        }]
      },
      value1: '',
      value2: '',
      value3: '',
      dialogVisible: false,
      tableKey: 0,
      list: null,
      sels: '', // 当前选框选中的值
      total: 0,
      listQuery: {
        page: 1,
        size: 10,
        name: '',
        schedule_type: ''
      },
      sortOptions: [{ label: '升序', key: 'target' }, { label: '降序', key: '-target' }],
      scheduleOptions: [{ label: '定时任务', key: 'future_scan' }, { label: '周期任务', key: 'recurrent_scan' }],
      statusOptions: ['test', 'big'],
      srcptOptions: ['test', 'top100', 'top1000', 'all'],
      levelptOptions: ['test', 'top100', 'top1000', 'all'],
      showReviewer: false,
      temp: {
        policy_id: '',
        schedule_type: '',
        start_date: '',
        task_tag: '',
        target: '',
        name: '',
        cron: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      dialogPvVisible: false,
      pvData: [],
      downloadLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    tocron(row) {
      this.$router.push({
        path: '/rule/rule-info',
        query: {
          _id: row.policy_id
        }
      })
    },
    addplantask() {
      this.dialogVisible = false
      const dateObj = new Date(this.temp.start_date)
      const formattedDate = dateObj.toLocaleString('zh-CN', { hour12: false }).replace(/\//g, '-')
      const result = {
        name: this.temp.name,
        policy_id: this.temp.policy_id,
        schedule_type: this.temp.schedule_type,
        target: this.temp.target,
        task_tag: this.temp.task_tag
      }
      if (this.temp.schedule_type === 'future_scan') {
        result.start_date = formattedDate
      } else if (this.temp.schedule_type === 'recurrent_scan') {
        result.cron = this.temp.cron
      }
      if (!this.temp.name) {
        this.$message({
          message: '名称不能为空',
          type: 'warning'
        })
        return
      }
      schedulecreate(result).then(response => {
        this.dialogFormVisible = false
        if (response.code === 200) {
          this.$notify({
            title: '成功',
            message: '创建成功',
            type: 'success',
            duration: 2000
          })
          this.getList()
        }
      }).catch(error => {
        // Handle the error
        console.error(error)
        this.$notify({
          title: '失败',
          message: error,
          type: 'error',
          duration: 2000
        })
      })
    },
    schedulecreate() {
      // eslint-disable-next-line no-sequences
      this.temp.schedule_type = ''
      this.temp.name = ''
      this.dialogStatus = 'create'
      this.dialogVisible = true
      this.size = 1000
      this.order = '-update_date'
      const newlistQ = {
        size: 1000,
        order: '-update_date'
      }
      policyPlan(newlistQ).then(response => {
        this.ruleOption = response.items

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1 * 1000)
      })
    },
    getList() {
      this.listLoading = true
      scheduleList(this.listQuery).then(response => {
        this.list = response.items
        this.total = response.total

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
    handleModifyStatus_stop(row, status) {
      stopArticle(row)
      this.$message({
        message: '操作成功',
        type: 'success'
      })
      row.status = status
    },
    handleModifyStatus_start(row, status) {
      startArticle(row)
      this.$message({
        message: '操作成功',
        type: 'success'
      })
      row.status = status
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    handleCreate() {
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          updateArticle(tempData.uid, tempData).then(() => {
            const index = this.list.findIndex(v => v.id === this.temp.id)
            this.list.splice(index, 1, this.temp)
            this.dialogFormVisible = false
            this.$notify({
              title: '成功',
              message: '更新成功',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleSelectionChange(sels) {
      this.sels = sels
    },
    // 批量删除执行操作
    figupload() {
      pocSync()
      this.$notify({
        title: '成功',
        message: '更新成功',
        type: 'success',
        duration: 2000
      })
      setTimeout(() => {
        location.reload()
      }, 1000)
    },
    schedulebatchDelect() {
      // 删除前的提示
      this.$confirm('确认删除记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        const data = {
          _id: this.sels.map((item) => item._id)
        }
        scheduleDelect(data).then(response => {
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
    schedulebatchDelect1(row) {
      // 删除前的提示
      this.$confirm('确认删除记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        const data = {
          _id: [row._id]
        }
        scheduleDelect(data).then(response => {
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
    schedulebatchstop() {
      const data = {
        _id: this.sels.map((item) => item._id)
      }
      scheduleStop(data).then(response => {
        if (response.code === 200) {
          this.$notify({
            title: '成功',
            message: '停止成功',
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
    },
    schedulerecover(row) {
      const data = {
        _id: [row._id]
      }
      scheduleRecover(data).then(response => {
        if (response.code === 200) {
          // 如果返回的code不是200，则显示错误信息
          this.$notify({
            title: '成功',
            message: '恢复成功',
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
    },
    schedulebatchstop1(row) {
      const data = {
        _id: [row._id]
      }
      scheduleStop(data).then(response => {
        if (response.code === 200) {
          this.$notify({
            title: '成功',
            message: '停止成功',
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
    },
    handleFetchPv(pv) {
      fetchPv(pv).then(response => {
        this.pvData = response.data.pvData
        this.dialogPvVisible = true
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
