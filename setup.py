from setuptools import setup

setup(
    name="MicroCompiler",
    version="0.0.1",
    packages=[
        "MicroCompiler",
        "MicroCompiler.Lookahead",
        "MicroCompiler.ParserGenerator",
    ],
    url="https://github.com/howl-anderson/MicroCompiler",
    license="MIT",
    author="Xiaoquan Kong",
    install_requires=["pyyaml", "MicroRegEx", "jinja2"],
    author_email="u1mail2me@gmail.com",
    description="A micro compiler project to provide LL/LR/LALR syntax parser",
)
