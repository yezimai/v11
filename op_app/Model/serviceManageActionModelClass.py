#!/usr/bin/python
# -*- coding: UTF-8 -*-

from op_app.Model.base.baseModelClass import BaseDbModelClass
from op_app.logger.log import dblog
from op_app.lib import pub
import json
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
                select p.name,de.install_user,e.type_app,de.app_dir,
                        de.pkgname,de.server_port,e.name
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
            select p.name,de.install_user,e.type_app,de.app_dir,
                    de.pkgname,de.server_port,e.name
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
            res_dic['projectname'] = i[0]
            res_dic['install_user'] = i[1]
            app_type = i[2]
            res_dic['appdir'] = i[3]
            res_dic['pkgname'] = i[4]
            res_dic['port'] = i[5]
            app_name = i[6]
        if app_type == '1':
            res_dic['apptype'] = 'tomcat'
        elif app_type == '2':
            res_dic['apptype'] = 'weblogic'
        else:
            print('invalid AppType..')
            return False
        config_status = self.ConfigFile(ip, app_name, res_dic)
        if config_status:  # 配置文件构建成功
            pass

    def ConfigFile(self, ip, app_name, r_dic):  # 构建配置文件
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_dir = '{}{}{}{}{}{}'.format(current_dir, '/../../tasks/server_manage/', ip, '/',  app_name, '/scripts')
        print('config_dir------>\033[44;1m%s\033[0m' % config_dir)
        if not os.path.exists(config_dir):
            try:
                os.makedirs(config_dir)
            except Exception as e:
                print('---mkdir error')
                dblog.error("[ERROR] mkdirs error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (
                    e, __file__, sys._getframe().f_lineno))
                return False
        # 将最新的start，stop脚本同步到config_dir

        source_dir = '{}{}'.format(current_dir, '/../../scripts/client/service_manage/bin')

        try:
            for file in os.listdir(source_dir): # 获取目标文件夹的文件列表信息
                #print(os.listdir(source_dir))
                source_file = os.path.join(source_dir,file)
                target_file = os.path.join(config_dir,file)

                if os.path.isfile(source_file): # 判断是否为文件，真则写入到目标文件中
                    open(target_file, "wb").write(open(source_file, "rb").read())
                else:
                    dblog.error("[ERROR] File--type error, Catch exception:, file: [ %s ], line: [ %s ]" % (
                         __file__, sys._getframe().f_lineno))
                    return False
        except IOError as e:
            print('Unable to copy file.%s' % e)
            return False
        except:
            print('Unexected error:', sys.exc_info())
            return False

        # 写入配置文件
        conf_file = '{}{}'.format(config_dir,'/conf')
        print('0-0,',r_dic)
        if not os.path.exists(conf_file):
            os.makedirs(conf_file)
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
            f.write('appwarname[1]={0}'.format(r_dic['pkgname']) + '\n')
            f.write('startuptime[1]=1000' + '\n')
            f.write('port[1]={0}'.format(r_dic['port']) + '\n')
        except Exception as e:
            dblog.error("[ERROR] write to config file error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (
                e, __file__, sys._getframe().f_lineno))
            return False

        return True





        # print('res------>\033[32;1m%s\033[0m' % res)





        # for j in self.data:
        #     code = j['code']
        #     print '2222222',code
        #     sql = '''select DISTINCT d.id,d.navname,d.url from auth_user a,op_app_group_user ab,op_app_group b,
        #                               op_app_group_permission bc,op_app_permission c,op_app_nav d ,
        #                               op_app_permission_nav cd
        #               where a.id=%s and a.id=ab.user_id and ab.group_id=b.id and b.id=bc.group_id
        #                     and bc.permission_id=c.id and c.id=cd.permission_id and cd.nav_id=d.id
        #                     and d.pid = (select dd.id from op_app_nav dd where dd.code=%s)'''
        #     try:
        #         res = self._cursorQuery(sql, [id, code])
        #         print 'navinfo!!!!!',res
        #         if len(res) < 0:
        #             dblog.error('navinfo is None , file: [ %s ], line: [ %s ]' % (__file__, sys._getframe().f_lineno))
        #             return []
        #     except Exception as e:
        #         dblog.error("[ERROR] Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (
        #             e, __file__, sys._getframe().f_lineno))
        #         return []
        #     else:
        #         r_list = []
        #         for i in range(len(res)):
        #
        #             dic = dict()
        #             dic['id']=res[i][0]
        #             dic['text'] = res[i][1]
        #             dic['url'] = res[i][2]
        #             r_list.append(dic)
        #             j['children']=r_list
        #         print('<------>\033[32;1m%s\033[0m' %r_list)
        #
        # # dblog.info("nav_data last: %s,file: [ %s ], line: [ %s ]" % (
        # #     json.dumps(self.data, indent=4), __file__, sys._getframe().f_lineno))
        # #print('navinfo------>\033[32;1m%s\033[0m' %self.data)
        # return self.data
# if __name__ == '__main__':
#     m_db = DbBaseModelClass()
#     sql = 'select * from book_info limit 1'
#     ret = m_db._cursorQuery(sql, [])
#     print('ret:', ret)