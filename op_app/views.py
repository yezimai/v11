#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, render_to_response
from Controllers.loginControllerClass import LoginControllerClass
from op_app.Controllers.taskManageControllerClass import TaskManageControllerClass
from op_app.Controllers import (getNavControllerClass, getProjectNavControllerClass,
                                getProjectDetailControllerClass,getHostInfoControllerClass,
                                serviceManageActionControllerClass,logDetailControllerClass)


def login(request):
    c_login = LoginControllerClass(request)
    return c_login.login()
# 退出
def logout(request):
    c_login = LoginControllerClass(request)
    return c_login.logout()
# 密码更改
def password_change(request):
    c_login = LoginControllerClass(request)
    return c_login.password_change()
# 密码更改完成
def password_change_done(request):
    return render(request, 'login/password_change_done.html')
# 首页
def index(request):
    c_login = LoginControllerClass(request)
    return c_login.index()




####### code begin ##############

def getNav(request):
    '''
    导航数据获取
    :param request:
    :return:
    '''
    # data = [
    #     {
    #         'text': u'蜂巢系统',
    #         'id': 23L,
    #         'children': [
    #             {
    #                 'text': u'管理',
    #                 'id': 40L,
    #                 # 'children': []
    #             }, {
    #                 'text': u'统计',
    #                 'id': 50L,
    #                 # 'children': []
    #             }
    #         ]
    #      },{
    #         'text': u'信审系统',
    #         'id': 27L,
    #         'children': [
    #             {
    #                 'text': u'管理',
    #                 'id': 40L,
    #                 # 'children': []
    #             }, {
    #                 'text': u'统计',
    #                 'id': 50L,
    #                 # 'children': []
    #             }
    #         ]
    #     }
    # ]
    # 获取用户有权限的项目
    i_pro_class = getProjectNavControllerClass.GetProjectNavControllerClass(request)
    data = i_pro_class.getProject()
    #获取导航
    i_nav_class = getNavControllerClass.GetNavControllerClass(request, data)
    data = i_nav_class.getNav()


    return JsonResponse(data, safe=False)


def manage(request):
    '''
    管理页面获取
    :param request:
    :return:
    '''
    data = {
        'project_name': '蜂巢系统',
        'project_code': 'HCS',
        'project_id': 1,
        'envs': [
            {
                'id': 1,
                'name': 'DEV',
                'selected': 0
            },{
                'id': 2,
                'name': 'SIT',
                'selected': 0
            },{
                'id': 3,
                'name': 'UAT',
                'selected': 1
            },{
                'id': 4,
                'name': 'PRE',
                'selected': 0
            },{
                'id': 5,
                'name': 'PRD',
                'selected': 0
            }
        ],
        'apps': [
            {
                'id': 10,
                'name': 'beehive',
            },{
                'id': 11,
                'name': 'LoginSYS',
            },{
                'id': 12,
                'name': 'fileupload',
            }
        ]
    }
    i_class = getProjectDetailControllerClass.GetProjectDetailControllerClass(request)
    data = i_class.getProject()
    return render(request, 'manage/index.html', {'data': data})

def release(request):
    '''
    发布页面获取
    :return:
    '''
    return render(request, 'release/release.html', {'data': 'test release'})

def statistics(request):
    '''
    统计页面获取
    :return:
    '''
    return render(request, 'statistics/statistics.html', {'data': 'test statistics'})


def hostInfo(request):
    '''
    获取主机信息，返回给前端管理页面
    :param request: GET 传参，  project_id、 env_type、 select_app
    :return:
    '''
    project_id, env_id, app_id = request.GET.get('project_id', '0'), request.GET.get('env_id', '0'), request.GET.get('app_id', '0')
    print('project_id:', project_id, ' env_id:', env_id, ' select_app:', app_id)

    data = {
        "data": [
            {
                "ip": "10.0.0.2",
                "server_type": 2,
                "server_id": 1,
                "env_name": "sit1",
                "manager": "刘国华"
            },
            {
                "ip": "10.0.0.3",
                "server_type": 2,
                "server_id": 2,
                "env_name": "sit3",
                "manager": "李华"
            },
            {
                "ip": "10.0.0.4",
                "server_type": 2,
                "server_id": 3,
                "env_name": "sit4",
                "manager": "游昌永"
            },
            {
                "ip": "10.0.0.5",
                "server_type": 2,
                "server_id": 4,
                "env_name": "sit5",
                "manager": "游昌永"
            },
            {
                "ip": "10.0.0.6",
                "server_type": 2,
                "server_id": 5,
                "env_name": "sit1",
                "manager": "李智军"
            },
            {
                "ip": "10.0.0.7",
                "server_type": 2,
                "server_id": 6,
                "env_name": "sit1",
                "manager": "游昌永"
            },
            {
                "ip": "10.0.0.8",
                "server_type": 2,
                "server_id": 7,
                "env_name": "sit7",
                "manager": "刘国华"
            },
            {
                "ip": "10.0.0.9",
                "server_type": 2,
                "server_id": 8,
                "env_name": "sit1",
                "manager": "李智军"
            },
            {
                "ip": "10.0.0.10",
                "server_type": 2,
                "server_id": 9,
                "env_name": "sit1",
                "manager": "刘国华"
            },
            {
                "ip": "10.0.0.11",
                "server_type": 2,
                "server_id": 10,
                "env_name": "sit1",
                "manager": "游昌永"
            },
            {
                "ip": "10.0.0.12",
                "server_type": 2,
                "server_id": 11,
                "env_name": "sit1",
                "manager": "刘国华"
            },
            {
                "ip": "10.0.0.13",
                "server_type": 2,
                "server_id": 12,
                "env_name": "sit1",
                "manager": "李智军"
            },
        ]
    }
    i_class = getHostInfoControllerClass.GetHostInfoControllerClass(request)
    return JsonResponse(i_class.getHostInfo(), safe=False)

