#!/usr/bin/python
# coding:utf8

import os
import sys
import json

def dirlist(path):
    ret = []
    try:
        filelist = os.listdir(path)
    except Exception as e:
        print("[ERROR] Catch exception: [ %s ], file: [ %s ], line: [ %s ]" %
              (e, __file__, sys._getframe().f_lineno))
        return False, ret
    else:
        for filename in filelist:
            new_file_path = os.path.join(path, filename)
            if os.path.exists(new_file_path):
                tmp_dic = {}
                if os.path.isdir(new_file_path):
                    tmp_dic['text'] = filename
                    tmp_dic['state'] = {}
                    tmp_dic['state']['opened'] = "true"
                    new_ret, new_data = dirlist(new_file_path)
                    if new_data:
                        tmp_dic['children'] = new_data
                else:
                    tmp_dic['text'] = filename
                    tmp_dic['type'] = "file"
                    tmp_dic['icon'] = "jstree-file"
                ret.append(tmp_dic)
    return True, ret


if __name__ == "__main__":
    # data = dirlist("c:/tmp")
    path = sys.argv[1]
    ret, data = dirlist(path)
    if ret == False:
        exit(1)
    print(data)
    exit(0)
