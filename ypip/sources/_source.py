# MIT License
# Copyright (c) 2016 Genome Research Limited
from abc import ABCMeta, abstractmethod
from typing import List

class Source(metaclass=ABCMeta):
    '''
    Interface for understanding how to work with a source's packages
    '''
    @abstractmethod
    def is_package_from_source(self, pkg:str) -> bool:
        '''
        Check that the package URL conforms to the source modelled by
        the current class

        @param   pkg  Package string to check
        @return  Yay or nay
        '''

    @abstractmethod
    def get_requirements(self, pkg:str) -> List[str]:
        '''
        @param   url           Package URL to check
        @return  List of requirements
        '''
