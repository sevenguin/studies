## 概念类的东西

机器学习：Tom Mitchell（1998）-对于一个计算机程序来说，给他一个任务T，一个性能测量方法P，如果在经验E的影响下，P对T的测量结果得到了改进，那么就说该程序从E中学习。

监督学习（Supervised Learing）:如分类，回归问题。

学习理论（Learn Theory）：how、why算法是有效的

无监督学习（Unsupervised Learing）：如聚类问题

加强学习（Reinforcement Learing）：一些列决策来做决定

### 监督学习应用，梯度下降

得到一个训练集—>提供给学习算法—>生成一个输出函数（函数接收输入，输出估计值）

梯度下降算法有时候会依赖初值的选定。

批量梯度下降（batch gradient descent：每次梯度迭代都需要遍历所有数据来计算，$\theta_i = \theta_i -\lambda \sum_{j=1}^n(h_\theta(x^{i})-y^i)\cdot x^i$

随机梯度下降（或增量梯度下降-incremental gradient descent）：每一次迭代只使用m个数据，$\theta_i=\theta_i-\lambda(h_\theta(x^{(j)})-y^{(j)})\cdot x^j_i，j取1到m，每一个取值j，都计算所有的i值$

最小二乘法两种解决方法，一种是向量正交，一种是根据迹的运算公式来证明。

梯度下降法更新每个参数时需要：Simultaneous update：

__correct__：

temp0 = $\theta_0$ - $\alpha{\delta\over\delta\theta_0}J(\theta_0, \theta_1)$;temp1 = $\theta_1$ - $\alpha{\delta\over\delta\theta_1}J(\theta_0, \theta_1)$

$\theta_0 = temp0$;$\theta_1=temp_1$

__incorrect__：

temp0 = $\theta_0$  - $\alpha{\delta\over\delta\theta_0}J(\theta_0, \theta_1)$;$\theta_0 = temp0$

$temp1 = \theta_1 - \alpha{\delta\over\delta\theta_1}J(\theta_0, \theta_1)$;$\theta_1=temp_1$

先同一计算然后赋值，否则第二种在计算$\theta_1$的值时，$\theta_0$的值已经是下个迭代中的值了。

梯度下降算法，在靠近最小值时，偏导数会越来越小，所以在距离局部最小值附近时，更新的幅度也会越来越小。

### 欠拟合与过拟合

将某个特征做一些函数变化（例如取平方），也是一种特征选择手段。某个特征取平方也可以将线性转换成n次模型——$\theta_0 + \theta_1x_1 + \theta_2x_1^2 +… + \theta_nx_1^n$当n太大是就会造成过拟合。

参数学习算法：有固定数目的参数以用来进行数据拟合的算法那，例如线性回归有参数。

非参数学习算法：参数数量会随着m增加的算法（m就是数据的大小）

#### 局部加权回归（LOESS）：

只考虑x固定区域内的数据点，对这个数据子集来进行线性回归，在局部加权回归中，我们要拟合出$\theta$，使得$\sum_iw^{(i)}(y^{(i)}-\theta^Tx^{(i)})^2$最小，其中$w^{(i)}$为权值，权值的取值有很多种方法，例如：$w^{(i)}=e^{-{(x^{(i)}-x)^2\over 2\lambda}}，其中x为需要预测的输入变量，\lambda为带宽$，这个权值可以达到离x近的权值较高（可以根据数据特征，x附近的值变化是否剧烈来选择权值函数的变化率），每一次预测都要重新生成算法，拟合$\theta$。

