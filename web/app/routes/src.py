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
from app import utils, celerytask
from app.arlmodules import ErrorMsg, TaskStatus, CeleryAction
import copy

ns = Namespace('src', description="未授权信息")

logger = get_logger()

base_search_fields = {
    'name': fields.String(description="SRC名称"),
}

base_search_fields.update(base_query_fields)

add_task_fields = ns.model('AddSrc', {  # 添加任务字段
    'name': fields.String(required=True, description="SRC名"),
    'url': fields.String(required=True, description="公告地址"),
    'level': fields.String(required=True, description="活跃程度"),
    'range': fields.List(fields.String, description="收录范围"),
    "gift": fields.List(fields.String, description="奖励内容")
})

update_task_fields = ns.model('UpdateSrc', {  # 添加任务字段
    '_id': fields.String(required=True, description="_id"),
    'name': fields.String(required=True, description="SRC名"),
    'level': fields.String(required=True, description="活跃程度"),
    'url': fields.String(required=True, description="公告地址"),
    'range': fields.List(fields.String, description="收录范围"),
    "gift": fields.List(fields.String, description="奖励内容")
})

delete_finger_fields = ns.model('deleteSrc', {
    '_id': fields.String(required=True, description="指纹 _id")
})


@ns.route('/')
class Src(ARLResource):
    parser = get_arl_parser(base_search_fields, location='args')

    @auth
    @ns.expect(parser)
    def get(self):
        """
        src信息查询
        """
        args = self.parser.parse_args()
        data = self.build_data(args=args, collection='src')

        return data

    @auth
    @ns.expect(add_task_fields)
    def post(self):
        """
        添加SRC
        """
        args = self.parse_args(add_task_fields)
        args.update_date = utils.curr_date_obj()

        utils.conn_db('src').insert_one(args)

        ret = {
            "code": 200,
            "message": "success",
            "items": args
        }

        finger_id = str(args.pop('_id'))

        args.pop('update_date')
        return utils.build_ret(ErrorMsg.Success, {"_id": finger_id, "data": ret})

    @auth
    @ns.expect(update_task_fields)
    def put(self):
        """
        修改SRC
        """
        args = self.parse_args(update_task_fields)
        args.update_date = utils.curr_date_obj()
        id = args.pop('_id')

        utils.conn_db('src').update_one({'_id': ObjectId(id)}, {'$set': args})

        ret = {
            "code": 200,
            "message": "success",
            "items": args
        }

        args.pop('update_date')

        return utils.build_ret(ErrorMsg.Success, {"_id": id, "data": ret})

    @auth
    @ns.expect(delete_finger_fields)
    def delete(self):
        """
        删除SRC
        """
        args = self.parse_args(delete_finger_fields)
        id = args.pop('_id')
        query = {'_id': ObjectId(id)}
        utils.conn_db('src').delete_one(query)

        return utils.build_ret(ErrorMsg.Success, {"_id": id})
