## 监督学习概论

### 最小二乘法和最近邻法

线性模型对数据结构和输出稳定性做了很多的假设，但是可能产生不精确的预测；knn对结构做了很少的假设：它的预测经常比较精确，但是不稳定。

#### 线性模型和最小二乘法

线性模型：假设有输入$X^T=(X_1, X_2, ..., X_p)（列矩阵，p为列数）$，则预测输出的模型为：
$$
\hat Y = \hat \beta_0 + \sum_{j=1}^pX_j\hat\beta_j
$$

一般情况下，$\hat\beta_0$考虑做$X_0=1$的参数（其本身为截距，ML中的偏差量），则算法可以表示为：
$$
\hat Y = X_T\hat\beta
$$
如何使用训练数据来拟合这个线性模型？最常用的是最小二乘法，这种方法，我们选择系数$\beta$来最小化残差平方和（RSS-residual sum of squares）：

$$RSS(\beta)=\sum_{i=1}^N(y_i - x_i^T\beta)^2=(\textbf{y} - \textbf{X}\beta)^T(\textbf{y} - \textbf{X}\beta)，\\本书中notation，y，X表示单个某个样本，\textbf{y, X}表示的是向量和矩阵，表示总体$$

RSS关于$\beta$的导数为：$X^T(\textbf{y - X}\beta) = 0$，导数为0的极值点。则如果$X^TX$非奇异矩阵，则$\hat\beta=(\textbf{X}^T\textbf{X})^{-1}\textbf{X}^T\textbf{y}$

有两个场景：

1. 训练数据的每个分类数据都不相关的分量和不同均值的bivariate Gaussian distributions 产生；
2. 训练数据的每个分类数据都是10个小方差的高斯分布混合产生的（使用K-nn）

#### 最近邻方法

最近邻方法使用训练数据集中最近的数据集来形成预测，k-nn拟合产生$\hat Y$过程如下：
$$
\hat Y(x)={1\over k}\sum_{x_i\in N_k(x)} y_i
$$
$N_k(x)$就是x最近的k个邻居，“最近”是个度量方式，一般使用欧氏距离（Euclidean distance）。

对于k-nn拟合，训练数据的错误率和k近似形成一个递增函数，即随着k的变大，错误率增加，当k=1时，一般情况下训练误差为0。(查询其他资料，k一般取值为$\sqrt N$)

#### 从最小二乘法到最近邻法

