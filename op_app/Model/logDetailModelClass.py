#!/usr/bin/python
# -*- coding: UTF-8 -*-

from op_app.Model.base.baseModelClass import BaseDbModelClass
from op_app.Model.permissionModelClass import PermissionModelClass
from op_app.logger.log import dblog
from op_app.lib import pub
import json
from op_app.Extends.paramikoTool import ParamikoTool
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class LogDetailModelClass(BaseDbModelClass):

    def __init__(self, request):
        super(LogDetailModelClass, self).__init__()
        self.request = request
        self.uid = self.request.user.id
        self.project_id = self.request.POST.get('project_id', '')
        self.env_id = self.request.POST.get('env_id', '')
        self.app_id = self.request.POST.get('app_id', '')
        self.ip = self.request.POST.get('ip', '')
        self.server_type = self.request.POST.get('server_type', '')
        self.server_id = self.request.POST.get('server_id', '')
        self.action = self.request.POST.get('action', '')

    def logDetail(self):
        # 判断前端传来的参数
        if self.project_id == '' or self.env_id == '' or self.app_id == '' or self.ip == ''\
                or self.action == ''or self.server_type == '' or self.server_id == '':
            print('invaild action args from web...')
            dblog.error("[ERROR] --wrong action args from web-----, Catch exception:, file: [ %s ], line: [ %s ]"
                        %(__file__,sys._getframe().f_lineno))
            return 'invaild action args from web...'
        #判断用户是否有权限
        web_args = [self.uid,self.server_type,self.server_id]

        user_permits = PermissionModelClass()
        if not user_permits.hasAccessPermission(*web_args):
            print('no permission')
            return 'no permission'
        else:
            pt = ParamikoTool()
            pt.getlogrow()
