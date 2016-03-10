# MIT License
# Copyright (c) 2016 Genome Research Limited
from typing import List, Optional
from ypip.vcs._vcs import HostedVCS

class GitOnGithub(HostedVCS):
    def __init__(self):
        pass

    def is_package_from_hosted_vcs(self, url:str) -> bool:
        pass

    def get_requirements(self, url:str, requirements:Optional[str] = 'requirements.txt') -> List[str]:
        pass
