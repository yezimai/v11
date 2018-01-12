#!/usr/bin/env python
# -*- coding: utf-8 -*-

from op_app.logger.log import runlog
from op_app.Model.base.baseModelClass import BaseDbModelClass
from op_app.Model.base.operation_dbModelClass import Operation_dbModelClass
from op_app.logger.log import dblog, runlog
from op_app.lib import appConfigDetailClass, pub
import json
from op_app.Extends.paramikoTool import ParamikoTool
import os
import sys

class LogDetailControllerClass(object):

    def __init__(self, request):
        # super(LogDetailControllerClass, self).__init__()
        self.request = request
        self.uid = self.request.user.id
        self.project_id = self.request.GET.get('project_id', '')
        self.env_id = self.request.GET.get('env_id', '')
        self.app_id = self.request.GET.get('app_id', '')
        self.ip = self.request.GET.get('ip', '')
        self.server_type = self.request.GET.get('server_type', '')
        self.server_id = self.request.GET.get('server_id', '')
        self.action = self.request.GET.get('action', '')
        self.line_num = self.request.GET.get('line_num', '100')

    def getLogDetail(self):
        # 判断前端传来的参数
        if self.project_id == '' or self.env_id == '' or self.app_id == '' or self.ip == ''\
                or self.action == ''or self.server_type == '' or self.server_id == '':
            # print('p_id,e_id,a_id,ip,action,server_type,server_id,',self.project_id,self.env_id,self.app_id,self.ip,self.action,self.server_type,self.server_id)
            print('invaild action args from web...')
            runlog.error("[ERROR] --wrong action args from web-----, Catch exception:, file: [ %s ], line: [ %s ]"
                        %(__file__,sys._getframe().f_lineno))
            return 'invaild action args from web...'

        else:
             #判断用户是否有权限，没有权限返回判断结果

            if not pub.hasAccessPermission(self.uid, self.server_type, self.server_id):
                return 'no permissions to view'
            # 获取app的用户名和密码
            instance = appConfigDetailClass.appConfigDetail()
            res, status = instance.AppConfigDetail(self.server_type, self.app_id, self.server_id, self.env_id, self.project_id)
            print('logapp--res',res)
            if not status:
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
                res_dic['sshuser'] = i[9]
            # 获取远程服务器日志目录指定行数的内容
            # print('dict_res',res_dic)
            if res_dic['app_type'] == '1': # app类型是tomcat
                if self.action == 'start':
                    log_file_path = '{}/logs/catalina.out'.format(res_dic['appdir'])
                # print('00---00',log_file_path)
                elif self.action == 'stop':
                    log_file_path = '/home/{}/service_manage/{}/scripts/log/stopapp.sh.log'.format(\
                        res_dic['sshuser'], res_dic['app_name'])
                elif self.action == 'log_show':
                    logdir_id = self.request.GET.get('logdir_id', '')
                    file_name = self.request.GET.get('file_name','')
                    print('nnnnnnnnnnnn',logdir_id,file_name)
                    if logdir_id == '' or file_name == '':
                        runlog.error("the logdir_id or filename is null, file: [ %s ], line: [ %s ]" % (
                            __file__, sys._getframe().f_lineno))
                        return 'invaild logdir_id to find the logfile'
                    # 找到app对应的日志目录
                    log_dir = instance.app_LogDir(self.app_id, self.server_type, self.server_id, logdir_id)
                    if len(log_dir) == 0:
                        runlog.error("the logdir is null, file: [ %s ], line: [ %s ]" % (
                            __file__, sys._getframe().f_lineno))
                        return 'invaild logdir to find the logfile'
                    log_file_path = '{}/{}'.format(log_dir[0][0],file_name)
                    print('logggggggg',log_file_path)
                else:
                    runlog.error("the APP type is not tomcat, file: [ %s ], line: [ %s ]" % (
                        __file__, sys._getframe().f_lineno))
                    return 'invaild action to find the logfile'
                pt = ParamikoTool()  # 实例化对象后，获取日志默认行数
                log_res = pt.getlogrow(self.ip, res_dic['sshport'], res_dic['sshuser'], \
                                       res_dic['pass'], log_file_path, self.line_num)
                # print('-------------',log_res)
                # 记录用户访问记录
                audit_log = Operation_dbModelClass()
                audit_log.inserToLog(self.request.user.username, self.ip, 'access', self.request.path, log_file_path)
                return log_res

            else:
                runlog.info("the APP type is not tomcat, file: [ %s ], line: [ %s ]" % (
                    __file__, sys._getframe().f_lineno))
                return 'just for app-type like tomcat..'

    def logDir(self):
        # 返回的字典格式
        data = {
            'project_id': self.project_id,
            'env_id': self.env_id,
            'app_id': self.app_id,
            'server_type': self.server_type,
            'server_id': self.server_id,
            'ip': self.ip,
        }
        if self.app_id == '':
            runlog.error("[ERROR] -getlogdir-wrong action args from web-----, Catch exception:, file: [ %s ], line: [ %s ]"
                        %(__file__,sys._getframe().f_lineno))
        if not pub.hasAccessPermission(self.uid, self.server_type, self.server_id):
            return ['no permissions to view']
        # 获取app的用户名和密码
        instance = appConfigDetailClass.appConfigDetail()
        res, status= instance.AppConfigDetail(self.server_type, self.app_id, self.server_id, self.env_id,
                                       self.project_id)
        print('logapp--res', res)
        if not status:
            runlog.error("the APP Data is null, file: [ %s ], line: [ %s ]" % (
                __file__, sys._getframe().f_lineno))
        data['user'] = res[0][1]
        res_dir = instance.whole_appLogDirs(self.app_id, self.server_type, self.server_id)   # 通过appid查找出对应的所有的日志目录
        print('whole_appLogDirs------>\033[42;1m%s\033[0m' % res_dir)
        if len(res_dir) == 0:
            print('nono is logdir...')
            return {}
        res_list = []
        for i in res_dir:
            res_dic = dict()
            res_dic['id'] = i[1]
            res_dic['dir'] = i[0]
            res_list.append(res_dic)
        data['logdirs'] = res_list
        return data

    def getlogInfo(self):  # 获取app日志目录下所有日志的详细信息，大小，拥有者，修改时间等
        logdir_id = self.request.GET.get('logdir_id', '')
        # 判断前端传来的参数
        if self.project_id == '' or self.env_id == '' or self.app_id == '' or self.ip == ''\
                or self.server_type == '' or self.server_id == '' or logdir_id == '':
            # print(self.project_id,self.env_id,self.app_id,self.ip,self.server_type,self.server_id,logdir_id)
            # print('getLogInfo-error-invaild action args from web...')
            runlog.error("[ERROR] -getLogInfo-error-wrong action args from web-----, Catch exception:, file: [ %s ], line: [ %s ]"
                        %(__file__,sys._getframe().f_lineno))
            return 'invaild action args from web...'
        if not pub.hasAccessPermission(self.uid, self.server_type, self.server_id):

            runlog.error("[ERROR] --no permission-----, Catch exception:, file: [ %s ], line: [ %s ]"
                        %(__file__,sys._getframe().f_lineno))
            return {}
        instance = appConfigDetailClass.appConfigDetail()
        res_dir = instance.app_LogDir(self.app_id, self.server_type, self.server_id, logdir_id)
        if len(res_dir) == 0:
            return {}

        # 获取app的用户名和密码
        instance = appConfigDetailClass.appConfigDetail()
        res, Status = instance.AppConfigDetail(self.server_type, self.app_id, self.server_id, self.env_id,
                                       self.project_id)
        #print('pppppppppppplogapp--res', res)
        if not Status:
            runlog.error("the APP Data is null, file: [ %s ], line: [ %s ]" % (
                __file__, sys._getframe().f_lineno))

        pk = ParamikoTool()  # 实例化对象，调用方法后将文件大小按时间排序展示
        data_res, status = pk.getDirInfo(self.ip, res[0][8], res[0][9], res[0][7], res_dir[0][0])
        # '''data='-rw-rw-r-- 1 beehive beehive  22900 Feb  8  2017 catalina.2017-02-08.log\n
        # -rw-rw-r-- 1 beehive beehive 171910 Feb  9  2017 catalina.2017-02-09.log\n
        #print('2222data_res------>\033[31;1m%s\033[0m' % data_res)
        if not status:
            runlog.error("getDirInfo is null, file: [ %s ], line: [ %s ],error:[ %s ]" % (
                __file__, sys._getframe().f_lineno, data_res))
        final_data_dic = dict()  # 将得到的结果按字典的格式返回
        final_data_dic['data'] = data_res
        return final_data_dic