def doServiceManageAction(request):
    '''
    用户操作页面， 如启动、停止、等等执行运行远程命令的操作
    :param request:
    :return:
    '''
    project_id = request.POST.get('project_id', '0')
    env_id = request.POST.get('env_id', '')
    app_id = request.POST.get('app_id', '')
    ip = request.POST.get('ip', '')
    action = request.POST.get('action', '')
    server_type = request.POST.get('server_type', '')
    server_id = request.POST.get('server_id', '')

    '''根据项目、环境、应用、ip对对应的部署在此机器上的应用进行操作,
        1、确定要操作的机器，找出应用部署的用户名、端口、密码，部署路径等详细信息；
        2、同步本地脚本到远程端；
           假如有个应用 LoginSYS，部署在 10.0.0.3 机器，部署用户为 beehive用户，那么：
           2.1 在tasks 下创建一个
             service_manage/10.0.0.3/LoginSYS/scripts/
                - bin/ 这个是从 scripts/client/service_manage/bin/* 拷贝过来的；
                - conf/ 这个下面有个配置文件：app_config.conf 文件实时生成；
                配置文件参考

            # 写入配置文件
            f = open(scriptdir + '/conf/app_config.conf', 'w') # 开始写入配置文件
            f.write('pkgfile={0}'.format(REMOTE_BASE_DIR + dir_name + '/'  + appname + '/pkg/' + dic['pkgname']) + '\n')
            f.write('appnumber={0}'.format('1') + '\n')
            f.write('projectname={0}'.format(data[1]) + '\n')
            f.write('ip={0}'.format(ip) + '\n')
            f.write('user[1]={0}'.format(dic['install_user']) + '\n')
            f.write('upgradetype[1]=full' + '\n')
            f.write('apptype[1]=tomcat' + '\n')
            f.write('backupdir[1]={0}'.format(REMOTE_BASE_DIR + dir_name + '/' + appname + '/backup') + '\n')
            f.write('appdir[1]={0}'.format(dic['appdir']) + '\n')
            f.write('appwarname[1]={0}'.format(dic['pkgname']) + '\n')
            f.write('startuptime[1]=1000' + '\n')
            f.write('port[1]=8080' + '\n')
            f.close() # 写入配置文件完成

           2.2 将 service_manage/10.0.0.3/ 目录下的内容 rsync 同步到远程目录固定目录： ${HOME}/service_manage/ 下，
           2.3 远程调用 10.0.0.3 机器下  ${HOME}/service_manage/bin/startapp.sh 或者 stopapp.sh, 成功返回成功，失败返回失败

    '''
    import time
    i_class = serviceManageActionControllerClass.ManageActionControllerClass(request)
    res = i_class.getAction()
    time.sleep(5)
    return JsonResponse(res, safe=False)


def doFunctionPage(request):
    '''
    单独的页面进行操作如：日志查看、任务管理、命令执行、机器详情页面
    :param request:
    :return:
    '''
    project_id = request.GET.get('project_id', '0')
    env_id = request.GET.get('env_id', '')
    app_id = request.GET.get('app_id', '')
    ip = request.GET.get('ip', '')
    action = request.GET.get('action', '')
    server_type = request.GET.get('server_type', '')
    server_id = request.GET.get('server_id', '')
    print('server_type:', server_type)
    print('server_id:', server_id)

    if action == 'log_show':  # 日志查看
        data = {
            'project_id': project_id,
            'env_id': env_id,
            'app_id': app_id,
            'server_type': server_type,
            'server_id': server_id,
            'ip': ip,
            'user': 'user1',
            'logdirs': [
                {
                    'id': 11,
                    'dir': '/usr/local/tomcat8080/logs'
                },{
                    'id': 12,
                    'dir': '/usr/local/tomcat8081/logs'
                }
            ],
        }
        return render(request, 'manage/log_show.html', {'data': data})
    elif action == 'task_manage':  # 任务管理
        data = {
            'project_id': project_id,
            'env_id': env_id,
            'app_id': app_id,
            'server_type': server_type,
            'server_id': server_id,
            'content': '''
*/10 * * * * /usr/sbin/ntpdate -u cn.pool.ntp.org >/dev/null 2>&1
*/1 * * * * cd /usr/local/gse/gseagent; ./cron_agent.sh 1>/dev/null 2>&1''',
        }
        return render(request, 'manage/task_manage.html', {'data': data})
    elif action == 'run_command':  # 命令执行
        return render(request, 'manage/run_command.html', {'data': 'test run_command'})
    elif action == 'configuration':  # 配置文件更改
        return render(request, 'manage/configuration.html', {'data': 'test configuration'})
    elif action == 'machine_detail':  # 机器详情
        return render(request, 'manage/machine_detail.html', {'data': 'test machine_detail'})
    else:
        return render(request, '404.html', {'data': 'test 404'})

