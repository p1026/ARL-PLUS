/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const PocRouter = {
  path: '/poc',
  component: Layout,
  redirect: '/poc/poc-info',
  meta: {
    icon: 'edit'
  },
  children: [
    {
      path: 'poc-info',
      component: () => import('@/views/table/poc-info'),
      name: 'poc-info',
      meta: { title: 'POC信息' }
    }
  ]
}

export default PocRouter
