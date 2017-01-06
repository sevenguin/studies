# Gradient boosting

Gradient boosting是机器学习中，用来解决回归或分类问题的技术，也属于一种集成学习算法，通过集成多个弱预测模型来产生一个新的较好的预测模型。一般这些弱模型为决策树。

在许多监督学习的机器学习算法中，对于数据集$\{(x_1,y_1),...,(x_n, y_n)\}$，寻找接近真值$y_i$的近似函数$\hat F(x)$，这个函数一般会大到损失函数$L(y, F(x))$的期望的最小值，即：
$$
\hat F=arg\min_F \mathbb E_{x,y}[L(y, F(x))]
$$
Gradient boosting方法是假设寻找的最优模型$\hat F(x)$是一些列函数$h_i(x)$的加权和，而$h_i(x)$是基础学习模型（即弱模型），假设基础学习模型集合为$\mathcal H$。
$$
F(x)=\sum_{i=1}^M \gamma_ih_i(x) + const
$$
基于上面的假设，起始模型记为$F_0(x)$，则整个模型描述如下：
$$
F_0(x) = arg\min_\gamma\sum_{i=1}^nL(y_i, \gamma)\\
F_m(x) = F_{m-1}(x) + arg\min_{f\in\mathcal H}\sum_{i=1}^n L(y_i, F_{m-1}(x_i) + f(x_i))=F_{m-1}(x)-\gamma_m\sum_{i=1}^n\nabla_{F_{m-1}}L(y_i,F_{m-1}(x_i))
$$
其中：$\gamma_m=arg\min_\gamma\sum_{i=1}^nL(y_i, F_{m-1}(x_i) - \gamma{\partial L(y_i, F_{m-1}(x_i))\over\partial F_{m-1}(x_i)})$。



参考：https://en.wikipedia.org/wiki/Gradient_boosting#Gradient_tree_boosting