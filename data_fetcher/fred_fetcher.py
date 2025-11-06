from .data_fetcher_interface import DataFetcherInterface
from pandas_datareader import data as pdr

class FredFetcher(DataFetcherInterface):
    def fetch_data(self, symbol: str, start_date: str, end_date: str):
        df = pdr.DataReader(symbol, 'fred', start_date, end_date)
        if df.empty:
            raise ValueError(f"No FRED data for {symbol}")
        return df.iloc[:, 0].dropna().rename(symbol)

