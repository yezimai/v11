#!/usr/bin/python
# -*- coding: UTF-8 -*-


from op_app.Model.base.baseModelClass import BaseDbModelClass
from op_app.logger.log import dblog
import sys

class GetProjectDetailModelClass(BaseDbModelClass):

    def __init__(self,nav_id,user_id):
        super(GetProjectDetailModelClass,self).__init__()
        self.nav_id = nav_id
        self.user_id = user_id

    def getProjectInfo(self):
        '''#
        :return:返回的格式是一个字典
        '''
        # 先查找出所在服务器的类型，虚拟机or物理机
        dict_final = dict()
        sql = '''select DISTINCT de.server_type 
                    from cmdb_project p, -- 项目表	
                                cmdb_app e , 	-- APP表
                                cmdb_server_app de  -- 服务器-app-中间表
                    where e.project_id= p.id and e.id=de.app_id 
                    and p.code=
                                (select aa.code from op_app_nav aa 
                                where aa.id=
                                            (SELECT a.pid from op_app_nav a where a.id=%s))'''
        try:
            server_type = self._cursorQuery(sql,[self.nav_id])
            print '!!!!!server_type :', server_type
        except Exception as e:
            dblog.error("[ERROR] Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (
                e, __file__, sys._getframe().f_lineno))
        if len(server_type) == 0 :
            print('wrong server_type11')
            return ''
        for i in server_type:
            if int(i[0]) == 2: #虚拟机
                sql = '''
                select DISTINCT p.name,p.`code`,p.id as project_id,h.id as env_id,
                      e.id as app_id,e.`name`,h.env_type
                from cmdb_project p, -- 项目表	
                    cmdb_app e , 	-- APP表
                    cmdb_server_app de , -- 服务器-app-中间表
                    cmdb_virtual_server d, -- 虚拟机
                    cmdb_env h,	-- 环境表
                    cmdb_env_server hd -- 环境-服务器-中间表
                where e.project_id= p.id and e.id=de.app_id 
                    and d.id=de.virtual_server_id and d.id=hd.virtual_server_id and hd.env_id=h.id
                    and p.code=
                            (select aa.code from op_app_nav aa 
                            where aa.id=
                                        (SELECT a.pid from op_app_nav a where a.id=%s))
                '''
                try:
                    res = self._cursorQuery(sql, [self.nav_id])
                except Exception as e:
                    dblog.error("[ERROR] Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (
                        e, __file__, sys._getframe().f_lineno))
                if len(res) == 0:
                    print('wrong server_type12')
                    return ''
                for v in res:
                    v_dic = dict()
                    v_dic['project_name'] = v[0]
                    v_dic['project_code'] = v[1]
                    v_dic['project_id'] = v[2]
                    app_dic = dict()
                    app_dic['id'] = v[4]
                    app_dic['name'] = v[5]
                    app_list = []
                    app_list.append(app_dic)
                    v_dic['apps'] = app_list
                    env_dic = dict()
                    env_dic['id'] = v[3]
                    env_id = v[6]
                    env_dic['selected'] = 0
                    env_type_choices={
                        1:'dev',
                        2:'sit',
                        3:'uat',
                        4:'pre',
                        5:'prd',
                    }
                    if env_id in env_type_choices:
                        env_dic['name'] = env_type_choices[env_id]
                    env_list = []
                    env_list.append(env_dic)
                    v_dic['envs'] = env_list
                    print('<DDDDDDDDDDDD------>\033[32;1m%s\033[0m' % dict_final)



        # res_dic = {}
        # r_list=[]
        #
        # app_list=[]
        # for v in data:
        #     r_dic = {}
        #     res_dic['project_name'] = v[0]
        #     res_dic['project_code'] = v[1]
        #     res_dic['project_id'] = v[2]
        #     r_dic['name']=v[3]
        #     r_dic['id']=v[4]
        #     r_list.append(r_dic)
        #     res_dic['apps']=r_list
        #     #app_list.append(v[4])
        # print('rdic<------>\033[32;1m%s\033[0m' % res_dic)
        # #print('app_list<------>\033[32;1m%s\033[0m' % app_list)
        # #2.找到权限对应环境相关信息
        # #
        # sql = '''SELECT b.type from auth_user a,op_app_group b,op_app_group_user ab \
        #           WHERE a.id=%s and a.id=ab.user_id and ab.group_id=b.id'''
        # try:
        #     data = self._cursorQuery(sql,[self.user_id])
        # except Exception as e:
        #     dblog.error("[ERROR] Query error, Catch exception:[ %s ], file: [ %s ], line: [ %s ]" % (
        #         e, __file__, sys._getframe().f_lineno))
        # env_list = []
        # print('envtpye999999',data)
        # if data:
        #     env_type_choices={
        #         1:'dev',
        #         2:'sit',
        #         3:'uat',
        #         4:'pre',
        #         5:'prd',
        #     }
        #     for i in data:  #data=((2,), (1,))
        #         env_dic={}
        #         print('pppp',i)
        #         index=i[0]
        #         if index in  env_type_choices:
        #             #env_type_name = env_type_choices[i]
        #             env_dic['id'] = index
        #             env_dic['name'] = env_type_choices[index]
        #             env_dic['selected'] = 0
        #             env_list.append(env_dic)
        #             print('@@@@@@------',env_list)
        # res_dic['envs'] = env_list
        #
        # print('resdic<------>\033[34;1m%s\033[0m' % res_dic)
        #return res_dic
        #return r_list