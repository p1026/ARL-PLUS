/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const GroupRouter = {
  path: '/src',
  component: Layout,
  redirect: '/src/src',
  meta: {
    icon: 'el-icon-s-finance'
  },
  children: [
    {
      path: 'src-info',
      component: () => import('@/views/table/src-info'),
      name: 'src-info',
      meta: { title: 'SRC信息' }
    }
  ]
}

export default GroupRouter
