# MIT License
# Copyright (c) 2016 Genome Research Limited
from abc import ABCMeta, abstractmethod
from typing import List, Optional

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
        @param   pkg  Package string
        @return  List of requirements
        '''

    @abstractmethod
    def identify(self, pkg:str) -> Optional[str]:
        '''
        @param   pkg  Package string
        @return  An invariant form of the package string (usually with
                 version information stripped out)
        '''

    @abstractmethod
    def version_conflict(self, pkg1:str, pkg2:str) -> Optional[bool]:
        '''
        @param   pkg1  Package string
        @param   pkg2  Package string
        @return  Whether the two versions conflict
        '''
