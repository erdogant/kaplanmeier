# %% Examples
from kaplanmeier import kaplanmeier as km
# Example data
df = km.example_data()
# Fit
results = km.fit(df['time'], df['Died'], df['group'])
# Plot
km.plot(results, title='Custom title text')
km.plot(results, cmap='Set1', cii_lines=True, cii_alpha=0.05)
km.plot(results, cmap=[(1, 0, 0),(0, 0, 1)])
km.plot(results, cmap='Set1', methodtype='custom', title=None)
results['logrank_P']
results['logrank_Z']

# %%

# Import library
import kaplanmeier as km

# Import example data
df = km.example_data()

# Data
time_event = df['time']
censoring = df['Died'] 
y = df['group']

print(df)
#       time  Died  group
# 0     485     0      1
# 1     526     1      2
# 2     588     1      2
# 3     997     0      1
# 4     426     1      1
# ..    ...   ...    ...
# 175   183     0      1
# 176  3196     0      1
# 177   457     1      2
# 178  2100     1      1
# 179   376     0      1
    # 
# [180 rows x 3 columns]

# Compute Survival
results = km.fit(time_event, censoring, y)

# Plot
km.plot(results)

km.plot(results, cmap='Set1', cii_lines=None, cii_alpha=0.05)
km.plot(results, cmap='Set2', cii_lines='dense', cii_alpha=0.05)
