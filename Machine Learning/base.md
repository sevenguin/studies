## 统计学习方法

监督学习：给定的有限的训练数据集合中，假设数据是独立同分布产生的，并且假设要学习的模型属于某个函数的集合，称为假设空间，应用某个评价标准，从假设空间中选取一个最优的模型，使他对已知训练数据以及未知测试数据在给定的评价标准下有最优的预测。所以模型主要包括：假设空间，模型选择的准则以及模型学习的算法

统计学习三要素：方法= 模型+策略+算法

* 模型：模型就是要学习的决策函数或概率分布，模型的假设空间包括所有可能取值的决策函数或概率分布

* 策略：在确定了模型的假设空间，则需要考虑按照什么样的准则和方法选择最优模型。

  * 损失函数和风险函数：用损失函数来度量预测错误的程度，损失函数是f(X)和Y的非负实值函数，记作L(Y,f(X))，常用的损失函数：

    * 0-1损失函数：$L(Y,f(X))=1\ if\ Y\ne f(X) else 0$
    * 平方损失函数：$L(Y, f(X)) = (Y - f(X))^2$
    * 绝对损失函数：$L(Y, f(X)) = |Y - f(X)|$
    * 对数损失函数：$L(Y, f(X)) = -\log P(Y|X)$

    损失函数的期望是：
    $$
    R_{exp}(f)=E_p[L(Y, f(X))] = \int_{x\times y}L(y, f(x))P(x,y)dxdy
    $$
    称之为风险函数或期望损失。

    一般通过对训练数据集的经验风险来估计损失函数期望（因为X和Y的联合分布未知），经验风险如下：
    $$
    R_{emp} = {1\over N}\sum_{i=1}^NL(y_i, f(x_i))
    $$

  * 经验风险最小化与结构风险最小化：如果数据量不足，经验封校最小化可能会导致过拟合，结构化风险就是为了防止过拟合而提出的策略，结构风险最小化等价于正则化。结构化风险在经验风险上增加模型复杂度的正则化或罚项。结构风险的定义是：
    $$
    R_srm = {1\over N}\sum_{i=1}^NL(y_i, f(x_i)) + \lambda J(f)
    $$

* 算法：算法是指学习模型具体计算方法，基本就是最优化问题的算法。

### 模型评估与模型选择

训练误差：训练数据中产生的误差；测试误差：测试数据时产生的误差。

两者都是通过计算经验风险来评估，只是两者计算的样本容量不同。

### 正则化与交叉验证

#### 正则化

模型选择的典型方法就是正则化，正则化是结构风险最小化策略的实现。正则化一般形式如下：
$$
min_{f\in F}{1\over N}\sum_{i =1}^N L(y_i, f(x_i)) + \lambda J(f)
$$
其中$J(f)$可以是$L_2$范数，或$L_1$范式。

#### 交叉验证

随机将数据切分成三部分：训练集、验证集合测试集，训练集用来训练模型，验证集用来进行模型选择，测试集用来对最终学习方法进行评估。

* 简单交叉验证：只分为训练集和测试集，选出测试集上测试误差较小的模型
* S折交叉验证：将数据随机分为S个互相交大小相同的数据集，然后利用S-1个数据训练数据，利用余下的子集测试模型，将这种方式进行S次，选择模型中平均误差较小的。
* 留一交叉验证：S折交叉验证的特殊情况，S=N

### 泛化能力

泛化能力是指学习模型在未知数据上预测的能力，一般使用测试误差来进行评估。泛化误差（generalization error）就是把经验误差中的f替换成$\hat f$——学习到的模型。

泛化误差上界：

对二类问题，当假设空间是有限个函数的集合：$F={f_1, f_2, ..., f_d}$，对于任意$f\in F$， 至少以概率$1 - \delta$，以下不等式成立：
$$
R(f) \le \hat R(f) + \epsilon(d, N, \delta)，其中\epsilon(d, N, \delta)=\sqrt{{1\over 2N}(\log d + \log{1\over \delta})}
$$

