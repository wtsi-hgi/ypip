# MIT License
# Copyright (c) 2016 Genome Research Limited
from abc import ABCMeta, abstractmethod
from typing import List

class HostedVCS(metaclass=ABCMeta):
    '''
    Interface for understanding how to work with hosted VCS-based
    packages (i.e., type matching and how to retrieve the
    requirements.txt file)
    '''
    @abstractmethod
    def is_package_from_hosted_vcs(self, url:str) -> bool:
        '''
        Check that the package URL conforms to the VCS modelled by the
        current class

        @param   url  Package URL to check
        @return  Yay or nay
        '''

    @abstractmethod
    def get_requirements(self, url:str, requirements:str = 'requirements.txt') -> List[str]:
        '''
        @param   url           Package URL to check
        @param   requirements  Requirements file to fetch
        @return  List of requirements
        '''
