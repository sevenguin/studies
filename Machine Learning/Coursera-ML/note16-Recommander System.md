## Recommander System

### Problem Formulation

假设问题是基于对电影评分模式进行推荐系统设计

notation：$n_u$,用户数，$n_m$电影数，$r(i,j)$如果一个用户j对电影i进行了评分，则此值为1，$y^{(i,j)}$如果$r(i,j)$为1，则此值为用户j对电影i的评分。

对$r(i,j)\ne1$的元素，预测$y^{(i,j)}$值。

### Content  Based Recommendations

假设电影有n个特征描述其内容，特征的值是和这个特征的相关性（例如：动作片、爱情片）。

然后可以对每一个用户j，学习参数$\theta^{(j)}(维度是n+1的向量)$，预测用户j对电影i的评分为：$(\theta^{(j)})^Tx^{(i)}$

这里的$x^{(i)}$是第i个电影n个特征值的值(还包括了$x_0=1$)

$r(i,j)$=1 if user j has rated movie j(0 otherwise)

$y^{(i,j)}$=rating by user j on movie i

$\theta^{(j)}$=parameter vector for user j

$x^{(i)}$=feature vector for movie i

for user j, movie i predicted rating:$(\theta^{(j)})^T(x^{(i)})$

$m^{(j)}$=no. of movies rated by user j, to lean $\theta^{(j)}$:
$$
\min_{\theta^{(j)}}{1\over 2}\sum_{i:r(i,j)=1}((\theta^{(j)})^Tx^{(i)}-y^{(i,j)})^2 + {\lambda\over 2}\sum_{k=1}^n(\theta_k^{(j)})^2
$$
对于有$n_u$个用户来说，优化目标为：
$$
J(\theta^{(1)},...,\theta^{(n_u)})=\min_{\theta^{(1)},\theta^{(2)},...,\theta^{(n_u)}}{1\over 2}\sum_{j=1}^{n_u}\sum_{i:r(i,j)=1}((\theta^{(j)})^Tx^{(i)}-y^{(i,j)})^2 + {\lambda\over 2}\sum_{j=1}^{n_u}\sum_{k=1}^n(\theta_k^{(j)})^2
$$
梯度更新：
$$
\theta_k^{(j)} := \theta_k^{(j)} - \alpha\sum_{i:r(i,j)=1}((\theta^{(j)})^Tx^{(i)}-y^{(i,j)})x_k^{(i)}(for\ k = 0)\\
\theta_k^{(j)} := \theta_k^{(j)} - \alpha(\sum_{i:r(i,j)=1}((\theta^{(j)})^Tx^{(i)}-y^{(i,j)})x_k^{(i)} + \lambda\theta_k^{(j)})(for\ k \ne 0)
$$
注意正则化项只是$k\ne0$时处理。

但是如果内容特征不好获取，则此方法可能就不好办。

### 协同过滤算法

可以自行学习所要使用的特征。

给定$\theta^{(1)},\theta^{(2)},…,\theta^{(n_u)}$来学习$x^{(1)},x^{(2)},x^{(1)},…,x^{(n_m)}$，学习目标如下：
$$
J(x^{(1)},...,x^{(n_m)})=\min_{x^{(1)},x^{(2)},...,x^{(n_m)}}{1\over 2}\sum_{i=1}^{n_m}\sum_{j:r(i,j)=1}((\theta^{(j)})^Tx^{(i)}-y^{(i,j)})^2 + {\lambda\over 2}\sum_{i=1}^{n_m}\sum_{k=1}^n(\theta_k^{(j)})^2
$$
$n_u$ no. of the users;$n_m$ no. of the movies.

基于内容过滤是给定$x$来估计$\theta$，而协同过滤是给定$\theta$，估计$x$，所以可以先随机猜测一个$\theta$，然后求出$x$，然后根据求出的$x$，再计算$\theta$，不断迭代，直到算法收敛到一好的结果。

### Collaboration Filtering algorithm

合并上面两个公式：
$$
J(x^{(1)},...,x^{(n_m)},\theta^{(1)},...,\theta^{(n_u)})=\min_{x^{(1)},x^{(2)},...,x^{(n_m)},\theta^{(1)},...,\theta^{(n_u)}}{1\over 2}\sum_{i,j:r(i,j)=1}((\theta^{(j)})^Tx^{(i)}-y^{(i,j)})^2 \\+ {\lambda\over 2}\sum_{i=1}^{n_m}\sum_{k=1}^n(\theta_k^{(j)})^2+ {\lambda\over 2}\sum{j=1}^{n_u}\sum_{k=1}^n(\theta_k^{(j)})^2			
$$
算法步骤：

1. 初始化$x,\theta$一个小的随机值
2. 最小化$J(x,\theta)$
3. 对于一个用户的参数$\theta$，和电影的特征向量$x$，得到评分$\theta^Tx$

可以通过计算两个movie的特征向量（x）的距离最小来判断其两者的关联性。

#### 均值

对于新用户（没有过评分操作），对这种用户对Item的评分，可以取值这个Item所有评分的均值。