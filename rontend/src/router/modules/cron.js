/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const CronRouter = {
  path: '/cron',
  component: Layout,
  redirect: '/cron/cron-info',
  meta: {
    icon: 'el-icon-message-solid'
  },
  children: [
    {
      path: 'cron-info',
      component: () => import('@/views/table/cron-info'),
      name: 'cron-info',
      meta: { title: '计划任务' }
    }
  ]
}

export default CronRouter
