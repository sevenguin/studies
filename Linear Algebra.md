#Linear Algebra
##消元
矩阵消元和回代

矩阵乘以向量的结果是矩阵列的线性组合

分别用行和列进行矩阵操作——核心

初等矩阵：对某个元素消除（E-表示，I表示单位矩阵）

置换矩阵：交换矩阵的行或列，置换矩阵在目标矩阵左边则是行置换；右边则是列置换

矩阵相乘，第一个矩阵的行乘以第二个矩阵的列，生成的元素位置就是[第一个矩阵的行号，第二个矩阵的列号]

E*A=U  A变换成U

U->A 逆变换

##矩阵计算
###矩阵乘法
结合满足；交换不满足  
两个矩阵相乘，可以看做是前面的矩阵和后面的矩阵的每列表示的向量做乘积，这样就可以和之前的线性方程连接起来，C中的每一列等价于A中的各列的线性组合（A*B=C）  
四中方法：

* 第一个矩阵行乘以第二个矩阵的列——传统的计算方法，C第i行第j列的元素值是A矩阵第i行点成B矩阵第j列求和得到的值
* 第一个矩阵的列乘以第二个矩阵的行（列一乘以行一，列二乘以行二，组成矩阵相加），做列的线性组合，A分别乘以B的每一列，B的每一列都能看做是A的列的线性组合
* 看做行的线性组合，A的每一行分别乘以B，A的每一行看做B的行的线性组合
* 列*行，A的第i列乘以B的第i行，组成的矩阵相加得到最后结果（行向量和列向量都是单个向量的线性组合）

第五种：分块计算

###逆（Inverses）
存在左逆和右逆，左逆*矩阵=单位矩阵；  
矩阵可逆的情况

奇异矩阵(sigular matrices)：没有逆矩阵，可以通过非0向量计算得到0向量

Gauss-Jordan：同时处理两个方程组。（对[AI]组合成的长矩阵做行消元处理（做行消元主要是是因为看做线性方程的增广矩阵，线性方程都是通过行叠加来消元处理）——》E[AI]=[EA EI]

A的转置的逆等于A的逆的转置
增广矩阵：右边向量加到左边矩阵中

###置换矩阵
行行互换（确保主元不为0）

置换矩阵：是行重新排列了的单位矩阵

对称矩阵：A的转置等于A，则A是对称矩阵，A的转置矩阵*A=对称矩阵

###向量空间
空间：一整个空间的向量，而且这些向量必须能够进行线性组合（进行加减乘除，而且运算完之后也属于这个向量空间）。空间也不一定包含所有向量，可能就只包含一类向量——例如穿过原点的一个向量。     
例如：R*R二维向量，穿过0的直线子空间；只有0点也是一个向量空间；R\*R整个也是向量空间;其实就是降维（直线就类似一维）    
矩阵构成向量空间：列向量组成的叫做列空间，这些列线性组合构成了一个Rn的子空间

向量空间：就是一些向量，对一些运算封闭内任何两向量相加（加法）结果仍然在空间内（或用空间内任意向量乘以数也是封闭的）——线性组合是封闭的     
A的列空间由所有列的线性组合构成

Ax=b有解，b应该属于A的列空间；pivot column：主列，A中表示列空间不能被剔除的列（不和其他列线性表达共线的列）    
Ax=b solvability（可解）——condition on b when b is column space of A

列空间和0空间，使用向量空间的思维方式来思考AX=b.  

A的秩表示A的主元的个数（消元法之后，每一行存在非零元素行的个数）     
零空间矩阵，由特解组成了矩阵的列（特解就是自由变量赋值为0或1，然后回带求出pivot 元（主元）得到的解得向量）;零空间就是Ax=0 x所有的取值（即所有解，如果A可逆，那x就是0向量）     
特解：自由变量全为0，然后带回方程计算出主元    
Ax=b的解为特解+零空间的列向量（多个就多个，然后这些列向量可以带上线性参数）    
几种情况，矩阵的秩决定了方程组解的数目：

* r=n<m(列满秩，解为0或1个)
* r=n=m(满秩， 肯定有解，一个)
* r=m<n(行满秩，解为一个或无穷个)
* r<m, r<n(解为0个或无穷个（可能存在某些行为0，而b不为0，则这种情况下无解）)

向量线性无关：不存在非零解得Ax=0，则A中的列向量线性无关。A的零空间的子空间只有[0]矩阵。，这个向量组合的秩是n

