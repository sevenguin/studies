## 一些实际场景

### OCR Problem

OCR是从我们拍摄的照片中读出文字的信息（文字区域分割，字符分割，字符识别）

OCR pipline：image->Text detection-> character segmentation->character recognition.

在很多复杂的机器学习系统，这种流水线形式都非常普遍，在流水线中分成不同模块，每个模块都能成为机器学习系统的一个组件（有时候也不一定是机器学习组件，只是一个接一个连在一起的一系列数据）。如果要设计一个机器学习系统，其中需要作出的最重要的决定就是要怎样组织好这个pipeline，流水线中每一个模块都可能影响整个机器学习系统的性能。

如何构建一个机器学习系统以及如何分配资源？

Sliding windows to text detection，character segmentation and character classification.

可以通过增加噪音来增加数据量（人工合成数据）；自己收集、标签数据；众包

### Ceiling Analysis

上限分析

在pipeline中，在哪一模块需要花费更多的时间去改善。

找到一个度量标准，然后分段去校验测试每个段的度量值。例如精确度，可以先手动进行Text detection（100%的精确度），然后可以测试Character segmentation的精确度。知道了每个段的度量，则可以明确每段的优化潜力，从而明确整个系统的瓶颈。避免无意义的工作。