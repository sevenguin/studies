# pandas

[官网](http://pandas.pydata.org/)

`pandas`构建在`numpy`之上，所以使用`numpy`的应用可较好的迁移至`pandas`。

## 两个重要的数据结构

`pandas`有两个重要的数据结构`DataFrame`和`Series`

### Series

`Series`是一个一维的数据，如果没有指定索引，则默认索引为0~N-1，直接打印Series对象，则出现两列数据，第一列为索引第二列为数据。

```
> obj=Series(['x', 'y', 'z'], index=['a', 'b', 'c'])  #index可以不指定，默认为数字，类型int
> obj
   a x
   b y
   c z
   dtype: object
> obj.values
  array(['x', 'y', 'z'], dtype=object)
> ojb.index
  Index(['a', 'b', 'c'], dtype='object')
```

可以通过布尔数组（布尔数组的元素数可以和`obj`不一致）来过滤一些数据，例如：`obj[obj>'x']; obj[[True, False]]`，因为索引可以指定，所以，可以将`Series`看做是一个定长、有序的字典。也可以通过`python`的字典来创建`Series`。

```
> dict_data = {'c': 1, 'b': 2, 'a': 3, 'd': 4}      #注意键值顺序
> s_data = Series(dict_data)
> s_data
  a    1
  b    2
  c    3
  d    4
  dtype: int64
```

Series创建之后是对index进行排序之后的数据，如果指定了`index`（则按照指定`index`指定的顺序列出），而`index`的长度大于数据，则就会出现`NaN`的数据，这时候可以使用`isnull`或`notnull`来检测数据丢失。而且`Series`有一点，就是`index`可以重复，这时候通过索引获得的数据是一个数组，类型为`Series`，而如果非重复的`index`，则返回值就是对应的`value`，类型就是此`value`的类型。

```
> s_data = Series(dict_data, index=['a', 'b','c', 'c', 'o'])
> s_data
  a    1
  b    2
  c    3
  d    4
  o  NaN
  dtype: float64   #注意，这里的dtype也发生了变化
> pandas.isnull(s_data)
  a    False
  b    False
  c    False
  c    False
  o     True
  dtype: bool
> pandas.notnull(s_data)  #和isnull刚好相反
  a     True
  b     True
  c     True
  c     True
  o    False
  dtype: bool
```

可以设置`Series`对象本身和索引的`name`，例如：

```
> s_data.name = 'value'
> s_data.index.name='index..'
  index..
  a     3
  b     2
  c     1
  c     1
  o   NaN
  Name: value, dtype: float64
```

索引也是可修改的，直接指定：`s_data.index = ['m', 'a', 'b', 'c', 'd']`，这里指定的数组的长度必须和`index`长度一致。

> 注意，即便是`Series`指定了索引，但是还是可以使用位置来检索数据，例如：`s_data[0]`获得第一个元素

### DataFrame

`DataFrame`就是一个表格，底层就是通过一个或多个二维数组存储的，面向列和面向行的操作是对称的，而且每一列都可以有不同的数据类型，正因为以二维数组存储，所以可以分层索引。而且DF有行和列索引，索引结果就是一个个`Series`。

同`Series`类似，可以通过如下方法创建：

```	
> data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9]}
> frame = DataFrame(data)
```

也可以在构建`DataFrame`的时候指定`columns`和`index`来构建该数据：

```
> frame = DataFrame(data, columns=['year', 'state', 'pop', 'debt'], index=['o', 't', 'th', 'f', 'fi'])
> frame       #上面的columns可以大于列数（用NaN补），index必须和原始数据长度相等
      year   state  pop debt
  o   2000    Ohio  1.5  NaN
  t   2001    Ohio  1.7  NaN
  th  2002    Ohio  3.6  NaN
  f   2001  Nevada  2.4  NaN
  fi  2002  Nevada  2.9  NaN
```

可以通过字典类型的方法检索，也可以通过属性检索（列名为属性名），这种都是索引列，例如：`frame['state']`，而不能是`frame['th']`。行一般通过位置或名字来索引：`frame.iloc[1]; frame.iz['t']`。

索引到的数据可以直接赋值，修改其中的指定位置的数据，这个时候赋值的数组的长度必须和索引到的数据长度一致，如果使用`Series`进行赋值，则可以不一致，这时会精确匹配两者的索引。

```
> val = Series([-1.2, -1.5, -1.7], index=['two', 'four', 'five'])
> frame['debt'] = val
```

给以个不存在的列赋值就会创建一个新的列，`del`会删除列：

```
> frame['eastern'] = frame.state == 'Ohio'
> del frame['eastern']
```

> 索引`DataFrame`得到的是一个`reference`而不是一个拷贝，所以修改就直接反映到数据中了

如果数据字典是嵌套的格式，则外部键为列索引，内部键为行索引：

```
> pop = {'Nevada': {2001: 2.4, 2002: 2.9},'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}}
> df = DataFrame(pop)
> df
        Nevada  Ohio
  2000     NaN   1.5
  2001     2.4   1.7
  2002     2.9   3.6
```

类似`Series`，`DataFrame`的`values`也是返回一个`numpy.ndarray`。

### 索引对象

在`pandas`中，有一个类型：`pandas.core.index.Index`，表示索引对象，可以通过`df.index`或`series.index`来获得，获得之后的索引对象不能由用户修改其值。（但可以整体赋值修改）这样有利于共享索引。

三个方法：

* `iloc`： Purely integer-location based indexing for selection by position. Allowed inputs are:
  * An integer, e.g. ``5``.
  * A list or array of integers, e.g. ``[4, 3, 0]``.
  * A slice object with ints, e.g. ``1:7``.
  * A boolean array.
* `loc`：Purely label-location based indexer for selection by label. Allowed inputs are:
  * A single label, e.g. ``5`` or ``'a'``, (note that ``5`` is interpreted as a *label* of the index, and **never** as an integer position along the index).
  * A list or array of labels, e.g. ``['a', 'b', 'c']``.
  * A slice object with labels, e.g. ``'a':'f'`` (note that contrary to usual python slices, **both** the start and the stop are included!).
  * A boolean array.
* `ix`：A primarily label-location based indexer, with integer position fallback. ``.ix[]`` supports mixed integer and label based access. It is primarily label based, but will fall back to integer positional access unless the corresponding axis is of integer type. e.g.`ix[rowsindex(or array), colsindex(or array)]`

这三个方法都支持直接使用`Indexer`来做索引，下满说一些`indexer`支持的一些简单操作：

* `diff` 索引差集，`diff`已经被遗弃了，应该用`difference`
* `intersection` 计算交集
* `union` 计算并集
* `isin` 计算出一个布尔数组表示每一个值是否包含在所传递的集合里
* `delete, drop, insert` 删、清、插
* `unique` 计算索引唯一值数组
* `is_unique` 判断是否有重复值，如果没有则返回`True`
* `is_monotonic` 如果返回`True`，则表示每一个元素都比它前面的元素大

```
> df = DataFrame({'col':{'a':1, 'b':2, 'c':3}})
> df.index
  Index(['a', 'b', 'c'], dtype='object')
> df.index.isin(['a', 'd', 'c'])
  array([ True, False,  True], dtype=bool)
> df.index.is_unique
  True
> df.index.unique()
  array(['a', 'b', 'c'], dtype=object)
```

## 基本功能

### 重新索引

`reindex`使数据符合一个新的索引来构造一个新的对象：

```
> obj = Series([4.5, 7.2, -5.3, 3.6], index=['d', 'b', 'a', 'c'])
> obj2 = obj.reindex(['a', 'b', 'c', 'e', 'd'], fill_value=0) #注意fill_value和e的位置
  a -5.3
  b 7.2
  c 3.6
  e 0.0
  d 4.5
  dtype: float64
```

上面的`reindex`中新增的填充值直接指定，也可以使用方法指定：

```
> obj3 = Series(['blue', 'purple', 'yellow'], index=[0, 2, 4])
> obj3.reindex(range(6), method='ffill')  #使用方法ffill，使用前一个值填充
  0      blue
  1      blue
  2    purple
  3    purple
  4    yellow
  5    yellow
  dtype: object
```

上面`method`可以设置的值：

* `ffill/pad` 向前/前进位填充
* `bfill/backfill` 后向/后进位填充
* `nearest` 使用最近的有效观察值填充
* `default` 不填充

可以使用`obj3.reindex(columns=newcolumns)`来重建列索引。

### 行列操作

#### 删除行、列

`drop`之后返回一个新的对象，原来对象的值没变

```
> obj = Series(np.arange(5.), index=['a', 'b', 'c', 'd', 'e'])
> new_obj = obj.drop('c')  #通过设置drop参数axis=1，来删除列
  a   0
  b   1
  d   3
  e   4
  dtype: float64
```

#### 索引，挑选和过滤

`Series`的索引工作原理和numpy索引类似：

```
> obj = Series(np.arange(4.), index=['a', 'b', 'c', 'd'])
> obj['b']
  1.0
> obj[1]
  1.0
> obj[2:4]
  c    2
  d    3
  dtype: float64
> obj[['b', 'a', 'd']]
  b    1
  a    0
  d    3
  dtype: float64
> obj[obj.index.delete(0)]
  b    1
  c    2
  d    3
  dtype: float64
> obj['b':'c'] = 5   #可以通过结果看出，这里的切片不像numpy中，之类包括切片指定的最后一个元素
  a    0
  b    5
  c    5
  d    3
  dtype: float64

```

对于`DataFrame`，操作可能有些不同：

```
> data = DataFrame(np.arange(16).reshape((4, 4)), index=['Ohio', 'Colorado', 'Utah', 'New York'], columns=['one', 'two', 'three', 'four'])
> data[1]   #不能使用数值索引
  ...
  KeyError: 1
> data[:1]  #这样获得第一行
        one  two  three  four
  Ohio    0    1      2     3
> data[data['three'] > 5]
            one  two  three  four
  Colorado    4    5      6     7
  Utah        8    9     10    11
  New York   12   13     14    15
```

#### 运算和对齐

例如加法，在`DataFrame`行列索引都重合的时候进行相加，不重合的地方填充`NaN`。

`DataFrame`和`Series`间的运算：DataFrame和Series间的算术运算Series的索引将匹配DataFrame的列，并在行上扩展，如果一个索引值在`DataFrame`中找不到，则联合重建索引。

```
> frame = DataFrame(np.arange(12.).reshape((4,3)), columns=list('bde'), index=list('mnop'))
> series = frame.ix[0]
> frame
     b   d   e
  m  0   1   2
  n  3   4   5
  o  6   7   8
  p  9  10  11
> series 
  b    0
  d    1
  e    2
  Name: m, dtype: float64
> frame - series
     b  d  e
  m  0  0  0
  n  3  3  3
  o  6  6  6
  p  9  9  9

> series2 = Series(range(3), index=list('bef'))
> frame + series2
     b   d   e   f
  m  0 NaN   3 NaN
  n  3 NaN   6 NaN
  o  6 NaN   9 NaN
  p  9 NaN  12 NaN
> frame.sub(series, axis=1)
     b  d  e
  m  0  0  0
  n  3  3  3
  o  6  6  6
  p  9  9  9
```

### 函数和映射

Numpy的ufuncs（基于元素的数组方法）都可以使用，例如：`np.abs(fm)`

有一个常用方法：`apply`，每次处理一行或一列：

```
> frame = DataFrame(np.random.randn(4, 3), columns=list('bde'), index=['Utah', 'Ohio', 'Texas', 'Oregon'])
                 b         d         e
  Utah    0.540385 -0.491874  0.454840
  Ohio   -0.669294  0.068683 -0.369552
  Texas   0.750237 -0.741963 -0.840675
  Oregon  0.310264  0.801820 -0.220166
> f = lambda x: x.max() - x.min()
> frame.apply(f)    #按列   
  b    1.419531
  d    1.543783
  e    1.295516
  dtype: float64
> frame.apply(f, axis=1)
  Utah      1.032259
  Ohio      0.737977
  Texas     1.590912
  Oregon    1.021987
  dtype: float64
```

`apply`的返回值也不一定要常量值，也可以是`Series`：

```
> def f(x):
      return Series([x.min(), x.max()], index=['min', 'max'])
> frame.apply(f)
              b         d         e
  min -0.669294 -0.741963 -0.840675
  max  0.750237  0.801820  0.454840
```

如果应用到单个元素上，则使用`applymap`：

```
> format = lambda x: '%.2f' % x
> frame.applymap(format)
              b      d      e
  Utah     0.54  -0.49   0.45
  Ohio    -0.67   0.07  -0.37
  Texas    0.75  -0.74  -0.84
  Oregon   0.31   0.80  -0.22
```

### 排序和排列

`frame.sort_index(axis=0/1, ascending=False/True, by=[])`是按照行列__索引__进行排序，`by`可以指定多列排序；

`series.order()`按照__值__排序，任何缺失值都默认放在最后；

`rank`返回各个元素在特定`method`下的位置：

```
> obj = Series([7, -5, 7, 4, 2, 0, 4])
> obj.rank(method='first')   #每个位置的元素从大到小排序后的位置
  0    6
  1    1
  2    7
  3    4
  4    3
  5    2
  6    5
  dtype: float64
> obj.rank(method='min')
  0    6
  1    1
  2    6
  3    4
  4    3
  5    2
  6    4
  dtype: float64
```

`method`取值：

* `average`  赋平均的排序
* `min`   使用最小值的序列，第几小
* `max`    使用最大值的序列，第几大
* `first` 使用排序的序号

### 一些其他方法

方法列表：

* `cumsum` 逐行、列累加列表，例如：$line_i = \sum_{j=0}^i line_j$
* `idxmax` 每一行、列的最大值的位置（索引）
* `describe` 一些统计信息

### 相关性和协方差

基于某一行各行的变化率：`pct_change`，相邻两行之间的变化率：$line_i - line_{i+1}\over line_i$，参数`periods`指明`shift`几行，即从跳过几行，跳过后的那行计算变化率还是基于第一行处理。

`corr`返回两列数据的相关性（`colA.corr(colrB)`），`cov`返回数据的协方差。`corrwith`返回和其他行、列的相关性（`frame.corrwith(colA)`）。直接`frame.cov、corr`返回相关性、协方差矩阵。

### Unique、Counts

`series.unique()`

`series.value_counts()`

`series.isin(array)`，返回一个bool数组，表示元素是否在array中。

### 丢失数据处理

丢失数据使用`NaN`来替换掉浮点或非浮点的数组数据，使用`isnull`来检测哪些是`NaN`：`frame.isnull`返回一各矩阵，为`NaN`值的元素所在位置为`True`，其实Python中的`None`值在`isnull`判断中也会被判断为`True`。

几个函数：

* `dropna` 过滤`axis`指定的label中含有`na`的数据
* `fillna`填充遗失值（固定值），或者使用插值函数`ffill`或`bfill`（取前面元素还是后面元素的值填充）
* `isnull`或者`notnull`

```python
> from numpy import nan as NA
> data = Series([1, NA, 3.5, NA, 7])
> data.dropna()
  0 1.0
  2 3.5
  4 7.0
  dtype: float64
```

使用`fillna`：

```python
> df = DataFrame(np.random.randn(7, 3))
> df.ix[:4, 1] = NA; df.ix[:2, 2] = NA
> df.fillna({1: 0.5, 2: -1}) #第2列为0.5，第3列为-1， 参数inplace为True则直接反应到df中而不是新返回一个
```

### 分层索引

分层索引允许多个层级的索引在一个方向（`axis`）上，可以使用低维度的方式来操作高维度数据：

```python
> data = Series(np.random.randn(10), index=[['a', 'a', 'a', 'b', 'b', 'b', 'c', 'c', 'd', 'd'], [1, 2, 3, 1, 2, 3, 1, 2, 2, 3]])
> data
  a  1    2.852514
     2    0.457402
     3    0.062776
  b  1    0.275232
     2   -1.057302
     3    0.376364
  c  1    1.234883
     2    2.025264
  d  2   -0.623794
     3   -0.260643
  dtype: float64
> data.index
  MultiIndex(levels=[['a', 'b', 'c', 'd'], [1, 2, 3]],
           labels=[[0, 0, 0, 1, 1, 1, 2, 2, 3, 3], [0, 1, 2, 0, 1, 2, 0, 1, 1, 2]])
> data.unstack()  #转换成DataFrame
            1         2         3
  a  2.852514  0.457402  0.062776
  b  0.275232 -1.057302  0.376364
  c  1.234883  2.025264       NaN
  d       NaN -0.623794 -0.260643
```

这个还是蛮有用，想目录那种分层概括的数据。