def getLogDetail(request):
    '''
    在执行命令的时候，获取实时的日志输出，主要针对 action是启动、停止、重启
    远程执行命令获取日志信息返回，
    :param request:
    :return:
    '''
    project_id = request.GET.get('project_id', '0')
    env_id = request.GET.get('env_id', '')
    app_id = request.GET.get('app_id', '')
    ip = request.GET.get('ip', '')
    action = request.GET.get('action', '')
    server_type = request.GET.get('server_type', '')
    server_id = request.GET.get('server_id', '')

    data = {
        'data': '''{"hostname":"10.41.0.106:10006","remote_addr":"116.211.165.13","date":"2018-01-03T13:39:21+08:00","request_method":"POST","path_info":"/identity/liveness_selfie_verification","query_string":"","http_version":"HTTP/1.0","http_status":200,"user_agent":null,"referer":null,"content_type":"application/json;charset=utf-8","content_length":217,"runtime":1.004671985,"request_id":"TID990cc530bcfb4fa2b18c73dbc78b4eab","key_id":"64b72c0cebee46eb87620ff99c2be78b","params":{"captures":[]},"uri":"/identity/liveness_selfie_verification","format":"JPEG","quality":85,"image_id":"2a01dbb249d5443eb92f6cd6d65792ab","status":"OK"}
","remote_addr":"10.41.0.253","date":"2018-01-03T13:59:54+08:00","request_method":"POST","path_info":"/identity/selfie_idcard_watermark_verification","query_string":"","http_version":"HTTP/1.1","http_status":200,"user_agent":"HttpComponents/1.1","referer":null,"content_type":"application/json;charset=utf-8","content_length":150,"runtime":0.98213683,"request_id":"TIDc1f4e401d89f452580880020936071c6","params":{"watermark_picture_url":"http://ifcs.bqjr.cn:8081/2018/01/03/13/511011199006192527.jpg","selfie_auto_rotate":"true","idcard_auto_rotate":"true","selfie_is_multifaces":"true","captures":[]},"uri":"/identity/selfie_idcard_watermark_verification","format":"JPEG","quality":78,"image_id":"1d5ded73dd1747baa3bfa0992b990897","status":"OK","exif_orient":1}
{"hostname":"10.41.0.106:10006","remote_addr":"10.41.0.253","date":"2018-01-03T14:00:14+08:00","request_method":"POST","path_info":"/identity/selfie_idcard_watermark_verification","query_string":"","http_version":"HTTP/1.1","http_status":200,"user_agent":"HttpComponents/1.1","referer":null,"content_type":"application/json;charset=utf-8","content_length":151,"runtime":0.817649989,"request_id":"TID54f7f8026f7343e1a121b54eb181f64f","params":{"watermark_picture_url":"http://ifcs.bqjr.cn:8081/2018/01/03/14/422801198406132414.jpg","selfie_auto_rotate":"true","idcard_auto_rotate":"true","selfie_is_multifaces":"true","captures":[]},"uri":"/identity/selfie_idcard_watermark_verification","format":"JPEG","quality":100,"image_id":"5e216f4d72d64d5f9964a23b4631a6e6","status":"OK"}
{"hostname":"10.41.0.106:10006","remote_addr":"10.41.0.253","date":"2018-01-03T14:00:14+08:00","request_method":"GET","path_info":"/","query_string":"","http_version":"HTTP/1.1","http_status":404,"user_agent":"Zabbix","referer":null,"content_type":"application/json","content_length":null,"runtime":0.000159685}
{"hostname":"10.41.0.106:10006","remote_addr":"10.41.0.253","date":"2018-01-03T14:00:20+08:00","request_method":"GET","path_info":"/","query_string":"","http_version":"HTTP/1.1","http_status":404,"user_agent":"Zabbix","referer":null,"content_type":"application/json","content_length":null,"runtime":0.000309835}
{"hostname":"10.41.0.106:10006","remote_addr":"10.41.0.253","date":"2018-01-03T14:00:24+08:00","request_method":"POST","path_info":"/identity/selfie_idcard_watermark_verification","query_string":"","http_version":"HTTP/1.1","http_status":200,"user_agent":"HttpComponents/1.1","referer":null,"content_type":"application/json;charset=utf-8","content_length":151,"runtime":0.940364446,"request_id":"TIDa2c8a73d93144a3484b580faad273d13","params":{"watermark_picture_url":"http://ifcs.bqjr.cn:8081/2018/01/03/14/150421198411060087.jpg","selfie_auto_rotate":"true","idcard_auto_rotate":"true","selfie_is_multifaces":"true","captures":[]},"uri":"/identity/selfie_idcard_watermark_verification","format":"JPEG","quality":78,"image_id":"302c6ac33ba547a99a6ff9b711230958","status":"OK","exif_orient":1}
{"hostname":"10.41.0.106:10006","remote_addr":"116.211.165.16","date":"2018-01-03T14:00:26+08:00","request_method":"POST","path_info":"/identity/liveness_selfie_verification","query_string":"","http_version":"HTTP/1.0","http_status":200,"user_agent":null,"referer":null,"content_type":"application/json;charset=utf-8","content_length":218,"runtime":0.973778874,"request_id":"TID88eecba180d24a9483351ec87195dc04","key_id":"64b72c0cebee46eb87620ff99c2be78b","params":{"captures":[]},"uri":"/identity/liveness_selfie_verification","format":"JPEG","quality":85,"image_id":"d03196f622e9410d84ddd9bd669b0b83","status":"OK"}
{"hostname":"10.41.0.106:10006","remote_addr":"10.41.0.253","date":"2018-01-03T14:00:42+08:00","request_method":"GET","path_info":"/","query_string":"","http_version":"HTTP/1.1","http_status":404,"user_agent":"Zabbix","referer":null,"content_type":"application/json","content_length":null,"runtime":0.000155472}
{"hostname":"10.41.0.106:10006","remote_addr":"10.41.0.253","date":"2018-01-03T14:00:54+08:00","request_method":"POST","path_info":"/identity/selfie_idcard_watermark_verification","query_string":"","http_version":"HTTP/1.1","http_status":200,"user_agent":"HttpComponents/1.1","referer":null,"content_type":"application/json;charset=utf-8","content_length":149,"runtime":0.897179794,"request_id":"TIDbfb1309c645a4765ae6eddb53e23b4a0","params":{"watermark_picture_url":"http://ifcs.bqjr.cn:8081/2017/12/30/15/15252719720510393X.jpg","selfie_auto_rotate":"true","idcard_auto_rotate":"true","selfie_is_multifaces":"true","captures":[]},"uri":"/identity/selfie_idcard_watermark_verification","format":"JPEG","quality":94,"image_id":"17abe2c740bd4c4988aac51ca35cfeeb","status":"OK","exif_orient":1}
{"hostname":"10.41.0.106:10006","remote_addr":"10.41.0.253","date":"2018-01-03T14:01:07+08:00","request_method":"POST","path_info":"/identity/selfie_idcard_watermark_verification","query_string":"","http_version":"HTTP/1.1","http_status":200,"user_agent":"HttpComponents/1.1","referer":null,"content_type":"application/json;charset=utf-8","content_length":151,"runtime":1.165136439,"request_id":"TID45b6f468248e4a2ba45163e68388b6de","params":{"watermark_picture_url":"http://ifcs.bqjr.cn:8081/2018/01/03/13/150424199710015124.jpg","selfie_auto_rotate":"true","idcard_auto_rotate":"true","selfie_is_multifaces":"true","captures":[]},"uri":"/identity/selfie_idcard_watermark_verification","format":"JPEG","quality":100,"image_id":"5b49524f35ff45bba5f17134ff0640d1","status":"OK"}
{"hostname":"10.41.0.106:10006","remote_addr":"218.11.4.12","date":"2018-01-03T14:01:12+08:00","request_method":"POST","path_info":"/identity/liveness_selfie_verification","query_string":"","http_version":"2.3.5","http_status":200,"user_agent":"Wallet/2.3.5 (iPhone; iOS 11.0.3; Scale/3.00)","referer":null,"content_type":"application/json;charset=utf-8","content_length":232,"runtime":1.173941963,"request_id":"TID404d31718d1344b29db300e769d8f9fa","params":{"captures":[]},"uri":"/identity/liveness_selfie_verification","format":"JPEG","exif_orient":1,"quality":78,"image_id":"a07024c0c95c4a7dbdaa87c10713f6fb","status":"OK"}
{"hostname":"10.41.0.106:10006","remote_addr":"10.41.0.253","date":"2018-01-03T14:01:24+08:00","request_method":"POST","path_info":"/identity/selfie_idcard_watermark_verification","query_string":"","http_version":"HTTP/1.1","http_status":200,"user_agent":"HttpComponents/1.1","referer":null,"content_type":"application/json;charset=utf-8","content_length":151,"runtime":0.976346191,"request_id":"TID34c0334acbc04f66a18a361fdaca5ccf","params":{"idcard_picture_url":"http://prdmmtoss01.vpc100-oss-cn-shenzhen.aliyuncs.com/prd/user/1712319823058401/1001.jpg?Expires=1530597680&OSSAccessKeyId=LTAIDprnSAmmYlmV&Signature=r89VYvrWi3AmuFVFRc%2FanqJudBg%3D","selfie_url":"http://prdmmtoss01.vpc100-oss-cn-shenzhen.aliyuncs.com/prd/user/1712319823058401/1004.jpg?Expires=1530597680&OSSAccessKeyId=LTAIDprnSAmmYlmV&Signature=0juvLXKaq1jxfkd1EQoQQ9sjkcE%3D","watermark_picture_url":"http://ifcs.bqjr.cn:8081/2018/01/03/14/510322199303306759.jpg","selfie_auto_rotate":"true","idcard_auto_rotate":"true","selfie_is_multifaces":"true","captures":[]},"uri":"/identity/selfie_idcard_watermark_verification","format":"JPEG","quality":80,"image_id":"3acc2379f98b4697b23be2093a8fb478","status":"OK"}
{"hostname":"10.41.0.106:10006","remote_addr":"10.41.0.253","date":"2018-01-03T14:01:24+08:00","request_method":"POST","path_info":"/identity/selfie_idcard_watermark_verification","query_string":"","http_version":"HTTP/1.1","http_status":200,"user_agent":"HttpComponents/1.1","referer":null,"content_type":"application/json;charset=utf-8","content_length":151,"runtime":0.981608297,"request_id":"TID26ae6df2e0684121b2a42196b6dcc3fe","params":{"idcard_picture_url":"http://prdmmtoss01.vpc100-oss-cn-shenzhen.aliyuncs.com/prd/user/1709179556598201/1001.jpg?Expires=1530597680&OSSAccessKeyId=LTAIDprnSAmmYlmV&Signature=yt%2BsNO%2FjVEeU2vjGPtj%2FXYAmgtA%3D","selfie_url":"http://prdmmtoss01.vpc100-oss-cn-shenzhen.aliyuncs.com/prd/user/1709179556598201/1004.jpg?Expires=1530597680&OSSAccessKeyId=LTAIDprnSAmmYlmV&Signature=FyBdoEH3AMggEKdsEFa1HPF3BV0%3D","watermark_picture_url":"http://ifcs.bqjr.cn:8081/2018/01/03/14/140321199104111857.jpg","selfie_auto_rotate":"true","idcard_auto_rotate":"true","selfie_is_multifaces":"true","captures":[]},"uri":"/identity/selfie_idcard_watermark_verification","format":"JPEG","quality":80,"image_id":"7da18732c7974bc9a8c52594a7d4e086","status":"OK"}
{"hostname":"10.41.0.106:10006","remote_addr":"10.41.0.253","date":"2018-01-03T14:01:25+08:00","request_method":"POST","path_info":"//identity/liveness_selfie_verification","query_string":"","http_version":"HTTP/1.1","http_status":200,"user_agent":null,"referer":null,"content_type":"application/json;charset=utf-8","content_length":232,"runtime":1.301026609,"request_id":"TIDe5ed6da3a910403ca41b4406e72d4bcb","params":{"liveness_data_url":"http://static.xjd.billionsfinance.cn/imgsys/customer_pic/2018-01-03/5783672_package","selfie_url":"http://static.xjd.billionsfinance.cn/imgsys/customer_pic/2018-01-03/24416650_vivo_idCard_face.jpg","selfie_auto_rotate":"1","captures":[]},"uri":"/identity/liveness_selfie_verification","format":"JPEG","quality":100,"image_id":"cba9f2b7b07f4315a35cf2ee3dd42d5f","status":"OK"}''',
        'title': '运维平台-日志查看-日志详情'
    }
    i_class = logDetailControllerClass.LogDetailControllerClass(request)

    data = dict()
    data['title'] = '运维平台-日志查看-日志详情'
    data['data'] = i_class.getLogDetail()
    return render(request, 'manage/logdetail.html', {'data': data})


