from abc import ABC, abstractmethod
import pandas as pd

class DataFetcherInterface(ABC):
    @abstractmethod
    def fetch_data(self, symbol: str, start_date: str, end_date: str) -> pd.Series:
        """Fetch price data for a symbol."""
        pass
