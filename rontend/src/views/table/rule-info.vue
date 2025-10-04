<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.name"
        :placeholder="$t('table.name')"
        style="width: 200px"
        class="filter-item"
        @keyup.enter.native="handleFilter"
      />
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <el-input
        v-model="listQuery._id"
        placeholder="策略id"
        style="width: 200px"
        class="filter-item"
        @keyup.enter.native="handleFilter"
      />
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        {{ $t('table.search') }}
      </el-button>
      <br> <br>
      <el-button type="success" class="filter-item" @click="toaddrule">新建策略</el-button>
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
      <el-table-column type="expand" label="配置" width="60">
        <template slot-scope="props">
          <h3>域名和ip配置</h3>
          <span style="font-weight: bold;">
            域名爆破类型：
          </span>
          <span>
            {{ props.row.policy.domain_config.domain_brute_type === 'big' ? '大字典' : '测试' }}
          </span>
          <br><br>
          <span style="font-weight: bold;">
            端口扫描类型：
          </span>
          <span>
            {{ props.row.policy.ip_config.port_scan_type }}
          </span>
          <br><br>
          <span style="font-weight: bold;">
            配置信息：
          </span>
          <span>
            {{ props.row.policy.domain_config.domain_brute === true ? '域名爆破、' : '' }}
            {{ props.row.policy.domain_config.domain_oneforall === true ? 'oneforall调用、' : '' }}
            {{ props.row.policy.domain_config.alt_dns === true ? 'DNS字典智能生成、' : '' }}
            {{ props.row.policy.domain_config.arl_search === true ? 'ARL 历史查询、' : '' }}
            {{ props.row.policy.domain_config.search_engines === true ? '搜索引擎调用、' : '' }}
            {{ props.row.policy.domain_config.dns_query_plugin === true ? '域名查询插件、' : '' }}}
            {{ props.row.policy.ip_config.skip_scan_cdn_ip === true ? '跳过CDN、' : '' }}
            {{ props.row.policy.ip_config.port_scan === true ? '端口扫描、' : '' }}
            {{ props.row.policy.ip_config.service_detection === true ? '服务扫描、' : '' }}
            {{ props.row.policy.ip_config.os_detection === true ? '操作系统识别、' : '' }}
            {{ props.row.policy.ip_config.ssl_cert === true ? 'SSL 证书获取、' : '' }}
            {{ props.row.policy.npoc_service_detection === true ? '(py)服务识别' : '' }}
          </span>
          <br><br>
          <h3>
            站点和风险配置
          </h3>
          <span style="font-weight: bold;">
            配置信息：
          </span>
          <span>
            {{ props.row.policy.site_config.site_identify === true ? '站点识别、' : '' }}
            {{ props.row.policy.site_config.site_capture === true ? '站点截图、' : '' }}
            {{ props.row.policy.site_config.site_spider === true ? '站点爬虫、' : '' }}
            {{ props.row.policy.site_config.nuclei_scan === true ? 'nuclei 调用、' : '' }}
            {{ props.row.policy.site_config.unauth_scan === true ? 'unauth 调用、' : '' }}
            {{ props.row.policy.site_config.findvhost === true ? 'host碰撞 调用、' : '' }}
            {{ props.row.policy.site_config.web_info_hunter === true ? 'wih 调用、' : '' }}
            {{ props.row.policy.file_leak === true ? '文件泄露、' : '' }}
            {{ props.row.policy.site_config.xray_scan === true ? 'xray调用' : '' }}
          </span>
          <br><br>
          <h3>
            POC配置
          </h3>
          <span style="font-weight: bold;">
            配置信息：
          </span>
          <span v-for="items in props.row.policy.poc_config" :key="items">
            {{ items.vul_name + '、' }}
          </span>
          <br><br>
          <h3>
            弱口令爆破配置
          </h3>
          <span style="font-weight: bold;">
            配置信息：
          </span>
          <span v-for="items in props.row.policy.brute_config" :key="items">
            {{ items.vul_name + '、' }}
          </span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.name')" min-width="120px" align="center">
        <template slot-scope="{row}">
          <span>
            {{ row.name }}
          </span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.desc')" width="280px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.desc }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.groupid')" width="280px" align="center">
        <template slot-scope="{row}">
          <span class="link-type" @click="searchgroup(row)">{{ row.policy.scope_config.scope_id }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.update_date')" width="250px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.update_date }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.actions')" align="center" width="250" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button size="mini" type="success" @click="handtask(row)">
            {{ $t('table.run') }}
          </el-button>
          <el-button size="mini" type="danger" @click="batchDelect1(row)">
            {{ $t('table.delete') }}
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

    <el-dialog :title="ruletask[dialogStatus]" :visible.sync="dialogVisible">
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temps"
        label-position="left"
        label-width="70px"
        style="width: 400px; margin-left:50px;"
      >
        <el-form-item :label="$t('table.type')" required>
          <el-select v-model="temp.task_tag" size="small">
            <el-option v-for="item in taskOption" :key="item.key" :label="item.label" :value="item.key" />
          </el-select>
        </el-form-item>

        <el-form-item :label="$t('table.name')" required>
          <el-input
            v-model="taskName"
          />
        </el-form-item>
        <el-form-item :label="$t('table.target')" required>
          <el-input v-model="temp.target" :autosize="{ minRows: 2, maxRows: 4}" type="textarea" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addruleTask">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<style>
