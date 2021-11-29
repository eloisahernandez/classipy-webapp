import pandas as pd
import numpy as np
from scipy.stats import shapiro


def get_dataframe(df):
    df_rows = [
        get_row(df[col_name]) for col_name in df
    ]
    return pd.concat(df_rows, axis=0).reset_index(drop=True)

def get_row(column):
    """ try:
        col = column.sample(n_samples)
    except ValueError:"""
    col = column

    features = {
        "column_name": [column.name],
        "label": [np.nan],
    }

    feature_functions = {
        "column_values": lambda x: ", ".join(map(str, x.tolist())),
        "column_values_unique": lambda x: x.unique(),
        "n_unique_values": lambda x: x.nunique(),
        "unique_value_counts": lambda x: {val: freq for val, freq in x.value_counts().items()},
        'n_values': lambda x: x.shape[0],
        "mean": lambda x: x.mean(),
        "std": lambda x: x.std(),
        "median": lambda x: x.median(),
        "skew": lambda x: x.skew(),
        "kurt": lambda x: x.kurt(),
        "shapiro_wilk_test": lambda x: shapiro(x)[1],
    }

    for col_name, fn in feature_functions.items():
        try:
            val = fn(col)
        except (ValueError, TypeError):
            val = np.nan
        except Exception as e:  # DEBUGGING TYPES OF ERRORS
            val = np.nan
            #print(features['column_name'], col_name, 'Exception:', type(e))

        features[col_name] = [val]

    return pd.DataFrame.from_dict(features)
