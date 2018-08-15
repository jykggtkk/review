#下载hive的src包
#centos7 yum 安装 mysql
CentOS7的yum源中默认安装mysql是mariadb。为了解决这个问题，
我们要先下载mysql的repo源，然后再安装mysql

0.先删除本机的mariadb
rpm -qa|grep mariadb  // 查询出来已安装的mariadb
rpm -e --nodeps 文件名  // 卸载mariadb，文件名为上述命令查询出来的文件
rm /etc/my.cnf

1. 下载mysql的repo源

$ wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm

2. 安装mysql-community-release-el7-5.noarch.rpm包

$ sudo rpm -ivh mysql-community-release-el7-5.noarch.rpm
安装这个包后，会获得两个mysql的yum repo源：/etc/yum.repos.d/mysql-community.repo，/etc/yum.repos.d/mysql-community-source.repo。

3. 安装mysql

$ sudo yum install mysql-server
根据步骤安装就可以了，不过安装完成后，没有密码，需要重置密码。

4. 重置密码

重置密码前，首先要登录

$ mysql -u root
登录时报这样的错：ERROR 2002 (HY000): Can‘t connect to local MySQL server through socket ‘/var/lib/mysql/mysql.sock‘ (2)，原因是/var/lib/mysql的访问权限问题。下面的命令把/var/lib/mysql的拥有者改为当前用户：

$ sudo chown -R  root:root /var/lib/mysql
然后，重启服务：

$ service mysqld restart
接下来登录重置密码：

$ mysql -u root
mysql > use mysql;
mysql > update user set password=password('l123') where user='root';
mysql > CREATE USER 'hive'@'%' IDENTIFIED BY 'l123';
mysql > exit;

5. 需要更改权限才能实现远程连接MYSQL数据库

可以通过以下方式来确认：
root#mysql -h localhost -uroot -p
Enter password: ******
Welcome to the MySQL monitor.   Commands end with ; or \g.
Your MySQL connection id is 4 to server version: 4.0.20a-debug
Type ‘help;’ or ‘\h’ for help. Type ‘\c’ to clear the buffer.
mysql> use mysql; (此DB存放MySQL的各种配置信息)
Database changed
mysql> select host,user from user; (查看用户的权限情况)
mysql> select host, user, password from user;
+-----------+------+-------------------------------------------+
| host       | user | password                                   |
+-----------+------+-------------------------------------------+
| localhost | root | *4ACFE3202A5FF5CF467898FC58AAB1D615029441 |
| 127.0.0.1 | root | *4ACFE3202A5FF5CF467898FC58AAB1D615029441 |
| localhost |       |                                            |
+-----------+------+-------------------------------------------+
4 rows in set (0.01 sec)
由此可以看出，只能以localhost的主机方式访问。
解决方法：
mysql> Grant all privileges on *.* to 'root'@'%' identified by '123456' with grant option;
 Grant all privileges on *.* to 'hive'@'%' identified by 'l123' with grant option;
(%表示是所有的外部机器，如果指定某一台机，就将%改为相应的机器名；‘root’则是指要使用的用户名，)
mysql> flush privileges;    (运行此句才生效，或者重启MySQL)
Query OK, 0 rows affected (0.03 sec)
再次查看。。
mysql> select host, user, password from user;
+-----------+------+-------------------------------------------+
| host       | user | password                                   |
+-----------+------+-------------------------------------------+
| localhost | root | *4ACFE3202A5FF5CF467898FC58AAB1D615029441 |
| 127.0.0.1 | root | *4ACFE3202A5FF5CF467898FC58AAB1D615029441 |
| localhost |       |                                            |
| %          | root | *4ACFE3202A5FF5CF467898FC58AAB1D615029441 |
+-----------+------+-------------------------------------------+
4 rows in set (0.01 sec)


#直接编译
 mvn clean package -DskipTests -Phadoop-2 -Pdist
 # 编译生成的包在以下位置：
 packaging/target/apache-hive-3.1.0-bin.tar.gz

 #安装
 #解压到 /home/hadoop/hive
echo 'export HIVE_HOME=/home/hadoop/hive'>>~/.bash_profile
echo 'export PATH=$HIVE_HOME/bin:$PATH'>>~/.bash_profile


#修改hive-env.sh  conf下
 cp hive-env.sh.template  hive-env.sh&&vi hive-env.sh
HADOOP_HOME=/home/hadoop/hive

