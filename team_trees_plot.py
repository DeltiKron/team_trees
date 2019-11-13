import pandas as pd 
df = pd.read_csv("/dat/schaffer/scripts/team_trees_count.csv",parse_dates=[0],names=['date','count'],index_col=0) 
import matplotlib.pyplot as plt 
import numpy as np
import datetime

fit_res = np.polyfit(np.arange(len(df)),df["count"],deg=1) 
correction = np.arange(len(df))*fit_res[0]+fit_res[1] 
df["differences"] = df.diff()["count"]

# Create Subplots
fig = plt.figure(figsize=(16, 10), dpi=80)
axes = fig.subplots(2,2)
ax1, ax2, ax3, ax4 = axes[0,0],axes[1,0],axes[0,1],axes[1,1]

# plot total over entire range
ax1.plot(df['count']/10**6)
ax1.set_xlabel('Date')
ax1.set_ylabel('Total Donations / Million $')

# plot total differences
differences = df.diff()['count'].groupby(pd.Grouper(freq="30min")).mean()
ax2.plot(differences*2/30)
ax2.set_xlabel('Date')
ax2.set_ylabel('Rate/ $ min^-1')

# Plot change by time of day
by_hour = differences.groupby(differences.index.hour).median()
ax3.plot(by_hour*2)
ax3.set_xlabel('Date')
ax3.set_ylabel('Rate, Hourly Median / $ min^-1')


# Predicted sum on closing date over time
hourly = df.groupby(pd.Grouper(freq="H"))['differences'].mean()
hours_left = (datetime.datetime(2020,1,1)-hourly.index).total_seconds()/3600
total = df['count']
total_at_time = total.resample('h').mean().reindex(hourly.index)
expected_total = total_at_time+(hourly*hours_left)
print(expected_total - total_at_time)
ax4.plot(expected_total/10**6,label='Expected total at Close')
ax4.set_xlabel('Date')
ax4.set_ylabel('Expected Total at Close / Million $')
print(hourly.index[0],hourly.index[-1])
ax4.axhline(20,color='r',linestyle='--',alpha=.5,label='Target of 20 Million')
ax4.legend()

plt.tight_layout()
plt.show()

# df["count"].plot() 

# plt.title("Team Trees Donation Total")
# plt.xlabel("Date")
# plt.ylabel("Difference / \$")
# ax = plt.gca()
# ax.annotate(f"Average Slope: {fit_res[0]*2:6.2f}\$/min",xy=(0.05,.95), xycoords='axes fraction')

# # calculate expected value on new years:
# import datetime
# now = datetime.datetime.now()
# new_year = datetime.datetime(2020,1,1)
# minutes_left = (new_year - now).seconds/60
# total_now = df["count"][-1]
# expected_total = total_now+(fit_res[0]*2*minutes_left)
# ax.annotate(f"Current total:{total_now:10.2f} \$",xy=(.05,.9), xycoords='axes fraction')
# ax.annotate(f"Expected on New Years Eve:{expected_total:10.2f} \$",xy=(.05,.85), xycoords='axes fraction')


# plt.show() 

