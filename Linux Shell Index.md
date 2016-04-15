#Linux Shell Index

@(Linux)

#####<< Linux Command Line and Shell Scripting Bible>>
###1. Base
The memory locations are grouped into blocks called pages. The kernel locates each page of memory either in the physical memory or the swap space. The kernel then maintains a table of the memory pages that indicates which pages are in physical memory and which pages are swapped out to disk.
>`ipcs -m`     allow you to view the current share memory pages on the system

The Kernel create the first process, called the *init* process, to start all other processes on the system.When the kernel starts, it loads the init process into virtual memory. As the kernel starts each additional process, it gives it a unique area in virtual memory to store the data and code that the process uses.

> `/etc/init.d /etc/rcx.d` 文件夹中包含了init启动时启动的程序，而rcx中的x是run level
> `ps -ax` 状态，S- sleeping；SW-Sleeping and Waiting；R-Running

The Linux system identifies hardware devices as special files, called device files.There are three different classifications of device files:
* Character *Character device files are for devices that can only handle data one character at atime*
* Block *Block files arefor devices that can handle data in large blocks at a time, such as disk drives*
* Network  *The network file types are used for devices that use packets to send and receive data.This includes network cards and a special loopback device that allows the Linux system*

> `ls -al` 列出的结果中，第一列 brw-rw---- 等，第一个字符就表示设备文件不同的分类

The kernel must be compiled with supports for all types of filesystems.
不同shell有不同的应用优势和倾向
X Windows相当于将这些外围硬件的接入做了一个集合，底层对接，后面的KDE等可以基于X Windows来构建更高层的应用
字符集：字符编码是基于字符集来编码，解码字符数据
Control Code、Display Buffer
Terminal emulation packages that can emulate different types of terminals.The terminfo database is a set of files that identify the characteristics of various terminals that can be used on the Linux system. 
> `/usr/share/terminfo` 存储不同类型终端类型的信息，都是按照首字母存放
> `inforcmp` 由于terminfo都是binary，所以可以用inforcmp来转换成text

* PS1 控制默认的行提示 `echo $PS1 -> [\u@\h \W]\$` P75
* PS2 控制第二层的提示（例如 >）

**Virtual Dictionary**:This is not the method used by Linux. Linux stores files within a single directory structure, called a virtual directory. The virtual directory contains filepaths from all the storage devices installed on the PC, merged into a single directory structure.
**Mount Point**:On the root drive, Linux creates special directories called mount points. Mount points
are directories in the virtual directory where you assign additional storage devices.
**Root Drive**:The first hard drive installed in a Linux PC is called the root drive. The root drive
contains the core of the virtual directory. Everything else builds from there.
在使用一个新的设备文件时，首先需要把它挂载到某个虚拟目录中。

####文件连接（file link）
If you need to maintain two (or more) copies of the same file on the system, instead of having separate physical copies, you can use one physical copy and multiple virtual copies,called links. A link is a placeholder in a directory that points to the real location of the file.
* Symbolic，or soft link
* A hard link
硬链接的inode相同，软链接的inode不同。软连接是一个新文件，存储指向的文件的信息
无论是软链接还是硬链接，拷贝链接文件，其实是拷贝原文件。如果想单纯拷贝链接文件，则重新创建链接即可。如果对软链接文件创建链接，则会产生一个链条，容易断裂造成很多问题 

