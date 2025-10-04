<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="localListQuery.ip"
        :placeholder="$t('table.ip')"
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
      <el-table-column :label="$t('table.ip')" min-width="210px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.ip }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.os')" width="140px" align="center">
        <template slot-scope="{row}">
          <span>{{ JSON.stringify(row.os_info).replace('{}', '-') }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.port')" width="200px" align="center">
        <template slot-scope="{row}">
          <div class="scrollable">
            <span v-html="row.port_info ? row.port_info.map(item => item.port_id).join(',') : '-' " />
          </div>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.lndomain')" width="260px" align="center">
        <template slot-scope="{row}">
          <div class="scrollable">
            <span v-html=" row.domain.join('<br>') " />
          </div>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.cdn')" width="200px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.cdn_name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.Geo')" width="230px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.geo_city.country_name }}</span>-
          <span>{{ row.geo_city.region_name }}</span>-
          <span>{{ row.geo_city.city }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.asn')" width="269px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.geo_asn.organization }}</span>
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
  hostList,
  fetchPv,
  createArticle,
  updateArticle,
  startArticle,
  stopArticle,
  deleteArticle
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
    listQuery: Object // 定义要传递的参数
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
    this.$set(this.localListQuery, 'ip', '')
  },
  methods: {
    getList() {
      this.listLoading = true
      hostList(this.listQuery).then(response => {
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
    searchgetList() {
      this.listLoading = true
      hostList(this.localListQuery).then(response => {
        this.list = response.items
        this.total = response.total

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
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
    indexMethod(index) {
      return index + 1
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
