#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.conf.urls import url
from views import *


urlpatterns = [
    ##### login ####
    url(r'^$', index, name='index'),
    url(r'^index/$',  index, name='index'),
    url(r'^login/$',  login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^password_change/$', password_change,name='password_change'),
    url(r'^password_change_done/$', password_change_done, name='password_change_done'),
    ##### login end ####

    ## 导航 ##
    url(r'^getNav/$', getNav, name='getNav'),

    ## 管理 ###
    url(r'^manage/$', manage, name='manage'),
    url(r'^hostInfo/$', hostInfo, name='hostInfo'),
    url(r'^doServiceManageAction/$', doServiceManageAction, name='doServiceManageAction'),
    url(r'^getLogDetail/$', getLogDetail, name='getLogDetail'),
    url(r'^doFunctionPage/$', doFunctionPage, name='doFunctionPage'),

    ### 日志查看  #####
    url(r'^getLogInfo/$', getLogInfo, name='getLogInfo'),
    url(r'^getShowLogDetail/$', getShowLogDetail, name='getShowLogDetail'),
    url(r'^downloadlog/$', downloadlog, name='downloadlog'),



    ### 配置文件更改  #####
    url(r'^getAppDirs/$', getAppDirs, name='getAppDirs'),  # 获取目录结构
    url(r'^getFileContent/$', getFileContent, name='getFileContent'),  # 获取文件内容返回
    url(r'^renameDirOrFile/$', renameDirOrFile, name='renameDirOrFile'),
    url(r'^dealUploadFile/$', dealUploadFile, name='dealUploadFile'),
    url(r'^sshCreateFolder/$', sshCreateFolder, name='sshCreateFolder'),
    url(r'^saveFileContent/$', saveFileContent, name='saveFileContent'),
    url(r'^removeDirOrFile/$', removeDirOrFile, name='removeDirOrFile'),






    ### 发布 ###
    url(r'^release/$', release, name='release'),

    ### 统计 ###
    url(r'^statistics/$', statistics, name='statistics'),



    url(r'^test/$', test, name='test'),

]