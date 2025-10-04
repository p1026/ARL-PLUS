<template>
  <el-form>
    <el-form-item label="旧密码">
      <el-input v-model.trim="user.old_password" />
    </el-form-item>
    <el-form-item label="密码">
      <el-input v-model.trim="user.new_password" />
    </el-form-item>
    <el-form-item label="确认密码">
      <el-input v-model.trim="user.check_password" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submit">Update</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import { chpasswd } from '@/api/article'
import store from '@/store'

export default {
  props: {
    user: {
      type: Object,
      default: () => {
        return {
          check_password: '',
          new_password: '',
          old_password: ''
        }
      }
    }
  },
  methods: {
    submit() {
      const data = {
        old_password: this.user.old_password,
        new_password: this.user.new_password,
        check_password: this.user.check_password
      }
      chpasswd(data).then(response => {
        if (response.code === 200) {
          this.dialogFormVisible = false
          this.$message({
            message: response.message,
            type: 'success',
            duration: 2000
          })
          setTimeout(() => {
            store.dispatch('user/resetToken').then(() => {
              location.reload()
            })
          }, 3000)
        } else {
          // 在这里处理其他情况，例如显示错误信息
          this.$message({
            message: response.message,
            type: 'error',
            duration: 2000
          })
        }
      }).catch(error => {
        this.$message({
          message: error,
          type: 'error',
          duration: 2000
        })
      })
    }
  }
}
</script>
