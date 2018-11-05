#!/bin/bash
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