####进程信号
|**Signal**|**Name**|**Description**|
|:--------:|-------:|:--------------|
|1|HUP|Hang up|
|2|INT|Interrupt|
|3 |QUIT |Stop running.|
|9 |KILL |Unconditionally terminate.|
|11| SEGV| Segment violation.|
|15| TERM| Terminate if possible.|
|17| STOP| Stop unconditionally, but don't terminate.|
|18| TSTP| Stop or pause, but continue to run in background.|
|19| CONT| Resume execution after STOP or TSTP.|
Bash Shell默认情况下忽略任何SIGQUIT（3）、SIGTERM（15）的信号量；Bash Shell处理它接收到的任何SIGHUP（1）和SIGINT（2）的信号量
后台进程模式就是一个进程运行时不把STDIN、STDOUT、STDERR关联到一个终端会话上
`command parameters &` 后台模式运行命令command 输出`[jobid]processid`，可以使用`ps`查看，即便是这样，也是关联到了某个`terminal`，如果这个`terminal session`结束，则这个进程也退出。
`nohup command paramters &` 这样可以避免和某个`terminal`关联，`nohup`取消了进程和终端的关联，所以进程失去了和STDOUT和STDERR的关联（其实是和默认的文件描述符的关联），因此进程所有的输出都重定向到一个文件`nohup.out`中
`$$` 表示当前脚本的PID
`jobs`列出所有的job
`Ctrl-Z`发送STOP信号给进程
`jobs -l` 列出的job中，有`+`的表示是默认处理的job（如果处理job的命令没有指定特定的job的时候）；`-`表示的是第二默认处理（第一个处理掉之后他就变成默认）
`bg/fg jobid` 表示将jobid的job以后台/前台方式从STOP变成Running
`nice`指定命令优先级，值越大则优先级越低，例如：
`nice -n 10 command &` 指定command的优先级在默认值上加10，也就是降低优先级
`renice`修改已经运行的进程的优先级，例如：`renice 10 -p 29504`降低`PID`为`29504`的进程的优先级
`at [-f filename] time` 定时执行某个脚本，`at`是将这个命令写入队列目录（/var/spool/at）中，然后进程`atd`定时（默认是60s）检查这个目录，按时执行特定命令。
`atq` 会打印出at增加任务，第一列是ID
`atrm`可以根据上面的ID来删除某个任务
`cron` at是某个时间执行任务，但是像每天、每月、每年这种周期执行，用`cron`
`crontab -e`可以用来增减需要周期执行的任务，格式一定，例如：
`00 12 * * * if ['date +%d -d tomorrow’ = 01 ] ; then ; command`
前面的格式：`minute hour dayofmonth month dayofweek command`，如果是`*`表示允许，上面就是每天12点执行。
`crontab -l`列出任务，和`at`一样，也有一个目录来让crontd来check，/etc/cron.*ly
`anacron` 如果在周期内机器关闭，重启时，一般不会去再执行机器关闭期间没有执行的任务，而anacron回在启动时执行周期内miss的任务。/var/spool/ana	cron.* 就是他的列表
**启动时执行**
按照不同的level（/etc/inittab中配置的）来配置文件，现在看系统目前处理方式是：将要启动时执行的命令都放在`/etc/init.d`目录中，然后`/etc/rc?.d`(?就是level)建立要执行的命令连接到init.d，这个。这个处理也可以理解，避免创建过多的相同的命令文件。（创建的是软链接，因为inode不同，且文件大小不一致）
现在正在朝Upstart init Process移动，这个是新的管理服务（上面的叫System V init），这些脚本不是按照run level来管理，而是按照startup event，文件在`/etc/event.d`中配置
`.bash_profile`文件执行，在一个新登录时。`.bashrc`在一个新的shell执行时执行。

####Linux环境变量
`printenv` 打印<font color='red'>***全局***</font>环境变量
全局环境变量也是可以被当前shell session创建的子进程访问
`set` 打印<font color='red'>***局部***</font>环境变量
标准的语法规则：自定义的局部变量是大写字符；系统的局部变量用小写字符
`export` 把局部变量变成全局变量
`unset` remove环境变量，注意unset时变量不要带`$`
#####login shell
`/etc/profile`  登陆时执行（所有用户都生效）`/etc/pfrofile.d` redhat里面没有，效果和profile类似
`$HOME/.bash_profile` 指定用户的环境变量（也是登陆时执行）(其他Linux版本这个文件名可能是`.bash_login`或`.pfofile`)
`.bashrc` 文件在用户输入bash而不login system时执行（但是怎么才会出现不login？而且不login怎么知道执行哪个user目录下的`.bashrc`---`/etc/bashrc`存在，所以这个问题解决了）
`BASH_ENV` 这个里面可以设置系统启动时需要执行的文件
#####File Permissions
`/etc/passwd` 里面可以看到有很多用户，其实有些用户不是实际的用户，而是`system user`，只要是用来控制访问资源的权限。`root`用户的`UID`是0；Linux将500以下的`UID`保留给`system user`。自己创建的都是从500开始。
`/etc/shadow` 文件控制Linux系统如何管理密码
`SGID` 在某个文件夹下创建的文件默认都是这个文件夹的组--group
`sticky bit` 文件一直保存在内存中，直到程序退出
`chmod g+s dirtest` 给dirtest这个目录增加`SGID`——`s`
####Linux filesystems
Linux支持一些文件系统来管理文件和文件夹，每一个文件系统实现虚拟目录接口都有稍许的不同，这个需要注意。
#####ext
使用虚拟目录来管理设备，然后存储数据使用固定长度的块。
使用***inode***来管理跟踪存在虚拟目录中的文件的信息。每一个物理设备上都会创建一个***inode table***
文件系统使用***inode***来区分文件而不是使用文件名和路径。所以才有了硬链接，由于文件系统文件目录是虚拟的，指向的是硬盘上的block，那硬链接其实是拷贝了一份inode数据，所以删除这个硬链接的文件其实只是删除了inode的一份数据而已，其他没变化
#####ext2
ext创建文件大小有限制（2GB），而且ext2增加了文件创建、修改、最后一次访问时间等信息。文件最大可以到32TB。ext存储文件的block通常是分散的，所以需要花费时间去找文件在disk上的block，而ext2是分组分配。
#####Journaling filesystem
不像上面的ext文件系统，先写入数据到磁盘然后再更新inode table（有可能写入磁盘inode table没有，导致文件丢失）。而这个是先写入一个临时文件（叫做***Journal file***），然后写入磁盘和更新inode table，操作做完之后，然后再删除临时文件。
######ext3 ext4 Reiser
这两个都算是Journaling filesystem，ext3对于意外删除的文件，不提供任何恢复机制；ext4支持压缩和加密（而且只讲首个block的地址保存到inode table）。这这几个格式只将inode table写入Journal file中，所以速度会快一点。
#####Journaled Fielsystem
看起来和ext3有点类似，不清楚区别在哪。ext3也是将inode table写入Journal file然后等到实际的数据写入存储设备之后，删除Journal file.
XFS属于此类系统
`fdisk`创建分区，然后`mkfs`来对创建的分区指定文件系统
####Logical Volume Managers
一个工具将多个磁盘进行逻辑上的集合，可以当做一个磁盘来用，上面的磁盘管理就是基本的对磁盘管理，而LVM在磁盘上和OS中间加了一层。
物理设备就是physical volumes（PV），每一个PV对应一个hard driver的一个物理分区。多个PV组成一个VG（Volume Group）。逻辑卷管理就把VG看成一个物理硬盘，而VG是由多个硬盘的多个物理分区组成。PV对一个到各个磁盘的特定物理分区;VG将PV这些分区逻辑上搞成一个大磁盘，而LV（Logical Volume）是和OS对接，对应OS创建的分区（对应于上面fdisk创建，只不过fdisk创建的是物理分区）
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

