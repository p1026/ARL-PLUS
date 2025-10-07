<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.title" :placeholder="$t('table.website')" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-select v-model="listQuery.sort" style="width: 80px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        {{ $t('table.search') }}
      </el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">
        {{ $t('table.export') }}
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
      <el-table-column :label="$t('table.website')" min-width="160px" align="center">
        <template slot-scope="{ row }">
          <a class="link-type" :href="row.site" target="_blank">{{ row.site }}</a>
          <br>
          <img :src="row.favicon.url? row.favicon.url : '/defult.jpg'" style="width: 27px;height: 27px" align="center">
          <span class="el-tag el-tag--success el-tag--medium el-tag--light">{{ row.tag.join(',') }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.title')" width="220px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.title ? row.title : 'Not Found' }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.headers')" width="600px">
        <template slot-scope="{ row }">
          <div class="scrollable">
            <pre>{{ row.headers }}</pre>
          </div>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.finger')" width="180px">
        <template slot-scope="{row}">
          <span v-html="row.finger ? row.finger.map(({ name }) => name).join('<br>') : 'Null' " />
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.screenshot')" width="260px" align="center">
        <template slot-scope="{row}">
          <el-popover placement="top-start" trigger="click"> <!--trigger属性值：hover、click、focus 和 manual-->
            <img :src="`/api/${row.screenshot}`" style="width: 600px;height: 600px" align="center">
            <img slot="reference" :src="`/api/${row.screenshot}`" style="width: 180px;height: 160px; cursor:pointer">
          </el-popover>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.size" @pagination="getList" />

  </div>
</template>

<script>
import { webList, fetchPv, createArticle, updateArticle, startArticle, stopArticle, deleteArticle } from '@/api/article'
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
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      importanceOptions: [1, 2, 3],
      sortOptions: [{ label: '升序', key: '+id' }, { label: '降序', key: '-id' }],
      showReviewer: false,
      listQuery: {
        page: 1,
        size: 10,
        task_id: this.$route.query.task_id,
        targetName: this.$route.query.targetName,
        site_cnt: this.$route.query.site_cnt,
        domain_cnt: this.$route.query.domain_cnt,
        ip_cnt: this.$route.query.ip_cnt,
        cert_cnt: this.$route.query.cert_cnt,
        service_cnt: this.$route.query.service_cnt,
        fileleak_cnt: this.$route.query.fileleak_cnt,
        url_cnt: this.$route.query.url_cnt,
        vuln_cnt: this.$route.query.vuln_cnt,
        npoc_service_cnt: this.$route.query.npoc_service_cnt,
        cip_cnt: this.$route.query.cip_cnt,
        nuclei_result_cnt: this.$route.query.nuclei_result_cnt,
        stat_finger_cnt: this.$route.query.stat_finger_cnt,
        tabIndex: this.$route.query.tabIndex,
        'finger.name': this.$route.query.fingername
      },
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
  },
  methods: {
    getList() {
      this.listLoading = true
      webList(this.listQuery).then(response => {
        this.list = response.items
        this.total = response.total

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    handleFilter() {
      this.listQuery.page = 1
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
  height: 160px;
  overflow: hidden;
}

.scrollable:hover {
  overflow-y: auto;
}

</style>
