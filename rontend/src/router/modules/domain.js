/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const DomainRouter = {
  path: '/task',
  component: Layout,
  redirect: '/task/domain-info',
  meta: {
    icon: 'nested'
  },
  children: [
    {
      path: 'domain-info',
      component: () => import('@/views/table/domain-info'),
      name: 'host-info',
      meta: { title: '域名信息' }
    }
  ]
}

export default DomainRouter