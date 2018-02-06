import matplotlib.pyplot as plt
import pandas as pd
from pandas.tools.plotting import table

df = pd.read_csv("sample.csv")
fig, ax = plt.subplots(1,1)
ax.xaxis.set_visible(False)  # hide the x axis
ax.yaxis.set_visible(False)  # hide the y axis

# table(ax, df)  # where df is your data frame

df.plot(table=True, ax=ax)

plt.show()
# plt.savefig('mytable.png')