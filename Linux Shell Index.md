#Linux Shell Index
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

###2. Some Command
shell参数一般有好几种格式，例如GNU是长命令`--param`，大部分使用的是短的`-param`， 还有一部分不用前缀，直接使用`param`
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
`du -s` 列出总大小
`du -c` 先输出明细，然后输出一个总的大小
####sort
`sort -n` sort命令会识别数字字符，然后按照数字大小排序
`sort -t : -k 3 -n /etc/passwd` `-t`指定分隔符；`-k`指定第几个`field`，然后按照这个field排序，这个命令的意思就是把`passwd`的第三列当做数字来排序
####grep
`grep -v t file` `-v`表示翻转，不匹配的结果，这里就是`file`中输出不包含`t`的数据
`grep -n t file` 可以列出匹配行的行号；`-c`表示匹配次数； `-e` 指定多个匹配，例如：`grep -e t -e f -e n file`匹配有`t`、`f`或`n`都可以（`[tfn]`使用正则表达式匹配）

#P127


