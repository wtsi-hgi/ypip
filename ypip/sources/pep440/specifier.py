"""
PEP440 Compliant Version Specifier Object
=========================================
Version specifier objects created by parsing input strings, per PEP440
[1], and providing a predicate interface

1. https://www.python.org/dev/peps/pep-0440/

FIXME Only the most common cases implemented; edge cases and "exotic"
conditions are not considered, when they probably should

License
-------
MIT License
Copyright (c) 2016 Genome Research Limited
"""
import re
from typing import Callable
from ypip.sources.pep440.version import Version
from ypip.sources.pep440.exceptions import ParseError


_PredicateT = Callable[[Version], bool]

def _equality_factory(rhs:Version, wildcard:bool) -> _PredicateT:
    pass

def _inequality_factory(rhs:Version, wildcard:bool) -> _PredicateT:
    pass

def _absolute_factory(rhs:Version) -> _PredicateT:
    pass

def _lt_factory(rhs:Version) -> _PredicateT:
    pass

def _lte_factory(rhs:Version) -> _PredicateT:
    pass

def _gt_factory(rhs:Version) -> _PredicateT:
    pass

def _gte_factory(rhs:Version) -> _PredicateT:
    pass

def _compatible_factory(rhs:Version) -> _PredicateT:
    pass


class Specifier(object):
    """ Parse version specifier string, a la PEP440 """

    # NOTE Arbitrary equality (===) is not fully supported
    pattern = re.compile(r'''
        ^
        (?P<op>===|[~!=<>]=|<|>)
        \s*
        (?P<v>.+)
        $
    ''', re.VERBOSE | re.IGNORECASE)

    wildcard = re.compile(r'\.?\d*\*')

    factory = {
        '==':  _equality_factory,
        '!=':  _inequality_factory,
        '===': lambda v, _: _absolute_factory(v),
        '<':   lambda v, _: _lt_factory(v),
        '<=':  lambda v, _: _lte_factory(v),
        '>':   lambda v, _: _gt_factory(v),
        '>=':  lambda v, _: _gte_factory(v),
        '~=':  lambda v, _: _compatible_factory(v)
    }

    def __init__(self, spec:str):
        """
        Construct Specifier by parsing input string

        @param  spec  Input string to parse
        @note   Will raise ParseError if not compliant
        """
        specifiers = re.split(r'\s*,\s*', spec.strip())
        self.comparators = []

        if not specifiers:
            raise ParseError('Specifier string is empty')

        for s in specifiers:
            parsed = Specifier.pattern.match(s)

            if not parsed:
                raise ParseError('Could not parse "{}" in accordance with PEP440'.format(s))

            v = parsed.group('v')
            op = parsed.group('op')

            has_wildcard = op in ['==', '!='] and Specifier.wildcard.search(v)
            if has_wildcard:
                # Strip wildcard from version string
                v = Specifier.wildcard.split(v)[0]

            version = Version(v)

            # Add comparator predicate to conjunction
            self.comparators.append(Specifier.factory[op](version, has_wildcard))

    def __call__(self, version:Version) -> bool:
        """
        Check input version satisfies the specification (predicate)

        @param   version  Version to check against specification
        @return  Boolean
        """
        return all(comp(version) for comp in self.comparators)
