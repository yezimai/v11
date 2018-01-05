#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
from op_app.Model.base.baseModelClass import BaseDbModelClass
from op_app.logger.log import dblog


class GetHostInfoModelClass(BaseDbModelClass):
    def __init__(self, request):
        super(GetHostInfoModelClass, self).__init__()
        self.request = request

    def getHostInfo(self):
        '''# 先获取服务器的类型1为物理机，2为虚拟机
        :return:返回的格式是一个字典
        '''
        r_list = []
        user_id = self.request.user.id
        project_id = self.request.GET.get('project_id', '')
        env_id = self.request.GET.get('env_id', '')  # 环境类型的id -1.dev,2.sit
        app_id = self.request.GET.get('app_id', '')  # 应用id
        # print('project_id--userid--env_id,app_id',project_id,user_id,env_id,app_id)
        if project_id == '' or env_id == '' or app_id == '':
            dblog.error('wrong args from web, file: [ %s ], line: [ %s ]'
                        % (__file__, sys._getframe().f_lineno))
            return []
        # 先查询出服务器类型
        sql = '''SELECT DISTINCT ab.server_type 
                  from cmdb_app a, cmdb_server_app ab 
                  where a.id=%s and a.id=ab.app_id'''
        try:
            data = self._cursorQuery(sql, [app_id])
        except Exception as e:
            dblog.error("[ERROR] Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" \
                        % (e, __file__, sys._getframe().f_lineno))
            return []
        else:
            if len(data) == 0:
                dblog.error('Data is null, file: [ %s ], line: [ %s ]'
                            % (__file__, sys._getframe().f_lineno))
                return []
            for v in data:
                if int(v[0]) == 2:  # 虚拟机,获取虚拟机的ip，责任人信息
                    sql = '''select ip.sys_ip,u.user_name,h.name,hd.server_type,hd.virtual_server_id
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
                                    and h.env_type=%s and h.id=hd.env_id and d.id=hd.virtual_server_id'''
                    try:
                        data2 = self._cursorQuery(sql, [user_id, app_id, env_id])
                    except Exception as e:
                        dblog.error("Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]"
                                    % (e, __file__, sys._getframe().f_lineno))
                        return []
                    else:
                        if len(data2) == 0:
                            dblog.error("Data2 is null virtualserver ip fail or no permissions, \
                                        file: [ %s ], line: [ %s ]"
                                        % (__file__, sys._getframe().f_lineno))
                            return []
                        for v_data2 in data2:
                            dic1 = dict()
                            dic1['ip'] = v_data2[0]
                            dic1['manager'] = v_data2[1]
                            dic1['env_name'] = v_data2[2]
                            dic1['server_type'] = v_data2[3]
                            dic1['server_id'] = v_data2[4]
                            r_list.append(dic1)
                else:   # 如果是物理服务器
                    sql = '''select u.user_name,ip.sys_ip,hd.server_type,hd.physical_server_id
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
                                            and h.env_type=%s and h.id=hd.env_id and hd.physical_server_id = d.id
                                '''
                    try:
                        data3 = self._cursorQuery(sql, [user_id, app_id, env_id])
                    except Exception as e:
                        dblog.error("Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]"
                                    % (e, __file__, sys._getframe().f_lineno))
                        return []
                    for v_data3 in data3:
                        dic2 = dict()
                        dic2['ip'] = v_data3[0]
                        dic2['manager'] = v_data3[1]
                        dic2['env_name'] = env_id
                        dic2['server_type'] = v_data3[3]
                        dic2['server_id'] = v_data3[4]
                        r_list.append(dic2)
        return r_list