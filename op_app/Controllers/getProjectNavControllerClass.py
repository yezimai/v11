#!/usr/bin/env python
# -*- coding: utf-8 -*-

from op_app.Model.projectNavinfoModelClass import GetProjectModelClass
from op_app.logger.log import runlog
import sys

class GetProjectNavControllerClass(object):

    # 检测是否有session 构造函数
    def __init__(self, request):
        self.request = request
        self.id = self.request.user.id
        self.projectNavinfo = GetProjectModelClass()

    def getProject(self): #获取对应的项目
        # user = self.request.user
        # i_class = GetProjectModelClass(user)
        # data = i_class.getProjectInfo()
        # import json
        # runlog.info('getProjectInfo data: %s' % (json.dumps(data, indent=4)))
        # return data
        '''# 1.先根据用户-组-权限-机器-应用-菜单来获取系统的菜单表，具体是先获取服务器的类型1为物理机，2为虚拟机
        2.在根据用户-组-权限-菜单来获取菜单，然后将2个获取的菜单合并展示出最后的菜单表
        3.根据菜单表来获取对应的nav导航
        :return:返回的格式是一个字典 {}
        '''
        runlog.info("Enter getProjectInfo successed,file: [ %s ], line: [ %s ]" % (
                            __file__, sys._getframe().f_lineno))
        r_list = []
        r_list_final = []
        # print('9999999999999',id)

        data_from_project = self.projectNavinfo.projectNavinfoFromProjectTable(self.id)
        if len(data_from_project) == 0:
            return []
        for i in data_from_project:
                if int(i[0]) == 2:  # 虚拟机
                    project_code = self.projectNavinfo.getProjectCodeFromVirtual_server(self.id)
                else:
                    project_code = self.projectNavinfo.getProjectCodeFromPhsical_server(self.id)
                if len(project_code) == 0:
                    return []
                for i in project_code:
                    r_list.append(i[0])

        # 通过user-组-权限-机器-应用-系统来获取对应的系统列表
        m_list=[]
        data_from_navtable = self.projectNavinfo.getProjectNavinfoFromNavTable(self.id)

        if len(data_from_navtable) == 0:
            return []
        for v in data_from_navtable:
            m_list.append(v[0])
        # 对2个获取的项目code进行求交集,然后去找对应的导航
        r_set = set(r_list)
        m_set = set(m_list)
        final_set = r_set.intersection(m_set)    # final_set = set([u'CAP'])
        final_list = list(final_set)

        # args = tuple(final_list)
        # print('<final_tuple------>\033[34;1m%s\033[0m' % args)
        if len(final_list) == 0:
            print('no intersection--')
            return []

        # for i in final_list:
        # 获取导航信息
        data = self.projectNavinfo.getProject_info(final_list)

        if len(data) == 0:
            return []
        for j in data:
            dic = dict()
            dic['id'] = j[0]
            dic['text'] = j[1]
            dic['code'] = j[2]
            dic['iconCls'] = j[3]
            r_list_final.append(dic)

        return r_list_final





