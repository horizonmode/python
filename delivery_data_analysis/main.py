from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from delivery_analysis import DeliveryAnalysis


def main() -> None:
    data = pd.read_csv(Path(__file__).with_name("data.csv"))
    analysis = DeliveryAnalysis(data)

    missing = analysis.missing_values()
    if missing.any():
        print("There are missing values in the dataset.")
        print(missing)
    else:
        print("No missing values found.")

    errors = analysis.type_errors()
    if errors:
        for error in errors:
            print(error)
        # Numeric comparisons and calculations require suitable column types.
        return
    print("All columns have correct types.")

    print("Invalid rows:")
    print(analysis.invalid_rows())
    print(f"Average cost: £{analysis.average_cost():.2f}")
    print("Delivery counts, average cost, and average days by delivery type:")
    print(analysis.summary())

    print("Descriptive statistics for the dataset:")
    print(analysis.descriptive_statistics())

    print("Welch's test: equal mean delivery times vs different means")
    try:
        result = analysis.test_delivery_times(alpha=0.05)
    except ValueError as error:
        print(f"Significance test unavailable: {error}")
    else:
        print(f"Mean difference (standard - express): {result.mean_difference_days:.2f} days")
        print(f"p-value: {result.p_value:.4g}; significance threshold: {result.alpha}")
        if result.significant:
            print("Reject equal population means under the test assumptions.")
        else:
            print("Insufficient evidence to reject equal means; this does not prove equality.")
        print("This comparison assumes independent observations and does not establish causation.")

    # This interpretation describes the supplied three-row sample.
    print(
        "In these three deliveries, longer distances were associated with longer "
        "delivery times. Express was faster and more expensive on average, but "
        "the small sample and differing weights and distances limit what we "
        "can conclude."
    )

    analysis.plot_delivery_times()
    analysis.plot_average_cost()
    # Build both figures first, then keep both windows open.
    plt.show()


if __name__ == "__main__":
    main()
