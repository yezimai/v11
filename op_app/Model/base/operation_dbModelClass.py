#!/usr/bin/python
# -*- coding: UTF-8 -*-
from op_app.Model.base.baseModelClass import BaseDbModelClass
import sys
class Operation_dbModelClass(BaseDbModelClass):

    def __init__(self):
        self.db = 'op_db'
        super(Operation_dbModelClass, self).__init__(self.db)

    def inserToLog(self, username, ip, action, memo):
        '''用户名，ip，动作，内容'''
        sql = '''
            INSERT into operation_log (`username`,`ip`,`action`,`memo`) 
            VALUES(%s,%s,%s,%s)
        '''
        try:
            status = self._cursorInsert(sql, [username, ip, action, memo])
        except Exception as e:
            print("[ERROR] Insert error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (e, __file__, sys._getframe().f_lineno))
            return False
        else:
            if status == '1':
                return True
            else:
                return False