import pandas as pd
from tabulate import tabulate

def formatTable(df, fmt="simple_outline", align="left", index=False, floatfmt=".2f"):
  
    """Returns a formatted table from a pandas DataFrame."""

    table = tabulate(
      df,
      headers="keys",
      tablefmt=fmt,
      showindex=index,
      numalign=align,
      floatfmt=floatfmt
    )
    return table

def genMetadata(df):
    
    """Returns a table with the metadata of a Pandas DataFrame."""

    data_type = df.dtypes
    null_count = df.isnull().sum()
    statistics = df.describe(include='all').transpose()

    metadata = pd.DataFrame(
      {
      'Variable': data_type.index,
      'Data Types': data_type.values,
      'Nulls': null_count.values,
      'Minimum': statistics['min'],
      'Maximum': statistics['max'],
      'Mean': statistics['mean'],
      }
    )
    return metadata