import request from '@/utils/request'

export function searchUser(name) {
  return request({
    url: '/vue-element-admin/search/user',
    method: 'get',
    params: { name }
  })
}

export function transactionList(query) {
  return request({
    url: '/task/list',
    method: 'get',
    params: query
  })
}

export function indexList(query) {
  return request({
    url: '/index/',
    method: 'get',
    params: query
  })
}
