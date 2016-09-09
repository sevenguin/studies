#SBT
Simple Build Tool

* 依赖管理功能
	* Ivy用来管理依赖
* 所有任务的创建都支持scala
* 可连续执行命令
* 可以在工程上下文里启动REPL

##Install
###Windows
可以直接下载msi程序安装，安装后直接配置.bat到PATH中，则可以随处使用
###Linux
下载sbt-launch.jar
然后创建运行shell
> `#!/bin/bash
SBT_OPTS="-Xms512M -Xmx1536M -Xss1M -XX:+CMSClassUnloadingEnabled -XX:MaxPermSize=256M"
java $SBT_OPTS -jar `dirname $0`/sbt-launch.jar "$@"`

配置这个shell 到path中
直接执行此shell即可

##Hello World
创建hello目录，并且创建hello.scala代码：
`object Hi {
def main(args: Array[String]) = println("Hi!")
}`
在hello目录中，执行sbt，然后执行`run`子命令，会得到输出：
`Hi!`
在上面过程中，sbt将自动查找下列文件或目录：
* 当前目录下的源文件
* src/main/scala或src/main/java中的源文件（也包括这个下面的子目录）
* src/test/scala或src/test/java中的源文件
* src/main/resources或src/test/resources中的数据文件
* lib中的jar包

默认情况下sbt使用sbt自己使用scala版本来build工程

##Build Definition
大部分工程都需要一些手工设置，一般在项目目录下会有一个build.sbt来配置设置值。例如上面的，在hello目录下就会有一个build.sbt文件。
可以在hello/project/build.properties文件中强制指定sbt版本：
`sbt.version=0.13.11`
一般build的结果放在工程目录下的target下，所以.getignore一般包含此文件夹
.scala也可以组成build.sbt，例如：在project/Build.scala中进行定义和说明
###Running
####Interactive mode
直接在工程目录下执行`sbt`命令，不带任何参数
然后可以在子命令提示符下执行`compile/run`等命令，退出使用`exit` or `ctrl+D(Unix)/Z(Win)`
交互模式下sbt提供自动补全功能
####Batch mode
命令和参数可以用空格分开，如果命令带参数，则将该命令和所带参数用引号括起来：
`sbt clean compile "testOnly TestA TestB"`（这里扩的也只是`testOnly`的参数）
####Continuous build and test
`~ compile`
可以watch，如果有文件改动，则自动compile（or other command）
`~ sbt`
可以watch，如果有改动，则test
####Common commands 
命令列表
* $clean$ 删除所有生成的文件
* $compile$ 编译所有的main文件，src/main/scala(java)下面文件或base path下面的
* $test$ 编译和运行所有的测试，src/test/scala(java)
* $console$ 开启一个scala解释器，将当前编译的源文件和所有依赖纳入到classpath中
* $run$ 使用该sbt相同的jvm来运行此project的main class
* $package$ 创建一个jar文件，包含src/main/resources文件和src/main/scala(java)下源文件编译后的文件
* $help$ 帮助命令
* $reload$ 重新加载build definition，一般在修改了build definition之后使用

####History commands
命令列表
* $!$ history command help
* $!!$ 执行前一个命令
* $!:$ 列出所有之前的命令
* $!:n$ 列出最后n个命令
* $!n$ 执行第n个命令（like linux shell）
* $!-n$ 执行这个命令之前的第n个命令
* $!string$ 执行最近以'string'开头的命令
* $?string$ 执行最近的包含string的命令
###.sbt build definition
介绍build.sbt的语法和规则
每一个工程关联一个不变的map描述次工程，在build.sbt中，你可能创建一个$Project Definition$，Project位于当前目录，如：
`lazy val root = (project in file(".") ).
settings(
name:="somename"
)`
>A build definition defines Projects with a list of Setting[T], where
a Setting[T] is a transformation affecting sbt’s map of key-value pairs and T
is the type of each value.

build.sbt定义了一个工程，保存一个Scala表达式的列表——settings：
`lazy val commonSettings = Seq(
organization := "com.example",
version := "0.1.0",
scalaVersion := "2.11.7"
)`
`lazy val root = (project in file(".")).
settings(commonSettings: _*).
settings(
name := "hello"
)`
每一个Setting是由Scala表达式定义，setting中的表达式都是相互独立的，他们只是表达式而非完整的scala statement。
build.sbt一般定义为val、lazy val和def，像顶层的class、object等目前在build.sbt中是不允许的
在setting的左侧，像name、version这种都是key，一个key是一个SettingKey[T], TaskKey[T], or InputKey[T]实例，而key有方法`:=`，所以`name.:=value`其实也是可以的，只不过scala中可以对只带一个参数的函数采用这种方法调用：`name := value`, `:=`这个方法返回一个Setting[String]，所以value的类型不对，会报错。
setting会根据依赖有一个排序
####Keys
#####Types
key的类型
* $SettingKey[T]$ key值只计算一次，只在load这个project的时候计算一次
* $TaskKey[T]$ 可以每次都重新计算一次，a key for a value, called a task
* $InputKey[T]$ a key for a task that has command line arguments as input.
####Build-in keys
build.sbt隐式的导入了sbt.Keys，所以上面的name其实是sbt.Keys.name
####Custom keys
由上面Types的几个类型来定义，如：
`lazy val hello = TaskKey[Unit]("An example")`
为一个task定义一个key，叫做hello
#####Task vs Setting keys
一个TaskKey定义一个task——如compile、package之类，每一次执行sbt的task的时候，task将被重新跑一次
####Defining tasks and settings
使用:=，可以为一个setting赋值或者为一个task计算值,对一个setting，这个值将在第一次加载的时候计算。对task，在每一次task被执行时都会重新运算。
`lazy val hello = taskKey[Unit]("An example task")
lazy val root = (project in file(".")).
settings(
hello := { println("Hello!") }
)`
默认导入的库：
`import sbt._
import Process._
import Keys._
`
####Adding library dependencies
一般使用第三方库有两种办法：
1. 直接将jar包拖入工程
2. 使用工具管理依赖，例如使用build.sbt

这里说明的第二个方法，例如：
`var derby = "org.apache.derby" % "derby" % "10.4.1.3" 
lazy val commonSettings = Seq(
organization := "com.example",
version := "0.1.0",
scalaVersion := "2.11.7"
)
lazy val root = (project in file(".")).
settings(commonSettings: _*).
settings(
name := "hello",
libraryDependencies += derby
)`
注意$libraryDependencies $使用的是`+=`，这个表示append。表示当前项目依赖derby，其版本是10.4.1.3
上面的`file(".")`表示编译结果target放在当前目录，也可以自己指定目录

withSources() withJavadocs() 在libraryDependencies后可配置