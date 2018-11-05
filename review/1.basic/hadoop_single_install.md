官方教程：http://hadoop.apache.org/docs/r2.7.3/

# 1.Hadoop安装的三种模式
1. 单机模式（standalone）
单机模式是Hadoop的默认模式。当首次解压Hadoop的源码包时，Hadoop无法了解硬件安装环境，便保守地选择了最小配置。在这种默认模式下所有3个XML文件均为空。当配置文件为空时，Hadoop会完全运行在本地。因为不需要与其他节点交互，单机模式就不使用HDFS，也不加载任何Hadoop的守护进程。该模式主要用于开发调试MapReduce程序的应用逻辑。
此程序一般不建议安装，网络上很少这方面资料。
2. 伪分布模式（Pseudo-Distributed Mode）
伪分布模式在“单节点集群”上运行Hadoop，其中所有的守护进程都运行在同一台机器上。该模式在单机模式之上增加了代码调试功能，允许你检查内存使用情况，HDFS输入输出，以及其他的守护进程交互。比如namenode，datanode，secondarynamenode，jobtracer，tasktracer这5个进程，都能在集群上看到。
3. 全分布模式（Fully Distributed Mode）
Hadoop守护进程运行在一个集群上。
意思是说master上看到namenode,jobtracer，secondarynamenode可以安装在master节点，也可以单独安装。slave节点能看到datanode和tasktracer
# 2.JDK安装及验证
centos默认带的是openjdk  要换成oracle的jdk
下载jdk1.8的tar.gz 解压后 拷贝到/usr/lib/jvm 下面  并将文件夹改名为jdk
`mv jdk1.8.0_181 jdk`
配置环境变量 
```
vim /etc/profile 
export JAVA_HOME=/usr/lib/jvm/jdk
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=.:$JAVA_HOME/lib:$JER_HOME/lib:$CLASSPATH
export PATH=$JAVA_HOME/bin:$JER_HOME/bin:$PATH
source /etc/profile 
java -version
```
# 3.用户创建及免密码登陆
```
useradd -m hadoop -s /bin/bash
passwd Hadoop

visudo #为 hadoop 用户增加管理员权限，方便部署  输入i切换到insert模式，在root ALL=(ALL) ALL 这行下面添加：hadoop  ALL=(ALL)       ALL
```
# 4.安装编译依赖软件
`yum install g++ autoconf automake libtool cmake zlib1g-dev pkg-config libssl-dev ant`
# 5.安装protobuf 
`tar -zxvf protobuf-2.5.0.tar.gz`到`/root/soft `
```
cd  /root/soft/protobuf-2.5.0
./configure --prefix=/root/soft/protobuf-2.5.0    
make
make check
make clean
make install
```
### 安装完成，配置： 
`vim /etc/profile`，添加以下内容：
```
export PATH=$PATH:/root/soft/protobuf/bin/
export PKG_CONFIG_PATH=/root/soft/protobuf/lib/pkgconfig/
```
同时在~/.profile中添加上面两行代码，否则会出现登录用户找不到protoc命令。
`source /etc/profile`
### 配置动态链接库
`vim /etc/ld.so.conf`，在文件中添加`/usr/local/protobuf/lib`（注意: 在新行处添加），然后执行命令: 
`ldconfig`
 注意：  在要使用的用户（hadoop）的.bash_profile 中仍需要再配置环境变量 不然命令还是执行不了

# 6.准备maven 
解压 `apache-maven-3.3.9-bin.tar.gz` 到 `/home/hadoop/soft` ，添加环境变量
```
export MAVEN_HOME=/usr/soft/apache-maven-3.3.9
export PATH=.:$PATH:$JAVA_HOME/bin:$MAVEN_HOME/bin
```
`mvn -version`

# 7.编译源码程序，生成部署安装包
进入hadoop文件夹执行：
`mvn clean package -Pdist,native,docs -DskipTests -Dtar `
如果是编译过程中出现错误，在解决错误问题后再进行编译可以去掉clean，否则每次编译都要现从外网下载所有的程序包会比较慢。
`mvn package -Pdist,native,docs -DskipTests -Dtar` 
编译时不clean，会接着上次结束的地方继续下载jar包等。如果一次编译没有成功（因为包没有下全），可以多次编译。
建议编译时加native参数，否则在运行hadoop时会出现warning。（我是直接把别的编译好的so文件拿来用了）
编译成功（如下）,生成的jar包会放在`/work/hadoop-2.7.3-src/hadoop-dist/target/hadoop-2.7.3.tar.gz`。
另外每个模块也会有对于的生成的jar包。
如果修改了部分hadoop的源码，只需要局部编译，然后去对应位置替换即可。
在局部编译后的target目录下，找到jar包，替换整体编译好后 share/hadoop/yarn下的jar包。

