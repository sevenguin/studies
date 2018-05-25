### LIME：Local Interpretable Model-agnostic Explaination

orgin data: $x\in \mathbb R^d$

可解释表示方法，二进制向量表示，$x' \in \{0, 1\}^{R'}$

dene an explanation as a model $g \in G$，G是可能的可解释模型中的一类。g可以通过图表或者文字的方式被阅读。$g$的domain是$\{0,1\}^{d'}$，g acts over absence/presence of the interpretable components.

$\Omega(g)$表示g的复杂度，例如：g是树模型的话，这个值就可能是树的深度，如果是线性模型，则有可能是非0权值。

> 定义
>
> 假设我们需要解释的模型是标识为$f: \mathbb R^d \to \mathbb R$，例如分类算法中，$f$表示x属于某一类的概率值。然后，我们使用$\pi_x(z)$来作为一个接近度来度量实例$z$到$x$，从而方便定义$x$的邻域。最后使用$\ell(f, g, \pi_x)$来度量用$g$来近似$f$的不可靠程度，为了同时保证可解释性和局部可靠性，我们必须同时最小化$\ell$和$\Omega$，通过LIME得到解释可以通过下面式子获得：
> $$
> \xi(x) = arg\min_{g\in G} \ell(f, g, \pi_x) + \Omega(g)
> $$
>

$z'$是从$x'$而来，是随机抽取$x'$的非零元素获得。

但是$x'$是什么值？$d'$是什么值？

