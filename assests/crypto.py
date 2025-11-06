# assets/crypto.py

from typing import Dict
from .asset_interface import AssetInterface

class Crypto(AssetInterface):
    def __init__(self, name: str, symbol: str, exchange: str = "Binance"):
        self.name = name
        self.symbol = symbol
        self.exchange = exchange

    def get_symbol(self) -> str:
        return self.symbol

    def get_type(self) -> str:
        return "crypto"

    def get_metadata(self) -> Dict:
        return {"name": self.name, "exchange": self.exchange}
