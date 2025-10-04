<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="localListQuery.plugin"
        :placeholder="$t('table.vul')"
        style="width: 200px;"
        class="filter-item"
        @keyup.enter.native="handleFilter"
      />
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        {{ $t('table.search') }}
      </el-button>
    </div>

    <el-table
      :key="tableKey"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="sortChange"
    >
      <el-table-column type="index" :index="indexMethod" align="center" width="60" label="序号" />
      <el-table-column type="expand" label="细节" width="60">
        <template slot-scope="props">
          <span style="font-weight: bold;">
            路径：
          </span>
          <span>
            {{ props.row.detail.addr }}
          </span>
          <br><br>
          <span style="font-weight: bold;">
            payload：
          </span>
          <span>
            {{ props.row.detail.payload }}
          </span>
          <br><br>
          <span style="font-weight: bold;">
            Links：
          </span>
          <span>
            {{ props.row.detail.extra.Links ? props.row.detail.extra.Links[0] : '-' }}
          </span>
          <br><br>
          <span style="font-weight: bold;">
            Params：
          </span>
          <span>
            {{ props.row.detail.extra.param }}
          </span>
          <br><br>
          <span style="font-weight: bold;">
            数据包：
          </span>
          <br><br>
          <span>请求1：<div style="overflow-x: auto; white-space: nowrap;"><pre><div v-for="(str, index) in props.row.detail.snapshot[0]" :key="index">{{ str }}</div></pre></div></span>
          <br>
          <span>请求2：<div style="overflow-x: auto; white-space: nowrap;"><pre><div v-for="(str, index) in props.row.detail.snapshot[1]" :key="index">{{ str }}</div></pre></div></span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.target')" min-width="180px" align="center">
        <template slot-scope="{ row }">
          <a :href="row.target.url" class="link-type" target="_blank">{{ row.target.url }}</a>
        </template>
      </el-table-column>
      <el-table-column label="漏洞插件" width="450px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.plugin }}</span>
        </template>
      </el-table-column>
      <el-table-column label="保存时间" width="250px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.save_date }}</span>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="localListQuery.page"
      :limit.sync="localListQuery.size"
      @pagination="searchgetList"
    />
  </div>
</template>

<script>
import {
  fetchPv,
  createArticle,
  updateArticle,
  startArticle,
  stopArticle,
  deleteArticle,
  xrayList
} from '@/api/article'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

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
  isFullScreen: false,
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    },
    typeFilter(type) {
      return calendarTypeKeyValue[type]
    }
  },
  props: {
    // eslint-disable-next-line vue/require-default-prop
    listQuery: Object,
    row: Object// 定义要传递的参数
  },
  data() {
    return {
      localListQuery: {},
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      importanceOptions: [1, 2, 3],
      sortOptions: [{ label: '升序', key: '+id' }, { label: '降序', key: '-id' }],
      showReviewer: false,
      temp: {
        id: undefined,
        importance: 1,
        remark: '',
        timestamp: new Date(),
        title: '',
        type: '',
        status: 'published'
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      dialogPvVisible: false,
      pvData: [],
      rules: {
        type: [{ required: true, message: '类型不能为空', trigger: 'change' }],
        domain: [{ required: true, message: '域名不能为空', trigger: 'change' }],
        name: [{ required: true, message: '厂商不能为空', trigger: 'blur' }]
      },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
    this.localListQuery = JSON.parse(JSON.stringify(this.listQuery))
    this.$set(this.localListQuery, 'plugin', '')
  },
  methods: {
    formatRequest(requestString) {
      if (!requestString) return ''
      const lines = requestString.split('\r\n')
      const formattedLines = lines.filter(line => line.trim() !== '')
      return formattedLines.join('\n')
    },
    getList() {
      this.listLoading = true
      xrayList(this.listQuery).then(response => {
        this.list = response.items
        this.total = response.total

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    searchgetList() {
      this.listLoading = true
      xrayList(this.localListQuery).then(response => {
        this.list = response.items
        this.total = response.total

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    handleFilter() {
      this.searchgetList()
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
    resetTemp() {
      this.temp = {
        id: undefined,
        timestamp: new Date(),
        status: ''
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
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          this.temp.id = 2 // mock a id
          createArticle(this.temp).then(() => {
            this.list.unshift(this.temp)
            this.dialogFormVisible = false
            this.$notify({
              title: '成功',
              message: '创建成功',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    indexMethod(index) {
      return index + 1
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.temp.timestamp = new Date(this.temp.timestamp)
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
          tempData.timestamp = +new Date(tempData.timestamp) // change Thu Nov 30 2017 16:41:05 GMT+0800 (CST) to 1512031311464
          updateArticle(tempData).then(() => {
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
    handleDelete(row, index) {
      deleteArticle(row)
      this.$notify({
        title: '成功',
        message: '删除成功',
        type: 'success',
        duration: 2000
      })
      this.list.splice(index, 1)
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
        const tHeader = ['id', 'name', 'domain', 'importance', 'status']
        const filterVal = ['id', 'name', 'domain', 'importance', 'status']
        const data = this.formatJson(filterVal)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'table-list'
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
      const sort = this.listQuery.sort
      return sort === `+${key}` ? 'ascending' : 'descending'
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