### 生成模型和判别模型

生成模型（generative model）通过学习联合概率分布$P(X,Y)$，然后求出条件概率分布$P(Y|X)$，即生成模型：$P(Y|X)={P(X,Y)\over P(X)}$，之所以叫生成模型应为模型表示了给定输入X和给定输出Y的生成关系，典型的生成模型有：朴素贝叶斯和隐形马尔科夫模型。

生成模型的的特点：

* 学习收敛速度快
* 计算出X,Y联合分布
* 当存在隐变量时，生成方法仍然可用

判别模型（discriminative model）直接学习决策函数$f(X)$或$P(Y|X)$为预测模型。

判别模型的特点：

* 直接得到决策函数，往往准确率较高
* 由于直接学习，所以可以对数据进行各种程度上的抽象

### 分类、标注、回归问题

#### 分类问题

这里主要说明一下评价分类性能的指标：

* 分类准确率（accuracy）：正确分类的样本数与总样本数之比
* 精确率（precision）和召回率（recall）：对于二类问题使用，将类别分为正类和负类两个，精确率为：$P={TP\over TP+FP}$，召回率：$R = {TP\over TP+FN}$，TP是正类分为正类；FP是负类分为正类；FN是正类分为负类；TN是负类分为负类。
* $F_1$值：精确率和召回率的调和均值，即：${2\over F_1}={1\over P} + {1\over R}，F_1={2TP\over 2TP+FP+FN}$。

#### 标注问题

标注问题和分类问题相似，但是更复杂，标注问题的输入是一个观测序列，输出是一个标记序列或状态序列。标注问题的目标在于学习一个模型，使它能够对观测序列给出标记序列作为预测。

例如对语句进行分词、提取信息等。标注常用的统计学习方法有：隐形马尔科夫模型，条件随机场。

#### 回归问题

回归模型是表示输入变量到输出变量之间的映射的函数，回归问题等价于函数拟合，选择一条函数曲线使其很好的拟合已知数据且很好的拟合未知数据。




## 模型评估

### 线性回归模型

