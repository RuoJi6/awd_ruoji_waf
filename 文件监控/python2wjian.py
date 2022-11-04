# -*- coding: utf-8 -*-
import os
import re
import hashlib
import shutil
import ntpath
import time
import sys

# 设置系统字符集，防止写入log时出现错误
reload(sys)
sys.setdefaultencoding('utf-8')
CWD = os.getcwd()
FILE_MD5_DICT = {}      # 文件MD5字典
ORIGIN_FILE_LIST = []

# 特殊文件路径字符串
Special_path_str = 'drops_B0503373BDA6E3C5CD4E5118C02ED13A' #drops_md5(icecoke1024)
bakstring = 'back_CA7CB46E9223293531C04586F3448350'          #bak_md5(icecoke1)
logstring = 'log_8998F445923C88FF441813F0F320962C'          #log_md5(icecoke2)
webshellstring = 'webshell_988A15AB87447653EFB4329A90FF45C5'#webshell_md5(icecoke3)
difffile = 'difference_3C95FA5FB01141398896EDAA8D667802'          #diff_md5(icecoke4)

Special_string = 'drops_log'  # 免死金牌
UNICODE_ENCODING = "utf-8"
INVALID_UNICODE_CHAR_FORMAT = r"\?%02x"

# 文件路径字典
spec_base_path = os.path.realpath(os.path.join(CWD, Special_path_str))
Special_path = {
    'bak' : os.path.realpath(os.path.join(spec_base_path, bakstring)),
    'log' : os.path.realpath(os.path.join(spec_base_path, logstring)),
    'webshell' : os.path.realpath(os.path.join(spec_base_path, webshellstring)),
    'difffile' : os.path.realpath(os.path.join(spec_base_path, difffile)),
}

def isListLike(value):
    return isinstance(value, (list, tuple, set))

# 获取Unicode编码
def getUnicode(value, encoding=None, noneToNull=False):

    if noneToNull and value is None:
        return NULL

    if isListLike(value):
        value = list(getUnicode(_, encoding, noneToNull) for _ in value)
        return value

    if isinstance(value, unicode):
        return value
    elif isinstance(value, basestring):
        while True:
            try:
                return unicode(value, encoding or UNICODE_ENCODING)
            except UnicodeDecodeError, ex:
                try:
                    return unicode(value, UNICODE_ENCODING)
                except:
                    value = value[:ex.start] + "".join(INVALID_UNICODE_CHAR_FORMAT % ord(_) for _ in value[ex.start:ex.end]) + value[ex.end:]
    else:
        try:
            return unicode(value)
        except UnicodeDecodeError:
            return unicode(str(value), errors="ignore")

# 目录创建
def mkdir_p(path):
    import errno
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

# 获取当前所有文件路径
def getfilelist(cwd):
    filelist = []
    for root,subdirs, files in os.walk(cwd):
        for filepath in files:
            originalfile = os.path.join(root, filepath)
            if Special_path_str not in originalfile:
                filelist.append(originalfile)
    return filelist

# 计算机文件MD5值
def calcMD5(filepath):
    try:
        with open(filepath,'rb') as f:
            md5obj = hashlib.md5()
            md5obj.update(f.read())
            hash = md5obj.hexdigest()
            return hash
# 文件MD5消失即为文件被删除，恢复文件
    except Exception, e:
        print u'[*] 文件被删除 : ' + getUnicode(filepath)
    shutil.copyfile(os.path.join(Special_path['bak'], ntpath.basename(filepath)), filepath)
    for value in Special_path:
        mkdir_p(Special_path[value])
        ORIGIN_FILE_LIST = getfilelist(CWD)
        FILE_MD5_DICT = getfilemd5dict(ORIGIN_FILE_LIST)
    print u'[+] 被删除文件已恢复！'
    try:
         f = open(os.path.join(Special_path['log'], 'log.txt'), 'a')
         f.write('deleted_file: ' + getUnicode(filepath) + ' 时间: ' + getUnicode(time.ctime()) + '\n')
         f.close()
    except Exception as e:
         print u'[-] 记录失败 : 被删除文件: ' + getUnicode(filepath)
         pass

# 获取所有文件MD5
def getfilemd5dict(filelist = []):
    filemd5dict = {}
    for ori_file in filelist:
        if Special_path_str not in ori_file:
            md5 = calcMD5(os.path.realpath(ori_file))
            if md5:
                filemd5dict[ori_file] = md5
    return filemd5dict

# 备份所有文件
def backup_file(filelist=[]):
    for filepath in filelist:
        if Special_path_str not in filepath:
            shutil.copy2(filepath, Special_path['bak'])

if __name__ == '__main__':
    print u'---------持续监测文件中------------'
    for value in Special_path:
        mkdir_p(Special_path[value])
    # 获取所有文件路径，并获取所有文件的MD5，同时备份所有文件
    ORIGIN_FILE_LIST = getfilelist(CWD)
    FILE_MD5_DICT = getfilemd5dict(ORIGIN_FILE_LIST)
    backup_file(ORIGIN_FILE_LIST) 
    print u'[*] 所有文件已备份完毕！'
    while True:
        file_list = getfilelist(CWD)
        # 移除新上传文件
        diff_file_list = list(set(file_list) ^ set(ORIGIN_FILE_LIST))
        if len(diff_file_list) != 0:
            for filepath in diff_file_list:
                try:
                    f = open(filepath, 'r').read()
                except Exception, e:
                    break
                if Special_string not in f:
                    try:
                        print u'[*] 查杀疑似WebShell上传文件: ' + getUnicode(filepath)
                        shutil.move(filepath, os.path.join(Special_path['webshell'], ntpath.basename(filepath) + '.txt'))
                        print u'[+] 新上传文件已删除!'
                    except Exception as e:
                        print u'[!] 移动文件失败, "%s" 疑似WebShell，请及时处理.'%getUnicode(filepath)
                    try:
                        f = open(os.path.join(Special_path['log'], 'log.txt'), 'a')
                        f.write('new_file: ' + getUnicode(filepath) + ' 时间: ' + str(time.ctime()) + '\n')
                        f.close()
                    except Exception as e:
                        print u'[-] 记录失败 : 上传文件: ' + getUnicode(e)

        # 防止任意文件被修改,还原被修改文件
        md5_dict = getfilemd5dict(ORIGIN_FILE_LIST)
        for filekey in md5_dict:
            if md5_dict[filekey] != FILE_MD5_DICT[filekey]:
                try:
                    f = open(filekey, 'r').read()
                except Exception, e:
                    break
                if Special_string not in f:
                    try:
                        print u'[*] 该文件被修改 : ' + getUnicode(filekey)
                        shutil.move(filekey, os.path.join(Special_path['difffile'], ntpath.basename(filekey) + '.txt'))
                        shutil.copyfile(os.path.join(Special_path['bak'], ntpath.basename(filekey)), filekey)
                        print u'[+] 文件已复原!'
                    except Exception as e:
                        print u'[!] 移动文件失败, "%s" 疑似WebShell，请及时处理.'%getUnicode(filekey)
                    try:
                        f = open(os.path.join(Special_path['log'], 'log.txt'), 'a')
                        f.write('difference_file: ' + getUnicode(filekey) + ' 时间: ' + getUnicode(time.ctime()) + '\n')
                        f.close()
                    except Exception as e:
                        print u'[-] 记录失败 : 被修改文件: ' + getUnicode(filekey)
                        pass
        time.sleep(2)