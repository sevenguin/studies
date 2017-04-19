#Scala

一些好玩的东西

1. `s"abc${variable}prefix"`，有个变量`val variable = 2`，就可以直接用来，字符串前面加一个prefix，然后用$，如果前后有字符，则需要用大括号括起来名字（类似shell）
2. `Any`为Scala的绝对父类型，所有其他类型都继承于其两个子类型`AnyVal`和`AnyRef`，其中`AnyVal`是包含`Char,Boolean,Unit`和所有`Numeric`类型，这个类型的变量可能在运行时分配到堆或者栈上，作为一个JVM的基本类型值；`AnyRef`都是分配到堆上，这里的Ref其实就是表示这个类型是一个引用类型。
3. `Noting`类型是所有类型的子类型，所以可以作为任何返回值返回，Nothing不能实例化，仅仅作为type使用，抛出异常时，就返回的是Nothing。
4. `None`类型是所有`AnyRef`类型的子类，其有个关键字是`null`，表示的是不指向任何内存中的实例
5. 不支持自动将其他类型值作为`Boolean`判断，即便是`null`，也不会判断为`false`
6. `Unit`类型被用作函数或者表达式的返回类型，表示没有返回任何东西，`Unit`表示出来的值就是`()`，你可以定义变量是`Unit`类型：`val a:Unit = ()`，但是一半是作为函数或表达式中使用。
7. `Tuple`，可以包含不同类型，`_1,_2`来对第一第二个元素索引，起始位置不是`0`。构造两个元素的tuple:`val t='a'->97`
8. `match`不像C中，没有`break`会顺序执行，这个不会，且没有break；多个pattern：`case pattern1|pattern2 => expression`，可以有`case other`作为通配，这里也可以写为`case _ => expression`还可以：`case <pattern> if <boolean expression> => expression`和判断类型`case x:Boolean => println("it's boolean")`
9. `scala source`，可以直接执行scala文件（例如命令，main文件）；也可以在scala下执行`:load source`加载


## 基础知识

纯函数：

* 有一个或多个输入参数
* 计算只是用输入参数
* 返回一个值
* 相同的输入总是对应相同的输出
* __不要使用（影响）函数外的变量（的值）__
* 不被这个函数外的任何数据影像

函数定义:

`def <identifier>(arg: argtype):<type> = <expression>`

函数调用，如果没有参数：`identifier`就可以直接调用（不用带括号，当然带上也可以）；如果一个参数可以传统方式调用，也可以`identifer <expression>`，这个表达式只要返回类型和参数一致即可（多个参数用这个方法我还没发现如何弄）。

也可以使用入参的默认值。

__Vararg__：类似Python中的`*arg, **argw`，表示多个入参：

```scala
def sum(items:Int*): Int = {
  var total = 0
  for(i <- items){
    total += i
  }
  total
}
sum(10, 10, 20)
```

__Parameters Groups__：不同于将所有参数放在一个Group中，可以分成多组：

```scala
def dosome(a:String)(b:String): Unit = {
  println(s"$a, $b")
}
```

__Type Parameters__：

```scala
# define
def <function name>[type-name](parameters-name:paramters-type):<type-name> = <expression>

def iden[A](a:A): A = a
iden[String]("hello")
```

__Method__：一个method是在类中定义，并且在整个类中任何实例中可用。调用方法处了传统的方法，还有：

`<object> <method> <paramter>`，如：`"abc" compare "c"`

注意：`var d =3; d.+(4)`，则`d`为7，`+`当做一个计算函数（这样上面的调用方法也可以解释的通）

__函数类型（Method Type）__：其实就是函数也可以作为一种类型、一种变量传递。定义方式：

`([<type>,...]) => <type`，如果是一个参数，前面的`()`可以省略。例如：

```scala
def f(a: Int, d: Double): Double = {
    a + d
}
val df: (Int, Double)=>Double = f(_, _)    # 这点和`learning scala`上有些不同，这里等号右边的表达式必须是函数带上参数占位符‘_’,而且和实际参数数量相同
```

__Higher-Order Functions（高阶函数）__：高阶函数是一个函数有一个函数类型的参数或返回值

