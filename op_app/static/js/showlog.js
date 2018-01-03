$(function(){
//    alert('dddddd');
//    $('#action_table tbody').bind('click', '.btn-show', function(e){
//        alert('show');
//    });
//    $('#action_table tbody').bind('click', '.btn-download', function(e){
//        alert('download');
//    });

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

    $("#table2_demo4").dataTable({
        autoWidth: true,
        lengthChange: true,       //不允许用户改变表格每页显示的记录数
        pageLength : 10,          //每页显示几条数据
        lengthMenu: [10, 20, 40], //每页显示选项
        pagingType: 'full_numbers',
        ajax : '/op/getLogInfo/',
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
                    <a target="_blank"  class="king-btn king-radius king-info click-btn" value="show" >查看</a>
                    <a target="_blank"  class="king-btn king-radius king-warning click-btn" value="download" >下载</a>`
                return btn_html;
            }
          }
        ],
        language:language
    });


    $('#ok').bind('click', function(e){
        $.ajax({                             // 提交数据表单
            type:'POST',
            url : '/show/getDirFilesDetails/',
            data : {
                id : $('#id').val(),
                dirname : $.trim($('.select-log').find('option:selected').text()),
            },
            beforeSend:function(jqXR, settings){
                $.messager.progress();
                $('tbody').find('tr').remove();
            },
            success:function(data){
                $.messager.progress('close');
                console.log(data);
                loaddatasuccess();
            },
            error : function(XMLHttpRequest, textStatus, errorThrown) {
                $.messager.progress('close');
                $.messager.show({
                    title:'提示',
                    msg:'获取日志文件失败！，错误信息：' + errorThrown,
                    showType: 'slide',
                    timeout: 3000
                });
            },
        });
    });

    function loaddatasuccess(){
        $('a[name="show"]').bind('click', function(e){             // 查看日志
            var _this = $(this);
            var id = $('#id').val();
            var dirname = $.trim($('.select-log').find('option:selected').text());
            var logfilename = $.trim(_this.parent().parent().find('.filename').text());
            var rownum = _this.parent().find('input[name="line"]').val();
            if (!(/(^[1-9]\d*$)/.test(rownum))){
                _this.parent().find('input[name="line"]').css({
                    'border': '2px solid red',
                });
                setTimeout(function(){
                    _this.parent().find('input[name="line"]').css({
                        'border': '1px solid #ccc',
                    });
                }, 2000);
                return
            }else{
                _this.attr('href', '/show/showlog/?id='+ id + '&dirname=' + dirname + '&logfilename='+logfilename + '&rownum='+rownum);
            }
        });

        $('a[name="download"]').bind('click', function(e){
            var _this = $(this)
            var id = $('#id').val();
            var dirname = $.trim($('.select-log').find('option:selected').text());
            var logfilename = $.trim(_this.parent().parent().find('.filename').text());
            //_this.attr('href', '/show/showlog/?id='+ id + '&dirname=' + dirname + '&logfilename='+logfilename + '&rownum='+rownum);
            $.ajax({                             // 提交数据表单
                type:'GET',
                url : '/show/downloadlog/',
                data : {
                    id : id,
                    dirname : dirname,
                    logfilename : logfilename
                },
                beforeSend:function(jqXR, settings){
                    $.messager.progress();
                },
                success:function(data){
                    $.messager.progress('close');
                    console.log(data);
                    window.open(data);
                },
                error : function(XMLHttpRequest, textStatus, errorThrown) {
                    $.messager.progress('close');
                    $.messager.show({
                        title:'提示',
                        msg:'获取日志文件失败！，错误信息：' + errorThrown,
                        showType: 'slide',
                        timeout: 3000
                    });
                },
            });
        });
    }
});