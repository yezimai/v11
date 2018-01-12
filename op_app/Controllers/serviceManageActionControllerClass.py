#!/usr/bin/env python
# -*- coding: utf-8 -*-

from op_app.logger.log import runlog
from op_app.lib import pub,appConfigDetailClass
from op_app.Extends import paramikoTool
import sys, os
from op_app.Model.base.operation_dbModelClass import Operation_dbModelClass


class ManageActionControllerClass(object):
    def __init__(self, request):
        self.request = request
        self.project_id = self.request.POST.get('project_id', '')
        self.env_id = self.request.POST.get('env_id', '')
        self.app_id = self.request.POST.get('app_id', '')
        self.ip = self.request.POST.get('ip', '')
        self.server_type = self.request.POST.get('server_type', '')
        self.server_id = self.request.POST.get('server_id', '')
        self.action = self.request.POST.get('action', '')
        self.pt = paramikoTool.ParamikoTool()

    def getAction(self):
        if self.project_id == '' or self.env_id == '' or self.app_id == '' or self.ip == ''\
                or self.action == ''or self.server_type == '' or self.server_id == '':
            print('invaild action args from web...')
            runlog.error("[ERROR] --wrong action args from web-----, Catch exception:, file: [ %s ], line: [ %s ]"
                        %(__file__,sys._getframe().f_lineno))
            return False
        #  根据项目、环境、应用、ip对对应的部署在此机器上的应用信息
        instance = appConfigDetailClass.appConfigDetail()
        res, res_status = instance.AppConfigDetail(self.server_type, self.app_id, self.server_id,\
                                        self.env_id, self.project_id)
        if not res_status:
            runlog.error("the APP Data is null, file: [ %s ], line: [ %s ]" % (
                            __file__, sys._getframe().f_lineno))
            return False
        res_dic = dict()    # 字典存储结果
        for i in res:
            res_dic['projectcode'] = i[0]
            res_dic['install_user'] = i[1]
            app_type = i[2]
            res_dic['appdir'] = i[3]
            res_dic['pkgname'] = i[4]
            res_dic['port'] = i[5]
            res_dic['app_name'] = i[6]
            res_dic['pass'] = i[7]
            res_dic['sshport'] = i[8]
            res_dic['sshuser'] = i[9]
        if app_type == '1':
            res_dic['apptype'] = 'tomcat'
        elif app_type == '2':
            res_dic['apptype'] = 'weblogic'
        else:
            # print('invalid AppType..')
            runlog.error("[ERROR]--invalid AppType-----, Catch exception:, file: [ %s ], line: [ %s ]"
                        %(__file__,sys._getframe().f_lineno))
            return False
        # print('123123123',res_dic)
        config_status = self.ConfigFile(self.ip, **res_dic)
        if config_status:  # 配置文件构建成功
            if self.rsyncFile(self.ip,**res_dic) :   # 同步文件到远程机器
                # print('rsync-succ----->\033[31;1m\033[0m')
                runlog.info("---rsync-file to remote-success----:file: [ %s ], line: [ %s ]" % (
                    __file__, sys._getframe().f_lineno))
                exec_dir = '{}/{}/{}'.format(self.remote_dir, res_dic['app_name'], 'scripts/bin/')  # 远程执行的目录
                # 在bqadm家目录权限设为777
                # mkdir_cmd = "chmod 777 -R {}".format(remote_home)
                # mkdir_res = self.pt.execCommand(ip, username, sshport, password, mkdir_cmd)
                if self.action == 'start':  # 判断执行动作

                    # cmd = 'cd {}&&chmod a+x *.sh&&nohup ./startapp.sh 1>/dev/null 2>&1 &&sleep 10&&ps -ef|grep {}|grep {}|grep -v grep|wc -l' \
                    #     .format(exec_dir, res_dic['appdir'], res_dic['install_user'])
                    cmd = 'chmod 777 -R {};sudo su - {} -c "cd {}&&nohup ./startapp.sh 1>/dev/null 2>&1"'\
                            .format(self.remote_dir, res_dic['install_user'], exec_dir)
                elif self.action == 'stop':
                    cmd = 'chmod 777 -R {};sudo su - {} -c "cd {}&&./stopapp.sh 1>/dev/null 2>&1"'\
                            .format(self.remote_dir, res_dic['install_user'], exec_dir)
                else:  # action参数无效时
                    runlog.error("[ERROR] --invaild-action------, Catch exception:, file: [ %s ], line: [ %s ]"
                                % (__file__,sys._getframe().f_lineno))
                    return False
                # 记录用户访问记录
                audit_log = Operation_dbModelClass()
                audit_log.inserToLog(self.request.user.username, self.ip, self.action, self.request.path, '{}'.format(res_dic['app_name']))
                return self.runScript(self.ip, cmd, **res_dic)  # 返回执行脚本后的结果 true or false
            else:  # 同步文件失败
                # print('rsync-fail----->\033[31;1m\033[0m')
                runlog.error("[ERROR] --rsync-config-file-failed------, Catch exception:, file: [ %s ], line: [ %s ]"
                            % (__file__, sys._getframe().f_lineno))
                return False
        else:  # 创建配置文件失败
            # print('configFile create error..123')
            runlog.error("[ERROR] --configFile-create-failed------, Catch exception:, file: [ %s ], line: [ %s ]"
                        % (__file__, sys._getframe().f_lineno))
            return False


    def ConfigFile(self, ip, **r_dic):  # 构建配置文件
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_dir = '{}{}{}{}{}{}'.format(current_dir, '/../../tasks/service_manage/', ip, '/',  r_dic['app_name'], '/scripts')
        self.app_path = '{}{}{}/{}'.format(current_dir, '/../../tasks/service_manage/', ip, r_dic['app_name'])
        self.rsyncScriptPath = '{}{}'.format(current_dir, '/../../scripts/server/bin/execRsync.exp')
        if not os.path.exists(config_dir):
            try:
                for i in ['/bin', '/conf']:
                    os.makedirs(config_dir+i)
            except Exception as e:
                runlog.error("[ERROR] mkdirs error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (
                    e, __file__, sys._getframe().f_lineno))
                return False
        # 将最新source_dir下的start，stop脚本复制到config_dir
        source_dir = '{}{}'.format(current_dir, '/../../scripts/client/service_manage/bin')

        try:
            for file in os.listdir(source_dir):  # 获取目标文件夹的文件列表信息
                source_file = os.path.join(source_dir, file)
                target_file = '{}{}{}'.format(config_dir, '/bin/', file)
                if os.path.isfile(source_file):  # 判断是否为文件，真则写入到目标文件中
                    with open(target_file, "wb") as t_f:
                        t_f.write(open(source_file, "rb").read())
                else:
                    runlog.error("[ERROR] File--type error, Catch exception:, file: [ %s ], line: [ %s ]" % (
                         __file__, sys._getframe().f_lineno))
                    return False
            print('6666,copy files to tasks is ready....')
        except Exception as e:
            runlog.error("Unexected error: [ %s ], file: [ %s ], line: [ %s ]" % (
                    e, __file__, sys._getframe().f_lineno))
            return False

        # 写入配置文件
        conf_file = '{}{}'.format(config_dir, '/conf')
        try:
            with open(conf_file + '/app_config.conf', 'w') as f:
                # f = open(conf_file+'/app_config.conf','w')
                #f.write('pkgfile={0}'.format(REMOTE_BASE_DIR + dir_name + '/' + appname + '/pkg/' + dic['pkgname']) + '\n')
                f.write('appnumber={0}'.format('1')+'\n')
                f.write('projectcode={0}'.format(r_dic['projectcode']) + '\n')
                f.write('ip={0}'.format(ip) + '\n')
                # f.write('projectname=%s'%r_dic['projectname'] + '\n')
                f.write('user[1]={0}'.format(r_dic['install_user']) + '\n')
                f.write('upgradetype[1]=full' + '\n')
                f.write('apptype[1]={0}'.format(r_dic['apptype']) + '\n')
                #f.write('backupdir[1]={0}'.format(REMOTE_BASE_DIR + dir_name + '/' + appname + '/backup') + '\n')
                f.write('appdir[1]={0}'.format(r_dic['appdir']) + '\n')
                f.write('appwarname={0}'.format(r_dic['pkgname']) + '\n')
                f.write('startuptime[1]=1000' + '\n')
                f.write('port[1]={0}'.format(r_dic['port']) + '\n')
        except Exception as e:
            runlog.error("Write to config file error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (
                            e, __file__, sys._getframe().f_lineno))
            return False
        return True

    def rsyncFile(self, ip, **r_dic):
        username, sshport, password = r_dic['sshuser'], r_dic['sshport'], r_dic['pass']
        # 利用rsync脚本将配置文件和启动脚本推送过去,rsync可以自动创建文件夹，所以注释掉上面的代码

        # self.remote_dir = '{}/{}/{}/'.format('/home', username, 'service_manage')
        chmod_cmd = [['chmod', '+x', self.rsyncScriptPath]]
        if pub.execShellCommand(*chmod_cmd) == False:
            runlog.error("Exec chmod_cmd command error, file: [ %s ], line: [ %s ]" % (
                            __file__, sys._getframe().f_lineno))
            return False
        # 寻找服务器的家目录的命令
        remote_home_dir_cmd = [["grep", "^{}:".format(username), "/etc/passwd|awk -F ':' '{print $6}'"]]
        output_lst = self.pt.execCommandInRemoteHostOutput(self.ip, username, sshport, password, *remote_home_dir_cmd)
        print('oooouuutttpputt------>\033[42;1m%s\033[0m' %output_lst)
        if output_lst[0][0] != 0:
            return False
        remote_home = output_lst[0][1][:-1]  #remot_home = /home/bqadm
        print('rrrrrrr_home',remote_home)

        # print('remote_home_dir_cmd',remote_home_dir_cmd,type(remote_home_dir_cmd),len(remote_home_dir_cmd))
        # /home/bqadm

        self.remote_dir = '{}/service_manage'.format(remote_home)
        connect_args = [ip, username, sshport, password, self.app_path, self.remote_dir]
        if pub.rsyncServerToClients(self.rsyncScriptPath, *connect_args) != True:
            runlog.error("[ERROR] rsync file to client error, Catch exception:, file: [ %s ], line: [ %s ]" % (
                __file__, sys._getframe().f_lineno))
            return False
        return True

    def runScript(self, ip, cmd, **r_dic):
        username, sshport, password = r_dic['sshuser'], r_dic['sshport'], r_dic['pass']

        status = self.pt.execCommand(ip, username, sshport, password, cmd)
        if status:
            runlog.info("--script execute-success--:file: [ %s ], line: [ %s ]" % (
                __file__, sys._getframe().f_lineno))
            return True
        else:
            runlog.error("[ERROR] --run cmd-fail------, Catch exception:, file: [ %s ], line: [ %s ]" % (
                  __file__,sys._getframe().f_lineno))
            return False