__function literals（匿名函数）__：定义为`(<arg>:<type>,...)=><expression`，例如：`(a:String)=>s"Hello, $a"`，匿名函数作为参数的时候可以简写，如：`df((a,b)=>a+b)`

__占位符__:占位符是function literals的缩写形式，将参数名用`_`来替换，一般需要满足一下两种情况：

* 显式类型（明确指定类型）
* 这个参数只被使用一次

```scala
val doubler: Int => Int = _ * 2
def df(f:(Int, Int)=>Int) = f(2, 3)
df(_ + _)   # 这个就直接定义成函数了，都省了(...) => <expression>
```

__Partial Functions（偏函数）__：之前介绍的函数都称作Total Function（全函数），因为他们能够处理所有可能的输入值。有一些函数不能对所有可能的满足输入参数类型输入值进行处理，称作Partial Function（偏函数），例如：函数对入参求开方，传入的值为负数。

在Scala中，偏函数是通过function literals来定义，其是应用一系列`case`到`input`，需要`input`至少`match`到其中一个`pattern`，如果没有一个`match`，则会抛出`Scala error`。

__Partial Applied Function__：在调用函数时，我们都需要传入参数，有时候想重用传递参数如何办？可以使用partial applied function。

如下：

```scala
def factorOf(x: Int, y: Int) = y % x == 0
# 想保留函数的所有参数，只是想简写函数
val f = factorOf _    # f 就是Partial Applied Function
# 想保留一部分参数，而其他的被指定
val multipleOf3 = factorOf(3, _: Int)  # 这里第二个参数被保留，这个参数需要被显式指定
```

__Currying__:在函数类型方面，具有多个参数列表的函数被认为是多个函数的链.

```scala
# 对比两个函数
def factorOf(x: Int, y: Int) = y % x == 0
def factorOf(x: Int)(y: Int) = y % x == 0
# 对第二个函数
val isEven = factorOf(2) _
val z = isEven(32)   # 对比上面多参数（一个列表）的partial applied function, 更好理解了
```

#### Collections

 `arrays,lists,maps,sets,trees`

所有可迭代的集合（iterable collection）的根类是`Iterable`。

__不可变集合(Lists, Sets, and Maps__)：

| 函数名                | 函数用途/说明                            | 备注   |
| ------------------ | ---------------------------------- | ---- |
| size               | Collection大小                       |      |
| head               | 第一个元素                              |      |
| tail               | 除第一个之外，余下所有的元素                     |      |
| map/foreach/reduce | Iterable即其子类拥有                     |      |
| asJava             | List(12, 29).asJava                |      |
| asScala            | new java.util.ArrayList(5).asScala |      |

__可变集合__:

| 不可变集合对象                   | 可变集合对象                    |
| ------------------------- | ------------------------- |
| collection.immutable.List | collection.mutable.Buffer |
| collection.immutable.Set  | collection.mutable.Set    |
| collection.immutable.Map  | collection.mutable.Map    |

Seq是所有sequences的基类

__单体集合__:

* Option：值为Some or None，`Option(null)-->None`，`Option(2)--->Some(2)`
* Try: `util.try`，值为Success or Failure
* future：concurrent.Future


##Basic OOP in Scala

`class Lotus(val color: String, reserved: Boolean) extends Car("Lotus", reserved)`

###Class and Object Basic

由于Scala中也允许声明object，所以为了区别scala中从class new出来的对象和object声明的对象，class new出来的叫做instance of some class
> final class A，A不能被继承
> abstract class B，B不能被实例化 

重载：不同的参数和返回值都可以（有些语言返回值不在考虑范围内）

scala中，在函数中直接使用匿名函数时需要注意：
* `list.map((line:String)=>do something)` map里面的line指定String的时候需要用括号括起来
* `list.map(lien=>do something)` 这个时候可以不指定String，默认就是类型一定的，这个时候是不用括起来的
  其实指定类型是比较冗余的，而且想想，如果加上括号其实是生成了一种tuple，这个tuple第一个元素是line。如果是传入多个字段的话，map其实就是把这个变量当做一个tuple，这时候也不用指定，直接用line._1/_2来指定tuple里面的元素了。这个后面研究下Function再说
