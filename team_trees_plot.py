from os.path import join, dirname

import pandas as pd
from scipy.optimize import curve_fit

infile = join(dirname(__file__), "team_trees_count.csv")
df = pd.read_csv(infile, parse_dates=[0], names=['date', 'count'], index_col=0)
import matplotlib.pyplot as plt
import datetime
import numpy as np

df = df.resample('30s').mean()
df = df.interpolate()
df["differences"] = df.diff()["count"]

# Create Subplots
fig = plt.figure(figsize=(16, 10), dpi=80)
axes = fig.subplots(2, 2)
ax1, ax2, ax3, ax4 = axes[0, 0], axes[1, 0], axes[0, 1], axes[1, 1]

# plot total over entire range
ax1.plot(df['count'] / 10 ** 6)
ax1.set_xlabel('Date')
ax1.set_ylabel('Total Donations / Million $')
# Set axis ranges to reflect fundraising period and draw goal line
ax1.axhline(20, color='r', linestyle='--', alpha=.5, label='Target of 20 Million')
ax1.set_xlim(df.index.min(), datetime.date.fromisoformat("2020-01-01"))
ax1.set_ylim(0, 22)

# plot estimate of last week
last_date = df.index.max()
last_week = last_date - datetime.timedelta(days=7.)
counts_last_week = df.loc[last_week:, "count"]


def func(x, a, b):
    return a + x * b


x = counts_last_week.index.values.astype(datetime.datetime)
y = counts_last_week.values
popt, pcov = curve_fit(func, x, y)
x_test = np.array([counts_last_week.index.min(), datetime.datetime.fromisoformat("2020-01-01T00:00:00")])
x_test = pd.to_datetime(x_test)

y_fit = func(pd.to_datetime(x_test).values.astype(datetime.datetime), *popt)
ax1.plot(x_test, y_fit, 'g--')


def predict_close(series):
    epochs = (series.index - pd.Timestamp("1970-01-01")) // pd.Timedelta('1ms')
    pars = np.polyfit(epochs, series.values, 1)

    closing_date = datetime.datetime(2020, 1, 1, 0, 0, 0)
    closing_epoch = (closing_date - pd.Timestamp("1970-01-01")) // pd.Timedelta('1ms')
    expected_close = pars[0] * closing_epoch + pars[1]
    return expected_close


# plot total differences
differences = df.diff()['count'].groupby(pd.Grouper(freq="30min")).mean()
differences_ = differences * 2 / 30
ax2.plot(differences_.rolling(300).sum())
ax2.set_xlabel('Date')
ax2.set_ylabel('Rate/ $ min^-1')
# ax2.set_yscale('log')

# Plot change by time of day
by_hour = differences.groupby(differences.index.hour).median()
ax3.plot(by_hour * 2)
ax3.set_xlabel('Date')
ax3.set_ylabel('Rate, Hourly Median / $ min^-1')

# Predicted sum on closing date over time
total = df['count']
hourly = df['count'].resample('24h', how='last')
expected_total = hourly.rolling(24).agg({'count': predict_close})

ax4.plot(expected_total / 10 ** 6, label='Expected total at Close')
ax4.set_xlabel('Date')
ax4.set_ylabel('Expected Total at Close / Million $')
ax4.axhline(20, color='r', linestyle='--', alpha=.5, label='Target of 20 Million')
ax4.set_yscale('log')
ax4.legend()

plt.tight_layout()
plt.show()
