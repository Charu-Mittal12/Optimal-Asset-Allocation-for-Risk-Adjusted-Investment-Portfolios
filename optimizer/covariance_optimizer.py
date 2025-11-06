"""
covariance_optimizer.py
------------------------
Implements an analytical solution for portfolio optimization
based on the inverse covariance-weighted returns.

Formula:
    w ∝ Σ⁻¹μ

This optimizer provides a quick analytical alternative to
Mean-Variance Optimization.
"""

import numpy as np
import pandas as pd
from .optimizer_interface import OptimizerInterface


class CovarianceOptimizer(OptimizerInterface):
    """
    Analytical optimizer based on inverse covariance weighting.
    """

    def optimize(self, expected_returns: pd.Series, cov_matrix: pd.DataFrame) -> pd.Series:
        Sigma = cov_matrix.values
        mu = expected_returns.values

        # Compute inverse covariance and weight allocation
        inv_cov = np.linalg.pinv(Sigma)
        raw_weights = inv_cov @ mu

        # Normalize weights to sum to 1
        weights = raw_weights / np.sum(raw_weights)

        return pd.Series(weights, index=expected_returns.index, name="weights")
