# High Performance Python

## Understanding Performant Python

#### Computing Units

对于多核CPU，Python的一个限制是使用GIL（Global interpreter lock），GIL确保Python进程一次只能运行一个指令，不管现在正在使用的核数。为了解决这个问题，可以使用：multiprocessing或者如numexpr、Cpython或分布式计算模型。

#### Memory Units

一般来说一次读取大量的数据比一点一点读取效率更高（前者连续读取，后者随机读取），但是具体对各种存储设备来说（CPU寄存器、Memory或磁盘）影响可能各有不同。

存储单元很明显是分层结构，数据原来位于磁盘，然后根据需要加载到内存、L1/L2缓存。所以在进行__Memory优化__时，唯一需要考虑就是：优化数据存储位置，数据的布局以及在各个层级进行移动的次数。

#### Communications Layers

所有的连接都叫做bus，只是根据不同的层级叫不同名字而已。

GPU的缺点都来自于其一般作为外围设备，所以连接GPU和Memory Units的bus是PCI bus，效率比较低，不像fronted bus——连接CPU L1/L2、memory Units的bus。Putting the Fundamental Elements Together

考虑找到一个将计算组件组合在一起最好的解决方法，明白python底层到底如何处理，可以逐步的使我们的python代码优化。所以需要考虑面对问题的解决方案（拆分成运算组件）以及python运行机制，结合这两者来不对进行代码优化。

和分布式类似，减少数据的传输（不同的是，这里不是网络传输，而是存储器之间的传输），尽量使一个指令执行多个数据。__传输运算而不是数据__。

numpy：执行运算更快；pandas：处理数据更加方便，所以这可能就是numpy和pandas的差异。

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

IPython和Anaconda中的qt-console中都可以使用`%timeit`直接通过交互式的方式来测量某个语句的执行速度。

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

user+sys和real的差可能是I/O消耗的时间，也可能是告诉你当前系统正在忙着处理其他的程序。`time --verbose`可以获得更多的信息（time也包含了python的启动时间）。

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

加上`@profile`装饰器之后，才能产生统计信息。`kernprof -l -v profile.py`直接看

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

`List`的mutable是以memory和computation作为代价的

### Lists as Dynamic Arrays

`List`是会分配M（M>N）个存储空间给它，然后当元素数N==M的时候，创建一个新的`List`，然后分配M个空间，然后将原来的`List`复制过去，新的M大于当时的长度N。在2.7时，M的计算方式是：

```python
M = (N >> 3) + (N < 9 ? 3 : 6)
```

### Tuples As Static Arrays

`Tuple`是静态的，但是可以相加来扩充：`t1+t2`，具体底层操作和`List`resize一致，就是没有额外的内存分配。

还有一点需要注意，Python是提供垃圾回收机制的，当你不使用一个对象时进行垃圾回收释放内存。但是对于大小为1~20的`tuple`（不同版本可能会做大小调整），如果不使用时不会立刻进行回收，而这部分内存是保留起来供以后可能使用。这就是说如果以后有新的`tuple`要创建，则可以直接使用这个内存，而不需要跟OS交流，申请内存。所以之前说的reserve memory就是这个了。所以相对于`List`每次都需要和OS先做一下申请，`Tuple`就会快那么一丢丢。

```python
>>> %timeit l = [0,1,2,3,4,5,6,7,8,9] 
   1000000 loops, best of 3: 697 ns per loop
>>> %timeit t = (0,1,2,3,4,5,6,7,8,9)
   10000000 loops, best of 3: 23.1 ns per loop
```

对比上面，差别还是比较大的。

## Dictionaries and Sets

`set`和`dictionary`不像`tuple`和`list`，有固定的顺序（可以使用元素位置来索引），但是他们有固定的值来索引——`key`。其中`set`没有`value`，只有`key`。

> 一个`hashable`类型，是实现了`__hash__`这个_magic function_，也实现了`__eq__`或`__cmp__`

`Dictionary`和`Set`都有一个花销，由于要保存`key`，所以会有多余的内存开销，而且虽然检索是`O(1)`，但是具体的索引时间还是要看`hashable`函数。

对比下面两个做法，就能体会到选择不同数据结构存储对性能的影响了：

