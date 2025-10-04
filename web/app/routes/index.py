# -*- coding: utf-8 -*-
"""
@Time ： 2023/7/18 4:44 PM
@Auth ： xinghe
@File ：index.py
@IDE ：PyCharm
@Motto:但行好事，莫问前程
"""
import json

import psutil
from flask_restx import fields, Namespace
from app.utils import get_logger, auth
from . import base_query_fields, ARLResource, get_arl_parser
from app.utils import conn_db as conn
import platform
import socket
import subprocess
import distro, docker

from ..arlconfig import Config

ns = Namespace('index', description="主页信息")

logger = get_logger()

base_search_fields = {
    'task_id': fields.String(description="js链接"),
    'url': fields.String(description="url"),
    'status_code': fields.String(description="状态码"),
}

base_search_fields.update(base_query_fields)


@ns.route('/')
class IndexData(ARLResource):
    parser = get_arl_parser(base_search_fields, location='args')

    @auth
    @ns.expect(parser)
    def get(self):
        """
        未授权信息查询
        """

        data = self.index_data()
        return data

    def is_service_running(self):
        client = docker.from_env()
        container_names = ['arl_web', 'arl_worker', 'arl_scheduler', 'arl_mongodb', 'arl_rabbitmq']
        result = {}
        for container_name in container_names:
            try:
                container = client.containers.get(container_name)
                status = container.status
                result[container_name] = status
            except docker.errors.NotFound:
                result[container_name] = "error"
        return result

    def index_data(self):
        """
        主页数据
        """
        task_cnt = conn('task').count()
        site_cnt = conn('site').count()
        domain_cnt = conn('domain').count()
        vul_cnt1 = conn('nuclei_result').count()
        vul_cnt2 = conn('vuln').count()
        vul_cnt3 = conn('npoc_service').count()
        vul_cnt4 = conn('xray_result').count()
        vul_cnt = vul_cnt4 + vul_cnt3 + vul_cnt2 + vul_cnt1

        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent

        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                process_info = {
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'memory': proc.info['memory_info'].rss
                }
                processes.append(process_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # 按照内存占用进行排序
        sorted_processes = sorted(processes, key=lambda x: x['memory'], reverse=True)
        top_processes = sorted_processes[:4]
        menm_list = []
        for process in top_processes:
            data = {
                "pid": process['pid'],
                "name": process['name']
            }
            menm_list.append(data)
        architecture = platform.machine()
        hostname = socket.gethostname()

        # 获取运行时间
        uptime_process = subprocess.Popen(['uptime', '-p'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        uptime_output, _ = uptime_process.communicate()
        uptime = uptime_output.decode().strip()
        distros = distro.linux_distribution()
        distros = str(distros).split(',')[0][2:-1]

        sys = {
            "os": architecture,
            "name": hostname,
            "runtime": uptime,
            "distro": distros
        }

        if Config.ISDOCKER_KEY == "docker":
            result = self.is_service_running() #容器部署使用这个
        else:
            result = {
                "arl_web": "running",
                "arl_worker": "running",
                "arl_scheduler": "exit",
                "arl_mongodb": "running",
                "arl_rabbitmq": "running"
            }


        data = {
            "message": "success",
            "code": 200,
            "data": {
                "task_cnt": task_cnt,
                "site_cnt": site_cnt,
                "domain_cnt": domain_cnt,
                "vul_cnt": vul_cnt,
                "cpu": cpu_percent,
                "memoryinfo": {
                    "memory": memory_percent,
                    "menm_list": menm_list

                },
                "service": result,
                "sysinfo": sys,
                "disk": disk_percent
            }
        }
        return data
