<template>
  <div>
    <el-badge v-if="showBadge" style="line-height: 25px;margin-top: -5px;" @click.native="dialogTableVisible=true" >
      <el-button style="padding: 8px 10px;" size="small" type="danger">
        <svg-icon icon-class="bug" />
      </el-button>
    </el-badge>

    <el-dialog :visible.sync="dialogTableVisible" width="40%" append-to-body>
      <div slot="title">
        <el-button size="mini" type="primary" icon="el-icon-delete" @click="clearAll">Clear</el-button>
      </div>
      <el-row :gutter="24">
        <el-col :span="6">
          <el-checkbox v-model="onetmp" :true-label="true" :false-label="false">Oneforall结果文件</el-checkbox>
        </el-col>
        <el-col :span="6">
          <el-checkbox v-model="arltmp" :true-label="true" :false-label="false">nuclei、xray缓存</el-checkbox>
        </el-col>
        <el-col :span="6">
          <el-checkbox v-model="pfztmp" :true-label="true" :false-label="false">PFZ未授权扫描缓存</el-checkbox>
        </el-col>
        <el-col :span="6">
          <el-checkbox v-model="pfzres" :true-label="true" :false-label="false">PFZ未授权结果缓存</el-checkbox>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import { clear } from '@/api/article'

export default {
  name: 'ErrorLog',
  data() {
    return {
      onetmp: false,
      arltmp: false,
      pfztmp: false,
      pfzres: false,
      dialogTableVisible: false
    }
  },
  computed: {
    errorLogs() {
      return this.$store.getters.errorLogs
    }
  },
  methods: {
    clearAll() {
      this.dialogTableVisible = false
      this.$confirm('确认清除后台缓存吗? 确认所有任务完成后清除，否则会造成数据丢失和程序中断', '提示', {
        type: 'warning'
      }).then(() => {
        const data = {
          'onetmp': this.onetmp,
          'arltmp': this.arltmp,
          'pfztmp': this.pfztmp,
          'pfzres': this.pfzres
        }
        clear(data).then(response => {
          if (response.code === 200) {
            this.$notify({
              title: '成功',
              message: '清除成功',
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
      })
    }
  }
}
</script>

<style scoped>
.message-title {
  font-size: 16px;
  color: #333;
  font-weight: bold;
  padding-right: 8px;
}
</style>
