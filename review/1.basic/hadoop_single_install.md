1.JDK安装及验证
    centos默认带的是openjdk  要换成oracle的jdk
    下载jdk1.8的tar.gz 解压后 拷贝到/usr/lib/jvm 下面  并将文件夹改名为jdk
     mv jdk1.8.0_181 jdk

     配置环境变量 vim /etc/profile 
    export JAVA_HOME=/usr/lib/jvm/jdk
    export JRE_HOME=$JAVA_HOME/jre
    export CLASSPATH=.:$JAVA_HOME/lib:$JER_HOME/lib:$CLASSPATH
    export PATH=$JAVA_HOME/bin:$JER_HOME/bin:$PATH

    source /etc/profile 

    java -version 
2.用户创建及免密码登陆
    useradd -m hadoop -s /bin/bash
    passwd Hadoop
    visudo #为 hadoop 用户增加管理员权限，方便部署  输入i切换到insert模式，在root ALL=(ALL) ALL 这行下面添加：hadoop  ALL=(ALL)       ALL
3.安装编译依赖软件
    yum install g++ autoconf automake libtool cmake zlib1g-dev pkg-config libssl-dev
4.安装protobuf 
     tar -zxvf protobuf-2.5.0.tar.gz  到  /root/soft
     
    $ cd  /root/soft/protobuf-2.5.0
    $ ./configure --prefix=/root/soft/protobuf-2.5.0    
    $ make
    $ make check
    $ make clean
    $ make install

    安装完成，配置： 
    vim /etc/profile，添加
　　export PATH=$PATH:/root/soft/protobuf/bin/
　　export PKG_CONFIG_PATH=/root/soft/protobuf/lib/pkgconfig/
　　保存执行，source /etc/profile。同时在~/.profile中添加上面两行代码，否则会出现登录用户找不到protoc命令。
    配置动态链接库
　　vim /etc/ld.so.conf，在文件中添加/usr/local/protobuf/lib（注意: 在新行处添加），然后执行命令: ldconfig
    注意：  在要使用的用户（hadoop）的.bash_profile 中仍需要再配置环境变量 不然命令还是执行不了

5.maven 准备 
    解压 apache-maven-3.3.9-bin.tar.gz 到 /home/hadoop/soft ，添加环境变量
    export MAVEN_HOME=/usr/soft/apache-maven-3.3.9
    export PATH=.:$PATH:$JAVA_HOME/bin:$MAVEN_HOME/bin
    测试， mvn -version 

    --报warning：
    which: no javac in (.:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/hadoop/.local/bin:/home/hadoop/bin:/home/hadoop/.local/bin:/home/hadoop/bin:/bin:/home/hadoop/soft/apache-maven-3.3.9/bin)
    Warning: JAVA_HOME environment variable is not set.


6.编译程序
  进入hadoop文件夹执行：
  mvn clean package -Pdist,native,docs -DskipTests -Dtar 
  错误后再进行编译可以去掉clean
  mvn package -Pdist,native,docs -DskipTests -Dtar 

  编译时不clean，会接着上次结束的地方继续下载jar包等。如果一次编译没有成功（因为包没有下全），可以多次编译。
  建议编译时加native参数，否则在运行hadoop时会出现warning。（我是直接把别的编译好的so文件拿来用了）
编译成功（如下）,生成的jar包会放在/work/hadoop-2.7.3-src/hadoop-dist/target/hadoop-2.7.3.tar.gz。另外每个模块也会有对于的生成的jar包。
如果修改了部分hadoop的源码，只需要局部编译，然后去对应位置替换即可。
在局部编译后的target目录下，找到jar包，替换整体编译好后 share/hadoop/yarn下的jar包。

7.编译错误总结：
  1）
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

原因解析：
${env.FINDBUGS_HOME}/src/xsl/default.xsl doesn't exist   关键信息
 需要安装  findbugs软件 
 mv findbugs-3.0.1 /usr/local/findbug

 配置环境变量
export FINDBUGS_HOME=/opt/findbug

export PATH=$PATH:$FINDBUGS_HOME/bin

 #还要补充安装 
 yum install ant


编译成功生成的文件在 
/home/soft/hadoop-2.7.5-src/hadoop-dist/target/hadoop-2.7.5.tar.gz

如果修改了部分hadoop的源码，只需要局部编译，然后去对应位置替换即可。
在局部编译后的target目录下，找到jar包，替换整体编译好后 share/hadoop/yarn下的jar包。

8.安装启动
永久修改主机名 
 修改centos网络配置文件/etc/sysconfig/network，在末尾添加HOSTNAME=master
vim /etc/sysconfig/network
NETWORKING=yes
NOZEROCONF=yes
HOSTNAME=master
#修改/etc/hosts文件
添加 
192.168.245.128 master 

创建安装目录
tar xfz hadoop-2.7.5.tar.gz
#移动到/opt目录
mkdir /opt/hadoop
mv hadoop-2.7.5/* /opt/hadoop
#更改目录所有者为hadoop
chown -R hadoop:hadoop /opt/hadoop
--用户权限移不动  暂时使用 /home/hadoop/hadoop 目录吧

#环境变量配置
vim /etc/profile
export HADOOP_HOME=/home/hadoop/hadoop
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin


#编辑hadoop-env.sh文件
cd $HADOOP_HOME/etc/hadoop
vim hadoop-env.sh

#将export JAVA_HOME=${JAVA_HOME}改为如下 -- 不改他读取不到系统的JAVA_HOME
export JAVA_HOME=/usr/local/jvm/jdk


#编辑core-site.xml文件，configuration中的内容添加

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

#创建目录
mkdir /home/hadoop/hadoop/hadoopdata
mkdir /home/hadoop/hadoop/hadoopdata/namenode
mkdir /home/hadoop/hadoop/hadoopdata/datanode


#创建mapred-site.xml文件
cp mapred-site.xml.template mapred-site.xml

#编辑mapred-site.xml文件，configuration中的内容添加
<configuration>
 <property>
  <name>mapreduce.framework.name</name>
  <value>yarn</value>
 </property>
</configuration> 

#编辑yarn-site.xml文件，configuration中的内容
<!-- Site specific YARN configuration properties -->
<property>
  <name>yarn.nodemanager.aux-services</name>
  <value>mapreduce_shuffle</value>
</property> 

#初始化HDFS文件系统
hdfs namenode -format
#启动服务  进入sbin文件夹
cd /opt/hadoop/sbin 
#启动Hadoop服务
start-dfs.sh 
#启动yarn
start-yarn.sh 
#查看服务运行状态
jps
#测试
访问主机端口50070或8088查看


额外的
#去除告警信息
#WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
log4j.logger.org.apache.hadoop.util.NativeCodeLoader=ERROR