def getLogInfo(request):
    project_id = request.GET.get('project_id', '0')
    env_id = request.GET.get('env_id', '')
    app_id = request.GET.get('app_id', '')
    ip = request.GET.get('ip', '')
    # action = request.POST.get('action', '')
    logdir_id = request.GET.get('logdir_id', '')
    server_type = request.GET.get('server_type', '')
    server_id = request.GET.get('server_id', '')

    print('getLogDetail project_id:', project_id)
    print('getLogDetail env_id:', env_id)
    print('getLogDetail app_id:', app_id)
    print('getLogDetail ip:', ip)
    print('getLogDetail logdir_id:', logdir_id)

    data1 = {
        'data': [
            {
                'no': '4',
                'file': '4.catalina.out',
                'owner': 'beehive',
                'group': 'group1',
                'size': '1.5M',
                'last_modify': '2017-12-08 15:33:36',
            }, {
                'no': '5',
                'file': '5.catalina.out',
                'owner': 'beehive',
                'group': 'group1',
                'size': '1.6M',
                'last_modify': '2017-12-08 15:33:12',
            }, {
                'no': '6',
                'file': '6.catalina.out',
                'owner': 'beehive',
                'group': 'group1',
                'size': '2.3M',
                'last_modify': '2017-12-08 15:08:40',
            },{
                'no': '7',
                'file': '7.catalina.out',
                'owner': 'beehive',
                'group': 'group1',
                'size': '3.6M',
                'last_modify': '2017-12-08 15:34:40',
            }, {
                'no': '8',
                'file': '8.catalina.out',
                'owner': 'beehive',
                'group': 'group1',
                'size': '3.5M',
                'last_modify': '2017-12-08 15:12:40',
            },{
                'no': '9',
                'file': '9.catalina.out',
                'owner': 'beehive',
                'group': 'group1',
                'size': '6.1M',
                'last_modify': '2017-12-08 15:11:40',
            }
        ]
    }
    data2 = {
        'data': [
            {
                'no': '100',
                'file': '111.catalina.out',
                'owner': 'beehive',
                'group': 'group1',
                'size': '2.5M',
                'last_modify': '2017-12-18 15:33:40',
            }, {
                'no': '500',
                'file': '121.catalina.out',
                'owner': 'beehive',
                'group': 'group1',
                'size': '3.5M',
                'last_modify': '2017-12-28 15:33:40',
            }, {
                'no': '600',
                'file': '131.catalina.out',
                'owner': 'beehive',
                'group': 'group1',
                'size': '12M',
                'last_modify': '2017-01-08 15:33:40',
            }, {
                'no': '700',
                'file': '141.catalina.out',
                'owner': 'beehive',
                'group': 'group1',
                'size': '36M',
                'last_modify': '2017-02-08 15:33:40',
            }, {
                'no': '800',
                'file': '151.catalina.out',
                'owner': 'beehive',
                'group': 'group1',
                'size': '65M',
                'last_modify': '2017-03-08 15:33:40',
            }, {
                'no': '900',
                'file': '161.catalina.out',
                'owner': 'beehive',
                'group': 'group1',
                'size': '32M',
                'last_modify': '2017-06-08 15:33:40',
            }
        ]
    }
    if int(logdir_id) == 12:
        return JsonResponse(data1, safe=False)
    else:
        return JsonResponse(data2, safe=False)

