# MIT License
# Copyright (c) 2016 Genome Research Limited
import re
from urllib.request import urlopen
from urllib.error import HTTPError
from typing import List, Optional
from typing.re import Match
from warnings import warn

from ypip.sources._source import Source

class GitOnGitHub(Source):
    def __init__(self):
        self._pkg_pattern = re.compile('^(?:-e)?git\+(?:git|https|ssh)://github.com/(.+?(?=/))/(.+(?=\.git))\.git@(.+(?=#))#egg=(.+)$')
        self._req_url = 'https://raw.githubusercontent.com/{org}/{repo}/{branch_tag_or_commit}/requirements.txt'

    def _get_match(self, pkg:str) -> Optional[Match]:
        return self._pkg_pattern.match(pkg)

    def is_package_from_source(self, pkg:str) -> bool:
        return True if self._get_match(pkg) else False

    def get_requirements(self, pkg:str) -> List[str]:
        output = []
        match = self._get_match(pkg)

        if match:
            output.append(pkg)

            org, repo, branch_tag_or_commit, _ = match.groups()
            req_url = self._req_url.format(
                org                  = org,
                repo                 = repo,
                branch_tag_or_commit = branch_tag_or_commit
            )

            with urlopen(req_url) as response:
                try:
                    raw = response.read()
                except HTTPError as exception:
                    if exception.code == 404:
                        msg = 'requirements.txt not found in {}/{}@{}'.format(org, repo, branch_tag_or_commit)
                        print("Warning!", msg)
                        warn(msg, Warning)
                    else:
                        raise exception

                output += raw.splitlines()

        return output

    def identify(self, pkg:str) -> Optional[str]:
        match = self._get_match(pkg)

        if match:
            org, repo, _, egg = match.groups()
            return '{}:GitHub {}/{}'.format(egg, org, repo)

        else:
            return None

    def version_conflict(self, pkg1:str, pkg2:str) -> Optional[bool]:
        match1 = self._get_match(pkg1)
        match2 = self._get_match(pkg2)

        if match1 and match2:
            org1, repo1, ver1, egg1 = match1.groups()
            org2, repo2, ver2, egg2 = match2.groups()

            return not(egg1  == egg2 \
                   and org1  == org2 \
                   and repo1 == repo2 \
                   and ver1  == ver2)
        else:
            return None
