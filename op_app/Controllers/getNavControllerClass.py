#!/usr/bin/env python
# -*- coding: utf-8 -*-

from op_app.Model.getNavModelClass import GetNavModelClass


class GetNavControllerClass(object):

    # 检测是否有session 构造函数
    def __init__(self, request,data):
        self.request = request
        self.data = data

    def getNav(self):
        user = self.request.user
        i_class = GetNavModelClass(user, self.data)
        return i_class.getNavInfo()





