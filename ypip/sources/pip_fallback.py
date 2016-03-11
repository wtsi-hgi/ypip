# MIT License
# Copyright (c) 2016 Genome Research Limited
import re
from typing import List, Optional
from typing.re import Match

from ypip.sources._source import Source

class PipFallback(Source):
    def __init__(self):
        # FIXME You can have multiple version specifiers
        # FIXME foo[bar, quux] is a valid specifier
        # See PEP 440
        self._pkg_pattern = re.compile('^(\w+)((?:\s*)([~=!<>]=|[<>]|===)(?:\s*)(.+))?$')

    def _get_match(self, pkg:str) -> Optional[Match]:
        return self._pkg_pattern.match(pkg)

    def is_package_from_source(self, pkg:str) -> bool:
        return True if self._get_match(pkg) else False

    def get_requirements(self, pkg:str) -> List[str]:
        output = []
        if self.is_package_from_source(pkg):
            output.append(pkg)

        return output

    def identify(self, pkg:str) -> Optional[str]:
        match = self._get_match(pkg)

        if match:
            return match.group(1)

        else:
            return None

    def version_conflict(self, pkg1:str, pkg2:str) -> Optional[bool]:
        # TODO group(3) is the operator; group(4) is the version
        # Can I co-opt pip to do this for me?...
        return False
