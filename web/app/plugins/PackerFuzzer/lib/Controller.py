# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
import html
import os
import sqlite3

from lib.ParseJs import ParseJs
from lib.vulnTest import vulnTest
from lib.common.utils import Utils
from lib.getApiText import ApiText
from lib.ApiCollect import Apicollect
from lib.Database import DatabaseType
from lib.FuzzParam import FuzzerParam
from lib.CheckPacker import CheckPacker
from lib.PostApiText import PostApiText
from lib.common.beautyJS import BeautyJs
from lib.Recoverspilt import RecoverSpilt
from lib.CreateReport import CreateReport
from lib.getApiResponse import ApiResponse
from lib.LoadExtensions import loadExtensions
from lib.reports.CreatWord import Docx_replace
from lib.common.CreatLog import creatLog, log_name, logs
from lib.common import readConfig
from app.arlconfig import Config


def build_data(url, jslink, content):
    data = dict()
    data['url'] = str(url)[2:-2]
    data['jslink'] = str(jslink)[2:-2]
    data['len'] = f'{len(str(content)[2:-2])}'
    data['status_code'] = 200
    if len(str(url)[2:-2]) < 2000:
        data['content'] = html.unescape(str(content)[2:-2])
    else:
        data['content'] = str(url)[2:-2]
    return data

class Project():

    def __init__(self, url, options):
        self.url = url
        self.codes = {}
        self.options = options
        self.resultFilters = readConfig.ReadConfig().getValue('vulnTest', 'resultFilter')[0]

    def parseStart(self):
        projectTag = logs
        DatabaseType(projectTag).createDatabase()
        ParseJs(projectTag, self.url, self.options).parseJsStart()
        checkResult = CheckPacker(projectTag, self.url, self.options).checkStart()
        if checkResult == 1 or checkResult == 777:
            if checkResult != 777:
                creatLog().get_logger().info("[!] " + Utils().getMyWord("{check_pack_s}"))
            RecoverSpilt(projectTag, self.options).recoverStart()
        else:
            creatLog().get_logger().info("[!] " + Utils().getMyWord("{check_pack_f}"))
        Apicollect(projectTag, self.options).apireCoverStart()
        apis = DatabaseType(projectTag).apiPathFromDB()  # 从数据库中提取出来的api
        self.codes = ApiResponse(apis, self.options).run()
        DatabaseType(projectTag).insertResultFrom(self.codes)
        if self.options.sendtype == "GET" or self.options.sendtype == "get":
            allPaths = DatabaseType(projectTag).allPathFromDB()
            getTexts = ApiText(allPaths, self.options).run()  # 对get请求进行一个获取返回包
            DatabaseType(projectTag).updatePathsMethod(1)
            DatabaseType(projectTag).insertTextFromDB(getTexts)
        elif self.options.sendtype == "POST" or self.options.sendtype == "post":
            allPaths = DatabaseType(projectTag).allPathFromDB()
            postTexts = PostApiText(allPaths, self.options).run()
            DatabaseType(projectTag).updatePathsMethod(2)
            DatabaseType(projectTag).insertTextFromDB(postTexts)
        else:
            getPaths = DatabaseType(projectTag).sucesssPathFromDB()  # 获取get请求的path
            getTexts = ApiText(getPaths, self.options).run()  # 对get请求进行一个获取返回包
            postPaths = DatabaseType(projectTag).wrongMethodFromDB()  # 获取post请求的path
            if len(postPaths) != 0:
                postTexts = PostApiText(postPaths, self.options).run()
                DatabaseType(projectTag).insertTextFromDB(postTexts)
            DatabaseType(projectTag).insertTextFromDB(getTexts)
        if self.options.type == "adv":
            creatLog().get_logger().info("[!] " + Utils().getMyWord("{adv_start}"))
            creatLog().get_logger().info(Utils().tellTime() + Utils().getMyWord("{beauty_js}"))
            BeautyJs(projectTag).rewrite_js()
            creatLog().get_logger().info(Utils().tellTime() + Utils().getMyWord("{fuzzer_param}"))
            FuzzerParam(projectTag).FuzzerCollect()
        creatLog().get_logger().info(Utils().tellTime() + Utils().getMyWord("{response_end}"))
        vulnTest(projectTag, self.options).testStart(self.url)
        data = self.dbtest()
        data = str(data)[1:-1]
        if data != "":
            with open(Config.PFresult_PATH + f"{self.options.out}_result.json", 'a+') as f:
                f.write(data + ',')

    def deletedir(self):
        os.sep.join()

    def dbtest(self):
        projectDBPath = DatabaseType(logs).getPathfromDB() + logs + ".db"
        connect = sqlite3.connect(os.sep.join(projectDBPath.split('/')))
        cursor = connect.cursor()
        connect.isolation_level = None
        sql = "select * from vuln"
        cursor.execute(sql)
        api_infos = cursor.fetchall()
        result = []
        for i in range(len(api_infos)):
            sql = f'select path from api_tree where id={api_infos[i][1]}'
            cursor.execute(sql)
            urls = cursor.fetchall()
            sql = f'select path from js_file where id={api_infos[i][2]}'
            cursor.execute(sql)
            jslink = cursor.fetchall()
            if urls != [] and jslink != []:
                for resultfilter in self.resultFilters.split(","):
                    if resultfilter not in str(api_infos[i][6]):
                        result.append(build_data({str(urls[0])[2:-3]}, {str(jslink[0])[2:-3]}, {str(api_infos[i][6])}))
        return result
