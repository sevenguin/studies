## 正则化

### Overfitting

后面会讲到调试和诊断导致学习算法故障的东西，会介绍如何用专门的工具来识别过拟合，和可能发生的欠拟合。

对于一维和二维数据，可以通过绘出假设模型的图像来研究问题所在，然后选择合适多项式来拟合数据；但是这种方法对特征比较多的情况就很无力了。所以一般有两种方法解决：

* 减少特征数（缺点是：舍掉特征也就舍掉了一些信息）
  * 人工选择哪些特征最好，保留这些好的，丢掉不好的
  * 模型自动选择采用哪些特征
* 正则化
  * 保留所有特征，但是调整（减少）他们的参数($\theta_j$)
  * 在拥有很多特征时也能运行良好，每一个特征都能对于预测值做出一点影响

### Cost Function

正则化后的损失函数：
$$
J(\theta) = {1\over 2m}[\sum_{i=1}^m(h_\theta(x^{(i)}) - y^{(i)})^2 + \lambda\sum_{j=1}^m\theta_j^2]
$$
但是需要注意的是$\lambda$需要选择合适的值，否则会出现欠拟合的情况，例如$\lambda$的值很大，则容易造成各个$\theta$的值为0.（注意后面正则项中，从$j=1$开始，$\theta_0$并没有参与正则化。

后面会介绍一系列自动选择参数的方法。

### 线性回归的正则化

线性回归有两种算法，一种是梯度下降，一种是正规方程（normal equation），分别介绍两种算法的正则化.

#### 梯度下降方法

对上线的Cost Function使用梯度下降方法计算参数，有：
$$
repeat\{\\
    \theta_0 = \theta_0 - \alpha{1\over m}\sum_{i=1}^m(h_\theta(x^i) - y^i)x_0^i\\
    \theta_j = \theta_0 - \alpha[{1\over m}\sum_{i=1}^m(h_\theta(x^i) - y^i)x_j^i + {\lambda\over m}\theta_j]
  \\
\}
$$
将第一个参数分离开是因为正则计算里面不对他进行正则化。

#### 正规方程

正则方法：
$$
\theta = (X^TX + \lambda M)^{-1}X^Ty
$$
M是一个除了第一个元素为0外，对角线上所有元素为1的，其他元素都为0的(n+1)*(n+1)的矩阵。如果使用带有正则项的Cost Function仍然可以达到全局最优。

### Logistics回归正则化

对于Cost Function：
$$
repeat\{\\
    \theta_0 = \theta_0 - \alpha{1\over m}\sum_{i=1}^m(h_\theta(x^i) - y^i)x_0^i\\
    \theta_j = \theta_0 - \alpha[{1\over m}\sum_{i=1}^m(h_\theta(x^i) - y^i)x_j^i + {\lambda\over m}\theta_j],(j=1,2,3...,n)
  \\
\}
$$
虽然式子和上面的线性回归很相似，但是这里的$h_\theta$是不同的，这里的$h_\theta={1\over 1+e^{-\theta^Tx}}$