线性模型的概率解释：对OLS赋予概率意义，对于OLS的目标函数：$y^{(i)}=\theta^Tx^{(i)}+\epsilon^{(i)}，\epsilon^{(i)}$是误差项，可以把误差项看做未建模的特征的补偿（例如购买时机没有考虑到等）。假设这些误差项存在一个概率分布，假设是服从高斯分布$N(0,\sigma^2)$，也就是说给定参数时，$y$也服从高斯分布，即$P(y^{(i)}|x^{(i)};\theta)={1\over \sqrt{2\pi}\sigma}\exp^-{{(y^{(i)}-\theta^Tx^{(i)})^2}\over 2\sigma^2}$。也就是在给定参数和特征的值之后（数据），y是服从高斯分布的随机变量，即：$y^{(i)}|x^{(i)};\theta$~$N(\theta^Tx^{(i)},\sigma^2)$。$\theta$为参数，而不是随机变量，这个要明确一下。另一个假设，不同输入对应的误差项是彼此独立同分布的，$L(\theta)P(y|x;\theta)=\prod_i^mP(y^{(i)}|x^{(i)};\theta)，L(\theta)表示\theta的似然性$，然后使用极大似然估计来估计$\theta$的值（代入高斯分布的分布函数，再求log，得到的式子最大值等价于，之前OLS的$J(\theta)$求最小值。

#### Logistics Regression（classification）

假设$y\in{0,1}(二元)，h_\theta\in[0,1]，我们选择h_\theta(x)=g(\theta^Tx)={1\over 1+ e^{(-\theta^Tx)}}，即g(z)={1\over 1 + e^{-z}}$,sigmoid函数。

概率解释：$P(y|x;\theta)=h_\theta(x)^y(1-h_\theta(x))^{1-y}，L(\theta)=\prod_iP(y^{(i)}|x^{(i)};\theta)=\prod_ih_\theta(x^{(i)})^{y^{(i)}}(1-h_\theta(x)^{(i)})^{(1-y^{(i)})}$。$L_\theta=\sum_{i=1}^m(y^{(i)}-h_\theta(x^{(i)}))x_j^{(i)}，L_\theta就是L(\theta)对\theta求偏导，L(\theta)是对上式求对数的结果函数$。这个偏导就和线性回归很像了，不同的是$h_\theta$不同。

#### 感知器算法（perceptron）

$g(z)=\begin{cases}1&z\ge 0\\0&otherwise\end{cases}，h_\theta(x)=g(\theta^Tx)，L_\theta和上面的Logistics一样，不同之处还是h_\theta(x)不同$

### 牛顿方法

共轭梯度法有两点疑惑，为什么$X_{k+1}$为极小点？为什么$X^*-X_0=a_0S_0+...+a_{n-1}S_{n-1}$?

假设有函数$f(\theta)$，求使$f(\theta)=0$时的$\theta$值，则使用牛顿法可以求选择初始点，然后对该点求导，导数为斜率的线的切线为0时的$\theta$值为下一次迭代的$\theta$值，对于牛顿方法的一次迭代：$\theta^{(t+1)}=\theta^{(t)} - {f(\theta^{(t)})\over f^\prime(\theta^{(t)})}$（这里$\theta$是一维变量）。一般形式（$\theta$为向量）的公式为：$\theta^{(t+1)}=\theta^{(t)}  H^{(-1)-}\nabla_\theta l，\nabla_\theta l为目标函数的梯度，H是一个Hessian矩阵，其中元素H_{ij}={\delta^l\over\delta\theta_i\delta\theta_j}$

牛顿算法的优点就是迭代速度会比梯度下降法快，但是每次迭代都需要计算Hessian矩阵，会耗费很大。

无论是一般线性回归（概率解释服从高斯分布），还是logistics的服从伯努利分布，都是属于指数分布族，可以一般的写作：$f(y;\eta)=b(y)*exp(\eta^TT(y)-a(\eta))，其中\eta-分布的自然参数；T(y)-充分统计量（大部分情况下T(y)=y）。$如果给定了a、b和T，则这个公式就定义了一个概率分布的集合。例如：
$$
伯努利分布~B(\phi)，即p(y=1;\phi)=\phi，则f(y;\eta)=\phi^y(1-\phi)^{(1 - y)}=\exp(\log\phi^y(1-\phi)^{(1-y)})\\
=\exp(y\log\phi + (1-y)\log(1-\phi))=\exp(\log{\phi\over 1-\phi}y + \log(1-\phi))\\
对照指数分布族，则\eta=\log{\phi\over 1-\phi}, T(y)=y, a(\eta)=-\log(1-\phi)(其实通过第一个式子求\phi={1\over 1+e^{-\eta}})即logistics分布。
$$
__注意：__统计量T(x)是位置数据分布P参数$\theta$的充分统计量，当且仅当，样本数据X关于统计量T(x)的条件分布，独立于$\theta$，简而言之就是，当且仅当T(x)包含了$\theta$的全部信息。

