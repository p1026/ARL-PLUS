/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const VulRouter = {
  path: '/task',
  component: Layout,
  redirect: '/task/vul-info',
  meta: {
    icon: 'chart'
  },
  children: [
    {
      path: 'vul-info',
      component: () => import('@/views/table/vul-info'),
      name: 'vul-info',
      meta: { title: '漏洞信息' }
    }
  ]
}

export default VulRouter