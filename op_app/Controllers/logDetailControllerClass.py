#!/usr/bin/env python
# -*- coding: utf-8 -*-

from op_app.Model.logDetailModelClass import LogDetailModelClass
from op_app.logger.log import runlog

class LogDetailControllerClass(object):

    # 检测是否有session 构造函数
    def __init__(self, request):
        self.request = request


    def getLogDetail(self): #
        #print '------>',user.username,type(user),type(user.username)
        i_class = LogDetailModelClass(self.request)
        return i_class.logDetail()
        import json
        #runlog.info('getProjectInfo data: %s' % (json.dumps(data, indent=4)))
        # return data





