#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
from django.db import connections, connection
from op_app.Model.base.baseModelClass import BaseDbModelClass
from op_app.logger.log import dblog


class GetHostInfoModelClass(BaseDbModelClass):
    def __init__(self,request):
        super(GetHostInfoModelClass, self).__init__()
        self.request = request

    def getHostInfo(self):
        '''# 先获取服务器的类型1为物理机，2为虚拟机
        :return:返回的格式是一个字典
        '''
        user_id =self.request.user.id
        project_id = self.request.GET.get('project_id', '')
        env_id = self.request.GET.get('env_id','') #环境类型id
        app_id = self.request.GET.get('app_id','') #应用id
        print('project_id--userid--env_id,app_id',project_id,user_id,env_id,app_id)
        if project_id == '' or env_id == '' or app_id == '':
            print('wrong args from web..')
            return []
        sql = '''SELECT ab.server_type 
                  from cmdb_app a, cmdb_server_app ab 
                  where a.id=%s and a.id=ab.app_id'''
        try:
            data = self._cursorQuery(sql, [app_id])
            print '!!!!!',data
        except Exception as e:
            dblog.error("[ERROR] Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" \
                        % (e, __file__, sys._getframe().f_lineno))
        if len(data) == 0:
            print('server_type is valid.')
            return []
        r_list = []
        for v in data:
            if int(v[0]) == 2:  # 虚拟机,获取虚拟机的ip，责任人信息
                sql = '''select ip.sys_ip,u.user_name,h.name
                        from auth_user a, -- 用户表
                                        op_app_group b, -- 组表
                                        op_app_group_user ab, -- 用户-组-中间表
                                        op_app_permission c, -- 权限表
                                        op_app_group_permission bc, -- 权限- 组-中间表
                                        op_app_permission_server cd ,  -- 权限-服务器-中间表
                                        cmdb_virtual_server d, -- 虚拟服务器表
                                        cmdb_app e ,  			-- app表
                                        cmdb_server_app de,		-- 服务器 - app-中间表
                                        cmdb_project p, 		-- 项目表
                                        cmdb_user_info u,		-- 用户详情表
                                        cmdb_ip ip,              -- ip表
                                        cmdb_env h ,		    -- 环境信息表
                                        cmdb_env_server hd   	-- 环境-服务器中间表
                        where a.id=%s and a.id=ab.user_id and ab.group_id = b.id 
                                and b.id=bc.group_id and bc.permission_id=c.id 
                                and c.id=cd.permission_id and cd.server_type=2 and cd.virtual_server_id=d.id
                                and d.id=de.virtual_server_id and de.app_id=e.id and e.id= %s 
                                and e.project_id=p.id and p.project_manager=u.only_id and d.ip_id=ip.id
                                and h.id=%s and h.id=hd.env_id and d.id=hd.virtual_server_id'''
                try:
                    data = self._cursorQuery(sql, [user_id, app_id, env_id])
                except Exception as e:
                    dblog.error("[ERROR] Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" \
                                % (e, __file__, sys._getframe().f_lineno))
                if len(data) == 0:
                    print('virtualserver ip fail')
                    return []
                for i in range(len(data)):
                    dic1 = dict()
                    dic1['ip'] = data[i][0]
                    dic1['manager'] = data[i][1]
                    dic1['env_name'] = data[i][2]
                    # print data[i][1]
                    r_list.append(dic1)
                print('<------>\033[32;1m%s\033[0m' %r_list)
            else:   # 如果是物理服务器
                sql = '''select u.user_name,ip.sys_ip
                            from auth_user a, -- 用户表
                                op_app_group b, -- 组表
                                op_app_group_user ab, -- 用户-组-中间表
                                op_app_permission c, -- 权限表
                                op_app_group_permission bc, -- 权限- 组-中间表
                                op_app_permission_server cd ,  -- 权限-服务器-中间表
                                cmdb_physical_server d, -- 虚拟服务器表
                                cmdb_app e ,  				-- app表
                                cmdb_server_app de,		-- 服务器 - app-中间表
                                cmdb_project p, 			-- 项目表
                                cmdb_user_info u,			-- 用户详情表
                                cmdb_ip ip,					-- ip表
                                cmdb_env h ,		    -- 环境信息表
                                cmdb_env_server hd   	-- 环境-服务器中间表 
                            where a.id=%s and a.id=ab.user_id and ab.group_id = b.id 
                                        and b.id=bc.group_id and bc.permission_id=c.id 
                                        and c.id=cd.permission_id and cd.server_type=1 and cd.physical_server_id=d.id
                                        and d.id=de.physical_server_id and de.app_id=e.id and e.id= %s
                                        and e.project_id=p.id and p.project_manager=u.only_id and d.ip_id=ip.id
                                        and h.id=%s and h.id=hd.env_id and hd.physical_server_id = d.id
                            '''
                try:
                    data = self._cursorQuery(sql,[user_id, app_id,env_id])
                except Exception as e:
                    dblog.error("[ERROR] Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]"
                                % (e, __file__, sys._getframe().f_lineno))
                for i in range(len(data)):
                    dic2 = dict()
                    dic2['ip']=data[i][0]
                    dic2['manager'] = data[i][1]
                    dic2['env_name'] = env_id
                    r_list.append(dic2)
        print('rlist<------>\033[32;1m%s\033[0m' % r_list)
        return r_list