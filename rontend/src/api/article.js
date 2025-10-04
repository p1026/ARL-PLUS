import request from '@/utils/request'

export function fetchList(query) {
  return request({
    url: '/task/',
    method: 'get',
    params: query
  })
}

export function syncList(query) {
  return request({
    url: 'task/sync_scope/',
    method: 'get',
    params: query
  })
}

export function monitorList(query) {
  return request({
    url: '/scheduler/',
    method: 'get',
    params: query
  })
}

export function ruleList(query) {
  return request({
    url: '/policy/',
    method: 'get',
    params: query
  })
}

export function groupList(query) {
  return request({
    url: '/asset_scope/',
    method: 'get',
    params: query
  })
}

export function srcList(query) {
  return request({
    url: '/src/',
    method: 'get',
    params: query
  })
}

export function domainList(query) {
  return request({
    url: '/domain/',
    method: 'get',
    params: query
  })
}

export function pocList(query) {
  return request({
    url: '/poc/',
    method: 'get',
    params: query
  })
}

export function upfigList(query) {
  return request({
    url: '/fingerprint/',
    method: 'get',
    params: query
  })
}

export function scheduleList(query) {
  return request({
    url: '/task_schedule/',
    method: 'get',
    params: query
  })
}

export function gitList(query) {
  return request({
    url: '/github_task/',
    method: 'get',
    params: query
  })
}

export function gitdataList(query) {
  return request({
    url: '/github_result/',
    method: 'get',
    params: query
  })
}

export function gitcronList(query) {
  return request({
    url: '/github_scheduler/',
    method: 'get',
    params: query
  })
}

export function pocDelete(query) {
  return request({
    url: '/poc/delete/',
    method: 'get',
    params: query
  })
}

export function pocSync(query) {
  return request({
    url: '/poc/sync/',
    method: 'get',
    params: query
  })
}
export function hostList(query) {
  return request({
    url: '/ip/',
    method: 'get',
    params: query
  })
}

export function webList(query) {
  return request({
    url: '/site/',
    method: 'get',
    params: query
  })
}

export function downloadSite(query) {
  return request({
    url: '/site/export/',
    method: 'get',
    params: query,
    responseType: 'blob'
  })
}

export function fileList(query) {
  return request({
    url: '/fileleak/',
    method: 'get',
    params: query
  })
}

export function vulList(query) {
  return request({
    url: '/nuclei_result/',
    method: 'get',
    params: query
  })
}

export function xrayList(query) {
  return request({
    url: '/xray_result/',
    method: 'get',
    params: query
  })
}

export function urlList(query) {
  return request({
    url: '/url/',
    method: 'get',
    params: query
  })
}

export function unauthList(query) {
  return request({
    url: '/unauth/',
    method: 'get',
    params: query
  })
}

export function wihList(query) {
  return request({
    url: '/wih/',
    method: 'get',
    params: query
  })
}
export function serList(query) {
  return request({
    url: '/service/',
    method: 'get',
    params: query
  })
}

export function pyserList(query) {
  return request({
    url: '/npoc_service/',
    method: 'get',
    params: query
  })
}

export function cList(query) {
  return request({
    url: '/cip/',
    method: 'get',
    params: query
  })
}

export function fingList(query) {
  return request({
    url: '/stat_finger/',
    method: 'get',
    params: query
  })
}

export function sslList(query) {
  return request({
    url: '/cert/',
    method: 'get',
    params: query
  })
}

export function vulnList(query) {
  return request({
    url: '/vuln/',
    method: 'get',
    params: query
  })
}

export function fetchArticle(id) {
  return request({
    url: '/vue-element-admin/article/detail',
    method: 'get',
    params: { id }
  })
}

export function fetchPv(pv) {
  return request({
    url: '/vue-element-admin/article/pv',
    method: 'get',
    params: { pv }
  })
}