```python
# phonebook中first name重，phonename的形式：[(name, phoneno)]
>>> def f_list(phonebook):
        unique_names = []
        for name, phone in phonebook:
            f_name = name.split(' ', 1)[0]
            if f_name not in unique_names:    # 这个应该也是一个O(n)的算法，遍历列表
                unique_names.append(f_name)
        return len(unique_names)
>>> def f_set(phonebook):
        unique_names = set()
        for name, phone in phonebook:
            f_name = name.split(' ', 1)[0]
            unique_names.add(f_name)
        return len(unique_names)
>>> phonebook = [
    ("John Doe", "555-555-5555"),
    ("Albert Einstein", "212-555-5555"),
    ("John Murphey", "202-555-5555"),
    ...
    ("Albert Rutherford", "647-555-5555"),
    ("Elaine Bodian", "301-555-5555")]   # 29071个元素
>>> %timeit f_list(phonebook)
   1 loops, best of 3: 1.39 s per loop
>>> %timeit f_set(phonebook)
   10 loops, best of 3: 22.2 ms per loop
>>> len(phonebook)
   29071
```

对比两个方法，数据量如果很大的话，效率还是相差一个数量级的。

### How Do Dictionaries and Sets work?

`Dictionaries and Sets`都是通过`hash tables`来做到在查找和插入上的时间复杂度为`O(1)`。`hash function`将例如字符串、对象的key转换为对一个list的索引，从而有效的做到了这一点。

#### Inserting and Retrieving

key值先经过hash处理，在经过masked，mask保证最后结果在分配的buckets个数中。如果这个mask会根据内存分配大小变化，其实就是将key值映射成一个integer数字，这个数字可以索引buckets——如list般。这还么完，如果最后处理结果找到的bucket已经被用了(_hash collision_)，则对当前bucket中索引的value值（key/value的value）和目前我们要插入的value是否相等，如果相等则不更新（这个value对象使用`cmp`方法）直接返回。如果不等则使用一个线性函数继续找一个合适的值作为索引。如果最后处理结果找到的bucket没有使用，则直接插入值返回。

```python
# key处理过程的伪码
def index_sequence(key, mask=0b111, PERTURB_SHIFT=5): 
    perturb = hash(key) #
	i = perturb & mask
	yield i
	while True: 
        i=((i<<2)+i+perturb+1) 
        perturb >>= PERTURB_SHIFT
		yield i & mask
```

#### Deletion _(?)_

由于`NULL`值在探测hash collision时使用`NULL`作为标志值（不理解，前面也没看到记录，姑且记下来），所以deletion的使用一个特殊值来标识这个bucket为空，但是在解决hash collision时可能仍然被认作是有值（出现hash冲突时，还是不能使用？为什么要这样，既然已经空了？）。这里的空槽（empty slots）可以在将来使用（将来是什么时候），也可以在resize的时候被删除。

#### Resize

类似`list`这种方式，分配内存也是因为元素数增长存储整体数量也增长（只不过增长方式不同），而且一个关键点是，如果resize的时候，会重新将老的元素插入到新分配的空间中，所以index也是重新计算（因为mask的值因为分配bucket的数量变化而变化了），所以数据量大的时候效率会很低。resize不仅仅是insert，delete也会。

#### Hash Functions and Entroy

Python中的对象一般都是hashable，因为他们都有内建的`__hash__`和`__cmp__`函数关联。对于数值类型（`int or float`），hash值是简单的bit值；`Tuple`和`String`hash值基于他们的content。而`List`由于值会发生变化，所以不可以被hash（因为值变化，真求hash值则位置就会发生变化）。用户自定义的类有默认的`__hash__`和`__cmp__`，`__hash__`默认返回对象的内存位置（`id`得到的值），`__cmp__`默认比对的也是内存位置。（py2.6中并没有`__hash__`和`__cmp__`默认，py3.5中有，但是hash值并不是id还是有差别）。

### Dictionaries and Namespaces

在python的命名空间中也使用了Dictionary的O(1)检索的优点。

