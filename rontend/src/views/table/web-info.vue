<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="localListQuery.site"
        :placeholder="$t('table.website')"
        style="width: 200px;"
        class="filter-item"
        @keyup.enter.native="handleFilter"
      />
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <el-input
        v-model="localListQuery.title"
        :placeholder="$t('table.title')"
        style="width: 200px;"
        class="filter-item"
        @keyup.enter.native="handleFilter"
      />
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <el-input
        v-model="localListQuery.status"
        :placeholder="$t('table.status')"
        style="width: 200px;"
        class="filter-item"
        @keyup.enter.native="handleFilter"
      />
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        {{ $t('table.search') }}
      </el-button>
      <br><br>
      <el-button type="primary" icon="el-icon-download" @click="downloadFile">
        导出
      </el-button>
      <el-button type="success" @click="handtask">
        任务下发
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

    <el-dialog title="任务下发" :visible.sync="dialogVisible">
      <el-form
        :rules="rules"
        :model="temps"
        label-position="left"
        label-width="70px"
        style="width: 400px; margin-left:50px;"
      >
        <el-form-item v-if="dialogStatus !== 'site'" :label="$t('table.rule')" required>
          <el-select v-model="temp.policy_id" class="filter-item" style="width: 500px">
            <el-option v-for="item in policyid" :key="item._id" :label="item.name" :value="item._id" style="width: 500px" />
          </el-select>
        </el-form-item>
        <el-form-item :label="$t('table.name')" required>
          <el-input v-model="temp.name" :min="1" :max="1000" style="width: 500px" />
        </el-form-item>
        <span>目标： 选择目标数 {{ this.result.result_total }}</span>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handsTask">确 定</el-button>
      </span>
    </el-dialog>

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
  webList,
  fetchPv,
  createArticle,
  updateArticle,
  startArticle,
  stopArticle,
  deleteArticle,
  policyGroup, resultSet, createruletask
} from '@/api/article'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination'
import axios from 'axios'
import Cookies from 'js-cookie' // secondary package based on el-pagination

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
    listQuery: {
      type: Object,
      // 提供一个默认值，以防父组件没有传值
      default: () => ({})
    },
    row: Object
  },
  data() {
    return {
      policyid: [],
      result: {},
      dialogVisible: false,
      token: Cookies.get('Admin-Token'),
      localListQuery: {},
      other: {
        site: '',
        title: '',
        status: ''
      },
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      importanceOptions: [1, 2, 3],
      sortOptions: [{ label: '升序', key: '+id' }, { label: '降序', key: '-id' }],
      showReviewer: false,
      temp: {
        policy_id: '',
        name: '风险巡查任务-',
        result_set_id: '',
        target: '',
        task_tag: ''
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

    // 如果父组件传递的对象没有 site 属性，添加一个（可以根据实际情况替换 ''）
    if (!('site' in this.localListQuery)) {
      this.$set(this.localListQuery, 'site', '')
    }
    if (!('title' in this.localListQuery)) {
      this.$set(this.localListQuery, 'title', '')
    }
    if (!('status' in this.localListQuery)) {
      this.$set(this.localListQuery, 'status', '')
    }
  },
  methods: {
    handtask() {
      this.dialogVisible = true
      policyGroup(1000).then(response => {
        this.policyid = response.items
        console.log(this.policyid.name)
      })
      resultSet(this.listQuery).then(response => {
        this.result = response.data
      })
    },
    handsTask() {
      this.dialogVisible = false
      const result = {
        name: this.temp.name,
        policy_id: this.temp.policy_id,
        result_set_id: this.result.result_set_id,
        target: '',
        task_tag: 'risk_cruising'
      }
      createruletask(result).then(response => {
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
    },
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
    searchgetList() {
      this.listLoading = true
      webList(this.localListQuery).then(response => {
        this.list = response.items
        this.total = response.total
        const page = Math.floor(this.total / 10) + 1
        if (page < this.localListQuery.page) {
          this.$message({
            message: '超过最大页数' + page + '，接口请求是' + this.localListQuery.page,
            type: 'success'
          })
        }

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    handleFilter() {
      this.searchgetList()
    },
    downloadFile() {
      this.listQuery.size = 10000
      axios({
        url: '/api/site/export/',
        method: 'GET',
        responseType: 'blob',
        params: this.listQuery,
        headers: {
          // eslint-disable-next-line no-undef
          'Token': `${this.token}`
        }
      }).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        // 从响应头中获取文件名，如果无法获取，则自定义一个
        const contentDisposition = response.headers['content-disposition']
        let filename = 'downloadedfile'
        if (contentDisposition) {
          const fileNameMatch = contentDisposition.match(/filename="?(.+)"?\b/)
          if (fileNameMatch.length > 1) {
            filename = fileNameMatch[1]
          }
        }
        link.setAttribute('download', filename)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
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
