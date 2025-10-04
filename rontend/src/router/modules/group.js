/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const GroupRouter = {
  path: '/group',
  component: Layout,
  redirect: '/group/group-info',
  meta: {
    icon: 'tree'
  },
  children: [
    {
      path: 'group-info',
      component: () => import('@/views/table/group-info'),
      name: 'group-info',
      meta: { title: '资产分组' }
    }
  ]
}

export default GroupRouter