在使用一个变量、函数或模块（var，function，module）时，首先，会在`locals()`的字典中查找(python对这个做了足够多的优化），如果没找到去`globals()`中查找，如果还没找到，则在`__builtin__`模块的`locals()`中查找。看下面的代码类说明这个层次感：

```python
>>> import math
    from math import sin
    import dis
>>> def test1(x):
    	return math.sin(x)
>>> def test2(x):
    	return sin(x)
>>> def test3(x, sin=math.sin):
    	return sin(x)
>>> dis.dis(test1)
  6           0 LOAD_GLOBAL              0 (math)    # global lookup module math
              3 LOAD_ATTR                1 (sin)     # lookup the attribute
              6 LOAD_FAST                0 (x)       # local lookup(fast)
              9 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
              12 RETURN_VALUE
>>>  dis.dis(test2)
  2           0 LOAD_GLOBAL              0 (sin)     # explicit import the sin，then directly lookup sin
              3 LOAD_FAST                0 (x)       # local lookup(fast)
              6 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
              9 RETURN_VALUE
>>> dis.dis(test3)
  2           0 LOAD_FAST                1 (sin)     # local lookup(fast)
              3 LOAD_FAST                0 (x)       # local lookup(fast)
              6 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
              9 RETURN_VALUE
```

虽然`locals`返回一个`dictionary`，但是局部变量不需要在字典中查找，他们存储在一个非常小的数组中，查找速度会非常快。

当然，`test3`代码不那么`Pythonic`，如果函数内部迭代调用很多globa变量、函数，可以在函数内使用本地变量替换这些全局的变量：`local_var = global_var`，这样可以增加效率。（但是测试了一下，效率提升不是很显著，100W次的调用也就是`ms`级的改进）。

## Iterators and Generators

迭代器和生成器

创建迭代器之前需要先创建一个`list`，而generator是逐个创建并返回，所以在内存使用上generator更胜一筹，使用内部`__iter__`来使用iterator来进行`for ..in ..`循环。

> __两个比较__
>
> ```python
> >>> l = [1,2,3,4,5]
> >>> [i for i in l if i > 2]   # 注意，这里可以使用if呦
>     [3,4,5]   # 输出是一个list
> >> (i for i in l if i > 2)   # 注意这里的括号
>     <generator object <genexpr> at 0x03B370F0>    # 输出的是一个生成器
> ```

### Iterators for Infinite Series

`Generator`可以将数据产生和转换分成两个阶段，这样就可以选择将一个转换函数作用到一个新的数据集还是一个已经存在的数据集。

```python
def gen():
    for i in range(10):
        yield i
def trans():
    for d in gen():
        #do som trans
        pass
```

### Lazy Generator Evaluation

由于generator只是计算当前值，所以在某些情况可能比较难搞。但是`itertools`提供了很多办法。`built-in`也停工了一些内建的方法，如：`map,reduce,filter,zip`

## Matrix and Vector Computation

将复杂问题拆解成简单基本的事件来分析处理。

### Memory Fragmentation

由于Python中没有专门对vector的数据结构，在使用List时，其本身的特点限制了整体的效率。我们都知道，List中元素存储的不是实际的值，而是一个指针，指向实际值的位置，这会导致两个问题：增加检索次数；内存碎片。例如：在检索`data[2][4]`时，首先我们找到到`data`的第3个row，然后再通过这里存储的指针找到这个row的真正的值，然后在这个列表（值是列表）中找到第5个元素的位置，然后通过这个位置找时机值，所以总共多了两次检索。而且由于存储的是地址，实际值很可能存在内存的各个片段，所以在OS进行加载时并不能有效的预加载，这就造成了内存碎片的问题。

Linux中的`perf`命令可以有效的展示程序占用的资源，例如：

```shell
$perf stat -e cycles,stalled-cycles-frontend,stalled-cycles-backend,instructions,cache-references,cache-misses,branches,branch-misses,task-clock,faults,minor-faults,cs,migrations -r 3 python script.py
```

计算的向量化只能发生在相关数据都缓存在CPU cache中，而bus只能从连续的内存读取数据存储到CPU cache中，所以不连续的数据就没有办法缓存，也就没有办法向量化计算。

`array`可以解决内存碎片的问题，这个数据结构中存储的是数据值本身。但是Python并没有完全解决计算向量化，因为即使数据缓存了，Python仍然不知道如何向量化我们的循环。

由于`array`底层实现的原因，每次存取的时候会产生额外的消耗，所以`array`也不利于math方面的工作，更适合于`fixed-type`的数据——有效的内存处理（整体缓存）。

#### Enter numpy

`numpy`很好的解决了上述问题，存储数据在连续的内存块中，而且支持向量化操作。而且`numpy`拥有较好的操作性，不仅仅性能有保障，而且使用起来也更简单。

在使用list、array、numpy比对上，numpy最优，而且是成百倍的提升，array最差。

由于申请内存会需要经过和其他进程、kernel等来完成，所以相比预先分配好直接replace-in（改其中元素），效率会差很多.

#### numexpr: Making In-Place Operations Faster and Easier

numpy向量操作一次只能做一个计算，如果A\*B-C，则先进行A\*B然后存在临时vector中，然后再做后面的计算。

`numpyexpr`可以有效的进行整个向量运算，将其编译成有效的代码，更合适的内存、CPU处理。其中一个关键点就是`numpexpr`考虑了CPU cache，保证各个level的CPU cache存储适当的数据。

```python
from numexpr import evaluate
def evolve(grid, dt, next_grid, D=1):
    laplacian(grid, next_grid)
    evaluate("next_grid*D*dt+grid", out=next_grid)
```

当要处理的`grid`变大时，`numpexpr`就会显出其充分利用CPU cache的优势，体现出由于`pure numpy`的性能。

**结语**

综上，我们可以看到优化主要是两方面的工作：减少CPU获得数据的时间和次数；减少CPU必须做的工作。要注意在程序中分配内存、读取配置文件、预计算一些数据等，如何将这些的使用次数降到最低。

不断分析程序中的性能瓶颈，找到问题所在，然后优化。

## Compiling to C

Python的几种编译器以及适用范围：

* `Cython` 将Python代码编译成C代码，适用于包含numpy和一般的Python代码
* `Shed Skin` 非numpy代码编译成C
* `Numba` 对numpy专门的编译器
* `Pythran` 对于numpy和非numpy代码的一个新的编译器
* `PyPy` 一个稳定的JIT（just in time）编译器，也是只对非numpy代码

如果你的代码不包括numpy，则可以使用`Cython, Shed Skin, PyPy`，但是如果使用了`numpy`，则可选择`Cython, Numba, Pythran`。

当然得注意各种编译器的新版本是否有支持对象的调整。

### JIT Versus AOT Compilers

AOT:Ahead of time，包括的编译器`Cython, Shed Skin, Pythan`

JIT:Just in time，包括编译器`Numba, PyPy`

AOT编译器一般针对自己的机器特别编译一个版本，也可以像Anaconda那样直接使用通用版，但是下载源码自己编译是否会优于通用版？

JIT的一个问题时，如果你经常运行的小的脚本，使用JIT效率会影响较大，因为编译需要耗费时间。

所以具体使用哪种，也需要根据情况考虑。

### Why Does Type Information Help the Code Run Faster?

由于Python变量类型是动态的，在一个片段中变量类型可以变换，而有些函数由于类型不同会产生不同的操作，例如：

```python
a = 1.0
abs(a)
a = 1.0 + 1.0j
abs(a)
```

`abs`会根据具体类型是`float`还是`complex`，来决定具体的运算，所以在开始的时候确定类型很重要。

而且Python会对一些基本类型（int等）进行封装成更高级的对象——包含`__hash__`等内建方法，如果我们需要的是数学运算，那最好的方式就是使用基本类型而不是封装成的类。

### Using a C Compiler

Cython使用gcc，Shed Skin使用g++，Microsoft的编译器是cl，Intel's的是icc。

gcc适用于更多的平台，但是统一性就会部分损害优化的程度，例如针对Intel的芯片，icc的优会优于gcc。

### Cython

注意是Cython不是CPython，Cython是另一个编译器，支持编译pure python和扩展的Cython代码（基于Pyrex）。更有利于编写Python的C扩展。

使用Cython的库有：scipy、scikit-learn，lxml和zmq。

#### Compiling a Pure-Python Version Using Cython

下面说明个例子，直接使用Cython编译成pyd，可以直接通过`import`导入。

```python
# filename: cythonfn.pyx
def calculate_z(maxiter, zs, cs):
	"""Calculate output list using Julia update rule"""
	output = [0] * len(zs)
	for i in range(len(zs)):
		n = 0
		z = zs[i]
		c = cs[i]
		while n < maxiter and abs(z) < 2:
			z = z * z + c
			n += 1
		output[i] = n
	return output

# filename setup.py
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
setup(
	cmdclass = {'build_ext': build_ext},
	ext_modules = [Extension("calculate", ["cythonfn.pyx"])]
	)

# execute cmd
>>> python setup.py build_ext --inplace
# 得到calculate.cp35-win32.pyd文件，在windows下是pyd，linux下应该是pyc文件，pyd可以通过dll工具反编译
```

#### Cython Annotations to Analyze a Block of Code

虽然Cython这样简单的方式speedup 我们的代码，但是要知其所以然，我们才能有的放矢的进行优化工作。

`cython -a code.pyx`可以生成一个`code.html`，产生了一个注解的`code.pyx`的代码页面。黄色越深说明PVM调用越多（生成了更多的C代码），颜色月浅说明越少生成C代码（越少的PVM调用）。目标就是消灭那些深黄色的代码，最好一片白。

循环语句中控制循环的一般执行比较多，但是可优化余地有限，可以关注循环语句中的内部语句，注意调整其代码，增加性能。

#### Adding Some Type Annotations

即便是在python中使用基本类型，如：`int`等，在使用的时候也会和PVM交互（进行Python更高level对象的转换）。而可以使用Cython的方法来减少这方面的消耗，使用：`cdef type var`，例如上面`cythonfn.pyx`代码类型提前在函数最开始声明：

```python
def calculate_z(maxiter, zs, cs):
    cdef unsinged int i,n
    cdef double complex z,c
    ...
```

再使用Cython产生一个`html`，可以看到只涉及到`z,c,i,n`的运算操作都是白的——即和PVM没有交互。

Cython和Numpy的使用需要配置setup.py和一些schedule的设置（static, dynamic等）

Cython会做边界检查，会消耗一点CPU时间，可以通过增加flag来去掉边界检查：

```python
#cython: boundcheck=False
def func():
    pass
```

### PyPy

PyPy是CPython的替代，提供了所有的内置模块。PyPy的JIT编译器非常有效，只需做很少甚至不做任何工作就可以取得不错的速度提升。

PyPy在性能表现方面要强于CPython。

#### Garbage Collection Differences

PyPy相比CPython使用不同类型的垃圾回收器，CPython使用引用计数，而PyPy使用修改标记和清除方法，PyPy可能会更晚的清除不用的对象。

所以在写代码的时候还是要有这方面的考虑，虽然代码上的差异不是很大，但是还是有一些细微的差别。[PyPy和CPython不同](http://doc.pypy.org/en/latest/cpython_differences.html)

由于两者之间还是有一些差别，所以PyPy尚且不能支持所有的模块，不支持并不是不能用，而是这部分包和模块还是使用CPython，PyPy尽可能的移除模块对C extension libraries的依赖。[PyPy兼容的模块](https://bitbucket.org/pypy/compatibility/wiki/Home)

在PyPy中，使用numpy需要一个中间层（会导致速度变慢）——`cpyext`，但是对于numpy，PyPy有一个实验项目：[numpypy](http://buildbot.pypy.org/numpy-status/latest.html)

### Foreign Function Interfaces

可以使用C来开发，然后编译成so(linux)，放在系统中可以检索到的lib目录，然后使用标准库`ctypes`来加载so，并做一些两者之间的交互（类型转换和函数提取等）

`ctypes`处理起来有点麻烦，就像还没有进化好的工具，`cffi`看了一眼，觉得没有更优秀，处理方式和`ctypes`不同。

## Concurrency

并行程序并不受制于I/O，这是最大的收获。在一个并行程序中，区别于顺序执行——one line to next——并行的代码处理`events`，不同部分的代码处理不同的`events`。

### Introduction to Asynchronous Programming

当程序进入I/O等待，执行的程序将暂停，这样内核可以进行低级的操作处理I/O请求（叫做上下文切换context switch）。这样就需要将CPU缓存中的数据取出（切出时）和重新装载（切入时）。

在并发程序中，我们一般会有一个`event loop`，管理什么时候要执行什么程序。其实这个`event loop`只是一个简单的函数列表。在列表顶端的函数执行，然后下一个。例如：

```python
from queue import Queue
from functools import partial
eventloop = None
class EventLoop(Queue):
    def start(self):
        while True:
            function = self.get()
            function()
def do_hello():
    global eventloop
    print("Hello")
    eventloop.put(do_world)
def do_world():
    global eventloop
    print("world")
    eventloop.put(do_hello)
if __name__ == '__main__':
    eventloop = EventLoop()
    eventloop.put(do_hello)
    eventloop.start()
        
```

采用`event loop`一般使用两种模式：`callback`或`futures`。

* __callback__： 众所周知，在`callback`模式中参数是一个函数——叫做callback function。例如：

```python
def save_data_to_db(callback):
    pass
def print_response(value):
    pass
save_data_to_db(print_response)
```

​	`save_data_to_db`异步执行，存储数据库立即返回，等到真的执行完再执行`print_response`回调，继续执行下面的逻辑。

* __futures__：在futures中，异步程序先返回一个future result的promise，等到异步程序执行完之后（可以使用`yeild`，我们期望的实际值返回之后再进行其他运算。下面例子就是使用`yield`实现，类似串行执行的程序：

```python
@coroutine
def save_value(value, callback):
    print("Saveing...")
    db_response = yield save_to_db(result, callbacl)
    print("Saved")
eventloop.put(partial(save_value, "hello world"))
```

Python2.7（future-based concurrency）和Python3.3+（`asyncio`留意）的处理还是有些不同，下面会对两个版本进行介绍。

### Serial Crawler

#### [gevent](http://www.gevent.org/intro.html)

一个最简单的异步处理库是`gevent`，它使用的是返回`futures`的编程模式。`gevent`在运行时对I/O标准库函数进行修改达到异步的目的（monkey-patches：运行时对程序进行修改），所以大部分时候就是使用标准的IO库函数。

_`gevent` is a coroutine-based Python networking library._

`gevent`提供两种机制来实现异步编程——正如我们刚刚提到的，对标准库IO进行修正达到异步IO，它也提供一个`Greenlet`对象，其可以用于并行执行。`greenlet`是一个`coroutine`类型，可以考虑成一个线程，其实，所有的`greentlets`使用一个物理线程。相比于使用多个CPU来运行所有的`greentlet`，`gevent`的调度是使用一个`event loop`在I/O等待期间切换它们进行运行。`gevent`使用`wait`使处理`event loop`更透明，一个`wait`函数将启动一个`eventloop`，而且尽可能久的运行，直到所有的`greenlet`都执行完。一般`gevent`代码都是顺序执行，在某一点设置很多`greenlets`做一些并行的任务，然后使用`wait`函数启动一个`event loop`来执行所有并行任务，当`wait`函数正在执行，所有在queue中的并行任务开始执行直到所有都完成，然后又回到之前的顺序执行中（serial）。

`gevent.iwait`是只要有返回，即处理，而`gevent.wait`是等到所有都处理完才返回。

> __monkey patch__
>
> A **monkey patch** is a way for a program to extend or modify supporting system software locally (affecting only the running instance of the program).
>
> 在不同语言中其意义可能各有不同，在Python等动态语言中，monkey patch仅仅指在运行时动态修改一个类或模型，用来弥补目前第三方代码的问题（可能是bug，也可能是一些不能满足现在需求的功能）。
>
> 作用：
>
> 1. 在运行时替换`methods/attributes/functions`
> 2. 在不维护一套私有的源码情况下，修改或扩展第三方产品的行为
> 3. 在运行时，对内存中的对象使用一个patch来替换在磁盘上的源码
> 4. 发布与源码一起存在的安全或功能修复（像一个插件一样，保存原来功能的前提下，修复原有的问题）
>
> 使用monkey patch时也要考虑其和可能引来的问题。具体详见Wikipedia.

`grequests`将`request`和`gevent`融合，这样使用起来就会相对简单一些。

### tornado

不同于`gevent`，`tornado`是使用回调函数来实现异步操作。

### AsyncIO

Python3.4+从新构造了原有标准库的`asyncio`，实现异步功能来处理IO消耗多的的系统。

使用`async def`或`@asyncio.coroutine`来定义函数或方法。

注意`yield from`.

