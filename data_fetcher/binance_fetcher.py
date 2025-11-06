import yfinance as yf
import pandas as pd
from .data_fetcher_interface import DataFetcherInterface

class BinanceFetcher(DataFetcherInterface):
    def fetch_data(self, symbol: str, start_date: str, end_date: str) -> pd.Series:
        print("binanceeeeeeeeeeeeeeeeeeeeeeeee")
        try:
            df = yf.download(symbol, start=start_date, end=end_date, progress=False)
            if not df.empty:
                s = df['Adj Close'] if 'Adj Close' in df.columns else df['Close']
                return s.dropna().rename(symbol)
        except Exception:
            pass
        raise ValueError(f"Unable to fetch crypto data for {symbol}. Try BTC-USD, ETH-USD, etc.")
