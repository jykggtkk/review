# 禅道本地部署安装

利用新的项目机会进行实践。禅道的功能非常多，有些复杂，就实施项目的实际情况，大部分情况下不会用到太多的功能和流程，而且对新上手的人来说，还是应该着重于实际的管理套路流程，再看禅道中哪些功能和流程能结合起来来实现这些套路。

## 1.0 禅道安装

禅道提供了windows/linux的一键式安装包，非常简单，只需要注意会初始化的几个配置和一些启停命令就可以，没必要深入研究原理：

```
# 1.开源版安装包下载
[root@localhost ~]# cd /opt
[root@localhost opt]# wget http://dl.cnezsoft.com/zentao/9.0.1/ZenTaoPMS.9.0.1.zbox_64.tar.gz

# 2.解压
[root@localhost opt]# tar -zxvf ZenTaoPMS.9.0.1.zbox_64.tar.gz -C /opt

# 3.修改端口号
修改禅道自带apache端口：
[root@localhost opt]# /opt/zbox/zbox -ap 9000
修改禅道自带mysql端口：
[root@localhost opt]# /opt/zbox/zbox -mp 9001

# 4.禅道运行命令
[root@localhost opt]# /opt/zbox/zbox start   #命令开启Apache和Mysql
[root@localhost opt]# /opt/zbox/zbox stop    #命令停止Apache和Mysql
[root@localhost opt]# /opt/zbox/zbox restart #命令重启Apache和Mysql
[root@localhost opt]# /opt/zbox/zbox  -h     #命令来获取关于zbox命令的帮助

# 5.初始化配置
# 创建数据库账号
[root@localhost opt]# /opt/zbox/auth/adduser.sh  
This tool is used to add user to access admin
Account: admin
Password: Adding password for user admin
#注：mysql数据库的用户名：root，密码为空。应用的数据库管理用的是admin，但是为了安全，访问admin的时候需要身份验证，需要运行脚本添加账户

# 命令行登录禅道自带mysql数据库：
[root@localhost opt]# /opt/zbox/bin/mysql -u root -P 3306 -p   # 注意端口号不用改为9001
# 命令行导入备份的数据：
/opt/zbox/bin/mysql -u root -P 3306 -p zentaopro < zentao.sql
# 如果是首次安装“禅道”，此处略过；如果之前已经装有“禅道”，想导入之前的数据，则可以导入备份的zentao.sql文件

# 6.配置iptables防火墙规则，允许端口访问
[root@localhost opt]# /sbin/iptables -I INPUT -p tcp --dport 9000 -j ACCEPT
[root@localhost opt]# /sbin/iptables -I INPUT -p tcp --dport 9001 -j ACCEPT
```
### 浏览器访问
http://IP:9000 
默认账号密码：admin/123456


![登陆界面](https://upload-images.jianshu.io/upload_images/13323529-522b9ab70135485e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


### 修改项目名称
通过访问管理端：http://IP:9000，点击右下角的“数据库”，输入账号点击后即可跳转到数据库登录页面，输入adduser.sh脚本创建的用户名和密码即可登录成功。
找到**zt_company**表，编辑表，修改**name**字段为你想要的公司名/项目名即可。