#增加hive-site.xml
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration> 
<property>
<name>javax.jdo.option.ConnectionURL</name>
<value>jdbc:mysql://localhost:3306/vincent_hive?createDatabaseIfNotExist=true</value>
</property>
<property>
<name>javax.jdo.option.ConnectionDriverName</name>
<value>com.mysql.jdbc.Driver</value>
</property>
<property>
<name>javax.jdo.option.ConnectionUserName</name>
<value>root</value>
</property>
<property>
<name>javax.jdo.option.ConnectionPassword</name>
<value>l123</value>
</property>
</configuration>

#放置驱动程序
unzip mysql-connector-java-5.1.46.zip 
cp mysql-connector-java-5.1.46-bin.jar /home/hadoop/hive/lib/

#初始化hive 
从 Hive 2.1 版本开始, 我们需要先运行 schematool 命令来执行初始化操作。

schematool -dbType mysql -initSchema

beeline相关的Server.Thrift配置  
主要是hive/conf/hive-site.xml中hive.server2.thrift相关的一些配置项，但要注意一致性

  <property>
    <name>hive.server2.thrift.bind.host</name>
    <value>master</value>
    <description>Bind host on which to run the HiveServer2 Thrift service.</description>
  </property>

  <property>
    <name>hive.server2.thrift.port</name>
    <value>10000</value>
    <description>Port number of HiveServer2 Thrift interface when hive.server2.transport.mode is 'binary'.</description>
  </property>

  <property>
    <name>hive.server2.thrift.http.port</name>
    <value>10001</value>
    <description>Port number of HiveServer2 Thrift interface when hive.server2.transport.mode is 'http'.</description>
  </property>

  进入beeline连接数据库后，因为要访问的文件在HDFS上，对应的路径有访问权限限制，所以，这里要设成hadoop中的用户名，实例中用户名即为'hadoop’。如果使用其它用户名，可能会报权限拒绝的错误。或通过修改hadoop中的配置项hadoop.proxyuser.ＸＸ为“*”　来放宽用户名和权限，如示例。

  <property>
    <name>hive.server2.thrift.client.user</name>
    <value>hadoop</value>
    <description>Username to use against thrift client</description>
  </property>
  <property>
    <name>hive.server2.thrift.client.password</name>
    <value>hadoop</value>
    <description>Password to use against thrift client</description>
  </property>

  #修改hadoop core-site.xml 
  <property>
    <name>hadoop.proxyuser.hadoop.hosts</name>
    <!--value>master</value-->
    <value>*</value>
    </property>
    <property>
    <name>hadoop.proxyuser.hadoop.groups</name>
    <!--value>hadoop</value-->
    <value>*</value>
  </property>


#使用命令启动hiveserver2 
  nohup hive --service hiveserver2  >> /home/hadoop/hive/log/output.log 2>&1 &



PyHive连接hive

1.依赖包：

pip install thrift-sasl
pip install thrift 
pip install future 
#sasl安装比较麻烦 需要安装wheel
#pip install wheel 
#然后下载sasl的wheel文件后执行安装
[root@localhost ~]# pip install sasl
Collecting sasl
  Using cached https://files.pythonhosted.org/packages/8e/2c/45dae93d666aea8492678499e0999269b4e55f1829b1e4de5b8204706ad9/sasl-0.2.1.tar.gz
Requirement already satisfied: six in ./.pyenv/versions/3.6.5/lib/python3.6/site-packages (from sasl) (1.11.0)
Building wheels for collected packages: sasl
  Running setup.py bdist_wheel for sasl ... error
  Complete output from command /root/.pyenv/versions/3.6.5/bin/python -u -c "import setuptools, tokenize;__file__='/tmp/pip-install-t_2jp4ah/sasl/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.re
