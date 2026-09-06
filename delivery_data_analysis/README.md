# Delivery data analysis

A beginner Python data science exercise: load delivery records, inspect their
quality, summarise costs and delivery times, plot results, and attempt a statistical
comparison. The code uses pandas, Matplotlib, NumPy, and SciPy.

## Setup and run

From `delivery_data_analysis`, create a virtual environment if you do not already have one:

```sh
cd /Users/sebsmith/python/delivery_data_analysis
python3 -m venv .venv
```

Activate it, install the packages, and run the program:

```sh
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

Create the environment once. Activate it when using a new terminal to install
packages or run this project. Activation selects this environment's Python and
packages for that terminal; `deactivate` leaves it without deleting anything.

The CSV path is resolved relative to `main.py`, so it does not depend on the
terminal's current folder.

## Dataset

`data.csv` contains three deliveries:

| Column | Meaning |
| --- | --- |
| `delivery_id` | Identifier for a delivery |
| `weight_kg` | Parcel weight in kilograms |
| `delivery_type` | Standard or express |
| `distance_km` | Delivery distance in kilometres |
| `actual_days` | Actual delivery time in days |
| `cost` | Delivery cost in pounds |

The sample is deliberately tiny. It is suitable for learning calculations, not
for drawing reliable conclusions about a delivery service.

## Object-oriented structure

| File or class | Responsibility |
| --- | --- |
| `main.py` | Loads data, creates the analysis, prints results, and displays plots |
| `DeliveryAnalysis` in `delivery_analysis.py` | Holds the DataFrame and provides analysis methods |
| `SignificanceResult` in `delivery_analysis.py` | Stores the outcome of a significance test |

```python
analysis = DeliveryAnalysis(data)
print(analysis.summary())
analysis.plot_delivery_times()
analysis.plot_average_cost()
plt.show()
```

`self.data` is the object's state. Methods operate on that dataset, keeping related
behaviour together. Supplying the DataFrame through the constructor is dependency
injection: a caller can supply a different dataset without changing the class.
The class retains the supplied DataFrame rather than copying it.

`DeliveryAnalysis` is a regular class because it performs work. `SignificanceResult`
is a frozen dataclass because it represents structured output: the mean difference,
p-value, and chosen threshold. Its `significant` property computes whether the
p-value is below that threshold. Neither a Protocol nor an abstract class is needed
for this example.

## Data quality checks

- `missing_values()` counts missing values per column.
- `type_errors()` compares column types with the expected types.
- `invalid_rows()` finds non-positive weights or negative distances, times, or costs.

These checks report problems; they do not clean the dataset automatically.
`main.py` stops on type errors, but currently continues after reporting missing
values or invalid rows. Decide how to handle those rows before interpreting a
different dataset. Numeric summaries generally skip missing values.

The type check expects specific pandas dtypes. A valid numeric column inferred
with another dtype may be flagged. These are introductory checks, not a complete
schema validator: they do not cover missing columns, duplicate IDs, or every
invalid category.

## Descriptive statistics

`summary()` groups deliveries by type and calculates:

- Number of deliveries.
- Mean and median cost.
- Standard deviation of cost.
- Mean and median delivery time.
- Standard deviation of delivery time.
- Fastest and slowest delivery times.

`average_cost()` calculates the overall mean cost. `descriptive_statistics()` uses
`DataFrame.describe()` for numeric counts, means, standard deviations, minimums,
maximums, and percentiles. The 50th percentile is the median. Statistics on
`delivery_id` have no useful interpretation because it is an identifier.

For the supplied data:

| Delivery type | Count | Mean cost | Mean days | Sample standard deviation of days |
| --- | ---: | ---: | ---: | ---: |
| Express | 1 | £17.50 | 1 | Undefined (`NaN`) |
| Standard | 2 | £8.00 | 4 | Approximately 1.41 |

The overall mean cost is approximately £11.17.

### Understanding standard deviation

Standard deviation measures spread around the mean, in the same units as the
observations. Smaller values indicate less variation; larger values indicate more.

The standard delivery times are 3 and 5 days:

```text
Mean = (3 + 5) / 2 = 4
Squared deviations = (3 - 4)² + (5 - 4)² = 2
Sample variance = 2 / (2 - 1) = 2
Sample standard deviation = √2 ≈ 1.41 days
```

Pandas uses sample standard deviation by default, dividing by `n - 1`. With only
one express delivery, this calculation is undefined. `NaN` therefore means
insufficient observations here, not zero variation or necessarily missing input.

## Graphs

`plot_delivery_times()` creates a scatter plot of distance against time, coloured
by delivery type. `plot_average_cost()` creates a bar chart of mean cost by type.

Each method uses `fig, ax = plt.subplots()`, Matplotlib's object-oriented interface.
`fig` represents the figure and `ax` is the plotting area. Explicit axes keep the
two plots separate.

Both figures are created before `plt.show()`. With a desktop GUI backend, both
windows can open together, and the program waits for them to close. Notebook
backends may display figures inline instead.

`plt.show(block=False)` lets execution continue, but a running GUI event loop is
still needed for responsive windows. Windows usually close when the script exits.
To save a figure instead, use `fig.savefig("plot.png", bbox_inches="tight")` inside
its plotting method.

## Significance test

`test_delivery_times(alpha=0.05)` performs a two-sided Welch two-sample t-test:

- Null hypothesis: standard and express have equal population mean delivery times.
- Alternative hypothesis: their population mean delivery times differ.

Welch's test allows unequal group variances. Observations should be independent.
For small samples, the normality assumption matters; having enough rows to execute
the calculation does not guarantee that the test is appropriate.

The method excludes missing times, checks for at least two observations in each
group, and rejects negative or non-finite times. It also rejects the case where
both groups have zero variance and checks that the resulting p-value is finite.

**The current CSV cannot support this calculation:** it has only one express
delivery. The method raises a descriptive `ValueError`, which `main.py` catches
and prints while allowing the rest of the program to continue.

With suitable data, the interface is:

```python
try:
    result = analysis.test_delivery_times(alpha=0.05)
