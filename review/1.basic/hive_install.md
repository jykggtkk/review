#hive编译及安装配置
##一、安装mysql作为hive的元数据库
    CentOS7的yum源中默认安装mysql是mariadb。为了解决这个问题，我们要先下载并修改mysql的repo源，然后再安装mysql
    1.先删除本机的mariadb
      rpm -qa|grep mariadb  // 查询出来已安装的mariadb
      rpm -e --nodeps 文件名  // 卸载mariadb，文件名为上述命令查询出来的文件
      rm /etc/my.cnf
    2.下载mysql的repo源
      wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm
    3.安装mysql-community-release-el7-5.noarch.rpm包  这个包会使系统yum能获取到mysql的安装源
      rpm -ivh mysql-community-release-el7-5.noarch.rpm
      安装这个包后，会获得两个mysql的yum repo源：/etc/yum.repos.d/mysql-community.repo，/etc/yum.repos.d/mysql-community-source.repo。
    4.安装mysql
      yum install mysql-server
    5.安装完成后，没有密码，需要重置密码
      登录
      mysql -u root
      登录时报这样的错：ERROR 2002 (HY000): Can‘t connect to local MySQL server through socket ‘/var/lib/mysql/mysql.sock‘ (2)，原因是/var/lib/mysql的访问权限问题。下面的命令把/var/lib/mysql的拥有者改为当前用户：
      chown -R  root:root /var/lib/mysql
      重启服务
      service mysqld restart
      重置密码
      mysql -u root
      mysql > use mysql;
      mysql > update user set password=password('l123') where user='root';
      mysql > CREATE USER 'hive'@'%' IDENTIFIED BY 'l123';
      mysql > exit;
    6.需要更改权限才能实现远程连接MYSQL数据库
      mysql -h localhost -uroot -pl123 
      mysql> use mysql; (此DB存放MySQL的各种配置信息) 
      mysql> select host,user from user; (查看用户的权限情况)
      mysql> select host, user, password from user;
      | host       | user | password                                   |
      |:----------:|:------|------------------------------------------:|
      | localhost | root | *4ACFE3202A5FF5CF467898FC58AAB1D615029441 |
      | 127.0.0.1 | root | *4ACFE3202A5FF5CF467898FC58AAB1D615029441 |
      | localhost |       |                                            | 
      mysql> Grant all privileges on *.* to 'root'@'%' identified by 'l123' with grant option;
      mysql> Grant all privileges on *.* to 'hive'@'%' identified by 'l123' with grant option;
      (%表示是所有的外部机器，如果指定某一台机，就将%改为相应的机器名；‘root’则是指要使用的用户名，)
      mysql> flush privileges;
      (运行此句才生效，或者重启MySQL)
      mysql> select host, user, password from user;
      | host       | user | password                                   |
      |:----------:|:-----|------------------------------------------:|
      | localhost | root | *4ACFE3202A5FF5CF467898FC58AAB1D615029441 |
      | 127.0.0.1 | root | *4ACFE3202A5FF5CF467898FC58AAB1D615029441 |
      | localhost |       |                                            |
      | %          | root | *4ACFE3202A5FF5CF467898FC58AAB1D615029441 |
##二、HIVE编译
    mvn clean package -DskipTests -Phadoop-2 -Pdist
    编译生成的包在以下位置：
    packaging/target/apache-hive-3.1.0-bin.tar.gz
##三、HIVE安装
###解压编译好生成的安装包到指定位置并配置环境变量
    tar -xvzf apache-hive-3.1.0-bin.tar.gz /home/hadoop/hive/
    echo 'export HIVE_HOME=/home/hadoop/hive'>>~/.bash_profile
    echo 'export PATH=$HIVE_HOME/bin:$PATH'>>~/.bash_profile
    source ~/.bash_profile
###修改conf/hive-env.sh 
    首先从模板拷贝一份
    cp hive-env.sh.template  hive-env.sh&&vi hive-env.sh
    增加以下内容，以使hive能访问到hadoop
    HADOOP_HOME=/home/hadoop/hadoop
###增加conf/hive-site.xml
    hive-site.xml默认是没有的，该文件用来定义hive访问的元数据库配置
```
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
```
###放置驱动程序
      unzip mysql-connector-java-5.1.46.zip 
      cp mysql-connector-java-5.1.46-bin.jar /home/hadoop/hive/lib/

###初始化hive 
      从 Hive 2.1 版本开始, 我们需要先运行 schematool 命令来执行初始化操作。
      schematool -dbType mysql -initSchema
###运行hive
      hive不是像hadoop的dfs yarn一样的jps程序运行，而是配置好后直接运行
      hive
      后进入操作界面进行SQL的编写执行
      而我们常用的beeline需要启动hiverserver2服务后使用
###beeline相关的Server.Thrift配置 
      主要是hive/conf/hive-site.xml中hive.server2.thrift相关的一些配置项，但要注意一致性
```
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
```
  进入beeline连接数据库后，因为要访问的文件在HDFS上，对应的路径有访问权限限制，所以，这里要设成hadoop中的用户名，实例中用户名即为'hadoop’。如果使用其它用户名，可能会报权限拒绝的错误。或通过修改hadoop中的配置项hadoop.proxyuser.ＸＸ为“*”　来放宽用户名和权限，如示例。
```
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
```
###修改hadoop core-site.xml 
```
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
```
###使用命令启动hiveserver2 
    nohup hive --service hiveserver2  >> /home/hadoop/hive/log/output.log 2>&1 &

##四、python使用PyHive连接hive，安装pyHive
###依赖包
      pip install thrift-sasl
      pip install thrift 
      pip install future 
      sasl安装比较麻烦 需要安装wheel
      pip install wheel 
      然后下载sasl的wheel文件sasl-0.2.1-cp27-cp27m-win_amd64.whl后执行安装
      pip install sasl
      会报一些错误是因为缺少一部分系统软件：
      yum install cyrus-sasl-lib.x86_64
      yum install cyrus-sasl-devel.x86_64
      yum install libgsasl-devel.x86_64
      yum install saslwrapper-devel.x86_64
      一般前面三句基本能解决问题，第四句留着实在没办法时用。
      错误描述：
      error:sasl/saslwrapper.h:22:23: 致命错误：sasl/sasl.h：没有那个文件或目录
      error: command 'gcc' failed with exit status 1

      pip install pyHive
      