#Scala

##Basic OOP in Scala
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
