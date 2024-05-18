import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("time_history2.txt")

print(df.head())
# Plot the data
x = np.linspace(1, len(df), len(df))
df["number clients"] = x

# Set the x-axis ticks to be every 2 clients
plt.xticks(np.arange(0, len(df)+1, 2))

sns.lineplot(data=df, x="number clients", y="timestamp")
plt.show()