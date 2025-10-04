/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const MonitorRouter = {
  path: '/monitor',
  component: Layout,
  redirect: '/monitor/monitor-info',
  meta: {
    icon: 'tree-table'
  },
  children: [
    {
      path: 'monitor-info',
      component: () => import('@/views/table/monitor-info'),
      name: 'monitor-info',
      meta: { title: '资产监控' }
    }
  ]
}

export default MonitorRouter
