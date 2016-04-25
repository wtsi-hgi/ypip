"""
PEP440 Compliant Version Object
===============================
Version objects created by parsing input strings, per PEP440 [1]

1. https://www.python.org/dev/peps/pep-0440/

License
-------
MIT License
Copyright (c) 2016 Genome Research Limited
"""
import re
from typing import Any, Optional
from functools import total_ordering


def _maybe_int(s:Optional[Any]) -> Optional[int]:
    """ Cast to integer, if possible, otherwise None """
    try:
        return int(s)
    except:
        return None


class ParseError(Exception):
    """ Version parse error """
    pass


@total_ordering
class Version(object):
    """ Parse, normalise and order version strings, a la PEP440 """

    # Yikes...
    pattern = re.compile(r'''
        ^
        v?
        (?:(?P<epoch>\d+)!)?
        (?P<release>\d+(?:\.\d+)*)
        (?:[-._]?(?P<pre>a(?:lpha)?|b(?:eta)?|rc|pre(?:view)?)[-._]?(?P<preN>\d*))?
        (?:(?:[-._]?(?P<post>post|r(?:ev)?)[-._]?(?P<postN>\d*))|(?:(?P<postImp>-)(?P<postImpN>\d+)))?
        (?:[-._]?(?P<dev>dev)(?P<devN>\d*))?
        (?:\+(?P<local>(?=[a-z0-9])[-._a-z0-9]+(?<=[a-z0-9])))?
        $
    ''', re.VERBOSE | re.IGNORECASE)

    def __init__(self, version:str):
        """
        Construct Version by parsing input string

        @param  version  Input string to parse
        @note   Will raise ParseError if not compliant
        """
        parsed = Version.pattern.match(version.strip())

        if not parsed:
            raise ParseError('Could not parse "{}" in accordance with PEP440'.format(version))

        self.epoch = _maybe_int(parsed.group('epoch'))
        self.release = tuple(map(int, parsed.group('release').split('.')))

        self.pre = None
        self.post = None
        self.dev = None
        self.local = None

        if parsed.group('pre'):
            pre_type = { 'a': 'a', 'alpha': 'a',
                         'b': 'b', 'beta': 'b',
                         'rc': 'rc', 'pre': 'rc', 'preview': 'rc' }[parsed.group('pre').lower()]
            pre_version = _maybe_int(parsed.group('preN')) or 0
            self.pre = pre_type, pre_version

        if parsed.group('post') or parsed.group('postImp'):
            self.post = _maybe_int(parsed.group('postImpN')) \
                            or _maybe_int(parsed.group('postN')) \
                            or 0

        if parsed.group('dev'):
            self.dev = _maybe_int(parsed.group('devN')) or 0

        if parsed.group('local'):
            # TODO? Split by separator
            self.local = re.sub('[-_]', '.', parsed.group('local'))

    def __str__(self):
        output = []

        if self.epoch is not None:
            output.append('{}!'.format(self.epoch))

        output.append('.'.join(map(str, self.release)))

        if self.pre is not None:
            output.append('{}{}'.format(*self.pre))

        if self.post is not None:
            output.append('.post{}'.format(self.post))

        if self.dev is not None:
            output.append('.dev{}'.format(self.dev))

        if self.local is not None:
            output.append('+{}'.format(self.local))

        return '{}'.format(''.join(output))

    def __repr__(self):
        return '<Version {} at {}>'.format(str(self), hex(id(self)))

    def __eq__(self, other:'Version') -> bool:
        return self.epoch   == other.epoch \
           and self.release == other.release \
           and self.pre     == other.pre \
           and self.post    == other.post \
           and self.dev     == other.dev \
           and self.local   == other.local

    def __lt__(self, other:'Version') -> bool:
        pass
