# portfolio_analyzer/volatility_calculator.py

import numpy as np
import pandas as pd

class VolatilityCalculator:
    """
    Computes portfolio volatility and related metrics.
    """

    def calculate_portfolio_volatility(self, daily_returns: pd.DataFrame, weights: pd.Series) -> float:
        """
        Compute annualized portfolio volatility.
        """
        cov_matrix = daily_returns.cov()
        portfolio_volatility = np.sqrt(weights.T @ cov_matrix @ weights)
        return portfolio_volatility

    def calculate_asset_volatility(self, daily_returns: pd.DataFrame) -> pd.Series:
        """
        Compute annualized volatility for each asset.
        """
        return daily_returns.std() * np.sqrt(252)
