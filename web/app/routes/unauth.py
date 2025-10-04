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
from app.arlmodules import ErrorMsg, TaskStatus, CeleryAction
import copy

ns = Namespace('unauth', description="未授权信息")

logger = get_logger()

base_search_fields = {
    'task_id': fields.String(description="js链接"),
    'url': fields.String(description="url"),
    'status_code': fields.String(description="状态码"),
}

base_search_fields.update(base_query_fields)


@ns.route('/')
class UnAuth(ARLResource):
    parser = get_arl_parser(base_search_fields, location='args')

    @auth
    @ns.expect(parser)
    def get(self):
        """
        未授权信息查询
        """
        args = self.parser.parse_args()
        if args.status_code == '':
            args.status_code = None
        elif args.status_code is not None:
            args.status_code = int(args.status_code)
        data = self.build_data(args=args, collection='unauth')

        return data
