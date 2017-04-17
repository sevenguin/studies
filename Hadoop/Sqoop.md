#Sqoop

@(大数据)

Sqoop的任务是在在Hadoop和关系型数据库之间传输数据。
Sqoop分两个版本，Sqoop1和Sqoop2，Sqoop1的版本对应到1.4.x；Sqoop2的版本对应到1.99.x。
1和2的版本差异较大，而且不兼容。
下面是安装Sqoop步骤：
1、下载解压Sqoop1.99.x
2、配置环境变量.bash_profile,并`source .bash_profile`使其生效，配置如下：

> export SQOOP_HOME=sqooppath
> export PATH = sqooppath/bin:$PATH
> export CATALINA_BASE=sqooppath/server
> export LOGDIR=$SQOOP_HOME/logs/

3、修改`server/conf/sqoop.properties`，属性`org.apache.sqoop.submission.engine.mapreduce.configuration.directory`为hadoop配置文件目录
4、修改`server/conf/catalina.properties `属性`common.loader`为hadoop的所有jar包路径
`common.loader=HADOOP_HOME/share/hadoop/common/*.jar,HADOOP_HOME/share/hadoop/common/lib/*.jar,HADOOP_HOME/share/hadoop/hdfs/*.jar,HADOOP_HOME/share/hadoop/hdfs/lib/*.jar,HADOOP_HOME/share/hadoop/mapreduce/*.jar,HADOOP_HOME/share/hadoop/mapreduce/lib/*.jar,HADOOP_HOME/share/hadoop/tools/*.jar,HADOOP_HOME/share/hadoop/tools/lib/*.jar,HADOOP_HOME/share/hadoop/yarn/*.jar,HADOOP_HOME/share/hadoop/yarn/lib/*.jar,HADOOP_HOME/share/hadoop/httpfs/tomcat/lib/*.jar`
5、将SQL驱动包放入server/lib下（如果在创建连接时，写如JDBC Driver Class时报错
$No class Found$，
那也把这个驱动放到server/webapp/WEB-INF/lib下）
6、参照：http://sqoop.apache.org/docs/1.99.6/Sqoop5MinutesDemo.html步骤

Oracle（ojdbc.jar)的JDBC Driver Class和JDBC Connection String：
* ***Driver Class:*** oracle.jdbc.driver.OracleDriver
* ***Connection String: *** jdbc:oracle:thin:@ip:port:sid（port必须指定，不然会连接失败， 1521）

Mysql：
* ***DriverClass:*** com.mysql.jdbc.Driver
* ***Connection String:*** jdbc:mysql://ip:port/database (port 需要指定，3306)

DB2：
* ***DriverClass:*** com.ibm.db2.jcc.DB2Driver
* ***Connection String:*** jdbc:db2://ip:port/dbname)

HDFS：
HDFS URI： `hdfs://host:8020/`

一些命令：
`create link -c connector_ID`  创建连接
`update link -l link_id` 更新连接
`create job -f from_link_id -t to_link_id`  创建job时，from从oracle的话，schema就是用户名，表名不用带用户了

Oracle中Schema作为一数据库对象的集合，一个用户对应一个Schema，该用户的Schema名等于用户名。

如果报错，则注意配置log目录下的sqoop.log文件记录最新的日志信息；如果表没有ID字段会报错，因为他会查找：`SELECT MAX(ID),MIN(ID) from user.dbname`——这里写的有问题，这里的ID是分区字段，是在创建job的时候指定的：$Partition Column name$设置基于分区的字段名
设定Job时，SQL Statement必须指定conditions——`where (congdition)`

`start job` 时报错`FileNotFoundException File does not exists: hdfs://.....`
--由于实际的mapper执行都是在datanode上，而job的这些类在本地，mapper执行时肯定会出错，唯一的解决办法就是把这些jar包放到hdfs所指的路径。把server/lib/*.jar 和server/webapps/sqoop/WEB-INF/lib/*.jar 放进去

Sqoop对两个数据源数据进行转义，两个数据源就配置成link（使用connector来分类），然后创建job，job对应两个link（一个源、一个目的地）


