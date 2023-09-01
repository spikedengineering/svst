# Standalone Variable Static Typing (SVST)
Python Standalone Variables Static Type Checking with [Abstract Syntax Trees](https://docs.python.org/3/library/ast.html).



## Why?
Python is an amazing programming language, my favorite one for a lot of reasons. With its broad functionality, ease of use, development speed, and friendly community, I could be here all day saying good things about it.

One of the major selling points is dynamic typing, at least at first.

When you start scaling Python and using it on huge projects dealing with many different entities and flows, you might make a mistake and find the pitfall of not knowing why your variable isn't being interpreted as you wish it was, among other issues. If you try to statically type an existing codebase with MyPy, you'll find how inconsistent your code might be in terms of type consistency; at least, that's what happened to me.

After fixing a huge mess, I wanted to go a step further and not only enforce the type of functions/classes input and output but also type my standalone variables. That's when I found out that mypy doesn't check that because his goal is to find the balance between dynamic and static typing; I wanted to go full-on static.

Initially, I created a simple file to do this, but soon realized I needed a proper implementation to carry over to all my projects and potentially help the community.

A huge kudos to [@alphasensei](https://github.com/alphasensei) for doing the initial research and developing the proof of concept of what this library was at first.

This is an attempt to bring full static typing to Python and, with it, much more robust codebases.
