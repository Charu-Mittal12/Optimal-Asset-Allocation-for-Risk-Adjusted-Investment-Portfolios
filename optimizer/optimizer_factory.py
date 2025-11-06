"""
optimizer_factory.py
---------------------
Factory class responsible for instantiating the right optimizer
based on the method name.

Follows SOLID principles:
- Open/Closed: Add new optimizers without modifying existing logic.
- Dependency Inversion: The system depends on the OptimizerInterface abstraction.
"""

from .mean_variance_optimizer import MeanVarianceOptimizer
from .covariance_optimizer import CovarianceOptimizer


class OptimizerFactory:
    """
    Factory for creating optimizer instances.
    """

    @staticmethod
    def get(method: str):
        """
        Returns an optimizer instance based on the selected method.

        Parameters
        ----------
        method : str
            The optimizer type. Options:
            - 'mean_variance'
            - 'covariance'

        Returns
        -------
        OptimizerInterface
            A concrete optimizer instance.
        """
        method = method.lower()
        if method == "mean_variance":
            return MeanVarianceOptimizer()
        elif method == "covariance":
            return CovarianceOptimizer()
        else:
            raise ValueError(f"Unknown optimizer method: {method}")