def getShowLogDetail(request):
    '''
    在日志查看的时候，获取实时的日志输出
    远程执行命令获取日志信息返回，
    :param request:
    :return:
    '''
    project_id = request.GET.get('project_id', '0')
    env_id = request.GET.get('env_id', '')
    app_id = request.GET.get('app_id', '')
    ip = request.GET.get('ip', '')
    logdir_id = request.GET.get('logdir_id', '')
    server_type = request.GET.get('server_type', '')
    server_id = request.GET.get('server_id', '')
    file_name = request.GET.get('file_name', '')

    print('getShowLogDetail project_id:', project_id)
    print('getShowLogDetail env_id:', env_id)
    print('getShowLogDetail app_id:', app_id)
    print('getShowLogDetail ip:', ip)
    print('getShowLogDetail logdir_id:', logdir_id)
    print('getShowLogDetail server_type:', server_type)
    print('getShowLogDetail server_id:', server_id)
    print('getShowLogDetail file_name:', file_name)

    data = {
        'data': '''{"hostname":"10.41.0.106:10006","remote_addr":"116.211.165.13","date":"2018-01-03T13:39:21+08:00","request_method":"POST","path_info":"/identity/liveness_selfie_verification","query_string":"","http_version":"HTTP/1.0","http_status":200,"user_agent":null,"referer":null,"content_type":"application/json;charset=utf-8","content_length":217,"runtime":1.004671985,"request_id":"TID990cc530bcfb4fa2b18c73dbc78b4eab","key_id":"64b72c0cebee46eb87620ff99c2be78b","params":{"captures":[]},"uri":"/identity/liveness_selfie_verification","format":"JPEG","quality":85,"image_id":"2a01dbb249d5443eb92f6cd6d65792ab","status":"OK"}
","remote_addr":"10.41.0.253","date":"2018-01-03T13:59:54+08:00","request_method":"POST","path_info":"/identity/selfie_idcard_watermark_verification","query_string":"","http_version":"HTTP/1.1","http_status":200,"user_agent":"HttpComponents/1.1","referer":null,"content_type":"application/json;charset=utf-8","content_length":150,"runtime":0.98213683,"request_id":"TIDc1f4e401d89f452580880020936071c6","params":{"watermark_picture_url":"http://ifcs.bqjr.cn:8081/2018/01/03/13/511011199006192527.jpg","selfie_auto_rotate":"true","idcard_auto_rotate":"true","selfie_is_multifaces":"true","captures":[]},"uri":"/identity/selfie_idcard_watermark_verification","format":"JPEG","quality":78,"image_id":"1d5ded73dd1747baa3bfa0992b990897","status":"OK","exif_orient":1}
{"hostname":"10.41.0.106:10006","remote_addr":"10.41.0.253","date":"2018-01-03T14:00:14+08:00","request_method":"POST","path_info":"/identity/selfie_idcard_watermark_verification","query_string":"","http_version":"HTTP/1.1","http_status":200,"user_agent":"HttpComponents/1.1","referer":null,"content_type":"application/json;charset=utf-8","content_length":151,"runtime":0.817649989,"request_id":"TID54f7f8026f7343e1a121b54eb181f64f","params":{"watermark_picture_url":"http://ifcs.bqjr.cn:8081/2018/01/03/14/422801198406132414.jpg","selfie_auto_rotate":"true","idcard_auto_rotate":"true","selfie_is_multifaces":"true","captures":[]},"uri":"/identity/selfie_idcard_watermark_verification","format":"JPEG","quality":100,"image_id":"5e216f4d72d64d5f9964a23b4631a6e6","status":"OK"}
{"hostname":"10.41.0.106:10006","remote_addr":"10.41.0.253","date":"2018-01-03T14:00:14+08:00","request_method":"GET","path_info":"/","query_string":"","http_version":"HTTP/1.1","http_status":404,"user_agent":"Zabbix","referer":null,"content_type":"application/json","content_length":null,"runtime":0.000159685}
{"hostname":"10.41.0.106:10006","remote_addr":"10.41.0.253","date":"2018-01-03T14:00:20+08:00","request_method":"GET","path_info":"/","query_string":"","http_version":"HTTP/1.1","http_status":404,"user_agent":"Zabbix","referer":null,"content_type":"application/json","content_length":null,"runtime":0.000309835}
{"hostname":"10.41.0.106:10006","remote_addr":"10.41.0.253","date":"2018-01-03T14:00:24+08:00","request_method":"POST","path_info":"/identity/selfie_idcard_watermark_verification","query_string":"","http_version":"HTTP/1.1","http_status":200,"user_agent":"HttpComponents/1.1","referer":null,"content_type":"application/json;charset=utf-8","content_length":151,"runtime":0.940364446,"request_id":"TIDa2c8a73d93144a3484b580faad273d13","params":{"watermark_picture_url":"http://ifcs.bqjr.cn:8081/2018/01/03/14/150421198411060087.jpg","selfie_auto_rotate":"true","idcard_auto_rotate":"true","selfie_is_multifaces":"true","captures":[]},"uri":"/identity/selfie_idcard_watermark_verification","format":"JPEG","quality":78,"image_id":"302c6ac33ba547a99a6ff9b711230958","status":"OK","exif_orient":1}
{"hostname":"10.41.0.106:10006","remote_addr":"116.211.165.16","date":"2018-01-03T14:00:26+08:00","request_method":"POST","path_info":"/identity/liveness_selfie_verification","query_string":"","http_version":"HTTP/1.0","http_status":200,"user_agent":null,"referer":null,"content_type":"application/json;charset=utf-8","content_length":218,"runtime":0.973778874,"request_id":"TID88eecba180d24a9483351ec87195dc04","key_id":"64b72c0cebee46eb87620ff99c2be78b","params":{"captures":[]},"uri":"/identity/liveness_selfie_verification","format":"JPEG","quality":85,"image_id":"d03196f622e9410d84ddd9bd669b0b83","status":"OK"}
{"hostname":"10.41.0.106:10006","remote_addr":"10.41.0.253","date":"2018-01-03T14:00:42+08:00","request_method":"GET","path_info":"/","query_string":"","http_version":"HTTP/1.1","http_status":404,"user_agent":"Zabbix","referer":null,"content_type":"application/json","content_length":null,"runtime":0.000155472}
{"hostname":"10.41.0.106:10006","remote_addr":"10.41.0.253","date":"2018-01-03T14:00:54+08:00","request_method":"POST","path_info":"/identity/selfie_idcard_watermark_verification","query_string":"","http_version":"HTTP/1.1","http_status":200,"user_agent":"HttpComponents/1.1","referer":null,"content_type":"application/json;charset=utf-8","content_length":149,"runtime":0.897179794,"request_id":"TIDbfb1309c645a4765ae6eddb53e23b4a0","params":{"watermark_picture_url":"http://ifcs.bqjr.cn:8081/2017/12/30/15/15252719720510393X.jpg","selfie_auto_rotate":"true","idcard_auto_rotate":"true","selfie_is_multifaces":"true","captures":[]},"uri":"/identity/selfie_idcard_watermark_verification","format":"JPEG","quality":94,"image_id":"17abe2c740bd4c4988aac51ca35cfeeb","status":"OK","exif_orient":1}
{"hostname":"10.41.0.106:10006","remote_addr":"10.41.0.253","date":"2018-01-03T14:01:07+08:00","request_method":"POST","path_info":"/identity/selfie_idcard_watermark_verification","query_string":"","http_version":"HTTP/1.1","http_status":200,"user_agent":"HttpComponents/1.1","referer":null,"content_type":"application/json;charset=utf-8","content_length":151,"runtime":1.165136439,"request_id":"TID45b6f468248e4a2ba45163e68388b6de","params":{"watermark_picture_url":"http://ifcs.bqjr.cn:8081/2018/01/03/13/150424199710015124.jpg","selfie_auto_rotate":"true","idcard_auto_rotate":"true","selfie_is_multifaces":"true","captures":[]},"uri":"/identity/selfie_idcard_watermark_verification","format":"JPEG","quality":100,"image_id":"5b49524f35ff45bba5f17134ff0640d1","status":"OK"}
{"hostname":"10.41.0.106:10006","remote_addr":"218.11.4.12","date":"2018-01-03T14:01:12+08:00","request_method":"POST","path_info":"/identity/liveness_selfie_verification","query_string":"","http_version":"2.3.5","http_status":200,"user_agent":"Wallet/2.3.5 (iPhone; iOS 11.0.3; Scale/3.00)","referer":null,"content_type":"application/json;charset=utf-8","content_length":232,"runtime":1.173941963,"request_id":"TID404d31718d1344b29db300e769d8f9fa","params":{"captures":[]},"uri":"/identity/liveness_selfie_verification","format":"JPEG","exif_orient":1,"quality":78,"image_id":"a07024c0c95c4a7dbdaa87c10713f6fb","status":"OK"}
{"hostname":"10.41.0.106:10006","remote_addr":"10.41.0.253","date":"2018-01-03T14:01:24+08:00","request_method":"POST","path_info":"/identity/selfie_idcard_watermark_verification","query_string":"","http_version":"HTTP/1.1","http_status":200,"user_agent":"HttpComponents/1.1","referer":null,"content_type":"application/json;charset=utf-8","content_length":151,"runtime":0.976346191,"request_id":"TID34c0334acbc04f66a18a361fdaca5ccf","params":{"idcard_picture_url":"http://prdmmtoss01.vpc100-oss-cn-shenzhen.aliyuncs.com/prd/user/1712319823058401/1001.jpg?Expires=1530597680&OSSAccessKeyId=LTAIDprnSAmmYlmV&Signature=r89VYvrWi3AmuFVFRc%2FanqJudBg%3D","selfie_url":"http://prdmmtoss01.vpc100-oss-cn-shenzhen.aliyuncs.com/prd/user/1712319823058401/1004.jpg?Expires=1530597680&OSSAccessKeyId=LTAIDprnSAmmYlmV&Signature=0juvLXKaq1jxfkd1EQoQQ9sjkcE%3D","watermark_picture_url":"http://ifcs.bqjr.cn:8081/2018/01/03/14/510322199303306759.jpg","selfie_auto_rotate":"true","idcard_auto_rotate":"true","selfie_is_multifaces":"true","captures":[]},"uri":"/identity/selfie_idcard_watermark_verification","format":"JPEG","quality":80,"image_id":"3acc2379f98b4697b23be2093a8fb478","status":"OK"}
{"hostname":"10.41.0.106:10006","remote_addr":"10.41.0.253","date":"2018-01-03T14:01:24+08:00","request_method":"POST","path_info":"/identity/selfie_idcard_watermark_verification","query_string":"","http_version":"HTTP/1.1","http_status":200,"user_agent":"HttpComponents/1.1","referer":null,"content_type":"application/json;charset=utf-8","content_length":151,"runtime":0.981608297,"request_id":"TID26ae6df2e0684121b2a42196b6dcc3fe","params":{"idcard_picture_url":"http://prdmmtoss01.vpc100-oss-cn-shenzhen.aliyuncs.com/prd/user/1709179556598201/1001.jpg?Expires=1530597680&OSSAccessKeyId=LTAIDprnSAmmYlmV&Signature=yt%2BsNO%2FjVEeU2vjGPtj%2FXYAmgtA%3D","selfie_url":"http://prdmmtoss01.vpc100-oss-cn-shenzhen.aliyuncs.com/prd/user/1709179556598201/1004.jpg?Expires=1530597680&OSSAccessKeyId=LTAIDprnSAmmYlmV&Signature=FyBdoEH3AMggEKdsEFa1HPF3BV0%3D","watermark_picture_url":"http://ifcs.bqjr.cn:8081/2018/01/03/14/140321199104111857.jpg","selfie_auto_rotate":"true","idcard_auto_rotate":"true","selfie_is_multifaces":"true","captures":[]},"uri":"/identity/selfie_idcard_watermark_verification","format":"JPEG","quality":80,"image_id":"7da18732c7974bc9a8c52594a7d4e086","status":"OK"}
{"hostname":"10.41.0.106:10006","remote_addr":"10.41.0.253","date":"2018-01-03T14:01:25+08:00","request_method":"POST","path_info":"//identity/liveness_selfie_verification","query_string":"","http_version":"HTTP/1.1","http_status":200,"user_agent":null,"referer":null,"content_type":"application/json;charset=utf-8","content_length":232,"runtime":1.301026609,"request_id":"TIDe5ed6da3a910403ca41b4406e72d4bcb","params":{"liveness_data_url":"http://static.xjd.billionsfinance.cn/imgsys/customer_pic/2018-01-03/5783672_package","selfie_url":"http://static.xjd.billionsfinance.cn/imgsys/customer_pic/2018-01-03/24416650_vivo_idCard_face.jpg","selfie_auto_rotate":"1","captures":[]},"uri":"/identity/liveness_selfie_verification","format":"JPEG","quality":100,"image_id":"cba9f2b7b07f4315a35cf2ee3dd42d5f","status":"OK"}''',
        'title': '运维平台-日志查看-日志详情'
    }
    return render(request, 'manage/logdetail.html', {'data': data})




