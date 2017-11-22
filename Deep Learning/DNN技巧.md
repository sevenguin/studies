## DNN技巧

### 初始化参数

对于不同类型的激活函数，不同的初始化方法可以帮助更加快速的收敛。

| 激活函数                   | 均匀分布                                     | 正态分布（$\mu=0$）                            |
| ---------------------- | ---------------------------------------- | ---------------------------------------- |
| Logistic(sigmoid)      | $r=\sqrt{\frac 6 {n_{inputs} + n_{outputs}}}$ | $\sigma=\sqrt{\frac 2 {n_{inputs} + n_{outputs}}}$ |
| tang                   | $r=4\sqrt{\frac{6}{n_{inputs}+n_{outputs}}}$ | $\sigma=4\sqrt{\frac 2 {n_{inputs} + n_{outputs}}}$ |
| ReLU(and its variants) | $r=\sqrt{2}\sqrt{\frac 6 {n_{inputs} + n_{outputs}}}$ | $\sigma=\sqrt2\sqrt{\frac 2 {n_{inputs} + n_{outputs}}}$ |

### 不同激活函数

$ReLU=\max(0, z)$

$Leaky ReLU = \max(\alpha z, z),$ $\alpha $为超参，可能一般会设置为$0.01$

$ELU = \alpha(\exp(z) -1)，z<0；z，z\ge0$

$tanh =  2sigmoid(2z)-1$

$logistic = \frac{1}{1 + e^{-z}}$

$RReLU$公式和$LeakyReLU$一样，但是$\alpha$值在训练时是在一定范围内随机选择，测试时取一个平均值

$PReLU\to parametric\ leaky\ ReLU$，$\alpha$作为一个参数而不是超参，可以在反响传播时计算。

一般ELU>leakyReLU>ReLU>tanh>logistic，但是ELU计算比较慢，leakyReLU有超参。

#### Batch Normalization

