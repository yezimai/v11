#!/usr/bin/python
# -*- coding: UTF-8 -*-

from op_app.Model.base.baseModelClass import BaseDbModelClass
from op_app.logger.log import dblog, runlog
from op_app.lib import pub
import json
from op_app.Extends.paramikoTool import ParamikoTool
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ManageActionModelClass(BaseDbModelClass):

    def __init__(self, request):
        super(ManageActionModelClass, self).__init__()
        self.request = request
        self.project_id = self.request.POST.get('project_id', '')
        self.env_id = self.request.POST.get('env_id', '')
        self.app_id = self.request.POST.get('app_id', '')
        self.ip = self.request.POST.get('ip', '')
        self.server_type = self.request.POST.get('server_type', '')
        self.server_id = self.request.POST.get('server_id', '')
        self.action = self.request.POST.get('action', '')


    def Action(self):
        if self.project_id == '' or self.env_id == '' or self.app_id == '' or self.ip == ''\
                or self.action == ''or self.server_type == '' or self.server_id == '':
            print('invaild action args from web...')
            dblog.error("[ERROR] --wrong action args from web-----, Catch exception:, file: [ %s ], line: [ %s ]"
                        %(__file__,sys._getframe().f_lineno))
            return False
        res = pub.AppConfigDetail.AppConfigDetail(self.server_type, self.app_id, self.server_id,\
                                                  self.env_id, self.project_id)

        # # 根据项目、环境、应用、ip对对应的部署在此机器上的应用信息
        # if self.server_type == '2':
        #     sql = '''
        #         select p.code,de.install_user,
        #                 e.type_app,de.app_dir,
        #                 de.pkgname,de.server_port,e.name,
        #                 de.install_pass,de.ssh_port
        #         from cmdb_server_app de, -- 服务器-app中间表
        #               cmdb_env_server hd, 	-- 服务器-环境中间表
        #               cmdb_env h,					-- 环境表
        #               cmdb_project p,		  -- 项目表
        #               cmdb_app e					-- app表
        #         where de.app_id = %s and de.app_id=e.id and de.virtual_server_id = %s
        #               and hd.virtual_server_id=de.virtual_server_id
        #               and h.env_type=%s and h.id=hd.env_id and p.id=%s
        #     '''
        # elif self.server_type == '1':
        #     sql = '''
        #     select p.code,de.install_user,
        #             e.type_app,de.app_dir,
        #             de.pkgname,de.server_port,e.name,
        #             de.install_pass,de.ssh_port
        #         from cmdb_server_app de,    -- 服务器-app中间表
        #               cmdb_env_server hd, 	-- 服务器-环境中间表
        #               cmdb_env h,					-- 环境表
        #               cmdb_project p,		  -- 项目表
        #               cmdb_app e					-- app表
        #         where de.app_id = %s and de.app_id=e.id and de.physical_server_id = %s
        #               and hd.physical_server_id=de.physical_server_id
        #               and h.env_type=%s and h.id=hd.env_id and p.id=%s
        #     '''
        # else:
        #     # print('--wrong-server_type---->\033[42;1m\033[0m')
        #     dblog.error("[ERROR] --invalid-server_type-----, Catch exception:, file: [ %s ], line: [ %s ]"
        #                 %(__file__,sys._getframe().f_lineno))
        # try:
        #     res = self._cursorQuery(sql, [self.app_id, self.server_id, self.env_id, self.project_id])
        # except Exception as e:
        #     dblog.error("[ERROR] Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ],sql:[%s]" % (
        #         e, __file__, sys._getframe().f_lineno, sql))
        #     return False
        # if len(res) == 0:
        #     # print('*****wrong action args....')
        #     dblog.error("[ERROR]--invalid-action args-----, Catch exception:, file: [ %s ], line: [ %s ]"
        #                 %(__file__,sys._getframe().f_lineno))
        #res = self.AppConfigDetail(self.server_type,)
        if not res:
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
        if app_type == '1':
            res_dic['apptype'] = 'tomcat'
        elif app_type == '2':
            res_dic['apptype'] = 'weblogic'
        else:
            # print('invalid AppType..')
            dblog.error("[ERROR]--invalid AppType-----, Catch exception:, file: [ %s ], line: [ %s ]"
                        %(__file__,sys._getframe().f_lineno))
            return False
        # print('123123123',res_dic)
        config_status = self.ConfigFile(self.ip, **res_dic)
        if config_status:  # 配置文件构建成功
            if self.rsyncFile(self.ip,**res_dic) :   # 同步文件到远程机器
                # print('rsync-succ----->\033[31;1m\033[0m')
                dblog.info("---rsync-file to remote-success----:file: [ %s ], line: [ %s ]" % (
                    __file__, sys._getframe().f_lineno))
                exec_dir = '{}{}/{}'.format(self.remote_dir, res_dic['app_name'], 'scripts/bin/')  # 远程执行的目录
                if self.action == 'start':  # 判断执行动作
                    # cmd = 'cd {}&&chmod a+x *.sh&&nohup ./startapp.sh 1>/dev/null 2>&1 &&sleep 10&&ps -ef|grep {}|grep {}|grep -v grep|wc -l' \
                    #     .format(exec_dir, res_dic['appdir'], res_dic['install_user'])
                    cmd = 'cd {}&&chmod a+x *.sh&&nohup ./startapp.sh 1>/dev/null 2>&1'.format(exec_dir)
                elif self.action == 'stop':
                    cmd = 'cd {}&&chmod a+x *.sh&&nohup ./stopapp.sh 1>/dev/null 2>&1'.format(exec_dir)
                else:  # action参数无效时
                    dblog.error("[ERROR] --invaild-action------, Catch exception:, file: [ %s ], line: [ %s ]"
                                % (__file__,sys._getframe().f_lineno))
                    return False
                return self.runScript(self.ip, cmd, **res_dic) # 返回执行脚本后的结果 true or false
            else:  # 同步文件失败
                # print('rsync-fail----->\033[31;1m\033[0m')
                dblog.error("[ERROR] --rsync-config-file-failed------, Catch exception:, file: [ %s ], line: [ %s ]"
                            % (__file__, sys._getframe().f_lineno))
                return False
        else:  # 创建配置文件失败
            # print('configFile create error..123')
            dblog.error("[ERROR] --configFile-create-failed------, Catch exception:, file: [ %s ], line: [ %s ]"
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
                dblog.error("[ERROR] mkdirs error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (
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
                    dblog.error("[ERROR] File--type error, Catch exception:, file: [ %s ], line: [ %s ]" % (
                         __file__, sys._getframe().f_lineno))
                    return False
            print('6666,copy files to tasks is ready....')
        except Exception as e:
            dblog.error("Unexected error: [ %s ], file: [ %s ], line: [ %s ]" % (
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
            dblog.error("Write to config file error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (
                            e, __file__, sys._getframe().f_lineno))
            return False
        return True

    def rsyncFile(self, ip, **r_dic):
        username, sshport, password = r_dic['install_user'], r_dic['sshport'], r_dic['pass']
        # 利用rsync脚本将配置文件和启动脚本推送过去,rsync可以自动创建文件夹，所以注释掉上面的代码
        self.remote_dir = '{}/{}/{}/'.format('/home', username, 'service_manage')
        connect_args = [ip, username, sshport, password, self.app_path, self.remote_dir]
        chmod_cmd = [['chmod', '+x', self.rsyncScriptPath]]
        if pub.execShellCommand(*chmod_cmd) == False:
            runlog.error("Exec chmod_cmd command error, file: [ %s ], line: [ %s ]" % (
                            __file__, sys._getframe().f_lineno))
            return False
        if pub.rsyncServerToClients(self.rsyncScriptPath, *connect_args) != True:
            dblog.error("[ERROR] rsync file to client error, Catch exception:, file: [ %s ], line: [ %s ]" % (
                __file__, sys._getframe().f_lineno))
            return False
        return True

    def runScript(self, ip, cmd, **r_dic):
        username, sshport, password = r_dic['install_user'], r_dic['sshport'], r_dic['pass']
        pt = ParamikoTool()
        status = pt.execCommand(ip, username, sshport, password, cmd)
        if status == 'true':
            dblog.info("--script execute-success--:file: [ %s ], line: [ %s ]" % (
                __file__, sys._getframe().f_lineno))
            return True
        else:
            dblog.error("[ERROR] --run cmd-fail------, Catch exception:, file: [ %s ], line: [ %s ]" % (
                  __file__,sys._getframe().f_lineno))
            return False



