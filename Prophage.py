#!/usr/bin/env python3
import pandas as pd


class Prophage:
    def __init__(self, identifier):
        self.identifier = identifier.strip()
        self.samples_present = []

    def __str__(self):
        return "Prophage: " + str(self.identifier) + "Found in samples: " + str(self.samples_present)

    def add_samples(self, all_prophages_file_path):
        """
        Populate the samples_present list attribute for the current prophage,
        by finding all samples in the given file where the current prophage is present.
        """
        try:
            df = pd.read_csv(all_prophages_file_path)

            # Check that all_prophages_file_path has the required columns
            if 'Prophage' not in df.columns or 'Sample' not in df.columns:
                raise KeyError("Columns 'Prophage' and 'Sample' are required in the CSV file.")

            # Ensure columns are of type string and strip whitespaces
            df['Prophage'] = df['Prophage'].astype(str).str.strip()
            self.identifier = self.identifier.strip()

            # Filter rows matching the current prophage identifier
            matching_rows = df[df['Prophage'] == self.identifier]

            # Add matching samples to the current Prophage instance samples_present list
            self.samples_present = matching_rows['Sample'].astype(str).str.strip().tolist()

        # Exception handling not to do with missing data in all_prophages_file_path
        except FileNotFoundError:
            print(f"File not found: {all_prophages_file_path}")
        except KeyError as e:
            print(f"KeyError: Missing expected column in file: {e}")
        except Exception as e:
            print(f"An error occurred in add_samples: {e}")

    def get_ratio(self, sampleID, all_prophages_file_path):
        """Returns the prophage-host ratio of the current (self)
        prophage in the given (sampleID) sample

        Takes as input a sample ID, and the path to that sample's
        propagate results file (will read propagate results to get
        """
        try:
            data = pd.read_csv(all_prophages_file_path)

            # Check if the sampleID is a sample that contains the current prophage
            if sampleID in self.samples_present:

                # Ensure data in all_prophages_file_path is of type string and remove whitespaces
                data['Sample'] = data['Sample'].astype(str).str.strip()
                sampleID = sampleID.strip()

                # Filter data to only include data from sampleID that contains the current prophage
                row = data.loc[(data['Sample'] == sampleID) & (data['Prophage'] == self.identifier)]

                # Check that filtered data exists, then get prophage:host read ratio
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
            return f"Excel file at {all_prophages_file_path} not found."
        except KeyError as e:
            return f"Column {e} not found in the Excel file."
        except Exception as e:
            return f"Line 76: An error occurred: {str(e)}"

    def get_ratios_by_dehydration(self, all_prophages_file_path, metadata_file_path):
        """ Returns a dictionary that contains all the prophage:host read ratios
        existing for the current prophage, at their corresponding levels of
        dehydration severity.
        """
        result = {'Mild': [], 'Moderate': [], 'Severe': []}
        try:
            # Iterate through all samples that the current prophage is present in
            for sample in self.samples_present:

                # Get prophage:host read ratio
                current_ratio = self.get_ratio(sample, all_prophages_file_path)
                metadata_df = pd.read_csv(metadata_file_path)

                # Check that the current sample exists in the metadata file
                if 'Sample' not in metadata_df.columns or 'Dehydration_Status' not in metadata_df.columns:
                    raise KeyError("Metadata must have 'Sample' and 'Dehydration_Status' columns.")

                # Ensure that metadata sample names are of type string and strip whitespaces
                sample_metadata = metadata_df[metadata_df['Sample'].str.strip() == sample.strip()]

                # Ensure that data exists for the current sample
                if sample_metadata.empty:
                    print(f"No metadata found for sample: {sample}")
                    continue

                # Find the associated dehydration status of the current sample (that contains the current prophage)
                # Assign the current prophage:host read ratio value to the correct dehydration status
                dehydration_status = sample_metadata['Dehydration_Status'].iloc[0]
                if dehydration_status in ['Mild', '1', 1]:
                    result['Mild'].append(current_ratio)
                elif dehydration_status in ['Moderate', '2', 2]:
                    result['Moderate'].append(current_ratio)
                elif dehydration_status in ['Severe', '3', 3]:
                    result['Severe'].append(current_ratio)
                else:
                    print(f"Unknown dehydration status for sample {sample}: {dehydration_status}")

        # Exceptions for errors not to do with missing data in metadata_file_path
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except KeyError as e:
            print(f"KeyError: {e}")
        except Exception as e:
            print(f"An error occurred in get_ratios_by_dehydration: {e}")
        return result
