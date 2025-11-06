import numpy as np
import pandas as pd
from scipy.optimize import minimize
from .optimizer_interface import OptimizerInterface

class MeanVarianceOptimizer(OptimizerInterface):
    def optimize(self, expected_returns: pd.Series, cov_matrix: pd.DataFrame, target_return: float | None = None):
        n = len(expected_returns)
        mu = expected_returns.values
        Sigma = cov_matrix.values

        def port_vol(w):
            return np.sqrt(w.T @ Sigma @ w)

        x0 = np.ones(n) / n
        # Bound weights between 1% and 60% for diversification
        bounds = tuple((0.0, 0.7) for _ in range(n))
        cons = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0},)

        if target_return is not None:
            cons = (
                {'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0},
                {'type': 'eq', 'fun': lambda w: w @ mu - target_return}
            )

        res = minimize(lambda w: port_vol(w), x0, method='trust-constr', bounds=bounds, constraints=cons)
        if not res.success:
            raise RuntimeError('Optimization failed: ' + str(res.message))

        weights = res.x
        return pd.Series(weights, index=expected_returns.index)
