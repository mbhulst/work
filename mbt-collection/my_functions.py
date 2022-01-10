# functions required for analysis of mbt collection antismash files

import os
from glob import glob

from Bio.Seq import Seq
from Bio import SeqIO



def dir_folder(foldername):
    """Get the path to a folder in current directory."""

    cwd = os.getcwd()
    directory = cwd + '/' + foldername
    
    return directory


def folders_in_directory(directory):
    """Get a list of all the folders in the given directory."""
    
    subdirs_raw = glob(directory + '/*/')
    
    subfoldernames = []
    
    for subdir_raw in subdirs_raw:
        subdir = subdir_raw[:-1]  # remove trailing backslash
        subfoldername = os.path.basename(subdir)   # extract subfolder name
        subfoldernames.append(subfoldername)   # collect subfolder names in list
    
    return subfoldernames


def cur_dir():
    """Get the path to the current directory."""

    cwd = os.getcwd()
    
    return cwd


def folders_in_directory2(directory):
    """Get a list of all the folders in a given directory and their path."""
    
    subfolders_raw = glob(directory + '/*/')
    
    subfolders = []
    
    for directory_raw in subfolders_raw:
        directory = directory_raw[:-1]  # remove trailing backslashes
        subfolders.append(directory)   # collect subfolder directories in list
    
    return subfolders


def predicted_bgc_types(directory):
    """In a given folder, go through all antismash generated genbank sequences to collect the predicted BGC classes. """

    filenames = bgc_files_in_directory(directory)

    dict_hits = dict()

    for filename in filenames:
        record = open_genbank_file(directory, filename)
        bgc_type = extract_bgc_type(record)
        dict_hits[filename] = bgc_type
    
    return dict_hits


def bgc_files_in_directory(directory):
    """Get a list of all the bgc genbank filenames in a given directory."""

    filenames = []
    
    for filename in os.listdir(directory):
        if "region" in filename and filename.endswith(".gbk"): 
            filenames.append(filename)
    
    return filenames


def open_genbank_file(directory, filename):
    """This function opens a genbank file from a folderpath and a filename"""
    
    filepath = directory + '/' + filename
    record = SeqIO.read(filepath, "genbank")
    
    return record


def extract_bgc_type(record):
    """This function returns the predict bgc type for a given genbank file location."""

    # extract bgc type from gbk sequence
    for feat in record.features:
        if feat.type == "cand_cluster":
            bgc_type = feat.qualifiers["product"]
            break

    return bgc_type

