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

### Using line_profiler for line-by-line Measurement

安装：`pip install line_profiler`

使用：在要分析的函数上面使用`@profile`装饰器，用`kernprof.py`（windows里面有`kernprof.exe`）来执行我们的代码。

加上`@profile`装饰器之后，才能产生统计信息。

`-o`参数会输出lprof统计文件，可以通过`python -m line_profiler script_to_profile.py.lprof`来读取。

### Using memory_profiler to Diagnose Memory Usage

安装：`pip install memory_profiler`

使用：类似`line_profiler`，也使用`@profile`装饰器来标示出需要分析的函数。加上`@profile`装饰器之后，才能产生统计信息。

通过`python -m memory_profiler script.py`来产生指定函数的分析结果，然后使用`mprof run script.py`(mprof只有*unix系统支持)产生一个统计数据文件，然后使用`mprof plot stat.data`来进行可视化展示。

为了更好的在函数级观察代码行为，我们可以通过上下文管理器（context manager）来增加label：

```
@profile
def some_func():
	with profile.timestamp("label_name"):
		#do somthing in the func
		pass
```

__tracemalloc__

这个包是python3.4开始提供的标准库，用于跟踪内存分配等操作，提供功能：

* 跟踪一个对象在哪里被分配
* 统计每一个文件、每行代码分配的内存块：分配的内存块的总大小、数量和平均大小
* 对比两个snapshots，检测内存漏洞

### Inspecting Objects on the Heap with heapy

Guppy项目有一个堆（heap）检测工具，叫做`heapy`，这个项目我们可以看到Python堆上的__对象__的数量和大小，看看解释器里面和理解内存中存在的东西有助于解决很困难的调试问题，你真正需要知道有多少对象正在使用，以及他们是否在适当的时间收集垃圾。

安装：`pip install guppy`，安装guppy包，来获得`heapy`。

使用方法，见示例代码：

```
def func():
   ...
   from guppy import hpy
   hp = hpy()
   print("heap info:")
   h = hp.heap()
   print h
   ...
```

如果同一个代码里面用多个`hp.heap()`，则后面的堆可能会包含前面的，所以信息有点重复，可以使用`hpy.setrelheap()`来设置断点，`hp.heap()`产生的堆是从整个checkpoint开始的，所以只是阶段的信息，不重复。

Windows python3.5 安装失败

### Using dowser for Live Graphing of Instantiated Variables

`dowser`在当前运行代码的命名空间增加了钩子，提供实时的实例化变量视图（通过`CherryPy`接口）

安装：`pip install dowser` (`CherryPy`是依赖)

使用；代码示例：

```
def launch_memory_usage_server(port=8080):
    import cherrypy
    import dowser
    cherrypy.tree.mount(dowser.Root())
    cherrypy.config.update({
        'environment': 'embedded',
        'server.socket_port': port
    })
    cherrypy.engine.start()
def other func():
    ...
    launch_memory_usage_server()
    ...
```

Windows python3.5 安装失败

> __`CherryPy`说明__
>
> 面向对象的HTTP框架，拥有python语言规范，可以去看看代码。下面是一些特点：
>
> * 构建Web应用和构建其他面向对象程序采用一样的方式
> * 这个设计的目标是减少代码、增加可读性，从而使开发更加快速
> * 运行十多年来，证明了这个库快而稳定。也在很多站点已经证明。
>
> 代码实例：
>
> ```python
> import cherrypy
>
> class HelloWorld(object):
>     @cherrypy.expose
>     def index(self):
>         return "Hello World!"
>
> cherrypy.quickstart(HelloWorld())
> ```

### Using the dis Module to Examine CPython Bytecode

使用`dis.dis(func)`来输出某个指定函数的`bytecode`。

安装：`pip install dis`

使用：如上所示，输出第一列是代码的行数，第二列指定的是jump的位置（`>>>`）,第三列是指令名称，后面的是处理的参数和一些说明。

### Unit Testing During Optimization to Maintain Correctness

使用`coverage.py`来进行覆盖度测试，看看哪些地方没有被测试覆盖到。