####Other Shell
#####dash
*The Debian dash shell has had an interesting past. It's a direct descendant of the ash shell, a simple copy of the original Bourne shell available on Unix systems. *
#####zsh
*Another popular shell that you may run into is the Z shell (called zsh). The zsh shell is an open source Unix shell developed by Paul Falstad*
####一些事
在脚本中使用mysql：
`MYSQL=‘which mysql‘
$MYSQL test -u test <<EOF
show tables;
select * from employees where salary > 40000;
EOF`
`lynx`可以用来浏览网页
`mutt` graphical e-mail客户端  



###2. Programming
####array
`arr=(one two tree)` 这就定义了数组；`$arr`只返回第一个元素；`${arr[n]}`是取第n+1个元素；`${arr[*]}`表示数组所有元素；其实shell里面加上`{}`主要是为了表示后面跟的是一个整体(如果这里不加`{}`,那`$arr[0]`输出结果就是`one[0]`，是`$`作用的变量名;`unset arr[n]` 删除某个元素
####redirection
`<` 输入重定向；`>` 直接写入;  `>>`追加
`<<`是多行输入，第一个输入的字符串作为marker，当再输入这个marker时，输入结束。所以第一次一盘是`EOF`
####exit status
`$?` 输出退出状态，获得最后一个命令执行的状态，`0`是成功
返回状态是在0和255范围，如果超过255则取余（除以256），例如：300则结果是44
|Code|Description|
|:--:|:----------|
|0|Successful completion of the command|
|1|General unknown error|
|2|Misuse of shell command|
|126|The command can't execute|
|127|Command not found|
|128|Invalid exit argument|
|128+x|Fatal error with Linux signal x|
|130|Command terminated with Ctrl+C|
|255|Exit status out of range|
####Structured Commands
#####if else elif
`if command
then
　　commands
elif command
　　commands
else
　　commands
fi` 
-->`if command; then ... fi`
command状态为0，则`if`处理为success
`test conditinos` 这个语句可以替换`if`语句中的`command`，这样就可以实现一些条件判断例如`2>3`之类。这个可以简写成：`[conditions]`
***数字比较***`test`命令的比较，下同
|Comparison|Description|
|:--------:|:----------|
|n1 -eq n2|n1 == n2|
|n1 -ge n2|n1 >= n2|
|n1 -gt n2|n1 > n2|
|n1 -le n2|n1 <= n2|
|n1 -lt n2|n1 < n2|
|n1 -ne n2|n1 != n2|
***字符串比较***
|Comparison|Description|
|:-------------:|:-------------|
|str1 =(!=,<,>)str2|str1等于（不等于、小于、大于）str2|
|-n str1|校验str1长度是否大于0|
|-z str1|校验str1长度是否为0|
由于`<`、`>`也有重定向的意思，所以再使用时必须转义：`[  $str1 \> $str2 ]`(大写字符小于小写字符)
`(( expression ))` 可以进行数字运算，这个expression也可以是赋值运算，如： `(( var = 2 ** 3 ))` ，`$var`结果为`8`, `**`为幂次运算

***File Comoparisons***
|Comparison|Description|
|:-------------:|:-------------|
|-d(-e,-f,-r,-s,-w,-x,-O,-G)file|是否存在且是文件夹（是否存在、存在切实文件、存在且只读、存在且非空、存在且可写、存在且可执行、存在且属于当前用户、存在且和当前用户属于同一用户组）
|file1 -nt file2|file1是否比file2更新|
|file1 -ot file2|file1是否比file2更旧|
这些只能比较整数，浮点比较不了
***Compound Condition Testing***
组合条件
`[conditions2] &&(||) [conditions2]`

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
####`(( expression ))`
 执行复杂的数学公式运算例如：
`(( var = 3 ** 2 ))` 结果就是`9`
`var++/ ++var/**/~/<</>>/&/|/!/&&/||` 这些运算符都可以，从`~`到`|`是位运算符
####`[[ expression ]]`
字符串比较，双中括号可以使用标准的string比较，如：
`[[ $user == r* ]]` 比较时还可以使用正则表达式

####Function
语法：
`function name {commands}` ***<font color=red>注意name和{中间有个空格</font>***
函数定义必须在函数使用之前，使用时直接用名字即可，就像执行命令：`name`
#####返回值
函数的退出状态就是函数中commands中最后一个command的退出状态，也是用`$?`来获取；可以使用`return n`来修改，n只能是整数，使用return时，有两点需要注意：
* Remember to retrieve the return value as soon as the function completes.
* Remember that an exit status must be in the range of 0 to 255.
如果函数想输出一个字符串或比255大的数字，则可以使用echo，然后使用一般的取值方法即可。
**记住：函数return的值通过$?来获得（相当于修改状态）；输出值通过\`\`赋值（当做一个命令来获得）**
例如：
`function func {var=0;(( var++));echo var}`可以通过\` func\`来获取`var`的值
#####传参
`$0、$1、$2....`用这些传参，`$0`表示函数名，`$n`表示参数（n>=1)
`$#` 表示传参的个数
* 全局变量 在函数中声明、定义的变量都算全局，修改函数外定义的变量值，在函数外也可见
* 局部变量 在函数中使用局部变量，格式为：`local var`，如：`local tmp=$[ $value + 5 ]`
数组传参，需要把数组元素当成参数传入，
使用`$@`获取整个数组，`$1`只能获取第一个元素而已
`function f { echo $1; echo $@; newarr=(``echo "$@"``); echo "${newarr[*]}"; }`
上面的echo中的``其实只有一个（Markdown不知道怎么把这个转义）
`f ${arr[*]}`将数组`arr`传入函数`f`，然后创建新数组将传入数组传给他。
#####library 
创建的脚本可以作为library，使用时不能直接在文件中引用`/...path.../scripts`，因为执行一个脚本是在新创建的shell中执行，而在新的shell中创建的变量、函数只在本shell中有用，也就是说scripts创建的东西只有在scripts中可用。
引用方式应该是：`source ./scripts` 或者简写为`. ./scripts` 由于source命令是执行脚本是在当前shell上下文中，而不是新创建shell，所以可行（注意这里scripts要么用绝对路径，要么用相对路径，即便是在当前目录中，也必须使用`./scripts`而不能直接使用`scripts`)。
将自己经常使用的命令组合写入`.bashrc中，这样每次登陆之后就可以直接使用函数了。
####Text Menu
每次都是刷新屏幕，然后重新输出（先clear，然后再echo），详见$P433$
`select option in options;do dosomething; done`这个命令也很有用，对于这种菜单很适合
`zenity`是一个窗口工具`zenity --calendar`就能调出一个日历窗口

####Regular Expression
对字符串进行正则表达式匹配：
![正则表达式模型](./1460517224309.png)
一个正则表达式被正则表达式引擎执行，在Linux中，有两个比较流行的引擎：
* $BRE$ The Posix Basic Regular Expression engine
* $ERE$ The Posix Extended Regular Expression engine

$BRE：$
下面是一些特殊字符的含义
* _**^**_ 一般表示行首，但是在[]中时表示反向——不匹配的
* _**$**_ 表示行尾
* _**.**_ 表示任何字符，除了newline字符
* _**[abc]**_ 表示[]中匹配任何一个，[^ch]表示不匹配所有
* _**[1-9]**_ 表示范围1到9
* _**[[:alpha(alnum,blank,digit,lower,print,punct,space,upper):]]**_ 匹配字符（大小写都匹配）、数字和字符、k空格或tab、数字（0-9）、小写字符、可打印字符、标点符号、空格、大写。
* _*****_ 出现0或多次（表示前面的字符，如果是所有字符，应该是`.*`

$ERE：$
* _**?**_ 表示前面的字符出现0次或一次。 `x?` 表示x出现0<=次数<=1
* _**+**_ 出现一次或多次，即最少出现一次
* _**{m}、{m, n}**_ 前面的字符出现m次或最少m、最多n次，默认gawk不识别这个，需要增加`--re-interval`，例如：`gawk --re-interval 'expression'`
* _**expr1|expr2**_ 字符串expr1出现或expr2出现，这种前后是两个expression而不是像[]是字符，所以expr1和expr2可以不只是简单的字符串，还可以是正则表达式
* _**()**_ 这里面的东西被当做一个单独的字符处理，例如：`gawk /Sat(urday)?/{print $0}`，表示urday这个字符串出现0次或一次；

$正则表达式最短匹配$
默认正则表达式是贪婪匹配，就是匹配最长的，例如：`a.*b`匹配`aabab`会匹配整个字符串，而如果你想匹配`aab`和`ab`的话，则需要使用懒惰匹配，下面是集中情况，基本就是在多个匹配后加上？：
* $*?$	重复任意次，但尽可能少重复
* $+?$ 	重复1次或更多次，但尽可能少重复
* $??$ 	重复0次或1次，但尽可能少重复
* ${n,m}?$	重复n到m次，但尽可能少重复
* ${n,}?$	重复n次以上，但尽可能少重复


###3. Some Command
shell参数一般有好几种格式，例如GNU是长命令`--param`，大部分使用的是短的`-param`， 还有一部分不用前缀，直接使用`param`
####一些注意点
* ***$15***其实输出的是第一个参数和5，如果`$1`是`date`，结果就是`date5`，所以访问时需要加上`{}`——`${15}`
* 变量：赋值时不用$，使用时才需要
* ` `` `这个是将运行结果赋值给变量，而不是只执行命令，只执行命令时只需要直接写出来即可
* 
`trap commands signals` 在接收到`signals`时执行commands命令，例如：
`trap "echo 'sorry, i have trapped Ctrl-C'" SIGINT SIGTERM`  signal可以多个
`trap - siganls` 移除对信号的监控，例如：`trap - EXIT`

`bc` 浮点运算；`scale`可以用来指定精度
####uptime
系统目前状态统计命令
`df`统计磁盘使用
`free`统计内存使用
####yum
`yum localinstall package_name.rpm` 本地安装软件
`yum list updates` 查看可用的更新列表
`yum remove package_name` 卸载某个package，但是保留他的configure等文件
`yum erase package_name` 卸载某个package，并且删除他的所有文件
`yum clear all` `yum deplist package_name`查看package_namede依赖；`yum update --skip-broken` 允许跳过broken dependency的包，先更新其他包（broken dependency是多个包依赖同一个包，遭到覆盖的问题）
`yum repolist` 列出资源列表；`/etc/yum.repos.d`设置资源列表
####expr
`expr 3 + 4` 数学运算，结果是7；`\*`乘法需要这样处理一下；`expr STRING:PATTERN`还可以这么返回正则表达式匹配的结果。P260
`$[5 + 2]` 这个也可以运算
这些只支持`整数`运算

####echo
`echo -n` 输出数据但是不换行；多个字符串输出，放在一起就是连接了，而且加不加引号都当做字符串，例如：`echo this's a dog's shoe`结果是`thiss a dogs shoe`，把`'`当做标识字符串的，而不是实际的数值。如果要输出这个`'`则需要用双引号把这行数据引住。

####useradd userdel usermod passwd chpasswd
`useradd -D` 列出新增的user，系统给他默认的参数（例如：home目录、shell等）;还可以带参数修改默认值，例如`-s /bin/ksh`就可以修改默认的shell
`userdel -r user` 删除user，只是删除user，而不删除创建的那些目录
`usermod -l/L/p/U` 修改用户
`passwd` 改某个用户的密码
`chpasswd <filelist` 用来批量修改用户名， `filelist`中是用户名密码对，格式是：`userid:passwd`
####chsh chfn chage
`chsh -s /bin/csh test` 修改用户`test`的默认shell类型
`chfn `可以设置用户的comment，例如用户的电话等，也是在/etc/passwd中存储
`finger` 可以查看用户的这些comment
`chage` 可以用来修改用户密码的时效（过期时间等）

普通文件的类型（就是`ll`命令列出的第一列的第一个字符）
*  \- for files
* d for directories
* l for links
* c for character devices • b for block devices
* n for network devices
####umask
`umask`列出的创建文件默认的权限（是反的，普通文件最大是`666`，`umask`如果是`0022`，则文件权限就是`644`；目录最大是`777`）
####chmod
`chmod [+-=]` 修改文件权限(增加、修改、设置为)
####chown
`chown options owner[.group] file` 修改文件所属用户（组），组可以单独指定也可以不指定，单独指定的话：`.group`


#### ls
LS_COLORS 控制ls显示文件、目录的颜色
ls 第一行显示的total xxx，表示的是总的block数量，包含在该目录中
`ls -F` 末尾带/ 都是文件夹，带*都是可执行文件
`ls -R`可以递归显示，如果显示的第一层中有文件夹，则也显示文件夹的信息
`ls -i` 列出文件inode
`ls -s`列出文件占用block的大小，大小都是块大小的整数倍，所以会大于等于实际大小

####touch
`touch -t 2011122451200 file` 可以创建文件的时候指定文件的时间戳

####cp
`cp -p src dst` 可以保证dst和src的修改时间相同
`cp -l` 可以创建硬链接从dst到src

####rmdir
`rmdir --ignore-fail-non-empty` 删除文件夹，如果文件夹非空则不报错（但是也删不掉）

####file
`file filename`看文件的类型
* Textfiles
* Executable files
* Data Files

####cat
`cat -n file` 列出文件的行号 `cat -b`只对非空行标行号
`cat -s file` 把多行空行合并成一个空行 `cat -T`不显示tab字符串

####more less tail head
`tail -s sec` 和`-f`一起使用，sleep sec 秒后才输出

####ps
`ps -l` 输出很多格式 `PRI`为优先级，越大优先级越低;`STAT`由两个字符组成，第二个字符定义进程状态，例如是`l`表示的是多线程；`+`表示在前台跑等。 P108
`ps -H` 输出进程按照层级的格式（父-子层级）

####top
`top`包含很多命令，运行`top`之后可以直接输入某些字符，改变展示信息。P111

####kill
`kill`其实是指定发送信号给进程，用`-s`指定信号，信号是上面缩写的进程信号
`killall`来杀掉名字匹配的进程，可以通配

####mount P115
`mount -t type device directory` 例如：`mount -t vfat /dev/sdb1 /media/disk`
`mount -t iso9660 -o loop MEPIS-KDE.iso mnt` 挂在iSO到一个目录
`mount -t cifs -o username=weileilei,password=familysh@1 //192.168.112.28/pa ./windows/` 虚拟机中的Linux把Windows的共享文件夹挂在到目录下

####unmount
`unmount [directory | device]`取消挂在

####df
已经删除或创建，在df中没有列出来，所以有延时

####du
the disk usage for a specific directory
`du -s` 列出总大小·
`du -c` 先输出明细，然后输出一个总的大小
####sort
`sort -n` sort命令会识别数字字符，然后按照数字大小排序
`sort -t : -k 3 -n /etc/passwd` `-t`指定分隔符；`-k`指定第几个`field`，然后按照这个field排序，这个命令的意思就是把`passwd`的第三列当做数字来排序
####grep
`grep -v t file` `-v`表示翻转，不匹配的结果，这里就是`file`中输出不包含`t`的数据
`grep -n t file` 可以列出匹配行的行号；`-c`表示匹配次数； `-e` 指定多个匹配，例如：`grep -e t -e f -e n file`匹配有`t`、`f`或`n`都可以（`[tfn]`使用正则表达式匹配）
####bzip2 compress gzip zip
`bzip2` 对应文件格式为`.bz2`
* `bzip2` 压缩文件
* `bzcat` 展示压缩文件内容
* `bunzip2` 解压文件
* `bzip2recover` 恢复损坏文件

`compress`对应文件格式为`.Z`
`gzip` 对应文件格式为`.gz`
* `gzip gzcat gunzip` 压缩、展示、解压

`zip` 对应文件格式为`.zip`
* `zip zipcloak zipnote zipsplit unzip` 创建压缩文件、创建加密的压缩文件（包含文件列表和目录列表）、解压压缩文件注释、拆分压缩文件、解压文件
####tar
`tar -c` 创建归档文件，归档的意思是把目录、文件搞到一个文件里面 `-x`解压 `z` 将归档文件重定向到gzip压缩成gzip格式文件
####alias
`alias -p` 列出所有的别名

####sed
$Stream editor$ 先设定一些编辑规则，然后将这些规则设置于数据流。sed$读取数据中的一行$，然后用指定的所有命令处理，然后输出到STDOUT。
`sed options script file`，下面是`options`的列表：
|Option|Description|
|:----:|:----------|
|-e script|增加脚本script的命令处理文本，这里的脚本是直接在命令行，不是文件中|
|-f file|增加file中的命令处理文本，和上面一样的效果一样，只是来源不同|
|-n|先不对任何命令产生输出，直到显式使用`print--p`输出|
`sed s/old/new/[g] text` 其中`s`命令的意思就是将第一个字符（old）替换成dierge（new）;`g`是可有可无，表示是否替换全部匹配，默认是匹配第一个匹配到的字符串
`sed -e s/old1/new1/; s/old2/new2/ text` 多个命令一起，使用`-e`参数，将后面的堪称一个脚本
`sed -f scripts data` 这就体现了和上面`-e`的区别，`-f`是实际上从文件读取命令。scripts文件内容：`
s/old1/new1/
s/old2/new2/
s/old3/new3/
`
#####sed 的替换选项
上面只说了`s`是替换，后面跟`g`表示替换所有查找到的字符串，下面是其他几个：
格式是：`s/pattern/replacement/flags`，下面是flags列表：
* $数字$ 表示替换第几个匹配到的
* $p$ 所有被替换修改的内容都被展示，所以加上sed的参数`-n`才能只输出被修改的，因为默认sed输出所有的被修改的和没被修改的行
* $w file$ 将替换结果写入文件（没有替换的就不写）
#####Using Address
如果只处理某些行，可以指定行处理，有两种方式指定：
* 一个行范围，例如第2行到第8行
* 使用text pattern来过滤行

格式如下：
`[address] command`例如：`
address {
　　command1
　　command2
　　command3
}`
`sed '2s/old/new/' text` 只替换第二行
`sed '2,5s/old/new/' text` 替换第二行到第五行的，`$`表示最后一行
`sed '/pattern/s/old/new/' test` 匹配到pattern的行都处理
`sed '2,${
s/old1/new1/
s/old2/new2/
}' data`    批量处理
#####删除行
`d`，例如：
`sed 'd' data1` 删除所有数据
`sed '3d' data` 删除第三行
`sed '/number 1/d' data` 删除匹配到'number 1'的行
可以两次匹配指定范围：
`sed '/pattern1/,/pattern2/d' data` 从pattern1匹配到的到pattern2匹配到的整个范围内的行都删掉，如果第二个pattern2没有匹配到，则直至末尾
#####insert and append
* insert （i command）
* append （a command）

`sed '[address]command' "new line"` 用新行用引号括起来或直接新起一行，用`\`来和命令连接
`sed 'i "Test Line 2"' 'TEST line 1'` 在第一行前插入第二行
`sed 'a "Test Line 2"' 'Test Line 1'` 在第一行后附加第二行
#####change
可以修改整行内容：
`sed [address]c "new line"` ，例如：
`sed /number 1/c 'hello'` 将'number 1’匹配到的行都替换成hello
#####transform
修改单个字符：
`[address]y/inchars/outchars/` 一对一的将inchars的字符替换成outchars，例如：
`sed 'y/123/789/' data` 将所有行（因为没有address）的1替换成7,2替换成8,3替换成9
#####print
* $p$ 打印数据  `sed '2,3p' data` 列出2-3行,`sed -n '/pattern/{commands}'`commands可以多行命令
* $=$ 打印行号  `sed '=' data`显示每行行号，`sed -n '/pattern/{=; p}' data` 列出pattern的行和该行行号
* $l$ 允许打印可显示和不可显示的字符（例如\t等） `sed -n 'l' data` 最后还会展示结尾符——`$`
#####read file
从文件读数据，插如到匹配模板后的数据：
`sed '/number 2/r datafile' data` 将datafile文件数据读取出来，然后插入data匹配到number 2后面；
`sed '3r datafile' data`将文件内容读取出来放在第三行后；可以将3替换成`$`，表示插入在最后
####多行操作命令
* $N$ 将数据流的下一行增加成一组来处理
* $D$ 在多行处理中删除单行  `sed '/ˆ$/{N ; /header/D}'` D删除的是前面的空行，而header是为了保障，两行中第一行是空行，第二行包括header的（其实如果前后两个匹配都出现在第一行也没问题，只不过这个例子中第一个匹配的是空行，第二个肯定不会出现在第一行了）（这两行其实组成了多行匹配空间——$mutiline pattern space$）。会强制sed返回脚本的最开始，然后在相同的pattern space上重复执行这个命令（不会从data stream中读新行）
* $P$ 在多行处理中打印单行 当多行匹配到时，P只打印匹配空间中的第一行
######$N$ The Next Command
`n` 是将下一行放到pattern space，而`N`是将下一行增加到pattern space
`n` 这个只是指单独的下一行，例如：`sed '/header/{n; d} text'` 将包含header字符串的行的下一行删除，所以`n`只指定了一行而已
`N` 合并多行处理， 例如：`sed '/header{N;  s/\n/ /}' text` 将包含heard的行和他的下一行用空格连接成一行（这里注意，`N`处理了`\n`，而`n`命令没这个能力）。其实理解起来还是容易理解的，`N`将匹配的行和下一行放在一起处理，这个时候要处理的数据是两行，而这个数据中肯定包括换行符，所以能处理
####Hold Space && Pattern Space
Pattern Space就是放入字符串要匹配；Hold Space是你可以在处理其他行时，使用hold space临时存放text的一些行，下面是一些命令：
|Command|Description|
|:-----:|:----------|
|h|copy pattern space to hold space|
|H|append pattern space to hold space|
|g|copy hold space to pattern space|
|G|append hold space to pattern space|
|x|exchange contents of pattern and hold spaces|
无论是打印还是匹配都是处理的pattern space，从第一行处理开始，首先将数据放入pattern space。通过下面这个例子理解：
`sed -n '/first/{
h      #把pattern space的数据拷贝到hold space
p      #打印pattern space
n      #将匹配到first的行的下一行写入pattern space
p      #打印pattern space——匹配到first的行的下一行
g      #将hold space拷贝到pattern space（即匹配到first的行）
p      #打印pattern space——这个和第一次p的结果应该是一致的
}' data`
`!` 用来取消一个命令，例如：`sed -n '/header/!p' data` 匹配到header的数据不打印，否则则打印，相当于对匹配取反一样；`$!N` 表示最后一行不取下一行；`1!G`表示第一行不将holdspace附加到pattern space
`$` 表示文件的最后一行；
`sed -n '{1!G; h; $p}' data` 倒叙文件，注意最后一个`$p`只有到最后一行才处理`p`打印pattern space
$一开始时，hold spac为空，直接使用G，则相当于在pattern space后加上空行$
#####Branching for Sed
`branch`语法：
`[address]b [label]`  address是行数区间或者匹配字符区间，address决定哪些行触发branch command；label定义了branch命令执行的位置（类似goto语句），如果label没有设置，那就相当于没有指定command——也就实现了某一段数据的翻转处理，例如：
`sed '{2,3b ; s/This/this/; s/line/Line/}' data`  表示第2/3行处理branch命令，由于label没指定，则就是2,3行没有branch command，所以只有2,3行不处理（相当于2/3行翻转不处理）
`sed '{2,3b label; s/This/this/; :label; s/this/This/}' data` 表示2，3行执行后面的`/this/This`，而其他行处理`/This/this`，这里的label就实现了branch command位置指定的功能。
使用这个可以实现循环：
`sed -n '{
:start
s/old/new/1p
b start
}' data` 每次处理到start都直接跳到start标签，没指定范围就是从第一行开始。这是个死循环，可以在b前面增加范围——/old/当把所有old都替换掉之后就不会再出现问题了。
`test`语法
和`branch`语法相同，但是address是用一个替换命令而不是范围指定，例如：
`sed '{s/old/new/t s/oldother/newother/}' data` 只有前面的`/old/new/`替换失败（就是没有替换到）的时候才会执行后面的`/oldother/newother/`否则不执行后面的。
#####Pattern Replacement
`&` 指向在替换命令中匹配到的字符，例如：
`echo "The cat sleeps in his hat." | sed 's/.at/"&"/g'`
结果就是：`The "cat" sleeps in his "hat".`，所以`&`就表示`/.at/`匹配到的`cat`和`hat`
在sed的匹配正则表达式里面：正则表达式中()/{}都需要转义。这些属于extend regular expression，sed里面需要转义，否则需要使用参数-r。例如：
` s/\(.*[0-9]\)\([0-9]\{3\}\)/\1,\2/`  还有`\1`、`\2`这种是匹配到的第一个、第二个字符串，所以`()`还有提取功能，匹配的能通过数字索引到
$猜测：sed使用的正则表达式使用的是懒惰匹配——最短匹配法$

