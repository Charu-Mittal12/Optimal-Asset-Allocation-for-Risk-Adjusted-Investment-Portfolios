"""
optimizer_interface.py
-----------------------
Defines the abstract interface for all portfolio optimization strategies.

Follows SOLID principles:
- Interface Segregation: Defines a small, specific contract.
- Dependency Inversion: Higher-level modules depend on abstractions.
"""

from abc import ABC, abstractmethod
import pandas as pd


class OptimizerInterface(ABC):
    """
    Abstract base class for portfolio optimizers.
    """

    @abstractmethod
    def optimize(self, expected_returns: pd.Series, cov_matrix: pd.DataFrame) -> pd.Series:
        """
        Optimize the portfolio based on expected returns and covariance matrix.

        Parameters
        ----------
        expected_returns : pd.Series
            Expected annualized returns for each asset.
        cov_matrix : pd.DataFrame
            Annualized covariance matrix of asset returns.

        Returns
        -------
        pd.Series
            Optimal portfolio weights (sum to 1).
        """
        pass