except ValueError as error:
    print(error)
else:
    print(result.mean_difference_days)  # Standard mean minus express mean
    print(result.p_value)
    print(result.significant)
```

A positive mean difference means standard deliveries took longer on average.
Choose the significance threshold before inspecting the test result.

- A p-value below the threshold leads to rejecting equal means under the assumptions.
- A p-value at or above the threshold means insufficient evidence to reject equal
  means. It does not prove equality.

The p-value describes the probability, assuming the null hypothesis and model
assumptions, of a test statistic at least as extreme as the observed one. It is
not the probability that the null hypothesis is true. Statistical significance
also does not measure practical importance or establish causation. Distance and
other differences between groups may explain a difference in delivery times.

The current result reports the mean difference and p-value. It does not yet
provide a confidence interval or automatically assess the test's assumptions.

## SciPy and Pylance typing

SciPy's test result has a runtime `.pvalue` attribute. In the editor setup used for
this exercise, Pylance did not recognise that attribute. The code instead unpacks
the result:

```python
_, raw_p_value = ttest_ind(
    standard, express, equal_var=False, alternative="two-sided"
)
```

`_` receives the unused test statistic. Pylance also lacked a precise type for the
second value, so the implementation checks its type before converting it:

```python
if not isinstance(raw_p_value, (float, np.floating)):
    raise ValueError("Expected a scalar numeric p-value for two delivery groups.")
p_value = float(raw_p_value)
```

This accepts Python and NumPy floating-point scalars and narrows the type for the
editor without suppressing diagnostics. Our own dataclass names its field
`p_value`, with an underscore; this differs from SciPy's `.pvalue` spelling.

## Interpreting this sample

In these three deliveries, longer distances were associated with longer delivery
times. Express was faster and more expensive on average, but the groups also
differ in distance and weight. The sample cannot isolate those effects.

The interpretation printed in `main.py` is written for this particular sample.
Update it when changing the CSV; it is not generated automatically from the data.
