<template>
  <el-row :gutter="40" class="panel-group">
    <!-- 基础统计卡片 -->
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="indxData">
        <div class="card-panel-icon-wrapper icon-people">
          <svg-icon icon-class="chart" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            项目数量
          </div>
          <router-link to="../../task/add-task" class="card-panel-num link-type" :duration="2600" :start-val="0">{{list.task_cnt}}</router-link>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="indxData">
        <div class="card-panel-icon-wrapper icon-message">
          <svg-icon icon-class="eye-open" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            WEB站点
          </div>
          <router-link to="../../task/allweb-info" class="card-panel-num link-type" :duration="3000" :start-val="0">{{ list.site_cnt }}</router-link>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="indxData">
        <div class="card-panel-icon-wrapper icon-money">
          <svg-icon icon-class="guide" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            发现子域
          </div>
          <router-link to="../../task/alldomain-info" class="card-panel-num link-type" :duration="3200" :start-val="0">{{ list.domain_cnt }}</router-link>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="indxData">
        <div class="card-panel-icon-wrapper icon-shopping">
          <svg-icon icon-class="bug" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            漏洞数量
          </div>
          <router-link to="../../task/allnuclei-info" class="card-panel-num link-type" :duration="3600" :start-val="0">{{ list.vul_cnt }}</router-link>
        </div>
      </div>
    </el-col>
    
    <!-- 第二行：系统监控信息 -->
    <el-col :xs="24" :sm="24" :lg="24" class="card-panel-col">
      <el-row :gutter="20">
        <!-- CPU 使用率 -->
        <el-col :xs="12" :sm="6" :lg="3">
          <div class="card-panel cpu-panel" @click="indxData">
            <div class="panel-title">CPU：</div>
            <div class="circle-progress-wrapper">
              <div class="circle-progress" :style="{ background: `conic-gradient(#007bff ${list.cpu * 3.6}deg, #f0f0f0 0deg)` }"></div>
              <span class="progress-num">{{ list.cpu }}%</span>
            </div>
          </div>
        </el-col>

        <!-- 内存使用率 -->
        <el-col :xs="12" :sm="6" :lg="3">
          <div class="card-panel memory-panel" @click="indxData">
            <div class="panel-title">内存：</div>
            <div class="memory-content">
              <div class="memory-progress-wrapper">
                <div class="memory-progress" :style="{ width: list.memoryinfo.memory + '%' }"></div>
              </div>
              <span class="progress-num">{{ list.memoryinfo.memory }}%</span>
            </div>
          </div>
        </el-col>

        <!-- 容器状态 -->
        <el-col :xs="24" :sm="12" :lg="9">
          <div class="card-panel container-panel" @click="indxData">
            <div class="panel-title">容器：</div>
            <div class="container-list">
              <div v-for="(status, serviceName) in list.service" :key="serviceName" class="container-item">
                <span v-if="status === 'running'" class="status-running">
                  <i class="status-dot running"></i>
                  {{ serviceName }}: {{ status }}
                </span>
                <span v-else class="status-stopped">
                  <i class="status-dot stopped"></i>
                  {{ serviceName }}: {{ status }}
                </span>
              </div>
            </div>
          </div>
        </el-col>

        <!-- 系统信息 -->
        <el-col :xs="24" :sm="12" :lg="9">
          <div class="card-panel system-panel" @click="indxData">
            <div class="panel-title">系统：</div>
            <div class="system-info">
              <div class="system-item">
                <span class="system-label">系统:</span>
                <span class="system-value">{{ list.sysinfo.distro }} {{ list.sysinfo.os }}</span>
              </div>
              <div class="system-item">
                <span class="system-label">主机:</span>
                <span class="system-value">{{ list.sysinfo.name }}</span>
              </div>
              <div class="system-item">
                <span class="system-label">运行:</span>
                <span class="system-value">{{ list.sysinfo.runtime }}</span>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-col>

    <!-- 第三行：进程信息 -->
    <el-col :xs="24" :sm="24" :lg="24" class="card-panel-col">
      <div class="card-panel process-panel" @click="indxData">
        <div class="panel-title">进程信息：</div>
        <div class="process-list">
          <div v-for="item in menmList" :key="item.pid" class="process-item">
            <div class="process-pid">PID: <span class="process-value">{{ item.pid }}</span></div>
            <div class="process-name">Name: <span class="process-value">{{ item.name }}</span></div>
          </div>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<style scoped>
.panel-group {
  margin-top: 18px;
}

.card-panel-col {
  margin-bottom: 20px;
}

