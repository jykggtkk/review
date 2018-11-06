#!bin/python
#-*- coding: UTF-8 -*-

'''
脚本功能：
         1. 实现对指定字符串内容基于某个密钥的加解密内容输出
         2. 读取指定加密配置文件，根据信息项名称读取指定内容后加解密输出
         3. 读取指定配置文件，对文件内每一行信息项的具体内容进行加解密后生成新的加解密后的配置文件

改成类
version: v0.0.1
author:  Duwj
date: 2018-11-05
'''

import os
import sys
import getopt 
from optcrypt import optcrypt

class server():
    def __init__(self, args):
        for op, value in args:
            if op == "-d":
                self.func_name = value
            elif op == "-k":
                self.key_content = value
            elif op == "-c":
                self.txt_content = value
            elif op == "-f":
                self.file_name = value
            elif op == "-i":
                self.info_name = value
        #初始化密钥
        self.pc = optcrypt(self.key_content)

    #字符串加解密
    def stringCrpyt(self,func_name,value):
        if func_name =="se":
            crpyt_value=self.pc.aesencrypt(value)
        else:
            crpyt_value=self.pc.aesdecrypt(value)
        return crpyt_value

    #文件加解密
    def fileCrpyt(self,func_name,file_name):
        try:
            read_file = open(file_name,'Ur')
            write_file = open(file_name+"."+func_name+"crypt",'w')
            if func_name == "fe":
                for line in read_file.readlines():
                    line = line.strip().replace('\n', '')
                    if line=="":
                        pass
                    elif line.find("#")!=-1:
                        write_file.write(line+"\n")
                    else:
                        strs=line.split('=')[0]+"="+self.pc.aesencrypt(line.split('=')[1])
                        write_file.write(strs+"\n")
            else:
                for line in read_file.readlines():
                    line = line.strip().replace('\n', '')
                    if line=="":
                        pass
                    elif line.find("#")!=-1:
                        write_file.write(line+"\n")
                    else:
                        strs=line.split('=')[0]+"="+self.pc.aesdecrypt(line.split('=')[1])
                        write_file.write(strs+"\n")
        except Exception, e:
            raise e
        finally:
            read_file.close()
            write_file.close()
        return file_name+"."+func_name+"crypt"

    #信息项加解密输出
    def infoCrpyt(self,func_name,file_name,info_name):
        value=""
        try:
            pro_file = open(file_name, 'Ur')
            for line in pro_file.readlines():
                line = line.strip().replace('\n', '')
                if info_name == line.split('=')[0]:
                    value = line.split('=')[1]
            #print value 
        except Exception, e:
            raise e
        finally:
            pro_file.close()

        if func_name == "ie":
            crpyt_value=self.pc.aesencrypt(value)
        elif func_name=="id":
            crpyt_value=self.pc.aesdecrypt(value)
        return  crpyt_value

    def run(self):
        #根据功能类型执行
        if self.func_name in("se","sd"):
            result=self.stringCrpyt(self.func_name,self.txt_content)
        elif self.func_name in ("ie","id"):
            result=self.infoCrpyt(self.func_name,self.file_name,self.info_name)    
        elif self.func_name in ("fe","fd"):
            result=self.fileCrpyt(self.func_name,self.file_name)
        else:
            result=("there is no function named "+self.func_name)
        print result 
        return result

if __name__ == "__main__":
    #设置环境编码
    reload(sys)
    sys.setdefaultencoding('utf8')
     
    #获取参数
    opts, args = getopt.getopt(sys.argv[1:], "d:k:c:f:i:")
    if len(opts)==0:
        msg='''使用说明：python server.py 
         -d [选择方法[se 字符串加密 /sd 字符串解密/ie 信息项加密/id 信息项解密/fe 文件加密/fd 文件加密]]  
         -k [16位密钥]
         -c [加密内容]
         -f [文件名称]
         -i [信息项名称]
         字符串加解密必选项： -k -c 
         信息项加解密必选项： -k -f -i
         文件加解密必选项:    -k -f 
         '''   
        print(msg)
        sys.exit(0)
    else:
        ch=server(opts)
        ch.run()

    sys.exit(0)


