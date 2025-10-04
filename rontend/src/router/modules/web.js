/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const WebRouter = {
  path: '/task',
  component: Layout,
  redirect: '/task/allweb-info',
  meta: {
    title: '资产搜索',
    icon: 'search'
  },
  children: [
    {
      path: 'allweb-info',
      component: () => import('@/views/table/allweb-info'),
      name: 'allweb-info',
      meta: { title: '站点信息' }
    },
    {
      path: 'alldomain-info',
      component: () => import('@/views/table/alldomain-info'),
      name: 'alldomain-info',
      meta: { title: '子域信息' }
    },
    {
      path: 'allnuclei-info',
      component: () => import('@/views/table/allnuclei-info'),
      name: 'allnuclei-info',
      meta: { title: 'nuclei信息' }
    },
    {
      path: 'allxray-info',
      component: () => import('@/views/table/allxray-info'),
      name: 'allxray-info',
      meta: { title: 'xray信息' }
    }
  ]
}

export default WebRouter
