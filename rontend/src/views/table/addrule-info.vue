<template>
  <div class="app-container">
    <h3>策略信息</h3>
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
      <el-form-item label="描述">
        <el-input v-model="temp.desc" />
      </el-form-item>
    </el-form>

    <template>
      <table>
        <h3>资产扫描配置</h3>
        <span>域名爆破类型: </span>
        <el-select v-model="temp.domain_brute_type" class="filter-item">
          <el-option v-for="item in statusOptions" :key="item" :label="item" :value="item" />
        </el-select>
        <span>            端口扫描类型: </span>
        <el-select v-model="temp.port_scan_type" class="filter-item">
          <el-option v-for="item in levelptOptions" :key="item" :label="item" :value="item" />
        </el-select>
        <br><br>
        <span>            主机超时时类型: </span>
        <el-select v-model="temp.host_timeout_type" class="filter-item">
          <el-option v-for="item in hosttimeoutOptions" :key="item.key" :label="item.label" :value="item.key" />
        </el-select>
        <br><br>
        <div v-if="temp.host_timeout_type === 'custom'">
          <span>            主机超时时间: </span>
          <el-input-number v-model="temp.host_timeout" :min="0" :max="1000" style="width: 500px" />
        </div>
        <br>
        <span>            探测报文并行: </span>
        <el-input-number v-model="temp.port_parallelism" :min="1" :max="1000" style="width: 500px" />
        <br><br>
        <span>            最少发包速率: </span>
        <el-input-number v-model="temp.port_min_rate" :min="1" :max="1000" style="width: 500px" />
        <br><br>
        <el-row :gutter="32">
          <el-col :span="24">
            <el-button size="mini" @click="selectAll">全选</el-button>
            <el-button size="mini" @click="deselectAll">取消</el-button>
            <br>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="domain_brute" :true-label="true" :false-label="false">域名爆破</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="domain_oneforall" :true-label="true" :false-label="false">oneforall调用</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="alt_dns" :true-label="true" :false-label="false">DNS字典智能生成</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="arl_search" :true-label="true" :false-label="false">ARL 历史查询</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="dns_query_plugin" :true-label="true" :false-label="false">域名查询插件</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="port_scan" :true-label="true" :false-label="false">端口扫描</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="service_detection" :true-label="true" :false-label="false">服务识别</el-checkbox>
          </el-col>

          <el-col :span="8">
            <el-checkbox v-model="os_detection" :true-label="true" :false-label="false">操作系统识别</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="ssl_cert" :true-label="true" :false-label="false">SSL 证书获取</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="skip_scan_cdn_ip" :true-label="true" :false-label="false">跳过CDN</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="npoc_service_detection" :true-label="true" :false-label="false">服务(python)识别
            </el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="site_identify" :true-label="true" :false-label="false">站点识别</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="search_engines" :true-label="true" :false-label="false">搜索引擎调用</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="site_spider" :true-label="true" :false-label="false">站点爬虫</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="site_capture" :true-label="true" :false-label="false">站点截图</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="file_leak" :true-label="true" :false-label="false">文件泄露</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="findvhost" :true-label="true" :false-label="false">Host 碰撞</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="web_info_hunter" :true-label="true" :false-label="false">wih调用</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="unauth_scan" :true-label="true" :false-label="false">unauth调用</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="nuclei_scan" :true-label="true" :false-label="false">nuclei 调用</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="xray_scan" :true-label="true" :false-label="false">xray 调用</el-checkbox>
          </el-col>
        </el-row>
        <br><br>
      </table>
    </template>

    <template>
      <h3>弱口令爆破</h3>
      <div class="checkbox-group">
        <el-checkbox v-model="checkAll" :indeterminate="isIndeterminate" @change="handleCheckAllChange">全选
        </el-checkbox>
        <el-checkbox-group
          v-model="checkedPlugins"
          class="checkbox-items-container"
          @change="handleCheckedCitiesChange"
        >
          <div v-for="plugin in plugins" :key="plugin.plugin_name" class="checkbox-item">
            <el-checkbox :label="plugin.plugin_name">{{ plugin.vul_name }}</el-checkbox>
          </div>
        </el-checkbox-group>
      </div>
    </template>

    <template>
      <h3>POC配置</h3>
      <div class="checkbox-group">
        <el-checkbox v-model="poccheckAll" :indeterminate="pocisIndeterminate" @change="pochandleCheckAllChange">全选
        </el-checkbox>
        <el-checkbox-group
          v-model="poccheckedPlugins"
          class="checkbox-items-container"
          @change="pochandleCheckedCitiesChange"
        >
          <div v-for="plugin in pocplugins" :key="plugin.plugin_name" class="checkbox-item">
            <el-checkbox :label="plugin.plugin_name">{{ plugin.vul_name }}</el-checkbox>
          </div>
        </el-checkbox-group>
      </div>
    </template>

    <template>
      <h3>资产组配置</h3>
      <el-select v-model="selectedId">
        <el-option
          v-for="item in taskOptions"
          :key="item._id"
          :label="item.name + ' ('+ item.scope +')'"
          :value="item._id"
        />
      </el-select>
    </template>
    <br>
    <br><br>

    <div slot="footer" class="dialog-footer">
      <el-button @click="dialogFormVisible = false">
        {{ $t('table.cancel') }}
      </el-button>
      <el-button type="primary" @click="createData">
        {{ $t('table.confirm') }}
      </el-button>
    </div>
  </div>
