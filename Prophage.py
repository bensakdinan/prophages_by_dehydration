#!/usr/bin/env python3
import pandas as pd


class Prophage:
    """
    def __init__(self, identifier, nt_length, start_nucleotide, end_nucleotide):
        self.identifier = identifier
        self.nt_length = nt_length
        self.start_nucleotide = start_nucleotide
        self.end_nucleotide = end_nucleotide
        self.samples_present = []
    """

    def __init__(self, identifier):
        self.identifier = identifier
        self.samples_present = []

    def __str__(self):
        return "Prophage: " + str(self.identifier) + "Found in samples: " + str(self.samples_present)

    def add_samples(self, all_prophages_file_path):
        other_samples = self.find_other_samples(all_prophages_file_path)
        for sample in other_samples:
            self.samples_present.append(sample)

    def find_other_samples(self, all_prophages_file_path):
        """ I need to write this method to go through my all_prophages_file_path.xlsx file to
        find every instance of the current (self) prophage and add the current sample name to self.samples_present.
        Every row in this file is a prophage and has a row named 'Sample' that has the name of the sample that
        prophage is found in. Find every instance of self.prophage in this csv file and add the sample names
        to all_other_samples"""
        all_other_samples = []
        try:
            df = pd.read_csv(all_prophages_file_path)
            print(df.head())
            print(df.columns)
            for _, row in df.iterrows():
                all_other_samples.append(row['Sample'])
            return all_other_samples

        except FileNotFoundError:
            print(f"File not found: {all_prophages_file_path}")
        except KeyError as e:
            print(f"KeyError: Missing expected column in file: {e}")
        except Exception as e:
            print(f"Line 44: An error occurred: {e}")

        return all_other_samples

    def get_ratio(self, sampleID, file_path):
        """Returns the prophage-host ratio of the current (self)
        prophage in the given (sampleID) sample

        Takes as input a sample ID, and the path to that sample's
        propagate results file (will read propagate results to get
        """
        try:
            data = pd.read_csv(file_path)

            # Check if the prophage is present in sample ID
            if sampleID in self.samples_present:
                row = data.loc[data['Sample'] == sampleID]
                if not row.empty:
                    prophage_host_ratio = row['prophage-host_ratio'].values[0]
                    return prophage_host_ratio
                else:
                    return f"Error in get_ratio, {sampleID} not found in excel data"
            # If the prophage is not present in the given sample
            else:
                return f"{sampleID} does not contain prophage: {self.identifier}"

        # Exceptions/bugs not to do with missing sampleID or prophage
        except FileNotFoundError:
            return f"Excel file at {file_path} not found."
        except KeyError as e:
            return f"Column {e} not found in the Excel file."
        except Exception as e:
            return f"Line 76: An error occurred: {str(e)}"

    def get_ratios_by_dehydration(self, all_prophages_file_path, metadata_file_path):
        """For the given prophage, returns a list of 3 dictionaries.
        3 dictionaries per dehydration status,"Mild", "Moderate", or "Severe",
        and the values are any and all prophage-host ratios observed at that
        dehydration status """

        result = {'Mild': [], 'Moderate': [], 'Severe': []}
        try:
            """samples_with_prophage = []
            df = pd.read_excel(all_prophages_file_path)
            for _, row in df.iterrows():
                # Check if the current row contains this prophage
                if self.identifier in row.values:
                    # Add the corresponding sample name to the list
                    samples_with_prophage.append(row['Sample']) """
            for sample in self.samples_present:

                ###
                # I need to check that all_prophages_file_path is going to get the right ratio, since this file
                # will have ALL the prophages in it. Make sure that I am indexing by sample
                ###
                current_ratio = self.get_ratio(sample, all_prophages_file_path)

                # Checking that get_ratio() didn't fail
                if isinstance(current_ratio, str):
                    return ("Error occurred in get_ratio method, get_ratios_by_dehydration was given argument of type "
                            "str()")
                # Go to the metadata to find the dehydration severity of the sample (will be done for every sample
                # with current phage in it)
                else:
                    metadata_df = pd.read_csv(metadata_file_path)
                    sample_metadata = metadata_df[metadata_df['Sample'] == sample]
                    if not sample_metadata.empty:
                        if sample_metadata['Dehydration_Status'].iloc[0] == 'Mild' \
                                or sample_metadata['Dehydration_Status'].iloc[0] == '1' \
                                or sample_metadata['Dehydration_Status'].iloc[0] == 1:
                            result['Mild'].append(current_ratio)
                        elif sample_metadata['Dehydration_Status'].iloc[0] == 'Moderate' \
                                or sample_metadata['Dehydration_Status'].iloc[0] == '2' \
                                or sample_metadata['Dehydration_Status'].iloc[0] == 2:
                            result['Moderate'].append(current_ratio)
                        elif sample_metadata['Dehydration_Status'].iloc[0] == 'Severe' \
                                or sample_metadata['Dehydration_Status'].iloc[0] == '3' \
                                or sample_metadata['Dehydration_Status'].iloc[0] == 3:
                            result['Severe'].append(current_ratio)
                        else:
                            return "Error in get_ratios_by_dehydration(), no key for mild, moderate, or severe found"
                    else:
                        return "sample_metadata dataframe is empty"
        # Exceptions
        except FileNotFoundError:
            return f"Excel file at {all_prophages_file_path} or {metadata_file_path} not found."
        except Exception as e:
            print(f"Line 131: An error occurred: {e}")
