#!/usr/bin/env python
# -*- coding: utf-8 -*-
from op_app.logger.log import runlog
import os
from op_app.lib import appConfigDetailClass
from op_app.lib.pub import *
from op_app.Model.base.operation_dbModelClass import Operation_dbModelClass


class DownloadLogControllerClass(object):
    def __init__(self, request):
        self.request = request
        self.uid = self.request.user.id
        self.project_id = self.request.GET.get('project_id', '')
        self.env_id = self.request.GET.get('env_id', '')
        self.app_id = self.request.GET.get('app_id', '')
        self.ip = self.request.GET.get('ip', '')
        self.server_type = self.request.GET.get('server_type', '')
        self.server_id = self.request.GET.get('server_id', '')
        self.action = self.request.GET.get('action', '')
        self.logdir_id = self.request.GET.get('logdir_id','')
        self.logfilename = self.request.GET.get('file_name','')
        # if not self.judge_args():
        #     runlog.error("[ERROR] --invalid args for downloading -----, Catch exception:, file: [ %s ], line: [ %s ]"
        #                  % (__file__, sys._getframe().f_lineno))

    def judge_args(self):
        if self.uid == '' or self.logdir_id == '' or self.logfilename == '' or self.server_type == '' \
                or self.server_id == '' or self.app_id == '' or self.env_id == '' or self.project_id == '':
            print('judge,,,,', self.logdir_id, self.logfilename)
            return False
        return True

    def download(self): #
        if not self.judge_args():
            runlog.error("[ERROR] --invalid args for downloading -----, Catch exception:, file: [ %s ], line: [ %s ]"
                         % (__file__, sys._getframe().f_lineno))
            return 'invalid args from web....'

        # 验证是否有权限
        # user_permits = permissionModelClass.PermissionModelClass(self.uid)
        if not hasAccessPermission(self.uid, self.server_type, self.server_id):
            # print('no permission')
            runlog.error("--no permission to access the logfile from web-----, Catch exception:, file: [ %s ], line: [ %s ]"
                        %(__file__,sys._getframe().f_lineno))
            return False
        rsync_file = os.path.dirname(os.path.abspath(__file__)) + '/../../scripts' + '/server/bin/execRsync.exp'  # rsync 脚本
        cmd1 = [['chmod', '+x', rsync_file]]  # 增加执行权限
        # i_calss = appLogDirModelClass.appLogModelClass(self.request)
        # dirname = i_calss.app_LogDir()


        # 获取app的用户名和密码
        instance = appConfigDetailClass.appConfigDetail()
        dirname = instance.app_LogDir(self.app_id, self.server_type, self.server_id, self.logdir_id) # 获取app的日志目录
        if len(dirname) == 0:
            runlog.error("the APP dirname is null, file: [ %s ], line: [ %s ]" % (
                __file__, sys._getframe().f_lineno))
            return 'no found the logdir'
        logfile = dirname[0][0] + os.sep + self.logfilename  # 得到app的日志的绝对路径
        res, status = instance.AppConfigDetail(self.server_type, self.app_id, self.server_id, self.env_id,
                                       self.project_id)
        print('logapp-1-res', res, logfile)
        if not status:
            runlog.error("the APP Data is null, file: [ %s ], line: [ %s ]" % (
                __file__, sys._getframe().f_lineno))
        connectmessage = {'ip': self.ip,
                          'port': res[0][8],
                          'user': res[0][9],
                          'password': res[0][7],
                          'remote_file': logfile,
                          'local_dir': os.path.dirname(os.path.abspath(__file__)) + '/../static/log/'
                          }
        # print cmd1
        if execShellCommand(*cmd1) != True:
            runlog.error("exec permission shell error, file: [ %s ], line: [ %s ]" % (
                __file__, sys._getframe().f_lineno))
            return 'exec permission shell error'
            # return JsonResponse('exec command failed!', safe=False)

        connect_lst = [connectmessage['ip'], connectmessage['user'], connectmessage['port'], connectmessage['password'],
                       connectmessage['remote_file'], connectmessage['local_dir']]
        filename = connectmessage['local_dir'] + connectmessage['ip'] + logfile.replace(os.sep, '-')

        retstr = '/static/log/' + connectmessage['ip'] + logfile.replace(os.sep, '-')

        if rsyncRemoteFileToLocal(rsync_file, *connect_lst) != True:
            runlog.error("rsyncRemoteFileToLocal error, file: [ %s ], line: [ %s ]" % (
                __file__, sys._getframe().f_lineno))
            return 'rsyncRemoteFileToLocal error'
        else:

            os.chdir(connectmessage['local_dir'])   # 切换到服务器上存放的日志目录路径下，将下载的文件加上ip后，重命名
            # print filename, self.logfilename
            os.system('mv  ' + self.logfilename + '  ' + filename)
            # 记录用户访问记录
            audit_log = Operation_dbModelClass()
            audit_log.inserToLog(self.request.user.username, self.ip, self.action, self.request.path,
                                 '{}'.format(filename))
            return retstr  # 路径可以根据自己定义
