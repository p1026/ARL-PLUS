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
        v-model="listQuery.target"
        :placeholder="$t('table.target')"
        style="width: 200px"
        class="filter-item"
        @keyup.enter.native="handleFilter"
      />
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        {{ $t('table.search') }}
      </el-button>
      <br> <br>
      <el-select
        v-model="listQuery.order"
        style="width: 120px"
        class="filter-item"
        placeholder="排序"
        @change="handleFilter"
      >
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-button
        class="filter-item"
        style="margin-left: 10px;"
        type="primary"
        icon="el-icon-edit"
        @click="handleCreate"
      >
        {{ $t('table.add') }}
      </el-button>
      <el-button type="danger" class="filter-item" @click="batchDelect">批量删除</el-button>
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
      <el-table-column :label="$t('table.name')" min-width="230px" align="center">
        <template slot-scope="{row}">
          <span class="link-type" @click="navigateToAllInfo(row)">
            {{ row.name }}
          </span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.domain')" min-width="150px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.target }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.src')" min-width="80px" align="center">
        <template slot-scope="{row}">
          <a class="link-type" :href="row.options.remark" target="_blank"> {{ row.options.src }} </a>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.tj')" min-width="130px" align="center">
        <template slot-scope="{row}">
          <div style="display: flex;flex-direction: column">
            <span>站点： {{ row.statistic ? row.statistic.site_cnt : '0' }}</span>
            <span>子域： {{ row.statistic ? row.statistic.domain_cnt : '0' }}</span>
          </div>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.status')" min-width="150px" align="center">
        <template slot-scope="{row}">
          <el-tooltip placement="top" :open-delay="1">
            <el-tag :type="row.status | statusFilter">
              {{ row.status }}
            </el-tag>
            <div slot="content">
              <pre v-for="(item, index) in row.service" :key="index">{{ item.name }}：{{ item.elapsed }}</pre>
            </div>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.create_date')" min-width="155px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.start_time }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.end_date')" min-width="155px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.end_time }}</span>
        </template>
      </el-table-column>
      <el-table-column
        fixed="right"
        :label="$t('table.actions')"
        align="center"
        width="380"
        class-name="small-padding fixed-width"
      >
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" @click="syncTask(row)">
            {{ $t('table.sync') }}
          </el-button>
          <el-button size="mini">
            {{ $t('table.exp') }}
          </el-button>
          <el-button
            size="mini"
            type="info"
            :disabled="row.status === 'done' || row.status === 'stop' || row.status === 'error'"
            @click="taskStop(row)"
          >
            {{ $t('table.draft') }}
          </el-button>
          <el-button size="mini" type="danger" @click="handleDelete(row)">
            {{ $t('table.delete') }}
          </el-button>
          <el-button size="mini" type="success" @click="reStarts(row)">
            {{ $t('table.reboot') }}
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
        <el-form-item :label="$t('table.name')" prop="task">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item :label="$t('table.domain')" prop="domain" required>
          <el-input v-model="temp.domain" :autosize="{ minRows: 2, maxRows: 4}" type="textarea" placeholder="请输入域名、IP、IP段" />
        </el-form-item>
        <el-form-item :label="$t('table.domain_brute_type')">
          <el-select v-model="temp.domain_brute_type" class="filter-item">
            <el-option v-for="item in statusOptions" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item :label="$t('table.port_type')">
          <el-select v-model="temp.port_scan_type" class="filter-item">
            <el-option v-for="item in levelptOptions" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item :label="$t('table.src')">
          <el-input v-model="temp.src" />
        </el-form-item>
        <el-form-item label="地址">
          <el-input
            v-model="temp.remark"
            :autosize="{ minRows: 2, maxRows: 4}"
            type="textarea"
            placeholder="Please input"
          />
        </el-form-item>
        <el-row :gutter="32">
          <el-col :span="24">
            <el-button size="mini" @click="selectAll">全选</el-button>
            <el-button size="mini" @click="deselectAll">全部取消</el-button>
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
            <el-checkbox v-model="dns_query_plugin" :true-label="true" :false-label="false">域名查询插件</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="arl_search" :true-label="true" :false-label="false">ARL 历史查询</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="port_scan" :true-label="true" :false-label="false">端口扫描</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="service_detection" :true-label="true" :false-label="false">服务识别</el-checkbox>
          </el-col>
          <br><br> <br>
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
            <el-checkbox v-model="site_identify" :true-label="true" :false-label="false">站点识别</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="search_engines" :true-label="true" :false-label="false">搜索引擎调用</el-checkbox>
          </el-col>
          <el-col :span="8">
            <el-checkbox v-model="site_spider" :true-label="true" :false-label="false">站点爬虫</el-checkbox>
          </el-col>
          <br><br> <br>
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
            <el-checkbox v-model="web_info_hunter" :true-label="true" :false-label="false">WIH调用</el-checkbox>
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

    <el-dialog :title="synctask[dialogStatus]" :visible.sync="dialogVisible">
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temps"
        label-position="left"
        label-width="70px"
        style="width: 400px; margin-left:50px;"
      >
        <el-form-item label="资产" required>
          <el-select v-model="temp._id" class="filter-item" style="width: 500px">
            <el-option v-for="item in synclist" :key="item._id" :label="item.name + '('+ item.scope + ')'" :value="item._id" style="width: 500px" />
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addsyncTask">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<style>
.scrollable-content {
  width: 200px; /* 宽度根据需要调整 */
  height: 300px; /* 高度根据需要调整 */
  overflow-y: scroll;
  border: 1px solid #ccc;
  padding: 5px;
  white-space: pre-wrap; /* 保留换行和空格 */
}
</style>

