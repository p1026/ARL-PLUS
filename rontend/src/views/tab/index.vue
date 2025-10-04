<template>
  <div class="tab-container">
    <el-tabs v-model="activeName" style="margin-top:15px;" type="border-card">
      <el-tab-pane v-for="(item, idx) in tabMapOptions" :key="item.key" :label="item.label" :name="item.key">
        <div v-if="item.key === 'site'">
          <webTask :list-query="listQuery(idx)" />
        </div>
        <div v-if="item.key === 'domain'">
          <DomainTask :list-query="listQuery(1)" />
        </div>
        <div v-if="item.key === 'ip'">
          <HostTask :list-query="listQuery(2)" />
        </div>
        <div v-if="item.key === 'ssl'">
          <SslTask :list-query="listQuery(3)" />
        </div>
        <div v-if="item.key === 'server'">
          <SerTask :list-query="listQuery(4)" />
        </div>
        <div v-if="item.key === 'file'">
          <FileTask :list-query="listQuery(5)" />
        </div>
        <div v-if="item.key === 'url'">
          <UrlTask :list-query="listQuery(6)" />
        </div>
        <div v-if="item.key === 'risk'">
          <RiskTask :list-query="listQuery(7)" />
        </div>
        <div v-if="item.key === 'pyser'">
          <PySerTask :list-query="listQuery(8)" />
        </div>
        <div v-if="item.key === 'c'">
          <CTask :list-query="listQuery(9)" />
        </div>
        <div v-if="item.key === 'vul'">
          <VulTask :list-query="listQuery(10)" />
        </div>
        <div v-if="item.key === 'fing'">
          <FingTask :list-query="listQuery(11)" />
        </div>
        <div v-if="item.key === 'unauth'">
          <UnauthTask :list-query="listQuery(12)" />
        </div>
        <div v-if="item.key === 'xray'">
          <XrayTask :list-query="listQuery(13)" />
        </div>
        <div v-if="item.key === 'wih'">
          <WihTask :list-query="listQuery(14)" />
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import webTask from '../table/web-info'
import DomainTask from '../table/domain-info'
import HostTask from '../table/host-info'
import FileTask from '../table/file-info'
import UrlTask from '../table/url-info'
import VulTask from '../table/nuclei-info'
import RiskTask from '../table/risk-info'
import SslTask from '../table/ssl-info'
import SerTask from '../table/service-info'
import PySerTask from '../table/pyser-info'
import CTask from '../table/c-info'
import FingTask from '../table/finger-info'
import UnauthTask from '../table/unauth-info'
import XrayTask from '../table/xray-info'
import WihTask from '../table/wih-info'

export default {
  name: 'Tab',
  components: {
    webTask,
    DomainTask,
    HostTask,
    FileTask,
    UrlTask,
    VulTask,
    RiskTask,
    SslTask,
    SerTask,
    PySerTask,
    CTask,
    FingTask,
    UnauthTask,
    XrayTask,
    WihTask
  },
  data() {
    return {
      index: 0,
      tabMapOptions: [
        { label: `站点-${this.$route.query.site_cnt ? this.$route.query.site_cnt : '0'}`, key: 'site' },
        { label: `子域名-${this.$route.query.domain_cnt ? this.$route.query.domain_cnt : '0'}`, key: 'domain' },
        { label: `IP-${this.$route.query.ip_cnt ? this.$route.query.ip_cnt : '0'}`, key: 'ip' },
        { label: `SSL-${this.$route.query.cert_cnt ? this.$route.query.cert_cnt : '0'}`, key: 'ssl' },
        { label: `服务-${this.$route.query.service_cnt ? this.$route.query.service_cnt : '0'}`, key: 'server' },
        { label: `文件泄露-${this.$route.query.fileleak_cnt ? this.$route.query.fileleak_cnt : '0'}`, key: 'file' },
        { label: `URL-${this.$route.query.url_cnt ? this.$route.query.url_cnt : '0'}`, key: 'url' },
        { label: `风险-${this.$route.query.vuln_cnt ? this.$route.query.vuln_cnt : '0'}`, key: 'risk' },
        {
          label: `服务(python)-${this.$route.query.npoc_service_cnt ? this.$route.query.npoc_service_cnt : '0'}`,
          key: 'pyser'
        },
        { label: `C段-${this.$route.query.cip_cnt ? this.$route.query.cip_cnt : '0'}`, key: 'c' },
        {
          label: `nuclei-${this.$route.query.nuclei_result_cnt ? this.$route.query.nuclei_result_cnt : '0'}`,
          key: 'vul'
        },
        {
          label: `指纹统计-${this.$route.query.stat_finger_cnt ? this.$route.query.stat_finger_cnt : '0'}`,
          key: 'fing'
        },
        { label: `未授权-${this.$route.query.unauth_cnt ? this.$route.query.unauth_cnt : '0'}`, key: 'unauth' },
        { label: `xray-${this.$route.query.xray_result_cnt ? this.$route.query.xray_result_cnt : '0'}`, key: 'xray' },
        { label: `wih-${this.$route.query.wih_cnt ? this.$route.query.wih_cnt : '0'}`, key: 'wih' }
      ],
      activeName: 'site',
      createdTimes: 0
    }
  },
  computed: {
    listQuery() {
      return (idx) => ({
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
        unauth_cnt: this.$route.query.unauth_cnt,
        wih_cnt: this.$route.query.wih_cnt,
        xray_result_cnt: this.$route.query.xray_result_cnt,
        stat_finger_cnt: this.$route.query.stat_finger_cnt,
        tabIndex: idx,
        ts: new Date().getTime()
      })
    }
  },
  watch: {
    activeName(val) {
      // 获取当前活动tab的索引
      const idx = this.tabMapOptions.findIndex(item => item.key === val)
      // 如果找到相应的tab，则获取查询参数并添加到URL中
      if (idx !== -1) {
        const parameters = this.listQuery(idx)
        this.$router.push({ path: `${this.$route.path}?tab=${val}`, query: parameters })
      }
    }
  },
  created() {
    // init the default selected tab
    const tab = this.$route.query.tab
    if (tab) {
      this.activeName = tab
    }
  },
  methods: {
  }
}
</script>

<style scoped>
  .tab-container {
    margin: 30px;
  }
</style>
