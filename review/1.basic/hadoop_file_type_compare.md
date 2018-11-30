
# 背景
在实施大数据平台项目或直接说hadoop平台类的项目时，开发设计人员总会对"文件格式"感到困惑，不知道该如何理解和使用。常见的问题有以下几种：
1. hdfs支持哪些文件格式？
2. txt格式、rc格式和orc格式有什么区别？
3. orc格式和parquet格式哪个好？
4. 该怎么去选择这些格式，这些格式的文件都有什么优缺点？
5. Hbase和ElasticSearch为什么也是文件存储格式的一种？
6. kudu又是什么？

事实上，如果对这些问题不了解或一知半解，在使用中会遇到很多麻烦问题，所以有必要将hdfs上的这些文件格式的概念和特点讲清楚。

# hdfs支持哪些文件格式？
我们知道狭义的hadoop指的是一套用于在由通用硬件构建的大型集群上运行应用程序的框架，主要包含四个部分：
* hadoop common hadoop的核心模块
* hadoop yarn hadoop的资源管理器
* hadoop hdfs 分布式文件系统
* hadoop mapreduce 高性能并行计算框架

hdfs是一套类似于挂载在linux系统上的一个目录系统，任何文件都是可以上传到hdfs上并下载的。
通常我们说支持哪些文件格式是指像Apache Hive /Impala这种数据分析引擎能够访问读取的文件格式。
hive原生支持的格式包括：
* TEXTFILE
_textfile为默认格式，存储方式为行式存储，在检索时磁盘开销大 数据解析开销大，而对压缩的text文件 hive无法进行合并和拆分_
* SEQUENCEFILE
_二进制文件,以<key,value>的形式序列化到文件中,存储方式为行式存储，可以对文件进行分割和压缩，一般使用block压缩，使用Hadoop 的标准的Writable 接口实现序列化和反序列化,和hadoop api中的mapfile是相互兼容的。_
* RCFILE
_存储方式为数据按行分块，每块按照列存储的行列混合模式，具有压缩快，列存取快的特点。_
_在使用时，读记录尽量涉及到的block最少，这样读取需要的列只需要读取每个row group 的头部定义，具有明显速度优势。_
_读取全量数据的操作 性能可能比sequencefile没有明显的优势。_
# Apache Orc 和Apache Parquet
这两种是hive发展过程中出现的存储格式并发展为Apache独立顶级项目。
* Orc是从HIVE的原生格式RCFILE优化改进而来。
* Parquet是Cloudera公司研发并开源的格式。

这两者都属于列存储格式，但Orc严格上应该算是行列混合存储，首先根据行组分割整个表，在每一个行组内进行按列存储。
Parquet文件和Orc文件都是是自解析的，文件中包括该文件的数据和元数据，Orc的元数据使用Protocol Buffers序列化。
两者都支持嵌套数据格式（struct\map\list），但策略不同：
* Parquet支持嵌套的数据模型，类似于Protocol Buffers，每一个数据模型的schema包含多个字段，每一个字段有三个属性：重复次数、数据类型和字段名。
* ORC原生是不支持嵌套数据格式的，而是通过对复杂数据类型特殊处理的方式实现嵌套格式的支持。

压缩：
两者都相比txt格式进行了数据压缩，相比而言，Orc的压缩比例更大，效果更好。

计算引擎支持：都支持spark、MR计算引擎。

查询引擎支持：Parquet被Spark SQL、Hive、Impala、Drill等支持，而Orc被Spark SQL、Presto、Hive支持，Orc不被Impala支持。

功能及性能对比：
使用TPC-DS数据集并且对它进行改造以生成宽表、嵌套和多层嵌套的数据。使用最常用的Hive作为SQL引擎进行测试
最终表现：
功能：
* ORC的压缩比更大，对存储空间的利用更好
* ORC可以一定程度上支持ACID操作，Parquet不可以
性能：
* 数据导入 orc更快
* 聚合查询 orc更快
* 单表查询 orc快一点点点
* 带有复杂数据构成的表查询 （1层） orc更快
* 带有复杂数据构成的表查询  （3层） orc更快

