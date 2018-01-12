#!/usr/bin/python
# -*- coding: UTF-8 -*-
from op_app.Model.base.baseModelClass import BaseDbModelClass
import sys
from op_app.logger.log import dblog, runlog

#####构建sql获取APP应用的信息#######
class appConfigDetail(BaseDbModelClass):
    def __init__(self):
        super(appConfigDetail, self).__init__()


    def AppConfigDetail(self,server_type,app_id, server_id, env_id, project_id):  # 查找app的
        # 根据项目、环境、应用、ip对对应的部署在此机器上的应用信息
        if server_type == '2':
            sql = '''
                select p.code,de.install_user,
                        e.type_app,de.app_dir,
                        de.pkgname,de.server_port,e.name,
                        de.ssh_pass,de.ssh_port,de.ssh_user
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
                    de.ssh_pass,de.ssh_port,de.ssh_user
                from cmdb_server_app de,    -- 服务器-app中间表
                      cmdb_env_server hd, 	-- 服务器-环境中间表
                      cmdb_env h,					-- 环境表
                      cmdb_project p,		  -- 项目表	
                      cmdb_app e					-- app表
                where de.app_id = %s and de.app_id=e.id and de.physical_server_id = %s 
                      and hd.physical_server_id=de.physical_server_id 
                      and h.env_type=%s and h.id=hd.env_id and p.id=%s 
            '''
        else:
            # print('--wrong-server_type---->\033[42;1m\033[0m')
            runlog.error("[ERROR] --invalid-server_type-----, Catch exception:, file: [ %s ], line: [ %s ]"
                        %(__file__,sys._getframe().f_lineno))
            return ['', False]
        try:
            res = self._cursorQuery(sql, [app_id, server_id, env_id, project_id])
        except Exception as e:
            dblog.error("[ERROR] Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ],sql:[%s]" % (
                e, __file__, sys._getframe().f_lineno, sql))
            return ['', False]
        if len(res) == 0:
            # print('*****wrong action args....')
            dblog.error("[ERROR]--invalid-action args-----, Catch exception:, file: [ %s ], line: [ %s ]"
                        %(__file__,sys._getframe().f_lineno))
            return ['', False]
        return [res, True]

    def app_LogDir(self, app_id, server_type, server_id, logdir_id):  # 获取具体的某个日志目录
        if server_type == '2':  # 虚拟机
            sql = '''
                  SELECT b.log_dir
                    from cmdb_server_app a ,  -- server—app的中间表
                                op_app_logdir b			-- app日志目录表
                    where a.app_id = %s and a.server_type = %s 
                                and a.virtual_server_id = %s and a.id = b.server_app_id and b.id = %s
                  '''
        elif server_type == '1':
            sql = '''
                  SELECT b.log_dir
                    from cmdb_server_app a ,  -- server—app的中间表
                                op_app_logdir b			-- app日志目录表
                    where a.app_id = %s and a.server_type = %s 
                                and a.physical_server_id = %s and a.id = b.server_app_id and b.id = %s
                  '''
        try:
            res_dir = self._cursorQuery(sql, [app_id, server_type, server_id, logdir_id])
        except Exception as e:
            dblog.error("[ERROR] Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (
                e, __file__, sys._getframe().f_lineno))
            return {}
        else:
            if len(res_dir) == 0:
                runlog.error("[ERROR] --no found the logdir-----, Catch exception:, file: [ %s ], line: [ %s ]"
                             % (__file__, sys._getframe().f_lineno))
                return {}
        return res_dir

    def whole_appLogDirs(self, app_id, server_type, server_id):  # 获取这个app在这个服务器上所有的日志目录
        # print('oooooooooo',app_id,server_type,server_id)
        if server_type == '2':  # 虚拟机
            sql = '''
                  SELECT b.log_dir,b.id
                    from cmdb_server_app a ,  -- server—app的中间表
                                op_app_logdir b			-- app日志目录表
                    where a.app_id = %s and a.server_type = %s 
                                and a.virtual_server_id = %s and a.id = b.server_app_id
                  '''
        elif server_type == '1':
            sql = '''
                  SELECT b.log_dir,b.id
                    from cmdb_server_app a ,  -- server—app的中间表
                                op_app_logdir b			-- app日志目录表
                    where a.app_id = %s and a.server_type = %s 
                                and a.physical_server_id = %s and a.id = b.server_app_id
                  '''
        try:
            res_dir = self._cursorQuery(sql, [app_id, server_type, server_id])
        except Exception as e:
            dblog.error("[ERROR] Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (
                e, __file__, sys._getframe().f_lineno))
            return ''
        else:
            if len(res_dir) == 0:
                runlog.error("[ERROR] --no found the logdir-----, Catch exception:, file: [ %s ], line: [ %s ]"
                             % (__file__, sys._getframe().f_lineno))
                # print('logdir is nonononononono')
                return ''
        return res_dir