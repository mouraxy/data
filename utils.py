import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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

def showDuplicates(df):
    """
    Returns the number, percentage, and a heatmap of duplicates
    """  
    df_duplicated = df[df.duplicated()]
    duplicates = len(df_duplicated)
    percentage = duplicates / len(df)

    plt.figure(
      figsize=(7, 2), 
      constrained_layout=True
    ) 
    
    sns.heatmap(
      df.duplicated().to_frame().transpose(),
      cmap='binary',
      cbar=False,
      xticklabels=False,
      yticklabels=False
    )
    return duplicates, percentage

def showTopValues(df):
    
    """Shows the distribution of data by column of a Pandas DataFrame."""

    fCol = []

    for col in df.columns:
        count = df[col].value_counts()
        
        data = {
        'Var': col,
        'Top1': count.index[0],
        'Top2': count.index[1],
        'Others': f'+{len(count) - 2}'
        }
        
        fCol.append(data)

    return pd.DataFrame(fCol)

def CountCorrelatedColumns(CorrMatrix, CorrRange=0.85):
    """Identifies variables with strong correlation"""

    CorrelatedColumns = []
  
    for (var1, var2), corr in CorrMatrix.unstack().items():

      if var1 != var2 and abs(corr) >= CorrRange:
        CorrelatedColumns.append((var1, var2)) 

    return CorrelatedColumns