最小二乘法产生的决策边界非常平滑，而且在拟合时也很稳定。这种方法具有较低的方差和较高的偏差（Error=variance （方差）+ $bias^2$（偏差 + noise（噪音）），方差反映每一次输出结果与模型期望之间的误差，即模型的稳定性，偏差是模型本身的预测和实际值之间存在偏移——因为总是通过有限的训练样本预测无限的真实数据。降低偏差，容易造成过拟合，增加方差。偏差是预测值或预测值的均值与真值之间的差异；方差是模型在某个数据点上预测的变化量。偏差和方差之间的权衡，详见[BiasVariance](http://scott.fortmann-roe.com/docs/BiasVariance.html)）

最小二乘法更适合于上面描述的情景1，而最邻近法更适合情景2。最邻近法的预测结果依赖于点的位置和周围数据分布，所以模型稳定性上不好，方差较高但更准确（偏差更低）。

### 统计决策理论

这节创建了一些理论，用来为开发模型提供一些框架（例如之前介绍的那两个）。

我们寻找一个函数f(X)来预测Y，这个理论需要一个损失函数(loss function)$L(X,f(X))$，到目前为止最常见和最方便的是平方误差损失（squared error loss）：$L(X, f(X)) = (Y - f(X))^2$，这个导出我们选择f的标准：
$$
EPE(f) = E(Y - f(X))^2 = \int[y - f(x)]^2Pr(dx, dy)
$$
离散变量时上式的推到过程：
$$
设g(X,Y)=[Y- f(X)]^2，则\\
EPE(f) = E_{X,Y}(g(X,Y)) \\
= \sum_{x,y}g(x,y)p(X=x,Y=y)\\
=\sum_{x,y}g(x,y)p(Y=y|X=x)p(X=x)\\
=\sum_x(\sum_yg(x,y)p(Y=y|X=x))p(X=x)\\
=E_X(\sum_yg(X,y)p(Y=y|X))\\
=E_XE_{Y|X}(g(X,Y)|X)，\\
E_{X,Y}是表示X,Y联合分布的期望，E_{Y|X}表示设X是常量，求Y的期望。
$$
所以求EPE最小，其实是求$E_XE_{Y|X}(g(X, Y)|X)$最小，因为$E_{Y|X}(g(X, Y)|X)>0$，上式最小等价于求$E_{Y|X}(g(X, Y)|X)$最小，而$E_{Y|X}((Y-f(X))^2|X) \ge E_{Y|X}((Y - E(Y|X))^2|X)$，因此当$f(X)=E(Y|X)$时，$E_{Y|X}(g(X, Y)|X)>0$最小。所以最优解决方案就是$f(X) = E(Y|X)$。

$E([Y-f(X)]^2|X) \ge E([Y - E(Y|X)]^2|X)$证明过程：
$$
E((Y-f(X))^2|X) = E(([Y-E(Y|X)] + [E(Y|X) - f(X)])^2|X)\\
=E([Y - E(Y|X)]^2 + [E(Y|X - f(X))]^2 + 2(Y-E(Y|X))(E(Y|X - f(X)) |X)\\
=E([Y - E(Y|X)]^2|X) +  E([(Y|X - f(X))]^2|X)\\
\ge E([Y - E(Y|X)]^2|X)，由于给定X则E(E(Y|X)-f(X))为常量
$$
EPE-the expected（squared）prediction error（$X^2$的概率和X的概率相同，XX表示一次实验X发生且X发生的概率，那当然是X的概率了，$X^2$不是表示两次实验都是X，而是表示一次实验，这点要理清楚）。

最小化EPE：$f(x)=argmin_cE_{Y|X}([Y-c]^2|X=x)$，得到$f(x)=E(Y|X=x)$。

局部常量函数——一般函数是set to set，但是局部常量函数是拓扑空间 to set，拓扑空间是一个域，可能是某一点的邻域组成。knn就是求x点最近的几个邻居，相当于说是x点的邻域内的点的值都统一个值，所以是局部常量函数。

这里只介绍了这一个损失函数，把L2替换成L1就是另一个损失函数，后面会涉及到其它的损失函数。

对于分类型变量，将损失函数定义成K*K的矩阵L，K=card(G)（card-集合G的元素个数），L对角线上的元素值为0，其他地方为非零值，L(k,l)的值是将类别$G_k$分类为$G_l$的代价。最常用的是0-1损失函数，所有被错误分类的元素都被填充为1，那么预测错误值的期望：$EPE=E[L(G, \hat G(X))]$，设分布为$Pr(G, \hat G)$，所以$EPE=E_X\sum_{k=1}^KL(G_k, \hat G(X))Pr(G_k|X)$，则$\hat G(x) = argmin_{g\in G}\sum_{k=1}^K L(G_k, g)Pr(G_k|X=x)$，因为是0-1损失函数，则$\hat G(x)=argmin_{g\in G}[1 - Pr(g|X=x)]，\hat G(x) = \max_{g\in G} Pr(G_k|X=x)$。这个解决方案被称作贝叶斯分类器（其实就是样本中出现概率最大的为分类器结果。

最近邻法可以处理非线性数据，以及可以对数据自适应。

### 高纬度

维度增大，使得点与点之间的距离越来越远，设想使用欧氏距离计算距离：$\sum_{j=1}^p(x_j - y_j)^2，p$，则随着p增大，此值变大，则会整个空间会变得很稀疏。各点距离单位球中心距离的中间值计算公式：$d(p, N)=(1-2^{1/N})^{1/p}$。

<red>这一章读起来很费劲，稍后回过头来再读。<red>

### 统计模型，监督学习和函数逼近

根据上面的介绍，回归函数f(x)=E(Y|X=x)，但是有两种情况下是行不通的：

1. 输入空间是高纬度，最近邻因为没有要求和目标点距离的限制（最近的点可能也离得很远），这样会导致很大错误
2. 如果存在已知的特殊结构，按这种接口可以更好的拟合数据，减少偏差和方差

下面介绍一些在算法中克服维度问题的方法。

#### 联合分布的统计模型

假设我们的数据服从统计模型：$Y=f(X) + \epsilon，E(\epsilon) = 0$，而且$\epsilon$和X互相独立。

一般来说还有其他未测量的误差对Y产生影响，也包括测量误差。这个AM模型假设我们可以通过错误$\epsilon$来捕获隐藏的确定的关系。

#### 监督学习

假设$Y=f(X) + \epsilon，E(\epsilon) = 0$这个是合理的推测，监督学习试图通过样例数据学习得到f，由$(x_i, y_i)，i=1,...,N$组成训练数据，将输入数据输入学习算法的系统中，产生对应的输出结果$\hat f(x_i)$。通过修改输入输出之间的关系f来使用偏差来计算选择合适的算法。在完成学习后，希望人工产生的学习算法的产出能够足够接近实际值，而且可用于新的输入值。

#### Function Approximation

前面的学习范例一直是研究机器学习（与人类推理类比）和神经网络（与具有大脑的生物类比）领域中的监督学习问题的动机。主要使用了数学方法和统计方法，主要是函数逼近和估计。

我们遇到的很多函数估计都会和参数$\theta$关联，例如线性模型$f(x) = x^T\beta，\theta=\beta$，另一类有用的函数估计即广义线性模型：
$$
f_\theta(x) = \sum_{k=1}^K h_k(x)\theta_k
$$
其中$h_k$是函数或者x输入向量的转换操作，一般是多项式($x_1^2,x_1x_2^2$)或三角函数($\cos x_1$)等。当然也有非线性的函数，例如sigmoid（logistics regression）：$h_k(x)={1\over 1 + exp(-x^T\beta_k)}$。

我们可以使用最小二乘法来估计线性模型$f_\theta$参数$\theta$，最小化残差平方和：
$$
RSS(\theta) = \sum_{i=1}^N(y_i - f_\theta(x_i))^2
$$
这个可以作为一个$\theta$的函数，这可以作为additive error model合理的标准。

我们得到了一个简单的方法来做，解决方案需要使用迭代方法或者数字优化（numerical optimization）。

最小二乘法通常是比较合适的方法，但是它不是唯一的方法，而且在某些时候会显得不那么合适。一个更加通用的方法是最大似然估计（maximum likelihood estimation），设有随机变量$y_i, i = 1, ..., N$服从分布$Pr_\theta(y)$，则N个事件发生的概率是$\prod_{i=1}^NPr_\theta(y_i)$，对其取log得到：$L(\theta)=\sum_{i=1}^N\log Pr_\theta(y_i)$。

__最大似然估计的假设__是：$\theta$最合理的值就是使样本存在的概率最大的值。

最小二乘法模型$Y=f_\theta(X) + \epsilon，\epsilon \sim N(0, \sigma^2)$，在最大似然估计模型下表示为：$P(Y|X,\theta)=N(f_\theta(X), \sigma^2)$，根据之前的推论$f(X) = E(P(Y|X))$。

正态分布的公式为：$f = {1\over\sqrt{2\pi}\sigma}exp(-{(x-\mu)^2\over 2\sigma^2})$，将$f, \mu = f_\theta(X)$带入$L(\theta)$中得到：

$\sum_{i=1}^N\log{1\over \sqrt{2\pi}\sigma} - \sum_{i=1}^N{(y_i-f_\theta(X))^2\over 2\sigma^2}=-{N\over 2}\log(2\pi) - N\log\sigma - {1\over 2\sigma^2}\sum_{i=1}^N(y_i - f_\theta(X))^2$，前两项是定值，所以等价于求$\sum_{i=1}^N(y_i - f_\theta(X))^2$最小，这个就和最小二乘的结果切合了。

### 结构回归模型（Structured Regression Models）

对于一些结构化的的方法可能比上面提到的方法更适合，更能拟合数据。

#### 一些问题

考虑下面公式：$RSS(f)=\sum_{i=1}^N(y_i - f(x_i))^2$，对于任何f，传入训练数据$(x_i, y_i)$，都是一个解决方案。

因为N是有限的，所以为了获得有用的结果，我们必须限制无限的解决方案成一个更小的函数集合。如何决定这些限制条件基于对数据的发现，这些限制可能通过$f_\theta$编码或者直接产生学习算法。这些解决方案的限制类别是这本书的主题。有一件事必须说明，任何对获得唯一解决方案的限制都不能消除其他可能性。有无限多可能的限制，每一个都会对应一个唯一的解决方案，所以问题关键就是对约束的选择。

通常，大多数学习方法施加的约束可以被描述为一种或另一种的复杂度限制。 这通常意味着输入空间的小区域中的某种规则行为。 也就是说，对于在一些度量中彼此足够接近的所有输入点x，f表现出一些特殊结构，例如接近常数，线性或低阶多项式行为。 然后通过在该邻域中的平均或多项式拟合获得估计量。

约束的强度由邻域大小决定。 邻域的大小越大，约束越强，解决方案对约束的特定选择越敏感。 例如，局部常数拟合在无穷小的邻域中根本没有约束; 非常大的邻域中的局部线性拟合几乎是全局线性模型，并且非常有限。

 一些方法，如内核和局部回归和基于树的方法，直接指定邻域的度量和大小。 到目前为止讨论的最近邻法是基于局部函数是常数的假设; 接近目标输入$x_0$，函数不会改变太多，因此可以平均输出以产生$f(x_0)$。

但是，有个事情必须清楚，邻域问题很容易在高维数据中出现问题。而克服高纬度问题的方法具有用于测量邻域的相关方法，这些方法基本上不允许邻域在所有方向上同时较小。

### 限制估计器的类别

非参数回归技术或学习方法的多样性根据所施加的限制的性质而分为许多不同的类别。这些类不是独特的，确实有些方法分为几个类。每个类具有与其相关联的一个或多个参数，有时称为平滑参数，其控制局部邻域的有效大小。 这里我们描述三大类。

#### 粗糙惩罚和贝叶斯方法（Roughness Penalty and Bayesian Methods）

这个方法是通过给RSS(f)增加一个显示的惩罚项——粗糙惩罚——来控制：$PRSS(f;\lambda)=RSS(f) + \lambda J(f)$。

惩罚函数也叫做正则化方法。例如一维输入数据的一个惩罚项，__三次平滑样条（cubic smoothing spline） __：$PRSS(f;\lambda)=\sum_{i=1}^N(y_i - f(x_i))^2 + \lambda\int[f^{\prime\prime(x)}]^2dx$。

__[投影追踪回归(projection pursuit regression)](http://www.csee.wvu.edu/~xinl/library/papers/math/statistics/projection_pursuit.pdf)__

#### 核方法和局部回归（Kernel Methods and Local Regression）

这个方法可以被认为是通过指明邻域的性质和局部拟合的正则函数来明确提供回归函数估计或条件期望。kernel function $K_\lambda(x_0, x)$指明了邻域，这个函数给$x_0$的一个区域内赋权值，例如：Gaussian kernel使用的是Gaussian密度函数：
$$
K_\lambda(x_0, x) = {1\over \lambda} exp[-{||x - x_0||^2\over 2\lambda}]
$$
可以知道，距离$x_0$越远，则权值越小。

最简单也是最早的核估计——Nadaraya–Watson，加权平均：$\hat f(x_0) = {\sum_{i=1}^NK_\lambda(x_0, x_i)y_i\over\sum_{i=1}^NK_\lambda(x_0, x_i)}$，分母能发现是所有权值的和。一般情况下，我们能够定义$f(x_0)$的一个局部回归为$\hat f_{\hat\theta}(x_0)$，最小化$\hat\theta:RSS(	f_\theta, x_0) = \sum_{i=1}^NK_\lambda(x_0, x_i)(y_i - f_\theta(x_i))^2$。

$f_\theta$是一些参数化方法，例如一些低阶多项式，如：

* $f_\theta(x) = \theta_0$，常数函数，Nadaraya–Watson就是这样
* $f_\theta(x) = \theta_0 + \theta_1 x$就是著名的局部线性回归模型

KNN也可以被看做一个核方法，$f_\theta(x)={1\over k}\sum f(K_k(x_0, x))，K_k(x_0, x)=I(||x-x_0||\le||x_{(k)} - x_0||)$，指示函数$I$用于表示某个元素是否在集合中，例如：$I_A(x)=1，x \in A；0，x\notin A$。

这些方法都需要在高维的情况下进行调整，针对高维情况，下面再介绍。

#### Basis Functions and Dictionary Methods

这类方法包括了我们熟悉的线性和多项式展开，也包括了跟多灵活的模型。f基本函数的线性扩展：
$$
f_\theta(x) = \sum_{m=1}^M\theta_mh_m(x)，h_m是输入变量x的一个函数（h算是基本函数？），线性指的是\theta的操作
$$
对于一维数据x，K阶的多项式样条函数（样条函数是一个函数分段由多项式函数定义，在每个多项式对接的地方高度平滑，这些对接点称为knots）可以由M个样条基函数适当的序列来表示，M个样条函数又由M-K knots决定。

具有线性输出权重的单层前馈神经网络模型可以被认为是一种自适应的基函数的方法，模型可以被表示为：
$$
f_\theta(x) = \sum_{m=1}^M\beta_m\sigma(\alpha^T_mx+b_m)，\sigma(x) = 1/(1 + e^{-x})被称为激活函数（activation function）
$$
激活函数：在神经网络中，一个节点的激活函数定义在给定输入或输入集时节点的输出。一个计算机芯片电路可以被看做是数字网络中的激活函数——根据输入来输出”ON“（1）或者”OFF“（0）。

这些自适应选择的基函数也被称作是字典方法（dictionary method），而且通过某种类型的搜索机制建立模型。

### 模型选择和偏差-方差的衡量

上面描述的所有模型和很多接下来要讨论的模型都有平滑或者复杂性参数，这些取决于：

* 罚项的参数，如ridge、lasso函数罚项的参数
* 核的宽度，如局部加权平均函数的sigmoid函数的宽度
* 基函数的数量，如上面介绍的线性扩展

预测误差期望：$EPE_k(x_0)=E[(Y-\hat f(x_0))^2|X=x_0]=$

## 线性回归方法

线性模型比较简单，而且也经常能够对数据输入输出做出比较好的解释。就预测目的而言，线性模型甚至可以跑赢非线性模型，尤其是小数据量、低噪音和稀疏数据的情况下。虽然线性模型在计算机之前已经开始研究，但是这是理解非线性模型的基础，而且有些非线性模型直接就是线性模型的推广。

### 线性回归模型和最小二乘法

设我们有输入向量$X^T=(X_1, X_2,...,X_p)$，预测真值Y，线性模型格式如下：
$$
f(X) = \beta_0 + \sum_{j=1}^p X_j\beta_j
$$
线性模型的前提假设是回归函数E(Y|X)是线性的，或者线性模型是一个合理的近似估计。其中$\beta_j$是未知参数，$X_j$可以来自于下面的几种场景：

* 定量输入，数值型
* 定量输入值的一些转换，例如：log，平方根或者平方等
* 基本数据的扩展，例如：$X_2 = X_1^2$, $X_3=X_1^3$，多项式表示
* 数字的或者定量输入进行分段然后使用哑编码，例如：G是一各5级的输入，我们创建$X_j，j=1,2..5；X_j=I(G=j)$
* 变量之间运算，例如：$X_3=X_1\cdot X_2$

设训练集$(x_1, y_1),...,(x_N, y_N)，估计\beta=(\beta_0, ..., \beta_p)^T，x_i = (x_{i1}, x_{i2},...,x_{ip})^T$，最常用的估计方法就是最小二乘法，最小化残差平方和：$RSS(\beta) = \sum_{i=1}^N(y_i - f(x_i))^2 = \sum_{i=1}^N(y_i - \beta_0 - \sum_{j=1}^p x_{ij}\beta_j)^2$。

从统计学角度来看，如果数据$(x_i, y_i)​$是在其总体中随机抽样产生的，则这个估计方法是很合理的。即便$x_i​$不是随机的，只要$y_i​$在给定$x_i​$后事条件独立的，则这个估计还是有效的。

使用矩阵表示RSS，可以得到$\hat\beta=(\textbf X^T\textbf X)^{-1}\textbf X^Ty$，则预测值为：$\hat y = X\hat\beta = \textbf X (\textbf X^T\textbf X)^{-1}\textbf X^Ty$，y前面的那块叫做”hat“矩阵，像是y的一个hat。

协方差矩阵（covariance matrix，dispersion matrix或variance–covariance matrix）：矩阵的i,j位置是随机向量的第i个和第j个元素的协方差。

假设观测值$y_i$无关联的，并且其方差不变，设为$\sigma^2$，并且设$x_i$是固定的（非随机）。则最小二乘法估计的协方差矩阵是：$Var(\hat\beta)=(\textbf X^T\textbf X)^{-1}\sigma^2，i,j位置上的元素值是\hat\beta的第i个和第j个的协方差值$，一般$\sigma^2$估计值为$\hat\sigma^2={1\over N-p-1}\sum_{i=1}^N(y_i - \hat y_i)^2$，之所以分母是N-p-1而不是N，是为了使$\hat\sigma^2$是$\sigma^2$的无偏估计，即:$E(\hat\sigma^2)=\sigma^2$。

假设$f(X) = \beta_0 + \sum_{j=1}^p X_j\beta_j$是平均值的正确的模型，即Y的条件期望对$X_1, X_2,...,X_p$是线性的。假设Y和他的均值的偏差是可加而且服从高斯分布。因此：
$$
Y=E(Y|X_1, ..., X_p) + \epsilon = \beta_0 + \sum_{j=1}^pX_j\beta_j + \epsilon，\epsilon\sim N(0, \sigma^2)
$$

__卡方分布__:设$Z_1,Z_2,...,Z_k$是独立服从正态分布的随机变量，$Q=\sum_{i=1}^kZ_i^2$服从分布叫做自由度为k的卡方分布，一般标识为:$Q\sim \chi^2 or Q\sim\chi_k^2$。

- [ ] 疑问：P66-67，$（N-p-1)\sigma^2$服从的卡方分布的假设检验和置信区间的问题？

[__自由度__](https://en.wikipedia.org/wiki/Degrees_of_freedom_(statistics)):统计计算中可以自由修改的变量个数，换句话是定义位置所需要的最少数量的独立坐标的个数。

__z-score__:标准分数，一个分数与平均数的差再除以标准差的过程，用公式表示为：$z=(x-\mu)/\sigma$，z值代表原始分数和平均值之间的距离，是以标准差为单位计算。表示原始分数离平均分多少个标准差，表明原始分数在分布中的地位

__测试系数的重要性__，例如测试是否可以将一个分类变量排除到模型之外，我们需要测试对这个分类变量的所有哑变量的参数系数是否都可以设置成0，这里我们使用F分布：
$$
F={(RSS_0 - RSS_1)/(p_1 - p_0)\over RSS_1/(N-p_1 - 1)}，RSS_1是更大的模型（p_1+1个参数）残差平方和；RSS_0是更小模型的残差平方和
$$
F统计（F-test，F检验）可以用来表达两个模型之间的显著性，例如上式，可以定量的表示出$RSS_1$是否会更好的拟合数据。$p_1-p_0$个变量考虑其参数为0。（$RSS_1$模型嵌套$RSS_0$模型，意思应该是后面的模型参数包含在前面模型中，拥有更多参数的模型能够更好的拟合数据，而且拟合程度最差也跟更小参数一样）。

F统计测量在一个更大模型中增加每个参数时RSS的变化，通过$\sigma^2$来进行归一化。

#### 高斯马尔科夫定理

最小二乘法估计获得的参数$\beta$在各种无偏估计中有最小的方差（应该是偏差吧），但是事实证明无偏估计不一定是明智的选择。
设$\theta=\alpha^T\beta，E(\alpha^T\beta) = E(\alpha^T(X^TX)^{-1}X^Ty)= E(\alpha^T(X^TX)^{-1}X^TX\beta)=\alpha^T\beta$。所以，最小二乘法是无偏估计，估计量的期望等于真值。第二个推导公式$y=X^T\beta$。

高斯马尔科夫定理定义：如果有任何其他线性估计$\widetilde \theta = c^Ty$是$\alpha^T\beta$的无偏，即$E(c^Ty)=\alpha^T\beta$，则$Var(\alpha^T\hat\beta)\le Var(c^Ty)$。

MSE(mean square error): $MSE(\widetilde \theta)=E(\widetilde\theta - \theta)^2 = Var(\widetilde\theta) + E(\widetilde \theta- \theta)^2$，第一项就是方差，第二项就是偏差的平方，由于线性估计是无偏估计，所以偏差为0。

然而可能存在一个有偏估计——有更小的MSE值，通过增大一点偏差来大幅度减小方差。

有偏估计使用还是比较普遍，任何方法收缩或者设置某个最小二乘法中的系数为0可能就是一个有偏估计，之前提到过的变量子集（variable subset）、ridge回归等都是有偏估计。从实际观点来看，大多是模型对于真值都是有偏差的，因此就是有偏的，选择一个适当的模型就是在偏差和方差之间做衡量。

均方误差和预测精度息息相关，假设存在估计$\widetilde f(x_0)=x^T_0\widetilde\beta$，其EPE（expected prediction error）是：
$$
E(Y_0 - \widetilde f(x_0))^2 = \sigma^2 + E(x_0^T\widetilde\beta - f(x_0))^2 = \sigma^2 + MSE(\widetilde f(x_0))
$$
EPE和MSE之间就差了一个$Y_0$的方差。

#### 从单变量回归到多变量回归

假设单变量无截距的模型：$Y=X\beta + \epsilon$， 则$\hat\beta={X^Ty\over X^TX}={\sum_1^Nx_iy_i\over\sum_1^Nx_i^2}={<x,y>\over<x,x>}，<x,y>即x和y的内积$.

输入数据正交基本都是实验需要，对于实际的观测数据，基本上不会正交，所以需要我们对他们进行正交化。

可以采用Grem-smichdt正交化方法来对输入的数据的列向量进行正交化。

这里采用的方法，选N维向量为基向量，向量元素值全为1，即：`np.ones(N)`。

__计算方法__：一共分两步，第一步计算第$x_j$的正交基$\textbf z_j，\textbf z_j=x_j - \sum_{k=0}^{j-1}\hat\gamma_{kj}\textbf z_k$，然后再计算$\hat\beta_j = {<\textbf z_j, y>\over<\textbf z_j, z_j>}$。如果$x_p$和某一个$x_k$高度相关，残差向量$z_p$将趋向于。

可以使用下面的式子表示$\textbf X，\textbf X=\textbf Z \Gamma$，$\Gamma$是上三角矩阵，元素值为$\hat\gamma_{kj}$，引入对角矩阵$\textbf D$，其元素值$D_{jj}=||z_j||$，所以：
$$
\textbf X = \textbf Z\Gamma=\textbf Z\textbf D^{-1}\textbf D\Gamma=\textbf Q \textbf R，这就是QR分解（QR decomposition）
$$
这样，则$\hat\beta=\textbf R^{-1}\textbf Q^Ty，\hat y = \textbf{QQ}^Ty$，这里$\textbf{QQ}^T=\textbf I$。

#### 多输出（multiple outputs）

假设我们有多输出变量$Y_1, Y_2, ..., Y_K$，通过输入变量$X_1, X_2, ..., X_p$来预测，我们假设线性模型对每一个输出有：
$$
Y_k = \beta_{0k} + \sum_{j=1}^pX_j\beta_{jk} + \epsilon_k=f_k(X) + \epsilon_k
$$
有N个训练数据实例我们可以写成矩阵的形式：$\textbf Y = \textbf{XB} + \textbf E，\textbf Y-(N,K)，\textbf X-(N,p+1)，\textbf B-(p+1, K)，\textbf E-(N, K)$

但变量函数损失变量的直接推广：
$$
RSS(\textbf B)=\sum_{k=1}^K\sum_{i=1}^N(y_{ik} - f_k(x_i))^2=tr[(\textbf Y-\textbf X\textbf B)^T\textbf (\textbf Y-\textbf X\textbf B)]，tr为矩阵的迹=\sum_{i=1}^na_{ii}
$$
最小二乘法估计和之前公式一样：$\hat{\textbf B}=(\textbf X^T\textbf X)^{-1}\textbf X^T \textbf Y$。

### 子集选择（Subset Selection）

有两个原因让我们对最小二乘法估计感到不满：

* __预测精度(prediction accuracy)__：最小二乘法通常有低偏差（bias-因为就是以低bias来构建算法的）和高方差（数据集的不同产生差异较大的结果），而这两者之和体现了预测误差。预测精度可以通过收缩某写特征的参数或设置某些参数为0来提升，这样可能会让偏差变大，但是方差会降低，从而达到提升整体的预测精度。（是否可以判断偏差的一阶导数和方差的一阶导数来判断变更可能导致的两者的变化速率关系）；
* __可解释性(interpretation)__：有时候我们有大量的预测因子（predictor-即特征），我们经常想获得尽可能小的预测因子子集来表现出最强的效果，少量的预测因子也更利于我们更好的解释预测因子与预测变量之间的关系（x和y的关系）。

保留变量的子集，然后从模型删除其他的变量，然后使用最小二乘法对保留的子集变量进行参数估计。

#### 最佳子集选择

最佳子集选择回归查找每一个$k\in{0,1,2,...,p}$，使得RSS最小。如何选择k是在偏差和方差之间做权衡。

一个方法：[leaps and bounds](http://www.stat.washington.edu/adobra/classes/536/Files/week3/leapsandbounds.pdf)

#### 向前和向后逐步选择

Forward- and Backward-Stepwise Selection

如果p大于40，要遍历所有k的可能值则变得不可能。

##### Forward-stepwise selection

从截距开始，然后逐步从预测因子（特征值）中选择最能提升拟合效果的预测因子作为子集的元素值，得到一系列以k为索引的模型，所以按照这个方法肯定可以获得k值。由于可能候选的预测因子较多，要进行较多的运算，将数据进行可以利用当前拟合的QR分解来迅速的选择下一个候选因子（只计算$z_k$即可计算新增因子的QR分解，从而能够很快计算出拟合参数）。

向前逐步选择方法是一个贪婪算法，相比best-subset selection，此方法可能产生的不是最优解，但是有几个原因说明他是可选的：

* __计算性__: 对于p很大的情况，计算best-subset selection基本是不可能的，但是Forward-stepwise selection永远是可行的
* __统计性__: 选择best-subset的每一个大小都会付出一部分方差的代价，forward-stepwise selection有更多的限制条件，将获得更低的方差，当然可能产生较大的偏差

##### Backward-stepwise Selection

和forword相反，backward是从全模型开始，然后逐步剔除对拟合数据产生最小影响的预测因子。候选的预测因子中最小z-score的变量将被删除。__backward仅仅只能用于N>p的情况，而forward在任何情况下都是可用的。__

有一些软件包同时进行forward和backward，选择最好的一个，例如R中的step函数使用AIC准则来权衡选择——在每一步中，选择因增加或丢掉造成AIC最小的预测因子。

__AIC__:Akaike information criterion，最小信息准则，衡量统计模型拟合优良性的一种标准。一般情况下:$AIC=2k-2\ln(L)$，k是参数数量，L是似然函数。假设条件是模型误差服从独立正态分布。n为观察数，RSS为残差平方和，则AIC变为：$AIC=2k + n\ln(RSS/n)$。

#### Forward-Stagewise Regression

FS（Forward-Stagewise）回归相比froward-stepwise回归有更多的约束，它和stepwise的起点相同，都是从截距开始（截距值为$\overline y$），其他因子的系数都初始化为0。每次迭代，算法识别与当前残差最相关的变量（每次迭代都计算一次残差？看每个变量减小残差的大小？多次迭代可能会对同一个变量产生影响），然后计算当前残差关于这个自变量简单的最小二乘法的系数（因为线性模型最小化残差就会得到参数值），随后将这个系数加到之前这个变量的系数上，算法持续到没有自变量与残差有关系。与stepwise不同的是，stagewise只更新当前选定的变量的系数，而stepwise每一步取得新变量，都要重新计算一次，会对其他变量的参数产生影响。所以stagewise拟合数据相对较慢，但正因为此，在高维数据中可能会有更好的表现。

注意和stepwise的不同，这里每一步都是选和残差自相关，而且迭代一次不会删除变量，也就是类似于有放回式的抽样，每次迭代都是从所有变量里面选，所以迭代计算中会出现多次选择同一变量，更新其参数值。

### 收缩方法（Shrinkage Methods）

通过subset selection，可以保留或丢掉预测因子，产生相比整个模型来说解释性较强、预测误差更低。然而因为其是非连续的方法（变量要么被保留要么被丢弃），它经常表现出一种高方差，所以对预测误差来说也产生不良影响。收缩方法则更加连续，而且不受高可变性影像，更加稳定。

#### Ridge Regression（岭回归）

岭回归通过对他们（参数$\beta$）的大小施加惩罚来收缩回归系数，岭回归中，最小化惩罚后的残差平方和：
$$
\hat\beta^{ridge}=argmin_\beta\{\sum_{i=1}^N(y_i - \beta_0 - \sum_{j=1}^px_{ij}\beta_j)^2 + \lambda\sum_{j=1}^p\beta^2_j\}
$$
这里的$\lambda\ge 0$，是控制收缩量的复杂度参数：$\lambda$越大，收缩量越大。

另一种等价的表达方式：
$$
\hat\beta^{ridge}=argmin_\beta\sum_{i=1}^N(y_i - \beta_0 - \sum_{j=1}^px_{ij}\beta_j)^2 ，subject\ to\  \sum_{j=1}^p\beta^2_j\le t
$$
这个对参数的限制就很明显了，上面两个式子中的$\lambda$和t一一对应。

当线性模型中有很多变量相关，他们的系数就会变得不确定，导致每次拟合产生的系数方差很大（因为$\textbf X$是奇异矩阵），假设$x_i$和$x_j$相关，则$\beta_i$可以和$\beta_j$抵消（这两个系数值绝对值大小相当，但是符号相反——这样这两个值的取值就有无穷个方法，而对实际y值结果产生不大的影响）。增加__对参数大小的约束__，这个问题可以得到有效的缓解。

由于岭回归不同输入级别结果不同（例如身高单位为cm，都是100级，age，都是10级别）,所以一般先进行数据的标准化。

需要注意的是，惩罚项对$\beta_0$不起约束作用，对截距的惩罚将使程序取决于Y的选择的原点，即：向每个y添加c将不会简单地导致预测的移动相同的量c（也就是说，无截距估计$\hat y$和真值之间差别就是截距，如果对截距惩罚，缩小截距，会对预测产生无法估计的影响，因为调整截距相当于调整y值，而调整y值不会简单导致预测也移动相同的值）。我们估计$\beta_0=\overline y={1\over N}\sum_1^Ny_i$。

按照第一个公式，其$RSS(\lambda) = (\textbf y - \textbf X\beta)^T(\textbf y - \textbf X\beta) + \lambda\beta^T\beta$,岭回归的solution：$\hat\beta^{bridge}=(\textbf X^T\textbf X + \lambda\textbf I)^{-1}\textbf X^T\textbf y$,这样$\textbf X^T\textbf X$就不会是奇异矩阵了，这个是Ridge regression最根本的动机。

如果输入的列向量正交，则$\hat \beta^{ridge}=\hat\beta/(1+\lambda)$。可通过`sklearn.linear_model.ridge.Ridge`和`sklearn.linear_model.base.LinearRegression`来测试。可以发现`Ridge`和`LinearRegression`也都是使用$\overline y$作为$\beta_0$的估计值的。

在使用算法的时候要注意，`fit_intercept`即是否有截距，如果在X中包括1（截距包括在算法中），则在X中增加一列是1，而`fit_intercept`设置为`False`(这样$\beta_0$就不是$\overline y$)，但是Ridge这种就不能使用？因为参数缩减的时候就会将$\beta_0$考虑进去了。如果数据本身没有截距，而回归计算时设置计算截距，则回归计算出来的系数会不那么准确。所以可以在`fit_intercept`位`True`和`False`时都进行拟合，然后评测。

P66~P68需要再看看，SVD对Ridge的影响。

#### Lasso

lasso估计定义为：
$$
\hat\beta^{lasso}=argmin_\beta\sum_{i=1}^N(y_i - \beta_0 - \sum_{j=1}^px_{ij}\beta_j)^2，满足\sum_{j=1}^p|\beta_j|\le t
$$


使用拉格朗日算子格式：
$$
\hat\beta^{lasso}=argmin_\beta\lbrace\sum_{i=1}^N(y_i - \beta_0 - \sum_{j=1}^px_{ij}\beta_j)^2 + \lambda\sum_{j=1}^p|\beta|\rbrace
$$
一些待解决的数学问题：

quadratic programming problem、SVD、field、Lasso的最优化问题

#### 子集选择，岭回归和Lasso回归

当输入矩阵X是正交矩阵时：

* __Ridge regression__：按比例收缩，$\hat\beta^{ridge}={\hat\beta\over 1 + \lambda}$
* __Lasso regression__：Lasso通过因子转换，通过0来丢弃参数，这叫做“soft-thresholding"，$\hat\beta^{lasso}=sign(\hat\beta_j)(|\hat\beta_j|-\lambda)_+$。
* __Best subset__：丢掉所有系数小于第M个最大值的，叫做"hard-thresholding"，$\hat\beta_j\dot I[rank(|\hat\beta_j|\le M)]$

RSS方程产生的椭圆和限制条件形成的区域的第一次交点视为最优解，第一次和限制条件相交就是椭圆最小值了，这时候获得的参数就是该方法下最优的。否则继续放大椭圆还有交点，但是此时的椭圆已经是变大了。

我们可以推广Ridge和Lasso回归，将其视为Bayes估计，考虑下面的式子：
$$
\overline\beta = arg\min_\beta\lbrace\sum_{i=1}^N(y_i - \beta_0 - \sum_{j=1}^px_{ij}\beta_j)^2 + \sum_j^p|\beta_j|^q\rbrace
$$
对于$q\ge0$，q取不同的值，限制条件形成的区域各不相同。q=1是最小的值，使得约束区域凸。

依这种观点，lasso、ridge回归和best subset selection是有不同先验概率的贝叶斯估计，则每个模型就是求最大的后验概率值。使用后验概率的均值作为贝叶斯估计比较常见，ridge回归是后验的均值，但是lasso和best subset不是。（这个均值--贝叶斯不是很理解）

__Elastic Net__：惩罚项为$\lambda\sum_{j=1}^p(\alpha\beta_j^2 + (1 - \alpha)|\beta_j|)$，约束区域有更尖锐的角（不可微分）

#### 最小角度回归（least angle regression）

Least angle regression（LAR）是一个比较新（2004，Efron）的算法，算是一种forward stepwise “democratic“ 版本，正如我们所知LAR和Lasso密切相关，也提供了一种有效的算法，用来计算整个lasso路径（缩小限制范围，减小t值）。

最小角度回归使用方法描述：和forward stepwise类似的策略，但是只需要他需要的预测因子数量。第一步，先识别和输出最相关的变量，相比完全拟合这个变量，LAR将这个变量的参数值连续的向它的最小平方值移动（以减小演化过程中和残差的关系），直到另一个变量和残差关系更大，则将这个变量也纳入计算，它们的系数以保持它们的相关性并减小的方式一起移动，这个过程一致迭代直至所有变量都被纳入模型，最后以完整的最小二乘法拟合结束。

> 算法步骤描述：
>
> 1. 先对所有预测因子标准化（均值为0，向量长为1），开始的残差和参数值为：$r=y-\overline y，\beta_1, \beta_2,...,\beta_p=0$。即：$\sum_{i=1}^Ny_i = 0，\sum_{i=1}^Nx_i=0，\sum_{i=1}^Nx_i^2=1$;
> 2. 找到和r最相关的预测因子$x_j$，计算它们的相关系数，相关系数用两个向量间的夹角余弦值来度量:$<x_j,r>/|x_j||r|$，余弦值越大则说明相关性越大（夹角越小），因为标准化了，所以上面的值就等于$<x_j, r>=x_j^Tr$;
> 3. 设置$\beta_j$从0朝它的最小二乘系数$<x_j, r>$移动，直到有一个其他的变量$x_k$与当前的残差有更大的关系（每次得到一个变量，则使用变量按照最小二乘法来拟合数据，计算出系数，算出残差，然后再找和残差相关性最大的变量。设$A_k$是第k步选择的变量集合（此时k刚进入集合），$\beta_{A_k}$是第k步这些变量的参数（k-1个非零值，第k个刚加入还是0），设当前的残差值为：$r_k=y - X_{A_k}\beta_{A_k}$，那么这一步$\beta_k$的改变方向是：$\delta_k=(\textbf X_{A_k}^T\textbf X_{A_k})^{-1}\textbf X_{A_k}^Tr_k$，系数则被更新为：$\beta_{A_k}(\alpha)=\beta_{A_k} + \alpha\cdot\delta_k$。
> 4. 参照第三步
> 5. 直到p个预测因子全部纳入$A_k$

假设第k步开始时拟合向量是$\hat f(k)$，那么它这一步的变化为：$\hat f_k(\alpha) = f_k + \alpha \textbf u_k，\textbf u_k=\textbf X_{A_k}\delta_k$，$\textbf u_k$是新的拟合方向，”least angle“的意思就是：$\textbf u_k$使得新方向与$A_k$中每一个方向的向量夹角最小（且相等）。$\alpha$是步长，是可以通过预测因子的协方差和算法的分段线性计算出来。（Exercise 3.25）

构造的LAR系数，通过分段线性变化方式进行。

>  当第四步中重新计算参数值时，存在非零参数值变为0，则直接丢弃此变量，然后重新计算残差和系数值。

对于拟合向量$\hat y=(\hat y_1, \hat y_2, ..., \hat y_N)，df(\hat y) = {1\over\sigma^2}\sum_{i=1}^NCov(\hat y_i, y_i)$，df-有效自由度

### Methods Using Derived Input Directions

在许多情况下，我们有大量的输入输数据是相关的，这节介绍产生原始输入$X_j$的少量的线性组合$Z_m，m=1,2,...,M$线性组合，$Z_m$用来代替$X_j$作为回归中的输入，这个方法和线性组合的构建是不同的。

#### 主成分回归（Principal Components Regression）

线性组合$Z_m$使用主成分，主成分回归的输入为列$ z_m=\textbf X v_m$,然后求$y在z_1,..,z_M，M\le p$上的回归，因为$ z_m$是正交的回归公式可以写作：
$$
\hat y^{pcr}_{(M)} = \overline y1 + \sum_{m=1}^M\hat\theta_m z_m，\theta_m = <z_m, y/z_m, z_m>
$$
相当于进行数据转换降维，使用新坐标来表示原始输入数据。

SVD中$\textbf X=\textbf U\Sigma \textbf V^T，\textbf X^T\textbf X=\textbf V\Sigma^T\textbf U^T\textbf U\Sigma \textbf V^T=\textbf V\Sigma^2 \textbf V^T，\textbf U和\textbf V都是正交矩阵，\textbf U^T\textbf U=\textbf I，\Sigma是对角矩阵$，则$\textbf V$中列向量作为主成分进行计算。

主成分分析（Principal Components Analysis）：PCA是一个统计方法，使用正交转换来将一组可能相关的观察值集合（集合大小为p）转换成一组线性不相关变量集合（集合大小为M)，这些新变量叫做主成分，$M\le  p$。

这个转换定义成:首先，第一个主成分是原始数据中方差最大的，第二个新坐标选择和第一个坐标正交且具有最大方差的方向，该过程一直重复，重复次数为数据中的特征数（p），结果向量是一个线性不相关的正交基集合。

协方差矩阵（Covariance Matrix），在概率论和统计学中，协方差矩阵是一个矩阵，其第i,j位置元素值是第i和第j个向量的协方差值。主成分就是协方差矩阵的特征值，可以只取前面几个相对较大的特征值。由于之前计算的时候对$\textbf X$做了标准化（减去均值），则标准化后的$Cov(X_i, X_j)=<X_i, X_j>$，所以协方差矩阵就是$\textbf X^T\textbf X$，可以选择特征值最大的N个对应的特征向量组成的矩阵$\textbf V$，则$\textbf z = \textbf X \textbf V$。

#### 部分最小二乘（Partial Least Squares）

算法步骤：

1. 标准化$x_j，\mu=0, \sigma=1$。设置$\hat y^{(0)} = \overline y1，x_j^{(0)}=x_j，j=1,2,...,p$;
2. 对于m=1,2,...p
   * $z_m = \sum_{j=1}^p(\hat\varphi_{mj}x_j^{(m-1)})，其中\hat\varphi_{mj}=<x_j^{(m-1)}, y>$
   * $\hat\theta=<z_m, y>/<z_m, z_m>$
   * $\hat  y^{(m)} = \hat y^{(m - 1)} + \hat\theta_mz_m$
   * 求$x_j^{(m-1)}$相对$z_m$垂直的向量（其实就是垂直z_m方向上的分量）:$x_j^{(m)} = x_j^{(m - 1)}-[<x_j^{(m-1) }- z_m>/<z_m, z_m>]$
3. 输出序列$\{\hat y^{(m)}\}_1^p$（这个符号的意思应该是，m取值1到p，即输出1到p拟合过程中的$\hat y$值），因为$z_m$是$\textbf X$列向量的线性组合，所以：$\hat y^{(m)}=\textbf X\hat\beta^{pls}(m)$，可以通过PLS的转换过程求出$\hat\beta$。

### Selection方法和Shrinkage方法比对

Ridge Regression：在所有方向收缩，但是对低方差的方向（变量、特征）收缩最大；

PCR：值保留前M个比较大的方差的方向；

PLS：也是收缩低方差方向，但是同样会拉伸方差大的方向。PLS相对不太稳定，所以方差较大，而且预测错误也比ridge回归更高；

相比来说，Ridge有最小的预测错误率，相比PCR和PLS优势有限。

总的来说，Ridge、PLS、PCR回归行为上都比较相似，Ridge regression可能是更好的选择，因为收缩比较平滑。Lasso回归兼有ridge、best subset regression的特点。

## 线性分类方法

### 简介

__odds ratio:__在统计学中，OR是在给定群体的情况下，量化存不存在A和存不存在B的关系强度的三个主要方法中的一个。设A事件发生概率为$p_A$，B事件发生概率为$p_B$,则：$OR={p_A/1-p_A\over p_B/1 - p_B}$。

__log-odds(logit)__: 公式定义：$logit(p)=\log({p\over 1-p})$

$\log(OR)=logit(p_A) - logit(P_B)$

本章我们将集中讨论线性决策边境，我们将讨论非常流行但是不同的方法（可能是对logit中的概率函数）：线性判别分析（linear discriminant analysis）和线性逻辑回归（linear logistics regression），这两个方法本质上的不同是拟合训练数据的线性函数的方式不同（后面具体方法了解后再对比）。

超平面进行分类的分类器：perceptron（感知器），寻找训练数据中的分离超平面。另一种方法就是最佳分离超平面（optimally separating hyperplane）。

虽然本章专注于讨论线性决策边界，但是还是存在很多扩展空间。例如我们扩展数据集$X_1, X_2, ..., X_p$，新数据集中包括他们的乘积和两两乘积$X_1^2, X_2^2, X_1X_2 ..., X_1, X_2, ..., X_p$，这样数据维度就扩充了p(p+1)/2个。在这个增强空间中的线性函数映射到原始空间中的二次函数，因此在原始空间中，决策边境就是二次函数了。这个方法可以被用来表示任何基本的转换：$h(X), h:IR^p\to IR^q，q>p$。

### 指标矩阵的线性回归（Linear Regression of an Indicator Matrix）

这个算法中，输出变量的每一个分类都是通过一个指标变量来表示，记$G$是输出元素的所有可能值的集合。如果$G$有$K$个分类，那么就有$K$个这样的指标$Y_k，k=1, 2, ..., K$，当取值为$G_k$，则$Y_k=1$，其他都是0。则$Y=(Y_1, Y_2, ..., Y_K)$，N个训练集实例组成一个(N,K)的指标矩阵：$\textbf Y$，$\textbf Y$中的元素非0即1，每一个行向量只有一个值是1，回归系数为：
$$
\hat{\textbf B} = (\textbf X^T\textbf X)^{-1}\textbf X^T\textbf Y，因为\textbf Y是(N, K)，所以\hat{\textbf B}是（p+1,K）
$$
如果有新值过来，则分两步对其分类：

* 计算拟合输出：$\hat f(x) = [(1,x)\hat{\textbf B}]^T，产生一个K个元素的向量$
* 识别最大的分量并进行相应的分类：$\hat G(x) = arg\max_{k\in G}\hat f_k(x)，即\hat f(x)向量中最大元素的位置为索引取G中的值$

为什么上面的方法是合理的？一个比较正式的理由就是将回归看做是条件期望。对于随机变量$Y_k，E(Y_k|X=x)=Pr(G=k|X=x)​$，因此每一个$Y_k​$的条件期望似乎是比较合理的目标。

__贝叶斯分类规则__:$\hat G(x)=arg\min_gE_{G|X=x}L(g,G)，L(g,G)，是估计量g和真值G的损失函数$

0-1损失函数$L(g,g')=1,g \ne g';0,g=g'，E_{G|X=x}L(g,G)=1 - Pr(G=g|X=x)$，所以按照贝叶斯分类规则:
$$
\hat G(x)=arg\min_gE_{G|X=x}L(g,G)，L(g,G) = arg\min_g (1 - Pr(G=g|X=x))=arg\max_gPr(G=g|X=x)
$$

而$\hat f(x) = E(Y|X=x)$，所以根据上面的期望等于G=k的概率，所以$\hat G(x) = arg\max_{g\in G}\hat f(x)$。

另一种解释：设$t_k$是（K,K）的单位矩阵（对角线元素全为1，其他元素为0）的列向量（其实就是所有类别的向量集合，第k个元素为1，则表明是k类）。则有：$\hat G(x) = arg\min_k||\hat f(x) - t_k||^2$，而只有$t_k$向量中元素为1的位置和$\hat f(x)$中最大值元素的位置相同时才会取值最小，所以和上式是等价的。

在$K\ge 3$时，一个普遍的规则是使用K-1阶多项式来进行分类。

### 线性判别分析（Linear Discriminant Analysis）

设$f_k(x)$是关于X在G=k时的条件类密度函数，假设$\pi_k$是类k的先验概率，$\sum_{k=1}^K \pi_k = 1$，贝叶斯定理的一个简单应用：
$$
Pr(G=k|X=x) = {f_k(x)\pi_k\over \sum_{l=1}^Kf_l(x)\pi_l}
$$
有很多基于类密度模型的技术，例如高斯分布等。

假设每一个类（类k）都服从多元高斯分布：
$$
f_k(x) = {1\over (2\pi)^{p/2}|\Sigma_k|^{1/2}}e^{-{1\over 2}(x-\mu_k)^T\Sigma_k^{-1}(x-\mu_k)}，\Sigma_k是类k的协方差矩阵
$$
对比k和l两个分类，使用对数比（log-ratio）：
$$
\log{Pr(G=k|X=x)\over Pr(G=l|X=x)}=\log{f_k(x)\over f_l(x)} + \log{\pi_k\over\pi_l}=\log{\pi_k\over\pi_l} - {1\over2}(\mu_k + \mu_l)^T\Sigma^{-1}(\mu_k- \mu_l) + x^T\Sigma^{-1}(\mu_k-\mu_l)
$$
当此式为0，即两个后验概率相等时，其为决策边界，由上式可知其为x的线性函数，在维度为p是为超平面。只考虑其中一个类别，例如k，则得到线性判别函数（这个函数是在所有类别__$\Sigma$__都相同的假设情况下得到的）：
$$
\delta_k(x) = x^T\Sigma_{-1}\mu_k - {1\over 2}\mu_k^T\Sigma^{-1}\mu_k + \log\pi_k
$$
按照决策规则，$G(x) = arg\max_k\delta_k(x)$，由于在实际问题中，高斯分布的参数我们都不知道，所以使用训练数据估计，如下：

* $\hat\pi_k = N_k/N，N_k$为类别为k的观察值数量，N为总的训练数据数量
* $\hat \mu_k=\sum_{g_i}x_i/N_k$，这里是求和
* $\hat\Sigma=\sum_{k=1}^K\sum_{g_i = k}(x_i - \hat\mu_k)(x_i - \hat\mu_k)^T/(N - K)$ (由此可以看出\Sigma对所有类别计算时都是一样得)

如果去掉$\Sigma$对所有类别都相同的假设，则得到__二次判别函数（quadratic discriminant functions (QDA)）__：
$$
\delta_k(x) = -{1\over2}\log|\Sigma| - {1\over2}(x-\mu_k)^{T}\Sigma_k^{-1}(x-\mu_k) + log\pi_k
$$
类与类之间的决策边界：$\lbrace x:\delta_k(x)=\delta_l(x)\rbrace$。

#### 正则化判别分析（Regularized Discriminant Analysis）

一种LDA和QDA的折中，收缩QDA中各个类别独立的协方差矩阵到LDA只有一个共同的协方差矩阵。正则协方差矩阵形式如下：
$$
\hat\Sigma_k(\alpha) = \alpha\hat\Sigma_k + (1-\alpha)\hat\Sigma
$$
对于上式中的$\hat\Sigma$也可以使用同样的方法来将其向一个常量收缩：
$$
\hat\Sigma(\gamma) = \gamma\hat\Sigma + (1 - \gamma)\hat\sigma^2\textbf I，\hat\sigma是设定的值？应该是计算的，因为是估计量
$$
$\hat\sigma$值后续章节可能涉及，需要注意。

#### LDA的计算（Computations for LDA）

对于QDA，计算每一个$\Sigma_k$的特征值分解，$\Sigma_k=\textbf U_k\textbf D_k\textbf U_k^T$，类似LDA的$\Sigma$也可以进行分解，然后带入上面的估计值中计算。

*目前没发现这种方式计算的任何好处，以及书里面写到$\textbf U_k$是标准正交矩阵，这个特征矩阵为什么就是标准正交？*

#### Reduced-Rank Linear Discriminant Analysis

P131

### Logistic Regression

Logistic Regression：通过x的线性函数来对K个类型的后验概率进行建模，与此同时需要保证这些模型的和为1，而且取值范围为[0, 1]。这些模型的形式如下：
$$
\log{Pr(G=1|X=x)\over Pr(G=K|X=x) }= \beta_{10} + \beta_1^Tx;\\\log{Pr(G=2|X=x)\over Pr(G=K|X=x) }= \beta_{20} + \beta_2^Tx;\\\log{Pr(G=K-1|X=x)\over Pr(G=K|X=x) }= \beta_{(K-1)0} + \beta_{K-1}^Tx
$$
虽然这里选的最后一个类别的概率为分母，但是主要在满足取值范围为(0,1]范围内的值都可以作为分布。一种简单的计算如下：
$$
Pr(G=k|X=x)={exp(\beta_{k0} + \beta_k^Tx)\over 1+\sum_{l=1}^{K-1}exp(\beta_{l0} + \beta_l^Tx)}，k=1,...,K-1\\
Pr(G=K|X=x)={1\over 1+\sum_{l=1}^{K-1}exp(\beta_{l0} + \beta_l^Tx)}
$$
设所有参数集合为：$\theta=\lbrace\beta_{10}, \beta_1^T, ..., \beta_{(K-1)0}, \beta_{K-1}^T\rbrace$，将类别$k$的后验概率表示为：$Pr(G=k|X=x) = p_k(x;\theta)$。

K=2时就是比较简单的模型了，一般医学上应用比较多，判断病人可能生、死或是否患病。

#### 拟合Logistic Regression模型（Fitting Logistic Regression Models）

Logistic Regression模型通常使用最大似然估计来拟合，使用条件概率Pr(G|X)，对于N各观察值，最大似然函数为：
$$
l(\theta) = \sum_{i=1}^N\log p_{gi}(x_i; \theta)，p_k = Pr(G=k|X=x_i;\theta)
$$

对于两类（两类的概率是特殊的为$p^y\cdot(1-p)^{1-y}，y\in\lbrace0,1\rbrace$，$p=p(y=1|x)$，则可以表示为：
$$
l(\beta) = \sum_{i=1}^N \lbrace y_i\log p(x_i;\beta) + (1-y_i)log(1-p(x_i;\beta))\rbrace=\sum_{i=1}^N\lbrace y_i\beta^Tx_i - \log(1 + e^{\beta^Tx_i}) \rbrace\\
\beta = \lbrace \beta_0, \beta_1\rbrace
$$
使得最大似然函数取最大值，则根据$\beta$偏导方程为：
$$
{\partial l(\beta)\over\partial\beta}=\sum_{i=1}^Nx_i(y_i - p(x_i;\beta))=0
$$
为了计算上式，需要使用牛顿方法（又称Newton–Raphson Algorithm），需要二次求导，或者是（Hessian matrix）：
$$
{\partial^2l(\beta)\over\partial\beta\partial\beta^T} = - \sum_{i=1}^Nx_ix_i^Tp(x_i;\beta)(1-p(x_i;\beta))
$$
则：$\beta^{new} = \beta^{old}  - ({\partial^2l(\beta)\over\partial\beta\partial\beta^T})^{-1}{\partial l(\beta)\over\partial\beta}$。

设$\textbf y、\textbf X、\textbf p、\textbf W$分别为$y_i、x_i、p(x_i,\beta^{old})、p(x_i;\beta^{old})(1-p(x_i;\beta^{old}))$的数组、矩阵表示，那么上面一阶、二阶偏导可以表示为：
$$
{\partial l(\beta) \over \partial\beta} = \textbf X^T(\textbf y - \textbf p)；{\partial^2l(\beta)\over\partial\beta\partial\beta^T}=-\textbf X^T\textbf W\textbf X
$$
牛顿方法步骤：
$$
\beta^{new} = \beta^{old} + (\textbf X^T\textbf W\textbf X)^{-1}\textbf X^T(\textbf y - \textbf p) =  (\textbf X^T\textbf W\textbf X)^{-1}\textbf X^T\textbf W(\textbf X\beta^{old} + \textbf W^{-1}(\textbf y - \textbf p)) =   (\textbf X^T\textbf W\textbf X)^{-1}\textbf X^T\textbf W\textbf z
$$
使用加权最小二乘法重新表示牛顿步骤：
$$
\textbf z =\textbf X\beta^{old} + \textbf W^{-1}(\textbf y - \textbf p)
$$
这个算法叫做加权迭代最小二乘（iteratively reweighted least squares-IRLS），因为每次迭代解决加权最小二乘问题：
$$
\beta^{new} \gets arg\min_\beta(\textbf z- \textbf X\beta)^T\textbf W(\textbf z - \textbf X\beta)
$$
$\beta=0$可以作为迭代的起始值。

在进行拟合之后，可以对每个特征的参数计算Z-score（每一个参数除以他们的标准差），这样剔除最不显著的（小于2），然后重新拟合求出新参数，再进行判断剔除，最后到没有不显著的参数。

或者另一个更好但是更耗时的方法是逐一剔除一个特征，然后进行拟合，然后执行偏差分析（analysis of deviance）来决定哪一个应该被剔除。

> __最大似然估计（Maximum likelihood estimation）__
>
> $L(X_1, X_2, ..., X_n;\theta_1, \theta_2, ..., \theta_n)=f(X_1;\theta_1, ...,\theta_k)f(X_2;\theta_1,...,\theta_k)...f(X_n;\theta_1,...,\theta_k)$,
>
> $f(X_1;\theta_1,...,\theta_k)是以\theta_1,...,\theta_k为参数的概率密度分布$，则$\hat\theta = arg\max_{\theta_1,\theta_2,...,\theta_k}L(X_1,X_2,...,X_n;\theta_1,...,\theta_k)$
>
> 求$\log L=\sum_{i=1}^n\log f(X_i;\theta_1,..., \theta_k)$最大，导数为0，得到参数估计值。

> 黑塞（海塞）矩阵（Hessian Matrix）
>
> 函数二阶偏导数的方阵，这个函数假设是f，则其是$\mathbb{R}^n\to \mathbb{R}$，即是以一个向量$\textbf x\in\mathbb{R}^n$作为输入，以标量$f(\textbf x)\in \mathbb{R}$为输出，如果f的所有二阶偏导存在，则函数f的Hessian Matrix矩阵是(n,n)的，通常定义为：
> $$
> \textbf H = \begin{vmatrix}\frac{\partial^2f}{\partial x_1^2}& \frac{\partial^2f}{\partial x_1\partial x_2}&...& \frac{\partial^2f}{\partial x_1\partial x_n}\\
> \frac{\partial^2f}{\partial x_2\partial x_1}& \frac{\partial^2f}{\partial^2 x_2}&...& \frac{\partial^2f}{\partial x_2\partial x_n}\\
> ...&...&...&...\\
> \frac{\partial^2f}{\partial x_n\partial x_1}& \frac{\partial^2f}{\partial x_n\partial x_2}&...& \frac{\partial^2f}{\partial^2 x_n}
> \end{vmatrix}
> $$
> 单个元素可以表示为：$\textbf H_{i,j} = {\frac{\partial^2f}{\partial x_i\partial x_j}}$。

> __牛顿方法__
>
> 输入：目标函数$f(x)$，这里可能就是$l(\beta)$，梯度$g(x)=\nabla f(x)$，黑塞矩阵H(x)，精度要求为$\epsilon$
>
> 输出：设f(x)的极小值点为$x^*$
>
> 1. 设初始点$x^{(0)}$，置迭代次数k=0
> 2. 计算$g_k = g(x^{(k)})$
> 3. 若梯度$||g_k||\lt\epsilon$，则停止计算，且$x^*=x^{(k)}$
> 4. 计算$H_k = H(x^{(k)})$，并求$p_k=-H_k^{-1}g_k$
> 5. 置$x^{(k+1)}= x^{(k)} + p_k$
> 6. 置k=k+1，转（2）
>
> 推导过程：
>
> 假设f(x)具有二阶连续偏导数，若第$k$次迭代值为$x^{(k)}$，则可将$f(x)$在$x^{(k)}$附近进行二阶泰勒展开：
> $$
> f(x) = f(x^{(k)}) + g_k^T(x - x^{(k)}) + {1\over 2}(x-x^{(k)})^TH(x^{(k)})(x-x^{(k)})，g_k=g(x^{k})=\nabla f(x^{(k)})，H(x^{(k)})是f(x)的黑塞矩阵
> $$
> 牛顿法利用极小点的必要条件：$\nabla f(x) = 0$，每次迭代中从点$x^{(k)}$开始，求目标函数的极小点，作为第$k+1$次迭代值$x^{(k+1)}$，具体地，假设$x^{(k+1)}$满足：$\nabla f(x^{(k+1)}) = 0$，对上面的泰勒展开求梯度：$\nabla f(x) = g_k + H_k(x - x^{(k)})$，所以设k+1次就是极值点，$\nabla f(x^{(k+1)}) = g_k + H_k(x^{(k+1)} - x^{(k)}) = 0$，因此：$x^{(k+1)} = x^{(k)}  - H_k^{-1}g_k$。

> __M-estimator__
>
> 设$f$是一个有参数$\theta$的函数，则：$\hat\theta = arg\min_\theta(\sum_{i=1}^nf(x_i,\theta))$被叫做M-estimator（M for maximum likelihood-type)

> __IRLS__
>
> Iteratively reweighted least squares(IRLS)方法被用来解决有如下形式目标函数最优化问题：
> $$
> \hat\beta = arg\min_\beta\sum_{i=1}^n|y_i - f_i(\beta)|^{p}
> $$
> 通过迭代方法，每一步包括解决一个加权最小二乘问题（如下形式）：
> $$
> \beta^{t+1} = arg\min_\beta \sum_{i+1}^n(w^{(t)})|y_i - f_i(\beta)|^2，w^{(t)}=|y_i - X_i\beta^{(t)}|^{p-2}，p为Lp问题阶数
> $$
> IRLS被用来寻找一般线性模型的最大似然估计

> __Deviance__
>
> 偏差，统计学中偏差是用来衡量模型拟合质量，它是OLS（一般最小二乘法）下使用残差和来评估模型的一个一般化方法，将其应用到最大似然估计的模型拟合方法中。
>
> 在OLS中，最小的残差平方和来作为最优模型的度量，也是通过这个方法来拟合参数值。在最大似然估计拟合出的模型参数后，如何度量哪个最大似然估计更好？
>
> 模型$M_0$基于数据集$y$的$deviance$定义为：
> $$
> D(y) = -2(\log(p(y|\hat\theta_0)) - \log(p(y|\hat\theta_s)))
> $$
> $\hat\theta_0$表示为模型$M_0$拟合出来的参数值，$\hat\theta_s$表示为saturated model拟合出来的参数（saturated model：饱和模型，自由度为0，指各观测变量之间均容许相关的最复杂的模型，是人为设定的约束条件最少的模型，纯粹按照数据的相互关系来构建最优的模型，所以是理想状态下的最优模型）。
>
> 事实上如果存在$M_1$和$M_2$，则$D_1 - D_2 = -2(\log(p(y|\hat\theta_1)) - \log(p(y|\hat\theta_2)))$，不用计算饱和来比较两个模型中的偏差

#### $L_1$正则Logistic回归

类似Lasso，Logistic也是用$L_1$来作为模型罚项，截距也不在罚项范围内，和Lasso不同的是，这里的罚项是为了求最大值：
$$
\max_{\beta_0, \beta}\lbrace\sum_{i=1}^N[y_i(\beta_0 + \beta^Tx_i) - \log(1+e^{\beta_0 + \beta^Tx_i})] - \lambda\sum_{j=1}^p|\beta_j|\rbrace
$$
上面这个函数是凹的，一个解决方案是使用非线性规划方法。

#### Logistic回归还是LDA？

一般来说，LDA的前提假设是输出数据服从高斯分布，但是这个条件可能不满足。所以Logistic相对来说更安全，也更健壮，因为其所需要的假设更少。据经验来说，这些模型的结果相似，甚至LDA在不适合的地方使用时。

### 分离超平面（Separating Hyperplanes）

有如下分类器，计算输入特征的线性组合，然后返回分类结果，叫做感知器（perceptrons）：
$$
\lbrace x:\hat\beta_0 + \hat\beta_1x_1 + \hat\beta_2x_2 = 0\rbrace
$$
perceptron是neural network的基础。

一些线性代数的基础：

假设存在超平面$L$，由函数$f(x) = \beta_0 + \beta^Tx=0$组成，则有如下结论：

1. 对于$L$上的任意两个点$x_1, x_2$都有：$\beta^T(x_1-x_2) = 0$，因此$\beta^T$垂直$L$，且其单位向量为：$\beta^* = \beta/||\beta||$
2. 对$L$上任意一点$x_0$都有：$\beta^Tx_0 = \beta_0$
3. 任一点（包括不在$L$上的点）$x$到超平面$L$的有向距离是：$\beta^{*T}(x-x_0) = {1\over||\beta||}(\beta^Tx+\beta_0)={1\over||f^\prime(x)||}f(x)$

#### Rosenblatt的感知器学习算法

感知器是Rosenblatt在1958年发布工程文献，感知器学习算法尝试寻找一个分离超平面，来最小化误分类点到决策边界的距离。假设类$y_i=1$被误分类，那么$x_i^T\beta+\beta_0<0$，反之$y_i=-1$被误分类时其值大于0，所以等价为求下面公式的最小值：
$$
D(\beta, \beta_0)=-\sum_{i\in M}y_i(x_i^T\beta + \beta_0),M是误分类点的索引
$$
$D$的值非负，而且和误分类点到决策边界的距离成正比，对参数$\beta, \beta_0$求偏导如下：
$$
{\partial D(\beta,\beta_0)\over\partial\beta} = -\sum_{i\in M}y_ix_i，{\partial D(\beta, \beta_0)\over\partial\beta_0}=-\sum_{i\in M}y_i
$$
通过随机梯度下降方法（stochastic gradient descent），更新参数有：
$$
\binom{\beta}{\beta_0}\gets\binom{\beta}{\beta_0} + \rho\binom{y_ix_i}{y_i}
$$
因为求最小值，所以是反向梯度，和梯度的负号刚好抵消。

这个方法的一些问题：

* 当数据本身就是分散时，得到的结果可能不唯一，超平面的参数取决于选取的初始值
* 迭代的次数可能很大，步长$\rho$越小，则耗时越长
* 数据如果不是分散的，算法则会不收敛，迭代有可能在一些值之间震荡（循环），而且不易检测（由于震荡时间长？）

解决第一个问题的方案是通常对超平面做出一些特定的限制，从而达到唯一性。

第二个问题通常可以通过寻找不在原始输入空间的超平面来解决，通过创建原始变量的许多基函数变换而获得的大得多的空间。

#### 最优分类超平面（Optimal Separating Hyperplanes）

