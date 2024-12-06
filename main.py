#!/usr/bin/env python3
from Prophage import Prophage
import pandas as pd
import openpyxl

def main(all_prophages_names, all_prophages_file_path, metadata_file_path):
    print("Starting execution of main method...")

    data_prophage_names = pd.read_csv(all_prophages_names)
    data_prophage_tsv = pd.read_csv(all_prophages_file_path)
    data_metadata = pd.read_csv(metadata_file_path)

    result = []
    for prophage_name in data_prophage_names:
        current_prophage = Prophage(prophage_name)
        current_prophage.add_samples(data_prophage_tsv)

        ratios_by_dehydration = current_prophage.get_ratios_by_dehydration(data_prophage_tsv, data_metadata)
        result.append(ratios_by_dehydration)

    return result

    # Implement code here to output/reformat a new .xlsx file with prophage data
    # Should contain, every prophage


if __name__ == "__main__":
    # Also look into implementation for main to accept arguments (in a bash command line)

    # .txt file with names of all prophages
    all_prophages_names = "/Users/bensakdinan/Desktop/prophage_induction/Code/test_all_prophage_names.txt"
    # .xlsx file with all prophages, their prophage-host_ratio, and the corresponding sample
    all_prophages_file_path = "/Users/bensakdinan/Desktop/prophage_induction/Code/test_all_prophage_data.csv"
    # .xlsx file with one row per sample name, and all corresponding metadata, namely Dehydration_Status
    metadata_file_path = "/Users/bensakdinan/Desktop/prophage_induction/00_metadata.csv"

    # Run main method
    main(all_prophages_names, all_prophages_file_path, metadata_file_path)
