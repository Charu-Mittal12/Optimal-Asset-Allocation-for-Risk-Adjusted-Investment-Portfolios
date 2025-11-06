# portfolio_analyzer/portfolio_analyzer.py

import numpy as np
import pandas as pd
from portfolio_analyzer.analyzer_interface import AnalyzerInterface
from portfolio_analyzer.return_calculator import ReturnCalculator
from portfolio_analyzer.volatility_calculator import VolatilityCalculator

class PortfolioAnalyzer(AnalyzerInterface):
    """
    Concrete implementation of portfolio analysis combining
    returns, volatility, and performance metrics.
    """

    def __init__(self, risk_free_rate: float = 0.02):
        self.risk_free_rate = risk_free_rate
        self.return_calculator = ReturnCalculator()
        self.volatility_calculator = VolatilityCalculator()

    def analyze(self, price_data: pd.DataFrame, weights: pd.Series) -> dict:
        """
        Perform complete portfolio analysis.
        """

        # Step 1: Calculate daily returns
        daily_returns = self.return_calculator.calculate_daily_returns(price_data)

        # Step 2: Calculate portfolio daily returns
        portfolio_returns = self.return_calculator.calculate_portfolio_return(daily_returns, weights)

        # Step 3: Calculate cumulative return
        cumulative_return = self.return_calculator.calculate_cumulative_return(portfolio_returns)

        # Step 4: Calculate volatility
        portfolio_volatility = self.volatility_calculator.calculate_portfolio_volatility(daily_returns, weights)

        # Step 5: Calculate Sharpe ratio (annualized)
        sharpe_ratio = self._calculate_sharpe_ratio(portfolio_returns, portfolio_volatility)

        # Step 6: Bundle results
        analysis_results = {
            "Cumulative Return": round(cumulative_return * 100, 2),
            "Portfolio Volatility": round(portfolio_volatility * np.sqrt(252) * 100, 2),
            "Sharpe Ratio": round(sharpe_ratio, 3)
        }

        return analysis_results

    def _calculate_sharpe_ratio(self, portfolio_returns: pd.Series, portfolio_volatility: float) -> float:
        """
        Compute the annualized Sharpe Ratio.
        """
        mean_daily_return = portfolio_returns.mean()
        excess_return = mean_daily_return * 252 - self.risk_free_rate
        annualized_volatility = portfolio_volatility * np.sqrt(252)
        return excess_return / annualized_volatility if annualized_volatility != 0 else 0.0
