# Standalone Variable Static Typing
Standalone Variable Static Type Checker using [Abstract Syntax Trees](https://docs.python.org/3/library/ast.html)

### Why?
Python is an amazing programming language; my favorite one for a lot of reasons. With the broad functionality, ease of use, development speed, and friendly community, I could be here all day saying good things about it.

One of the major selling points the dynamic typing, at first.

When you start scaling Python and using it on huge projects dealing with a lot of different entities and flows you can make a mistake and find the pitfall of not knowing why your variable is not being interpreted as you wish it was; between other issues (if you try to statically type an existing codebase with MyPy you'll find how bad your code is in terms of typing consistency; at least that happened to me).

After fixing a huge mess I wanted to go a step further and not only enforce the type of functions/classes input and output but to type my standalone variables as well until I found that mypy doesn't do that.

At first, I created a simple file to do this but soon I found that I needed a proper implementation of this to spread to all my projects and possibly help the community.

A huge kudos to [@alphasensei](https://github.com/alphasensei) for doing the initial research and developing the proof of concept of what this library was at first.

This is an attempt of bringing full static typing to Python and with this much more robust codebases.
