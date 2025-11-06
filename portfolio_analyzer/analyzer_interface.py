# portfolio_analyzer/analyzer_interface.py

from abc import ABC, abstractmethod
import pandas as pd

class AnalyzerInterface(ABC):
    """
    Abstract base class for all portfolio analysis modules.
    Defines the contract for analyzing portfolio performance.
    """

    @abstractmethod
    def analyze(self, price_data: pd.DataFrame, weights: pd.Series) -> dict:
        """
        Analyze the portfolio given asset prices and weights.

        Args:
            price_data (pd.DataFrame): Historical price data with columns as asset names.
            weights (pd.Series): Portfolio weights for each asset.

        Returns:
            dict: Dictionary containing metrics like returns, volatility, and Sharpe ratio.
        """
        pass
