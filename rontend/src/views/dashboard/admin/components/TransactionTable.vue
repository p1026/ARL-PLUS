<template>
  <el-table :data="list" style="width: 100%;padding-top: 15px;">
    <el-table-column label="任务名称" min-width="200">
      <template slot-scope="scope">
        {{ scope.row.name}}
      </template>
    </el-table-column>
    <el-table-column label="目标" width="395" align="center">
      <template slot-scope="scope">
        {{ scope.row.target }}
      </template>
    </el-table-column>
    <el-table-column label="状态" width="200" align="center">
      <template slot-scope="{row}">
        <el-tag :type="row.status | statusFilter">
          {{ row.status }}
        </el-tag>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
import { fetchList } from '@/api/article'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        done: 'success',
        error: 'danger'
      }
      return statusMap[status]
    },
    orderNoFilter(str) {
      return str.substring(0, 30)
    }
  },
  data() {
    return {
      list: {
        page: 1,
        size: 8
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      fetchList(this.list).then(response => {
        this.list = response.items
      })
    }
  }
}
</script>
