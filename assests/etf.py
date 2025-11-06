# assets/etf.py

from typing import Dict
from .asset_interface import AssetInterface

class ETF(AssetInterface):
    def __init__(self, name: str, symbol: str, category: str | None = None):
        self.name = name
        self.symbol = symbol
        self.category = category

    def get_symbol(self) -> str:
        return self.symbol

    def get_type(self) -> str:
        return "etf"

    def get_metadata(self) -> Dict:
        return {"name": self.name, "category": self.category}
