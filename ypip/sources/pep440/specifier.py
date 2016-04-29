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
from ypip.sources.pep440.version import Version
from ypip.sources.pep440.exceptions import ParseError

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

            # TODO At this point, we've got a valid Version and a valid
            # comparison operator... Now to do something useful: create
            # a function that applies the argument against the operator
            # and RHS version and append it to a list.
            # self.comparators.append(...)

    def __call__(self, version:Version) -> bool:
        """
        Check input version satisfies the specification (predicate)

        @param   version  Version to check against specification
        @return  Boolean
        """
        return all(comp(version) for comp in self.comparators)
