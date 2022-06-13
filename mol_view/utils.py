import numpy as np
import pandas as pd
from rdkit import Chem


def fp2arr(fp):
    arr = np.zeros((0,))
    Chem.DataStructs.ConvertToNumpyArray(fp, arr)
    return arr


def process_data(path_to_df):
    df = pd.read_csv(path_to_df, index_col=None)

    novartis = df[df["type"] == "Novartis"]

    mask = (novartis["Compound Annotation"] == "acid") | (novartis["Compound Annotation"] == "base")
    novartis = novartis[mask]
    novartis.index = np.arange(len(novartis))

    df_A = novartis[novartis["Compound Annotation"] == "acid"]
    df_B = novartis[novartis["Compound Annotation"] == "base"]

    return df, df_A, df_B



def get_radius_size(path_to_df, min=10, factor=5):
    df = pd.read_csv(path_to_df, index_col=None)
    abs_error = df["AE"]
    abs_error = np.absolute(abs_error.to_numpy()).flatten()

    sizes = np.maximum(min, abs_error*factor)
    return sizes



