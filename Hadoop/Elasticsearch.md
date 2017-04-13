## Elasticsearch集群安装过程

一些资源：

https://es.xiaoleilu.com/index.html

### ElasticSearch集群介绍

ElasticSearch集群中可以监控统计很多信息，但是最重要的是集群建康，集群建康分为三种状态：green/yellow/red.可以通过restful请求获得：`/_cluster/health`。

节点分为三类：master、data和client。master不做检索和存储数据，data是存储和检索，client是接入节点，而且client也分两种，一种是纳入集群，一种是不纳入集群。

一个节点就是一个服务器（当然可以复用），每一个节点都可以和其他节点连接，也都知道文档在哪里，所以节点可以转发请求。

ElasticSearch中的数据结构和关系型数据库中的对比：

在Elasticsearch中，文档归属于一种**类型(type)**,而这些类型存在于**索引(index)**中，我们可以画一些简单的对比图来类比传统关系型数据库：

```
Relational DB -> Databases -> Tables -> Rows -> Columns
Elasticsearch -> Indices   -> Types  -> Documents -> Fields
```

### Elasticsearch 安装

1. 下载ElasticSearch，注意版本，ElasticSearch5.x的需要Java 8，如果你的环境是Java7，则选择ElasticSearch2.x版本，下载地址：https://www.elastic.co/downloads/past-releases（这里可以选择下载的软件和版本）
2. 解压 `tar -xzv elasticsearch-XXXX.tar.gz`
3. 配置`config/elasticsearch.yml`

```yaml
# 这个yaml配置格式需要注意的一点是，':'后面必须有一个空格
cluster.name: cluster_name # cluster就是按照相同的name来组集群的，所有节点有相同的集群名称
node.name: node-1
# path.data和path.logs这两个配置配置数据和日志的目录
path.data: /home/username/data
path.logs: /home/username/logs
http.port: 9200
network.host: 0.0.0.0
transport.tcp.port: 9330
node.master: false
node.data: true
discovery.zen.ping.unicast.hosts: ["cdh-worknode2"] # 配置当新机电加入时连入的机器
discovery.zen.ping.multicast.enabled: true
```

4. 启动`bin/elasticsearch`

### Kibana 安装

1. 下载Kibana， 地址：https://www.elastic.co/downloads/past-releases（这里可以选择下载的软件和版本）
2. 解压
3. 配置，需要修改的是`elasticsearch.url: 'http://cdh-worknode2:9200'`，配置好ElasticSearch的http请求地址就可以了
4. 启动`bin/kibana`

username什么的现在没用，也没配置。

### Marvel 安装

​     这个本来可以在线安装，使用`bin/kibana plugin`和elasticsearch中的`plugin`来安装，但是如果是离线环境则下面方法：

​     文档可参见：https://www.elastic.co/guide/en/marvel/current/installing-marvel.html#offline-installation

1. 下载，需要下载三个东西：
   1. https://download.elastic.co/elasticsearch/release/org/elasticsearch/plugin/license/2.4.4/license-2.4.4.zip
   2. https://download.elastic.co/elasticsearch/release/org/elasticsearch/plugin/marvel-agent/2.4.4/marvel-agent-2.4.4.zip
   3. https://download.elasticsearch.org/elasticsearch/marvel/marvel-2.4.4.tar.gz
2. 分两步：
   1. 在ElasticSearch中运行：`bin/plugin install file:///path/to/file/license-2.4.4.zip;bin/plugin install file:///path/to/file/marvel-agent-2.4.4.zip`
   2. 在Kibana中运行：`bin/kibana plugin --install marvel --url file:///path/to/file/marvel-2.4.4.tar.gz`

### 和Hive结合使用

需要下载elasticsearch-hadoop的包，这个程序向下兼容，所以5.x的包可以兼容ElasticSearch的2.x版本，详细见git地址：

https://github.com/elastic/elasticsearch-hadoop

下载完之后，里面是针对hadoop生态里面各个系统的jar包，可以使用这些jar包来和hadoop生态里面这些产品进行数据互通，例如：hive中写入数据，ElasticSearch中可以看到，反之亦然。

和hive结合使用过程如下：

```shell
sh$ hive
hive> add jar /path/to/elasticsearch-hadoop-dir/elasticsearch-hadoop-hive-5.3.0.jar
hive> create external table user(id int, name string) stored by 'org.elasticsearch.hadoop.hive.EsStorageHandler' tblproperties('es.resource'='index/document', 'es.nodes'='cdh-worknode2', 'es.port'='9200', 'es.nodes.wan.only'='true', 'es.index.auto.create'='true');  
hive> select * from user;   # 可以查询ElasticSearch中的数据了
hive> insert overwrite table user select s.id, s.name from user_source;  # 从user_source中数据插入user中
```