[paper](https://goo.gl/gA4GSP)

其实就是对各个层进行归一化，效果还是比较明显（在mnist数据集上，两层300，100神经网络）

#### Gradient Clipping

梯度修剪，为了防止梯度爆炸，可以让梯度永远不要超过某个阈值。

对RNN 比较有效。



### Reusing Pretrained Layers

对于DNN，可以将之前任务的low layers的参数作迁移使用。

#### 重用TF模型

可以通过下面一段代码来将TF之前训练好的模型的1/2/3隐藏层拿来在新模型使用：

```python
init = tf.global_variables_initializer()
reuse_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES,
scope="hidden[123]")
reuse_vars_dict = dict([(var.name, var.name) for var in reuse_vars])
original_saver = tf.Saver(reuse_vars_dict) # saver to restore the original model
new_saver = tf.Saver() # saver to save the new model
with tf.Session() as sess:
    sess.run(init)
    original_saver.restore("./my_original_model.ckpt") # restore layers 1 to 3
    [...] # train the new model
    new_saver.save("./my_new_model.ckpt") # save the whole model
```

#### 重用其他库的模型

和初始化参数方法一样，也使用feed_dict，只要将其他库模型的参数读出来即可（例如Theano）

#### Freezing the Lower Layers

像CNN，按照对神经网络的理解，底层网络会检查出图片的特征，所以在训练时，可以线freezing较低层的layer，即不训练他们，给他们固定值（从其他网络迁移过来的），下面代码可以做到这件事：

```python
train_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, 			                                              scope="hidden[34]|outputs")
training_op = optimizer.minimize(loss, var_list=train_vars)
```

则只训练3/4隐藏层和输出层，1/2隐藏层被称作frozen layers。

在选择需要重用的层时，可以从最顶层开始一层一层去掉frozen，即frozen最开始是全部隐藏层，逐渐从顶层replace成自己用训练数据训练。如果训练数据较少，则可以先drop底层的隐藏层，然后再重复之前frozen层数的选择。每一次迭代都将这次结果和上次结果比对，看看有没有提升，有多少提升。

#### Model Zoos

将自己的模型保存并可以检索，这样可以容易的将以前的模型重用。

当然，也有公开的Model zoos，一些人将自己以前训练的模型结果公布，其他人可以根据这些模型的任务和自己任务的相似性，来选择是否可以迁移到自己的模型上。

tensorflow的modelzoo： https://github.com/tensorflow/models

caffe的model zoo：https://goo.gl/XI02X3

caffe和tf的转换代码：https://github.com/ethereon/caffe-tensorflow

#### 无监督预训练

这个可以使用__RBM和自编码__来处理，这两块内容了解后再看。

### 更快速的求最优解

有四个方面可以入手：

1. 选择一个好的初始化策略；
2. 使用一个好的激活函数；
3. 使用Batch Normalization（Dropout？）
4. 使用Pretrained network

还有就是选择更好的优化方法（相比传统的梯度下降）。最后的结果可能是无论什么时候都优先使用Adam（在mnist上测试，确实效果比梯度下降好很多）

#### Momentum

梯度下降方法是直接将梯度值作用于权重参数，Momentum引入了一个速度的概念（可以这么理解），对比一下两个：

梯度下降方法：$w\leftarrow w - \eta\nabla w$

Momentum：$m\leftarrow \beta m + \lambda\nabla w；w\leftarrow w - m$

引入的m就相当于速度，设想$\nabla w$如果一直沿着一个方向，那m会累加，相当于加速。将一次计算当作一个单位时间。但是如果m太大，则如果到了最低点附近可能会导致越过，所以增加一个超参数$\beta\in[0,1]$，相当于摩擦力。

根据上面的公式，可以得到m是有一个最终值（终极速度），这时有：
$$
m = \beta m + \lambda\nabla w\\
\rightarrow m*(1-\beta)=\lambda\nabla w\\
\rightarrow m = \frac{1}{1-\beta}*\lambda\nabla w
$$
如果梯度一直保持不便，则m最终值就可以求得。

#### Nesterov Accelerated Gradient

是Momentum的变体，计算方法如下：

1. $m\leftarrow \beta m + \eta\nabla_\theta J(\theta - \beta m)$
2. $w\leftarrow w - m$

相比Momentum，主要是$J$的求导位置不同，Momentum是在w的原始位置求导，而NAG是在下一个点的位置求导，其梯度方向更加接近最优值，所以效果会笔一般的Momentum更好。

#### AdaGrad

可以看作是对学习率的调节，可以自动调节学习率，根据迭代次数，学习率逐渐减小。因为我们在进行梯度下降计算的时候，最开始梯度较大时下降较快而快到最优点时希望梯度下降慢一点，一般可以通过学习率来调节。

算法：

1. $s\leftarrow s + \nabla_\theta J(\theta)\otimes\nabla_\theta J(\theta)$
2. $\theta \leftarrow \theta - \eta\nabla_\theta J(\theta)\oslash\sqrt{s + \epsilon}$

可以看到，s随着迭代和$\theta$数量的增加，值会越来越大，所以在比较复杂的算法中会出现提前终止的问题（因为梯度基本缩减为0），所以在深度学习中不建议使用，但是可以在线性回归等比较简单的算法中使用。

#### RMSprop

由于上述说明s增长太快，导致无法到达最优点就提前终止，RMSprop算是AdaGrad的改良方法。

算法：

1. $ s\leftarrow \beta s+(1-\beta)\nabla_\theta J(\theta)\otimes\nabla_\theta J(\theta)$
2. $\theta \leftarrow \theta - \eta\nabla_\theta J(\theta)\oslash\sqrt{s + \epsilon}$

通过$\beta$来控制只选择最接近本次的梯度（因为$\beta$指数乘积，所以离的远的迭代几乎不起作用），一般$\beta$默认值为0.9，虽然引入这个超参，但是暂时一般默认值已经能表现很好。

在Adam算法没出现之前，RMSprop是最优选择的优化算法。

```python
# tensorflow
optimizer = tf.train.RMSPropOptimizer(learning_rate=learning_rate, momentum=0.9, decay=0.9, epsilon=1e-10)
# momentum这个参数不知道有何用，因为在算法中没有看到有momentum，API中也没有说明
```

#### Adam

融合了RMSProp和Momentum算法，保留了Momentum对过去梯度的指数收缩，也像RMSProp一样只考虑最近的一些梯度。[paper](https://arxiv.org/pdf/1412.6980.pdf)

算法：

1. $m\leftarrow \beta_1 m + (1 - \beta_1)\nabla_\theta J(\theta)$
2. $s\leftarrow \beta_2 s + (1-\beta_2)\nabla_\theta J(\theta)\otimes\nabla_\theta J(\theta)$
3. $m_t\leftarrow \frac{m}{1 - \beta_1^t}$
4. $s_t\leftarrow \frac{s}{1 - \beta_2^t}$
5. $\theta \leftarrow \theta - \eta m\oslash\sqrt{s+\epsilon}$

不同与Momentum直接指数收缩，这里相当于算了一个平均值的指数收缩（把$\beta_1$）理解成概率。

$\beta_1=0.9, \beta_2=0.999, \epsilon=10^{-8}$，3/4两步主要是为了在最开始提升m和s（如果m和s在第一次初始化为0，则最开始几次值都在很靠近0）。

上面这些模型都是基于梯度来计算，也就是计算一阶导数或一阶偏导。而二阶导数对最优很有用，但是却难以计算。或许以后如果有方便计算或者更快速的运算硬件，优化算法可能会有质的提升。

### Learning Rate调节

可以通过预设几个（指数级差异）学习率，然后画出学习曲线，选择合适的学习率。

下面有几种动态调节策略：

1. 预设一个常量，在特定步长进行调节（例如第一次是0.1，第五次epoch时调整为0.001）
2. 根据训练误差来自动调节，N步检查一次误差，当误差停止变小时，学习率减少一个因子$\lambda$
3. 指数级调度，设置学习率为迭代次数t的函数：$\eta(t) = \eta_0 10^{-t/r}$
4. 觅次调整，设置学习率为迭代次数t的函数：$\eta(t) = \eta_0(1+t/r)^{-c}$

有一个评比各个方法的[paper](http://static.googleusercontent.com/media/research.google.com/fr//pubs/archive/40808.pdf)，结果是2和3较好，但是3更容易开发和调试，所以更倾向于3.

当然选择具体的Learning Rate调节方法需要结合优化算法，因为部分优化算法入Adam等可以自己调节学习率。

