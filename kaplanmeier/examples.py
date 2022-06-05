# %% Examples
from kaplanmeier import kaplanmeier as km
# Example data
df = km.example_data()
# Fit
results = km.fit(df['time'], df['Died'], df['group'])
# Plot
km.plot(results)
km.plot(results, cmap='Set1', cii_lines=True, cii_alpha=0.05)
km.plot(results, cmap=[(1, 0, 0),(0, 0, 1)])
km.plot(results, cmap='Set1', methodtype='custom')
results['logrank_P']
results['logrank_Z']

# %%
