# 演示项目：模版引擎

## 最终目标
实现类似于 jinja (https://github.com/pallets/jinja) 或者 inja (https://github.com/pantor/inja) 的模板系统。

## 当前进度
* 实现了变量替换

## 使用示例

```python
from demo.template_engine.render_with_string import render_with_string

result = render_with_string("HELLO,{{ name }}", {"name": "Xiaoquan"})
print(result)
```

输出

```text
HELLO,Xiaoquan
```

## 测试
见 `render_with_string.py` 和 `render_with_tokens.py`