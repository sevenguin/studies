# Spline和Interpolation

## Spline

Spline是一个使用多项式函数进行分段定义的数值函数，这些函数在每一段多项式函数交接地方能够高度平滑，这些交接处称为_knots_。

最常用的样条（Splines）有cubic splines（三次样条）。三阶，立方B-spline。

一个简单的cubic splines：$S(t) = |t|^3$，$S^\prime(0)=0，S^{\prime\prime}(0) = 0$。

Spline的degree就是样条函数的最高幂次，cubic splines的degree=3。degree<k，k为knots个数。

#### B-Spline [wiki](http://mathworld.wolfram.com/B-Spline.html)

B-Spline是basis spline的缩写，是 [Bézier curve](http://mathworld.wolfram.com/BezierCurve.html)的泛化，假设我们有点：$\textbf T = \lbrace t_0, t_1, ..., t_m\rbrace$，$\textbf T$是非减序列，且$t_i\in[0, 1]$，定义控制点$\textbf P_0, ..., \textbf P_n$，定义级数为：$p = m - n - 1$，$t_{p+1}, ..., t_{m-p-1}$的 knots叫做内部knots（internal knots）。

定义基本的函数：
$$
C(t)=\sum_{i=0}^n \textbf P_i N_{i,p}(t)\\
N_{i,0}(t)=\begin {cases}1\ \ ， t_i\le t\le t_{i+1})\\ 0\ \ ，otherwise \end{cases}\\
N_{i,j}(t) = {t - t_i\over t_{i+j} - t_i}N_{i, j-1}(t) + {t_{i+j+1}  - t\over t_{i+j+1} - t_{i+1}}N_{i+1, j-1}(t)
$$
$C(t)$是B-spline曲线，$N_{i,k}(t)$是B-Spline基函数。cubic是p=3，控制点作为输入计算。

## Interpolation [wiki](https://en.wikipedia.org/wiki/Interpolation)

在数学领域内，interpretation是一个构造新数据点的方法，构造的点在一定的范围内或在一个离散数据集中。

在工程和科学领域内，经常会通过抽样或试验获得一些数据点，这些数据点表示了一个有限个数的独立变量组成的函数(f)的值，例如：$y=\sum_i h_i(x)，x是多个变量向量$，经常需要根据这些自变量的中间计算出的函数(f)值。一般可以通过回归分析和曲线拟合来求得。

通过简单的函数来近似复杂的函数也是内插（interpolation）的一个关键话题，假设给定的已知函数虽然很有效，但是很复杂。一些来自原始函数的数据点，可以通过一些简单的函数来构建内插。当然这时候肯定会产生一定的误差（interpolation errors），但是根据问题的领域（不同领域可能容错不同），获得简便性的好处可能大于精确度不足的损失。

假设有如下数据，求x=2.5时的插值：

| x    | f(x)    |
| ---- | ------- |
| 0    | 0       |
| 1    | 0.8415  |
| 2    | 0.9093  |
| 3    | 0.1411  |
| 4    | -0.7566 |
| 5    | -0.9589 |
| 6    | -0.2794 |

散点图：

![图](https://upload.wikimedia.org/wikipedia/commons/7/71/Interpolation_Data.svg)

几个插值方法：

#### 分段常量插值（Piecewise constant interpolation）

Nearest-nighbor interpolation，最简单的方法就是返回最靠近各个变量中间值的某个数据点的值。例如：$x=1.1$时，插值应该是取最近点$x=1$时的值$0.8415$。

#### 线性插值（Linear interpolation）

也称为$lerp$，另一个简单的方法，例如上面的$x=2.5$，这个利用上面的方法就搞不定，距离$x=2$和$x=3$距离相等，一个合理的处理方法是：取中间值：
$$
y=y_a + (y_b - y_a){x - x_a\over x_b - x_a}，在(x,y)点，x已知，求y。
$$
__优缺点__:线性插值比较快，而且简单，但是精确度不够，更关键的是在$x_k$点不可微。

#### 多项式插值（Polynomial interpolation）

多项式插值是线性插值的一个泛化的概念，我们使用更高级的多项式来替换这个插值，而不是线性的处理。

给定$n+1$个点$(x_i, y_i)$，可以找到一个最多$n$维的多项式$p$，有：
$$
p(x_i) = y_i,\  i=0, ..., n\\
p(x) = a_nx^n + a_{n-1}x^{n-1} + ... + a_2x^2 + a_1x + a_0
$$
存在$p$且唯一，证明参见：[Vandermonde matrix](https://en.wikipedia.org/wiki/Vandermonde_matrix)，关键就是求$a_i, i = 0, .., n$。

另一种表现形式是拉格朗日多项式（Lagrange polynomials）：
$$
p(x) = {(x-x_1)(x-x_2)...(x-x_n)\over(x_0 - x_1)(x_0-x_2)...(x_0-x_n)}y_0 + ... + {(x-x_1)(x-x_2)...(x-x_n)\over(x_n - x_1)(x_n-x_2)...(x_n-x_n)}y_n=\sum_{i=0}^n(\prod_{0\le j\le n,j\ne i}{x-x_i\over x_i - x_j})y_i
$$
__优缺点__:多项式插值可以解决上面线性插值的问题，但是也有一些缺点，计算复杂度太大，多项式插值可能会产生震荡问题（特别是终点，[[Runge's phenomenon](https://en.wikipedia.org/wiki/Runge%27s_phenomenon)]

> __Runge's phenomenon__
>
> 在数值分析的数学领域中，Runge现象是当在一组等间隔内差点上使用高幂次多项式来进行多项式内插时，在间隔边缘处出现的震荡问题。

#### 样条插值（Spline interpolation）

样条插值，在每个间隔中使用低级的多项式（low-degree），而且选择多项式片段使得他们之间能够平滑的连接起来。产生的函数称为样条（Spline）。

需要spline的形状弯曲度最小，而且在knots点连续，需要满足：
$$
q^\prime_i(x_i) = q_{i+1}^\prime(x_{i+1})；q_i^{\prime\prime} = q_{i+1}^{\prime\prime}(x_i) ,\   1\le i\le n-1
$$
$q_i$是第$i$个分段内的样条函数。所以样条插值多项式最高幂次应该大于等于3.

样条插值有时候都优于多项式插值，因为插值误差可以甚至更小。

__优缺点__：比线性插值误差更小，而且插值更平滑，而且比高级多项式更容易计算，而且没有Runge's phenomenon。

计算三次样条插值的算法：[Spline interpolation](Algorithm to find the interpolating cubic spline)

#### 其他方法

高斯方法：[Gaussian process](https://en.wikipedia.org/wiki/Gaussian_process)，[Kriging](https://en.wikipedia.org/wiki/Kriging).



