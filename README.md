# MicroCompiler

一个微型的 LL/LR/LALR 语法解析器，帮助编程语言设计者完成语言设计、测试等。

这个项目是我学习 Compilers: Principles,Techniques,and Tools (AKA Dragon book) 、[CS143: Compilers by Stanford University](http://web.stanford.edu/class/cs143/)、 [COMP 412: Compiler Construction for Undergraduates by Rice University](https://www.clear.rice.edu/comp412/) 和 [Engineering: CS1 - SELF PACED Compilers by Stanford University](https://lagunita.stanford.edu/courses/Engineering/Compilers/Fall2014/info) 的副产品。

# 目标
实现一个完整可用的工具集合，辅助用户实现编译器前端的设计

# 进展
- LL语法： 基本已经完成，LL语法可以覆盖绝大多数编程语言的需求了，比如 Python
- LR语法/LALR语法： 尚未完成，短期内不太可能会完成

# Features
计算 `6 * (2 + 2)` 的值过程可以通过以下抽象语法树（图由本项目编译器自动生成，经过 `Cytoscape` 渲染得到）：

![](demo/arithmetic_calculator/calculator.png)

# 使用文档
## LL(1) 语法
### MBNF 格式
MBNF 是 Micro Backus Normal Form 的缩写，是为了配合本项目的编译器特别设计的一种语法格式。MBNF 格式简单易懂，和常见的 BNF 表达式非常相似。使用者利用编写 MBNF 文件的方法，把语法信息传递给编译器。

文件 [demo/arithmetic_calculator/calculator.mbnf](demo/arithmetic_calculator/calculator.mbnf) 是一个支持 `+` `-` `*` `/` 和括号 `(` `)` 的算术计算语言的 MBNF 文件示例。

### Generator
`MicroCompiler.ParserGenerator.Generator.Generator` 可以读入 MBNF 格式的语法文件并生成一个包含 `First Set`，`Fellow Set` 等信息的 LL(1) 语法解析器必须的解析器构造数据。

这样的解析器构造数据，可以序列化成人类可读的 YAML 格式。文件 [demo/arithmetic_calculator/calculator.yaml](demo/arithmetic_calculator/calculator.yaml) 就是序列化成 YAML 格式的算术计算语言（见上文）的解析器构造数据。

### SkeletonParser
`MicroCompiler.SkeletonParser.SkeletonParser` 可以读入 YAML 格式的解析器构造数据和一系列 Token，判断这个 Token 序列的语法是否合法，并生成一个合法的解析依赖关系图。

### build_parser_evaluator
在依赖关系图的基础上，`MicroCompiler.parser_evaluator_builder.build_parser_evaluator` 根据依赖信息，构建抽象语法树。并得到按照拓扑排序构造的解析顺序。

### ParserBuilder
`MicroCompiler.parser_builder.ParserBuilder` 能够生成一个解析器基类，用户需要继承这个基类，在用户自定义类中添加相关语法生成式的解析方法。

### ParserEvaluator
`MicroCompiler.parser_evaluator.ParserEvaluator` 会在拓扑排序后的解析序列的指导下，依次执行用户自定义类中的方法，返回结果

### [可选] Evaluator
对于返回后缀表达式（逆波兰表达式）的用户自定类来说，用户可以选择使用 `MicroCompiler.postfix_expression.evaluator.Evaluator` 提供的功能，完成后缀表达式的求值工作。

# 演示
为了更好的验证和演示如何使用该项目，这里提供了几个示例

## 算术计算器
求解四则运算（`+`、`-`、`*`、`、`、`（`、`）`）的算术表达式语言的解析器。项目位于 [demo/arithmetic_calculator](demo/arithmetic_calculator), 内含详细的说明文档。

## 模板引擎
简单的模板渲染引擎，可以渲染诸如 `HELLO,{{ name }}` 的模板。项目位于 [demo/template_engine](demo/template_engine), 内含详细的说明文档。

# Acknowledge & Credits
http://hackingoff.com/compilers