#### $R^2$score, the coefficient of determination

 [coefficient of determination](https://en.wikipedia.org/wiki/Coefficient_of_determination)：决策系数，是一个数字，可以从自变量预测的因变量中的方差的比例的数字。即回归平方和（SSR）在总变差（SST）中占的比重，可以作为综合度量回归模型对样本观测值拟合优度的度量指标。说明解释变量对因变量的解释程度，可以用来判断线性回归的拟合效果，取值[0,1]。一般表示为$R^2, r^2$。
$$
R^2(y,\hat y) = 1 - {\sum_{i=0}^{n-1}(y_i - \hat y_i)^2\over \sum_{i=0}^{n-1}(y_i - \overline y)^2}，n是样本数，后面那一项表示总残差平方和占离差平方和的比例，越小说明拟合越好
$$
和相关系数一样，度量两个变量之间的关系，但是两者之间还是有些差别。

相关系数（r）用来度量__定距变量__间的线性相关性，反映了两个变量线性关系的方向和密切程度，没有单位。取值范围为[-1,1]，其却对值越大，则说明两个变量线性关系越好，反之线性关系越差或不存在，正号表示正相关，符号表示负相关。
$$
r={\sum_{i=1}^n(x_i -\overline x) (y_i - \overline y)\over \sqrt{\sum_{i=1}^n(x_i - \overline x)^2\sum_{i=1}(y_i - \overline y)^2}}
$$


定距变量：统计学依据数据的计量尺度将数据划分为四大类，即定距型数据（Interval Scale）、定序型数据（Ordinal Scale）、定类型数据（Nominal Scale）和定比型数据 (Ratio Scale)。定距型数据是数字型变量，可以求加减平均值等，但不存在基准0值，即当变量值为0时不是表示没有，如温度变量，当温度为0时，并不是表示没有温度，这样温度就为定距变量，而不是定比变量；定序型数据具有内在固有大小或高低顺序，但它又不同于定距型数据，一般可以数值或字符表示。如职称变量可以有低级、中级和高级三个取值，可以分别用1、2、3等表示，年龄段变量可以有老、中、青三个取值，分别用A、B、C表示等。摘自[百度百科](http://baike.baidu.com/link?url=mGAnoReZOlx5oH8_wGkQu25FAft9LSO4vQLid74gEFclL1cfSA3KLacH-wrrzJjLDdmvzU8hdTz5SkfBwRpt_gVhdFTauYjivZkkfVmE2WF90B8bnYqsgdkcvN8iZqQ6)。

可以根据相关程度判定是否进行回归分析，相关系数度量变量之间的线性关系的强弱程度或共变趋势。

scikit-learn库中`sklearn.metrics.r2_score`计算$R^2$。



### 模型评价标准

一般使用评价标准有logloss、accuracy、precision和AUC等，AUC和logloss比accuracy更常用，因为很多机器学习算法的预测都是分类结果是概率，如果要计算accuracy，则需要选择一个阈值，把概率转化成类别（大于阈值则为1或0等），而其他两个可以避免这个问题。下面详细介绍。

一个模型的效果如何一般可以通过测试集和训练集来评估，或者使用一些交叉验证、或者集成方法来评估。不同的模型有不同的评估方法，一般来说：

* 分类模型：精确度、反向误差、f-measure或者macro-average
* 概率分类：logloss、正确分类比例、MSE（mean squared error）、Brier‘s score、ROC、AUC
* 回归模型：MSE或MAE（mean absolute error）

一般通过对模型整体的观察和描述，可以得到一些方法来改进模型的准确度或置信度。而Calibration可以做到这两点。

#### ROC曲线

receiver operating characteristic，接收者操作特征，ROC曲线每个点反应对同一信号刺激的感受性。

X轴为伪阳率（false positive）值为$NP\over NP+TN$，Y轴为真阳率（true positive），值为$TP\over TP + FN$，对于二类分类问题有（两类为0(N-阴)，1(P-阳)），横轴为真实类别，纵轴为预测类别：

|       | 1(P)   | 0(N)   |
| ----- | ------ | ------ |
| 1(P') | TP（真阳） | NP（伪阳） |
| 0(N') | FN（伪阴） | TN（真阴） |

假如分类算法得到了分类结果，是一系列概率，则从0到1，逐个选择值作为阈值，每次选择一个都可以计算其伪阳率、真阳率，则这得到x,y坐标值，选择足够多的阈值，则可以画出一条曲线，则此曲线为Roc。（可以设阈值为t，则x=f(t)，y=g(t)）。

#### AUC

Area under Curve：Roc曲线下的面积，介于0.1到1之间。Auc可以作为数值直观评价分类器的好坏，值越大越好。

AUC的意义：如果从定义来理解AUC的含义，比较困难，实际上AUC和Mann–Whitney+U+test有密切的联系，我会在第三部说明。从Mann–Whitney+U+statistic的角度来解释，AUC就是从所有1样本中随机选取一个样本，+从所有0样本中随机选取一个样本，然后根据你的分类器对两个随机样本进行预测，把1样本预测为1的概率为p1，把0样本预测为1的概率为p0，p1>p0的概率就等于AUC。所以AUC反应的是分类器对样本的排序能力。根据这个解释，如果我们完全随机的对样本分类，那么AUC应该接近0.5。另外值得注意的是，AUC对样本类别是否均衡并不敏感，这也是不均衡样本通常用AUC评价分类器性能的一个原因。&oq=如果从定义来理解AUC的含义，比较困难，实际上AUC和Mann–Whitney+U+test有密切的联系，我会在第三部说明。从Mann–Whitney+U+statistic的角度来解释，AUC就是从所有1样本中随机选取一个样本，+从所有0样本中随机选取一个样本，然后根据你的分类器对两个随机样本进行预测，把1样本预测为1的概率为p1，把0样本预测为1的概率为p0，p1>p0的概率就等于AUC。所以AUC反应的是分类器对样本的排序能力。根据这个解释，如果我们完全随机的对样本分类，那么AUC应该接近0.5。另外值得注意的是，AUC对样本类别是否均衡并不敏感，这也是不均衡样本通常用AUC评价分类器性能的一个原因。

部分参考：[李小猫](https://www.zhihu.com/question/39840928?from=profile_question_card)回答。

### Calibration

Calibration一般应用于解决两个问题：

* how error is distributed：错误如何分布
* how self-assessment（confidence or probability estimation）is performed：如何进行自我评估（通过概率估计或者置信度）

给一个一般的校准技术，我们可以将其应用到任何现存的机器学习方法中。依据不同的任务使用不同的校准（Calibration）技术，同时也就有了对其更精准的定义。下面介绍一些最常用的校准技术（包括type code）：

* __Type CD：__Calibration techniques for __discrete classification__("(class) distribution calibration in classification" or simply "class calibration")，一个典型的校正发生在这样的情况下——预测出来的分类占比和原始的分类占比不同。例如：有类别A和B，原始问题中A和B的比例为95%和5%，但是预测结果中A类为99%，B类为1%。因此，类校正（class calibration）被定义为——真实或按照经验的类分布和预测类分布的近似程度。这个情况下一个标准的做法是，调整阈值，让A和B的比例靠近真实值，但是需要注意的是这种方法可能会导致更多的误分类。通常我们只对整体的占比感兴趣，但是校正可以对局部的学习和使用。
* __Type CP：__Calibration techniques for __probabilistic classification__（probabilitic calibration for classification），概率分类一般会伴随着预测的概率。如果我们预测某一分类的可能性是99%，那我们期望正确率应该就是99%，如果实际上仅仅只有50%的正确率，则这个是没有被校准，因为过于乐观。反之亦然，这两种情况，期望的值和实际值不匹配。这种情况下，校准的定义就是实际概率和预测概率的近似程度。一般好的校准意味着对不同的例子的估计概率不同。对于一些情况置信度比较高，对于一些难度较大的则置信度较低。这意味着，这种类型的校准的度量方式是——通过数据分区以局部方式评估期望值和实际值之间的一致性。（因为不同的数据有不同的校准值？）
* __Type RD：__Calibration techniques to fix error __distribution for regression__('distribution calibration in regression')，期望值应该接近于实际值，有几种方法评估——假设预估值为y'，实际值为y，则E(y')=E(y)，或E(y'-y)=0或E(y'y)=1。通常，通过用于评估回归模型的典型措施来检测和惩罚这些问题，并且许多技术（例如线性回归），生成校准模型。
* __Type RP：__Calibration techniques to improve __probability estimation for regression__ ('probabilistic calibration for regression')，这是相对比较新的领域，当连续预测伴随着一个概率密度函数，则可用。这种回归模型通常被称为密度预测模型。例如：不同于告诉你一个准确的值——预测明天温度是23.2℃，而是给一个概率密度函数，这个函数可以计算温度在21°-25°的概率是0.9，温度在15°-30°的概率是0.99。如果我们预测的很准，则密度函数应该比较窄（置信区间），如果我们预测的很差，则密度函数可能会很宽。类似于Type CP，一个好的校准通常需要每一个预测的密度函数是特定的，例如：对于一些例子当置信度比较高时，密度函数较窄，反之较宽。和Type CP类似，这种类型的校准的度量方式是——通过数据分区以局部方式评估期望值和实际值之间的一致性。

对于这四类问题的总结：

| TYPE | Task           | Problem               | Global/Local    | What is calibrated?    |
| ---- | -------------- | --------------------- | --------------- | ---------------------- |
| CD   | Classification | 期望类分布和实际的类分布不同（占比）    | Global or Local | Predictions            |
| CP   | Classification | 期望或估计的概率和实际的概率不一致     | Local           | Probability/confidence |
| RD   | Regression     | 期望输出和实际平均输出不一致        | Global or Local | Predictions            |
| RP   | Regression     | 期望的错误置信区间或概率密度函数太宽或太窄 | Local           | Probability/confidence |

需要注意的是，CD和RD的校准都需要修改预测结果（CD调整阈值影像，RD对预测值调大或调小），而CP和RP，由于只是修正Confidence，对实际的预测结果可能根本不会产生影响。所以，像平均误差这种度量方式不会受到这两个校准的影响。

校准测量是任何能够对校准程度做定量评定的测量方法，很多经典的质量评定方法对校准技术都不太有用，实际上，一些新的或特殊的测量方法被用来评估校准效果，特别是对CP和RP，下面是校准测量方法对每一个校准问题：

| TYPE |           Calibration measures           | Partially sensitive measures  |           Insensitive measures           |
| :--: | :--------------------------------------: | :---------------------------: | :--------------------------------------: |
|  CD  | Macro-averaged accuracy, proportion accuracy, proportion | Accuracy, mean F-measure, ... | Area Under the ROC Curve (AUC), MSEp,Logloss, ... |
|  CP  |      MSEp, LogLoss,CalBin, CalLoss       |                               |    AUC, Accuracy, mean F-measure, ...    |
|  RD  |       Average error,Relative error       |        MSEr, MAE, ...         |                                          |
|  RP  |        Anderson-Darling (A2) test        |                               | Average error, relative error, MSEr, MAE, ... |

假设存在数据集$T$，$n$表示数据集样本个数，$C$表示类的个数，$f(i,j)$表示实际情况下样本$i$对应的类别是$j$的概率，这里我们假设$f(i,j)$总是取值$\lbrace 0, 1\rbrace$，是严格的指标函数而不是概率。$n_j=\sum_{i=1}^nf(i,j)$，表示类$j$的个数。$p(j)$表示类$j$的先验概率，即：$p(j)=n_j/n$，给一个分类器，$p(i,j)$表示样本$i$属于类$j$的__预测__概率，取值案范围为$[0,1]$。

根据上面的假设和符号，下面针对上面的几个Calibration measures进行说明：

##### Mean Squared Error

MSE用来度量与真值的偏差率，有时候使用$MSE^p$来区别回归中的MSE，它定义为：
$$
MSE=\sum_{j=1}^C\sum_{i=1}^n{(f(i,j) - p(i,j))^2\over n\times C}={1\over n\times C}\sum_{j=1}^C\sum_{i=1}^n(f(i,j) - p(i,j))^2
$$
原始的MSE并不是一个校准测量方法，之后在校准损失和精化损失方面被分解。分解的一个重要思想是将数据组织成仓（bin），并且将每个仓中观察到的概率与预测概率或全局概率进行比较。在分解中，数据集$T$被分为$k$个仓（bins）：
$$
MSE={1\over n\times C}{\sum_{j=1}^C\sum_{l=1}^k\sum_{i=1,i\in l}^{n_l}n_l\times(p(i,j)-\overline f(i,j))^2 - \sum_{l=1}^kn_l\times(\overline f_l(i,j) -\overline f(j)) + \overline f(j) \times(1-\overline f(j))}
$$
其中：$\overline f_l(i,j)=\sum_{i=1, i=l}^{n_l}{f(i,j)\over{n_l}}，\overline f(j)=\sum_{i=1}^n{f(i,j)\over n}$。

##### LogLoss

$$
Logloss = \sum_{j=1}^C\sum_{i=1}^n{f(i,j) - \log p(i,j)\over n}
$$

##### CalBin

Calibration by Overlapping Bins：

> One typical way of measuring classifier calibration is that the test set must be split into several segments or bins, as the MSE decomposition shows (although MSE does not need to use bins to be computed). The problem of using bins is that if too few bins are defined, the real probabilities are not properly detailed to give an accurate evaluation. If too many bins are defined, the real probabilities are not properly estimated. A partial solution to this problem is to make the bins overlap.

A calibration measure based on overlapping binning is CalBin.

关于Calibration的详细说明见：[Calibration of Machine Learning Models](http://users.dsic.upv.es/~flip/papers/BFHRHandbook2010.pdf)。

#### Type CD的校准方法

在离散分类中，一个模型是否非校准的可以通过每一个类的数量来分析——具体通过混淆矩阵（confusion matrix）。混淆矩阵的列示real值，行时预测值，例如：有a,b,c三类

| predicted\real | a    | b    | c    |
| -------------- | ---- | ---- | ---- |
| a              | 20   | 2    | 3    |
| b              | 0    | 30   | 3    |
| c              | 0    | 2    | 40   |

实际值的比例a,b,c各位20,34,46，而预测的为25,33,42，比较一致，所以这个分类器是校准过的。（这个判断太ridiculous）
例如a,b比例为100,20,预测为62,58，则明显没有被校验。对于这种情况，可以考虑修改分割各个类的阈值来实现：

例如在朴素贝叶斯分类方法中，f(a|x)=0.3，f(b|x)=0.06，朴素贝叶斯的判断是如果f(a|x)>=f(b|x)则为a类否则为b类。这种分类可能会导致a类多分，所以可以考虑__估计__(注意这里的用词)一个阈值来调整分类结果。比如设$r=p(a|x)/p(b|x)$，这个比例范围为0到$$\infty$$，然后__估计__$r$值，设最优值为$u$，则$r>u$时取a类，否则为b类。

#### Type CP的校准方法

另一种情况是概率分类模型（CP类型）的校准，它需要更复杂的技术。 在这种情况下，目标是当模型预测类a的概率是0.99时，这意味着该模型更有信心该类是预测0.6时的类。确定预测的可靠性在许多应用中是最基本工作（诊断，实例选择和模型组合）。

可以通过reliability diagrams来分析模型是否校准，详见[Calibration of Machine Learning Models](http://users.dsic.upv.es/~flip/papers/BFHRHandbook2010.pdf)

有几种方法可以用来进行校准，下面介绍。

##### Bining Average

将测试样例中各个样例属于正类的概率进行排序，然后进行分段，新的预测变量先通过模型计算属于正类的概率，然后按照这个值找到所属于的bin中，然后修正后的概率为这个bin中所有概率的平均值。

#### Isotonic Regression(PAV)

PAV-pair-adjacent violators algorithm，相邻违反者算法。

这个算法必须满足 校准的概率必须是单调递减的序列，如：$p_1\ge p_2\ge p_3\ge...\ge p_n$,然后计算公式为：
$$
p^*(i,j)= {p(i, j) + p(i + 1, j)\over 2}
$$
这个过程不断的重复，直到得到一个isotonic set（有序集）

如果不满足单调递减序列，则PAV算法每次对于一对连续的不满足上面的递减的概率，将这一对的概率都替换成其这两个的均值，即：$p^*(i,j)=p^*(i+1, j) = {p(i, j) + p(i + 1, j)\over 2}$。

##### Platt's Method

Platt提出了一种使用Sigmoid的参数方法，将估计概率映射到校准概率。这个方法被开发用于对SVM（支持向量机）的输出做转换，将原始数据$[0-\infty，\infty]$转换为概率。当然也可以扩展到其他类型的模型。具体形式如下：
$$
p^*(i,j) = {1\over 1 + e^{A\times p(i,j) + B}}
$$
当预测概率的失真是呈现为sigmoid形式（误差分布？），Platt方法就很有效了。Isotonic Regression比较灵活，可以适用于任何单调失真。校准的效果可能依赖数据集大小，上述所有方法都可以使用训练集或附加验证集用于校准模型。

#### Type RD和Type RP的校准方法

Type RD一般在回归算法中就包含了类似校准的方式，如最小二乘中以偏差最小为策略来计算最优值。文档中没有详细的描述，不信就去看。



| bin  | instance | score |
| ---- | -------- | ----- |
| 1    |          |       |

