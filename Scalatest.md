#Scalatest

$FunSpec$ allows us to think of our test as a $behavior-driven test$.
[ScalaTest2.0更新说明](http://www.scalatest.org/release_notes/2.0_history)
ScalaTest两大Matcher：
1. $should matcher$ 方法就是`should`
2. $must matcher$ 方法是`must`
###Should Matcher的类型
####Simple Matcher
Simple Matcher就是两个值之间使用一个断言，如下例：
`val list = 2::4::5::Nil
list.size should be(3)`
> `be`可以被`equal`替换，而且`3`必须被`()`扩起来
> 上面不能使用`==`或`!=`来验证，如果携程`list.size==5`不会对其进行断言验证，只是验证这个表达式是`true`或`false`，需要验证相等，则用`===`，`==`只是判断是否相等而不进行验证，`===`判断以及验证断言

####String Matcher
一些字符串的操作，例如：`startswith、endwith、include、startwith regex、not endwith`等
####Floatingpoint Macher
由于浮点运算会有一些精度的差，例如`0.9-0.8`结果可能是`0.09999999999998`, scalatest提供了plusOrMinus方法来给断言提供一个误差允许范围：
`(0.9 - 0.8) should be (0.1 plusOrMinus .01)` 允许结果再`0.1±0.01`误差范围内（2.0以后，`plusOrMinus`函数改成了`+-`

####Iterable Macher
 `List() should be(empty)
 8 :: 6 :: 7 :: Nil should contain(7)`  
 
####Seq and Traversable Macher
 对于Seq和Traversable类型，提供了length和size方法：
 `(1 to 9) should have length (9)`
 `(20 to 60 by 2) should have size(21)`
####Map Macher 
Scalatest提供了一些特殊的方法，用来判断key后value是否在map中：
`val somemap = Map("key1"->"value1")
somemap should contain key("somemap")`
####Compound Macher
Scalatest中的and和or方法可以用来在测试中使用组合的断言，如下：
`val ss = List("A", "B")
ss should(contain("A") and (not contain("C")))`
> and的语句必须被括起来；参数必须被括起来；使用Matcher的and和or并不是短路

Scala中有一个类型Option，包括Some和None，所以Scala很少使用null，但是scalatest支持java，所以可以使用null：
`someobj should (not be (null) and be "abc")`
如果someobj为null，这个语句会抛出异常，因为不短路，所以and后面的验证还是会执行，所以最好把这两个分开

####Reference Macher
 验证引用是否相等：
 `val debe = new Artist("debe")
 debe should not be theSameInstanceAs(new Artist("hha"))`
####Property Macher
验证对象是否含有某些属性
`obj should have(
	'title' ("ba")
	'year'(2015)
) `  (测试有问题，但是`"2.0" should have length 3`却是好的——因为对象对应的的property其实就是一定的了，static的已经值确定，而普通object也已经确定)

####java.util.Collection.machers
ScalaTest是Java友好的，因此可以像在Scala集合上做断言，使用和上面的例子相同

###Must Matcher
简单来说，上面的should替换成must即可。
`val list = 2 :: 4 :: 5 :: Nil
list.size must be(3)`
Must和Should的两个Matcher的不同只是在测试报告中体现。 
$2.0之后，must版本也被deprecated了$

###异常处理
在ScalaTest中，有两种方式来验证异常的抛出和捕获：
1. intercept block
2. evaluating block

####intercept block
intercept block这种方式把任何可能抛出异常的代码放入一个intercept代码块中，如果代码块没有抛出异常，则测试失败，如：
`"An blum" should {
	"throw some Exception"
} 

####evaluating block
这种方式抛出的异常代码放入一个evaluating代码块中，使用should或must加一个produce来指明异常类型：
`evaluating { s.charAt(-1) } must produce [IndexOutOfBoundsException]`
但是evaluating也在1.x被抛弃，现在使用：
`an [IndexOutOfBoundsException] must be thrownBy s.charAt(-1)`
或
`val thrown=the [IndexOutOfBoundsException] thrownBy s.charAt(-1)`--这句可以返回捕获的异常，可以做一些其他的判断

###Informers
可以在任何地方输出一些测试信息，例如：
`some clause
info("test some thing")
some clause`

###GivenWhenThen
Given：前置条件
When：产生了某个动作或处于某种条件下
Then：前面两个条件产生的结果
`class SetSpec extends FlatSpec with GivenWhenThen {
  "A mutable Set" should "allow an element to be added" in {
    Given("an empty mutable Set")
    val set = mutable.Set.empty[String]
    When("an element is added")
    set += "clarity"
    Then("the Set should have size 1")
    assert(set.size === 1)
    And("the Set should contain the added element")
    assert(set.contains("clarity"))
    info("That's all folks!")
  }
}`
三个方法都会像informers一样输出一些信息（也就是形式上的组合吧，没有产生任何测试上实质的不同）
###待测试
Pending Test，pending是一个占位符，可以将尚未实现或定义的测试以pending来填充，Pending Test实际上就是利用pending来将测试标记为TODO，例如：
`test("some"){
pending
}`直接标识即可

###忽略测试
在FuncSpec中使用ignore
`ignore("skip it"){
	some test
}`

###标记
打标签的一些场景：
* 你想跳过某些很费时的测试
* 某些测试是检查一些相关的功能 需要在一起执行
* 你想给测试分成单元测试、综合测试、验收测试等分类时

由于sbt是对所有包使用，而由于ScalaCheck不支持标签，（scalatest和Specs2才支持），所以sbt test 命令不支持标签；但是可以使用sbt test-only来处理，`sbt test-only ModuleName -- -n TagName`

##Specifications
###FunSpec
[FunSpec详细介绍](http://doc.scalatest.org/3.0.0/index.html#org.scalatest.FunSpec)
FunSpec包括describe clauses和tests，describe使用`describe`来定义，test使用`it`或者`they`，`describe`,`it`,`they`都是FunSpec中定义的方法，都会被$SetSpec$的构造函数调用，describe后面带上spec text来指定测试主题，而每一个test(it/they)在spec text上写入具体的行为。

	import org.scalatest.FunSpec
	class SetSpec extends FunSpec {
		describe("A Set") {
		    describe("when empty") {
		        it("should have size 0") {
			        assert(Set.empty.size === 0)
			    }
		        it("should produce NoSuchElementException when head is invoked"){
		           assertThrows[NoSuchElementException] {
			           Set.empty.head
			       }
			    }
			    they("should do someting for test"){
			    }
		    }
		}
	}
FunSpec的生命周期分registrations和ready两个阶段，开始是registration，然后调用run时进入ready阶段，然后在剩下的生命周期内都是ready阶段。
tests只可以在FunSpec的注册阶段，通过$it$和$they$来注册，如果已经到了ready（执行run后）进行it、they声明，则会抛出异常。
当执行FunSpec时，它将会将事件中的Formatters发送给Reporters，ScalaTest的内建reporters将report这些events，通过容易阅读的形式展示一些输出信息，这些信息中包括了测试的主题等。

$Documenters$
FunSpec也提供了一个markup方法，返回一个Documenter，允许你发送一个MarkDown语法格式化的文本给Reporter，你可以传递额外的信息给Documenter，通过使用它的apply方法，Documenter然后传递这个信息给Reporter通过MarkupProvided事件。
	
	package org.scalatest.examples.funspec.markup

	import collection.mutable
	import org.scalatest._

	class SetSpec extends FunSpec with GivenWhenThen {

	  markup { """

	Mutable Set
	———--

	A set is a collection that contains no duplicate elements.

	To implement a concrete mutable set, you need to provide implementations
	of the following methods:

		def contains(elem: A): Boolean
		def iterator: Iterator[A]
		def += (elem: A): this.type
		def -= (elem: A): this.type

	If you wish that methods like `take`,
	`drop`, `filter` return the same kind of set,
	you should also override:

		def empty: This

	It is also good idea to override methods `foreach` and
	`size` for efficiency.

	  """ }

	  describe("A mutable Set") {
		it("should allow an element to be added") {
		  Given("an empty mutable Set")
		  val set = mutable.Set.empty[String]

		  When("an element is added")
		  set += "clarity"

		  Then("the Set should have size 1")
		  assert(set.size === 1)

		  And("the Set should contain the added element")
		  assert(set.contains("clarity"))

		  markup("This test finished with a **bold** statement!")
		}
	  }
	}	
虽然ScalaTest的内置reporter通过一些格式展示markup文本，HTML reporter将markup信息格式化成HTML，markup的主要目标就是为HTML报告增加友好的格式。 
上面的SetSpec的HTML reporter的样子（但是怎么生成的呢？）
![上面的SetSpec的HTML reporter](http://doc.scalatest.org/3.0.0/lib/funSpec.gif)

http://doc.scalatest.org/3.0.0/index.html#org.scalatest.FunSpec
http://doc.scalatest.org/3.0.0/index.html#org.scalatest.FunSpecLike
http://www.scalatest.org/user_guide
$搞完之后，可以对比一些Suite和Fun的区别$

###FeatureSpec


sbt目录示例（$Testing in scala$）
├── src
│ ├── main
│ │ ├── java
│ │ │ └── com
│ │ │ └── oreilly
│ │ │ └── testingscala
│ │ ├── resources
│ │ └── scala
│ │ └── com
│ │ └── oreilly
│ │ └── testingscala
│ │ ├── Album.scala
│ │ └── Artist.scala
│ └── test
│ ├── resources
│ └── scala
│ └── com
│ └── oreilly
│ └── testingscala
│ └── AlbumTest.scala
##错误处理
1. 在使用时报错`java.lang.NosSuchMethodError: scala.runtime.OjbectRef.create(Ljava/lang/Object:)Lscala/runtime/ObjectRef)`   
__解决方案:__ 因为scalatest和scala版本不一致
2. 在使用sbt，配置好相关项目之后，运行sbt compile，报错：`object scalatest is not a member of package org`   
__解决方案:__ test的文件必须在src/test/main目录下，而源码文件应该在src/scala/main下面
sbt配合：   
	* 在.sbt/0.13/global.sbt下增加：（如果global.sbt不存在自己增加）   
	`resolvers += "Artima Maven Repository" at "http://repo.artima.com/releases"`
	* 在项目目录下增加build.sbt，并写入以下内容：   
	`libraryDependencies += "org.scalactic" %% "scalactic" % "3.0.0"`
	`libraryDependencies += "org.scalatest" %% "scalatest" % "3.0.0" % "test"`
	* 在项目目录下新增project目录（如果已经存在则不用新建），增加plugins.sbt，内容：
	`addSbtPlugin("com.artima.supersafe" % "sbtplugin" % "1.1.0")`
3. 