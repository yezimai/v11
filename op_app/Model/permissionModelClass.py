#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
     权限模型类 model
'''

import sys
from op_app.Model.base.defaultDbModelClass import DefaultDbModelClass
from op_app.logger.log import dblog


class PermissionModelClass(DefaultDbModelClass):

    def __init__(self, uid):
        super(PermissionModelClass, self).__init__()
        self.uid = uid

    def getAccessServerInfo(self):
        '''
        根据用户id 获取能访问的机器信息
        :return: [[server_type, server_id], [2, 10], [1, 11]]
        '''
        ret_lst = []
        sql = '''
        SELECT t6.server_type, t6.physical_server_id, t6.virtual_server_id
                FROM auth_user t1,                   -- 用户表
                op_app_group_user t2,                -- 用户-用户组中间表
                op_app_group t3,                     -- 用户组表
                op_app_group_permission t4,          -- 用户组权限中间表
                op_app_permission t5,                -- 用户权限表
                op_app_permission_server t6
        WHERE t1.id=%s AND t1.id=t2.user_id AND
                t2.group_id=t3.id AND t3.id=t4.group_id AND
                t4.permission_id=t5.id AND t5.id=t6.permission_id

        '''
        try:
            data = self._cursorQuery(sql, [self.uid])
        except Exception as e:
            dblog.error('Catch error: [ %s ], file: [ %s ], line: [ %s ]'
                        % (e, __file__, sys._getframe().f_lineno))
            return ret_lst
        else:
            if len(data) == 0:
                dblog.error('Get data is null, file: [ %s ], line: [ %s ]'
                        % (__file__, sys._getframe().f_lineno))
                return ret_lst
            for e_data in data:
                # print('server_type:', e_data[0])
                # print('physical_server_id:', e_data[1])
                # print('virtual_server_id:', e_data[2])
                if e_data[1] is None:
                    ret_lst.append([int(e_data[0]), int(e_data[2])])
                else:
                    ret_lst.append([int(e_data[0]), int(e_data[1])])
            return ret_lst


















