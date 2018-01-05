#!/usr/bin/python
# -*- coding: UTF-8 -*-

from op_app.Model.permissionModelClass import PermissionModelClass
from op_app.logger.log import runlog

class TaskManageControllerClass(object):

    def __init__(self, request):
        '''
        构造函数，或者初始化函数，参数都存在request 中
        :param request: 前端出入的参数
        '''
        self.project_id = request.POST.get('project_id', '0')
        self.env_id = request.POST.get('env_id', '')
        self.app_id = request.POST.get('app_id', '')
        self.server_type = request.POST.get('server_type', '')
        self.server_id = request.POST.get('server_id', '')
        self.content = request.POST.get('content', '')
        self.user_id = request.user.id
        self.m_permission = PermissionModelClass(self.user_id)

    def getCrontabContent(self):
        '''
        获取crontab 内容返回
        :return:
        '''
        ret_info = self.m_permission.getAccessServerInfo()
        if (int(self.server_type), int(self.server_id)) not in ret_info:
            return 'no permission'
        else:
            return '''
*/10 * * * * /usr/sbin/ntpdate -u cn.pool.ntp.org >/dev/null 2>&1
*/1 * * * * cd /usr/local/gse/gseagent; ./cron_agent.sh 1>/dev/null 2>&1
*/10 * * * * cd /usr/local/test 1>/dev/null 2>&1
'''


    def saveCrontabContent(self):
        '''
        保持 crontab 内容到客户端
        :return:
        '''
        ret_info = self.m_permission.getAccessServerInfo()
        runlog.info('ret_info: [ %s ]' % ret_info)
        if (int(self.server_type), int(self.server_id)) not in ret_info:  # 没有权限
            return False
        else:
            ### 保存内容到客户端代码 ####
            runlog.info('true')
            return True