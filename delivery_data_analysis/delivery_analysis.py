from dataclasses import dataclass
from math import isfinite

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind


@dataclass(frozen=True)
class SignificanceResult:
    """Outcome of a two-sided Welch test; difference is standard minus express."""

    mean_difference_days: float
    p_value: float
    alpha: float

    @property
    def significant(self) -> bool:
        return self.p_value < self.alpha


class DeliveryAnalysis:
    """Keep a dataset together with its validation, summaries, and plots."""

    def __init__(self, data: pd.DataFrame) -> None:
        # The caller supplies the data: constructor dependency injection.
        self.data = data

    def missing_values(self) -> pd.Series:
        return self.data.isnull().sum()

    def type_errors(self) -> list[str]:
        expected_types = {
            "delivery_id": "int64",
            "weight_kg": "float64",
            "delivery_type": "str",
            "distance_km": "int64",
            "actual_days": "int64",
            "cost": "float64",
        }
        errors = []
        for column, expected in expected_types.items():
            actual = self.data[column].dtype
            if actual != expected:
                errors.append(
                    f"Column {column} has incorrect type. "
                    f"Expected {expected}, got {actual}."
                )
        return errors

    def invalid_rows(self) -> pd.DataFrame:
        return self.data[
            (self.data["weight_kg"] <= 0)
            | (self.data["distance_km"] < 0)
            | (self.data["actual_days"] < 0)
            | (self.data["cost"] < 0)
        ]

    def average_cost(self) -> float:
        return float(self.data["cost"].mean())

    def descriptive_statistics(self) -> pd.DataFrame:
        return self.data.describe()

    def test_delivery_times(self, alpha: float = 0.05) -> SignificanceResult:
        """Compare independent groups' means; this does not establish causation.

        Missing times are excluded. Two observations per group are a computational
        minimum, not a guarantee of reliable statistical evidence.
        """
        if not 0 < alpha < 1:
            raise ValueError("alpha must be between 0 and 1.")

        standard = self.data.loc[
            self.data["delivery_type"] == "standard", "actual_days"
        ].dropna()
        express = self.data.loc[
            self.data["delivery_type"] == "express", "actual_days"
        ].dropna()

        if len(standard) < 2 or len(express) < 2:
            raise ValueError(
                "Need at least two non-missing delivery times per group "
                f"(standard: {len(standard)}, express: {len(express)})."
            )
        if not all(isfinite(value) and value >= 0 for value in [*standard, *express]):
            raise ValueError("Delivery times must be finite, non-negative numbers.")
        if standard.var() == 0 and express.var() == 0:
            raise ValueError("Cannot estimate uncertainty when both groups have zero variance.")

        # SciPy's result supports unpacking into the statistic and p-value.
        # This also avoids attribute lookup issues in some editor type definitions.
        _, raw_p_value = ttest_ind(
            standard, express, equal_var=False, alternative="two-sided"
        )
        if not isinstance(raw_p_value, (float, np.floating)):
            raise ValueError("Expected a scalar numeric p-value for two delivery groups.")
        p_value = float(raw_p_value)
        if not isfinite(p_value):
            raise ValueError("The test could not produce a finite p-value.")
        return SignificanceResult(
            mean_difference_days=float(standard.mean() - express.mean()),
            p_value=p_value,
            alpha=alpha,
        )

    def summary(self) -> pd.DataFrame:
        return self.data.groupby("delivery_type").agg(
            deliveries=("delivery_id", "count"),
            average_cost=("cost", "mean"),
            median_cost=("cost", "median"),
            cost_std=("cost", "std"),
            average_days=("actual_days", "mean"),
            median_days=("actual_days", "median"),
            days_std=("actual_days", "std"),
            fastest_days=("actual_days", "min"),
            slowest_days=("actual_days", "max"),
        )

    def plot_delivery_times(self) -> None:
        # Each method explicitly works with its own figure and axes.
        fig, ax = plt.subplots()
        for delivery_type, group in self.data.groupby("delivery_type"):
            ax.scatter(group["distance_km"], group["actual_days"], label=delivery_type)
        ax.set(
            xlabel="Distance (km)",
            ylabel="Delivery time (days)",
            title="Distance vs delivery time",
        )
        ax.legend()
        fig.tight_layout()

    def plot_average_cost(self) -> None:
        fig, ax = plt.subplots()
        self.summary()["average_cost"].plot(kind="bar", ax=ax)
        ax.set(
            xlabel="Delivery type",
            ylabel="Average cost (£)",
            title="Average delivery cost",
        )
        fig.tight_layout()
