# assets/asset_interface.py

from abc import ABC, abstractmethod
from typing import Dict

class AssetInterface(ABC):
    """
    Interface for all asset classes.
    """

    @abstractmethod
    def get_symbol(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_type(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_metadata(self) -> Dict:
        raise NotImplementedError
