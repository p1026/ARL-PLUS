upfinger-info.vue
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
        v-model="listQuery.keyword"
        placeholder="关键字"
        style="width: 200px"
        class="filter-item"
        @keyup.enter.native="handleFilter"
      />
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <el-input
        v-model="listQuery.status"
        placeholder="状态"
        style="width: 200px"
        class="filter-item"
        @keyup.enter.native="handleFilter"
      />
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        {{ $t('table.search') }}
      </el-button>
      <br>
      <br>
      <el-button type="success" class="filter-item" @click="gitlstask">添加任务</el-button>
      <el-button type="danger" class="filter-item" @click="gitlsbatchDelect">批量删除</el-button>
      <el-button type="warning" class="filter-item" @click="gitlsbatchStop">批量停止</el-button>
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
      <el-table-column label="名称" min-width="129px" align="center">
        <template slot-scope="{row}">
          <span class="link-type" @click="togithubdata(row)">{{ row.name }}</span>
        </template>
      </el-table-column>

      <el-table-column label="关键字" min-width="120px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.keyword }}</span>
        </template>
      </el-table-column>
      <el-table-column label="cron" min-width="200px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.cron }}</span>
        </template>
      </el-table-column>
      <el-table-column label="状态" min-width="89px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.status }}</span>
        </template>
      </el-table-column>
      <el-table-column label="运行次数" width="180px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.run_number }}</span>
        </template>
      </el-table-column>
      <el-table-column label="上次运行" width="180px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.last_run_date }}</span>
        </template>
      </el-table-column>
      <el-table-column label="下次运行" width="250px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.next_run_date }}</span>
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('table.actions')"
        align="center"
        width="400"
        class-name="small-padding fixed-width"
      >
        <template slot-scope="{row}">
          <el-button size="mini" type="danger" @click="gitlsbatchDelect1(row)">
            {{ $t('table.delete') }}
          </el-button>
          <el-button size="mini" type="warning" @click="gitlsbatchStop1(row)" :disabled=" row.status === 'stop'">
            {{ $t('table.draft') }}
          </el-button>
          <el-button size="mini" type="success" @click="gitlsrecover(row)" :disabled=" row.status === 'running'">
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
    <el-dialog title="新建任务" :visible.sync="dialogVisible">
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
        <el-form-item label="关键字" required>
          <el-input v-model="temp.keyword" />
        </el-form-item>
        <el-form-item label="cron" required>
          <el-input v-model="temp.cron" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addlstask">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import {
  updateArticle,
  startArticle,
  stopArticle,
  gitlscreate, gitcronList, gitlsDelect, gitlsStop, gitlsRecover
} from '@/api/article'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination'
import Cookies from 'js-cookie'

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
      token: Cookies.get('Admin-Token'),
      dialogVisible: false,
      tableKey: 0,
      list: null,
      sels: '', // 当前选框选中的值
      total: 0,
      listQuery: {
        page: 1,
        size: 10,
        keyword: '',
        name: '',
        status: ''
      },
      sortOptions: [{ label: '升序', key: 'target' }, { label: '降序', key: '-target' }],
      statusOptions: ['test', 'big'],
      srcptOptions: ['test', 'top100', 'top1000', 'all'],
      levelptOptions: ['test', 'top100', 'top1000', 'all'],
      showReviewer: false,
      temp: {
        keyword: '',
        name: '',
        cron: '',
        domain_brute_type: 'big',
        port_scan_type: 'top100'
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
    addlstask() {
      this.dialogVisible = false
      const result = {
        keyword: this.temp.keyword,
        name: this.temp.name,
        cron: this.temp.cron
      }
      if (!this.temp.name) {
        this.$message({
          message: '名称不能为空',
          type: 'warning'
        })
        this.dialogVisible = false
      }
      gitlscreate(result).then(response => {
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
      })
        .catch(error => {
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
    gitlstask() {
      // eslint-disable-next-line no-sequences
      this.dialogStatus = 'create'
      this.dialogVisible = true
    },
    getList() {
      this.listLoading = true
      gitcronList(this.listQuery).then(response => {
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
    togithubdata(row) {
      this.$router.push({
        path: '/github/githubdata-info',
        query: {
          _id: row._id
        }
      })
    },
    handleSelectionChange(sels) {
      this.sels = sels
    },
    gitlsrecover(row) {
      // 删除前的提示
      const data = {
        _id: [row._id]
      }
      gitlsRecover(data).then(response => {
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
    // 批量删除执行操作
    gitlsbatchDelect() {
      // 删除前的提示
      this.$confirm('确认删除记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        const data = {
          _id: this.sels.map((item) => item._id)
        }

        gitlsDelect(data).then(response => {
          if (response.code === 200) {
            // 如果返回的code不是200，则显示错误信息
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
    gitlsbatchDelect1(row) {
      // 删除前的提示
      this.$confirm('确认删除记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        const data = {
          _id: [row._id]
        }
        gitlsDelect(data).then(response => {
          if (response.code === 200) {
            // 如果返回的code不是200，则显示错误信息
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
    gitlsbatchStop() {
      const data = {
        _id: this.sels.map((item) => item._id)
      }
      gitlsStop(data).then(response => {
        if (response.code === 200) {
          // 如果返回的code不是200，则显示错误信息
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
    gitlsbatchStop1(row) {
      const data = {
        _id: [row._id]
      }
      gitlsStop(data).then(response => {
        if (response.code === 200) {
          // 如果返回的code不是200，则显示错误信息
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
