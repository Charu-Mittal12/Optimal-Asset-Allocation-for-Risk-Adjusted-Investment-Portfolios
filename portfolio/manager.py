# portfolio/manager.py

import pandas as pd
import numpy as np
from typing import List, Dict, Optional

class PortfolioManager:
    """
    Orchestration class for building asset collections, fetching prices,
    computing returns/covariance, and running optimization & analysis.
    """

    def __init__(self, asset_factory, data_factory, optimizer_factory, analyzer):
        """
        Provide factories/classes (not instances) so we can inject mocks in tests.
        asset_factory: class providing create(...)
        data_factory: class providing get_fetcher_for_asset_type(...)
        optimizer_factory: class providing get(method)
        analyzer: an analyzer instance with analyze(price_df, weights)
        """
        self.asset_factory = asset_factory
        self.data_factory = data_factory
        self.optimizer_factory = optimizer_factory
        self.analyzer = analyzer

    def build_collection_from_specs(self, specs: List[Dict]) -> "AssetCollection":
        """
        specs: list of dicts: {"asset_type": "stock", "name": "...", "symbol": "...", ...}
        returns: AssetCollection
        """
        from assets.asset_collection import AssetCollection
        collection = AssetCollection()
        for s in specs:
            # map keys so factory signature matches
            asset = self.asset_factory.create(
                s.get("asset_type") or s.get("type") or s.get("asset"),
                s.get("name"),
                s.get("symbol"),
                **{k: v for k, v in s.items() if k not in ("asset_type", "name", "symbol")}
            )
            collection.add_asset(asset)
        return collection

    def fetch_prices(self, asset_collection, start_date: str, end_date: str) -> pd.DataFrame:
        """Fetch price series for all assets and align them."""
        series_list = []
        for asset in asset_collection.get_assets():
            fetcher = self.data_factory.get_fetcher_for_asset_type(asset.get_type())
            print(fetcher)
            symbol = asset.get_symbol().strip()
            print(symbol)
            print(start_date)
            print(end_date)
            print(f"Fetching {symbol} ({asset.get_type()}) using {fetcher.__class__.__name__}...")
            try:
                s = fetcher.fetch_data(symbol, start_date, end_date)
                print(s)
                print("Type of fetch_data:", type(fetcher.fetch_data))
                s = fetcher.fetch_data(symbol, start_date, end_date)

                if s.empty:
                    print(f"WARNING: fetched series for {symbol} is empty!")
                else:
                    series_list.append(s)
            except Exception as e:
                print(f"WARNING: failed to fetch {symbol}: {e}")

        if not series_list:
            raise RuntimeError("No price series fetched for any asset.")

        # Outer join with forward/backfill to align all assets
        price_df = pd.concat(series_list, axis=1, join='outer').ffill().bfill()
        return price_df

    def compute_expected_returns_covariance(self, price_df: pd.DataFrame):
        """Compute annualized returns, covariance and daily returns."""
        daily_returns = price_df.pct_change().dropna()
        expected_returns = daily_returns.mean() * 252
        covariance = daily_returns.cov() * 252

        # Regularize covariance to prevent singular matrix issues
        covariance += np.eye(len(covariance)) * 1e-6

        return expected_returns, covariance, daily_returns

    def optimize(self, expected_returns, covariance, method: Optional[str] = "mean_variance", target_return: Optional[float] = None):
        optimizer = self.optimizer_factory.get(method)
        try:
            # Most optimizers accept target_return
            weights = optimizer.optimize(expected_returns, covariance, target_return)  # type: ignore
        except TypeError:
            # fallback: call without target_return
            weights = optimizer.optimize(expected_returns, covariance)  # type: ignore
        except RuntimeError as e:
            # Catch optimization failures and provide a fallback equal-weight solution
            print(f"Optimization failed: {e}. Using equal weights as fallback.")
            weights = pd.Series(1 / len(expected_returns), index=expected_returns.index)
        # Ensure weights sum to 1
        weights = weights / weights.sum()
        return weights

    def analyze_portfolio(self, price_df: pd.DataFrame, weights):
        """
        Use analyzer to compute portfolio-level metrics.
        analyzer is expected to implement analyze(price_data, weights) -> dict
        """
        return self.analyzer.analyze(price_df, weights)