结果分析
从上述测试结果来看，星状模型对于数据分析场景并不是很合适，多个表的join会大大拖慢查询速度，并且不能很好的利用列式存储带来的性能提升，在使用宽表的情况下，列式存储的性能提升明显，ORC文件格式在存储空间上要远优于Text格式，较之于PARQUET格式有一倍的存储空间提升，在导数据（insert into table select 这样的方式）方面ORC格式也要优于PARQUET，在最终的查询性能上可以看到，无论是无嵌套的扁平式宽表，或是一层嵌套表，还是多层嵌套的宽表，两者的查询性能相差不多，较之于Text格式有2到3倍左右的提升。
另外，扁平式的表结构要比嵌套式结构的查询性能有所提升，所以如果选择使用大宽表，则设计宽表的时候尽可能的将表设计的扁平化，减少嵌套数据。
通过测试对比，ORC文件存储格式无论是在空间存储、导数据速度还是查询速度上表现的都较好一些，并且ORC可以一定程度上支持ACID操作，社区的发展目前也是Hive中比较提倡使用的一种列式存储格式，另外，本次测试主要针对的是Hive引擎，所以不排除存在Hive与ORC的敏感度比PARQUET要高的可能性。Parquet更多的是在Impala环境下使用[图片上传失败...(image-a4baa-1537673554146)]

