# MIT License
# Copyright (c) 2016 Genome Research Limited
import os.path
from typing import List

from ypip.sources._source import Source

class RequirementsTxt(Source):
    def is_package_from_source(self, pkg:str = 'requirements.txt') -> bool:
       return os.path.isfile(pkg)

    def get_requirements(self, pkg:str = 'requirements.txt') -> List[str]:
        if self.is_package_from_source(pkg):
            return open(pkg).read().splitlines()
        else:
            return []