</template>
<style>
.checkbox-items-container {
  display: flex;
  flex-wrap: wrap;
}

.checkbox-item {
  flex-basis: 33.33%;
  box-sizing: border-box;
}
</style>
<script>
import {
  fetchPv,
  startArticle,
  stopArticle,
  deleteArticle,
  batchdeleteArticle,
  reStart,
  Stop, pocList, groupList, policycreate
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
  // eslint-disable-next-line vue/no-unused-components
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        done: 'success',
        draft: 'info',
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
      checkAll: false,
      poccheckAll: false,
      checkedPlugins: [],
      poccheckedPlugins: [],
      plugins: [], // 你会在此处加载你的实际插件数据
      pocplugins: [],
      isIndeterminate: true,
      pocisIndeterminate: true,
      burteData: [],
      selectedId: '',
      taskOptions: [],
      pocData: [],
      pocData1: [],
      checkboxModels: {},
      domain_brute: false,
      domain_oneforall: false,
      alt_dns: false,
      dns_query_plugin: false,
      arl_search: false,
      port_scan: false,
      service_detection: false,
      os_detection: false,
      ssl_cert: false,
      skip_scan_cdn_ip: false,
      npoc_service_detection: false,
      site_identify: false,
      search_engines: false,
      site_spider: false,
      site_capture: false,
      file_leak: false,
      findvhost: false,
      unauth_scan: false,
      web_info_hunter: false,
      nuclei_scan: false,
      xray_scan: false,
      tableKey: 0,
      list: null,
      sels: '', // 当前选框选中的值
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        size: 10
      },
      listQuery1: {},
      listQuery2: {
        size: 10000,
        plugin_type: 'brute'
      },
      sortOptions: [{ label: '升序', key: 'target' }, { label: '降序', key: '-target' }],
      statusOptions: ['test', 'big'],
      srcptOptions: ['test', 'top100', 'top1000', 'all'],
      levelptOptions: ['test', 'top100', 'top1000', 'all'],
      hosttimeoutOptions: [{ label: '默认(900s)', key: 'default' }, { label: '自定义', key: 'custom' }],
      showReviewer: false,
      temp: {
        host_timeout_type: 'default',
        port_custom: '',
        port_parallelism: 32,
        port_min_rate: 60,
        host_timeout: 0,
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
      rules: {
        type: [{ required: true, message: '类型不能为空', trigger: 'change' }],
        domain: [{ required: true, message: '域名不能为空', trigger: 'change' }],
        name: [{ required: true, message: '厂商不能为空', trigger: 'blur' }]
      },
      downloadLoading: false
    }
  },
  created() {
    this.pocgetList()
    this.pocgetList1()
    this.groupgetList()
  },
  methods: {
    handleCheckAllChange(val) {
      this.plugins.forEach(plugin => {
        plugin.enable = val
        if (val && !this.checkedPlugins.includes(plugin.plugin_name)) {
          this.checkedPlugins.push(plugin.plugin_name)
        }
      })
      if (!val) {
        this.checkedPlugins = []
      }
      this.isIndeterminate = false
    },
    handleCheckedCitiesChange(value) {
      const checkedCount = value.length
      this.checkAll = checkedCount === this.plugins.length
      this.isIndeterminate = checkedCount > 0 && checkedCount < this.plugins.length

      // 更新plugins中每个插件的enable状态
      this.plugins.forEach(plugin => {
        plugin.enable = this.checkedPlugins.includes(plugin.plugin_name)
      })
    },
    pochandleCheckAllChange(val) {
      this.pocplugins.forEach(plugin => {
        plugin.enable = val
        if (val && !this.poccheckedPlugins.includes(plugin.plugin_name)) {
          this.poccheckedPlugins.push(plugin.plugin_name)
        }
      })
      if (!val) {
        this.poccheckedPlugins = []
      }
      this.pocisIndeterminate = false
    },
    pochandleCheckedCitiesChange(value) {
      const checkedCount = value.length
      this.checkAll = checkedCount === this.pocplugins.length
      this.pocisIndeterminate = checkedCount > 0 && checkedCount < this.pocplugins.length

      // 更新plugins中每个插件的enable状态
      this.pocplugins.forEach(plugin => {
        plugin.enable = this.poccheckedPlugins.includes(plugin.plugin_name)
      })
    },
    selectAll() {
      // eslint-disable-next-line no-sequences
      this.domain_brute = true,
      this.domain_oneforall = true,
      this.alt_dns = true,
      this.dns_query_plugin = true,
      this.arl_search = true,
      this.port_scan = true,
      this.service_detection = true,
      this.os_detection = true,
      this.ssl_cert = true,
      this.skip_scan_cdn_ip = true,
      this.npoc_service_detection = true,
      this.site_identify = true,
      this.search_engines = true,
      this.site_spider = true,
      this.site_capture = true,
      this.file_leak = true,
      this.findvhost = true,
      this.unauth_scan = true,
      this.web_info_hunter = true,
      this.nuclei_scan = true,
      this.xray_scan = true
    },
    deselectAll() {
      // eslint-disable-next-line no-sequences
      this.domain_brute = false,
      this.domain_oneforall = false,
      this.alt_dns = false,
      this.dns_query_plugin = false,
      this.arl_search = false,
      this.port_scan = false,
      this.service_detection = false,
      this.os_detection = false,
      this.ssl_cert = false,
      this.skip_scan_cdn_ip = false,
      this.npoc_service_detection = false,
      this.site_identify = false,
      this.search_engines = false,
      this.site_spider = false,
      this.site_capture = false,
      this.file_leak = false,
      this.findvhost = false,
      this.unauth_scan = false,
      this.web_info_hunter = false,
      this.nuclei_scan = false
      this.xray_scan = false
    },
    groupgetList() {
      this.listLoading = true
      this.listQuery.size = 100
      groupList(this.listQuery).then(response => {
        this.list = response.items
        this.total = response.total
        this.taskOptions = response.items

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1 * 1000)
      })
    },
    pocgetList() {
      this.listLoading = true
      pocList(this.listQuery2).then(response => {
        this.pocData = response.items
        this.total = response.total
        response.items.forEach(plugin => {
          this.plugins.push({
            plugin_name: plugin.plugin_name,
            vul_name: plugin.vul_name,
            enable: false
          })
        }).catch(error => {
          console.log(error)
        })

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1 * 1000)
      })
    },
    pocgetList1() {
      this.listLoading = true
      this.listQuery1.size = 10000
      this.listQuery1.plugin_type = 'poc'
      pocList(this.listQuery1).then(response => {
        this.pocData1 = response.items
        this.total = response.total
        response.items.forEach(plugin => {
          this.pocplugins.push({
            plugin_name: plugin.plugin_name,
            vul_name: plugin.vul_name,
            enable: false
          })
        }).catch(error => {
          console.log(error)
        })

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
      if (!this.temp.name) {
        this.$message({
          message: '名称不能为空',
          type: 'warning'
        })
        return
      }
      const enabledPlugins = this.plugins.filter(plugin => plugin.enable === true)
      const pocenabledPlugins = this.pocplugins.filter(plugin => plugin.enable === true)
      const result = {
        name: this.temp.name,
        desc: this.temp.desc,
        policy: {
          brute_config: enabledPlugins,
          ip_config: {
            host_timeout: this.temp.host_timeout,
            host_timeout_type: this.temp.host_timeout_type,
            os_detection: this.os_detection,
            port_custom: this.temp.port_custom,
            port_min_rate: this.temp.port_min_rate,
            port_parallelism: this.temp.port_parallelism,
            port_scan: this.port_scan,
            port_scan_type: this.temp.port_scan_type,
            service_detection: this.service_detection,
            ssl_cert: this.ssl_cert
          },
          npoc_service_detection: this.npoc_service_detection,
          poc_config: pocenabledPlugins,
          file_leak: this.file_leak,
          site_config: {
            nuclei_scan: this.nuclei_scan,
            unauth_scan: this.unauth_scan,
            web_info_hunter: this.web_info_hunter,
            xray_scan: this.xray_scan,
            search_engines: this.search_engines,
            site_capture: this.site_capture,
            site_identify: this.site_identify,
            site_spider: this.site_spider
          },
          scope_config: {
            scope_id: this.selectedId ? this.selectedId : ''
          }
        }
      }
      policycreate(result).then(response => {
        if (response.code === 200) {
          this.dialogFormVisible = false
          this.$notify({
            title: '成功',
            message: '创建成功',
            type: 'success',
            duration: 2000
          })
          this.$router.push('/rule/rule-info')
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
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    handleSelectionChange(sels) {
      this.sels = sels
    },
    // 批量删除执行操作
    batchDelect() {
      // 删除前的提示
      this.$confirm('确认删除记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        const data = {
          del_task_data: true,
          task_id: this.sels.map((item) => item._id)
        }
        batchdeleteArticle(data)
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
    handleDelete(row) {
      this.$confirm('确认删除记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        const data = {
          del_task_data: true,
          task_id: [row._id]
        }
        deleteArticle(data)
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
