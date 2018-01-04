#!/usr/bin/python
# -*- coding: UTF-8 -*-

from op_app.Model.base.baseModelClass import BaseDbModelClass
from op_app.logger.log import dblog
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

    def Action(self):
        project_id = self.request.POST.get('project_id', '')
        env_id = self.request.POST.get('env_id', '')
        app_id = self.request.POST.get('app_id', '')
        ip = self.request.POST.get('ip', '')
        print('ip!!!!!!!!!!!!!!!!',ip)
        server_type = self.request.POST.get('server_type', '')
        server_id = self.request.POST.get('server_id', '')
        action = self.request.POST.get('action', '')
        #print('mmmm',project_id,env_id,app_id,ip,server_id,server_type,action)
        if project_id == '' or env_id == '' or app_id == '' or ip == '' or action == ''\
                or server_type == '' or server_id == '':
            print('wrong action args from web...')
            return False
        # 根据项目、环境、应用、ip对对应的部署在此机器上的应用信息
        if server_type == '2':
            sql = '''
                select p.code,de.install_user,
                        e.type_app,de.app_dir,
                        de.pkgname,de.server_port,e.name,
                        de.install_pass,de.ssh_port
                from cmdb_server_app de, -- 服务器-app中间表	
                      cmdb_env_server hd, 	-- 服务器-环境中间表
                      cmdb_env h,					-- 环境表
                      cmdb_project p,		  -- 项目表	
                      cmdb_app e					-- app表
                where de.app_id = %s and de.app_id=e.id and de.virtual_server_id = %s 
                      and hd.virtual_server_id=de.virtual_server_id 
                      and h.env_type=%s and h.id=hd.env_id and p.id=%s 
            '''
        elif server_type == '1':
            sql = '''
            select p.code,de.install_user,
                    e.type_app,de.app_dir,
                    de.pkgname,de.server_port,e.name,
                    de.install_pass,de.ssh_port
                from cmdb_server_app de, -- 服务器-app中间表	
                      cmdb_env_server hd, 	-- 服务器-环境中间表
                      cmdb_env h,					-- 环境表
                      cmdb_project p,		  -- 项目表	
                      cmdb_app e					-- app表
                where de.app_id = %s and de.app_id=e.id and de.physical_server_id = %s 
                      and hd.physical_server_id=de.physical_server_id 
                      and h.env_type=%s and h.id=hd.env_id and p.id=%s 
            '''
        else:
            print('--wrong-server_type---->\033[42;1m\033[0m')
        try:
            res = self._cursorQuery(sql, [app_id, server_id, env_id, project_id])
            print('nnnnn',res)
        except Exception as e:
            dblog.error("[ERROR] Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ],sql:[%s]" % (
                e, __file__, sys._getframe().f_lineno, sql))
            return False
        if len(res) == 0:
            print('*****wrong action args....')
        res_dic = dict()    # 字典存储结果
        for i in res:
            res_dic['projectcode'] = i[0]
            res_dic['install_user'] = i[1]
            app_type = i[2]
            res_dic['appdir'] = i[3]
            res_dic['pkgname'] = i[4]
            res_dic['port'] = i[5]
            app_name = i[6]
            res_dic['pass'] = i[7]
            res_dic['sshport'] = i[8]
        if app_type == '1':
            res_dic['apptype'] = 'tomcat'
        elif app_type == '2':
            res_dic['apptype'] = 'weblogic'
        else:
            print('invalid AppType..')
            return False
        print('123123123',res_dic)
        config_status = self.ConfigFile(ip, app_name, **res_dic)
        if config_status:  # 配置文件构建成功

            if self.rsyncFile(ip,**res_dic) :   #同步文件到远程机器
                print('rsync-succ----->\033[31;1m\033[0m')

    def ConfigFile(self, ip, app_name, **r_dic):  # 构建配置文件
        print('ip!!!-----!!!!!!', ip)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_dir = '{}{}{}{}{}{}'.format(current_dir, '/../../tasks/service_manage/', ip, '/',  app_name, '/scripts')
        self.app_path = '{}{}{}/{}'.format(current_dir, '/../../tasks/service_manage/', ip,app_name)
        print('config_dir------>\033[44;1m%s\033[0m' % config_dir)
        self.rsyncScriptPath = '{}{}'.format(current_dir,'/../../scripts/server/bin/execRsync.exp')
        if not os.path.exists(config_dir):
            try:
                for i in ['/bin','/conf']:
                    os.makedirs(config_dir+i)
            except Exception as e:
                print('---mkdir error')
                dblog.error("[ERROR] mkdirs error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (
                    e, __file__, sys._getframe().f_lineno))
                return False
        # 将最新source_dir下的start，stop脚本复制到config_dir
        source_dir = '{}{}'.format(current_dir, '/../../scripts/client/service_manage/bin')

        try:
            for file in os.listdir(source_dir): # 获取目标文件夹的文件列表信息
                #print(os.listdir(source_dir))
                source_file = os.path.join(source_dir,file)
                target_file = '{}{}{}'.format(config_dir,'/bin/',file)

                if os.path.isfile(source_file): # 判断是否为文件，真则写入到目标文件中
                    open(target_file, "wb").write(open(source_file, "rb").read())
                else:
                    dblog.error("[ERROR] File--type error, Catch exception:, file: [ %s ], line: [ %s ]" % (
                         __file__, sys._getframe().f_lineno))
                    return False
            print('6666,copy files to tasks is ready....')
        except IOError as e:
            print('Unable to copy file.%s' % e)
            return False
        except:
            print('Unexected error:', sys.exc_info())
            return False

        # 写入配置文件
        conf_file = '{}{}'.format(config_dir,'/conf')
        print('0-0,',r_dic)
        # if not os.path.exists(conf_file):
        #     os.makedirs(conf_file)
        try:
            f = open(conf_file+'/app_config.conf','w')
            #f.write('pkgfile={0}'.format(REMOTE_BASE_DIR + dir_name + '/' + appname + '/pkg/' + dic['pkgname']) + '\n')
            f.write('appnumber={0}'.format('1')+'\n')
            f.write('projectname={0}'.format(r_dic['projectname']) + '\n')
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
            dblog.error("[ERROR] write to config file error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (
                e, __file__, sys._getframe().f_lineno))
            return False
        f.close()
        return True

        # print('res------>\033[32;1m%s\033[0m' % res)



    def rsyncFile(self, ip, **r_dic):
        # 首先判断远程目录是否存在
        username = r_dic['install_user']
        dest_dir = '${HOME}/service_manage/'
        sshport = r_dic['sshport']
        password = r_dic['pass']
        pt = ParamikoTool()
        status = pt.remoteHostHasDir(ip, username, sshport, password, dest_dir)
        # print 'remote_dirremote_dir,'
        if not status:
            return False
        #利用rsync脚本将配置文件和启动脚本推送过去
        remote_dir = '{}/{}/{}/'.format('/home',username,'service_manage')
        connect_args = [ip, username, sshport, password, self.app_path, remote_dir]
        if pub.rsyncServerToClients(self.rsyncScriptPath,*connect_args) != True:
            print('rsync-error----->\033[42;1m\033[0m')
            dblog.error("[ERROR] rsync file to client error, Catch exception:, file: [ %s ], line: [ %s ]" % (
                __file__, sys._getframe().f_lineno))
            return False
        else:
            return True




# if __name__ == '__main__':
#     m_db = DbBaseModelClass()
#     sql = 'select * from book_info limit 1'
#     ret = m_db._cursorQuery(sql, [])
#     print('ret:', ret)