# 8.编译错误总结：
1. findbugs软件 
```
[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 06:23 min
[INFO] Finished at: 2018-08-11T18:46:25+08:00
[INFO] Final Memory: 117M/366M
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-antrun-plugin:1.7:run (site) on project hadoop-common: An Ant BuildException has occured: stylesheet /home/hadoop/soft/hadoop-2.7.5-src/hadoop-comm
on-project/hadoop-common/${env.FINDBUGS_HOME}/src/xsl/default.xsl doesn't exist.[ERROR] around Ant part ...<xslt in="/home/hadoop/soft/hadoop-2.7.5-src/hadoop-common-project/hadoop-common/target/findbugsXml.xml" style="${env.FINDBUGS_HOME}/src/xsl/default.xsl" out="/home/hadoop/soft/hadoo
p-2.7.5-src/hadoop-common-project/hadoop-common/target/site/findbugs.html"/>... @ 43:261 in /home/hadoop/soft/hadoop-2.7.5-src/hadoop-common-project/hadoop-common/target/antrun/build-main.xml[ERROR] -> [Help 1]
[ERROR] 
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR] 
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoExecutionException
[ERROR] 
[ERROR] After correcting the problems, you can resume the build with the command
[ERROR]   mvn <goals> -rf :hadoop-common
```
原因解析：
关键信息:`${env.FINDBUGS_HOME}/src/xsl/default.xsl doesn't exist`
需要安装  findbugs软件 
`mv findbugs-3.0.1 /usr/local/findbug`
配置环境变量:
```
export FINDBUGS_HOME=/opt/findbug
export PATH=$PATH:$FINDBUGS_HOME/bin
```
### 还要补充安装 
yum install ant


编译成功后，生成的文件在 
`/home/soft/hadoop-2.7.5-src/hadoop-dist/target/hadoop-2.7.5.tar.gz`

如果修改了部分hadoop的源码，只需要局部编译，然后去对应位置替换即可。
在局部编译后的target目录下，找到jar包，替换整体编译好后 share/hadoop/yarn下的jar包。

# 9.安装启动
永久修改主机名 
修改centos网络配置文件`/etc/sysconfig/network`，在末尾添加`HOSTNAME=master`
`vim /etc/sysconfig/network` ，修改以下内容
```
NETWORKING=yes
NOZEROCONF=yes
HOSTNAME=master
```
修改/etc/hosts文件,添加以下内容，需要一个固定的IP地址：
`192.168.245.128 master `

创建安装目录
`tar xfz hadoop-2.7.5.tar.gz`
移动到/opt目录
```
mkdir /opt/hadoop
mv hadoop-2.7.5/* /opt/hadoop
```
更改目录所有者为hadoop:
`chown -R hadoop:hadoop /opt/hadoop`

环境变量配置:
```
vim /etc/profile
export HADOOP_HOME=/home/hadoop/hadoop
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
```
修改hadoop-env.sh文件
```
cd $HADOOP_HOME/etc/hadoop
vim hadoop-env.sh
```
将`export JAVA_HOME=${JAVA_HOME}`改为如下 -- 不改他读取不到系统的JAVA_HOME
`export JAVA_HOME=/usr/local/jvm/jdk`

编辑core-site.xml文件，configuration中的内容添加
```
<configuration>
<property>
  <name>fs.default.name</name>
    <value>hdfs://localhost:9000</value>
</property>
</configuration>

#编辑hdfs-site.xml文件，configuration中的内容添加
<configuration>
<property>
 <name>dfs.replication</name>
 <value>1</value>
</property>
 
<property>
  <name>dfs.name.dir</name>
  <value>file:///home/hadoop/hadoop/hadoopdata/namenode</value>
</property>
 
<property>
  <name>dfs.data.dir</name>
  <value>file:///home/hadoop/hadoop/hadoopdata/datanode</value>
</property>
</configuration> 
```
创建程序运行目录：
```
mkdir /home/hadoop/hadoop/hadoopdata
mkdir /home/hadoop/hadoop/hadoopdata/namenode
mkdir /home/hadoop/hadoop/hadoopdata/datanode
```

创建mapred-site.xml文件:
`cp mapred-site.xml.template mapred-site.xml`

编辑mapred-site.xml文件，configuration中的内容添加:
```
<configuration>
 <property>
  <name>mapreduce.framework.name</name>
  <value>yarn</value>
 </property>
</configuration> 
```
编辑yarn-site.xml文件，configuration中的内容:
```
<!-- Site specific YARN configuration properties -->
<property>
  <name>yarn.nodemanager.aux-services</name>
  <value>mapreduce_shuffle</value>
</property> 
```
初始化HDFS文件系统:
`hdfs namenode -format`
启动服务  进入sbin文件夹
`cd /opt/hadoop/sbin `
启动Hadoop服务
`start-dfs.sh `
启动yarn
`start-yarn.sh `
查看服务运行状态
`jps`
测试
访问主机端口50070或8088查看

去除告警信息
`#WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable`
修改配置：
`log4j.logger.org.apache.hadoop.util.NativeCodeLoader=ERROR`
