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

## Performing to Find Bottlenecks

优化之前先要进行perform的检测，知道程序的瓶颈在哪里，这样才能有的放矢的进行优化工作。

### Simple Approaches To Timming--print and Decorator

使用`time.time()`来对进行性能评估，在测量一个函数的perform时，可以使用装饰器（decorator）：

```
from functools import wraps
def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print("@timefn:" + fn.func_name + " took " + str(t2 - t1) + " seconds")
        return result
    return measure_time
@timefn
def some_func(*args, **kwargs):
    pass
```

也可以使用`timeit`模块来粗粒度的测量CPU-bound方法的执行速度。

IPython和Anaconda中的qt-console中都可以使用`%timeit`直接通过交互式的方式来测量某个语句的执行速度。`%%timeit`可以测量语句块。

也可以使用Linux下的`/usr/bin/time`(注意要带上路径`time`直接使用无法度量，但是`which time`显示的就是`/usr/bin/time`，这点很奇怪)，例如：

```
$ /usr/bin/time -p python julia1_nopil.py
Length of x: 1000
Total elements: 1000000
calculate_z_serial_purepython took 12.7298331261 seconds
real 13.46
user 13.40
sys 0.04
```

其中的option`-p`，表示：

* 真实的记录所花费的时间
* user记录的是非核函数消耗时间
* sys记录的是核函数消耗时间

user+sys和real的查可能是I/O消耗的时间，也可能是告诉你当前系统正在忙着处理其他的程序。`time --verbose`可以获得更多的信息（time也包含了python的启动时间）。

### Using the cProfile Module

一个好的习惯是，在profile自己的程序之前，先猜测自己代码各个部分的运行速度。（打印有疑问的程序片段，并注释标明，profile的时候可以加以验证）这样可以提升自己对固定编码风格的直觉。也可以有助于深层次的理解效率低下问题底层的原因，这样优化起来事半功倍。

cProfile是三个profilers标准库之一：cProfile、hotspot、profile.hotspot。默认使用cProfile。

使用方法：

```
$ python -m cProfile -s cumulative some.py
```

其中`-s cumulative`表示的是按照累计消耗时间排序。可以列出各个函数所消耗的时间。

