import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tabulate import tabulate
from sklearn.model_selection import cross_val_score, RandomizedSearchCV

def FormatTable(df, fmt="simple_outline", align="left", index=False, floatfmt=".2f"):
  
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

def GetMetadata(df):
    
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

def ShowDuplicates(df):
  
    """Returns the number, percentage, and a heatmap of duplicates/message."""

    df_duplicated = df[df.duplicated()]
    duplicates = len(df_duplicated)
    percentage = duplicates / len(df)
    
    if duplicates > 0:
        plt.figure(figsize=(7, 2), constrained_layout=True) 
        sns.heatmap(
            df.duplicated().to_frame().transpose(),
            cmap='binary',
            cbar=False,
            xticklabels=False,
            yticklabels=False
        )
        plt.show()
        return duplicates, percentage
    else:
        print('\n\n DataFrame without duplicates')

def ShowTopValues(df):
    
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
    
    """Identifies variables with strong correlation."""

    CorrelatedColumns = []
  
    for (var1, var2), corr in CorrMatrix.unstack().items():

      if var1 != var2 and abs(corr) >= CorrRange:
        CorrelatedColumns.append((var1, var2)) 

    return CorrelatedColumns


def ShowOutliers(df):

    """Calculates the number of outliers for each feature and plots a bar chart."""

    # iqr for each feature
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1

    # outlier bounds
    LowerBound = Q1 - 1.5 * IQR
    UpperBound = Q3 + 1.5 * IQR

    # outliers for each feature
    Outliers = df[(df < LowerBound) | (df > UpperBound)]
    OutliersCount = Outliers.count()

    # plot the outliers
    OutliersDf = pd.DataFrame(OutliersCount)
    sns.barplot(x=OutliersDf.index, y=OutliersDf[0])
    plt.xticks(rotation=90)
    plt.xlabel('')
    plt.ylabel('')
    plt.show()

def CrossValidation(Models, X_train, y_train, Metric='accuracy', cv=5):
    
    """Cross-validates a list of models."""

    Rows = []
    for ModelName, Model in Models.items():

        Scores = cross_val_score(Model, X_train, y_train, scoring=Metric, cv=cv)
        Rows.append([ModelName, Scores.mean()])
    
    df = pd.DataFrame(Rows, columns=['Model', Metric])
    return df

def FindBestParameters(model, params, X_train, y_train, Metric='recall'):

    """Randomly searches a list of hyperparameters."""

    random_search = RandomizedSearchCV(model, params, scoring=Metric, cv=5, random_state=42)
    random_search.fit(X_train, y_train)
    return random_search