#### 广义线性模型（generalized linear models）

假设1.$y|x;\theta$服从的分布属于以$\eta$为参数的指数分布族；2.给定x，目标输出是，即目标函数h(x)=E[T(y)|x](期望）；3. 输入特征和$\eta$存在关系：$\eta=\theta^TX$。

例如，对于伯努利分布，$y|x;\theta$~$B(\eta)$，则算法进行一次预测，
$$
h_\theta(x)=E[y|x;\theta]=p(p=1|x;\theta)=\phi={1\over 1 + e^{-\eta}}={1\over 1 + e^{-\theta^TX}}，logistics推导
$$
$g(\eta)=E[y;\eta]={1\over 1+e^{-\eta}}$被称作正则响应函数；$g^-1(\eta)$被称作正则关联函数。

##### 多项式分布(Multional)

广义线性模型一个较复杂的模型，$y\in \{1,2,…, k\}$，设参数是$\phi_1, \phi_2, …, \phi_k，p(y=i)=\phi_i$，因为这些参数都是表示的概率，所以其实有一个是冗余的，$\phi_k=1-(\phi_1 + \phi_2 + …  + \phi_{k-1})$，所以参数应该是$\phi_1, \phi_2, …, \phi_{k-1}$，第一次设置的参数有点over parameter。T(y)是第y个值为1，其他值为0的k-1维向量，T(y=k)则为k-1维0向量。指示函数$I,I\{True\}=1，I\{Flase\}=0$，则T(y)第i个元素值即$T(y)_i=I\{y=i\}$。则多项式分布表示成指数族分布为：
$$
P(y)=\phi_1^{I\{y=1\}}\phi_2^{I\{y=2\}}...\phi_k^{I\{y=k\}}=\phi_1^{T(y)_1}\phi_2^{T(y)_2}...\phi_{k-1}^{T(y)_{k-1}}\phi^{1-\sum_{j=1}^{k-1}T(y)_j}\\
=b(y)*exp(\eta^TT(y)-a(\eta))，
a(\eta)=-log(\phi_k)，b(y)=1, \eta=\begin{vmatrix}\log(\phi_1/\log\phi_k)\\.\\.\\.\\\log(\phi_{k-1}/\log\phi_k)\\\end{vmatrix}\\
\phi_i={e^{\eta_i}\over 1+\sum_{j=1}^{k-1}e^{\eta_j}}，\eta_i=\theta_i^TX\\
学习算法h_\theta(x)=E{T(y)|x;\theta}，\theta是一个n+1* k-1的矩阵，为什么是这种大小的矩阵并没有解释原因
$$
sofmax regression，logistics regression的扩展，由k=2，推广到k>2。

### 生成学习算法

高斯判别分析（Gaussian Discriminant Analysis）

__判别学习算法：__判别学习算法或直接学习算法p(y|x)，学习的到一个假设直接输出0或1，例如logistics。

__生成学习算法：__用来对p(x|y)（一个生成模型对样本特征建立概率模型，在给定样本类别的条件下）、p(y)进行建模，给定所属类的情况，显示某种特定特征的概率，然后通过贝叶斯公式计算p(y|x)。有了这两个之后，就可以很容易计算$p(y=1|x)=p(x|y=1)*p(y=1)/p(x)，p(x)=p(x|y=1)*p(y=1) + p(x|y=0)*p(y=0)$。

#### 高斯判别分析算法

Gaussian discrimnant analysis algorithm.

高斯判别分析算法有一个前提条件——假设$x\in IR^n$，并且是连续的。

高斯判别分析算法的核心假设是p(x|y)满足高斯分布（多元高斯分布），设y服从伯努利分布，$p(y)=\phi^y(1-\phi)^{1-y}，p(x|y=0)={1\over 2\pi^{-1/2}|\Sigma|^2}exp({-{1\over2}(x - \mu_0)^T\Sigma^{-{1}}(x-\mu_0)}),\\p(x|y=1)={1\over 2\pi^{-1/2}|\Sigma|^2}exp({-{1\over2}(x - \mu_1)^T\Sigma^{-{1}}(x-\mu_1)})$。

可以使用最大似然估计来对参数进行估计，$l(\phi,\mu_0,\mu_1,\Sigma)=\log\prod_{i=1}^mp(x^{(i)}, y^{(i)})=\log\prod_{i=1}^mp(x^{(i)}|y^{(i)})*p(y^{(i)})$。——__joint likelihood__

（30分之前的一个argmin公式）

对p(x)的建模：$p(x|y=0)p(y=0)+p(x|y=1)p(y=1)$

__多元高斯分布__：若p维随机向量$\textbf X = (X_1, X_2, …, X_p)$的密度函数为：
$$
f(x_1, ..., x_p) = {1\over\sqrt{(2\pi)^p}|\Sigma|^{1/2}}\exp(-{1\over 2}(x-\mu)^T\Sigma^{-1}(x-\mu))
$$
其中，$x=(x_1, …, x_p),\mu$，是p维向量，$\Sigma$是p阶正定矩阵（协方差矩阵），则称X服从p维正态分布，记为$\textbf X\sim N_p(\mu, \Sigma)$。

$p(x|y)$服从高斯分布，拟合出$p(x|y=1)$和$p(x|y=0)$，得到的可以作为分类器使用。

高斯判别分析和logistics回归有一些关系，高斯分布得到的p(y=1|x)的曲线和logistics有点像。（最好实际上能将这两个算法实现，而且画出他们的轨迹图）。

高斯判别分析假设x|y服从高斯分布，其能推导出p(y=1|x)的分布是logistics，但是反过来是不成立的。

假设x|y=1服从泊松分布$(\lambda_1)$，x|y=0服从泊松分布$(\lambda_0)$，则p(y=1|x)分布图形就是logistic。

假设x|y=1服从指数分布族，参数为$\lambda_1$，x|y=0服从指数分布族，参数为$\lambda_0$，则p(y=1|x)是一个logistics函数。

*了解各种统计数据符合的各个分布情况，则有利于选择模型*

logistics是一个模型选择上鲁棒性很好的模型，因为数据服从很多的分布时，都能拟合出logistics的模型。但是如果明确知道数据的分布情况，则使用特定的模型拟合会好于logistics。

因为高斯判别分析是基于更强的假设：x|y服从高斯分布，所以如果已知数据x|y是服从高斯分布，则其分类效果强于logistics，反之，如果不确定其分布，logistics会更优 。使用生成学习算法的真正的好处通常在于它需要更少的数据。

#### 朴素贝叶斯算法

第二个生成学习算法

假设给定y，$x_i$之间是独立的，即：$p(x_1, x_2, …, x_n|y)=p(x_1|y)*p(x_2|y)…p(x_n|y)=\prod_{i=1}^np(x_i|y)$。

__Laplace平滑__:在计算概率时，分子和分布都加上1，这样避免概率可能为0的情况。

要再对着讲义看一遍，梳理+复习+修复笔记。

朴素贝叶斯分类也可以很简单的理解成贝叶斯计算公式，但是如何将生成算法的整个数学公式串联起很重要，培养这种分析和学习理解方法，对于以后扩展、选择算法模型都很重要。

### 朴素贝叶斯算法

多项式事件模型（Multinomial Event Model）

设有字典D，邮件中包含的词有$n_i$个，则使用向量$v=<x_1^{(i)}, x_2^{(i)},…, x_{n_i}^{(i)}>$表示邮件中的所有出现的词，$x_j^{i}$表示的是D中的索引值，指向D中的某个词。

有参数$\phi_{k|y=1}=p(x_j=k|y=1)，\phi_{k|y=0}=p(x_j=k|y=0)，\phi_y=p(y=1)$第一个式子表示当发送垃圾邮件时包含词k时的概率，后面依理类推。给定训练参数，则可以求得这些参数的极大似然估计。

Vector:An n*1 matrix, n row, 1 columns.



3-5





