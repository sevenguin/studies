# 移动UI设计-Sketch

一些UI设计的基本知识和Sketch的学习、使用经验。

## Base

#### 字号、字体

分iOS和Android两个来说：

* __iOS__：中文字体为Heiti SC（黑体，华文黑体），字号使用pt（Point，磅因，国际通行印刷单位）
* __Android__：原生系统默认字体为Droid Sans Fallback，字号为dp和sp
  * __dp__：Density-independent pixels，写作dip或dpi，最常用，160ppi（像素密度）屏幕，1dp=1px，换算公式：1dp*屏幕ppi/160=1px
  * __sp__：Scale-independent pixels，一般有小、正常、大、超大等，以160ppi屏幕为标准，字体大小为100%时，1sp=1px。如果设置手机字体大小，sp的也会受到影响，而dp不会。

## Sketch

Tools中的Outline工具可以将文字转化为矢量路径，这样就可以使用路径工具对字体进行重新设计了。

可以将复用的控件创建为元件，这样修改一个的属性则会体现到所有使用这个元件上。

page、artboard、独立图层（注释图层）

右侧属性区域，线的Borders，⚙图标点击：

* __Ends__ 线端点部分的图形
* __Joins__ 线相接部分的图形


插件：

Measure、Notebook：可以用来标注设计元素的注入大小、位置等要素

其他工具：

Promotee：软件将设计稿通过仿真效果呈现（只是仿真设备中）；

Mockup：模拟真实使用场景（注重场景，智能的投入到各种场景中）;

Pixate: 动态效果设计器

Form：与QC类似的软件



在画一个图标前，分析图标的构成非常重要，首先将一个画面拆分，思考它用到了哪些元素、哪些工具和操作技巧后，再使用Sketch将其画出。