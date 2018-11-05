
由于python设计的初衷是开源的，因此py文件是可以直接看到源码的。但开发商业软件，代码加密保护就比较重要了。 
# python编译后程序
pyc文件是py文件经过编译后生成的二进制文件，因此可以发布pyc文件以隐藏源代码。pyc文件拥有更快的加载速度，执行速度没有区别。pyc是一种跨平台的字节码，pyc的内容是跟python的版本相关的，不同版本编译后的pyc文件是不同的，2.5编译的pyc文件，2.4版本的python是无法执行的。
python提供了内置的类库来实现把py文件编译为pyc文件，这个模块就是py_compile模块：
`#生成单个pyc文件`
`python -m py_compile test.py `
`python -O -m py_compile test.py `
`# -O 优化成字节码（pyo） `
`# -m 表示把后面的模块当成脚本运行 `
`#-OO 表示优化的同时删除文档字符串`
`#批量生成pyc文件`
`python -m compileall `

#程序加密
目前软件开发商对 Python 加密时可能会有两种形式，一种是对python转成的exe进行保护，另一种是直接对.py或者.pyc文件进行保护，下面将列举两种形式的保护流程。

###  1.pyexe、PyInstaller、py2app 打包软件
这些工具用于将一个Python项目打包成单个可执行的文件，对 python转exe加壳，方便（在没有Python环境的机器上）使用。但通过压缩包可以方便地得到所有pyc文件或源文件，与C/C++编译生成的可执行文件有本质上的区别，基本上是零保护。
###  2.对.py/.pyc加密
第一步，使用加壳工具对 python 安装目录下的 python.exe 进行加壳，将 python.exe 拖入到加壳工具 VirboxProtector 中，配置后直接点击加壳。
第二步，对.py/.pyc 进行加密，使用 DSProtector 对.py/.pyc 进行保护。

### 3.使用cython保护python的代码
先安装cython
`pip install cython`
然后安装python开发包 
centos系统下
`yum install python-devel` 
然后对python代码文件进行转换： 
`cython hello.py --embed   #把python代码转换成c代码`
会生成一个名为`hello.c`的c语言的源文件。
然后使用gcc编译成二进制可执行文件，这时候需要制定头文件、编译选项、链接选项：
```
gcc `python-config --cflags` `python-config --ldflags` hello.c -o hello
```
如果python版本较高的话可以使用
```
gcc `python3-config --cflags --ldflags` hello.c -o hello
```
这样代码就被编译成二进制的可执行程序了。
链接错误的话试试：
```
gcc `python-config --cflags` -o hello hello.c  `python-config --ldflags`
```
[链接问题解决参考](http://stackoverflow.com/questions/13782618/python-py-initialize-unresolved-during-compilation)
