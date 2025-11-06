# assets/stock.py

from typing import Dict
from .asset_interface import AssetInterface

class Stock(AssetInterface):
    def __init__(self, name: str, symbol: str, sector: str | None = None):
        self.name = name
        self.symbol = symbol
        self.sector = sector

    def get_symbol(self) -> str:
        return self.symbol

    def get_type(self) -> str:
        return "stock"

    def get_metadata(self) -> Dict:
        return {"name": self.name, "sector": self.sector}
