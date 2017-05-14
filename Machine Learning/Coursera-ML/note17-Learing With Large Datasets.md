## Learing With Large Datasets

是否决定使用更大的数据集，需要结合学习曲线来判断（根据算法现在是高偏差还是高方差）。

### stochastic  gradient descent

批量梯度下降（batch gradient descent）在你数据量大时计算会很耗时。

#### Batch Gradient Descent

$$
Repeat\{\theta_j := \theta_j - \alpha{1\over m}\sum_{i=1}^m {\delta \over\theta_j}J_{train}(\theta)\}
$$

#### Stochastic Gradient Descent

随机梯度算法：

1. 打乱数据（randomly shuffle dataset）
2. repeat $\{for i 1,…,m{\theta_j:=\theta_j-\alpha(h_\theta(x^{(i)})-y^{(i)})}x_j^{(i)}\}$

如果数据量足够大，随机梯度算法可能只需要一次迭代（repeat），即可得到最优值。

### Mini-batch gradient descent

介于批量和随机梯度下降，mini-batch每一次迭代使用b个样本数来进行梯度计算。即将批量算法中的m替换为b（当然i的范围是`np.arange(1, n, b)`)

在向量化计算时，mini-batch效率会更好。

b值可以通过CV来进行确定。

### Stochastic Gradient Descent Convergence

如何在学习过程中保证它能收敛并且如何选择学习速率$\alpha$?

在随机梯度下降算法计算时，在使用某个样本更新$\theta$之前，先计算出这个假设对这个训练样本的表现即计算cost函数值。

例如：在每100次迭代运算中，我们对最后100个样本的cost值求平均值，然后画出图，看cost的走向。同样可以根据这个图来判断学习速率是否合适（太大或太小）。

可以让学习速率是一个变量，根据迭代次数进行反向变化（$\alpha={const1\over iteraionNumber + const2}$)

### Online Learning

从在线数据流中学习，得到对决策有用的信息。

像随机梯度计算一样，实时获得用户的数据，使用这个数据更新参数（例如随机梯度计算，使用一个样例数据更新参数）

CTR的计算

### Map-reduce and data parallelism

像批量梯度计算中，求和像可以将数据集分为C（cluster规模）份，每个集群机器处理$1\over C$的数据求和。

所以先要判断算法是否是例如求和等可并行计算的算子进行计算，从而决定是否进行多台机器并行计算处理。

通过将算法表示为数据集计算求和或者函数计算求和的形式来进行并行化。