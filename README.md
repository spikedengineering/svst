# svst

![Python Version](https://img.shields.io/badge/Python-3.7+-yellow.svg)
[![Stable Version](https://img.shields.io/pypi/v/svst?color=blue)](https://pypi.org/project/svst/)
[![Downloads](https://img.shields.io/pypi/dm/svst)](https://pypistats.org/packages/svst)
[![Documentation Status](https://readthedocs.org/projects/svst/badge/?version=latest)](https://svst.readthedocs.io/en/latest/?badge=latest)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linting: ruff](https://img.shields.io/badge/linting-ruff-808080.svg)](https://github.com/astral-sh/ruff)
[![Uses: ast](https://img.shields.io/badge/uses-ast-000fff.svg)](https://github.com/astral-sh/ruff)

### Standalone Variables Static Typing

A full-on approach to Python static type checking.

## Why?

Python is an amazing programming language; my favorite one for a lot of reasons. With the broad functionality, ease of use, development speed, and friendly community; I could be here all day saying good things about it.

One of the major selling points the dynamic typing, at least initially.

When you start scaling Python and using it on huge projects dealing with a lot of different entities and flows you can make a mistake and find the pitfall of not knowing why your variable is not behaving as you wish it was; between other issues (if you try to statically type an existing codebase with mypy you'll find how bad your code is in terms of type consistency; at least that happened to me).

After fixing a huge mess I wanted to go a step further and not only enforce the typing of functions/classes input and output but to type my standalone variables as well until I found that mypy doesn't check that because his goal is to find the balance between dynamic and static typing; I wanted to go full-on static.

At first, I created a simple file to do this, but soon I found that I needed a proper implementation of this to spread to all my projects and possibly help the community.

I'd like to extend immense gratitude to [@alphasensei](https://github.com/alphasensei) for pioneering the research and developing the initial proof of concept for this library.

This is an attempt of bringing full-on static typing to Python and, with it, much more robust codebases.

For the core functionality `svst` uses [Abstract Syntax Trees](https://docs.python.org/3/library/ast.html).

## Quick start

Svst can be installed using pip:

```shell
python3 -m pip install -U svst
```

You can type-check the standalone variables of a program like this:

```shell
svst DIRECTORY_OR_FILE
```

You can type-check a program including the `mypy` functionality like this as well:

```shell
svst --mypy DIRECTORY_OR_FILE
```

You can run a simple check hiding the errors:

```shell
svst --mypy --check DIRECTORY_OR_FILE
```

## Intended Integrations [WiP]

* Vim
* PyCharm
* VS Code
* pre-commit

## Documentation [WiP]

[svst.readthedocs.org](https://svst.readthedocs.org/)

## Contributing

As you can see this project is still in pretty rough shape and a lot of improvement can be done.

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## License

Distributed under the Mozilla Public License Version 2.0. See `LICENSE` for more information.