####Currying(柯林)
Hashell Curry
柯林转换就是将一个多参数函数转换成一个函数链，每一个都有一个单独的参数，例如：
`def cat(s1:String)(s2:String)=s1+s2`
`def cat(s1: String) = (s2: String) => s1 + s2` 这个一般不用，但是也可以这么写
`Function.curried(somefunc _)` 注意somefunc和_中间的空格，这个可以将多参函数柯林化
柯林化的一个主要用途是：
`val partialCurryCat = curryCat("foo")(_)`生成新的函数，只带一个参数的函数，可以这样循环的将多参无限制的方法逐步限制（降参）
####函数与方法
REPL里面独立的方法是FunctionN（表示N表示有几个参数）的实例
类里面定义的方法是方法而不是函数
函数即对象（可以在对象中继承FunctionN，然后实现apply方法，可以将对象直接当方法使用）

####implicit
有两种情况：
#####Implicit Conversions 
如果你有一个类型的实例，这时候你需要和之前类型相似，但是在不同上下文环境运行。这种情况经常发生，所以需要一种自动转换机制。    
`val name:String = "scala"
println(name.capitalize)
` 
其实这里的`name`是`java.lang.String`(`Predef.scala`中有一些预先定义)，而`java.lang.String`中并没有`capitalize`函数，但是就是在`Predef.scala`中定义了介个`implicit`函数，进行多次转换，例如：
`implicit def any2stringfmt
implicit def augmentString(...):scala.collection.immutable.StringOps
implicit def any2stringadd
`
而`capitalize`就包含在`StringOps`中（它也是继承自`StringLike`，这里要说的就是2.11版的scala中`scala.runtime`中没有了`RichString`)
> `implicit` 关键字告诉编译器，这个method可以在适当的时候用于`String`和`StringOps`的隐式转换，编译器检测到尝试调用`capitalize`方法，然后发现`StringOps`有这个方法，然后去找当前范围（scope）中的一个将`String`转换成`StringOps`的隐式方法（implicit method），最后找到了`augmentString`

这个转换函数有些时候称作`views`

哪些`conversion methods`会被编译器找到呢？
* 如果当前对象中包含这个方法，则没有转换
* 只有implicit方法才会被考虑
* 只有当前范围的implicit方法被考虑，目标类型的`companion object`中定义的也可以
* implicit方法不会串行查找，即仅仅这个方法有一个当前类型的参数，返回值是目标类型（不具备传递性）
* 如果出现奇异（即有多个implicit方法可以被使用），则不会出现转换，implicit方法要起作用，则必须有且只有一个
  这里的范围应该是显式import的编译器隐式import的所有代码
#####Implicit Function Parameters 
2、可能会重复调用一个函数很多次，而且其某些参数在很多情况下是相同的，这种情况下你可能想给其赋默认值，这样就不需要每次都传入了
`
def test(i: Int)(implicit j: Int):Unit={
     println("test:" + i + ", " + j)
}
implicit val j = 23  #声明的时候implicit是必须的，变量名可以随意起，而且这个implicit val是继承自父类也是可以的；但是如果出现多个implicit val（var）都满足参数（和参数类型相同），则编译器无法确认，报错
test(2)  #这里j=23
test(2)(3)
`
如果有多个implicit参数，则必须写在一个里面，而且implicit必须是最后一个参数例如：
`def f(a:Int)(b:Int)(implicit c:Int, d:Int)` 这里面b的声明必须在implicit之前，而且c和d必须放在一起，implicit一旦声明，后面不许再跟()参数了

####annotation
#####specicalized
`class a[@specialized(Int) A]{
	def f (a:A){
	}
}`  
由于编译时的类型擦除和对基本类型的自动装箱（List[Int]，Int被自动装箱成一个Container），这个就是为了避免自动装箱，编译器会为a生成两个版本，一个类是正常情况，一个是继承自`class a[Int]`，这样就特殊化了，避免了自动装箱。

###一些特性
1. `class A(val a:String)` a作为A的一个property；`class A(a: String)` a就不是A的property
   因为类里面参数都声明为`val`，编译器生成一个私有的字段（在内部使用不同的名字），同时生成一个和声明参数相同的reader method.


详见：[Scala官方文档](http://www.scala-lang.org/sites/default/files/sids/dragos/Thu,%202010-05-06,%2017:56/sid-spec.pdf)
