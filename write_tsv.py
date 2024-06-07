import re
import time
import json
import zlib
from xml.etree import ElementTree
from urllib.parse import urlparse, parse_qs, urlencode
import requests
from requests.adapters import HTTPAdapter, Retry
import sys
import argparse
import json
import pyperclip
import os
from IDmapping import main as IDMapping_main
import pandas as pd 

def read_idsfile(file):
    with open(file, 'r') as f:
        content = f.read().strip()
        accessions_list = content.split()
    return accessions_list

def read_tsv_file(tsv_file):
    df = pd.read_csv(tsv_file, sep='\t', header=None, names=['Protein1', 'Protein2', 'Score'])
    df.insert(1, f'Protein1_GeneName', None)
    df.insert(3, f'Protein2_GeneName', None)
    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='UniprotMappingId', description='Map input_db to output_db')
    parser.add_argument('--idfile1', type=str, help='Please input a file of inputdb proteins (p1)')
    parser.add_argument('--idfile2', type=str, help='Please input a file of inputdb proteins')
    parser.add_argument('--inputdb', type=str, help='What type of data is being input? UniProtKB_AC-ID/Gene_Name', required=True)
    parser.add_argument('--outputdb', type=str, help='What type of data to convert into?', required=True)
    parser.add_argument('--taxonID', type=int, help='Is the organism specification needed?')
    parser.add_argument('--tsv_file', type=str, help='what file will you insert the genes into?')
    args = parser.parse_args()
    
    GENE_INPUT1 = read_idsfile(args.idfile1)
    tdf = read_tsv_file(args.tsv_file)
    genes_incorrect_order1, d1 = IDMapping_main(GENE_INPUT1, args.inputdb, args.outputdb, args.taxonID)
    tdf['Protein1_GeneName']  = tdf['Protein1'].map(d1) 
    GENE_INPUT2 = read_idsfile(args.idfile2)

    genes_incorrect_order1, d2 = IDMapping_main(GENE_INPUT2, args.inputdb, args.outputdb, args.taxonID)

    tdf['Protein2_GeneName'] = tdf['Protein2'].map(d2)
    tdf.to_csv(args.tsv_file, sep= '\t', index=False)