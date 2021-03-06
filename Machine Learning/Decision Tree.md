#Decision Tree
_部分内容参考李航老师的《统计学习方法》_    
决策树的关键点分为三个：   

1. 特征选择
2. 决策树的生成
3. 决策树的修剪

上面三个关键点的不同，造就了决策树的几个不同的算法，ID3、C4.5、CART。

决策树模型用于对数据进行分类的属性结构，包括节点和有向边，结点分为内部结点和叶节点。    
从根节点开始选择一个特征值进行分类，然后将分类后数据传向下一个结点，然后子节点再选择一个特征进行分类，如果在某个结点，所有数据都属于同一类，则此节点为叶节点。    

对于决策树的理解：
一方面，可以将决策树看做一系列if-then规则的集合，由决策树的根节点到叶结点的每一条路径构建一条规则，路径上内部结点的特征对应规则的条件，而叶结点对应规则的结论。所以的if-then集合有个特点：互斥且完备，既可以覆盖所有的数据，同一条数据又不会匹配多条路径。     
一方面，决策树也表示给定条件下类的条件概率分布。条件概率定义在特征空间的一个划分上，特征空间划分成互不相交的单元或区域，并在每个单元定义一个类的概率分布就构成了一个条件概率分布，决策树的一条路径对应于划分的一个单元。

##特征选择
特征选择在于选取对训练数据有分类能力的特征，这样可以提高决策树学习效率，如何选取特征则通常通过信息增益或信息增益比来选取。
###信息增益
__熵__:熵表示随机变量不确定性的度量，设X是一个取有限个值的__随机__离散变量，其概率分布为：
$P(X=x_i) = p_i, i=1,2,3...n$
则随机变量X的__熵__定义为：
$H(X) = -\sum_{i=1}^n p_i\log{p_i}$
熵越大，则随机变量的不确定性越大。    
__条件熵__:随机变量X给定条件下的随机变量Y的条件熵H(Y|X)，定义为X给定条件下Y的条件概率分布的熵对X的数据期望。
$H(Y|X)=\sum_{i=1}^n p_iH(Y|X=x_i), p_i=P(X=x_i)即X的各个分类在数据集中占比, i=1,2,...,n$

__信息增益__:特征A对训练数据集D的信息增益g(D,A)，定义为集合D的熵H(D)与特征Ａ给定条件下Ｄ的条件熵H(D|A)之差，即：g(D,A)=H(D)-H(D|A),一般熵与条件熵之间差称为互信息（mutual information）    
####几个公式：
$说明: D是数据集，D_i是又特征A的不同值分成的数据集，|D|表示数据集D的个数，D_{ik}表示数据集D\\\ 的A特征的值是A的第i个值，并且分类是C_k的数据集。C_k表示分类是k的数据集   $
__经验熵：__ $H(D)=-\sum_{k=1}^K{|C_k|\over|D|}log_2{|C_k|\over|D|}$
__特征A对数据集D的经验熵H(D|A):__    
$H(D|A)=\sum_{i=1}^n {|D_i|\over|D|}H(D_i)=-\sum_{i=1}^n {|D_i|\over|D|}\sum_{k=1}^K{|D_{ik}|\over|D_i|}log_2{|D_{ik}|\over|D_i|}$
      
__<font color = 'red'>注意：如果把决策树算法作为boost算法的基础算法时，在计算熵值中的概率时，可以考虑每个数据在概率计算中的概率是通过权值计算（默认是1，即频数计算）</font>__

###信息增益比
由于信息增益的大小并不能很有效的反应出来特征的一个有效性，因为原始特征值大了，相对信息增益就打，否则就小。所以大小是相对训练数据集而言，而信息增益比可以对这一问题矫正，也是选择特征值的另一个准则：
特征A对训练数据集D的信息增益比:
$g_r(D,A)={g(D,A)\over H(D)}$

##决策树生成
下面介绍ID3和C4.5的生成算法
###ID3算法
ID3算法核心是在决策树各个节点上应用信息增益准则选择特征值，递归构建决策树。    
具体方法：从根节点开始，从各个特征中选择一个信息增益最大的特征作为节点的特征，由该特征的不同取值建立子节点，递归调用次方法，直到信息增益很小或者没有特征可以选择为止。    
__算法介绍：__   
_输入_：训练数据集D，特征集A，阈值e；    
_输出_：决策树T    
_过程_：

1. 如果D所有实例属于同一类C或A为空，则D归为类C或D中类占比最大的类；
2. 否则，按照信息增益计算方式对各个特征计算信息增益，选择信息增益最大特征Ai，如果Ai小于阈值e，则分类结果通A为空；
3. 否则，对Ai的每一个可能值将D分割为子集Di，构建子节点（可以同时将Di中最大的类标记为节点的类别）；
4. 对此节点，以Di为训练树，以A-{Ai}为特征集，递归调用1~3步。

###C4.5算法
C4.5和ID3算法类似，C4.5算法对ID3算法进行改进。C4.5在生成的过程中，用信息增益比来选择特征。
步骤参考ID3

##决策树剪枝
决策树在进行构建时，直到不能继续下去，这样对测试集可能精确度比较高，但是容易产生过拟合现象。过拟合原因是在于学习过程中过多地考虑如何提高训练数据的正确分类，从而构建出过于复杂的决策树。通过决策树剪枝可以将一些叶结点减掉，把一些内部结点变成叶结点。从而简化决策树结构。    
决策树剪枝通常通过极小化决策树整体的损失函数或代价函数来实现，决策树的损失函数：
$
C_a(T) = \sum_{t=1}^{|T|}N_tH_t(T)+a|T|\\\
熵H_t(T)=-\sum_k{N_{tk}\over N_t}log{N_{tk}\over N_t}, N_{tk}是叶节点t属于k类的数据个数\\\
a|T|中，a参数，|T|表示模型复杂度，a较大则选择复杂度比较低的树，a较小则选择复杂度比较高的树。
$    
计算所有节点的熵（为什么计算所有的呢？因为要比较减树之前和之后的熵值，所以统一计算比较好），然后计算减掉某个叶子之后的损失函数值Cafter和之前的Cbefore，如果Cafter<=Cbefore，则进行减树操作，然后迭代计算，直到得到损失函数最小子树。    
###CART算法
CART：classification and regression tree，分类会归树    
CART是在给定输入随机变量X条件下输出随机变量Y的条件概率分布的学习方法。    
CART的区别就是构建一个二叉决策树，按照基尼指数找到各个特征最佳的分类点，作为二叉树分类，然后递归进行构建。所以可以作为对具有连续值的特征进行分类的算法，所以也可以作为回归算法。    
__基尼指数__:
$
Gini(p)=\sum_{k=1}^K p_k(1-p_k)=1-\sum_{k=1}^K p_k^2, K为类别个数，p_k为属于第k类的概率\\\
由于CART是二分树，所以K=2时，Gini(p)=2p(1-p)
$
