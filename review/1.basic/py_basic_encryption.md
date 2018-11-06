
# 背景
在实际项目实施中，会编写很多在服务器执行的作业脚本。程序中凡是涉及到数据库链接、操作系统用户链接、IP地址、主机名称的内容都是敏感信息。在纯内网系统中往因为开发时间紧迫，往往都直接将这些敏感信息明文方式写在脚本中了。
稍微规范一点的，创建一个通用的config文件，将所有这类敏感信息记录在这个文件中，脚本以读取文件方式获取这些信息。这种方式的好处是脚本不用在应用迁移、灾备部署的时候再起不同的版本，尤其是大数据平台作业运行的脚本，如果是需要做灾备集群，这种方式可以减少生产变更时的人工干预操作。但是这种方式仍不能解决安全性的问题，只要config文件泄露，那么平台会非常危险。
因此在这个config文件的基础上，对其进行改造，实现对内容的加密，而脚本使用时再对其进行解密。因此要求有一个程序能对文本内容进行加密，也能进行反向解密。
不可逆的加密方法使用最多的就是md5加密算法，我们一般用来检验文件的完整和安全性，不适用这个场景。
使用python语言对文本内容进行加解密有多种方式，从网上搜索结果看主要有以下几种：
# 1.方法一 使用base64转编码
Base64是一种用64个字符来表示任意二进制数据的方法。
用记事本打开exe、jpg、pdf这些文件时，我们都会看到一大堆乱码，因为二进制文件包含很多无法显示和打印的字符，所以，如果要让记事本这样的文本处理软件能处理二进制数据，就需要一个二进制到字符串的转换方法。Base64是一种最常见的二进制编码方法。
Base64的原理很简单，首先，准备一个包含64个字符的数组：
`['A', 'B', 'C', ... 'a', 'b', 'c', ... '0', '1', ... '+', '/']`
然后，对二进制数据进行处理，每3个字节一组，一共是3x8=24bit，划为4组，每组正好6个bit,得到4个数字作为索引，然后查表，获得相应的4个字符，就是编码后的字符串。
所以，Base64编码会把3字节的二进制数据编码为4字节的文本数据，长度增加33%，好处是编码后的文本数据可以在邮件正文、网页等直接显示。
如果要编码的二进制数据不是3的倍数，最后会剩下1个或2个字节怎么办？
Base64用\x00字节在末尾补足后，再在编码的末尾加上1个或2个=号，表示补了多少字节，解码的时候，会自动去掉。

## Python内置的base64可以直接进行base64的编解码：
```
import base64
userPassword="sunlinemdp201810"
unkownPassword=base64.b64encode(bytes(userPassword,'utf-8'))
print("加密后："+str(unkownPassword,'utf-8'))
kownPassword=str(base64.b64decode(unkownPassword),'utf-8')
print('解密后：'+kownPassword)
```
>补充说明：python3中对字符串加解密的方法 base64.encodestring('test') 不能用 因此只能采用bytes方法然后中间进行格式转换

>由于标准的Base64编码后可能出现字符+和/，在URL中就不能直接作为参数，所以又有一种"url urlsafe_b64encode"的base64编码方法，实现对+和/的转码，在现在使用的版本中这个功能已经整合在b64encode方法中了 
```
userPassword="sunlinemdp201810"
unkownPassword=base64.b64encode(bytes(userPassword,'utf-8'))
print("加密后："+str(unkownPassword,'utf-8'))
unkownPassword=base64.urlsafe_b64encode(bytes(userPassword,'utf-8'))
print("解密后："+str(unkownPassword,'utf-8'))
base64.urlsafe_b64decode(unkownPassword)
```

# 2.方法二 win32com.client
样例代码如下：
```
import win32com.client
def encrypt(key,content): # key:密钥,content:明文
    EncryptedData = win32com.client.Dispatch('CAPICOM.EncryptedData')
    EncryptedData.Algorithm.KeyLength = 5
    EncryptedData.Algorithm.Name = 2
    EncryptedData.SetSecret(key)
    EncryptedData.Content = content
    return EncryptedData.Encrypt()
def decrypt(key,content): # key:密钥,content:密文
    EncryptedData = win32com.client.Dispatch('CAPICOM.EncryptedData')
    EncryptedData.Algorithm.KeyLength = 5
    EncryptedData.Algorithm.Name = 2
    EncryptedData.SetSecret(key)
    EncryptedData.Decrypt(content)
    str = EncryptedData.Content
    return str

s1 = encrypt('sunline', 'hello world')
s2 = decrypt('sunline', s1)
print s1,s2
 
```
win32com是python操作windows程序的第三方包，放在服务器上使用不太合适。

