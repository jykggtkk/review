linux下python多版本环境设置（数据科学研究依赖环境安装）
经常遇到这样的情况：
系统自带的Python是2.6，自己需要Python 2.7中的某些特性；
系统自带的Python是2.x，自己需要Python 3.x；
此时需要在系统中安装多个Python，但又不能影响系统自带的Python，即需要实现Python的多版本共存。
pyenv就是这样一个Python版本管理器，除此之外，还可以使用virtualenv创建独立的纯净虚拟环境
# 一、pyenv安装
使用vm虚拟机安装centos7系统
  1)默认安装方式使用NAT网络连接方式  确认IP后可以直接实现宿主机和虚拟机的互联，也能直接连接互联网
  2)在centos安装配置界面中的软件选择界面，需要选择带有GHOME界面的配置，否则安装后的系统是不带界面的，使用不便
## 1.相关依赖软件安装
  1)安装GCC  
`yum install gcc`
  2)安装git,需要用git获取pyenv的代码
`yum -y install git`
  3)其他工具依赖
`yum install -y readline readline-devel readline-static openssl openssl-devel openssl-static sqlite-devel bzip2-devel bzip2-libs`
## 2.pyenv获取及配置
  1)获取pyenv,安装位置选择在root根目录下，使用.隐藏目录，并设置环境变量。这里设置为root用户可用了，其实可以基于其他用户clone一份自己用的独立环境
`git clone https://github.com/yyuu/pyenv.git ~/.pyenv`
  2)设置相关环境变量，使pyenv生效
```
echo 'export PYENV_ROOT="/root/.pyenv"' >>  ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
source ~/.bash_profile
```
# 二、pyenv的使用
## 1.安装不同版本的python
```
pyenv install --list #查看可安装的python版本
pyenv install 3.6.5  #安装python3.6.5
pyenv uninstall 3.6.5 #卸载python3.6.5
```
### 补充：网络问题导致安装缓慢或无法进行
如anaconda之类大容量的版本，由于网络的问题，总是连接中断，安装失败。此时可以先从官方网站下载安装包，然后放在`~/.pyenv/cache`文件中(注意cache是个文件），然后执行`pyenv install 此版本`，pyenv会自动先从此文件夹中搜索
```
wget https://www.python.org/ftp/python/2.7.15/Python-2.7.15.tar.xz
cp Python-2.7.15.tar.xz  ~/.pyenv/cache
pyenv install 2.7.15
```    
## 2.更新pyenv
安装完之后，需要更新一下才能看到已经安装的版本
```
pyenv rehash
pyenv versions #查看已经安装好的版本，带*号的为当前使用的版本
```
## 3.选择版本
`pyenv global 3.6.5 #设置全局版本，即系统使用的将是此版本`
这样在任意目录下执行python命令进入的都是3.6.5环境 
`pyenv local 2.7.15  #当前目录下的使用版本，有点类似virtualenv`
在当前目录下执行 python 进入的都是2.7.15环境  
`pyenv global  system #重新设置全局版本为系统的版本`
而除了root用户（设置pyenv的用户）外,其他用户使用的仍是系统默认的2.7.5版本的python
# 三、virtualenv安装及使用
## 1.python virtualenv安装
可以直接使用pip安装virtualenv也行，但是通过pyenv插件的形式安装virtualenv的虚拟环境更加方便。
```
git clone https://github.com/pyenv/pyenv-virtualenv.git
cd pyenv-virtualenv/
./install.sh
```
安装virtualenv插件，安装在主文件夹下的.pyenv文件夹中。
```
git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
./install.sh
``` 
## 2.创建虚拟环境
创建一个2.7.15的虚拟环境
```
pyenv virtualenv 2.7.15 py27
source ~/.bash_profile #执行这一步使当前用户环境都使用这个virtualenv环境
```
这条命令在本机上创建了一个名为env271的python虚拟环境，这个环境的真实目录位于：`~/.pyenv/versions/`
注意，命令中的 ‘2.7.15’ 必须是一个安装前面步骤已经安装好的python版本， 否则会出错。
可以通过`pyenv versions` 命令来查看当前的虚拟环境，列表中有一个 py27。

## 3.切换和使用新的python虚拟环境：
执行以下命令
`pyenv activate py27`
就能切换为`py27`这个版本的虚拟环境。
通过输入`python --version`查看现在版本，可以发现处于虚拟环境下了。
如果要切换回系统环境， 运行这个命令即可
`pyenv deactivate`
删除这个虚拟环境,只要直接删除它所在的目录就好：
`rm -rf ~/.pyenv/versions/py27/`
或者使用卸载命令：
`pyenv uninstall py27`

# 四、jupyter notebook 安装
## 1.安装数据科学依赖的软件
```
yum install bzip2 -y
yum groupinstall "Development Tools" -y
```
## 2.使用pyenv进入python3.6.5环境
在python3环境下实现数据科学的框架搭建
```
pyenv local 3.6.5
python --version
pip install ipython jupyter notebook
```
## 3.jupyter配置
jupyter安装完成后，验证命令是否可用并生成一个jupyter的配置文件。（确保pyenv环境正确）
`jupyter notebook --generate-config`
# 4.安全设置
为了比较安全的访问服务器资源，可以设置登录密码和设置https来实现安全登录。有条件可以通过安全认证中心来发放秘钥和认证。
首先打开ipython，生成sha1的密码，如下：
```
from notebook.auth import passwd
passwd()
#Enter password   sunline
#output sha1:5862585fb33e:afeb36aa85d02e0c37b0de7d7e6a4bc766e9fa6c
```
然后生成一个自签名认证的key，如下：
`openssl req -x509 -nodes -days 365 -newkey rsa:4096 -keyout jkey.key -out jcert.pem`
最后修改增加配置文件中的内容：
```
vim /home/user/.jupyter/jupyter_notebook_config.py
c.NotebookApp.password = 'sha1:<your-sha1-hash-value>'
c.NotebookApp.port = 8888
c.NotebookApp.ip = '192.168.245.128'
c.NotebookApp.open_browser = False
c.NotebookApp.certfile = '/home/user/jcert.pem'
c.NotebookApp.keyfile = '/home/user/jkey.key'
 ```
## 5.jupyter notebook使用
由于jupyter使用的8888作为默认端口，需要把端口给开放并重启防火墙。执行如下命令
`firewall-cmd --zone=public --add-port=8888/tcp --permanent`
然后重启防火墙
`systemctl restart firewalld.service`
到这里所有的安装和基本的设置都已经完成，直接在命令行输入：`jupyter notebook`.就可以启动进程。

## 6.实现后台运行并输出日志
创建`start.sh` 脚本内容为 
```
nohup  start.sh  >> output.log 2>&1 &
nohup  /root/jupyterNotebook/start.sh  >> /root/jupyterNotebook/output.log 2>&1 &
```
