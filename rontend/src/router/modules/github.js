/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const GitRouter = {
  path: '/github',
  component: Layout,
  redirect: '/github/github-info',
  meta: {
    title: 'github管理',
    icon: 'el-icon-s-flag'
  },
  children: [
    {
      path: 'github-info',
      component: () => import('@/views/table/github-info'),
      name: 'github-info',
      meta: { title: 'github任务' }
    },
    {
      path: 'githubtask-info',
      component: () => import('@/views/table/githubtask-info'),
      name: 'githubtask-info',
      meta: { title: 'github监控' }
    },
    {
      path: 'githubdata-info',
      component: () => import('@/views/table/githubdata-info'),
      name: 'githubdata-info',
      meta: { title: '仓库信息' },
      hidden: true
    }
  ]
}

export default GitRouter