.demo-table-expand {
  font-size: 0;
}
.border-box {
  border: 1px solid #ccc; /* light gray border */
  background-color: #f5f5f5; /* light gray background */
  padding: 10px;
  margin-bottom: 5px;
  display: block;
}
.demo-table-expand label {
  width: 90px;
  color: #99a9bf;
}
.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
}

::v-deep {
  .row-expand-unhas .el-table__expand-column {
    pointer-events: none;
  }
  .row-expand-unhas .el-table__expand-column .el-icon {
    visibility: hidden;
  }
}
</style>

<script>
import {
  fetchPv,
  createArticle,
  updateArticle,
  startArticle,
  stopArticle,
  reStart,
  Stop,
  batchdeletemonitor,
  batchstopmonitor,
  batchrecovermonitor,
  batchrecovermonitor1,
  ruleList,
  ruledelete,
  createruletask
} from '@/api/article'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination'
import row from 'element-ui/packages/row'

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
      taskOption: [{ label: '资产侦查任务', key: 'task' }, { label: '风险巡航任务', key: 'risk_cruising' }],
      dialogVisible: false,
      configdata: [],
      tableKey: 0,
      list: null,
      sels: '', // 当前选框选中的值
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        size: 10,
        order: '-update_date',
        _id: ''
      },
      configOptions: [{ label: '升序', key: 'target' }, { label: '降序', key: '-target' }],
      statusOptions: ['test', 'big'],
      srcptOptions: ['test', 'top100', 'top1000', 'all'],
      levelptOptions: ['test', 'top100', 'top1000', 'all'],
      showReviewer: false,
      temp: {
        name: '',
        target: '',
        task_tag: '',
        domain_brute_type: 'big',
        port_scan_type: 'top100'
      },
      dialogFormVisible: false,
      dialogStatus: '',
      ruletask: {
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
  computed: {
    taskName() {
      if (this.temp.task_tag === 'task') {
        return '资产侦查任务-' + this.temp.name
      } else if (this.temp.task_tag === 'risk_cruising') {
        return '风险巡航任务-' + this.temp.name
      } else {
        return this.temp.name
      }
    },
    row() {
      return row
    }
  },
  created() {
    this.listQuery._id = this.$route.query._id
    this.getList()
  },
  methods: {
    searchgroup(row) {
      this.$router.push({
        path: '/group/group-info',
        query: {
          _id: row.policy.scope_config.scope_id,
          scope_id: row.policy.scope_config.scope_id
        }
      })
    },
    getTaskName() {
      return this.temp.task_tag === 'task'
        ? '资产侦查任务-' + this.temp.name
        : this.temp.task_tag === 'risk_cruising'
          ? '风险巡航任务-' + this.temp.name
          : this.temp.name
    },
    addruleTask() {
      this.dialogVisible = false
      const result = {
        policy_id: this.temp.policy_id,
        name: this.getTaskName(),
        target: this.temp.target,
        task_tag: this.temp.task_tag
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
    handtask(row) {
      // eslint-disable-next-line no-sequences
      this.temp.task_tag = ''
      this.temp.target = ''
      this.temp.name = row.name
      this.temp.policy_id = row._id
      this.dialogStatus = 'create'
      this.dialogVisible = true
    },
    toaddrule() {
      this.$router.push('/rule/addrule-info')
    },
    headerCellStyle({ row, column, rowIndex, columnIndex }) {
      return { textAlign: 'center', background: '#E6E6E6' }
    },
    // 设置表内容样式
    cellStyle({ row, column, rowIndex, columnIndex }) {
      return { textAlign: 'center' }
    },
    // 设置row样式
    rowClassName({ row, rowIndex }) {
      console.log(JSON.stringify(row))
      const data = row
      const res = []
      if (data.datas && data.datas.length > 0) {
        res.push('row-expand-has')
        return res
      } else {
        res.push('row-expand-unhas')
        return res
      }
    },
    getList() {
      this.listLoading = true
      ruleList(this.listQuery).then(response => {
        this.list = response.items
        this.total = response.total
        this.configdata = response.items
        console.log(this.configdata)

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
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const result = {
            name: this.temp.name,
            target: this.temp.domain
          }
          createArticle(result).then(() => {
            this.list.unshift(this.temp)
            this.dialogFormVisible = false
            this.$notify({
              title: '成功',
              message: '创建成功',
              type: 'success',
              duration: 2000
            })
            setTimeout(() => {
              location.reload()
            }, 1000)
          })
        }
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
    // 批量删除执行操作
    batchDelect() {
      // 删除前的提示
      this.$confirm('确认删除记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        const data = {
          job_id: this.sels.map((item) => item._id)
        }
        batchdeletemonitor(data)
        this.$notify({
          title: '成功',
          message: '删除成功',
          type: 'success',
          duration: 2000
        })
        setTimeout(() => {
          location.reload()
        }, 1000)
      })
    },
    batchRecover() {
      // 删除前的提示
      const data = {
        job_id: this.sels.map((item) => item._id)
      }
      batchrecovermonitor(data)
      this.$notify({
        title: '成功',
        message: '恢复成功',
        type: 'success',
        duration: 2000
      })
      setTimeout(() => {
        location.reload()
      }, 1000)
    },
    batchRecover1(row) {
      const data = {
        job_id: row._id
      }
      batchrecovermonitor1(data)
      this.$notify({
        title: '成功',
        message: '恢复成功',
        type: 'success',
        duration: 2000
      })
      setTimeout(() => {
        location.reload()
      }, 1000)
    },
    batchStop() {
      // 删除前的提示
      const data = {
        job_id: this.sels.map((item) => item._id)
      }
      batchstopmonitor(data)
      this.$notify({
        title: '成功',
        message: '停止成功',
        type: 'success',
        duration: 2000
      })
      setTimeout(() => {
        location.reload()
      }, 1000)
    },
    batchStop1(row) {
      const data = {
        job_id: [row._id]
      }
      batchstopmonitor(data)
      this.$notify({
        title: '成功',
        message: '停止成功',
        type: 'success',
        duration: 2000
      })
      setTimeout(() => {
        location.reload()
      }, 1000)
    },
    batchDelect1(row) {
      // 删除前的提示
      this.$confirm('确认删除记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        const data = {
          policy_id: [row._id]
        }
        ruledelete(data).then(response => {
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
    reStarts(row) {
      const data = {
        task_id: [row._id]
      }
      reStart(data)
      this.$notify({
        title: '成功',
        message: '运行成功',
        type: 'success',
        duration: 2000
      })
      setTimeout(() => {
        location.reload()
      }, 1000)
    },

    taskStop(row) {
      Stop(row._id)
      this.$notify({
        title: '成功',
        message: '运行成功',
        type: 'success',
        duration: 2000
      })
      setTimeout(() => {
        location.reload()
      }, 1000)
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
