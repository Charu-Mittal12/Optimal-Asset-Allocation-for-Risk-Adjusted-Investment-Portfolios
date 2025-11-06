from .yahoo_fetcher import YahooFetcher
from .binance_fetcher import BinanceFetcher
from .fred_fetcher import FredFetcher

class DataFetcherFactory:
    @staticmethod
    def get_fetcher_for_asset_type(asset_type: str):
        asset_type = asset_type.lower()  # force lowercase
        if asset_type == 'stock' or asset_type == 'etf':
            return YahooFetcher()
        elif asset_type == 'crypto':
            return BinanceFetcher()
        elif asset_type == 'bond':
            return FredFetcher()
        else:
            return YahooFetcher()
