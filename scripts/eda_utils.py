import numpy as np
import pandas as pd
import Bio
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from Bio import pairwise2
from Bio.pairwise2 import format_alignment

def add_protein_features(df: pd.DataFrame, seq_col_name: str) -> pd.DataFrame:
    df = df.copy()
    
    # Make protein analysis object for each sequence
    df["protein_analysis"] = df[seq_col_name].map(ProteinAnalysis)

    # Extract protein features from analysis object column
    df["amino_acid_count"] = df["protein_analysis"].apply(lambda x: x.count_amino_acids())
    df["amino_acid_percent"] = df["protein_analysis"].apply(lambda x: x.get_amino_acids_percent())

    # df["molecular_weight"] = df["protein_analysis"].apply(lambda x: x.molecular_weight()) # X, B===============
    df["molecular_weight"] = df[seq_col_name].map(lambda x: x.replace('X', '')).map(lambda x: x.replace('B', '')) \
                                            .map(ProteinAnalysis).map(lambda x: x.molecular_weight())


    # df["instability_index"] = df["protein_analysis"].apply(lambda x: x.instability_index()) # U, X, B, O================
    df["instability_index"] = df[seq_col_name].map(lambda x: x.replace('X', '')).map(lambda x: x.replace('B', '')) \
                                            .map(lambda x: x.replace('U', '')).map(lambda x: x.replace('O', '')) \
                                            .map(ProteinAnalysis).map(lambda x: x.instability_index())

    # df["flexibility"] = df["protein_analysis"].apply(lambda x: x.flexibility()) # U, X, B, O==============
    df["flexibility"] = df[seq_col_name].map(lambda x: x.replace('X', '')).map(lambda x: x.replace('B', '')) \
                                            .map(lambda x: x.replace('U', '')).map(lambda x: x.replace('O', '')) \
                                            .map(ProteinAnalysis).map(lambda x: x.flexibility())

    # df["gravy"] = df["protein_analysis"].apply(lambda x: x.gravy()) # U, X, B, O===================
    df["gravy"] = df[seq_col_name].map(lambda x: x.replace('X', '')).map(lambda x: x.replace('B', '')) \
                                            .map(lambda x: x.replace('U', '')).map(lambda x: x.replace('O', '')) \
                                            .map(ProteinAnalysis).map(lambda x: x.gravy())

    df["aromaticity"] = df["protein_analysis"].apply(lambda x: x.aromaticity())
    df["isoelectric_point"] = df["protein_analysis"].apply(lambda x: x.isoelectric_point())
    df["charge_at_pH"] = df["protein_analysis"].apply(lambda x: x.charge_at_pH(7.4)) # average pH in body

    # Create three columns for helix, turn, and sheet from secondary structure fraction
    df["helix_frac"] = df["protein_analysis"].apply(lambda x: x.secondary_structure_fraction()[0])
    df["turn_frac"] = df["protein_analysis"].apply(lambda x: x.secondary_structure_fraction()[1])
    df["sheet_frac"] = df["protein_analysis"].apply(lambda x: x.secondary_structure_fraction()[2])

    # Get mean of molar extinction coefficients
    df["molar_extinction_coefficient"] = df["protein_analysis"].apply(lambda x: np.mean(x.molar_extinction_coefficient()))

    # Convert percentages in decimal form to percent form
    df["amino_acid_percent"] = df["amino_acid_percent"].apply(lambda x: {key: 100*val for key, val in x.items()})

    # Convert flexibility arrays into mean flexibility to get a single value, unless empty array, in which case replace with 0
    df["flexibility"] = df["flexibility"].apply(lambda x: np.mean(x) if (x != []) else 0)
    
    # Drop protein analysis object column
    df = df.drop("protein_analysis", axis=1)

    return df

def get_avg_amino_acid_count(df: pd.DataFrame, amino_acids: set or list) -> dict:
    # Initialize amino acid dict for all sequences
    am_acid_dict = dict.fromkeys(amino_acids, 0)

    for am_dict in df.amino_acid_count:
        for key in am_dict.keys():
            # If amino acid present in sequence
            if am_dict[key] != 0:
                am_acid_dict[key] = am_acid_dict.get(key) + am_dict[key]

    for key in am_acid_dict.keys():
        am_acid_dict[key] = am_acid_dict.get(key)/len(df)

    return am_acid_dict

def get_avg_amino_acid_percent(df: pd.DataFrame, amino_acids: set or list) -> dict:
    # Initialize amino acid dict for all sequences
    am_acid_dict = dict.fromkeys(amino_acids, 0)

    for am_dict in df.amino_acid_percent:
        for key in am_dict.keys():
            # If amino acid present in sequence
            if am_dict[key] != 0:
                am_acid_dict[key] = am_acid_dict.get(key) + am_dict[key]

    for key in am_acid_dict.keys():
        am_acid_dict[key] = am_acid_dict.get(key)/float(len(df))

    return am_acid_dict