# -*- coding: utf-8 -*-
"""
@Time ： 2023/7/7 4:13 PM
@Auth ： xinghe
@File ：unauth.py
@IDE ：PyCharm
@Motto:但行好事，莫问前程
"""
from bson import ObjectId
from flask_restx import Resource, Api, reqparse, fields, Namespace
from app.utils import get_logger, auth
from . import base_query_fields, ARLResource, get_arl_parser
from app.services.npoc import NPoC
from app import utils, celerytask

ns = Namespace('xray_result', description="xray信息")

logger = get_logger()

base_search_fields = {
    'task_id': fields.String(description="任务id"),
    'plugin': fields.String(description="扫描插件"),
}

base_search_fields.update(base_query_fields)


@ns.route('/')
class Xray(ARLResource):
    parser = get_arl_parser(base_search_fields, location='args')

    @auth
    @ns.expect(parser)
    def get(self):
        """
        xray信息查询
        """
        args = self.parser.parse_args()
        data = self.build_data(args=args, collection='xray_result')

        return data