在使用`@profile`装饰器的时候，同时使用单元测试，需要注意的是需要重新包装`@profile`，单元测试不会把这个装饰器注入程序，所以单元测试会报错。需要no-op。

例如：

```python
if '__builtin__' not in dir() or not hasattr(__builtin__, 'profile'):
    def profile(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner
```

### Strategies to Profile Your Code Successfully

由于芯片的加速机制，可能Cool CPU比Hot CPU有更好的性能——对同一段代码来说。操作系统也会有同样的一些机制，例如：例如笔记本使用电池时和使用直接电源时对CPU的控制的差异，为了构建一个稳定的标尺，可以禁用这些软硬件自己的一些优化机制。

## Lists and Tuples

不管`list`还是`tuple`都是一类数据结构——`array`，`list`是动态数组，而`tuple`是静态数组。但是他们的检索特定位置的数据耗费都是`O(1)`。

当创建一个`array`（无论`list`或者`tuple`）时，我们首先分配一个系统内存块（这块内存每一个section用来存储一个整数大小的指针指向实际数值）。Python的`list`存储数组大小，所以长度为5的`list`会分配6个block，第一个是长度。

`array`里面实际存储的是真是值的位置，每个位置存储叫做一个`bucket`，找到第一个`bucket`的位置位`M`，如果想要检索第`i`个元素，则元素所在位置的`bucket`为`M+i`。使用`tracemalloc`查看，`list`大小只是元素个数的大小，上面的`block`和这里的`bucket`的关系需要继续考究。

```python
>>> import tracemalloc
    tracemalloc.stop()
    tracemalloc.start(2)
    l5=[]
    snapshot = tracemalloc.take_snapshot()
    stas=snapshot.statistics('lineno')
    stas[-1]
Output: <Statistic traceback=<Traceback (<Frame filename='<ipython-input-37-1e09d79c3ce8>' lineno=5>,)> size=4 count=1>
```

#### A More Efficient Search

可以自定义对象，使用`__eq__和__lt__`来做用户自定义对象的比对。

可以在创建list的时候就进行排序，这样在通过value来检索数据的时候就可以使用二分法来检索，增进效率。

Python标准库`bisect`可以保证插入数组的时候是有序的，检索也会采用最优化的二分法。例如：

```python
>>> import bisect
    import random
    def f(count=100000, isbisect=False):
    numbers = []
    for i in range(count):
        value = random.randint(count*-1, count)
        if not isbisect:
            numbers.append(value)
        else:
            bisect.insort(numbers, value)
    return numbers
    n1 = f()
    n2 = f()
>>> %timeit n1=f()
1 loops, best of 3: 534 ms per loop
>>> %timeit n2=f(isbisect=True)
1 loops, best of 3: 2.23 s per loop
>>> %timeit n1.index(99999)
1000 loops, best of 3: 1.65 ms per loop
>>> %timeit bisect.bisect(n2, 99999)
The slowest run took 7.88 times longer than the fastest. This could mean that an intermediate result is being cached 
1000000 loops, best of 3: 1.3 µs per loop
```

可以看到`bisect`在插入数据时的低效和在检索上的高效，所以需要根据自己的所处的场景来进行具体应用的考量。

### Lists Versus Tuples

`list`和`tuple`使用相同的底层数据结构，但有下面几点差异：

* `List`是动态的，一旦创建成功，可以改变元素的个数，mutable
* `tuple`是静态的，一旦创建成功，则不可以改变元素的个数，immutable（元素值也不能修改）
* `tuple`在python运行期间，是被缓存起来，意味着不需要在使用时再要求内核保留内存

最后一点，Python运行时缓存，具体是缓存在哪里？python虚拟机的机制需要了解。

这两个类型都可以存不同的类型（mix types），但是保持类型的一致可以减少一些存储和计算的开销。一些其他库：`blist`和`array`也可以缩减这种开销。`blist`不是标准库，需要[安装](https://pypi.python.org/pypi/blist/1.3.6)。

`blist`通过使用array/tree的数据结构来优化remove的效率，所以`list`太大而且经常删数据，则比较有优势。而且它也维持了一个`bisect`，所以查找效率也可以保障。




