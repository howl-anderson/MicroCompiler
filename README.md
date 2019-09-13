# MicroCompiler

一个微型的 LL/LR/LALR 语法解析器，帮助编程语言设计者完成语言设计、测试等。

这个项目是我学习 Compilers: Principles,Techniques,and Tools (AKA Dragon book) 、[CS143: Compilers by Stanford University](http://web.stanford.edu/class/cs143/)、 [COMP 412: Compiler Construction for Undergraduates by Rice University](https://www.clear.rice.edu/comp412/) 和 [Engineering: CS1 - SELF PACED Compilers by Stanford University](https://lagunita.stanford.edu/courses/Engineering/Compilers/Fall2014/info) 的副产品。

# 目标
实现一个完整可用的工具集合，辅助用户实现编译器前端的设计

# 进展
- LL语法： 基本已经完成，LL语法可以覆盖绝大多数编程语言的需求了，比如 Python
- LR语法/LALR语法： 尚未完成，短期内不太可能会完成

# 使用文档
## LL(1) 语法
### MBNF 格式
MBNF 是 Micro Backus Normal Form 的缩写，是为了配合本项目的编译器特别设计的一种语法格式。MBNF 格式简单易懂，和常见的 BNF 表达式非常相似。使用者利用编写 MBNF 文件的方法，把语法信息传递给编译器。

文件 [MicroCompiler/ParserGenerator/sample.mbnf](MicroCompiler/ParserGenerator/sample.mbnf) 是一个支持 `+` `-` `*` `/` 和括号 `(` `)` 的算术计算语言的 MBNF 文件示例。
### Generator
`MicroCompiler.ParserGenerator.Generator.Generator` 可以读入 MBNF 格式的语法文件并生成一个包含 `First Set`，`Fellow Set` 等信息的 LL(1) 语法解析器必须的解析器构造数据。

这样的解析器构造数据，可以序列化成人类可读的 YAML 格式。文件 [MicroCompiler/output.yaml](MicroCompiler/output.yaml) 就是序列化成 YAML 格式的算术计算语言（见上文）的解析器构造数据。

### SkeletonParser
`MicroCompiler.SkeletonParser.SkeletonParser` 可以读入 YAML 格式的解析器构造数据和一系列 Token，判断这个 Token 序列的语法是否合法。

### TODO
生成一个类或者函数，其中预定义相关的语法访问函数，由使用者负责继承或者实现具体的业务数据构造等功能。由解析器负责依次调用各个方法或者函数。


# 如何使用
TODO (短时间内，暂时没有计划完成这个part)

# Acknowledge & Credits
http://hackingoff.com/compilers