ad().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" bdist_wheel -d /tmp/pip-wheel-rdwox626 --python-tag cp36:  running bdist_wheel
  running build
  running build_py
  creating build
  creating build/lib.linux-x86_64-3.6
  creating build/lib.linux-x86_64-3.6/sasl
  copying sasl/__init__.py -> build/lib.linux-x86_64-3.6/sasl
  running egg_info
  writing sasl.egg-info/PKG-INFO
  writing dependency_links to sasl.egg-info/dependency_links.txt
  writing requirements to sasl.egg-info/requires.txt
  writing top-level names to sasl.egg-info/top_level.txt
  reading manifest file 'sasl.egg-info/SOURCES.txt'
  reading manifest template 'MANIFEST.in'
  writing manifest file 'sasl.egg-info/SOURCES.txt'
  copying sasl/saslwrapper.cpp -> build/lib.linux-x86_64-3.6/sasl
  copying sasl/saslwrapper.h -> build/lib.linux-x86_64-3.6/sasl
  copying sasl/saslwrapper.pyx -> build/lib.linux-x86_64-3.6/sasl
  running build_ext
  building 'sasl.saslwrapper' extension
  creating build/temp.linux-x86_64-3.6
  creating build/temp.linux-x86_64-3.6/sasl
  gcc -pthread -Wno-unused-result -Wsign-compare -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -Isasl -I/root/.pyenv/versions/3.6.5/include/python3.6m -c sasl/saslwrapper.cpp -o build/temp.linux-x86_
64-3.6/sasl/saslwrapper.o  cc1plus: 警告：command line option ‘-Wstrict-prototypes’ is valid for C/ObjC but not for C++ [默认启用]
  In file included from sasl/saslwrapper.cpp:254:0:
  sasl/saslwrapper.h:22:23: 致命错误：sasl/sasl.h：没有那个文件或目录
   #include <sasl/sasl.h>
                         ^
  编译中断。
  error: command 'gcc' failed with exit status 1
  
  ----------------------------------------
  Failed building wheel for sasl
  Running setup.py clean for sasl
Failed to build sasl
Installing collected packages: sasl
  Running setup.py install for sasl ... error
    Complete output from command /root/.pyenv/versions/3.6.5/bin/python -u -c "import setuptools, tokenize;__file__='/tmp/pip-install-t_2jp4ah/sasl/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.
read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --record /tmp/pip-record-iwr7jc0p/install-record.txt --single-version-externally-managed --compile:    running install
    running build
    running build_py
    creating build
    creating build/lib.linux-x86_64-3.6
    creating build/lib.linux-x86_64-3.6/sasl
    copying sasl/__init__.py -> build/lib.linux-x86_64-3.6/sasl
    running egg_info
    writing sasl.egg-info/PKG-INFO
    writing dependency_links to sasl.egg-info/dependency_links.txt
    writing requirements to sasl.egg-info/requires.txt
    writing top-level names to sasl.egg-info/top_level.txt
    reading manifest file 'sasl.egg-info/SOURCES.txt'
    reading manifest template 'MANIFEST.in'
    writing manifest file 'sasl.egg-info/SOURCES.txt'
    copying sasl/saslwrapper.cpp -> build/lib.linux-x86_64-3.6/sasl
    copying sasl/saslwrapper.h -> build/lib.linux-x86_64-3.6/sasl
    copying sasl/saslwrapper.pyx -> build/lib.linux-x86_64-3.6/sasl
    running build_ext
    building 'sasl.saslwrapper' extension
    creating build/temp.linux-x86_64-3.6
    creating build/temp.linux-x86_64-3.6/sasl
    gcc -pthread -Wno-unused-result -Wsign-compare -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -Isasl -I/root/.pyenv/versions/3.6.5/include/python3.6m -c sasl/saslwrapper.cpp -o build/temp.linux-x8
6_64-3.6/sasl/saslwrapper.o    cc1plus: 警告：command line option ‘-Wstrict-prototypes’ is valid for C/ObjC but not for C++ [默认启用]
    In file included from sasl/saslwrapper.cpp:254:0:
    sasl/saslwrapper.h:22:23: 致命错误：sasl/sasl.h：没有那个文件或目录
     #include <sasl/sasl.h>
                           ^
    编译中断。
    error: command 'gcc' failed with exit status 1
    ·
    ----------------------------------------
Command "/root/.pyenv/versions/3.6.5/bin/python -u -c "import setuptools, tokenize;__file__='/tmp/pip-install-t_2jp4ah/sasl/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '
\n');f.close();exec(compile(code, __file__, 'exec'))" install --record /tmp/pip-record-iwr7jc0p/install-record.txt --single-version-externally-managed --compile" failed with error code 1 in /tmp/pip-install-t_2jp4ah/sasl/
安装sasl前需要安装以下软件 不然会报 以上错误
 
yum install cyrus-sasl-lib.x86_64
yum install cyrus-sasl-devel.x86_64
yum install libgsasl-devel.x86_64
yum install saslwrapper-devel.x86_64
一般拉说前面三句基本能解决问题，第四句留着实在没办法时用。