export function createArticle(data) {
  return request({
    url: '/task/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}

export function createruletask(data) {
  return request({
    url: '/task/policy/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}

export function figup(file) {
  const data = new FormData()
  data.append('file', file) // "file" is the field name, as per your example
  return request({
    url: '/fingerprint/upload/',
    method: 'post',
    data: data
  })
}

export function policycreate(data) {
  return request({
    url: '/policy/add/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}

export function clear(data) {
  return request({
    url: '/clear/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}

export function figcreate(data) {
  return request({
    url: '/fingerprint/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}

export function schedulecreate(data) {
  return request({
    url: '/task_schedule/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}
export function gitcreate(data) {
  return request({
    url: '/github_task/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}
export function gitlscreate(data) {
  return request({
    url: '/github_scheduler/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}
export function addGroup(data) {
  return request({
    url: '/asset_scope/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}

export function addSrc(data) {
  return request({
    url: '/src/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}

export function listtaskGroup(data) {
  return request({
    url: '/scheduler/add/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}

export function sitetaskGroup(data) {
  return request({
    url: '/scheduler/add/site_monitor/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}

export function policyGroup(size) {
  return request({
    url: `/policy/?size=${size}`,
    method: 'get'
  })
}

export function resultSet(query) {
  return request({
    url: `/site/save_result_set/`,
    method: 'get',
    params: query
  })
}
export function policyPlan(query) {
  return request({
    url: `/policy/`,
    method: 'get',
    params: query
  })
}

export function grouDelect(data) {
  return request({
    url: '/asset_scope/delete/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}

export function figDelect(data) {
  return request({
    url: '/fingerprint/delete/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}

export function scheduleDelect(data) {
  return request({
    url: '/task_schedule/delete/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}

export function scheduleStop(data) {
  return request({
    url: '/task_schedule/stop/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}

export function gitDelect(data) {
  return request({
    url: '/github_task/delete/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}

export function gitlsDelect(data) {
  return request({
    url: '/github_scheduler/delete/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}

export function gitlsRecover(data) {
  return request({
    url: '/github_scheduler/recover/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}

export function scheduleRecover(data) {
  return request({
    url: '/task_schedule/recover/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}

export function gitStop(data) {
  return request({
    url: '/github_task/stop/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}

export function gitlsStop(data) {
  return request({
    url: '/github_scheduler/stop/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}

export function addsync(data) {
  return request({
    url: '/task/sync/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}

export function grouDelectscope(scope_id, scope) {
  return request({
    url: `/asset_scope/delete/?scope_id=${scope_id}&scope=${scope}`,
    method: 'get',
    headers: {
      'Content-Type': 'application/json'
    }
  })
}

export function addGrouprange(data) {
  return request({
    url: '/asset_scope/add/',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}

export function updateSrc(data) {
  return request({
    url: '/src/',
    method: 'put',
    headers: {
      'Content-Type': 'application/json'
    },
    data: JSON.stringify(data)
  })
}
export function updateArticle(uid, data) {
  return request({
    url: `/v1/tasks/${uid}/`,
    method: 'put',
    data
  })
}

export function startArticle(data) {
  return request({
    url: '/api/task/start',
    method: 'post',
    data
  })
}

export function chpasswd(data) {
  return request({
    url: '/user/change_pass',
    method: 'post',
    dataType: 'json',
    data
  })
}

export function stopArticle(data) {
  return request({
    url: '/api/task/stop',
    method: 'post',
    data
  })
}

export function deleteArticle(data) {
  return request({
    url: `/task/delete/`,
    method: 'post',
    dataType: 'json',
    data
  })
}

export function reStart(data) {
  return request({
    url: `/task/restart/`,
    method: 'post',
    dataType: 'json',
    data
  })
}

export function Stop(id) {
  return request({
    url: `/task/stop/${id}`,
    method: 'get',
    dataType: 'json'
  })
}

export function batchdeleteArticle(data) {
  return request({
    url: `/task/delete/`,
    method: 'post',
    dataType: 'json',
    data
  })
}

export function batchdeletemonitor(data) {
  return request({
    url: `/scheduler/delete/`,
    method: 'post',
    dataType: 'json',
    data
  })
}

export function batchdeletesrc(data) {
  return request({
    url: `/src/`,
    method: 'delete',
    dataType: 'json',
    data
  })
}
export function ruledelete(data) {
  return request({
    url: `/policy/delete/`,
    method: 'post',
    dataType: 'json',
    data
  })
}

export function batchstopmonitor(data) {
  return request({
    url: `/scheduler/stop/batch`,
    method: 'post',
    dataType: 'json',
    data
  })
}

export function batchrecovermonitor(data) {
  return request({
    url: `/scheduler/recover/batch`,
    method: 'post',
    dataType: 'json',
    data
  })
}

export function batchrecovermonitor1(data) {
  return request({
    url: `/scheduler/recover/`,
    method: 'post',
    dataType: 'json',
    data
  })
}
