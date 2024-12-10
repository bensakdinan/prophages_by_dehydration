#!/usr/bin/env python3
from Prophage import Prophage
import csv
import argparse


def prophages_by_dehydration(prophage_names_path, prophages_data_path, metadata_path, output_path):
    print("Starting execution of prophages_by_dehydration.py main method...\n")

    data_prophage_names = f"{prophage_names_path}"

    # Dictionary to store all ratios by dehydration for every input prophage
    prophages_and_ratios_by_dehydration = {}

    # Iterate through every input prophage
    with open(data_prophage_names, 'r') as sample_names_file:
        for prophage_name in sample_names_file:
            # Create new instance for the current prophage
            current_prophage = Prophage(prophage_name)

            # Populate the current prophage samples_present attribute list
            current_prophage.add_samples(prophages_data_path)

            # Get and assign all prophage:host read ratios to their corresponding dehydration status
            ratios_by_dehydration = current_prophage.get_ratios_by_dehydration(prophages_data_path,
                                                                               metadata_path
                                                                               )
            # Update dictionary
            prophages_and_ratios_by_dehydration[current_prophage.identifier] = ratios_by_dehydration

    # Writing results of prophages_and_ratios_by_dehydration to final output.csv file
    write_dict_to_csv(prophages_and_ratios_by_dehydration, output_path)


def write_dict_to_csv(data, output_path):
    # Define the columns for the output CSV
    fieldnames = ['Prophage', 'Mild', 'Moderate', 'Severe']

    # Open/create the (new) CSV file for writing
    with open(output_path, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Write the header row

        # Write each prophage and its data
        for prophage, ratios in data.items():
            writer.writerow({
                'Prophage': prophage,
                'Mild': ratios['Mild'],
                'Moderate': ratios['Moderate'],
                'Severe': ratios['Severe']
            })


# Run prophages_by_dehydration.py in command line
# Takes 4 arguments
if __name__ == "__main__":
    # Instantiate parser object to accept command line arguments
    parser = argparse.ArgumentParser(description="Analyze prophage data and write results to a CSV.")

    # Command line arguments
    parser.add_argument("all_prophages_names.txt", help="Path to the file containing prophage names.")
    parser.add_argument("all/prophages/file/path.csv", help="Path to the CSV file containing all prophages.")
    parser.add_argument("metadata/file/path.csv", help="Path to the metadata CSV file.")
    parser.add_argument("output/csv/path.csv", help="Path to the output CSV file to be created.")

    args = parser.parse_args()

    ''' Test directories to run in a Python IDE (For testing and bug-fixing purposes only
    # .txt file with names of all prophages
    all_prophages_names = "/Users/bensakdinan/Desktop/prophage_induction/Code/test_all_prophage_names.txt"
    # .xlsx file with all prophages, their prophage-host_ratio, and the corresponding sample
    all_prophages_file_path = "/Users/bensakdinan/Desktop/prophage_induction/Code/test_all_prophage_data.csv"
    # .xlsx file with one row per sample name, and all corresponding metadata, namely Dehydration_Status
    metadata_file_path = "/Users/bensakdinan/Desktop/prophage_induction/00_metadata.csv"
    # output directory for .csv output
    output_csv_path = "/Users/bensakdinan/Desktop/prophage_induction/prophages_by_dehydration.csv"
    '''

    # Run main method
    prophages_by_dehydration(
        args.all_prophages_names,
        args.all_prophages_file_path,
        args.metadata_file_path,
        args.output_csv_path
    )
