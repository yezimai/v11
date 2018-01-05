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

    /* ajax 保存文件内容 */
    function ajax_save_file_content(new_content){
        $.ajax({
            type:'POST',
            url : '/op/saveCrontabContent/',
            data: {
                project_id : $('#project_id').val(),
                env_id :  $('#env_id').val(),
                app_id :  $('#app_id').val(),
                server_type: $('#server_type').val(),
                server_id: $('#server_id').val(),
                content : new_content
            },
            dataType : 'json',
            beforeSend:function(jqXR, settings){
                waitDialog.show();
            },
            success:function(data){
                waitDialog.close();
                if (data == true){
                    success('保存文件成功！');
                    $('#textarea_content').attr('readOnly', true);
                    $('#textarea_content').css('background', '#eee');
                }else{
                    error('保存文件失败！');
                }
            }
        });
    }

    function ajax_get_file_content(){   // 获取文件内容显示在页面
        $.ajax({
            type: 'POST',
            url : '/op/getCrontabContent/',
            data: {
                project_id : $('#project_id').val(),
                env_id :  $('#env_id').val(),
                app_id :  $('#app_id').val(),
                server_type: $('#server_type').val(),
                server_id: $('#server_id').val(),
            },
            dataType : 'json',
            beforeSend:function(jqXR, settings){
                waitDialog.show();
            },
            success:function(data){
                waitDialog.close();
                $('#textarea_content').val(data);
            }
        });
    }


    /* 编辑按钮点击 */
    $('#cron_edit').bind('click', function(e){
        $('#textarea_content').attr("readOnly", false);
        $('#textarea_content').css({
            'background': '#fff'
        });
    });

    /* 保存按钮点击  */
    $('#cron_save').bind('click', function(e){
        var new_content = $('#textarea_content').val();
        ajax_save_file_content(new_content);
    });

    /* 取消按钮点击  */
    $('#cron_cancel').bind('click', function(e){
        ajax_get_file_content();
    });

});