# 3.方法三 PyCrypto
一个极好的用于信息安全的python库，包括所有主流算法。
具体可以参考：
附[pycrypto调用方法](https://www.dlitz.net/software/pycrypto/api/current/)

## 服务器文件加密实现
现在假定要对一个存储各类ip、账户、密码的global.properties文件进行加密，同时，支持在读取时进行解密。
global.properties的内容假定如下图所示：
```
#ORACLE
database.ora10g.type=ORACLE
database.ora10g.name=ora10g
database.ora10g.ip=192.168.1.113
database.ora10g.port=10000
database.ora10g.username=dw
database.ora10g.password=Oracle
#HIVE
database.cm.type=HIVE
database.cm.name=cmr
database.cm.ip=192.168.1.113
database.cm.port=10000
database.cm.username=mdp
database.cm.password=mdp
#OS
server.host.type=LINUX
server.host.ip=192.168.1.113
server.host.port=22
server.host.username=dw
server.host.password=dw
```
每一行使用等号将信息分为两段，等号左边是信息项名称，等号右边是信息项具体的内容，我们要对信息项的具体的内容进行加密。
首先做需求分析，我们的需求可以拆分为以下几个：
1. 实现对指定字符串内容基于某个密钥的加解密内容输出
2. 读取指定加密配置文件，根据信息项名称读取指定内容后加解密输出
3. 读取指定配置文件，对文件内每一行信息项的具体内容进行加解密后生成新的加解密后的配置文件

第二步做程序设计，我是从功能上进行拆分设计：
基本功能包括：    
2. 加密解密      
3. 获取文件
4. 文件指定内容读取 
5. 运行日志 --后续--
6. 异常处理 --后续-- 

交互操作包括：
1. 参数读取解析
2. 具体功能实现，输出结果或生成文件

输入输出设计：
1. 输入：  功能类型 -d  对应 四种功能需求
2. 输入：  密钥 -k    密钥内容
3. 输入：  加密内容或解密内容 -c 对应功能2 
4. 输入：  配置文件路径名称  -f 对应功能 234
5. 输入：  信息项内容  -i    对应功能4
6. 输出：  加解密文   对应功能 1 4 
7. 输出：  文件路径及名称  对应功能 2 3 

第三步，首先根据他人提供的方法做了一个对具体字符串进行加解密的类，唯一多做的处理就是对加密使用的密钥多了一个base64编码的过程，文件保存为optcrypt.py：
```
#coding: utf8
'''
实现对指定字符串内容基于某个密钥的加解密内容输出
密钥使用base64多加一层处理

version: v0.0.1
author:  Duwj
date: 2018-10-24
'''

import sys
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import base64

class optcrypt():
    def __init__(self, key):
        self.key = str(base64.b64decode(key))
        self.mode = AES.MODE_CBC
        #self.iv = Random.new().read(AES.block_size)
    #加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def aesencrypt(self, text):

        #密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        cipher = AES.new(self.key, self.mode, self.key)
        #cipher=AES.new(bytes(self.key), self.mode,Random.new().read(AES.block_size))

        #加密文本text必须为16的倍数
        add = 16 - (len(text) % 16)
        text = text + ('\0' * (16 - (len(text) % 16)))
        self.ciphertext = cipher.encrypt(text)
        #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        #所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)
     
    #解密   
    def aesdecrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        #16进制转回后解密
        plain_text = cryptor.decrypt(a2b_hex(text))

        #rstrip()去掉补的空格
        return plain_text.rstrip('\0')


if __name__ == '__main__':
    #设置环境编码
    reload(sys)
    sys.setdefaultencoding('utf8')
    #测试
    pc = optcrypt('c3VubGluZW1kcDIwMTgxMQ==') 
    e = pc.aesencrypt("duwj") 
    d = pc.aesdecrypt("d518cdd30b854b84f5aa7c5511e03e38") 
    print "info:duwj,encrypt:"+e+",decrypt:"+d      
```
然后就是依托这个基础的字符串加解密类，实现对字符串、文件、信息项的加解密功能，在这个过程中没有对复杂的properties结构进行解析，单纯的使用`=`实现信息项和密文内容的分离，文件保存为server.py:
```
#!bin/python
#-*- coding: UTF-8 -*-

'''
脚本功能：
         1. 实现对指定字符串内容基于某个密钥的加解密内容输出
         2. 读取指定加密配置文件，根据信息项名称读取指定内容后加解密输出
         3. 读取指定配置文件，对文件内每一行信息项的具体内容进行加解密后生成新的加解密后的配置文件

version: v0.0.1
author:  Duwj
date: 2018-11-05
'''

import os
import sys
import getopt 
from optcrypt import optcrypt

#字符串加解密
def stringCrpyt(func_name,value):
    if func_name =="se":
        crpyt_value=pc.aesencrypt(value)
    else:
        crpyt_value=pc.aesdecrypt(value)
    return crpyt_value

#信息项加解密输出
def infoCrpyt(func_name,file_name,info_name):
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
        crpyt_value=pc.aesencrypt(value)
    elif func_name=="id":
        crpyt_value=pc.aesdecrypt(value)
    return  crpyt_value 

#文件加解密
def fileCrpyt(func_name,file_name):
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
                    strs=line.split('=')[0]+"="+pc.aesencrypt(line.split('=')[1])
                    write_file.write(strs+"\n")
        else:
            for line in read_file.readlines():
                line = line.strip().replace('\n', '')
                if line.find("#")!=-1:
                    write_file.write(line+"\n")
                else:
                    strs=line.split('=')[0]+"="+pc.aesdecrypt(line.split('=')[1])
                    write_file.write(strs+"\n")
    except Exception, e:
         raise e
    finally:
        read_file.close()
        write_file.close()
    return file_name+"."+func_name+"crypt"

if __name__ == "__main__":
    #设置环境编码
    reload(sys)
    sys.setdefaultencoding('utf8')
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
    #获取参数
    opts, args = getopt.getopt(sys.argv[1:], "d:k:c:f:i:")
    if len(opts)==0:
        print msg
        sys.exit(0)

    for op, value in opts:
        if op == "-d":
            func_name = value
        elif op == "-k":
            key_content = value
        elif op == "-c":
            txt_content = value
        elif op == "-f":
            file_name = value
        elif op == "-i":
            info_name = value
    #print(opts)  
    #初始化密钥
    pc = optcrypt(key_content)
    #根据功能类型执行
    if func_name in("se","sd"):
        print stringCrpyt(func_name,txt_content)
    elif func_name in ("ie","id"):
        print infoCrpyt(func_name,file_name,info_name)    
    elif func_name in ("fe","fd"):
        print fileCrpyt(func_name,file_name)
    else:
        print("there is no function named "+func_name)
    sys.exit(0)

```
注意在项目文件夹中增加一个__init__.py文件以便于脚本能识别optcrypt模块。

测试脚本test.sh：
```
#!/bin/bash

#依赖python pycrypt模块  安装这个模块的命令是 python setup.py install 
#系统必须现安装yum install python-devel
#测试加解密程序
#c3VubGluZW1kcDIwMTgxMQ== 是对 sunlinemdp201811 进行base64编码后的值 可以修改  方法为：
# 1.命令行执行 python 进入python编程环境
# 2.执行以下代码 
# import base64
# print s= base64.b64encode("sunlinemdp201811")    # 引号内为想编码的密钥文本

#帮助
python server.py
#字符串加密
python server.py -d se -k c3VubGluZW1kcDIwMTgxMQ== -c sunline
#字符串解密
python server.py -d sd -k c3VubGluZW1kcDIwMTgxMQ== -c cd3f4a3b1c4a189d3fe985495f6f963b
#文件加密
python server.py -d fe   -k c3VubGluZW1kcDIwMTgxMQ==  -f global.properties
#文件解密
python server.py -d fd   -k c3VubGluZW1kcDIwMTgxMQ==  -f global.properties.fecrypt
#信息项加密输出
python server.py -d ie  -k c3VubGluZW1kcDIwMTgxMQ==  -f global.properties -i database.ora10g.username
#信息项解密输出
python server.py -d id  -k c3VubGluZW1kcDIwMTgxMQ==  -f global.properties.fecrypt -i database.ora10g.username




#shell中获取python输出值的方法：
outputString=`python server.py -d ie  -k c3VubGluZW1kcDIwMTgxMQ==  -f global.properties -i database.ora10g.username`
echo outputString:${outputString}
outputFile=`python server.py -d fe   -k c3VubGluZW1kcDIwMTgxMQ==  -f global.properties`
echo outputFile:$outputFile


```

后续会对脚本进行内容补充，主要是增加一些之前为了功能实现而忽略的异常处理和日志登记的内容。
附[加密算法介绍](https://blog.csdn.net/kamaliang/article/details/6690979)

