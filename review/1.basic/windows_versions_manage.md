
1.windows
进入python2的安装路径 C:\Python27
修改python.exe，重命名为python2.exe
正常添加python的path环境变量 

想运行python2.7  执行  python2 命令  
python2 -m pip install 模块名称


安装anaconda 并配置anaconda的默认的环境变量到path


C:\soft\Anaconda3
C:\soft\Anaconda3\Scripts
C:\soft\Anaconda3\Library\bin 



然后，执行python2 进入2.7.13
执行python 进入3.6.5
C:\Users\DELL>python2
Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:53:40) [MSC v.1500 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> exit()

C:\Users\DELL>python
Python 3.6.5 |Anaconda, Inc.| (default, Mar 29 2018, 13:32:41) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>

也可以反过来 因为用2.7比较多 

2.virtualenv

用来创建单独的项目依赖空间 虚拟化环境

安装
python -m pip install virtualenv  /  python2 -m pip install virtualenv 
virtualenv - -help

virtualenv -p C:\Python27 venv


