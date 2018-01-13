#!/usr/bin/python
# -*- coding: UTF-8 -*-
from op_app.Model.base.baseModelClass import BaseDbModelClass
from op_app.logger.log import dblog
import sys


class GetProjectModelClass(BaseDbModelClass):
    def __init__(self):
        super(GetProjectModelClass, self).__init__()

    def projectNavinfoFromProjectTable(self, id):
        sql = '''
            SELECT DISTINCT t6.server_type,
                               t6.virtual_server_id,
                               t6.physical_server_id
                        FROM `auth_user` t1, -- 用户表
                                `op_app_group_user` t2, -- 用户-组-中间表
                                `op_app_group` t3,  -- 用户组表
                                `op_app_group_permission` t4, -- 组-权限中间表
                                `op_app_permission` t5, -- 权限表
                                `op_app_permission_server` t6 -- 权限-服务器中间表
                        WHERE t1.id=%s AND t1.id=t2.user_id AND t2.group_id=t3.id
                                    AND t3.id=t4.group_id AND t4.permission_id=t5.id
                                    AND t5.id=t6.permission_id'''
        try:
            data = self._cursorQuery(sql, [id])
            print('<------>\033[32;1m%s\033[0m' %len(data))
            dblog.info('data is: %s, file: [ %s ], line: [ %s ]' % (data, __file__, sys._getframe().f_lineno))
            if len(data) == 0:
                dblog.error('project data is None , file: [ %s ], line: [ %s ]' % (__file__, sys._getframe().f_lineno))
                return ''
        except Exception as e:
            dblog.error("[ERROR] Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (e, __file__, sys._getframe().f_lineno))
            return ''
        return data

    def getProjectCodeFromVirtual_server(self, id):
        sql = '''select f.code 
                  from auth_user a, -- 用户表
                        op_app_group_user ab, -- 用户-组-中间表
                        op_app_group b, -- 用户组表
                        op_app_permission c, -- 权限表
                        op_app_group_permission bc , -- 权限-组-中间表
                        cmdb_virtual_server d, -- 虚拟服务器表
                        op_app_permission_server cd, -- 权限-服务器-中间表
                        cmdb_server_app de, -- 服务器-app-中间表
                        cmdb_app e,-- app表
                        cmdb_project f -- 项目表
                  where a.id = %s and a.id =ab.user_id and ab.group_id=b.id and b.id=bc.group_id 
                        and bc.permission_id=c.id and c.id=cd.permission_id and cd.virtual_server_id=d.id 
                        and d.id=de.virtual_server_id 
                        and de.app_id=e.id and e.project_id=f.id'''
        try:
            data = self._cursorQuery(sql, [id])

            dblog.info(
                'data2 is: %s, file: [ %s ], line: [ %s ]' % (data, __file__, sys._getframe().f_lineno))
            return data
        except Exception as e:
            dblog.error("[ERROR] Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (
                e, __file__, sys._getframe().f_lineno))
            return ''

    def getProjectCodeFromPhsical_server(self, id):
        sql = '''
              select f.code 
              from auth_user a, -- 用户表
                    op_app_group_user ab, -- 用户-组-中间表
                    op_app_group b, -- 用户组
                    op_app_permission c, -- 权限表
                    op_app_group_permission bc, -- 组-权限-中间表
                    cmdb_physical_server d, -- 物理服务器表
                    op_app_permission_server cd,-- 权限-服务器-中间表
                    cmdb_server_app de, -- app-服务器-中间表
                    cmdb_app e, -- app表
                    cmdb_project f -- 项目表
              where a.id=%s and ab.user_id=a.id and b.id=bc.group_id 
                    and c.id=bc.permission_id and c.id=cd.permission_id 
                    and cd.physical_server_id=d.id=de.physical_server_id
                    and de.app_id=e.id and e.project_id=f.id'''
        try:
            data = self._cursorQuery(sql, [id])
            print('-----9999', data)
            dblog.info('data1 is: %s, file: [ %s ], line: [ %s ]' \
                       % (data, __file__, sys._getframe().f_lineno))
            return data
        except Exception as e:
            dblog.error("[ERROR] Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" \
                        % (e, __file__, sys._getframe().f_lineno))
            return ''

    def getProjectNavinfoFromNavTable(self, id):
        sql = '''select DISTINCT f.code 
                          from auth_user a , -- 用户表
                                op_app_group g, -- 组表
                                op_app_group_user ag, -- 用户-组-中间表
                                op_app_permission c, -- 权限表
                                op_app_group_permission cg, -- 权限-组-中间表
                                op_app_nav f ,-- 导航表
                                op_app_permission_nav cf  -- 导航-权限-中间表
                          where a.id = %s and a.id=ag.user_id and ag.group_id=g.id and g.id=cg.group_id 
                                and cg.permission_id=c.id and c.id=cf.permission_id and cf.nav_id=f.id and f.pid=0'''

        try:
            data = self._cursorQuery(sql, [id])
            return data
        except Exception as e:
            dblog.error("[ERROR] Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (
                e, __file__, sys._getframe().f_lineno))
            return ''

    def getProject_info(self, final_list):
        in_p = ', '.join((map(lambda x: '%s', final_list)))
        sql = '''select p.id, p.name, p.code, j.icon
                          from cmdb_project p, op_app_nav j  -- 项目表
                          where p.code=j.code and p.code in (%s)'''
        try:
            data = self._cursorQuery(sql % in_p, final_list)
            # dblog.info(
            #     'datajiaoji is: %s, file: [ %s ], line: [ %s ]' % (data, __file__, sys._getframe().f_lineno))
            return data
        except Exception as e:
            dblog.error("[ERROR] Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (
                e, __file__, sys._getframe().f_lineno))
            return ''