<script>
import {
  fetchList,
  createArticle,
  updateArticle,
  deleteArticle,
  batchdeleteArticle,
  reStart,
  Stop, syncList, addsync
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
      dialogVisible: false,
      domain_brute: false,
      domain_oneforall: false,
      alt_dns: false,
      dns_query_plugin: false,
      arl_search: false,
      port_scan: false,
      service_detection: false,
      service_brute: false,
      os_detection: false,
      ssl_cert: false,
      skip_scan_cdn_ip: false,
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
      synclist: [],
      sels: '', // 当前选框选中的值
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        size: 10
      },
      sortOptions: [{ label: '升序', key: 'target' }, { label: '降序', key: '-target' }],
      statusOptions: ['test', 'big'],
      srcptOptions: ['test', 'top100', 'top1000', 'all'],
      levelptOptions: ['test', 'top100', 'top1000', 'all'],
      showReviewer: false,
      temp: {
        name: '',
        domain: '',
        _id: '',
        task_id: '',
        domain_brute_type: 'big',
        port_scan_type: 'top1000'
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      synctask: {
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
    selectAll() {
      // eslint-disable-next-line no-sequences
      this.domain_brute = true,
      this.domain_oneforall = true,
      this.alt_dns = true,
      this.dns_query_plugin = true,
      this.arl_search = true,
      this.port_scan = true,
      this.service_detection = true,
      this.service_brute = true,
      this.os_detection = true,
      this.ssl_cert = true,
      this.skip_scan_cdn_ip = true,
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
      this.service_brute = false,
      this.os_detection = false,
      this.ssl_cert = false,
      this.skip_scan_cdn_ip = false,
      this.site_identify = false,
      this.search_engines = false,
      this.site_spider = false,
      this.site_capture = false,
      this.file_leak = false,
      this.findvhost = false,
      this.unauth_scan = false,
      this.web_info_hunter = false,
      this.nuclei_scan = false,
      this.xray_scan = false
    },
    navigateToAllInfo(row) {
      this.$router.push({
        path: 'all-info',
        query: {
          task_id: row._id,
          targetName: row.target,
          site_cnt: row.statistic ? row.statistic.site_cnt : '0',
          domain_cnt: row.statistic ? row.statistic.domain_cnt : '0',
          ip_cnt: row.statistic ? row.statistic.ip_cnt : '0',
          cert_cnt: row.statistic ? row.statistic.cert_cnt : '0',
          service_cnt: row.statistic ? row.statistic.service_cnt : '0',
          fileleak_cnt: row.statistic ? row.statistic.fileleak_cnt : '0',
          url_cnt: row.statistic ? row.statistic.url_cnt : '0',
          vuln_cnt: row.statistic ? row.statistic.vuln_cnt : '0',
          npoc_service_cnt: row.statistic ? row.statistic.npoc_service_cnt : '0',
          cip_cnt: row.statistic ? row.statistic.cip_cnt : '0',
          nuclei_result_cnt: row.statistic ? row.statistic.nuclei_result_cnt : '0',
          stat_finger_cnt: row.statistic ? row.statistic.stat_finger_cnt : '0',
          unauth_cnt: row.statistic ? row.statistic.unauth_cnt : '0',
          xray_result_cnt: row.statistic ? row.statistic.xray_result_cnt : '0',
          wih_cnt: row.statistic ? row.statistic.wih_cnt : '0'
        }
      })
    },
    getList() {
      this.listLoading = true
      fetchList(this.listQuery).then(response => {
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
      this.temp.name = ''
      this.temp.domain = ''
      this.deselectAll()
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
            target: this.temp.domain,
            domain_brute_type: this.temp.domain_brute_type,
            port_scan_type: this.temp.port_scan_type,
            domain_brute: !!this.domain_brute,
            domain_oneforall: !!this.domain_oneforall,
            alt_dns: !!this.alt_dns,
            dns_query_plugin: !!this.dns_query_plugin,
            arl_search: !!this.arl_search,
            port_scan: !!this.port_scan,
            service_detection: !!this.service_detection,
            service_brute: !!this.service_brute,
            os_detection: !!this.os_detection,
            ssl_cert: !!this.ssl_cert,
            skip_scan_cdn_ip: !!this.skip_scan_cdn_ip,
            site_identify: !!this.site_identify,
            search_engines: !!this.search_engines,
            site_spider: !!this.site_spider,
            site_capture: !!this.site_capture,
            file_leak: !!this.file_leak,
            findvhost: !!this.findvhost,
            web_info_hunter: !!this.web_info_hunter,
            unauth_scan: !!this.unauth_scan,
            nuclei_scan: !!this.nuclei_scan,
            xray_scan: !!this.xray_scan,
            src: this.temp.src,
            remark: this.temp.remark
          }
          createArticle(result).then(response => {
            if (response.code === 200) {
              this.list.unshift(this.temp)
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
            // 处理和显示异常
            this.$notify({
              title: '错误',
              message: error.message || '创建时发生错误', // 使用错误消息或默认的错误文本
              type: 'error',
              duration: 2000
            })
          })
        }
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
    syncTask(row) {
      this.dialogVisible = true
      this.temp.task_id = row._id
      const newList = {
        target: row.target
      }
      syncList(newList).then(response => {
        this.synclist = response.items
        this.total = response.total

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1 * 1000)
      })
    },
    addsyncTask() {
      const result = {
        scope_id: this.temp._id,
        task_id: this.temp.task_id
      }
      addsync(result).then(response => {
        this.$notify({
          title: '成功',
          message: '更新成功',
          type: 'success',
          duration: 2000
        })
        this.dialogVisible = false
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
    batchDelect() {
      this.$confirm('确认删除记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        const data = {
          del_task_data: true,
          task_id: this.sels.map((item) => item._id)
        }
        batchdeleteArticle(data).then(response => {
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
    handleDelete(row) {
      this.$confirm('确认删除记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        const data = {
          del_task_data: true,
          task_id: [row._id]
        }
        deleteArticle(data).then(response => {
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
      reStart(data).then(response => {
        if (response.code === 200) {
          this.$notify({
            title: '成功',
            message: '重启成功',
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
    taskStop(row) {
      Stop(row._id).then(response => {
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