V1~Vn个向量生成一个**空间**的意思是，这个空间包含这些向量所有的线性组合（这个可能是Rn的子空间，下面的基向量是生成Rn空间，如果V1~Vn线性相关，则生成的只是子空间，肯定有n个维度的空间无法生成）    
向量空间的一组基是指：一系列向量（V1~Vd）,这向量有两个特性，他们是线性无关的；他们生成整个空间。同时具有这两个特性的向量组合数量需要刚刚好。如果需要确定一个子空间，你把子空间的基给我，等于告诉我这个子空间的全部有用信息。只需要进行组合，找到其所有的线性组合就行了（三维空间中的一个基就是单位向量的列向量组，单位向量是线性无关的，也可以表示整个空间，*但是找到其他线性组合是怎么回事？ *）   ‘
基不是唯一的，所有基的向量个数都相同，表示有多少空间。这个向量的数称为维度   
如果矩阵A有逆，则其列向量肯定是非相关的，因为Ax=0，两边都乘以A的逆，则会有x=0，则A的列向量肯定非相关    
线性无关：着眼于线性组合不为0；生成：着眼于所有的线性组合；   
基：一组线性无关的向量，并生成空间；维度：表示基向量的个数（几个基向量能生成空间）    
矩阵的列向量的基向量，可以从列向量中挑选一部分线性无关的列向量来生成空间    
A的秩-》rank(A)=number of pivot columns=dimiemnsion of the C(A)->A的列空间的维数。    
一个矩阵，如果线性相关，就会损失一部分信息。A的列空间就是由线性不相关的列向量生成    
零空间的维数是自由变量的个数，即：n-r（r是矩阵的秩，n是矩阵的列数）    

标准基：单位向量也是一种基向量    
Ax=b的解，x=自由变量全取0得到的解向量 + 零空间（第一个因子没有参数，后面零空间的每一个向量都有一个参数，因为A*零空间向量的结果为0，所以分配率下来，零空间向量的任意倍数都是0，所以解就有无数多个。这个和导数求原函数经常加一个常量C一样，常量求导为0，所以导数为0的常量有无数个）
###四个基本子空间
* 列空间
* 零空间（null space）
* 行空间：行向量形成了行空间
* A转置矩阵的零空间（A的左零空间） 

行空间和列空间有相同的维度——r（A矩阵的秩）    
行变换会影响列空间（例如A矩阵最后一行和第一行线性相关，行变换会消除最后一行——即最后一行全为0，则变换后的基础矩阵列空间无法表 达A矩阵中最后一行不为0的列的向 量）

Symmetric mitrices(对称矩阵)；


###矩阵空间
矩阵空间的子空间：对称矩阵和上三角矩阵

加入是3*3的矩阵空间，对称空间和上三角矩阵这两个子空间的维度是6（因为只需要对角线和对角线上的三个数字就可以表达这个空间了，而原来的矩阵的维度是9）   
dim(S) + dim(U) = dim(S∩U) + dim(S+U) dim(S)表示的是S的维度

dim(C(A)) =  rank(A) = dim(C(A的转置)) C(A)表示的是A的列空间，rank(A)表示A的秩    
秩为1的矩阵就像是积木，可以构造出任何秩非1得矩阵。例如秩为3的矩阵可以由3个秩为1的矩阵构成     

###图
图是结点和边的集合，边连同各个结点    
线性代数的应用    
图对应的矩阵称为关联矩阵（incidence matrix），构造方法是，每一列表示一个node，每一行表示一条边，出的结点值为-1，入的结点值为1   
图的回路意味着关联矩阵中相应行的线性相关性   
关联矩阵源于问题，因此描述了问题的拓扑结构，而且关联矩阵也是稀疏的   

###正交(orthogonal)
A的转置*B=0，A和B正交
向量正交:正交是垂直的另一个说法

*子空间正交*:行空间和A转置的零空间正交--这两个子空间维数之和等于整个空间的维数（这就叫做n维空间里面的正交补，行空间（任何一个子空间）的正交补包含所有与之正交的向量，而不只是部分）；列空间和零空间也正交（正交两个子空间他们的维度之和等于空间维度）    

如何求解一个无解的方程组的解？    
不断去掉一些方程（找坏数据），达到解决很多方程中一些坏数据的方程，求得最优解。但这不是好方法，使用A的转置乘A来求解，这个很重要！    
N(A转置A)=N(A)? right，根据结合律，A*N(A)=0 ==> A转置AN(A)=0）     
对于矩阵、子空间的这些性质，多思考思考在算法中的应用

基正交     
###投影（projection）
b向量投影到a向量
投影由矩阵完成，所以投影就是，某个矩阵作用在b上面，使我们得到投影p，投影p是一个投影矩阵作用于随便的变量上。投影p就是一个投影矩阵作用于随便某个向量得到的矩阵。投影矩阵为a*a转置/a转置\*a   
性质    

1. 投影矩阵是对称矩阵    
2. 投影矩阵\*投影矩阵=投影矩阵(投影两次和投影一次结果相同，所以投影矩阵的平方和投影矩阵相同)
   