def saveCrontabContent(request):
    '''
    保存crontab 文件接口
    :param request:
    :return: True/False
    '''
    c_taskManage = TaskManageControllerClass(request)
    is_ok = c_taskManage.saveCrontabContent()

    # project_id = request.POST.get('project_id', '0')
    # env_id = request.POST.get('env_id', '')
    # app_id = request.POST.get('app_id', '')
    # server_type = request.POST.get('server_type', '')
    # server_id = request.POST.get('server_id', '')
    # content = request.POST.get('content', '')

    return JsonResponse(is_ok, safe=False)

def getCrontabContent(request):
    '''
    返回对应机器用户的crontab 文件内容
    :param request:
    :return: crontab 文件内容
    '''
    c_taskManage = TaskManageControllerClass(request)
    data = c_taskManage.getCrontabContent()

    # project_id = request.POST.get('project_id', '0')
    # env_id = request.POST.get('env_id', '')
    # app_id = request.POST.get('app_id', '')
    # server_type = request.POST.get('server_type', '')
    # server_id = request.POST.get('server_id', '')
#     data = '''
# */10 * * * * /usr/sbin/ntpdate -u cn.pool.ntp.org >/dev/null 2>&1
# */1 * * * * cd /usr/local/gse/gseagent; ./cron_agent.sh 1>/dev/null 2>&1
# */10 * * * * cd /usr/local/test 1>/dev/null 2>&1
#     '''
    return JsonResponse(data, safe=False)




















### 测试代码 #####
def test(request):
    # m_data = CmdbModelClass()
    return JsonResponse('123', safe=False)


### 测试代码 #####
def test2(request):
    # m_data = CmdbModelClass()
    return JsonResponse('123', safe=False)








