/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const TaskRouter = {
  path: '/task',
  component: Layout,
  redirect: '/task/add-task',
  name: 'Table',
  meta: {
    title: '任务管理',
    icon: 'table'
  },
  children: [
    {
      path: 'add-task',
      component: () => import('@/views/table/add-task'),
      name: 'add-task',
      meta: { title: '任务管理' }
    },
    {
      path: 'web-info',
      component: () => import('@/views/table/web-info'),
      name: 'web-info',
      meta: { title: '站点信息' },
      hidden: true
    },
    {
      path: 'domain-info',
      component: () => import('@/views/table/domain-info'),
      name: 'host-info',
      meta: { title: '域名信息' },
      hidden: true
    },
    {
      path: 'host-info',
      component: () => import('@/views/table/host-info'),
      name: 'host-info',
      meta: { title: '主机信息' },
      hidden: true
    },
    {
      path: 'service-info',
      component: () => import('@/views/table/service-info'),
      name: 'service-info',
      meta: { title: '服务信息' },
      hidden: true
    },
    {
      path: 'vul-info',
      component: () => import('@/views/table/vul-info'),
      name: 'vul-info',
      meta: { title: '漏洞信息' },
      hidden: true
    },
    {
      path: 'webfing-info',
      component: () => import('@/views/table/webfing-info'),
      name: 'webfing-info',
      meta: { title: '指纹信息' },
      hidden: true
    }
  ]
}

export default TaskRouter