####gawk
gawk是GNU版本awk程序
在gawk中你可以做一下操作：
* 定义存储数据变量
* 使用运算（字符或数字）操作数据
* 使用结构化语句，如`if-else`
* 从文件数据中按照格式抽取数据（例如抽取某些列）
`gawk options program file`下面是options可用列表：
|Option|Description|
|:----:|:----------|
|-F fs|指定文件分隔符|
|-f file|指定读取程序program的文件|
|-v var=value|定义变量和变量默认值|
|-mf N|定义可以处理的最大数量filed|
|-mr N|定义可以处理的最大记录大小|
|-W keyword|指定兼容方式或warning level|
`gawk '{print "hello world"}'` 必须使用`'{}'`来把命令行括起来，这样gawk就把这个脚本当做一个单独的文本字符。
gawk的文本可以通过STDIN输入，如果要停止，则`CTRL-D`来发送`EOF`终止输入（输入一行，gawk就处理一行）
$处理data field变量$
* $0 表示整行数据
* $n 表示第n行数据

每一个data filed都是被FS指定的分隔符分割的Field，默认是任何空字符（空格、tab等）
`echo "My name is Rich" | gawk '{$4="Christine"; print $0}'` 修改第四列，然后输出整行
***BEGIN END***
`gawk 'BEGIN {print "header"}'` BEGIN的比gawk后面指定的脚本先执行
${}组合一组命令，为一个script；每一组里面可以多个命令，用;来区分$
对应begin有个end：
`gawk 'END {print "END of process"}'`
这种BEGIN END就像单元测试里面的teardown和setup一样，程序运行完、之前执行一次

