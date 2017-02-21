# 机器学习

斯坦福大学课程

_"A computer program is said to learn from experience E with respect to some task T and some performance measure P, if its performance on T, as measured by P, improves with experience E."_

机器学习算法：

* 监督学习:按照已经有标签的样例数据将未标签的数据进行标签
* 非监督学习：发现数据的结构特点，例如聚类中发现两个类别数据
* others：增强学习、推荐系统

机器学习和AI中的实践经验，介绍在何时更好的使用它们。

非监督学习（大概只是聚类）的应用：

* 组织机器集群：找到哪些机器更倾向于协同，然后将这些及其放在一起
* 社交网络：寻找不同关系的用户群体
* 市场细分：（可能事先不知道有哪些细分市场）将客户根据客户的行为等信息，细分客户群体，有助于市场运营
* 天文数据分析

### Linear regression with one variable

#### Model Representation

$h_\theta(x)=\theta_0 + \theta_1x_1$（因为是单变量，所以这里就是1）

线性模型只是开始

#### Cost function

这个函数可以帮助我们计算出如何能最好的拟合数据。虽然损失函数很多，但是线性回归可能最常用的就是平方误差代价函数。代价函数的数学定义（平方根误差）：
$$
J(\theta_0,\theta_1)={1\over 2m}\sum_{i=1}^m(h_{\theta_0,\theta_1}(x^{i}) - y^{(i)})
$$
$J(\theta_0, \theta_1)$被称为代价函数（损失函数）。

注意：假设函数$h_\theta(x)$是对x的函数，而代价函数$J(\theta)$是对$\theta$的函数。

机器学习的目标就是选择$\theta$值，最大限度地减少$J(\theta)$

contour plot(等高线)(或许复习一下微积分中等高线的数学内容)

#### Gradient desent



Q:

支持向量积是如何处理无数个特征的?