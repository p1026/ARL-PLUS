/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const RuleRouter = {
  path: '/rule',
  component: Layout,
  redirect: '/rule/rule-info',
  meta: {
    icon: 'nested'
  },
  children: [
    {
      path: 'rule-info',
      component: () => import('@/views/table/rule-info'),
      name: 'rule-info',
      meta: { title: '策略配置' }
    },
    {
      path: 'addrule-info',
      component: () => import('@/views/table/addrule-info'),
      name: 'addrule-info',
      meta: { title: '添加策略' },
      hidden: true
    }
  ]
}

export default RuleRouter
