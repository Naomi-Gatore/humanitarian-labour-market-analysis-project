# %% [markdown]
# # HLMA - Exploratory Data Analysis
# ## Interactive EDA for Humanitarian Labour Market Analysis
#%%
import pandas as pd
df = pd.read_csv("data/master_dataset_v4.csv")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
# %%
# View first 10 rows
print(df.head(10))
# %%
print("\nShape:", df.shape)
# %%
print("\nColumns:", df.columns.tolist())