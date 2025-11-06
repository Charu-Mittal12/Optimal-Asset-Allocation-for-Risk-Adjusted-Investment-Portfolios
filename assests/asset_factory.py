# assets/asset_factory.py

from .stock import Stock
from .crypto import Crypto
from .bond import Bond
from .etf import ETF

class AssetFactory:
    """
    Factory for creating Asset objects.
    call: AssetFactory.create(asset_type=<str>, name=<str>, symbol=<str>, **kwargs)
    """
    @staticmethod
    def create(asset_type: str, name: str, symbol: str, **kwargs):
        t = asset_type.lower()
        if t == "stock":
            return Stock(name, symbol, kwargs.get("sector"))
        if t == "crypto":
            return Crypto(name, symbol, kwargs.get("exchange", "Binance"))
        if t == "bond":
            return Bond(name, symbol, kwargs.get("coupon_rate"), kwargs.get("maturity_years"))
        if t == "etf":
            return ETF(name, symbol, kwargs.get("category"))
        raise ValueError(f"Unknown asset type: {asset_type}")
