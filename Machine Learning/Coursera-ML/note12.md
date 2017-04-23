## Support Vector Machine

### Optimization Objective

相比Logistic regression的优化目标：
$$
\min_\theta{1\over m}[\sum_{m=1}^my^{(i)}(-\log h_\theta(x^{(i)})) + (1-y^{(i)})(-\log(1-h_\theta(x^{(i)})))] + {\lambda\over 2m}\sum_{j=1}^n\theta_j^2\\
s.t. \ \ y=1时，\theta^Tx\ge 0\\
\ \ \ \ \ \ y=0时，\theta^t\lt 0
$$
支持向量积的优化目标（相当于给上式乘以$m\over\lambda$，可以把C理解成$1\over\lambda$，因为这些是常量，对优化目标的结果不构成影响：
$$
\min_\theta C\sum_{i=1}^m[y^{(i)}cost_1(\theta^Tx^{(i)}) + (1-y^{(i)})cost_0(\theta^Tx^{(i)})] + {1\over2}\sum_{i=1}^n\theta_j^2\\
\ \ s.t. y=1时，\theta^Tx \ge 1\\
\ \ \ \ \ \ y=0时，\theta^Tx\le -1
$$
对比Logistic Regression和SVM的两个要求，SVM的要求更加严格，需要当$|\theta^Tx|\ge1$时才确定分类结果，所以SVM的分类效果会好于LR。而且需要注意的一点是，正是$|\theta^Tx|\ge1$这个条件，表现出了对最大间隔的诉求。

### Large Margin Intuition(最大间隔)

根据上面的表达式，当C取很大值时，只有当C后面的乘数为0时（或者尽量趋近与0时），整个优化目标才能取最小值，而最优化问题就变成了：
$$
\min_\theta{1\over 2}\sum_{j=1}^n\theta_j^2,\\
s.t.\ \ p^{(i)}\times||\theta||\ge 1, \ if\ y^{(i)}=1\\
\ \ \ \ \ \ p^{(i)}\times||\theta||\le -1, \ if\ y^{(i)} = 1
$$
这里的$y^{(i)}$是$x^{(i)}$向量在参数$\theta$向量上的投影长度（由于$\theta$向量和最大分割的超平面（$\theta$为参数的线性超平面）垂直，所以到$\theta$向量上的投影长度，其实就是$x^{(i)}$向量距离超平面的距离），因为需要满足两个不等式，所以只有在$p^{(i)}$足够大时，$\theta$的值才能足够小，才能满足表达式的优化目标。所以上面的式子就体现了最大间隔的优化目标。

但是上面的条件有个限制，就是对线性可分是适合的，如果线性不可分，则条件不能满足。而且出现异常点，很容易让SVM的超平面变得过拟合（即便异常点线性可分）。以上两个问题，可以通过降低C的值来做到（回想一下，C其实就是正则化项参数值的导数，降低C值其实就是提高正则化项值，所以就相当于降低拟合的正则化）。上面将C值推向最大，是为了直观的理解SVM最大间隔的计算推理。后面需要注意理解下C如果不是足够大时，SVM的处理方式。

### 核函数

核：给定输入$x$，计算一些新的特征$f_1,f_2...$，这些新特征依赖于相似性度量的标签如：$l^{(1)},l^{(2)},l^{(3)}.etc$.

如：
$$
给定x，有f_i=similarity(x, l^{(i)}) = \exp{(-{||x-l^{(i)}||^2\over 2\sigma^2})}
$$
这里的similarity函数术语上就称作核函数。而上式使用的就是高斯核函数，因为后面相似度就是使用高斯核函数。一般表示为$k(x,l^{(l)})$，需要注意这里的$x,l^{(i)}$都是向量。

如果$l^{(i)}\approx x$，则$f_i\approx $1，反之，则$f_i\approx 0$.

给定k个标记点$l$，就会得到k个新的特征$f$。

但是如何选择这些标记点，其他相似方程如何？能否替换了这个高斯核函数。

#### SVM with Kernels

如何选定标记点？可以在训练样本、交叉验证样本中选择已有的样本数据点为标记点。

给定$(x^{(1)},y^{(1)}), (x^{(2)},y^{(2)}),…, (x^{(m)},y^{(m)})$，

选择$l^{(1)} = x^{(1)}, l^{(2)} = x^{(2)},…,l^{(m)} = x^{(m)}$，

给定样本数据$x$:
$$
f_1 = similarity(x, l^{li})
$$
对于训练样本$(x^{(i)}, y^{(i)})$，对$x^{(i)}$进行转换：
$$
f^{(i)}_1 = sim(x^{i}, l^{(1)})\\
f^{(i)}_2 = sim(x^{i}, l^{(2)})\\
...\\
f^{(i)}_m = sim(x^{i}, l^{(m)})
$$
SVM parameters:

$C(={1\over \lambda})$:Large C: Lower bias, high variance;

​               Small C: Higher bias, low variance.

$\sigma^2$: Large $\sigma^2$, features $f_i$的变化会随着距离标注点l的距离变大而更平滑的变动。并且Highter bias, lower variance;

 Small $\sigma^2$, features $f_i$的变化会随着距离标注点l的距离变大而更剧烈的变动。并且Lower  bias, Higher variance。

因为核函数的缘故，优化目标会变为：
$$
\min_\theta C\sum_{i=1}^m[y^{(i)}cost_1(\theta^Tf^{(i)}) + (1-y^{(i)})cost_0(\theta^Tf^{(i)})] + {1\over2}\sum_{i=1}^n\theta_j^2\\
\ \ s.t. y=1时，\theta^Tx \ge 1\\
\ \ \ \ \ \ y=0时，\theta^Tx\le -1
$$
如果标注方式是按照上面的方式进行，则有m个数量的样本，则标注m个，则获得m个f，则最后模型参数$\theta$也将有m个（不对$\theta_0$做正则化）。因为最终模型为：

$h = \theta_0 + \theta_1\times f_1+\theta_2\times f_2 + … + \theta_m\times f_m$