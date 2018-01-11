$(function(){

    var waitDialog = dialog({   // 加载对话框
        width: 200,
        content: '<img class="mr5" src="https://magicbox.bkclouds.cc/static_api/v3/components/loading1/images/loading_2_16x16.gif">请稍后，加载中...'
    });

    var base_path = $('input[name="base_path"]').val();
    var selected_full_dir = '';
    var selected_full_file = '';
    var selected_node_id = '';

    $('#click_upload').bind('click', function(e){
        var form_data = new FormData();  // 对象类型
        var file_info = $('#file_upload')[0].files[0];
        form_data.append('file', file_info);
        if(file_info == undefined)  { // 判断是否有附件
            error('你没有选择任何文件');
            return;
        }
        $.ajax({
            type:'POST',
            url : '/op/dealUploadFile/?dir=' + selected_full_dir,
            data: form_data,
            processData: false,
            contentType: false,
            beforeSend:function(jqXR, settings){
                waitDialog.show();
            },
            success:function(data){
                waitDialog.close();
                success('上传成功！');
            }
        });
    });


    $('#plugin11_demo7').jstree({
        "core": {
            "check_callback": true,
            'data': {
    //            "url": function (node) {
    //                return node.id === '#' ?
    //                    'ajax_demo_roots.json' : 'ajax_demo_children.json';
    //            }
                'url' : '/op/getAppDirs/',
                'data' : function (node) {
    //                console.log(node);
                }
            }
        },
        // 配置节点类型
        "types": {
            "folder": {
                "icon": "fa fa-folder",
                "valid_children": ["file"]
            },
            "file": {
                "icon": "fa fa-file",
                "valid_children": []
            }
        },
        // 配置右键菜单
        "contextmenu": {
            "items": function (node) {
                var tmp = $.jstree.defaults.contextmenu.items();
                delete tmp.create.action;
                delete tmp.ccp; //删除复制和粘贴功能

                //重命名配置
                tmp.rename.label = '重命名';
                tmp.rename.icon = 'fa fa-pencil-square-o';
                tmp.rename.action = function(data){
                    console.log(data);
                    var inst = $.jstree.reference(data.reference);
                    var obj = inst.get_node(data.reference);
                    var objName = obj.text;
                    var old_full_dir_file = get_full_path(obj);
                    console.log("old_full_dir_file:", old_full_dir_file);
                    inst.edit(obj, objName, function(data){
                        var newName = data.text;
                        data.id = 'new_node';
                        var new_full_dir_file = get_full_path(data);
    //                    console.log(data);
                        console.log("new_full_dir_file:", new_full_dir_file);
                        ajax_rename_dir_or_file(old_full_dir_file, new_full_dir_file);
                    });
                }

                //删除配置
                tmp.remove.label = '删除';
                tmp.remove.icon = 'fa fa-trash-o';
                tmp.remove.action = function(data){
                    var inst = $.jstree.reference(data.reference);
                    var obj = inst.get_node(data.reference);
                    inst.delete_node(obj);
    //                console.log('删除');
                    var full_dir_file = get_full_path(obj);
    //                console.log("full_folder:" + full_dir_file);
    //                console.log("type:" + obj.type[0]);
                    ajax_remove_dir_or_file(obj.type[0], full_dir_file);
                }

                //创建配置
                tmp.create.label = '操作';
                tmp.create.icon = 'fa fa-plus-square ';
                tmp.create.submenu = {
                    create_folder: {
                        separator_after: false,
                        label: "新建目录",
                        icon: "fa fa-folder",
                        action: function (data) {
                            var inst = $.jstree.reference(data.reference);
                            var obj = inst.get_node(data.reference);
                            inst.create_node(obj, {
                                type: "default",
                                icon: "fa fa-folder",
                            }, "last", function (new_node) {
    //                            console.log('创建成功');
                                setTimeout(function () {
                                    inst.edit(new_node, 'new_folder', function(){
                                        var full_folder = get_full_path(new_node);
                                        ajax_create_folder(full_folder); //  ajax create folder
                                    });
                                }, 0);
                            });
                        }
                    },
                };
                //如果选中文件，则不显示创建操作
                if (this.get_type(node) == "file") {
                    delete tmp.create;
                }
                return tmp;
            }
        },
        'unique': {
            'duplicate': function (name, counter) {
                return name + ' ' + counter;
            }
        },
        'plugins': ['state', 'dnd', 'types', 'contextmenu', 'unique', 'changed']
    }).on('changed.jstree', function (e, data) {
        if(data && data.selected && data.selected.length) {
//            console.log(data.node.text);
            if (data.node.type == 'file'){         // 文件
                selected_full_dir = '';
                $('.file-div').css('display', 'none');
                var full_file = get_full_path(data.node);
                selected_full_file = full_file;
                ajax_get_file_content(full_file);
            }else{                                 // 是目录
                var full_dir = get_full_path(data.node);
                selected_full_dir = full_dir;
                selected_node_id = data.node.id;
                $('.file-div').css('display', 'block');
                $('#textarea_content').val('');
            }
        }

    });

    $('#edit').bind('click', '#textarea_content', function(e){     // 编辑
        $('#textarea_content').attr("readOnly", false);
        $('#textarea_content').css('background', '#fff');
    });

    $('#save').bind('click', '#textarea_content', function(e){
        var new_content = $('#textarea_content').val();
        ajax_save_file_content(selected_full_file, new_content);
    });

    $('#cancel').bind('click', '#textarea_content', function(e){
        ajax_cancel_file_edit(selected_full_file);
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
    function get_full_path(node){    // 获取树节点文件或者目录的全路径
        var instance = $('#plugin11_demo7').jstree(true);  // 树节点对象
        var full_file = '';
        for (var i=0;i<node.parents.length;i++){
            var id = node.parents[i];
            if (id != '#'){
                full_file = instance.get_node(id).text + '/' + full_file;
            }
        };
        full_file = full_file  + node.text
        return full_file
    }

    function ajax_create_folder(full_folder){  // sftp 服务器上创建目录
        $.ajax({
            type:'POST',
            url : '/op/sshCreateFolder/',
            data: {
                base_path: base_path + '/',
                folder : full_folder
            },
            dataType : 'json',
            beforeSend:function(jqXR, settings){
                waitDialog.show();
            },
            success:function(data){
                waitDialog.close();
                if (data == true){
                    success('创建并命名成功！');
                }else{
                    error('创建并命名失败！');
                }
            }
        });
    }

    function ajax_get_file_content(full_file){   // 获取文件内容显示在页面
        $.ajax({
            type:'POST',
            url : '/op/getFileContent/',
            data: {
                full_file : base_path + '/' + full_file
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

    function ajax_cancel_file_edit(full_file){   // 取消编辑页面
        $.ajax({
            type:'POST',
            url : '/op/getFileContent/',
            data: {
                full_file : base_path + '/' + full_file
            },
            dataType : 'json',
            beforeSend:function(jqXR, settings){
                waitDialog.show();
            },
            success:function(data){
                waitDialog.close();
                success('取消成功！');
                $('#textarea_content').val(data);
                $('#textarea_content').attr('readOnly', true);
                $('#textarea_content').css('background', '#eee');
            }
        });
    }

    function ajax_save_file_content(full_file, content){   // ajax 保存文件内容
        $.ajax({
            type:'POST',
            url : '/op/saveFileContent/',
            data: {
                full_file : base_path + '/' + full_file,
                content : content
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

    function ajax_remove_dir_or_file(type, dir_file){
        $.ajax({
            type:'POST',
            url : '/op/removeDirOrFile/',
            data: {
                type : type,
                dir_file : base_path + '/' + dir_file
            },
            dataType : 'json',
            beforeSend:function(jqXR, settings){
                waitDialog.show();
            },
            success:function(data){
//                console.log(data);
                waitDialog.close();
                if (data == true){
                    success('删除成功！');
                }else{
                    error('删除失败！');
                }

            }
        });
    }

    function ajax_rename_dir_or_file(old_dir_file, new_dir_file){
        $.ajax({
            type:'POST',
            url : '/op/renameDirOrFile/',
            data: {
                old_dir_file : base_path + '/' + old_dir_file,
                new_dir_file : base_path + '/' + new_dir_file
            },
            dataType : 'json',
            beforeSend:function(jqXR, settings){
                waitDialog.show();
            },
            success:function(data){
                waitDialog.close();
                success('重命名成功！');
                var instance = $('#plugin11_demo7').jstree(true);  // 树节点对象
                instance.refresh();
            }
        });
    }

});