#!/usr/bin/python
# -*- coding: UTF-8 -*-

from op_app.Model.base.baseModelClass import BaseDbModelClass
from op_app.Model.permissionModelClass import PermissionModelClass
from op_app.Model.base.operation_dbModelClass import Operation_dbModelClass
from op_app.logger.log import dblog, runlog
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
        self.project_id = self.request.GET.get('project_id', '')
        self.env_id = self.request.GET.get('env_id', '')
        self.app_id = self.request.GET.get('app_id', '')
        self.ip = self.request.GET.get('ip', '')
        self.server_type = self.request.GET.get('server_type', '')
        self.server_id = self.request.GET.get('server_id', '')
        self.action = self.request.GET.get('action', '')

    def logDetail(self):
        # 判断前端传来的参数
        if self.project_id == '' or self.env_id == '' or self.app_id == '' or self.ip == ''\
                or self.action == ''or self.server_type == '' or self.server_id == '':
            print('p_id,e_id,a_id,ip,action,server_type,server_id,',self.project_id,self.env_id,self.app_id,self.ip,self.action,self.server_type,self.server_id)
            print('invaild action args from web...')
            dblog.error("[ERROR] --wrong action args from web-----, Catch exception:, file: [ %s ], line: [ %s ]"
                        %(__file__,sys._getframe().f_lineno))
            return 'invaild action args from web...'
        # 判断用户是否有权限,将前端获取到的服务器信息，放入一个列表中，与数据库中根据用户id获取的信息对比，
        web_args = [int(self.server_type), int(self.server_id)]
        # 实例化对象，获取用户的有权限的机器
        user_permits = PermissionModelClass(self.uid)
        if not user_permits.hasAccessPermission(*web_args):
            # print('no permission')
            runlog.info("--no permission to access the logfile from web-----, Catch exception:, file: [ %s ], line: [ %s ]"
                        %(__file__,sys._getframe().f_lineno))
            return 'no permission'
        else:
            # 获取app的用户名和密码
            instance = pub.appConfigDetail()
            res = instance.AppConfigDetail(self.server_type, self.app_id, self.server_id, self.env_id, self.project_id)
            print('logapp--res',res)
            if not res:
                runlog.error("the APP Data is null, file: [ %s ], line: [ %s ]" % (
                    __file__, sys._getframe().f_lineno))
            res_dic = dict()
            for i in res:
                res_dic['install_user'] = i[1]
                res_dic['app_type'] = i[2]
                res_dic['appdir'] = i[3]
                res_dic['app_name'] = i[6]
                res_dic['pass'] = i[7]
                res_dic['sshport'] = i[8]
            # 获取远程服务器日志目录指定行数的内容
            # print('dict_res',res_dic)
            if res_dic['app_type'] == '1': # app类型是tomcat
                if self.action == 'start':
                    log_file_path = '{}/logs/catalina.out'.format(res_dic['appdir'])
                # print('00---00',log_file_path)
                elif self.action == 'stop':
                    log_file_path = '/home/{}/service_manage/{}/scripts/log/stopapp.sh.log'.format(\
                        res_dic['install_user'], res_dic['app_name'])
                else:
                    runlog.error("the APP type is not tomcat, file: [ %s ], line: [ %s ]" % (
                        __file__, sys._getframe().f_lineno))
                    return 'invaild action to find the logfile'
                pt = ParamikoTool()  # 实例化对象后，获取日志后100行
                log_res = pt.getlogrow(self.ip, res_dic['sshport'], res_dic['install_user'], res_dic['pass'], log_file_path)
                # print('-------------',log_res)
                # 记录用户访问记录
                audit_log = Operation_dbModelClass()
                audit_log.inserToLog(res_dic['install_user'], self.ip, 'access', log_file_path)
                return log_res

            else:
                runlog.info("the APP type is not tomcat, file: [ %s ], line: [ %s ]" % (
                    __file__, sys._getframe().f_lineno))
                return 'just for app-type like tomcat..'


