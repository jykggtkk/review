#!bin/python
#-*- coding: UTF-8 -*-

'''
文件基本操作代码   python3代码为主  python2只做区别说明
'''
#文件打开操作
#mode参数类型说明可查表，这里不再详述，常用的就是：
#r--只读，r+ --读写（从开头），w --只写（从开头重写或创建新文件),w+ --读写（从开头重写或创建新文件)
#a --追加（文件不存在则新建）   a+ --读写，新增内容是追加方式

#python3 需要指定encoding参数  python2没有
#python2：testf = open('D:\\page\\test.py',mode='r')
testf = open('D:\\page\\test.py',mode='r', encoding='utf-8')

#读取内容
#如不指定encoding参数打开，在读取数据时会报编码错误：
#UnicodeDecodeError: 'gbk' codec can't decode byte 0xbe in position 55: illegal multibyte sequence
a=testf.readlines()
#打印每一行
for line in a:
    print(line)

#文件属性
print(testf.name) #文件名称，带路径
print(testf.closed) #文件是否关闭  trueorfalse
print(testf.encoding) #文件编码格式
print(testf.buffer)   #文件输出流 没什么用
#print(testf.softspace) #末尾是否强制加空格  python3 好像没有


#文件关闭
testf.close()

print(testf.closed)


#文件写入，就不详述了   简单的  创建文件、覆盖写入、追加写入这几种
fo = open("D:\\page\\foo.txt", "w")
fo.write( "www.runoob.com!\nVery good site!\n")
fo.close()

fo = open("D:\\page\\foo.txt", "a")
fo.write( "www.runoob.com!\nVery good site!\n")
fo.close()

#文件定位

# tell()方法获取文件内的当前位置, 换句话说，下一次的读写会发生在文件开头这么多字节之后。
fo = open("D:\\page\\foo.txt", "r+")
str = fo.read(1)
print("读取的字符串是 : ", str)
# 查找当前位置
position = fo.tell()
print("当前文件位置 : ", position)
#seek（offset [,from]）方法改变当前文件的位置。Offset变量表示要移动的字节数。From变量指定开始移动字节的参考位置。
# 把指针再次重新定位到文件开头
position = fo.seek(0, 0)
str = fo.read(1)
print("重新读取字符串 : ", str)
fo.close()
#如果from被设为0，这意味着将文件的开头作为移动字节的参考位置。如果设为1，则使用当前的位置作为参考位置。如果它被设为2，那么该文件的末尾将作为参考位置。

#较复杂的或者较少用到的一些方法:

#缓冲区刷新,什么时候下使用 还需要学习
fo = open("D:\\page\\foo.txt", "wb")
print ("文件名为: ", fo.name)
# 刷新缓冲区
fo.flush() 
fo.close()

#next() 读取下一行     python2中应该有 file.next() 方法   python3中没有
#Python 3 中的 File 对象不支持 next() 方法。 
#Python 3 的内置函数 next() 通过迭代器调用 __next__() 方法返回下一项
#在循环中，next()方法会在每次循环中调用，该方法返回文件的下一行，如果到达结尾(EOF),则触发 StopIteration

testf = open('D:\\page\\test.py',mode='r', encoding='utf-8')
#testf.next()  #python2  每执行一次返回下一行  

#python3
next(testf)
next(testf)
next(testf)
testf.close()





#这部分其实是模块os的内容
#文件重命名,如果文件已存在不会覆盖而会报错
import os 
os.rename("D:\\page\\foo.txt", "D:\\page\\foo2.txt")

#删除文件
os.remove("D:\\page\\foo2.txt")

#目录创建

#改变当前目录

#删除目录