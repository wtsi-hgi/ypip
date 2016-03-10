Ypip
====
Ypip (pronounced "yip") is a simple wrapper to Python's pip package
manager that supports recursive installation of hosted VCS packages.
That is, it will work per ``pip install`` or ``pip install -r`` for PyPI
and ``requirements.txt`` dependencies, respectively. However, whenever
it encounters a hosted VCS dependency, it will attempt to fetch its
requirements and recursively install everything it needs (like pip
*should* do, anyway).

Usage::

    ypip [-u] [PACKAGE]

    -u       Upgrade all packages to the newest available version
    PACKAGE  The package string; this will default to requirements.txt

Motivation
----------
Say your ``requirements.txt`` looks like this::

    some-package==1.2.3
    anotherPackage==0.0.1
    git+https://github.com/foo/bar.git@branch#egg=myGitPackage

...and your ``setup.py`` includes these using the following pattern::

    setup(
        # All the other setuptools stuff here
        # ...
        install_requires=[x for x in open("requirements.txt").read().splitlines() if "://" not in x],
        dependency_links=[x for x in open("requirements.txt").read().splitlines() if "://" in x]
    )

...and the ``requirements.txt`` that exists in the git repository (with
a similar ``setup.py`` of its own) is like so::

    yet_another_thing_py=2016.04
    git+https://github.com/quux/xyzzy.git@commit_id#egg=another_vcs_package

...then, when running ``pip install -r requirements.txt``, then any of
the VCS-based packages listed down the tree (i.e., not at the root) will
**not** get installed and nor will any of their requirements.

This could *possibly* be due to the way the ``setup.py`` files are
defined. However, no amount of permutations, experimentation or enquiry
(documentation would have been nice!) gave the results we were looking
for. This is thus a hack, so we can stop hardcoding horrible ``curl``
and ``sed`` commands into our build scripts.

Currently Supported Package Sources
-----------------------------------
- ``requirements.txt``
- Git on GitHub
- PyPI

License
-------
MIT License

Copyright (c) 2016 Genome Research Limited
