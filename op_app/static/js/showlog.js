$(function(){

    var waitDialog = dialog({   // 加载对话框
        width: 200,
        content: '<img class="mr5" src="https://magicbox.bkclouds.cc/static_api/v3/components/loading1/images/loading_2_16x16.gif">请稍后，加载中...'
    });

    function success(data){     // 提交成功提示信息
        var animation = $(this).attr('data-animation');
        toastr.remove();
        toastr.success('<br>'+ data,'提示',{
            timeOut:1000,
            showMethod :animation
        });
    }

    function error(data){          //  错误时候提示信息
        var animation = $(this).attr('data-animation');
        toastr.remove();
        toastr.error('<br>'+ data,'提示',{
            timeOut:1500,
            showMethod :animation
        });
    }

    var language = {
        search: '搜索：',
        lengthMenu: "每页显示 _MENU_ 记录",
        zeroRecords: "没找到相应的数据！",
        info: "分页 _PAGE_ / _PAGES_",
        infoEmpty: "暂无数据！",
        infoFiltered: "(从 _MAX_ 条数据中搜索)",
        paginate: {
        first: '首页',
        last: '尾页',
        previous: '上一页',
        next: '下一页',
        }
    }

    var params = '?project_id='+ $('#project_id').val() +
                 '&env_id=' + $('#env_id').val() +
                 '&app_id=' + $('#app_id').val() +
                 '&ip='+ $('#ip').val() +
                 '&logdir_id=' + $('.select-log').val() +
                 '&server_type=' + $('#server_type').val() +
                 '&server_id=' + $('#server_id').val();

    /* 表格内容获取 */
    $("#table2_demo4").dataTable({
        autoWidth: false,
        lengthChange: true,       //不允许用户改变表格每页显示的记录数
        pageLength : 10,          //每页显示几条数据
        lengthMenu: [10, 20, 40], //每页显示选项
        pagingType: 'full_numbers',
        ajax : '/op/getLogInfo/' + params,
        ordering: true,
        columns : [
          {data:"no", orderable: true},
          {data:"file"},
          {data:"owner"},
          {data:"group"},
          {data:"size"},
          {data:"last_modify"},
          {
            data: null,
            orderable: false,
            render : function(data, type, row, meta){
                btn_html = `
                    <span>文件尾</span><input class="input-num" type="text" value="200" style="width:60px;margin:0 2px 0 2px;" ><span>行</span>
                    <a target="_blank"  class="king-btn king-radius king-info click-btn show-btn" value="show" >查看</a>
                    <a target="_blank"  class="king-btn king-radius king-warning click-btn download-btn" value="download" >下载</a>`
                return btn_html;
            }
          }
        ],
        language:language
    });


    var t = $("#table2_demo4").DataTable();  // 获取datatables对象
    // 绑定查看事件按钮
    $("#table2_demo4 tbody").on('click', 'a.show-btn', function(){
        var row = t.row( $(this).parents('tr') ),  // 获取按钮所在的行
          data = row.data();
        var params_detail = '?project_id='+ $('#project_id').val() +
                 '&env_id=' + $('#env_id').val() +
                 '&app_id=' + $('#app_id').val() +
                 '&ip='+ $('#ip').val() +
                 '&logdir_id=' + $('.select-log').val() +
                 '&server_type=' + $('#server_type').val() +
                 '&server_id=' + $('#server_id').val() +
                 '&file_name=' + data.file +
                 '&action=' + 'log_show' +
                 '&line_num=' + $(this).parent().find('.input-num').val();
        $(this).attr('href', '/op/getShowLogDetail/' + params_detail);
    });

    // 绑定下载事件按钮
    $("#table2_demo4 tbody").on('click', 'a.download-btn', function(){
        var row = t.row( $(this).parents('tr') ),  // 获取按钮所在的行
          data = row.data();
//        $(this).attr('href', '/op/download_log/');
        $.ajax({                             // 提交数据表单
            type:'GET',
            url : '/op/downloadlog/',
            data : {
                project_id: $('#project_id').val(),
                env_id: $('#env_id').val(),
                app_id: $('#app_id').val(),
                ip: $('#ip').val(),
                logdir_id: $('.select-log').val(),
                server_type: $('#server_type').val(),
                server_id: $('#server_id').val(),
                file_name: data.file,
                action: 'downloadlog'
            },
            beforeSend:function(jqXR, settings){
                waitDialog.show();
            },
            success:function(data){
                waitDialog.close();
                console.log(data);
                window.open(data);
            },
            error : function(XMLHttpRequest, textStatus, errorThrown) {
                waitDialog.close();
                error('获取日志文件失败！，错误信息:' + errorThrown);
            },
        });

    });


    /* 点击切换日志目录获取日志信息 */
    $('#ok').bind('click', function(e){

        // 重新获取表格数据
        var t = $("#table2_demo4").DataTable();
        var params = '?project_id='+ $('#project_id').val() +
                        '&env_id=' + $('#env_id').val() +
                        '&app_id=' + $('#app_id').val() +
                        '&ip='+ $('#ip').val() +
                        '&logdir_id='+ $('.select-log').val() +
                        '&server_type=' + $('#server_type').val() +
                        '&server_id=' + $('#server_id').val();
        var ajax_url ='/op/getLogInfo/';
        t.ajax.url(ajax_url + params).load();
    });

//    function loaddatasuccess(){
//        $('a[name="show"]').bind('click', function(e){             // 查看日志
//            var _this = $(this);
//            var id = $('#id').val();
//            var dirname = $.trim($('.select-log').find('option:selected').text());
//            var logfilename = $.trim(_this.parent().parent().find('.filename').text());
//            var rownum = _this.parent().find('input[name="line"]').val();
//            if (!(/(^[1-9]\d*$)/.test(rownum))){
//                _this.parent().find('input[name="line"]').css({
//                    'border': '2px solid red',
//                });
//                setTimeout(function(){
//                    _this.parent().find('input[name="line"]').css({
//                        'border': '1px solid #ccc',
//                    });
//                }, 2000);
//                return
//            }else{
//                _this.attr('href', '/show/showlog/?id='+ id +
//                                    '&dirname=' + dirname +
//                                    '&logfilename='+ logfilename +
//                                    '&rownum=' + rownum);
//            }
//        });

        /* 下载点击 */
//        $('a[name="download"]').bind('click', function(e){
//            var _this = $(this)
//            var id = $('#id').val();
//            var dirname = $.trim($('.select-log').find('option:selected').text());
//            var logfilename = $.trim(_this.parent().parent().find('.filename').text());
//            //_this.attr('href', '/show/showlog/?id='+ id + '&dirname=' + dirname + '&logfilename='+logfilename + '&rownum='+rownum);
//            $.ajax({                             // 提交数据表单
//                type:'GET',
//                url : '/show/downloadlog/',
//                data : {
//                    id : id,
//                    dirname : dirname,
//                    logfilename : logfilename
//                },
//                beforeSend:function(jqXR, settings){
//                    $.messager.progress();
//                },
//                success:function(data){
//                    $.messager.progress('close');
//                    console.log(data);
//                    window.open(data);
//                },
//                error : function(XMLHttpRequest, textStatus, errorThrown) {
//                    $.messager.progress('close');
//                    $.messager.show({
//                        title:'提示',
//                        msg:'获取日志文件失败！，错误信息：' + errorThrown,
//                        showType: 'slide',
//                        timeout: 3000
//                    });
//                },
//            });
//        });
//    }
});