![图片2.png](https://upload-images.jianshu.io/upload_images/13323529-c29f6c62a9cc484b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# kudu是什么？
Apache Kudu是由Cloudera开源的存储引擎，可以同时提供低延迟的随机读写和高效的数据分析能力。Kudu支持水平扩展，使用Raft协议进行一致性保证，并且与Cloudera Impala和Apache Spark等当前流行的大数据查询和分析工具结合紧密。 
现在提起大数据存储，我们能想到的技术有很多，比如HDFS，以及在HDFS上的列式存储技术Apache Parquet，Apache ORC，还有以KV形式存储半结构化数据的Apache HBase和Apache Cassandra等等。既然有了如此多的存储技术，Cloudera公司为什么要开发出一款全新的存储引擎Kudu呢？
对于会被用来进行分析的静态数据集来说，使用Parquet或者ORC存储是一种明智的选择。但是目前的列式存储技术都不能更新数据（补充：ORC是可以的），而且随机读写性能感人。而可以进行高效随机读写的HBase、Cassandra等数据库，却并不适用于基于SQL的数据分析方向。所以现在的企业中，经常会存储两套数据分别用于实时读写与数据分析，先将数据写入HBase中，再定期通过ETL到Parquet进行数据同步（该使用场景与常见金融hadoop平台的流程并不太一致）。
关键词： 随机访问 
基于HDFS的存储技术，比如Parquet，具有高吞吐量连续读取数据的能力；而HBase和Cassandra等技术适用于低延迟的随机读写场景，那么有没有一种技术可以同时具备这两种优点呢？Kudu提供了一种“happy medium”的选择：
![场景选择](https://upload-images.jianshu.io/upload_images/13323529-802cc92d97fed145.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Kudu不但提供了行级的插入、更新、删除API，同时也提供了接近Parquet性能的批量扫描操作。使用同一份存储，既可以进行随机读写，也可以满足数据分析的要求。
## kudu总览
### Tables和Schemas
从用户角度来看，Kudu是一种存储结构化数据表的存储系统。
在一个Kudu集群中可以定义任意数量的table，每个table都需要预先定义好schema。
每个table的列数是确定的，每一列都需要有名字和类型
每个表中可以把其中一列或多列定义为主键。
这么看来，Kudu更像关系型数据库
不过Kudu目前还不能像关系型数据一样支持二级索引。 

Kudu使用确定的列类型，而不是类似于NoSQL的“everything is byte”。
这可以带来两点好处：
确定的列类型使Kudu可以进行类型特有的编码。
可以提供 SQL-like 元数据给其他上层查询工具，比如BI工具

### 读写操作
用户可以使用 Insert，Update和Delete API对表进行写操作。 （非SQL）
不论使用哪种API，都必须指定主键。
但批量的删除和更新操作需要依赖更高层次的组件（比如Impala、Spark）。
Kudu目前还不支持多行事务。 
而在读操作方面，Kudu只提供了Scan操作来获取数据。
用户可以通过指定过滤条件来获取自己想要读取的数据，但目前只提供了两种类型的过滤条件：主键范围和列值与常数的比较。
由于Kudu在硬盘中的数据采用列式存储，所以只扫描需要的列将极大地提高读取性能。
### 一致性模型
Kudu为用户提供了两种一致性模型。
默认的一致性模型是snapshot consistency。这种一致性模型保证用户每次读取出来的都是一个可用的快照，但这种一致性模型只能保证单个client可以看到的数据，但不能保证多个client每次取出的都是一样的数据。
另一种一致性模型external consistency。可以在多个client之间保证每次取到的都是数据，但是Kudu没有提供默认的实现，需要用户做一些额外工作。
为了实现external consistency，Kudu提供了两种方式：
在client之间传播timestamp token。在一个client完成一次写入后，会得到一个timestamp token，然后这个client把这个token传播到其他client，这样其他client就可以通过token取到数据了。不过这个方式的复杂度很高。
通过commit-wait方式，这有些类似于Google的Spanner。但是目前基于NTP的commit-wait方式延迟实在有点高。不过Kudu相信，随着Spanner的出现，未来几年内基于real-time clock的技术将会逐渐成熟。
### Kudu的架构
![KUDU架构](https://upload-images.jianshu.io/upload_images/13323529-933c7bb6979ddd08.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Kudu使用单个的Master节点，用来管理集群的元数据，并且使用任意数量的Tablet Server节点用来存储实际数据。
Master
Kudu的master节点负责整个集群的元数据管理和服务协调。它承担着以下功能：
作为catalog manager，master节点管理着集群中所有table和tablet的schema及一些其他的元数据。
作为cluster coordinator，master节点追踪着所有server节点是否存活，并且当server节点挂掉后协调数据的重新分布。
作为tablet directory，master跟踪每个tablet的位置。
### Catalog Manager
Kudu的master节点会持有一个单tablet的table——catalog table，但是用户不能直接访问。
master将内部的catalog信息写入该tablet，并且将整个catalog的信息缓存到内存中。
元数据信息占用的空间不大，所以master不容易存在性能瓶颈。
catalog table保存了所有table的schema的版本以及table的状态（创建、运行、删除等）。
### Cluster Coordination
Kudu集群中的每个tablet server都需要配置master的主机名列表。
当集群启动时，tablet server会向master注册，并发送所有tablet的信息。
tablet server第一次向master发送信息时会发送所有tablet的全量信息，后续每次发送则只会发送增量信息，仅包含新创建、删除或修改的tablet的信息。 
作为cluster coordination，master只是集群状态的观察者。对于tablet server中tablet的副本位置、Raft配置和schema版本等信息的控制和修改由tablet server自身完成。master只需要下发命令，tablet server执行成功后会自动上报处理的结果。
### Tablet Directory
因为master上缓存了集群的元数据，所以client读写数据的时候，肯定是要通过master才能获取到tablet的位置等信息。
但是如果每次读写都要通过master节点的话，那master就会变成这个集群的性能瓶颈，所以client会在本地缓存一份它需要访问的tablet的位置信息，这样就不用每次读写都从master中获取。
因为tablet的位置可能也会发生变化（比如某个tablet server节点crash掉了），所以当tablet的位置发生变化的时候，client会收到相应的通知，然后再去master上获取一份新的元数据信息。
### Tablet存储
tablet存储主要想要实现的目标为：
* 快速的列扫描
* 低延迟的随机读写
* 一致性的性能

### RowSets
在Kudu中，tablet被细分为更小的单元，叫做RowSets。
一些RowSet仅存在于内存中，被称为MemRowSets，
而另一些则同时使用内存和硬盘，被称为DiskRowSets。
任何一行未被删除的数据都只能存在于一个RowSet中。 
无论任何时候，一个tablet仅有一个MemRowSet用来保存插入的数据，并且有一个后台线程会定期把内存中的数据flush到硬盘上。
当一个MemRowSet被flush到硬盘上以后，一个新的MemRowSet会替代它。
而原有的MemRowSet会变成一到多个DiskRowSet。
flush操作是完全同步进行的，在进行flush时，client同样可以进行读写操作。
### MemRowSet
MemRowSets是一个可以被并发访问并进行过锁优化的B-tree，主要是基于MassTree来设计的，但存在几点不同：
Kudu并不支持直接删除操作，由于使用了MVCC，所以在Kudu中删除操作其实是插入一条标志着删除的数据，这样就可以推迟删除操作。
类似删除操作，Kudu也不支持原地更新操作。
将tree的leaf链接起来，就像B+-tree。这一步关键的操作可以明显地提升scan操作的性能。
没有实现字典树（trie树），而是只用了单个tree，因为Kudu并不适用于极高的随机读写的场景。
与Kudu中其他模块中的数据结构不同，MemRowSet中的数据使用行式存储。因为数据都在内存中，所以性能也是可以接受的，而且Kudu对在MemRowSet中的数据结构进行了一定的优化。
### DiskRowSet
当MemRowSet被flush到硬盘上，就变成了DiskRowSet。当MemRowSet被flush到硬盘的时候，每32M就会形成一个新的DiskRowSet，这主要是为了保证每个DiskRowSet不会太大，便于后续的增量compaction操作。
Kudu通过将数据分为base data和delta data，来实现数据的更新操作。
Kudu会将数据按列存储，数据被切分成多个page，并使用B-tree进行索引。
除了用户写入的数据，Kudu还会将主键索引存入一个列中，并且提供布隆过滤器来进行高效查找。
### Compaction
为了提高查询性能，Kudu会定期进行compaction操作，合并delta data与base data，对标记了删除的数据进行删除，并且会合并一些DiskRowSet。
### 分区
和许多分布式存储系统一样，Kudu的table是水平分区的。
BigTable只提供了range分区，Cassandra只提供hash分区，而Kudu提供了较为灵活的分区方式。
当用户创建一个table时，可以同时指定table的的partition schema，partition schema会将primary key映射为partition key。一个partition schema包括0到多个hash-partitioning规则和一个range-partitioning规则。通过灵活地组合各种partition规则，用户可以创造适用于自己业务场景的分区方式。

## Kudu的应用
Kudu的应用场景很广泛，比如可以进行实时的数据分析，用于数据可能会存在变化的时序数据应用等，甚至还有人探讨过使用Kudu替代Kafka的可行性。
[KUDU VS HBASE](https://bigdata.163.com/product/article/15)

# HBASE  
hbase 和 ElasticSearch的组件介绍就略过了，这里只讲为什么 这两种组件有时也会被认为是文件格式的一种。
hbase是个构建hdfs上的nosql数据库，其底层文件格式是sequencefiles
相对于hive，hbase中的数据表其实是独立的，HBase利用Hadoop MapReduce来处理HBase中的数据（星环的hyperbase用spark作为计算引擎）。
Hadoop HDFS为HBase提供了高可靠性的底层存储支持，Hadoop MapReduce为HBase提供了高性能的计算能力，Zookeeper为HBase提供了稳定服务和failover机制。	Pig和Hive还为HBase提供了高层语言支持，使得在HBase上进行数据统计处理变的非常简单。 Sqoop则为HBase提供了方便的RDBMS（关系型数据库）数据导入功能，使得RDBMS数据向HBase中迁移变的非常方便。
我们常使用的hive提供对hbase的数据表的SQL语言支持，所以有hbase格式的hive表这么一种说法。在使用上，可以认为hive中基于hbase中的数据表的表是一种映射表，类似于hive中构建映射txt表，所以hbase也被认为是hive支持的一种数据存储格式。
# ElasticSearch
ElasticSearch已经可以与YARN、Hadoop、Hive、Pig、Spark、Flume等大数据技术框架整合起来使用，尤其是在添加数据的时候，可以使用分布式任务来添加索引数据，使用Hive操作ElasticSearch中的数据，将极大的方便开发人员。 
HIVE支持创建ES的映射表，语法类似hbase映射表,因此ES也经常会被视作hive支持的一种数据格式。