#!/usr/bin/env python
# -*- coding: utf-8 -*-

from op_app.Model.serviceManageActionModelClass import ManageActionModelClass
from op_app.logger.log import runlog

class ManageActionControllerClass(object):

    # 检测是否有session 构造函数
    def __init__(self, request):
        self.request = request


    def getAction(self): #
        #print '------>',user.username,type(user),type(user.username)
        i_class = ManageActionModelClass(self.request)
        data = i_class.Action()
        import json
        #runlog.info('getProjectInfo data: %s' % (json.dumps(data, indent=4)))
        return data





