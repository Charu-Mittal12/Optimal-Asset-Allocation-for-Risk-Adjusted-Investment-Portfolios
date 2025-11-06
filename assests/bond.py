# assets/bond.py

from typing import Dict
from .asset_interface import AssetInterface

class Bond(AssetInterface):
    def __init__(self, name: str, symbol: str, coupon_rate: float | None = None, maturity_years: int | None = None):
        self.name = name
        self.symbol = symbol
        self.coupon_rate = coupon_rate
        self.maturity_years = maturity_years

    def get_symbol(self) -> str:
        return self.symbol

    def get_type(self) -> str:
        return "bond"

    def get_metadata(self) -> Dict:
        return {"name": self.name, "coupon_rate": self.coupon_rate, "maturity_years": self.maturity_years}
