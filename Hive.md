#Hive
[Hive Wiki](https://cwiki.apache.org/confluence/display/Hive/Home)

###Apache Hive
Apache Hive是数据仓库软件，查询分布式存储系统的大数据集，提供以下工具：
* 可以进行简单的数据ETL
* 将各种格式的数据结构化
* 可以访问HDFS的文件，也可以处理HBase的数据
* 通过MR来查询数据

Hive可以和Hadoop、HBase整合，下面是Hive和HBase整合的使用方法，如果Hbase是单节点，则可以使用Hive Cli命令访问Hbase：
`$HIVE_SRC/build/dist/bin/hive --auxpath $HIVE_SRC/build/dist/lib/hive-hbase-handler-0.9.0.jar,$HIVE_SRC/build/dist/lib/hbase-0.92.0.jar,$HIVE_SRC/build/dist/lib/zookeeper-3.3.4.jar,$HIVE_SRC/build/dist/lib/guava-r09.jar --hiveconf hbase.master=hbase.yoyodyne.com:60000`
如果HBase使用分布式集群，三个ZK的quorum 机器，则用下列命令：
`$HIVE_SRC/build/dist/bin/hive --auxpath \$HIVE_SRC/build/dist/lib/hive-hbase-handler-0.9.0.jar,$HIVE_SRC/build/dist/lib/hbase-0.92.0.jar,$HIVE_SRC/build/dist/lib/zookeeper-3.3.4.jar,$HIVE_SRC/build/dist/lib/guava-r09.jar --hiveconf hbase.zookeeper.quorum=zk1.yoyodyne.com,zk2.yoyodyne.com,zk3.yoyodyne.com
`
详见[HBase Integration](https://cwiki.apache.org/confluence/display/Hive/HBaseIntegration#HBaseIntegration-Usage)

##Hive Programming总结
###Introduce
Hive提供了SQL查询来查找存储于hadoop的数据——HiveQL（Hive Query Language）
Metastore是一个单独的关系型数据库，用来存储hive的元数据
相比于Hive，HBase提供了行级的更新（row update）
`hive.metastore.warehouse.dir` 存储hive数据的目录
###CLI
`hive --define name=value`可以用这个给hive的cli里面传参，参数名为`name`，值为`value`
`--define`等价于`--hivevar`
`hive --hiveconf name=value`可以用这个来设置hive的配置参数（也可以是其他值，一般是配置）（define、hivevar、hiveconf都是变量的不同命名空间，而不同命名空间起到的作用不同，例如hiveconf对应的就是hive的配置参数）
  `hive -e "select * from tb"` 参数`-e`直接跟查询语句，`-S` 以silent方式将结果展示——不显示Ok、耗时等说明信息
  `hive -f file.hql` 执行hiveql脚本，或者在命令行内执行`source file.hql`
  **貌似新版的hive中没有src表了，可以自己创建一个dual来作为默认的测试表**
  `.hiverc`在hive执行之前执行，可以用于配置参数（语法还是hive的语法），也可以用`hive -i file` 来指定文件
>hive 提供自动缩进
>hive 提供直接执行shell命令，例如：`!pwd;`
>hive 直接执行hadoop命令，例如：`dfs -ls /;`
>hive 注释，类似oracle ——`--`
###Programming
####Data Type
#####Bae type
|Type|Size|Example|
|:---:|:--|:-----|
|tinyint|1 byte signed integer|11|
|smallint|2byte signed integer|20|
|int|4 byte signed integer|20| 
|bigint|8 byte signed integer|20|
|boolean|boolean true or false|true|
|float|single precision floating point|3.14159|
|double|double precision ..|3.14159|
|string|sequence of characters|'this is a man'|
|timestamp|integer,float,string|1327882394 (Unix epoch seconds),1327882394.123456789 (Unix epochseconds plus nanoseconds), and '2012-02-0312:34:56.123456789' (JDBCcompliantjava.sql.Timestampformat) |
|binary|array of bytes||
*这些类型都是会用Java实现的* `cast(s as float)`cast来进行类型转换，从小的类型转到大的类型

#####Collection type
|Type|Description|Example|
|:---:|:--|:-----|
|struct|like C,字段通过`.`来获得|struct('John', 'Doe')|
|map|使用数据型获得['key'],map是成对出现，第一个作为key，第二个作为value|map('first', 'John', 'last', 'Doe')|
|array|通过[index]来获得值|array('John','Doe')|
**将这些collection字段嵌入到表类型中，可以减少磁盘查找（因为减少了外键关联），所以提升了速度**
>用于创建表结构
`CREATE TABLE employees (
name STRING,
salary FLOAT,
subordinates ARRAY<STRING>,
deductions MAP<STRING, FLOAT>,
address STRUCT<street:STRING, city:STRING, state:STRING, zip:INT>)
row format delimited
fields terminatedby '\001'
collection items terminated by '\002'
map keys terminated by '\n'
stored as textfile 
;`

默认的文件分隔符：
* $\n$ 每一行表示一个record
* $^A(control A)$ 区分feilds，字段分隔符，octal code为`\001`
* $^B $ 区分元素是在一个array、struct或map中，octal code为`\002`
* $^C$ 分开key和value，在map中，`\003`

>数据示例：
`John Doe^A100000.0^AMary Smith^BTodd Jones^AFederal Taxes^C.2^BState
Taxes^C.05^BInsurance^C.1^A1 Michigan Ave.^BChicago^BIL^B60600
Mary Smith^A80000.0^ABill King^AFederal Taxes^C.2^BState Taxes^C.
05^BInsurance^C.1^A100 Ontario St.^BChicago^BIL^B60601
Todd Jones^A70000.0^AFederal Taxes^C.15^BState Taxes^C.03^BInsurance^C.
1^A200 Chicago Ave.^BOak Park^BIL^B60700
Bill King^A60000.0^AFederal Taxes^C.15^BState Taxes^C.03^BInsurance^C.
1^A300 Obscure Dr.^BObscuria^BIL^B60100`
相对应的Json数据：
`{
	"name": "John Doe",
	"salary": 100000.0,
	"subordinates": ["Mary Smith", "Todd Jones"],
	"deductions": {
	"Federal Taxes": .2,
	"State Taxes": .05,
	"Insurance": .1
},
	"address": {
	"street": "1 Michigan Ave.",
	"city": "Chicago",
	"state": "IL",
	"zip": 60600
	}
}`
>但是奇怪的是为什么`\033`这种说是非单字符呢？

传统的数据库，数据库文件只有数据库能操作，而hive的数据库文件可以用任何方式修改。这就叫：$schema  on  read$
###一些配置
* $hive.cli.print.header$ 表示打印查询结果是否打印列头信息
  


