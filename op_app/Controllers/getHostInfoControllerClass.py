#!/usr/bin/env python
# -*- coding: utf-8 -*-


from op_app.Model.getHostInfoModelClass import GetHostInfoModelClass


class GetHostInfoControllerClass(object):

    # 检测是否有session 构造函数
    def __init__(self, request):
        self.request = request

    def getHostInfo(self):  # 获取对应的项目
        i_class = GetHostInfoModelClass(self.request)
        data = dict()
        data['data'] = i_class.getHostInfo()
        return data





