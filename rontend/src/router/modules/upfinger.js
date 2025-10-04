/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const UpfigRouter = {
  path: '/upfig',
  component: Layout,
  redirect: '/upfig/upfinger-info',
  meta: {
    icon: 'el-icon-plus'
  },
  children: [
    {
      path: 'upfinger-info',
      component: () => import('@/views/table/upfinger-info'),
      name: 'upfinger-info',
      meta: { title: '指纹管理' }
    }
  ]
}

export default UpfigRouter
