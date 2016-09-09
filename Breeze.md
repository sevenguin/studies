#Breeze
> Breeze is a numerical processing library for Scala. [github](https://github.com/scalanlp/breeze)

##Quick Start
所有Vector是Column Vector，Row Vector应该用`Transpose[Vector[T]]`
$Vector$
`val x=DenseVector.zeros[Double] (5)
x(1)=3 #对第二个元素赋值
x(3 to 4) := 0.5 #修改第3 到第4个元素的值，slice，注意是:=，vectorized-set operator 
`
$Matrix$
 `val m = DenseMatrix.zeros[Int](5, 5)
()m.rows, m.cols)
m(::, 1)  #第一列向量——结果是Vector
m(4::,) = DenseVector(1,2,3,4,5).t #设置行向量
m(0 to 1, 0 to 1) = DenseMatrix((3,1),(-3,-1)) #matrix的分片，以及分片赋值
`
###Broadcasting
column-wise and row-wise
numpy中，broadcast是隐式的进行，而breeze中需要显式通过`*`来指定，例如：
`val dm=DenseMatrix((1,2,3),(4,5,6))
val res=dm(::, * ) + DenseVector(3, 4)   #表示在列上对数据增加，每一列都增加列向量[3,4]——DenseVector默认是列向量
==>
4,5,6
8,9,10
mean(dm(*, ::))  #对每一行进行求均值
` 
###Probability Distributions
discrete or continuous
`val poi = new Poisson(3)
val s=poi.sample(5)
`

##Universal Functions
UFunc 可以操作常量、向量、矩阵或者自定义的类型的函数。如果你自己增加collection type，则可以自定义UFunc来实现一些操作运算（如log）作用于自己的类型上。UFunc使得Breeze更具有扩展性。

three UFunc types：
* element-wise UFuncs  对元素产生作用？例如log(matrix)结果是对matrix每个元素都求log得到的矩阵
* operators UFuncs 这个容易理解，例如a+b
* reductionUFuncs 例如sum

###Element-wise UFuncs
大部分UFuncs通常集成自`MappingUFunc`，他们通常传入一个常量或集合，然后将函数作用于常量或者集合中每个元素。默认情况下UFunc通常返回一个新的对象，如果想直接修改集合里面数据得做一些其他工作，例如：
> `log(1.0)`
> `log(Complex(1.0, 1.0))`   #Complex复变函数
> `log(Array(1.0, 2.0))`    #Array[Double] = Array(0.0, 0.6931471805599453)
> `log(DenseMatrix((1.0, 2.0), (3.0, 4.0)))`
0.0                 0.6931471805599453
1.0986122886681098  1.3862943611198906
> `log.inPlace(someMatrix)` 这个就是直接作用于someMatrix内部的元素，由于inPlace函数有一个implicit参数，所以需要声明一个类型，实现apply方法，然后声明一个该类型的implicit变量

`import package.class=>alias` 起别名
###Operator UFuncs
这个类似于普通的数学运算
`DenseVector(1,2) + DenseVector(3,4)` =>等价于
`OpAdd(DenseVector(1, 2), DenseVector(3, 4))`
但是需要注意：
`DenseVector[Double].rank(4) + 3` 表示随机产生4个数字，然后随机数都加上3，这样是可以的，但是`3 + DenseVector[Double]`是不可以的，因为`+`是DenseVector的一个函数，前面的其实就是一个DenseVector的实例调用`+`整个函数，参数是3
不过Scala如何不用`.`来调用函数，而且不用`()`传参？
`:` 在前面的是element-wise，例如`:=`叫做OpSet，`A:=B`，就是将B的元素值赋值给A的元素，而A仍然指向原来的object，再如：`:*`表示点乘
###Reduction UFuncs
`val mat = DenseMatrix((1,2,3),(4,5,6))
sum(mat)
结果：21
`
[Breeze提供的FU](https://github.com/scalanlp/breeze/wiki/Universal-Functions)
###Implementing UFuncs
直接看Breeze源码示例。`breeze\numerics\pacakge.scala` 


