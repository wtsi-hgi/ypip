# MIT License
# Copyright (c) 2016 Genome Research Limited
import os.path
from typing import List, Optional

from ypip.sources._source import Source

class RequirementsTxt(Source):
    def is_package_from_source(self, pkg:str = 'requirements.txt') -> bool:
       return os.path.isfile(pkg)

    def get_requirements(self, pkg:str = 'requirements.txt') -> List[str]:
        if self.is_package_from_source(pkg):
            return open(pkg).read().splitlines()
        else:
            return []

    def identify(self, pkg:str) -> Optional[str]:
        return None

    def version_conflict(self, pkg1:str, pkg2:str) -> Optional[bool]:
        return None
