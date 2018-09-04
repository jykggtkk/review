windows下，不需要像linux那样复杂的配置，能够方便的两个版本替换使用就可以了。
这样python2选择安装2.7版本，python3选择使用anaconda的版本。
通过对执行程序名称的改变来实现命令的分离：
# python2环境
进入python2的安装路径`C:\Python27`，修改`python.exe`，重命名为`python2.exe`
添加PYTHON_HOME环境变量：`C:\Python27`
在python2的path环境变量中添加:
```
%PYTHON_HOME%
%PYTHON_HOME%\Scripts
```
## 运行python2.7  
执行`python2`命令  
#python2环境下安装模块
`python2 -m pip install 模块名称`
# python3环境
安装anaconda,并配置anaconda的默认的环境变量到path:
```
C:\soft\Anaconda3
C:\soft\Anaconda3\Scripts
C:\soft\Anaconda3\Library\bin 
```
# 验证
```
C:\Users\DELL>python2
Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:53:40) [MSC v.1500 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> exit()
C:\Users\DELL>python
Python 3.6.5 |Anaconda, Inc.| (default, Mar 29 2018, 13:32:41) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
也可以反过来 因为用2.7比较多 

# virtualenv
用来创建单独的项目依赖空间 虚拟化环境

## 安装
`python -m pip install virtualenv  /  python2 -m pip install virtualenv`

# 创建虚拟环境时指定已经安装的python版本路径
`virtualenv -p C:\Python27 venv`