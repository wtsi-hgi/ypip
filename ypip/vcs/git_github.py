# MIT License
# Copyright (c) 2016 Genome Research Limited
import re
from urllib.request import urlopen
from typing import List

from ypip.vcs._vcs import HostedVCS

class GitOnGithub(HostedVCS):
    def __init__(self):
        self._url_pattern = re.compile('^git\+(?:git|https|ssh)://github.com/(.+?(?=/))/(.+(?=\.git))\.git@(.+(?=#))#egg=.+$')
        self._req_url = 'https://raw.githubusercontent.com/{org}/{repo}/{branch_tag_or_commit}/{requirements}'

    def is_package_from_hosted_vcs(self, url:str) -> bool:
        return True if self._url_pattern.match(url) else False

    def get_requirements(self, url:str, requirements:str = 'requirements.txt') -> List[str]:
        output = []
        match = self._url_pattern.match(url)

        if match:
            output.append(url)

            org, repo, branch_tag_or_commit = match.groups()
            req_url = self._req_url.format(
                org                  = org,
                repo                 = repo,
                branch_tag_or_commit = branch_tag_or_commit,
                requirements         = requirements
            )

            with urlopen(req_url) as response:
                raw = response.read()
                output += raw.splitlines()

        return output
