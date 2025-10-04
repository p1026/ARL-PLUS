/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const AllRouter = {
  path: '/task',
  component: Layout,
  redirect: '/task/all-info',
  children: [
    {
      path: 'all-info',
      component: () => import('@/views/tab/index'),
      name: 'all-info',
      meta: { title: '全部信息' },
      hidden: true
    }
  ]
}

export default AllRouter