/* 基础卡片样式 */
.card-panel {
  height: auto;
  min-height: 120px;
  cursor: pointer;
  font-size: 14px;
  position: relative;
  overflow: hidden;
  color: #666;
  background: #fff;
  box-shadow: 4px 4px 40px rgba(0, 0, 0, .05);
  border-radius: 8px;
  padding: 20px;
  box-sizing: border-box;
  transition: all 0.3s ease;

  &:hover {
    box-shadow: 4px 4px 20px rgba(0, 0, 0, .1);
    transform: translateY(-2px);
  }
}

.panel-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #333;
}

/* CPU 面板样式 */
.cpu-panel {
  text-align: center;
}

.circle-progress-wrapper {
  position: relative;
  width: 80px;
  height: 80px;
  margin: 0 auto;
}

.circle-progress {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.progress-num {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

/* 内存面板样式 */
.memory-panel {
  text-align: center;
}

.memory-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.memory-progress-wrapper {
  width: 100px;
  height: 20px;
  background-color: #f0f0f0;
  border-radius: 10px;
  overflow: hidden;
}

.memory-progress {
  height: 100%;
  background-color: #007bff;
  transition: width 0.3s ease;
  border-radius: 10px;
}

/* 容器面板样式 */
.container-panel {
  height: auto;
}

.container-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 8px;
}

.container-item {
  display: flex;
  align-items: center;
  font-size: 13px;
}

.status-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 8px;
}

.status-dot.running {
  background-color: #52c41a;
}

.status-dot.stopped {
  background-color: #ff4d4f;
}

.status-running {
  color: #52c41a;
  font-weight: 500;
}

.status-stopped {
  color: #ff4d4f;
  font-weight: 500;
}

/* 系统信息面板样式 */
.system-panel {
  height: auto;
}

.system-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.system-item {
  display: flex;
  align-items: center;
  font-size: 13px;
}

.system-label {
  min-width: 40px;
  color: #666;
  margin-right: 8px;
}

.system-value {
  color: #333;
  font-weight: 500;
}

/* 进程信息面板样式 */
.process-panel {
  height: auto;
}

.process-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
}

.process-item {
  background: #f8f9fa;
  padding: 12px;
  border-radius: 6px;
  border-left: 4px solid #007bff;
}

.process-pid, .process-name {
  font-size: 12px;
  margin: 4px 0;
  line-height: 1.4;
}

.process-value {
  color: #1890ff;
  font-weight: bold;
}

/* 基础统计卡片样式 */
.card-panel-icon-wrapper {
  float: left;
  margin: 0;
  padding: 16px;
  transition: all 0.38s ease-out;
  border-radius: 6px;
}

.card-panel-icon {
  float: left;
  font-size: 48px;
}

.card-panel-description {
  float: right;
  font-weight: bold;
  margin: 0;
}

.card-panel-text {
  line-height: 18px;
  color: rgba(0, 0, 0, 0.45);
  font-size: 16px;
  margin-bottom: 12px;
}

.card-panel-num {
  font-size: 20px;
}

/* 悬停效果 */
.card-panel:hover {
  .card-panel-icon-wrapper {
    color: #fff;
  }

  .icon-people {
    background: #40c9c6;
  }

  .icon-message {
    background: #36a3f7;
  }

  .icon-money {
    background: #f4516c;
  }

  .icon-shopping {
    background: #34bfa3;
  }
}

.icon-people {
  color: #40c9c6;
}

.icon-message {
  color: #36a3f7;
}

.icon-money {
  color: #f4516c;
}

.icon-shopping {
  color: #34bfa3;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .container-list {
    grid-template-columns: 1fr;
  }
  
  .process-list {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .card-panel {
    padding: 15px;
  }
}

@media (max-width: 550px) {
  .process-list {
    grid-template-columns: 1fr;
  }
  
  .card-panel-description {
    display: block;
  }
}
</style>

<script>
import { indexList } from '@/api/remote-search'

export default {
  components: {
  },
  data() {
    return {
      list: {
        task_cnt: 0,
        site_cnt: 0,
        domain_cnt: 0,
        vul_cnt: 0,
        cpu: 0,
        memory: 0,
        disk: 0,
        memoryinfo: {
          memory: 0,
          menm_list: []
        },
        service: {},
        sysinfo: {
          distro: '',
          os: '',
          name: '',
          runtime: ''
        }
      },
      menmList: []
    }
  },
  created() {
    this.indxData()
  },
  methods: {
    handleSetLineChartData(type) {
      this.$emit('handleSetLineChartData', type)
    },
    indxData() {
      indexList().then(response => {
        this.list = response.data
        this.menmList = response.data.memoryinfo.menm_list || []
        console.log(response.data.memoryinfo.menm_list)
      })
    }
  }
}
</script>