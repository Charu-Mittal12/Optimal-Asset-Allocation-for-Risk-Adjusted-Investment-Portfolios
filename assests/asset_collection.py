# assets/asset_collection.py

from typing import List
from .asset_interface import AssetInterface

class AssetCollection:
    """
    Simple collection to hold AssetInterface objects.
    """
    def __init__(self):
        self.assets: List[AssetInterface] = []

    def add_asset(self, asset: AssetInterface):
        self.assets.append(asset)

    def get_assets(self) -> List[AssetInterface]:
        return list(self.assets)

    def get_symbols(self) -> List[str]:
        return [a.get_symbol() for a in self.assets]

    def describe(self) -> List[dict]:
        return [
            {"symbol": a.get_symbol(), "type": a.get_type(), **a.get_metadata()}
            for a in self.assets
        ]
