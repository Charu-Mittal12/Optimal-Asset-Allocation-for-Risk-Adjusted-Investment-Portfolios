# portfolio_analyzer/return_calculator.py

import pandas as pd

class ReturnCalculator:
    """
    Calculates asset-level and portfolio-level returns.
    """

    def calculate_daily_returns(self, price_data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate daily percentage returns for each asset.
        """
        daily_returns = price_data.pct_change().dropna()
        return daily_returns

    def calculate_portfolio_return(self, daily_returns: pd.DataFrame, weights: pd.Series) -> pd.Series:
        """
        Calculate the daily portfolio return.
        """
        portfolio_returns = (daily_returns * weights).sum(axis=1)
        return portfolio_returns

    def calculate_cumulative_return(self, portfolio_returns: pd.Series) -> float:
        """
        Calculate cumulative return of the portfolio.
        """
        cumulative_return = (1 + portfolio_returns).prod() - 1
        return cumulative_return
