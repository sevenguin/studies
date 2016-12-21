# High Performance Python

## Understanding Performant Python

#### Computing Units

对于多核CPU，Python的一个限制是使用GIL（Global interpreter lock），GIL确保Python进程一次只能运行一个指令，不管现在正在使用的核数。为了解决这个问题，可以使用：multiprocessing或者如numexpr、Cpython或分布式计算模型。

#### Memory Units

一般来说一次读取大量的数据比一点一点读取效率更高（前者连续读取，后者随机读取），但是具体对各种存储设备来说（CPU寄存器、Memory或磁盘）影响可能各有不同。

存储单元很明显是分层结构，数据原来位于磁盘，然后根据需要加载到内存、L1/L2缓存。所以在进行__Memory优化__时，唯一需要考虑就是：优化数据存储位置，数据的布局以及在各个层级进行移动的次数。

#### Communications Layers

所有的连接都叫做bus，只是根据不同的层级叫不同名字而已。

GPU的缺点都来自于其一般作为外围设备，所以连接GPU和Memory Units的bus是PCI bus，效率比较低，不想fronted bus——连接CPU L1/L2、memory Units的bus。

