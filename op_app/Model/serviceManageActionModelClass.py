#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
from django.db import connections, connection
from op_app.Model.base.baseModelClass import BaseDbModelClass
from op_app.logger.log import dblog
from op_app.lib import pub
import json
import os

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
        config_status = self.ConfigFile(ip,app_name)

    def ConfigFile(self, ip, app_name):  # 构建配置文件
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_dir = current_dir + '/../../tasks/server_manage/' + ip + '/' + app_name + '/scripts'
        print('config_dir------>\033[44;1m%s\033[0m' % config_dir)
        # if not pub.createDir(config_dir):
        #     print('---mkdir error')
        #     return False
        # 将最新的start，stop脚本同步到config_dir



        # 写入配置文件
        #f = open(config_dir + '/conf/app_config.conf', 'w')






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