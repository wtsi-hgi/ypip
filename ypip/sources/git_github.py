# MIT License
# Copyright (c) 2016 Genome Research Limited
import re
from urllib.request import urlopen
from urllib.error import HTTPError
from typing import List
from warnings import warn

from ypip.sources._source import Source

class GitOnGithub(Source):
    def __init__(self):
        self._url_pattern = re.compile('^git\+(?:git|https|ssh)://github.com/(.+?(?=/))/(.+(?=\.git))\.git@(.+(?=#))#egg=.+$')
        self._req_url = 'https://raw.githubusercontent.com/{org}/{repo}/{branch_tag_or_commit}/requirements.txt'

    def is_package_from_source(self, pkg:str) -> bool:
        return True if self._url_pattern.match(url) else False

    def get_requirements(self, pkg:str) -> List[str]:
        output = []
        match = self._url_pattern.match(url)

        if match:
            output.append(url)

            org, repo, branch_tag_or_commit = match.groups()
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
