import yfinance as yf
import pandas as pd
from .data_fetcher_interface import DataFetcherInterface

class YahooFetcher(DataFetcherInterface):
    def fetch_data(self, symbol: str, start_date: str, end_date: str) -> pd.Series:
        print(symbol)
        
        df = yf.download(symbol, start=start_date, end=end_date, progress=False)
        print(df)
        
        if df.empty:
            raise ValueError(f"No data returned for {symbol} from Yahoo Finance.")
        
        # Flatten MultiIndex columns
        df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]
        print("Flattened columns:", df.columns)
        
        # Slice Close column for the symbol
        col_name = f'Close_{symbol}'
        if col_name not in df.columns:
            raise ValueError(f"Column {col_name} not found in downloaded data")
        
        series = df[col_name].dropna().rename(symbol)
        print(series.head(), type(series))
        
        return series

