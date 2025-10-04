<template>
  <div class="block" style="height: 450px; overflow: hidden;">
    <div class="timeline-container">
      <el-timeline>
        <el-timeline-item v-for="(item,index) of timeline" :key="index" :timestamp="item.timestamp" placement="top">
          <el-card>
            <h4>{{ item.title }}</h4>
            <p>{{ item.content }}</p>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </div>
  </div>
</template>

<style scoped>
.timeline-container {
  animation: scrollTimeline linear infinite;
  animation-duration: 30s; /* 滚动的总时长 */
}

@keyframes scrollTimeline {
  from {
    transform: translateY(0); /* 初始位置 */
  }
  to {
    transform: translateY(-100%); /* 滚动距离，根据实际需求调整 */
  }
}
</style>
<script>
export default {
  data() {
    return {
      timeline: [
        {
          timestamp: '2025/10/30',
          title: 'cnvd',
          content: '已通过'
        },
        {
          timestamp: '2025/10/30',
          title: 'cnnvd',
          content: '已通过'
        },
        {
          timestamp: '2025/10/30',
          title: 'nvdb',
          content: '已通过'
        },
        {
          timestamp: '2025/10/30',
          title: 'ncc',
          content: '已通过'
        },
        {
          timestamp: '2025/10/30',
          title: '补天',
          content: '已通过'
        },
        {
          timestamp: '2025/10/30',
          title: '腾讯SRC',
          content: '已通过'
        },
        {
          timestamp: '2025/10/30',
          title: 'EDU',
          content: '已通过'
        },
        {
          timestamp: '2025/10/30',
          title: '360众测',
          content: '已通过'
        },
        {
          timestamp: '2025/10/30',
          title: '漏洞盒子',
          content: '已通过'
        }
      ]
    }
  },
}
</script>
