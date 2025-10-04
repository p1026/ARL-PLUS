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
        v-model="listQuery.human_rule"
        placeholder="规则"
        style="width: 200px"
        class="filter-item"
        @keyup.enter.native="handleFilter"
      />
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        {{ $t('table.search') }}
      </el-button>
      <br><br>
      <el-upload
        ref="upload"
        action="/fingerprint/upload/"
        :headers="{'Token': `${token}`}"
        :auto-upload="true"
        :on-success="handleUploadSuccess"
      >
        <el-button slot="trigger" size="small" type="primary">选取json文件</el-button>
      </el-upload>
      <br>
      <el-button type="success" class="filter-item" @click="upfig">新建指纹</el-button>
      <el-button type="danger" class="filter-item" @click="figbatchDelect">批量删除</el-button>
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
      <el-table-column label="名称" min-width="89px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="规则" width="570px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.human_rule }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.update_time')" width="650px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.update_date }}</span>
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
    <el-dialog title="新建指纹" :visible.sync="dialogVisible">
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
            v-model="temp.human_rule"
            :autosize="{ minRows: 4, maxRows: 8}"
            type="textarea"
            placeholder="只支持body, title, header, icon_hash 四个字段，仅仅可以使用逻辑或， 如 body=Powered by WordPress!"
          />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addfig">确 定</el-button>
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
  pocSync, upfigList, figcreate, figDelect
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
        order_name: 'update_date',
        name: '',
        human_rule: ''
      },
      sortOptions: [{ label: '升序', key: 'target' }, { label: '降序', key: '-target' }],
      statusOptions: ['test', 'big'],
      srcptOptions: ['test', 'top100', 'top1000', 'all'],
      levelptOptions: ['test', 'top100', 'top1000', 'all'],
      showReviewer: false,
      temp: {
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
    handleUploadSuccess(response, file, fileList) {
      // TODO: 根据实际返回值结构来判断
      if (response.code === 200) {
        this.$notify({
          title: '成功',
          message: '上传成功',
          type: 'success'
        })
      } else {
        this.$notify({
          title: '失败',
          message: response.message || '上传失败',
          type: 'error'
        })
      }
    },
    addfig() {
      this.dialogVisible = false
      const result = {
        human_rule: this.temp.human_rule,
        name: this.temp.name
      }
      if (!this.temp.name) {
        this.$message({
          message: '名称不能为空',
          type: 'warning'
        })
        return
      }
      figcreate(result).then(response => {
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
    upfig() {
      // eslint-disable-next-line no-sequences
      this.dialogStatus = 'create'
      this.dialogVisible = true
    },
    getList() {
      this.listLoading = true
      upfigList(this.listQuery).then(response => {
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
    figbatchDelect() {
      // 删除前的提示
      this.$confirm('确认删除记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        const data = {
          _id: this.sels.map((item) => item._id)
        }
        figDelect(data).then(response => {
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
