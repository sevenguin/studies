# Theano 初学

包括基础概念、安装、初步学习中遇到的问题。

## Basic Concepts

### Tensor

在数学领域中，tensor是一个几何对象，其用来描述几何向量、常量的线性关系。

### Type

在Theano中，所有的符号都是被定义为某种类型的，例如`dscalar`就是一种类型——定义为数据类型为`double`的`0`维的数据（标量）。`dscalar`不是一个类，`x = T.dscalar('x')`中，`x`并不是`dscalar`的实例，它是`TensorVariable`的实例，其实是给`x`的`type`字段赋值为Theano Type `dscalar`。表达式(`c=a+b`)也是类型`TensorVariable`，只不过Theano的type不是`dscalar`，_具体需要继续看看。_

一些类型如下，详见[Tensor creation](http://deeplearning.net/software/theano/library/tensor/basic.html#libdoc-tensor-creation)：

- **byte**: `bscalar, bvector, bmatrix, brow, bcol, btensor3, btensor4, btensor5`
- **16-bit integers**: `wscalar, wvector, wmatrix, wrow, wcol, wtensor3, wtensor4, wtensor5`
- **32-bit integers**: `iscalar, ivector, imatrix, irow, icol, itensor3, itensor4, itensor5`
- **64-bit integers**: `lscalar, lvector, lmatrix, lrow, lcol, ltensor3, ltensor4, ltensor5`
- **float**: `fscalar, fvector, fmatrix, frow, fcol, ftensor3, ftensor4, ftensor5`
- **double**: `dscalar, dvector, dmatrix, drow, dcol, dtensor3, dtensor4, dtensor5`
- **complex**: `cscalar, cvector, cmatrix, crow, ccol, ctensor3, ctensor4, ctensor5`

### 一些使用

`from theano import pp`，这个函数可以打印出计算表达式；

`from theano import In; function([x, In(y, value=1)], z)`，这里的`In`作为给`y`赋默认值；

#### Shared Variable

变量在多个函数中共享：

```python
from theano import function
from theano import shared
from theano import Tensor as T
s_value = shared(0)       # 0为初值
inc = T.iscalar('inc')
accmulator = function([inc], s_value, updates=[(s_value, s_value + inc)])

dec = T.iscalar('dec')
decrementor = function([dec], s_value, updates=[(s_value, s_value - dec)])
```

可以使用function的`copy(swap={old_state:new_state})`方法来新复制一个相同的函数，新函数使用新的共享`new_state`替换老的共享变量`old_state`。

随机数：`theano.tensor.shared_randomstreams.RandomStreams`

