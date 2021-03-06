#!/usr/bin/python
# -*- coding: UTF-8 -*-


from op_app.Model.base.baseModelClass import BaseDbModelClass
from op_app.logger.log import dblog
import sys
import json

class GetProjectDetailModelClass(BaseDbModelClass):

    def __init__(self,nav_id,user_id):
        super(GetProjectDetailModelClass,self).__init__()
        self.nav_id = nav_id
        self.user_id = user_id

    def getProjectInfo(self):
        '''#
        :return:返回的格式是一个字典
        '''
        # 先查找出所在服务器的类型，虚拟机or物理机

        sql = '''select DISTINCT de.server_type 
                    from cmdb_project p, -- 项目表	
                                cmdb_app e , 	-- APP表
                                cmdb_server_app de  -- 服务器-app-中间表
                    where e.project_id= p.id and e.id=de.app_id 
                    and p.code=
                                (select aa.code from op_app_nav aa 
                                where aa.id=
                                            (SELECT a.pid from op_app_nav a where a.id=%s))'''
        try:
            server_type = self._cursorQuery(sql,[self.nav_id])
            print '!!!!!server_type :', server_type
        except Exception as e:
            dblog.error("[ERROR] Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (
                e, __file__, sys._getframe().f_lineno))
        if len(server_type) == 0 :
            print('wrong server_type11')
            return ''
        res1=()
        res2=()
        for i in server_type:
            env_list = []
            app_list = []

            if int(i[0]) == 2: #虚拟机
                sql = '''
                select DISTINCT p.name,p.`code`,p.id as project_id,h.id as env_id,
                      e.id as app_id,e.`name`,h.env_type
                from cmdb_project p, -- 项目表	
                    cmdb_app e , 	-- APP表
                    cmdb_server_app de , -- 服务器-app-中间表
                    cmdb_virtual_server d, -- 虚拟机
                    cmdb_env h,	-- 环境表
                    cmdb_env_server hd -- 环境-服务器-中间表
                where e.project_id= p.id and e.id=de.app_id 
                    and d.id=de.virtual_server_id and d.id=hd.virtual_server_id and hd.env_id=h.id
                    and p.code=
                            (select aa.code from op_app_nav aa 
                            where aa.id=
                                        (SELECT a.pid from op_app_nav a where a.id=%s))
                '''
                try:
                    res1 = self._cursorQuery(sql, [self.nav_id])
                except Exception as e:
                    dblog.error("[ERROR] Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (
                        e, __file__, sys._getframe().f_lineno))
                if len(res1) == 0:
                    print('wrong server_info-res1')
                    return ''
                # print('res111',res1,type(res1))

            else:
                sql = '''
                    select DISTINCT p.name,p.`code`,p.id as project_id,h.id as env_id,
                          e.id as app_id,e.`name`,h.env_type
                    from cmdb_project p, -- 项目表	
                        cmdb_app e , 	-- APP表
                        cmdb_server_app de , -- 服务器-app-中间表
                        cmdb_physical_server d, -- 物理机
                        cmdb_env h,	-- 环境表
                        cmdb_env_server hd -- 环境-服务器-中间表
                    where e.project_id= p.id and e.id=de.app_id 
                        and d.id=de.physical_server_id and d.id=hd.physical_server_id and hd.env_id=h.id
                        and p.code=
                                (select aa.code from op_app_nav aa 
                                where aa.id=
                                            (SELECT a.pid from op_app_nav a where a.id=%s))
                    '''
                try:
                    res2 = self._cursorQuery(sql, [self.nav_id])
                    print('res2------',res2)
                except Exception as e:
                    dblog.error("[ERROR] Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (
                        e, __file__, sys._getframe().f_lineno))
                if len(res2) == 0:
                    print('wrong server_info-res2')
                    return ''
        res1 += res2
        # print('whole-res,',res1)
        v_dic = dict()
        for v in res1:
            v_dic['project_name'] = v[0]
            v_dic['project_code'] = v[1]
            v_dic['project_id'] = v[2]
            app_dic = dict()
            app_dic['id'] = v[4]
            app_dic['name'] = v[5]
            env_dic = dict()
            env_dic['id'] = v[6]
            env_id = v[6]
            env_dic['selected'] = 0
            env_type_choices={
                '1':'dev',
                '2':'sit',
                '3':'uat',
                '4':'pre',
                '5':'prd',
            }
            if env_id in env_type_choices:
                env_dic['name'] = env_type_choices[env_id]
            if env_dic not in env_list:
                env_list.append(env_dic)
                # print('<FFFFFFFFFFFFFF------>\033[32;1m%s\033[0m' % env_list)

            if app_dic not in app_list:
                app_list.append(app_dic)
        # 如果用户有多个环境类型的权限，把第一个环境类型设为默认select = 0
        env_list[0]['selected'] = 1
        v_dic['envs'] = env_list
        v_dic['apps'] = app_list
        # print('<DDDDDDDDDDDD------>\033[31;1m%s\033[0m' % v_dic)

        # dblog.info("v_dic88888 last: %s,file: [ %s ], line: [ %s ]" % (
        #     json.dumps(v_dic, indent=4), __file__, sys._getframe().f_lineno))
        return v_dic