#####使用变量
* build-in变量
* User-Defined 变量

$build-in 变量$
|Variable|Description|
|:----:|:----------|
|FILEWIDTHS|有空格间隔的一个数字列表，每个数字表示要读取的长度（位数），数据项按位数读|
|FS|输入的数据项按照分隔符读，filed|
|RS|定义了记录的分隔符，相当于把哪些数据算作一组来进行数据项读取，例如一段数据为一个record|
|OFS|输出数据项分隔符|
|ORS|输出记录数据分隔符｜
例如：
`gawk 'BEGIN{FIELDWIDTHS="3 5 2 5"}{print $1,$2,$3,$4}' data1b` 对一个record（默认是一行），读3位、5位。。
`gawk 'BEGIN{FS="\n"; RS=""} {print $1,$4}’ data2` 一行数据为一个field，然后按照RS将多行组成一个record
$P541$提供了很多内置变量列表
$User Defined 变量$
直接赋值和使用，例如：
`gawk 'BEGIN{
test_var="Hello"
print test_var
}'`
因为gawk可以引用脚本，所以可以在命令行上指定变量值，然后在脚本中使用：
$script:$
`BEGIN{FS=“,”}
{print $n}`
`gawk -f script1 n=2 data1`  这里n指明了打印data1的第几列，在BEGIN中定义使用变量不需要带上$，有一点就是BEGIN中获取不到命令行传入的变量，如果BEGIN要访问，则gawk带上参数`-v`。
`gawk 'BEGIN{
 var[1] = 34
 var[2] = 3
 total = var[1] + var[2]
 print total
 }'` 使用数组
 `for (var in arr){
	statement
}` for循环， arr[var]来获取元素值，var是索引而不是元素
`$n ~ /regular pattern/{print dosomething}` 指定某个项，对这个项进行正则表达式匹配（`~`就是用来提供对某些字段来做正则表达式处理的；反向操作可以：`!~`）
`-F:` 这个是指定`FS`的简写形式 
`gawk -F: '$4 == 0{print $1}' /etc/passwd` 打印第四列为0的数据的第一列（前面可以指定条件）
`if (condition) {statement1}`， 例如：`gawk '{if ($1 > 20) print $1}' data4`
`while(condition){}；do{}while(conditions)`语法和shell一样，位置和gawk的if一样，也是在{}里面
`for( variable assignment; condition; iteration process){}` 例如：`for (i = 1; i < 4; i++)`
`printf "format string", var1, var2` 格式化输出，类似C的`printf`，$	556$
`cos(x)、exp(x)、int(x)、log(x)` 等，有很多数学函数可用 $558
`asort(s[,d])、asorti(s [,d])、gensub(r, s, h[, t])、index(s, t)、length([s])、tolower(s)、toupper(s)`等，字符串处理函数
`mktime(datespec)、systime()、strftime(format [,timestamp])` 时间处理函数
$User-Defined Functions $
`function name([variables])
{
statements
}`
`gawk
function myprint(){
	print somthing
}
BEGIN{FS="\n"; RS=""}
 `
 还可以创建function library，专门创建一个文件写函数，然后使用`gawk -f funclib ...`来引用名为funclib的function library文件
 











#P538


