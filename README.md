# Standalone Variable Static Typing

![Python Version](https://img.shields.io/badge/Python-3.6.15-yellow.svg)
[![Stable Version](https://img.shields.io/pypi/v/svst?color=blue)](https://pypi.org/project/svst/)
[![Downloads](https://img.shields.io/pypi/dm/svst)](https://pypistats.org/packages/svst)
[![Build Status](https://github.com/spikedengineering/svst/actions/workflows/test.yml/badge.svg)](https://github.com/spikedengineering/svst/actions)
[![Documentation Status](https://readthedocs.org/projects/svst/badge/?version=latest)](https://svst.readthedocs.io/en/latest/?badge=latest)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Standalone Variable Static Type Checker using [Abstract Syntax Trees](https://docs.python.org/3/library/ast.html)

A full-on static typing approach to writing Python code <3

## Why?

Python is an amazing programming language; my favorite one for a lot of reasons. With the broad functionality, ease of use, development speed, and friendly community; I could be here all day saying good things about it.

One of the major selling points the dynamic typing, at least initially.

When you start scaling Python and using it on huge projects dealing with a lot of different entities and flows you can make a mistake and find the pitfall of not knowing why your variable is not behaving as you wish it was; between other issues (if you try to statically type an existing codebase with mypy you'll find how bad your code is in terms of type consistency; at least that happened to me).

After fixing a huge mess I wanted to go a step further and not only enforce the typing of functions/classes input and output but to type my standalone variables as well until I found that mypy doesn't check that because his goal is to find the balance between dynamic and static typing; I wanted to go full-on static.

At first, I created a simple file to do this, but soon I found that I needed a proper implementation of this to spread to all my projects and possibly help the community.

I'd like to extend immense gratitude to [@alphasensei](https://github.com/alphasensei) for pioneering the research and developing the initial proof of concept for this library.

This is an attempt of bringing full-on static typing to Python and, with it, much more robust codebases.

## Quick start

Svst can be installed using pip:

```shell
python3 -m pip install -U svst
```

You can type-check the standalone variables of a program like this:

```shell
svst PROGRAM
```

You can type-check a program including the `mypy` functionality like this as well:

```shell
svst --mypy PROGRAM
```

## Integrations

* Vim
* PyCharm
* VS Code
* pre-commit

## Documentation



## Contributing
