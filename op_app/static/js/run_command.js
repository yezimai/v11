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

    // 清空输入的命令
    $('#clear').bind('click', function(e){
        $('.cmds-content').val('');
    });

    // 执行远程命令
    $('#exec').bind('click', function(e){
        var cmd_content = $('.cmds-content').val();
        console.log('cmd_content:' + cmd_content);
//        $.ajax({
//            type:'POST',
//            url : '/op/exec_cmds/',
//            data: {
//                folder : full_folder
//            },
//            dataType : 'json',
//            beforeSend:function(jqXR, settings){
//                waitDialog.show();
//            },
//            success:function(data){
//                waitDialog.close();
//                if (data == true){
//                    success('创建并命名成功！');
//                }else{
//                    error('创建并命名失败！');
//                }
//            }
//        });
    });

    // 选择最近的命令触发事件
    $('.list-group-item').bind('click', function(e){
        var _this = $(this);
        console.log(_this);
//        var content = _this.find('.list-group-item').eq(0).attr("cmds");
        var content = _this.attr('cmds');
        var value = _this.text();
        console.log('cmds:' + content);
        console.log('value:' + value);
    });

    // 选择命令执行的目录
    $('.click-dir').bind('click', function(e){
        $(this).parent().find('.click-dir').removeClass('selected');
        $(this).addClass('selected');
    });

});