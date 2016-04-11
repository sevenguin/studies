###Linux Common
####Presenting Data
#####File Descriptor
* 0 STDIN Standard Input  `<` 来重定向输入
* 1 STDOUT Standard Output `>`重定向输出；`>>`追加文件，$重定向STDOUT不会自动重定向STDERR$
* 2 STDERR Standard Error  `2>`用来重定向STDERR，例如：`ls -al badfile 2> test4`
例如：
`ls -al test test2 test3 badtest 2> test6 1> test7` 重定向STDERR和STDOUT
`&>file`将STDOUT和STDERR都重定向到相同文件
`echo 'this is a error message' >&2` 将这个输出重定向到STDERR，这样可以在脚本中区分错误日志和正常日志；***当然这只是临时重定向，只对本次有效***
`exec 1>outfile; exec 2>errfile;exec 0<infile`用来***持久***重定向各个描述符
也可以用这个来创建自己的描述符，`exec 3>stdfile; echo somthing>&3`这样就可以将输出按自己的思路重定向了
`exec 3>&1; exec 1>otherfile; ....; exec 1>&3` 先保存STDOUT到文件描述符`3`然后，再对STDOUT重定向，然后再把STDOUT重定向回来。可以注意一下，这里在`>`的右边的，如果是文件名的话就不用带`&`，如果是文件描述符则需要带`&`，可以将描述符理解成指针，指向文件名标识的文件。而`&`其实就类似与C语言的指针取变量。
`exec 3<>testfile` 3的输入输出都是testfile
`exec 3>&-` 关闭3这个文件描述符
`lsof` 列出打开的文件描述符
`/dev/null` 将输出重定向到这个位置，就是阻止了输出内容展示到terminal或file
`cat /dev/null > file` 这样可以清空文件`file`--算是一个小技巧
`mktemp` 创建临时文件，如：`mktemp testing.XXXXXX`后面的`X`是在自动生成，有多少个`X`就自动生成多少个字符，而且各数量可以设置，必须大于等于最低数量。如果带上参数`-t`,则在系统的`/tmp`目录下创建。`-d`是创建临时目录
`tee file`可以把输出重定向到屏幕和文件（两个都显示）；`-a`是append，例如：
`who | tee testfile`即把`who`的结果输出到屏幕，也写入到`testfile`中



###Linux Programming
####`case`
case语句的语法：
`case var in
　　pattern1|pattern2) commands;;
　　pattern3) commands;;
　　*) default commands;;
esac`
####`for`
**for语句语法：**
`for value in values
do
　　commands
done` 
其中`value`这个变量的值会被后面的程序使用。其中`values`可以替换成命令输出，如`cat file`。将values整体替换成`cat file`即可（这个本身就是输出）
`for`默认是通过空格来作为分隔符，可以通过制定`IFS`的值设定分隔符，例如设置成按行分割：`IFS=$'\n'`,***一定要注意***这里的`'\n'`前面带了`$`,如果不带，则赋值的不会转义，也就是`IFS`的值为字符`n`，`IFS`可以指定多个分隔符：
`$'\n':\;\"`后面两个需要转义，但是这种和`\n`不同，`\n`需要用引号和$来确定，其他的不用。
`$"abc"`结果就是`abc`，`$'\;'`结果就是`\;` **`$`这个符号的作用和本质需要钻研下。**
**for C style 语法**
`for ((
　　variable assignment;
　　condition;
　　iteration process
))`例如：
`for (( a = 1; a < 10;  a++))`
####`while`
语法：
`while test command; do other commands; done`
例如：`while [ $var -gt 0 ]; do echo $var var=$[ $var - 1]; done`
`while`里面的`test command`可以使多个命令行，但是只有最后一个test命令决定`while`是否循环。例如：`while echo $var; [ $var -ge 0]; do ...; done` 只有最后一个`[  $var -ge 0 ]`对状态有效
####`until`
语法
`until test commands do; other commands; done`
就是C里面的` do{} while`
####`break continue`
`break n` 可以跳转到第`n`层循环，默认是`1`表示自己，自己是第一层、再外面是第二层，以此类推。这个是从内到外计数
`continue n` 和break类似，会跳过`n-1`的内层语句，继续执行第`n`层语句
**循环语句重定向** `....; done > file.txt`
####Command Line Prameters
`${10}` `9`之后必须使用`{}`来标识
`basename` 输出程序的名字，不包含路径，例如：`basename /usr/bin/python`结果是`python`
`"$1"` 用`""`括起来，这样可以保证这个参数是以一个参数传入的（如果不带，而$1带空格，就会被当做两个）
`[ -n "$1" ]` 表示是否存在`$1`这个参数
`$#` 表示输入参数的最后一个参数值
`$*` 表示把所有参数当做一行处理（例如：`one two tree`被当做一个参数，`for in`的时候就这个一行输出
`$@` 把所有参数当做单独的变量处理（例如：`one two three`被当做三个参数，`for in`的时候输出就是：`one`、`two`、`three`
`shift`	直接使用不带任何参数，就会将参数`$2`移到`$1`
`getopt options optstring paramters` 命令格式化，例如：
`getopt ab:cd -a -b test1 -cd test2 test3` 这里指的是option，只有abcd四个，冒号表示谁的option的value在哪里，如abc:d：表示，ab的value在--后面（最后），而c和d的value就紧跟他们option的后面
`set -- 'getopt -q ab:c "$@"'` getopts格式化后，产生的输出覆盖`$@`的所有参数（`'`对`getopt`的单引号应该是反引号——**`` ` ``**
（因为有些`-x`不需要带参数，所以使用`--`按顺序分割，如果需要带参可以直接入：`-a:abc`后面带参，`--`可能表示命令需要主参数，而不是前面`-x`的子参数）
`getopts optstring variable` 其中`optstring`和`getopt`类似，这个命令带了两个内部的变量`OPTARG`表示当前参数的带的参数（如果这个变量是带参数的）；`OPTIND`表示当前参数的位置。
`read -p 'Enter: ' firstname secondname` 提示`Enter:`然手输入两个参数，赋值给`fitstname`和`secondname`; `reat -t`指示`read`的超时时间；`read -s` 输入密码是使用这个，可以不回显输入值。
`cat testfile | while read line`可以按行读取文件




####Linux Shell Command
####`(( expression ))`
 执行复杂的数学公式运算例如：
`(( var = 3 ** 2 ))` 结果就是`9`
`var++/ ++var/**/~/<</>>/&/|/!/&&/||` 这些运算符都可以，从`~`到`|`是位运算符
####`[[ expression ]]`
字符串比较，双中括号可以使用标准的string比较，如：
`[[ $user == r* ]]` 比较时还可以使用正则表达式

###P384

