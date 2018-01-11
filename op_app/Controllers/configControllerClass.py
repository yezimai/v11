#!/usr/bin/python
# -*- coding: UTF-8 -*-


import os
import sys
import time
from op_app.Extends.paramikoTool import ParamikoTool


class ConfigControllerClass(object):

    def getAppDirs(self, request):
        '''
        返回树形的目录结构数据
        1、同步script/functions ${HOME}/op/ 下
        2、ssh 远程调用:
            funcions/bin/get_dir_files.py  /usr/local/tomcat8080/webapps/classes/conf
            获取返回结果并返回
        :return: data
        '''
        data = [
            {
                'text': 'document1',
                'state' : {
                    'opened': 'true',
                },
                'children': [
                    {
                        'text': 'document2',
                        'state' : {
                            'opened': 'true',
                        },
                        'children': [
                            {
                                'text': 'file2.txt',
                                'type' : 'file',
                                'icon' : 'jstree-file',
                            }
                        ]
                    }
                ]
            },{
                'text': 'file1.txt',
                'type' : 'file',
                'icon' : 'jstree-file',
            }
        ]

        t_pt = ParamikoTool()
        cmds = [['chmod', '+x', '/home/beehive/test/script/bin'],
                ['python', '/home/beehive/test/script/bin/get_dirs_files.py', '/home/beehive/test']]

        ip, user, port, passwd = '10.83.36.86', 'beehive', '10022', 'beehive_1'  # 参数demo
        ret_data = t_pt.execCommandInRemoteHostOutput(ip, user, port, passwd, *cmds)
        # print('type of ret_data:', type(ret_data))
        # print('ret_data:', ret_data)
        cmd_len, ret_data_len = len(cmds), len(ret_data)
        try:
            if len(ret_data) < cmd_len:  # 命令未全部执行完就已经报错
                print('cmd: [ %s ], error_info: [ %s ]' %
                      (cmds[ret_data_len - 1], ret_data[ret_data_len - 1][1]))
                return [{
                            'text': '获取文件目录结构失败',
                            'type': 'file',
                            'icon': 'jstree-file',
                         }]
            ret_status = ret_data[ret_data_len - 1][0]
            if int(ret_status) != 0:  # 执行最后一条命令出错
                print('Exec cmd: [ %s ] failed, error_info: [ %s ]' %
                      (cmds[ret_data_len - 1], ret_data[ret_data_len - 1][1]))
                return [{
                    'text': '获取文件目录结构失败',
                    'type': 'file',
                    'icon': 'jstree-file',
                }]
            org_data = ret_data[ret_data_len - 1][1]
            # print('type of data: ', type(org_data))
            # print('data:', org_data)
            list_data = eval(org_data)
            # print('type of list_data: ', type(list_data))
            # print('list_data:', list_data)
        except Exception as e:
            print('Catch error: [ %s ]' % (e))  # 记录详细日志
            return [{
                'text': '获取文件目录结构失败',
                'type': 'file',
                'icon': 'jstree-file',
            }]
        else:
            return list_data


    def getFileContent(self, request):
        '''
        获取指定文件内容返回,
        1、远程命令执行 cat -v xx.xml 来获取,获取后再在本地创建一个备份
        参考 saveFileContent 方法中的配置文件记录根目录（可配置，这里假设=/home/change_history）
        2、创建一个 {/home/change_history}/{登录用户}/{年月日}/org}/{配置文件目录}/{用户提交的相对目录这里是config}/a.xml 写入获取的内容
        3、审计日志写入
        :return:content
        '''
        data = '''中文：获取指定文件内容返回
        this is in china'''
        return data


    def dealUploadFile(self, request):
        '''
        1、文件上传到本地临时目录，此目录在配置模块中设置，使用yaml模块读取，假如这里是 /tmp/upload_files
            那么就将文件上传到 {/tmp/upload_files}/{登录用户}/{配置文件目录}/{用户提交的相对目录这里是config}/{a.file=用户上传的文件}
        2、将文件使用dos2unix 命令转换为unix 格式
        3、将文件使用rsync同步到 远程客户端
        4、审计日志记录
        :param request:
        :return: True/False
        '''
        file_obj, dir = request.FILES.get('file'), request.GET.get('dir')
        if file_obj:  # 处理附件上传到方法
            accessory_dir = '/tmp/test'  # 上传到此目录demo
            try:
                if not os.path.isdir(accessory_dir):
                    os.mkdir(accessory_dir)
                upload_file = "{}/{}".format(accessory_dir, file_obj.name)
                with open(upload_file, 'wb') as new_file:
                    for chunk in file_obj.chunks():
                        new_file.write(chunk)
            except Exception as e:
                print "[ERROR] Catch file: [ %s ], line:[ %s ] exception: [ %s ]" % (
                                        __file__, sys._getframe().f_lineno, e)
                return False
            else:
                return True
        return True


    # 重命名 远程机器 上目录或者文件
    def renameDirOrFile(self, request):
        '''
        1、运行远程命令进行 mv org_dir/org_file new_dir/new_file
        2、审计日志记录
        :param request:
        :return:
        '''
        old_name = request.POST.get('old_dir_file')
        new_name = request.POST.get('new_dir_file')
        print "old_name:", old_name
        print "new_name:", new_name
        return True

    def sshCreateFolder(self, request):
        '''
        1、运行远程命令进行 mkdir -p xx
        2、审计日志记录
        :param request:
        :return:
        '''
        print('sshCreateFolder test ok')
        return True

    def saveFileContent(self, request):
        '''
        前端传入文件内容，将内容首选utf-8格式写入到本地目录，然后在同步到远程对应文件目录中，本地保留一个时间搓的记录目录
        比如参数如下：
            1.配置文件目录为: /usr/local/tomcat8080/webapps/LoginSYS/WEB-INF
            2.用户更改配置文件为 {配置文件目录}/config/a.xml
            3.在工程的配置模块中 配置保存历史更改的配置文件的 基本目录(可以由用户自由配置，用yaml模块加载配置的值)，
              假如所有更改都保存在 /home/change_history
            当用户保存一个更改的文件的时候，将进行如下操作：
            1、将前端的文件内容写入到
                {op工程目录}/tasks/configuration/{登录用户}/{配置文件目录}/{用户提交的相对目录这里是config}/a.xml
            2、同步a.xml 到客户端：
                {配置文件目录}/{用户提交的相对目录这里是config}/a.xml:
                同步成功：保存一份记录到
                    {/home/change_history}/{登录用户}/{年月日}/时分秒_unix时间搓}/{配置文件目录}/{用户提交的相对目录这里是config}/a.xml
                同步失败：返回false

        :param request:
        :return:
        '''
        print('saveFileContent test ok')
        return True

    def removeDirOrFile(self, request):
        '''
        1、将此目录或者文件同步到
            {/home/change_history}/{登录用户}/{年月日}/org}/{配置文件目录}/{用户提交的相对目录这里是config}
          这里假如 用户删除 {配置文件目录}/{用户提交的相对目录这里是config} 的目录

        同步成功：执行rm -rf xx.dir   rm -f xx.file
        同步失败：返回 False
        2、无论成功失败，都要记录审计日志；
        :param request:
        :return:True/False
        '''
        print('removeDirOrFile test ok')
        return True