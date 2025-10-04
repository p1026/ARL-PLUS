/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const ServiceRouter = {
  path: '/task',
  component: Layout,
  redirect: '/task/service-info',
  meta: {
    icon: 'component'
  },
  children: [
    {
      path: 'service-info',
      component: () => import('@/views/table/service-info'),
      name: 'service-info',
      meta: { title: '服务信息' }
    }
  ]
}

export default ServiceRouter
