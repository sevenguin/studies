### 二重积分

Double integrals

和单变量积分相同，f(x,y)dA，dA是面积，乘以函数值f(x,y)就是分割的小体积的值，求总和就是整个积分的值了。定义为：$\int\int_R f(x,y)dA$

把二重积分转换成两个独立变量的单变量来计算积分。

一般先对x或先对y积分都没有关系，但是一般考虑到函数图形的特别性，可能对某一个先积分会使问题更简单。

例如求积分：$\int_0^1\int_x^\sqrt x {e^y\over y}dydx$?

解答，如果直接先对y进行积分计算，则很难算出中间函数的积分，如果换一下x,y的积分顺序则会很容易，观察x,y作用域，则积分的区域是$y=x$，和$y=\sqrt x$两个函数夹在中间的区域面积，x取值为0~1，则转换一下为y取值为$0\to1$，x取值为$y^2\to y$，即式子为$\int_0^1\int_{y^2}^y {e^y\over y}dxdy$。

### 极坐标的二重积分，应用

有一点需要注意：$dA=rdrd\theta$，而不是$drd\theta$。

二重积分的应用：

1. 给定区域R的面积，Area(A)是f(x,y)=1上求二重积分：$\int \int dxdy$，但是x,y的取值范围需要注意，两个变量可能非独立；
2. 区域上一些数量的平均值，在区域r上求函数f的均值，$f的均值=\overline f={1\over Area(A)}\int\int_RfdA$

### 变量的变化

在二重积分使用变量替换——$\int\int$

例如：椭圆$x^2/a^2+y^2/b^2=1，求椭圆面积=\int\int_{x^2/a^2+y^2/b^2<1}dxdy。设u=x/a,v=y/b，则\\dxdy=abdudv，则面积为ab\int\int_{u^2+v^2<1}dudv=ab\pi$

雅克比矩阵

设$u=u(x,y),v=v(x,y)；则转换dudv=|u_x u_y;v_x v_y|dxdy$，雅克比矩阵即：
$$
J={\delta(u,v)\over\delta(x,y)}= \begin{vmatrix}u_x&u_y\\v_x&v_y  \end{vmatrix}，J是这个矩阵的行列式，即一个数值
$$
dudv=|J|dxdy，这里是绝对值的意思，因为J本身已经是行列式的值了。

29min