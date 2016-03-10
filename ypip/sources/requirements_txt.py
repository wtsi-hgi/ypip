# MIT License
# Copyright (c) 2016 Genome Research Limited
from typing import List

from ypip.sources._source import Source

class RequirementsTxt(Source):
    def is_package_from_source(self, pkg:str) -> bool:
        pass

    def get_requirements(self, pkg:str) -> List[str]:
        pass