####投影的用处
在大量的实验中，为了求出参数A和未知变量的关系x的关系，通过监督学习方法，求解Ax=b，但是由于实验的误差或者本身数据线性相关的不完美性，可能这个式子无解，但是可以求出距离实际x最近的解，这时把b换成对A列空间的投影(这个投影属于A的列空间)，这个投影是最像b的一个能使得Ax有解的矩阵，求出的解x也就是一个近似值了。  
误差向量=b-投影得到的向量=b - A * X的最优解    
得到的投影矩阵是=A(A转置 * A)的逆A的转置b，由于投影到子空间，A是大部分情况是不可逆的矩阵，所以没法把中间展开，而A(A转置 * A)的逆A的转置就是投影矩阵    
最优解x=(A转置A)逆A转置b    
最小二乘法拟合就是这个的一个应用    

####正交基和正交矩阵
标准正交： `qi转置 * qj = 0（i≠j） or 1（i=j），qi、j为向量`，也就是一组向量中，两两正交（点成为0），自己跟自己点成为1    
一组正交向量组成矩阵A，`A转置*A=I`，这个按理也可以成为正交矩阵，但是只有当A为方阵的时候才将其称为正交矩阵，这时候A有点特殊——有逆矩阵，这样就可以根据上面的式子得到`A的转置=A的逆`    
阿德玛矩阵是一种只有1和-1的正交矩阵    
正交矩阵的好处是什么？它使哪些运算变得简单了？——看下节课    
x的修正值=Q转置*b    
$格拉姆-施密特（Graham-Schmidt）正交化法$
格拉姆：假设有线性无关的向量a/b/c，要求正交向量A/B/C，每个向量的单位向量就是该向量/向量的长度
格拉姆-施密特正交基：求上面三个向量的正交基，A=a；B=b-b在a上的投影；C=c-c在b上的投影-c在b上的投影    
A=QRs

####方阵的行列式以及特征值
行列式：detA = |A|，一个数告诉你这个矩阵是什么样的，行列式非0=矩阵可逆
性质：
性质需要分步使用

	1. detI = 1
	2. 如果你交换行列式的行，行列式的值的符号会相反
	3. 某一行乘以某个常数，则可以提取到行列式矩阵外面；简而言之：加法可以分解，乘法可以提取
	4. A的两行相等，detA=0
	5. 消元不改变行列式值
	6. detA=0 ，如果A是其一矩阵
	7. detA都能消元法转化成对角线元素的乘积（下三角或上三角都为0）
	8. detA=0,当且仅当A是奇异矩阵（Singular）
	9. detAB=detA * detB   =》det(A的逆)=1/detA
	10. A转置的行列式=A的行列式（所以行列式上对行成立的性质，对列都成立）
	
A=LU，L是下三角矩阵，U是上三角矩阵，L是A转换成U所做的操作
行列式无论多少次置换，符号都是可定义的（-1的置换次数方）

####行列式求解方法
代数余子式：i行j列元素a的代数余子式，除去，i行和j列剩余的元素，i+j为偶数，则代数余子式为正，否则为负（Cofactors）

A的逆=1/detA*(C的转置) C是代数余子式矩阵（C的第i,j位置就是A的i,j位置元素的代数余子式），C的转置一般称作伴随矩阵

克拉姆法则，由于Ax=b,x=A的逆*b=1/detA*(C的转置)*b--》C的转置*b就是一系列矩阵的行列式组成的向量，这些矩阵就是A的列j由b替换组成的新矩阵，设为Bj，xj=det(Bj)/det(Aj)

行列式的应用
行列式的值等于某几何体的体积。|detA|=n边形的面积（体积）（A为n边形的坐标）。如果这些点不是在原点，则A的n边形组成的矩阵加上一行全为1的行，这样，可以除第一行外其他行最后一个元素都化为0，而其他元素的值就是回到原点后的坐标。行列式算下来还是n-1个点组成的矩阵的行列式

####特征值和特征向量
Ax=λx：x是特征向量，λ是特征值
所有特征值的和=矩阵A的对角线元素和，这个值叫迹（trace）
Ax=λx -》(A-λI)x=0 ->A-λI奇异矩阵->det(A-λI)=0
矩阵其实就是用来乘以一个输入的向量，ML的模型中，大部分就是为了求的那个输入向量的最优解
特征值之和等于对角线元素之和；特征值之乘积等于对角线元素的乘积
将矩阵A的特征向量按列组成矩阵S，则S是特征向量矩阵。S的逆*A*S=Λ（S由A的n个线性无关的特征向量组成，Λ是由n个特征值组成的对角线矩阵）

##概念
主元：就是在矩阵消除中，每列要保留的非零元素，用他可以把列的其他元素消去

空间：某个线性组合的所有可能  
例如某个矩阵航空件，则是行所有可能的线性组合
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>
