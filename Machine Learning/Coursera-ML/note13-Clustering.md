## Clustering

### Unsupervised Learning

和之前介绍的算法不同，这类算法是非监督，即学习前不知道分类标签。

#### Application of clustering

* Market segmentation：市场分割，将客户分成不同的客户群，这样可以对不同类型的客户分别营销，或者分别提供更适合的服务
* Social network analysis：用户分群
* Organize computing clusters
* 天文数据分析


### K-Means

有以下几个步骤：

* 随机选择k个点（k是设定的分类数量）
* 簇分配：每个点距离这k个点中某个最近，则将这个点分配到这个点中，设定为一类
* 重新计算中心点
* 迭代

初始的K个中心值，一般先随机赋予初值。

算法步骤：

```python
repeat
    for i in range(m):    # m is the number of the samples
        c[i] is the index of the cluster(1,2,...K) to which example x[i] is currently assigend
    for k in range(K):
        u[k] is cluster centroid of the cluster k
```

  ### Optimization Objective

假设$\mu_c^{(i)}$是$x^{(i)}$的cluster的中心（cluster centroid），所以优化目标可以为：
$$
J(c^{(1)},..., c^{(m)}, \mu_1,...,\mu_K) = {1\over m}\sum_{i=1}^m||x^{(i)} - \mu_c^{(i)}||^2\\
\min_{c,\mu} J
$$
上面算法中每次迭代中的两步都是在逐渐的减小优化目标。

### Randomly initialize，如何避免局部最优

首先$K\lt m$，然后随机选择K个训练样本，然后设置$\mu_1,..,\mu_K$等于这$K$个样本。

由于是随机产生的$K$个点，可能会有一部分点落在本身属于同一个Cluster的簇中，所以最终可能产生局部最优值。

解决方法就是进行多次计算，选择100次随机初始值进行拟合，最后选择最优的结果（J最小的结果），实践证明，在$2\le K\le10$时，多次计算会有一个较好的结果。

### Choosing the Number of Clusters

一般可以通过可视化来人为的选择（当然是2D数据，或者可转换成2D）

Elbow method（肘部法则）：逐步增大K，然后求出针对每个K的最优情况下的J值，然后绘制成K和J的图，可以选择J突变时的k作为结果。但是这个方法不是很通用，因为有些情况k的变化是平缓的。

另一种方法，就是根据聚类的目的来评判。一般使用聚类肯定有一个目的，或是为了市场细分，或是为了客户分类，可以根据各种K值分类的结果对后续目标的影响来判断最优的K值。



